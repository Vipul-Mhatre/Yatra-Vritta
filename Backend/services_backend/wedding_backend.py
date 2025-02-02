# destination_wedding_backend.py
from flask import Flask, jsonify, request
import pandas as pd
import joblib
import os
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
from flask_cors import CORS
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Initialize Flask & Dash
server = Flask(__name__)
CORS(server)
app = Dash(__name__, server=server, url_base_pathname='/wedding_dashboard/')

# Load Model & Data
model_path = os.path.join(os.path.dirname(__file__), 'models_wedding')
if not os.path.exists(model_path):
    os.makedirs(model_path)

df = pd.read_csv('destination_wedding_ranking.csv')

# Handle missing values
df = df.dropna(subset=['countrycode'])

# Define features for ranking
features = [
    'Ease of Business Score',
    'GDP per Capita (USD)',
    'International Air Passengers',
    'Tourist Arrivals (millions)',
    'Safety Index (Low Crime Rate)',
    'Destination Wedding Score'
]

# Normalize features
scaler = StandardScaler()
X = df[features]
X_scaled = scaler.fit_transform(X)

# Compute weighted ranking score
weights = [0.2, 0.2, 0.15, 0.15, 0.15, 0.15]
df['City Ranking Score'] = (X_scaled * weights).sum(axis=1)

# Train KNN model
model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='brute')
model.fit(X_scaled)

# Save model & scaler
joblib.dump(model, os.path.join(model_path, 'wedding_ranking_model.pkl'))
joblib.dump(scaler, os.path.join(model_path, 'scaler.pkl'))
df.to_pickle(os.path.join(model_path, 'wedding_cities_df.pkl'))

print("Destination Wedding Model training completed!")

# Dashboard Layout
app.layout = html.Div([
    html.H1('Destination Wedding Planner', className='title'),

    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': i, 'value': i} for i in sorted(df['countrycode'].unique())],
            placeholder='Select a Country'
        ),
        dcc.Dropdown(
            id='city-dropdown',
            placeholder='Select a City'
        ),
    ], className='dropdown-container'),

    html.Div([
        html.Div([
            html.H3('Key Metrics'),
            html.Div(id='key-metrics', className='metrics-container')
        ], className='metrics-section'),

        html.Div([
            html.H3('Destination Popularity'),
            dcc.Graph(id='tourist-arrivals-chart')
        ], className='chart-section'),

        html.Div([
            html.H3('Safety Analysis'),
            dcc.Graph(id='safety-comparison')
        ], className='chart-section'),

        html.Div([
            html.H3('Top Wedding Destination Recommendations'),
            html.Div(id='recommendations-table')
        ], className='recommendations-section')
    ], className='dashboard-content')
], className='dashboard')

# Flask API Endpoints
@server.route('/countries', methods=['GET'])
def get_countries():
    countries = df['countrycode'].dropna().unique().tolist()
    return jsonify({'countries': sorted(countries)})

@server.route('/cities', methods=['GET'])
def get_cities():
    country = request.args.get('country')
    cities = df[df['countrycode'] == country]['name'].unique().tolist()
    return jsonify({'cities': sorted(cities)})

@server.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    city_name = data['city']
    country_code = data['country']

    city_data = df[(df['name'] == city_name) & (df['countrycode'] == country_code)]

    if city_data.empty:
        return jsonify({'error': 'City not found'}), 404

    # Get recommendations using KNN
    X_city = city_data[features]
    X_scaled = scaler.transform(X_city)
    distances, indices = model.kneighbors(X_scaled)
    recommendations = df.iloc[indices[0][1:]]

    # Sort recommendations by wedding score
    recommendations = recommendations.sort_values('Destination Wedding Score', ascending=False)

    return jsonify({
        'selected': city_data.iloc[0][['name', 'countrycode', 'Destination Wedding Score'] + features].to_dict(),
        'recommendations': recommendations.head(10).to_dict('records')
    })

# Dashboard Callbacks
@app.callback(
    Output('city-dropdown', 'options'),
    Input('country-dropdown', 'value')
)
def update_cities(country):
    if not country:
        return []
    cities = df[df['countrycode'] == country]['name'].unique()
    return [{'label': i, 'value': i} for i in sorted(cities)]

@app.callback(
    [Output('key-metrics', 'children'),
     Output('tourist-arrivals-chart', 'figure'),
     Output('safety-comparison', 'figure'),
     Output('recommendations-table', 'children')],
    [Input('country-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_dashboard(country, city):
    if not country or not city:
        return [], {}, {}, []

    city_data = df[(df['name'] == city) & (df['countrycode'] == country)]
    X_city = city_data[features]
    X_scaled = scaler.transform(X_city)
    distances, indices = model.kneighbors(X_scaled)
    recommendations = df.iloc[indices[0][1:]]

    # Metrics
    metrics = [
        html.Div(f"Wedding Score: {city_data['Destination Wedding Score'].iloc[0]:.2f}", className='metric-card'),
        html.Div(f"Safety Index: {city_data['Safety Index (Low Crime Rate)'].iloc[0]:.2f}", className='metric-card')
    ]

    # Tourist Arrivals Chart
    tourist_fig = px.bar(
        recommendations,
        x='name',
        y='Tourist Arrivals (millions)',
        title='Tourist Arrivals per Destination'
    )

    # Safety Comparison Chart
    safety_fig = px.scatter(
        recommendations,
        x='Safety Index (Low Crime Rate)',
        y='Destination Wedding Score',
        title='Safety vs Wedding Score'
    )

    # Recommendations Table
    recommendations_table = html.Table([
        html.Thead(html.Tr([html.Th('City'), html.Th('Country'), html.Th('Wedding Score')])),
        html.Tbody([html.Tr([html.Td(row['name']), html.Td(row['countrycode']), html.Td(f"{row['Destination Wedding Score']:.2f}")]) for _, row in recommendations.iterrows()])
    ])

    return metrics, tourist_fig, safety_fig, recommendations_table

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
