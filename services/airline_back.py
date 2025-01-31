import os
import io
import time
import datetime
import pandas as pd
from flask import Flask, request, jsonify
from opensky_api import OpenSkyApi

app = Flask(__name__)

# -------------------------------------------------------------------
# 1. Load 'airports.csv' into a DataFrame
# -------------------------------------------------------------------
AIRPORTS_CSV_FILE = "airports.csv"

# Attempt to read with tab delimiter; fallback to default
try:
    airports_df = pd.read_csv(AIRPORTS_CSV_FILE, delimiter='\t')
except:
    airports_df = pd.read_csv(AIRPORTS_CSV_FILE)

# Instead of dropping missing data, we do not discard rows. 
# We only replace actual NaN with "NA" to keep data consistent.
airports_df = airports_df.fillna("NA")

# -------------------------------------------------------------------
# 2. Initialize OpenSkyApi (anonymous or with credentials)
# -------------------------------------------------------------------
OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME", "ronitmehta")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD", "india111")
api = OpenSkyApi(username=OPENSKY_USERNAME, password=OPENSKY_PASSWORD)

# -------------------------------------------------------------------
# 3. Helper: parse date/time strings to Unix epoch
# -------------------------------------------------------------------
def parse_time(tstr):
    """
    Takes a string that might be an integer epoch or an ISO date 'YYYY-MM-DD HH:MM'
    and returns an integer (epoch). Simplify or expand as needed.
    """
    if not tstr:
        return 0
    try:
        return int(tstr)  # user provided an epoch
    except:
        # Assume a date/time string
        dt = datetime.datetime.fromisoformat(tstr)  # e.g. '2023-01-25 12:30'
        return int(dt.timestamp())

# -------------------------------------------------------------------
# 4. Multi-Step Filtering Endpoints for Airports
# -------------------------------------------------------------------
@app.route('/airports/continents', methods=['GET'])
def get_continents():
    """
    Distinct list of all continents from the CSV (including "NA" or any text).
    GET /airports/continents
    """
    df = airports_df.copy()
    # Just get distinct values in 'continent' (which may be "NA" if that's how your CSV is)
    continents = sorted(df['continent'].unique().tolist())
    return jsonify(continents), 200

@app.route('/airports/countries', methods=['GET'])
def get_countries_by_continent():
    """
    GET /airports/countries?continent=...
    Returns distinct iso_country for the chosen continent (could be "NA" for the US).
    """
    continent = request.args.get('continent', '').strip()
    if not continent:
        return jsonify({"error": "Please provide 'continent' parameter"}), 400

    df = airports_df.copy()
    df = df[df['continent'] == continent]
    countries = sorted(df['iso_country'].unique().tolist())
    return jsonify(countries), 200

@app.route('/airports/regions', methods=['GET'])
def get_regions():
    """
    GET /airports/regions?continent=...&iso_country=...
    Returns distinct iso_region that match the chosen filters.
    """
    continent = request.args.get('continent', '').strip()
    iso_country = request.args.get('iso_country', '').strip()
    if not continent or not iso_country:
        return jsonify({"error": "Missing 'continent' or 'iso_country'"}), 400

    df = airports_df.copy()
    df = df[(df['continent'] == continent) & (df['iso_country'] == iso_country)]
    regions = sorted(df['iso_region'].unique().tolist())
    return jsonify(regions), 200

@app.route('/airports/municipalities', methods=['GET'])
def get_municipalities():
    """
    GET /airports/municipalities?continent=...&iso_country=...&iso_region=...
    Returns distinct municipalities that match the chosen filters.
    """
    continent = request.args.get('continent', '').strip()
    iso_country = request.args.get('iso_country', '').strip()
    iso_region = request.args.get('iso_region', '').strip()

    if not continent or not iso_country or not iso_region:
        return jsonify({"error": "Missing 'continent', 'iso_country', 'iso_region'"}), 400

    df = airports_df.copy()
    df = df[
        (df['continent'] == continent) &
        (df['iso_country'] == iso_country) &
        (df['iso_region'] == iso_region)
    ]
    municipalities = sorted(df['municipality'].unique().tolist())
    return jsonify(municipalities), 200

@app.route('/airports/filter', methods=['GET'])
def filter_airports():
    """
    GET /airports/filter?continent=...&iso_country=...&iso_region=...&municipality=...
    Returns fully filtered rows. Each param is optional. 
    If your CSV uses 'NA' for "North America", user must pass ?continent=NA to see US airports, etc.
    """
    df = airports_df.copy()

    cont = request.args.get('continent', '').strip()
    if cont:
        df = df[df['continent'] == cont]

    country = request.args.get('iso_country', '').strip()
    if country:
        df = df[df['iso_country'] == country]

    region = request.args.get('iso_region', '').strip()
    if region:
        df = df[df['iso_region'] == region]

    muni = request.args.get('municipality', '').strip()
    if muni:
        df = df[df['municipality'] == muni]

    result = df.to_dict(orient='records')
    return jsonify({"count": len(result), "data": result}), 200

# -------------------------------------------------------------------
# 5. 'GET /airports' Endpoint: return entire CSV
# -------------------------------------------------------------------
@app.route('/airports', methods=['GET'])
def get_airports():
    """
    GET /airports -> returns entire list from 'airports_df' in JSON.
    """
    df = airports_df.copy()
    result = df.to_dict(orient='records')
    return jsonify(result), 200

