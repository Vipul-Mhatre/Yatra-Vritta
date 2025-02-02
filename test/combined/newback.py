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

# Flask app initialization
app = Flask(__name__)

# Initialize Overpass API
api = overpy.Overpass()

# Directory for saving output files
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Load the cities CSV file with robust UTF-8 handling
cities_file = "cities_lat_long_geonamescache_with_countries.csv"

try:
    # Attempt to read the file with UTF-8 encoding
    cities_data = pd.read_csv(cities_file, encoding='utf-8')
except UnicodeDecodeError:
    # Fallback to ISO-8859-1 or similar encoding if UTF-8 fails
    cities_data = pd.read_csv(cities_file, encoding='ISO-8859-1')
except Exception as e:
    raise ValueError(f"Failed to load the file: {e}")

# ------------------------------------------------------------------------------
# Existing categories and endpoints
# ------------------------------------------------------------------------------
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
    """
    Helper function to fetch Overpass data for given tags around a center_point (lat, lon).
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
    Helper function to process Overpass results into a GeoDataFrame.
    """
    points = []
    for result in results:
        # Process nodes
        for node in result.nodes:
            points.append({
                "name": node.tags.get("name", "Unnamed Location"),
                "category": category,
                "geometry": Point(float(node.lon), float(node.lat)),
            })

        # Process ways (polygons/lines)
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
    """Process the user request for a specific category and generate output files (including Folium map)."""
    data = request.json
    city_name = data.get("city")
    category = data.get("category")
    radius = data.get("radius", 100_000)

    if not (city_name and category):
        return jsonify({"error": "Missing required parameters"}), 400

    if category not in categories:
        return jsonify({"error": "Invalid category"}), 400

    # Get city coordinates
    city_data = cities_data[cities_data['City'] == city_name]
    if city_data.empty:
        return jsonify({"error": "City not found"}), 404

    lat, lon = city_data.iloc[0][['Latitude', 'Longitude']]
    tags = categories[category]
    center_point = (lat, lon)

    # Fetch Overpass data
    results = fetch_overpass_data(center_point, radius, tags)

    # Process results into a GeoDataFrame
    gdf = process_results(results, category)
    if gdf.empty:
        return jsonify({"error": "No data found"}), 404

    # Save GeoDataFrame to file
    csv_file = os.path.join(output_dir, f"{category}_{city_name}.csv")
    geojson_file = os.path.join(output_dir, f"{category}_{city_name}.geojson")
    gdf.to_csv(csv_file, index=False)
    gdf.to_file(geojson_file, driver="GeoJSON")

    # Generate static plot
    plot_file = os.path.join(output_dir, f"{category}_{city_name}_plot.png")
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color="blue", alpha=0.5, edgecolor="black")
    ax.set_title(f"{category.capitalize()} - {city_name}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.grid(True)
    plt.savefig(plot_file)
    plt.close(fig)

    # Generate Folium map
    map_file = os.path.join(output_dir, f"{category}_{city_name}_map.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            folium.Marker(
                location=(row.geometry.y, row.geometry.x),
                popup=row["name"],
                tooltip=category.capitalize(),
            ).add_to(m)
        elif isinstance(row.geometry, Polygon):
            folium.GeoJson(row.geometry, name=row["name"]).add_to(m)

    m.save(map_file)

    # Read the saved map file with safe encoding
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
        "map_content": html_content  # Optionally include the HTML content
    })

@app.route('/download', methods=['GET'])
def download_file():
    """Allow downloading of generated files."""
    file_path = request.args.get("file_path")
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

