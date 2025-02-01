from flask import Flask, request, jsonify, send_file
import overpy
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import folium
import matplotlib.pyplot as plt
import os
import matplotlib
import plotly.express as px

matplotlib.use('Agg') 

app = Flask(__name__)

api = overpy.Overpass()

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

cities_file = "cities_lat_long_geonamescache_with_countries.csv"

try:
    cities_data = pd.read_csv(cities_file, encoding='utf-8')
except UnicodeDecodeError:
    cities_data = pd.read_csv(cities_file, encoding='ISO-8859-1')
except Exception as e:
    raise ValueError(f"Failed to load the file: {e}")

categories = {
    "medical_tourism": [
        '["amenity"="hospital"]',
        '["amenity"="clinic"]',
        '["amenity"="pharmacy"]',
        '["amenity"="doctors"]',
        '["leisure"="spa"]',
        '["leisure"="fitness_centre"]',
        '["emergency"="ambulance_station"]',
        '["emergency"="fire_station"]',
    ],
    "mice": [
        '["amenity"="conference_centre"]',
        '["amenity"="exhibition_centre"]',
        '["amenity"="events_venue"]',
        '["amenity"="theatre"]',
        '["amenity"="parking"]',
        '["amenity"="wifi"]',
        '["amenity"="charging_station"]',
        '["amenity"="atm"]',
        '["amenity"="bank"]',
    ],
    "destination_weddings": [
        '["amenity"="place_of_worship"]',
        '["amenity"="events_venue"]',
        '["amenity"="toilets"]',
        '["amenity"="parking"]',
        '["leisure"="garden"]',
        '["shop"="bridal"]',
        '["shop"="gift"]',
        '["shop"="florist"]',
    ],
}

def fetch_overpass_data(center_point, radius, tags):
    results = []
    for tag in tags:
        query = f"""
        (
          node{tag}(around:{radius},{center_point[0]},{center_point[1]});
          way{tag}(around:{radius},{center_point[0]},{center_point[1]});
          relation{tag}(around:{radius},{center_point[0]},{center_point[1]});
        );
        out body;
        >;
        out skel qt;
        """
        try:
            result = api.query(query)
            results.append(result)
        except Exception as e:
            print(f"Error fetching data for tag {tag}: {e}")
    return results

def process_results(results, category):
    points = []
    for result in results:
        for node in result.nodes:
            points.append({
                "name": node.tags.get("name", "Unnamed Location"),
                "category": category,
                "geometry": Point(float(node.lon), float(node.lat)),
            })

        for way in result.ways:
            try:
                points_list = [(float(n.lon), float(n.lat)) for n in way.nodes]
                geometry = Polygon(points_list) if len(points_list) > 2 else None
                if geometry:
                    points.append({
                        "name": way.tags.get("name", "Unnamed Location"),
                        "category": category,
                        "geometry": geometry,
                    })
            except Exception as e:
                print(f"Skipping way {way.id} due to missing nodes: {e}")

    return gpd.GeoDataFrame(points, crs="EPSG:4326")

@app.route('/countries', methods=['GET'])
def get_countries():
    """Return the list of countries."""
    countries = cities_data['Country'].unique().tolist()
    return jsonify(countries)

@app.route('/cities', methods=['POST'])
def get_cities():
    """Return the list of cities for the selected country."""
    data = request.json
    selected_country = data.get("country")
    if not selected_country:
        return jsonify({"error": "No country provided"}), 400
    cities = cities_data[cities_data['Country'] == selected_country]['City'].unique().tolist()
    return jsonify(cities)

@app.route('/process', methods=['POST'])
def process_data():
    """Process the user request and generate output files."""
    data = request.json
    city_name = data.get("city")
    category = data.get("category")
    radius = data.get("radius", 100_000)

    if not (city_name and category):
        return jsonify({"error": "Missing required parameters"}), 400

    if category not in categories:
        return jsonify({"error": "Invalid category"}), 400

    city_data = cities_data[cities_data['City'] == city_name]
    if city_data.empty:
        return jsonify({"error": "City not found"}), 404

    lat, lon = city_data.iloc[0][['Latitude', 'Longitude']]
    tags = categories[category]
    center_point = (lat, lon)

    results = fetch_overpass_data(center_point, radius, tags)

    gdf = process_results(results, category)
    if gdf.empty:
        return jsonify({"error": "No data found"}), 404

    csv_file = os.path.join(output_dir, f"{category}_{city_name}.csv")
    geojson_file = os.path.join(output_dir, f"{category}_{city_name}.geojson")
    gdf.to_csv(csv_file, index=False)
    gdf.to_file(geojson_file, driver="GeoJSON")

    plot_file = os.path.join(output_dir, f"{category}_{city_name}_plot.png")
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color="blue", alpha=0.5, edgecolor="black")
    ax.set_title(f"{category.capitalize()} - {city_name}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.grid(True)
    plt.savefig(plot_file)
    plt.close(fig)

    map_file = os.path.join(output_dir, f"{category}_{city_name}_map.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(
                location=(row.geometry.y, row.geometry.x),
                popup=row["name"],
                tooltip=category.capitalize(),
            ).add_to(m)
    m.save(map_file)

    try:
        with open(map_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        with open(map_file, 'r', encoding='latin-1') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {map_file}")
        html_content = None

    return jsonify({
        "csv_file": csv_file,
        "geojson_file": geojson_file,
        "plot_file": plot_file,
        "map_file": map_file,
        "map_content": html_content 
    })

@app.route('/download', methods=['GET'])
def download_file():
    """Allow downloading of generated files."""
    file_path = request.args.get("file_path")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
