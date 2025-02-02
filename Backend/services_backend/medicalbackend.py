# backend.py
from flask import Flask, jsonify, request
import pandas as pd
import joblib
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import json
import os
from flask_cors import CORS

# Initialize Flask and Dash
server = Flask(__name__)
CORS(server)
app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Load artifacts
model_path = os.path.join(os.path.dirname(__file__), 'models')
model = joblib.load(os.path.join(model_path, 'medical_tourism_model.pkl'))
scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
df = pd.read_pickle(os.path.join(model_path, 'cities_df.pkl'))

features = [
    'Hospital Beds per 1,000',
    'Health Spending per Capita (USD)',
    'GDP per Capita (USD)',
    'Tourist Arrivals per Year',
    'Ease of Doing Business Score',
    'Safety Index (Homicide Rate)'
]

# Dashboard layout
app.layout = html.Div([
    html.H1('Medical Tourism Dashboard', className='title'),
    
    html.Div([
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
                html.H3('Healthcare Infrastructure'),
                dcc.Graph(id='healthcare-chart')
            ], className='chart-section'),
            
            html.Div([
                html.H3('Cost Analysis'),
                dcc.Graph(id='cost-analysis')
            ], className='chart-section'),
            
            html.Div([
                html.H3('Safety Comparison'),
                dcc.Graph(id='safety-comparison')
            ], className='chart-section'),
            
            html.Div([
                html.H3('Top Recommendations'),
                html.Div(id='recommendations-table')
            ], className='recommendations-section')
        ], className='dashboard-content')
    ], className='main-container')
], className='dashboard')

# Add custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Medical Tourism Dashboard</title>
        {%css%}
        <style>
            .dashboard {
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .title {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
            }
            .dropdown-container {
                display: flex;
                gap: 20px;
                margin-bottom: 30px;
            }
            .metrics-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .chart-section {
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .recommendations-section {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
        {%scripts%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

@server.route('/countries', methods=['GET'])
def get_countries():
    countries = df['countrycode'].dropna().unique().tolist()
    return jsonify({'countries': sorted(countries)})

@server.route('/cities', methods=['GET'])
def get_cities():
    country = request.args.get('country')
    cities = df[df['countrycode'] == country]['name'].unique().tolist()
    return jsonify({'cities': sorted(cities)})

def create_metric_card(title, value, trend=None):
    trend_element = html.Div([
        html.Span(f"{trend}%"),
        html.I(className=f"fas fa-arrow-{'up' if trend > 0 else 'down'}")
    ], className='trend') if trend is not None else None
    
    return html.Div([
        html.H4(title),
        html.Div([
            html.Span(value),
            trend_element
        ])
    ], className='metric-card')

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
     Output('healthcare-chart', 'figure'),
     Output('cost-analysis', 'figure'),
     Output('safety-comparison', 'figure'),
     Output('recommendations-table', 'children')],
    [Input('country-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_dashboard(country, city):
    if not country or not city:
        return [], {}, {}, {}, []
    
    # Get city data and recommendations
    city_data = df[(df['name'] == city) & (df['countrycode'] == country)]
    X_city = city_data[features]
    X_scaled = scaler.transform(X_city)
    distances, indices = model.kneighbors(X_scaled)
    recommendations = df.iloc[indices[0][1:]]
    
    # Create metrics cards
    metrics = [
        create_metric_card(
            'Tourism Score',
            f"{city_data['Medical Tourism Score'].iloc[0]:.1f}",
            5.2
        ),
        create_metric_card(
            'Healthcare Index',
            f"{city_data['Hospital Beds per 1,000'].iloc[0]:.1f}",
            3.1
        ),
        create_metric_card(
            'Safety Score',
            f"{city_data['Safety Index (Homicide Rate)'].iloc[0]:.1f}",
            1.8
        )
    ]
    
    # Create healthcare infrastructure chart
    healthcare_fig = go.Figure()
    healthcare_fig.add_trace(go.Bar(
        x=recommendations['name'],
        y=recommendations['Hospital Beds per 1,000'],
        name='Hospital Beds'
    ))
    healthcare_fig.update_layout(
        title='Healthcare Infrastructure Comparison',
        height=400
    )
    
    # Create cost analysis chart
    cost_fig = px.scatter(
        recommendations,
        x='Health Spending per Capita (USD)',
        y='Medical Tourism Score',
        size='GDP per Capita (USD)',
        hover_data=['name'],
        title='Cost vs Quality Analysis'
    )
    cost_fig.update_layout(height=400)
    
    # Create safety comparison chart
    safety_fig = go.Figure()
    safety_fig.add_trace(go.Scatter(
        x=recommendations['name'],
        y=recommendations['Safety Index (Homicide Rate)'],
        mode='lines+markers',
        name='Safety Index'
    ))
    safety_fig.update_layout(
        title='Safety Index Comparison',
        height=400
    )
    
    # Create recommendations table
    recommendations_table = html.Table([
        html.Thead(
            html.Tr([
                html.Th('City'),
                html.Th('Country'),
                html.Th('Tourism Score'),
                html.Th('Healthcare Index'),
                html.Th('Safety Score')
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td(row['name']),
                html.Td(row['countrycode']),
                html.Td(f"{row['Medical Tourism Score']:.1f}"),
                html.Td(f"{row['Hospital Beds per 1,000']:.1f}"),
                html.Td(f"{row['Safety Index (Homicide Rate)']:.1f}")
            ]) for _, row in recommendations.head(5).iterrows()
        ])
    ], className='recommendations-table')
    
    return metrics, healthcare_fig, cost_fig, safety_fig, recommendations_table

@server.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    city_name = data['city']
    country_code = data['country']
    
    # Find city data
    city_data = df[(df['name'] == city_name) & 
                   (df['countrycode'] == country_code)]
    
    if city_data.empty:
        return jsonify({'error': 'City not found'}), 404
    
    # Get recommendations and create visualizations
    X_city = city_data[features]
    X_scaled = scaler.transform(X_city)
    distances, indices = model.kneighbors(X_scaled)
    recommendations = df.iloc[indices[0][1:]]
    recommendations = recommendations.sort_values('Medical Tourism Score', 
                                               ascending=False)
    
    # Prepare dashboard data
    dashboard_data = {
        'selected': city_data.iloc[0][[
            'name', 'countrycode', 'Medical Tourism Score'] + features
        ].to_dict(),
        'recommendations': recommendations.head(20).to_dict('records'),
        'visualizations': {
            'healthcare': create_healthcare_visualization(city_data, recommendations),
            'cost': create_cost_visualization(city_data, recommendations),
            'safety': create_safety_visualization(city_data, recommendations)
        }
    }
    
    return jsonify(dashboard_data)

def create_healthcare_visualization(city_data, recommendations):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=recommendations['name'],
        y=recommendations['Hospital Beds per 1,000'],
        name='Hospital Beds'
    ))
    return json.loads(fig.to_json())

def create_cost_visualization(city_data, recommendations):
    fig = px.scatter(
        recommendations,
        x='Health Spending per Capita (USD)',
        y='Medical Tourism Score',
        size='GDP per Capita (USD)',
        hover_data=['name']
    )
    return json.loads(fig.to_json())

def create_safety_visualization(city_data, recommendations):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recommendations['name'],
        y=recommendations['Safety Index (Homicide Rate)'],
        mode='lines+markers'
    ))
    return json.loads(fig.to_json())

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)