# ------------------------------------------------------------------------------
# HOTEL ENDPOINTS (TBOH-like: search, details, book, cancel) + Folium
# ------------------------------------------------------------------------------
def fetch_hotels_overpy(lat, lon, radius=20000):
    """
    Fetch hotels around a coordinate using Overpy.
    'tourism=hotel' OR 'amenity'=hotel|motel|hostel|guest_house
    We'll request center geometry for ways/relations via 'out center;'.
    """
    query = f"""
    (
      node["tourism"="hotel"](around:{radius},{lat},{lon});
      node["amenity"~"^(hotel|motel|hostel|guest_house)$"](around:{radius},{lat},{lon});
      way["tourism"="hotel"](around:{radius},{lat},{lon});
      way["amenity"~"^(hotel|motel|hostel|guest_house)$"](around:{radius},{lat},{lon});
      relation["tourism"="hotel"](around:{radius},{lat},{lon});
      relation["amenity"~"^(hotel|motel|hostel|guest_house)$"](around:{radius},{lat},{lon});
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
    """
    Endpoint to search for hotels by city (and/or country) + optional radius.
    Example: GET /hotels/search?city=Paris&country=France&radius=30000
    Returns JSON list of hotels + a Folium map (HTML).
    """
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)  # default 20km

    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400

    if not city and not country:
        return jsonify({
            "status": "error",
            "message": "Please provide at least city or country."
        }), 400

    # Match city/country in the CSV
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

    # NODES
    for node in osm_result.nodes:
        hotel_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        tags_ = dict(node.tags)
        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # WAYS
    for way in osm_result.ways:
        hotel_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if way.center_lat else None
        lon_ = way.center_lon if way.center_lon else None
        tags_ = dict(way.tags)

        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })

        # Attempt polygon creation
        if len(way.nodes) >= 3:
            try:
                coords = [(float(n.lon), float(n.lat)) for n in way.nodes]
                poly_geom = Polygon(coords)
                geo_features.append({"name": name, "geometry": poly_geom})
            except Exception:
                if lat_ and lon_:
                    geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
        else:
            if lat_ and lon_:
                geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # RELATIONS
    for rel in osm_result.relations:
        hotel_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if rel.center_lat else None
        lon_ = rel.center_lon if rel.center_lon else None
        tags_ = dict(rel.tags)

        hotels_list.append({
            "hotel_id": hotel_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })

        # Typically rely on center coords
        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # Build Folium map
    gdf_data = []
    for feat in geo_features:
        gdf_data.append({"name": feat["name"], "geometry": feat["geometry"]})
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")

    map_file = os.path.join(output_dir, f"hotels_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        geom = row.geometry
        if isinstance(geom, Point):
            folium.Marker(
                location=(geom.y, geom.x),
                popup=row["name"],
                tooltip="Hotel"
            ).add_to(m)
        elif isinstance(geom, Polygon):
            folium.GeoJson(geom, name=row["name"]).add_to(m)
    m.save(map_file)

    # Read map HTML
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except UnicodeDecodeError:
        with open(map_file, 'r', encoding='latin-1') as f:
            map_html = f.read()
    except FileNotFoundError:
        map_html = None

    return jsonify({
        "status": "success",
        "count": len(hotels_list),
        "data": hotels_list,
        "map_file": map_file,
        "map_content": map_html
    }), 200

@app.route('/hotels/details/<path:hotel_id>', methods=['GET'])
def hotels_details(hotel_id):
    """
    Fetch details for a single hotel node/way/relation, re-querying Overpass.
    e.g. GET /hotels/details/node/12345?city=Paris
    """
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)

    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400

    if not city and not country:
        return jsonify({
            "status": "error",
            "message": "Please provide city or country to locate the hotel."
        }), 400

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

    # Build the details
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
    else:  # relation
        name = matched_item.tags.get("name", "N/A")
        lat_ = matched_item.center_lat if matched_item.center_lat else None
        lon_ = matched_item.center_lon if matched_item.center_lon else None
        tags_ = dict(matched_item.tags)

    response_data = {
        "hotel_id": hotel_id,
        "name": name,
        "lat": lat_,
        "lon": lon_,
        "tags": tags_
    }
    return jsonify({"status": "success", "data": response_data}), 200

@app.route('/hotels/book', methods=['POST'])
def hotels_book():
    """
    Mock booking endpoint for hotels.
    Expects JSON: {"hotel_id": "node/12345", "checkin_date": "...", ...}
    """
    data = request.get_json()
    if not data or "hotel_id" not in data:
        return jsonify({"status": "error", "message": "Missing 'hotel_id' in request body."}), 400

    booking_id = "BOOK-" + data["hotel_id"].replace('/', '-')
    return jsonify({
        "status": "success",
        "message": "Booking confirmed",
        "booking_id": booking_id,
        "details": data
    }), 200

@app.route('/hotels/cancel', methods=['POST'])
def hotels_cancel():
    """
    Mock cancellation endpoint for hotels.
    Expects JSON: {"booking_id": "BOOK-node-12345", ...}
    """
    data = request.get_json()
    if not data or "booking_id" not in data:
        return jsonify({"status": "error", "message": "Missing 'booking_id' in request body."}), 400

    return jsonify({
        "status": "success",
        "message": "Booking has been cancelled",
        "booking_id": data["booking_id"]
    }), 200

# ------------------------------------------------------------------------------
# NEW UNIVERSAL SIGHTSEEING ENDPOINTS (Similar to the hotel approach)
# ------------------------------------------------------------------------------
def fetch_sightseeing_overpy(lat, lon, radius=20000):
    """
    Fetch universal sightseeing spots around a coordinate using Overpy.
    For demonstration, let's combine typical 'tourism' features:
      - tourism=attraction, tourism=museum, tourism=theme_park, tourism=zoo
      - amenity=arts_centre, amenity=gallery, amenity=cinema
      - historic=monument, archaeological_site
    We'll also request center geometry for ways/relations via 'out center;'.
    """
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
    """
    Endpoint to search for sightseeing spots by city/country and optional radius.
    e.g. GET /sightseeing/search?city=Paris&country=France&radius=30000
    Returns JSON list + Folium map of attractions.
    """
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)

    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius value"}), 400

    if not city and not country:
        return jsonify({
            "status": "error",
            "message": "Please provide at least city or country."
        }), 400

    # Match city/country from the CSV
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

    # NODES
    for node in osm_result.nodes:
        item_id = f"node/{node.id}"
        name = node.tags.get("name", "N/A")
        lat_ = float(node.lat)
        lon_ = float(node.lon)
        tags_ = dict(node.tags)
        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })
        geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # WAYS
    for way in osm_result.ways:
        item_id = f"way/{way.id}"
        name = way.tags.get("name", "N/A")
        lat_ = way.center_lat if way.center_lat else None
        lon_ = way.center_lon if way.center_lon else None
        tags_ = dict(way.tags)

        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })

        # Attempt polygon creation
        if len(way.nodes) >= 3:
            try:
                coords = [(float(n.lon), float(n.lat)) for n in way.nodes]
                poly_geom = Polygon(coords)
                geo_features.append({"name": name, "geometry": poly_geom})
            except Exception:
                if lat_ and lon_:
                    geo_features.append({"name": name, "geometry": Point(lon_, lat_)})
        else:
            if lat_ and lon_:
                geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # RELATIONS
    for rel in osm_result.relations:
        item_id = f"relation/{rel.id}"
        name = rel.tags.get("name", "N/A")
        lat_ = rel.center_lat if rel.center_lat else None
        lon_ = rel.center_lon if rel.center_lon else None
        tags_ = dict(rel.tags)

        sightseeing_list.append({
            "sightseeing_id": item_id,
            "name": name,
            "lat": lat_,
            "lon": lon_,
            "tags": tags_
        })

        if lat_ and lon_:
            geo_features.append({"name": name, "geometry": Point(lon_, lat_)})

    # Build a Folium map
    gdf_data = []
    for feat in geo_features:
        gdf_data.append({"name": feat["name"], "geometry": feat["geometry"]})
    gdf = gpd.GeoDataFrame(gdf_data, crs="EPSG:4326")

    map_file = os.path.join(output_dir, f"sightseeing_map_{city or country}.html")
    m = folium.Map(location=[lat, lon], zoom_start=12)
    for _, row in gdf.iterrows():
        geom = row.geometry
        if isinstance(geom, Point):
            folium.Marker(
                location=(geom.y, geom.x),
                popup=row["name"],
                tooltip="Sightseeing"
            ).add_to(m)
        elif isinstance(geom, Polygon):
            folium.GeoJson(geom, name=row["name"]).add_to(m)
    m.save(map_file)

    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
    except UnicodeDecodeError:
        with open(map_file, 'r', encoding='latin-1') as f:
            map_html = f.read()
    except FileNotFoundError:
        map_html = None

    return jsonify({
        "status": "success",
        "count": len(sightseeing_list),
        "data": sightseeing_list,
        "map_file": map_file,
        "map_content": map_html
    }), 200

@app.route('/sightseeing/details/<path:sightseeing_id>', methods=['GET'])
def sightseeing_details(sightseeing_id):
    """
    Get details for a single sightseeing item: node/way/relation.
    e.g. GET /sightseeing/details/node/12345?city=Paris&radius=20000
    """
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '').strip()
    radius = request.args.get('radius', 20000)

    try:
        radius = int(radius)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid radius"}), 400

    if not city and not country:
        return jsonify({
            "status": "error",
            "message": "Please provide city or country to locate the sightseeing spot."
        }), 400

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

    # Build details
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

    response_data = {
        "sightseeing_id": sightseeing_id,
        "name": name,
        "lat": lat_,
        "lon": lon_,
        "tags": tags_
    }
    return jsonify({"status": "success", "data": response_data}), 200

@app.route('/sightseeing/book', methods=['POST'])
def sightseeing_book():
    """
    Mock booking endpoint for sightseeing.
    Expects JSON: {"sightseeing_id": "node/12345", "visit_date": "...", ...}
    """
    data = request.get_json()
    if not data or "sightseeing_id" not in data:
        return jsonify({"status": "error", "message": "Missing 'sightseeing_id' in request body."}), 400

    booking_id = "BOOK-SIGHT-" + data["sightseeing_id"].replace('/', '-')
    return jsonify({
        "status": "success",
        "message": "Sightseeing booking confirmed",
        "booking_id": booking_id,
        "details": data
    }), 200

@app.route('/sightseeing/cancel', methods=['POST'])
def sightseeing_cancel():
    """
    Mock cancellation endpoint for sightseeing bookings.
    Expects JSON: {"booking_id": "BOOK-SIGHT-node-12345", ...}
    """
    data = request.get_json()
    if not data or "booking_id" not in data:
        return jsonify({"status": "error", "message": "Missing 'booking_id' in request body."}), 400

    return jsonify({
        "status": "success",
        "message": "Sightseeing booking has been cancelled",
        "booking_id": data["booking_id"]
    }), 200

# ------------------------------------------------------------------------------
# Run the application
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
