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

matplotlib.use('Agg')  # Use non-interactive backend for Matplotlib

# Initialize Flask
app = Flask(__name__)

# Initialize Overpass API
api = overpy.Overpass()

# Define categories (used in /process endpoint)
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

# Create output directory if not exists
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Load cities CSV (ensure the file is present)
cities_file = "cities_lat_long_geonamescache_with_countries.csv"
try:
    cities_data = pd.read_csv(cities_file, encoding='utf-8')
except UnicodeDecodeError:
    cities_data = pd.read_csv(cities_file, encoding='ISO-8859-1')
except Exception as e:
    raise ValueError(f"Failed to load the file: {e}")

# ---------------------------
# Helper Functions
# ---------------------------

def fetch_overpass_data(center_point, radius, tags):
    """
    Fetch Overpass data for given tags around a center_point (lat, lon).
    """
    results = []
    lat, lon = center_point
    for tag in tags:
        query = f"""
        (
          node{tag}(around:{radius},{lat},{lon});
          way{tag}(around:{radius},{lat},{lon});
          relation{tag}(around:{radius},{lat},{lon});
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
    """
    Process Overpass results into a GeoDataFrame.
    Only includes features with a valid geometry.
    """
    points = []
    for result in results:
        for node in result.nodes:
            geom = Point(float(node.lon), float(node.lat))
            # Only add if geometry is valid
            if geom is not None:
                points.append({
                    "name": node.tags.get("name", "Unnamed Location"),
                    "category": category,
                    "geometry": geom,
                })
        for way in result.ways:
            try:
                pts = [(float(n.lon), float(n.lat)) for n in way.nodes]
                geom = Polygon(pts) if len(pts) > 2 else None
                if geom is not None:
                    points.append({
                        "name": way.tags.get("name", "Unnamed Location"),
                        "category": category,
                        "geometry": geom,
                    })
            except Exception as e:
                print(f"Skipping way {way.id}: {e}")
    # Filter out any items without a valid geometry (defensive creation)
    valid_points = [pt for pt in points if pt.get("geometry") is not None]
    return gpd.GeoDataFrame(valid_points, crs="EPSG:4326")

def generate_recommendations(gdf, category):
    """
    Generate recommendations from a GeoDataFrame.
    """
    recommendations = []
    if not gdf.empty:
        df_named = gdf[gdf['name'] != "Unnamed Location"]
        df_sorted = df_named.sort_values(by="name")
        for _, row in df_sorted.head(5).iterrows():
            recommendations.append({
                "name": row["name"],
                "category": row.get("category", category),
                "description": f"Highly recommended {category} spot: {row['name']}."
            })
    if not recommendations:
        recommendations.append({
            "name": "No recommendations available",
            "category": category,
            "description": "Try expanding your search radius or choose a different category."
        })
    return recommendations

def generate_recommendations_from_list(data_list, item_type):
    """
    Generate recommendations from a list of dictionaries.
    """
    recommendations = []
    filtered = [item for item in data_list if item.get("name") not in [None, "N/A", "Unnamed Location"]]
    filtered.sort(key=lambda x: x["name"])
    for item in filtered[:5]:
        recommendations.append({
            "name": item["name"],
            "item_type": item_type,
            "description": f"Recommended {item_type}: {item['name']}."
        })
    if not recommendations:
        recommendations.append({
            "name": "No recommendations available",
            "item_type": item_type,
            "description": "Insufficient data to generate recommendations. Consider expanding your search radius."
        })
    return recommendations

# ---------------------------
# Universal Endpoints
# ---------------------------
@app.route('/countries', methods=['GET'])
def get_countries():
    countries = cities_data['Country'].unique().tolist()
    return jsonify(countries)

@app.route('/cities', methods=['POST'])
def get_cities():
    data = request.json
    selected_country = data.get("country")
    if not selected_country:
        return jsonify({"error": "No country provided"}), 400
    cities = cities_data[cities_data['Country'] == selected_country]['City'].unique().tolist()
    return jsonify(cities)

@app.route('/process', methods=['POST'])
def process_data():
    """
    Process a city feature request for the City Feature Explorer.
    Returns CSV, GeoJSON, a static plot, a Folium map, and recommendations.
    """
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

    # Save output files
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
    # When creating the map GeoDataFrame, filter out items without valid geometry:
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} for feat in [
        {"name": row["name"], "geometry": row["geometry"]} for row in gdf.itertuples(index=False)
    ] if feat.get("geometry") is not None]
    # (Alternatively, our gdf already contains valid geometries.)
    for _, row in gdf.iterrows():
        if row.geometry:
            if isinstance(row.geometry, Point):
                folium.Marker(location=(row.geometry.y, row.geometry.x),
                              popup=row["name"],
                              tooltip=category.capitalize()).add_to(m)
            elif isinstance(row.geometry, Polygon):
                folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except Exception:
        html_content = None
    recs = generate_recommendations(gdf, category)
    return jsonify({
        "csv_file": csv_file,
        "geojson_file": geojson_file,
        "plot_file": plot_file,
        "map_file": map_file,
        "map_content": html_content,
        "recommendations": recs
    })

@app.route('/download', methods=['GET'])
def download_file():
    file_path = request.args.get("file_path")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

# ---------------------------
# HOTEL ENDPOINTS
# ---------------------------
def fetch_hotels_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["tourism"="hotel"](around:{radius},{lat},{lon});
      node["amenity"~"^(hotel|motel|guest_house|hostel)$"](around:{radius},{lat},{lon});
      way["tourism"="hotel"](around:{radius},{lat},{lon});
      way["amenity"~"^(hotel|motel|guest_house|hostel)$"](around:{radius},{lat},{lon});
      relation["tourism"="hotel"](around:{radius},{lat},{lon});
      relation["amenity"~"^(hotel|motel|guest_house|hostel)$"](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching hotel data: {e}")
        return None

@app.route('/hotels/search', methods=['GET'])
def hotels_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Please provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_hotels_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    hotels_list = []
    geo_features = []
    for node in osm_result.nodes:
        hotel_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        hotel_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        hotel_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    # Defensive creation: only include features with valid geometry
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"hotels_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="Hotel").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(hotels_list, "Hotel")
    return jsonify({
        "status": "success",
        "count": len(hotels_list),
        "data": hotels_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

@app.route('/hotels/details/<path:hotel_id>', methods=['GET'])
def hotels_details(hotel_id):
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Please provide city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "City/Country not found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_hotels_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "error", "message": "Hotel not found"}), 404
    try:
        h_type, h_osm_id = hotel_id.split('/')
        h_osm_id = int(h_osm_id)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid hotel_id format"}), 400
    matched_item = None
    if h_type == "node":
        for node in osm_result.nodes:
            if node.id == h_osm_id:
                matched_item = node
                break
    elif h_type == "way":
        for way in osm_result.ways:
            if way.id == h_osm_id:
                matched_item = way
                break
    elif h_type == "relation":
        for rel in osm_result.relations:
            if rel.id == h_osm_id:
                matched_item = rel
                break
    else:
        return jsonify({"status": "error", "message": "Unknown OSM element type"}), 400
    if not matched_item:
        return jsonify({"status": "error", "message": "Hotel not found"}), 404
    if h_type == "node":
        name = matched_item.tags.get("name", "N/A")
        lat_ = float(matched_item.lat)
        lon_ = float(matched_item.lon)
        tags_ = dict(matched_item.tags)
    elif h_type == "way":
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    else:
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    return jsonify({
        "status": "success",
        "data": {
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        }
    })

@app.route('/hotels/book', methods=['POST'])
def hotels_book():
    data = request.get_json()
    if not data or "hotel_id" not in data:
        return jsonify({"status": "error", "message": "Missing hotel_id in request body."}), 400
    booking_id = "BOOK-" + data["hotel_id"].replace('/', '-')
    return jsonify({
        "status": "success",
        "message": "Booking confirmed",
        "booking_id": booking_id,
        "details": data
    })

@app.route('/hotels/cancel', methods=['POST'])
def hotels_cancel():
    data = request.get_json()
    if not data or "booking_id" not in data:
        return jsonify({"status": "error", "message": "Missing booking_id in request body."}), 400
    return jsonify({
        "status": "success",
        "message": "Booking cancelled",
        "booking_id": data["booking_id"]
    })

# ---------------------------
# SIGHTSEEING ENDPOINTS
# ---------------------------
def fetch_sightseeing_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["tourism"~"^(attraction|museum|theme_park|zoo)$"](around:{radius},{lat},{lon});
      node["amenity"~"^(arts_centre|gallery|cinema)$"](around:{radius},{lat},{lon});
      node["historic"~"^(monument|archaeological_site)$"](around:{radius},{lat},{lon});
      way["tourism"~"^(attraction|museum|theme_park|zoo)$"](around:{radius},{lat},{lon});
      way["amenity"~"^(arts_centre|gallery|cinema)$"](around:{radius},{lat},{lon});
      way["historic"~"^(monument|archaeological_site)$"](around:{radius},{lat},{lon});
      relation["tourism"~"^(attraction|museum|theme_park|zoo)$"](around:{radius},{lat},{lon});
      relation["amenity"~"^(arts_centre|gallery|cinema)$"](around:{radius},{lat},{lon});
      relation["historic"~"^(monument|archaeological_site)$"](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching sightseeing data: {e}")
        return None

@app.route('/sightseeing/search', methods=['GET'])
def sightseeing_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_sightseeing_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    sightseeing_list = []
    geo_features = []
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    # Defensive creation: include only features with valid geometry
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"sightseeing_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="Sightseeing").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(sightseeing_list, "Sightseeing")
    return jsonify({
        "status": "success",
        "count": len(sightseeing_list),
        "data": sightseeing_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

@app.route('/sightseeing/details/<path:sightseeing_id>', methods=['GET'])
def sightseeing_details(sightseeing_id):
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "City/Country not found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_sightseeing_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "error", "message": "Sightseeing spot not found"}), 404
    try:
        s_type, s_osm_id = sightseeing_id.split('/')
        s_osm_id = int(s_osm_id)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid sightseeing_id format"}), 400
    matched_item = None
    if s_type == "node":
        for node in osm_result.nodes:
            if node.id == s_osm_id:
                matched_item = node
                break
    elif s_type == "way":
        for way in osm_result.ways:
            if way.id == s_osm_id:
                matched_item = way
                break
    elif s_type == "relation":
        for rel in osm_result.relations:
            if rel.id == s_osm_id:
                matched_item = rel
                break
    else:
        return jsonify({"status": "error", "message": "Unknown OSM element type"}), 400
    if not matched_item:
        return jsonify({"status": "error", "message": "Sightseeing spot not found"}), 404
    if s_type == "node":
        name = matched_item.tags.get("name", "N/A")
        lat_ = float(matched_item.lat)
        lon_ = float(matched_item.lon)
        tags_ = dict(matched_item.tags)
    elif s_type == "way":
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    else:
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    return jsonify({
        "status": "success",
        "data": {
            "sightseeing_id": sightseeing_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        }
    })

@app.route('/sightseeing/book', methods=['POST'])
def sightseeing_book():
    data = request.get_json()
    if not data or "sightseeing_id" not in data:
        return jsonify({"status": "error", "message": "Missing sightseeing_id in request."}), 400
    booking_id = "BOOK-SIGHT-" + data["sightseeing_id"].replace('/', '-')
    return jsonify({
        "status": "success",
        "message": "Sightseeing booking confirmed",
        "booking_id": booking_id,
        "details": data
    })

@app.route('/sightseeing/cancel', methods=['POST'])
def sightseeing_cancel():
    data = request.get_json()
    if not data or "booking_id" not in data:
        return jsonify({"status": "error", "message": "Missing booking_id in request."}), 400
    return jsonify({
        "status": "success",
        "message": "Sightseeing booking cancelled",
        "booking_id": data["booking_id"]
    })

# ---------------------------
# AIRPORT ENDPOINTS
# ---------------------------
def fetch_airports_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["aeroway"="airport"](around:{radius},{lat},{lon});
      way["aeroway"="airport"](around:{radius},{lat},{lon});
      relation["aeroway"="airport"](around:{radius},{lat},{lon});
      node["aeroway"="helipad"](around:{radius},{lat},{lon});
      way["aeroway"="helipad"](around:{radius},{lat},{lon});
      relation["aeroway"="helipad"](around:{radius},{lat},{lon});
      node["aeroway"="aerodrome"](around:{radius},{lat},{lon});
      way["aeroway"="aerodrome"](around:{radius},{lat},{lon});
      relation["aeroway"="aerodrome"](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching airport data: {e}")
        return None

@app.route('/airports/search', methods=['GET'])
def airports_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_airports_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    airports_list = []
    geo_features = []
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        airports_list.append({
            "airport_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        airports_list.append({
            "airport_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        airports_list.append({
            "airport_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    # Defensive creation: only include features with valid geometry
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"airports_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="Airport/Airfield").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(airports_list, "Airport/Airfield")
    return jsonify({
        "status": "success",
        "count": len(airports_list),
        "data": airports_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

@app.route('/airports/details/<path:airport_id>', methods=['GET'])
def airports_details(airport_id):
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "City/Country not found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_airports_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "error", "message": "Airport/Airfield not found"}), 404
    try:
        a_type, a_osm_id = airport_id.split('/')
        a_osm_id = int(a_osm_id)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid airport_id format"}), 400
    matched_item = None
    if a_type == "node":
        for node in osm_result.nodes:
            if node.id == a_osm_id:
                matched_item = node
                break
    elif a_type == "way":
        for way in osm_result.ways:
            if way.id == a_osm_id:
                matched_item = way
                break
    elif a_type == "relation":
        for rel in osm_result.relations:
            if rel.id == a_osm_id:
                matched_item = rel
                break
    else:
        return jsonify({"status": "error", "message": "Unknown OSM element type"}), 400
    if not matched_item:
        return jsonify({"status": "error", "message": "Airport/Airfield not found"}), 404
    if a_type == "node":
        name = matched_item.tags.get("name", "N/A")
        lat_ = float(matched_item.lat)
        lon_ = float(matched_item.lon)
        tags_ = dict(matched_item.tags)
    elif a_type == "way":
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    else:
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    return jsonify({
        "status": "success",
        "data": {
            "airport_id": airport_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        }
    })

# ---------------------------
# AIRLINE ENDPOINTS
# ---------------------------
def fetch_airlines_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["operator"~"Airlines", i](around:{radius},{lat},{lon});
      way["operator"~"Airlines", i](around:{radius},{lat},{lon});
      relation["operator"~"Airlines", i](around:{radius},{lat},{lon});
      node["name"~"Airlines", i](around:{radius},{lat},{lon});
      way["name"~"Airlines", i](around:{radius},{lat},{lon});
      relation["name"~"Airlines", i](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching airline data: {e}")
        return None

@app.route('/airlines/search', methods=['GET'])
def airlines_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_airlines_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    airlines_list = []
    geo_features = []
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        airlines_list.append({
            "airline_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        airlines_list.append({
            "airline_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        airlines_list.append({
            "airline_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"airlines_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="Airline").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(airlines_list, "Airline")
    return jsonify({
        "status": "success",
        "count": len(airlines_list),
        "data": airlines_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

@app.route('/airlines/details/<path:airline_id>', methods=['GET'])
def airlines_details(airline_id):
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "City/Country not found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_airlines_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "error", "message": "Airline not found"}), 404
    try:
        a_type, a_osm_id = airline_id.split('/')
        a_osm_id = int(a_osm_id)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid airline_id format"}), 400
    matched_item = None
    if a_type == "node":
        for node in osm_result.nodes:
            if node.id == a_osm_id:
                matched_item = node
                break
    elif a_type == "way":
        for way in osm_result.ways:
            if way.id == a_osm_id:
                matched_item = way
                break
    elif a_type == "relation":
        for rel in osm_result.relations:
            if rel.id == a_osm_id:
                matched_item = rel
                break
    else:
        return jsonify({"status": "error", "message": "Unknown OSM element type"}), 400
    if not matched_item:
        return jsonify({"status": "error", "message": "Airline not found"}), 404
    if a_type == "node":
        name = matched_item.tags.get("name", "N/A")
        lat_ = float(matched_item.lat)
        lon_ = float(matched_item.lon)
        tags_ = dict(matched_item.tags)
    elif a_type == "way":
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    else:
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)
    return jsonify({
        "status": "success",
        "data": {
            "airline_id": airline_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        }
    })

@app.route('/airlines/book', methods=['POST'])
def airlines_book():
    data = request.get_json()
    if not data or "airline_id" not in data:
        return jsonify({"status": "error", "message": "Missing airline_id in request."}), 400
    booking_id = "BOOK-AIR-" + data["airline_id"].replace('/', '-')
    return jsonify({
        "status": "success",
        "message": "Airline booking confirmed",
        "booking_id": booking_id,
        "details": data
    })

@app.route('/airlines/cancel', methods=['POST'])
def airlines_cancel():
    data = request.get_json()
    if not data or "booking_id" not in data:
        return jsonify({"status": "error", "message": "Missing booking_id in request."}), 400
    return jsonify({
        "status": "success",
        "message": "Airline booking cancelled",
        "booking_id": data["booking_id"]
    })

# ---------------------------
# MEDICAL TOURISM ENDPOINTS
# ---------------------------
def fetch_medical_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["amenity"="doctors"](around:{radius},{lat},{lon});
      node["amenity"="pharmacy"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="clinic"](around:{radius},{lat},{lon});
      way["amenity"="doctors"](around:{radius},{lat},{lon});
      way["amenity"="pharmacy"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="clinic"](around:{radius},{lat},{lon});
      relation["amenity"="doctors"](around:{radius},{lat},{lon});
      relation["amenity"="pharmacy"](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching medical data: {e}")
        return None

@app.route('/medical/search', methods=['GET'])
def medical_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_medical_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    medical_list = []
    geo_features = []
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        medical_list.append({
            "medical_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        medical_list.append({
            "medical_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        medical_list.append({
            "medical_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"medical_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="Medical Facility").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(medical_list, "Medical Facility")
    return jsonify({
        "status": "success",
        "count": len(medical_list),
        "data": medical_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

# ---------------------------
# MICE ENDPOINTS
# ---------------------------
def fetch_mice_overpy(lat, lon, radius=20000):
    query = f"""
    (
      node["amenity"="conference_centre"](around:{radius},{lat},{lon});
      node["amenity"="exhibition_centre"](around:{radius},{lat},{lon});
      node["amenity"="events_venue"](around:{radius},{lat},{lon});
      node["amenity"="theatre"](around:{radius},{lat},{lon});
      node["amenity"="parking"](around:{radius},{lat},{lon});
      node["amenity"="wifi"](around:{radius},{lat},{lon});
      node["amenity"="charging_station"](around:{radius},{lat},{lon});
      node["amenity"="atm"](around:{radius},{lat},{lon});
      node["amenity"="bank"](around:{radius},{lat},{lon});
      way["amenity"="conference_centre"](around:{radius},{lat},{lon});
      way["amenity"="exhibition_centre"](around:{radius},{lat},{lon});
      way["amenity"="events_venue"](around:{radius},{lat},{lon});
      way["amenity"="theatre"](around:{radius},{lat},{lon});
      way["amenity"="parking"](around:{radius},{lat},{lon});
      way["amenity"="wifi"](around:{radius},{lat},{lon});
      way["amenity"="charging_station"](around:{radius},{lat},{lon});
      way["amenity"="atm"](around:{radius},{lat},{lon});
      way["amenity"="bank"](around:{radius},{lat},{lon});
      relation["amenity"="conference_centre"](around:{radius},{lat},{lon});
      relation["amenity"="exhibition_centre"](around:{radius},{lat},{lon});
      relation["amenity"="events_venue"](around:{radius},{lat},{lon});
      relation["amenity"="theatre"](around:{radius},{lat},{lon});
      relation["amenity"="parking"](around:{radius},{lat},{lon});
      relation["amenity"="wifi"](around:{radius},{lat},{lon});
      relation["amenity"="charging_station"](around:{radius},{lat},{lon});
      relation["amenity"="atm"](around:{radius},{lat},{lon});
      relation["amenity"="bank"](around:{radius},{lat},{lon});
    );
    out center;
    >;
    out skel qt;
    """
    try:
        return api.query(query)
    except Exception as e:
        print(f"Error fetching MICE data: {e}")
        return None

@app.route('/mice/search', methods=['GET'])
def mice_search():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)
    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400
    if not city and not country:
        return jsonify({"status": "error", "message": "Provide at least city or country."}), 400
    place_filter = True
    if city:
        place_filter &= (cities_data['City'] == city)
    if country:
        place_filter &= (cities_data['Country'] == country)
    matched_places = cities_data[place_filter]
    if matched_places.empty:
        return jsonify({"status": "error", "message": "No matching city/country found"}), 404
    lat = matched_places.iloc[0]['Latitude']
    lon = matched_places.iloc[0]['Longitude']
    osm_result = fetch_mice_overpy(lat, lon, radius)
    if not osm_result:
        return jsonify({"status": "success", "count": 0, "data": []}), 200
    mice_list = []
    geo_features = []
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        mice_list.append({
            "mice_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(node.tags)
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if hasattr(way, 'center_lat') and way.center_lat else None
        lon_ = way.center_lon if hasattr(way, 'center_lon') and way.center_lon else None
        mice_list.append({
            "mice_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(way.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if hasattr(rel, 'center_lat') and rel.center_lat else None
        lon_ = rel.center_lon if hasattr(rel, 'center_lon') and rel.center_lon else None
        mice_list.append({
            "mice_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": dict(rel.tags)
        })
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
    gdf_data = [{"name": feat["name"], "geometry": feat["geometry"]} 
                for feat in geo_features if feat.get("geometry") is not None]
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")
    map_file = os.path.join(output_dir, f"mice_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(location=(row.geometry.y, row.geometry.x),
                          popup=row["name"],
                          tooltip="MICE Venue").add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)
    m.save(map_file)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except Exception:
        map_html = None
    recs = generate_recommendations_from_list(mice_list, "MICE Venue")
    return jsonify({
        "status": "success",
        "count": len(mice_list),
        "data": mice_list,
        "map_file": map_file,
        "map_content": map_html,
        "recommendations": recs
    })

# ---------------------------
# Run the Application
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
