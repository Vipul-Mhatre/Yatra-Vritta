# backend.py
from flask import Flask, jsonify, request
import pandas as pd
import joblib
import os
from flask_cors import CORS

# Initialize Flask
server = Flask(__name__)
CORS(server)

# Load artifacts
model_path = os.path.join(os.path.dirname(__file__), 'models_mice')
model = joblib.load(os.path.join(model_path, 'city_ranking_model.pkl'))
scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
df = pd.read_pickle(os.path.join(model_path, 'cities_df.pkl'))

# Updated features list
features = [
    'Ease of Doing Business Score',
    'GDP per Capita (USD)',
    'International Air Passengers',
    'Tourist Arrivals',
    'Safety Index (Homicide Rate)',
    'MICE Score'
]

@server.route('/countries', methods=['GET'])
def get_countries():
    """ Return a list of available countries. """
    countries = df['countrycode'].dropna().unique().tolist()
    return jsonify({'countries': sorted(countries)})

@server.route('/cities', methods=['GET'])
def get_cities():
    """ Return a list of cities for a given country. """
    country = request.args.get('country')
    cities = df[df['countrycode'] == country]['name'].unique().tolist()
    return jsonify({'cities': sorted(cities)})

@server.route('/recommend', methods=['POST'])
def recommend():
    """ Return recommendations for a selected city. """
    data = request.json
    city_name = data['city']
    country_code = data['country']

    # Find city data
    city_data = df[(df['name'] == city_name) & (df['countrycode'] == country_code)]

    if city_data.empty:
        return jsonify({'error': 'City not found'}), 404

    # Get recommendations based on KNN
    X_city = city_data[features]
    X_scaled = scaler.transform(X_city)
    distances, indices = model.kneighbors(X_scaled)
    recommendations = df.iloc[indices[0][1:]]
    
    recommendations = recommendations.sort_values('MICE Score', ascending=False)

    # Prepare response data
    dashboard_data = {
        'selected': city_data.iloc[0][['name', 'countrycode', 'MICE Score'] + features].to_dict(),
        'recommendations': recommendations.head(20).to_dict('records')
    }

    return jsonify(dashboard_data)

if __name__ == '__main__':
    server.run(debug=True, port=5000)