# -------------------------------------------------------------------
# 6. Arrivals by airport
# -------------------------------------------------------------------
@app.route('/flights/arrivals', methods=['GET'])
def get_arrivals():
    """
    GET /flights/arrivals?airport=EDDF&begin=1675075200&end=1675078800
    """
    airport = request.args.get('airport', '').strip()
    begin = parse_time(request.args.get('begin', '0'))
    end = parse_time(request.args.get('end', '0'))
    if not airport or not begin or not end:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    try:
        flights = api.get_arrivals_by_airport(airport, begin, end)
        print(flights)
        if flights is None:
            return jsonify({"status": "error", "message": "No data returned"}), 200
        result = []
        for f in flights:
            result.append({
                "icao24": f.icao24,
                "firstSeen": f.firstSeen,
                "estDepartureAirport": f.estDepartureAirport,
                "lastSeen": f.lastSeen,
                "estArrivalAirport": f.estArrivalAirport,
                "callsign": f.callsign,
                "departureAirportCandidatesCount": f.departureAirportCandidatesCount,
                "arrivalAirportCandidatesCount": f.arrivalAirportCandidatesCount
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------------------------------------------
# 7. Departures by airport
# -------------------------------------------------------------------
@app.route('/flights/departures', methods=['GET'])
def get_departures():
    """
    GET /flights/departures?airport=EDDF&begin=1675075200&end=1675078800
    """
    airport = request.args.get('airport', '').strip()
    begin = parse_time(request.args.get('begin', '0'))
    end = parse_time(request.args.get('end', '0'))
    if not airport or not begin or not end:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    try:
        flights = api.get_departures_by_airport(airport, begin, end)
        if flights is None:
            return jsonify({"status": "error", "message": "No data returned"}), 200
        result = []
        for f in flights:
            result.append({
                "icao24": f.icao24,
                "firstSeen": f.firstSeen,
                "estDepartureAirport": f.estDepartureAirport,
                "lastSeen": f.lastSeen,
                "estArrivalAirport": f.estArrivalAirport,
                "callsign": f.callsign,
                "departureAirportCandidatesCount": f.departureAirportCandidatesCount,
                "arrivalAirportCandidatesCount": f.arrivalAirportCandidatesCount
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------------------------------------------
# 8. Flights by aircraft
# -------------------------------------------------------------------
@app.route('/flights/aircraft', methods=['GET'])
def get_flights_by_aircraft():
    """
    GET /flights/aircraft?icao24=3c675a&begin=1674988800&end=1675075200
    """
    icao24 = request.args.get('icao24', '').strip().lower()
    begin = parse_time(request.args.get('begin', '0'))
    end = parse_time(request.args.get('end', '0'))
    if not icao24 or not begin or not end:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    try:
        flights = api.get_flights_by_aircraft(icao24, begin, end)
        if flights is None:
            return jsonify({"status": "error", "message": "No data returned"}), 200
        result = []
        for f in flights:
            result.append({
                "icao24": f.icao24,
                "firstSeen": f.firstSeen,
                "estDepartureAirport": f.estDepartureAirport,
                "lastSeen": f.lastSeen,
                "estArrivalAirport": f.estArrivalAirport,
                "callsign": f.callsign,
                "departureAirportCandidatesCount": f.departureAirportCandidatesCount,
                "arrivalAirportCandidatesCount": f.arrivalAirportCandidatesCount
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------------------------------------------
# 9. Flights by time interval
# -------------------------------------------------------------------
@app.route('/flights/interval', methods=['GET'])
def get_flights_by_interval():
    """
    GET /flights/interval?begin=1675075200&end=1675078800
    """
    begin = parse_time(request.args.get('begin', '0'))
    end = parse_time(request.args.get('end', '0'))
    if not begin or not end:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    try:
        flights = api.get_flights_from_interval(begin, end)
        if flights is None:
            return jsonify({"status": "error", "message": "No data returned"}), 200
        result = []
        for f in flights:
            result.append({
                "icao24": f.icao24,
                "firstSeen": f.firstSeen,
                "estDepartureAirport": f.estDepartureAirport,
                "lastSeen": f.lastSeen,
                "estArrivalAirport": f.estArrivalAirport,
                "callsign": f.callsign,
                "departureAirportCandidatesCount": f.departureAirportCandidatesCount,
                "arrivalAirportCandidatesCount": f.arrivalAirportCandidatesCount
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------------------------------------------
# 10. Track by aircraft
# -------------------------------------------------------------------
@app.route('/flights/track', methods=['GET'])
def get_track_by_aircraft():
    """
    GET /flights/track?icao24=3c4b26&t=0
    """
    icao24 = request.args.get('icao24', '').strip().lower()
    t_param = parse_time(request.args.get('t', '0'))
    if not icao24:
        return jsonify({"error": "Missing icao24"}), 400

    try:
        track = api.get_track_by_aircraft(icao24, t_param)
        if track is None:
            return jsonify({"status": "error", "message": "No track found"}), 200

        path = []
        for w in track.path:
            path.append({
                "time": w.time,
                "latitude": w.latitude,
                "longitude": w.longitude,
                "baro_altitude": w.baro_altitude,
                "true_track": w.true_track,
                "on_ground": w.on_ground
            })

        result = {
            "icao24": track.icao24,
            "startTime": track.startTime,
            "endTime": track.endTime,
            "callsign": track.callsign,
            "path": path
        }
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------------------------------------------------------
# 11. Run the Flask app
# -------------------------------------------------------------------
if __name__ == "__main__":
    # For quick local testing:
    # python back_opensky.py
    app.run(debug=True, port=5001)
