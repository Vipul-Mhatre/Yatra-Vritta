# airline_back.py (Modified to use pyflightdata instead of opensky_api)

import os
import io
import time
import datetime
import pandas as pd

from flask import Flask, request, jsonify

# NEW: import pyflightdata (unofficial FlightRadar24 scraper)
try:
    from pyflightdata import FlightData
except ImportError:
    raise ImportError("Please install pyflightdata first: pip install pyflightdata")

app = Flask(__name__)

# ------------------------------------------------------------------------------
# 1. Load 'airports.csv' into a DataFrame
# ------------------------------------------------------------------------------
AIRPORTS_CSV_FILE = "airports.csv"

try:
    airports_df = pd.read_csv(AIRPORTS_CSV_FILE, delimiter='\t')
except:
    airports_df = pd.read_csv(AIRPORTS_CSV_FILE)

# Replace missing data with 'NA' to keep consistent
airports_df = airports_df.fillna("NA")

# ------------------------------------------------------------------------------
# 2. Initialize pyflightdata
# ------------------------------------------------------------------------------
# No username/password needed, because it scrapes public data.
flight_data = FlightData()

# ------------------------------------------------------------------------------
# 3. Helper: parse date/time strings to epoch
#    (Kept from your original code, even though pyflightdata doesn't use times)
# ------------------------------------------------------------------------------
def parse_time(tstr):
    if not tstr:
        return 0
    try:
        return int(tstr)  # user provided an epoch
    except:
        # Assume an ISO date/time string
        dt = datetime.datetime.fromisoformat(tstr)
        return int(dt.timestamp())

# ------------------------------------------------------------------------------
# 4. Multi-Step Filtering Endpoints for Airports (unchanged)
# ------------------------------------------------------------------------------
@app.route('/airports/continents', methods=['GET'])
def get_continents():
    df = airports_df.copy()
    continents = sorted(df['continent'].unique().tolist())
    return jsonify(continents), 200

@app.route('/airports/countries', methods=['GET'])
def get_countries_by_continent():
    continent = request.args.get('continent', '').strip()
    if not continent:
        return jsonify({"error": "Please provide 'continent' parameter"}), 400

    df = airports_df.copy()
    df = df[df['continent'] == continent]
    countries = sorted(df['iso_country'].unique().tolist())
    return jsonify(countries), 200

@app.route('/airports/regions', methods=['GET'])
def get_regions():
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
    continent = request.args.get('continent', '').strip()
    iso_country = request.args.get('iso_country', '').strip()
    iso_region = request.args.get('iso_region', '').strip()

    if not continent or not iso_country or not iso_region:
        return jsonify({"error": "Please provide 'continent', 'iso_country', and 'iso_region'"}), 400

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

@app.route('/airports', methods=['GET'])
def get_airports():
    df = airports_df.copy()
    result = df.to_dict(orient='records')
    return jsonify(result), 200

# ------------------------------------------------------------------------------
# 5. ARRIVALS by airport (pyflightdata)
# ------------------------------------------------------------------------------
@app.route('/flights/arrivals', methods=['GET'])
def get_arrivals():
    """
    GET /flights/arrivals?airport=CDG
    Ignores 'begin' and 'end' because pyflightdata doesn't support time-based arrivals.
    """
    airport = request.args.get('airport', '').strip()
    if not airport:
        return jsonify({"error": "Missing 'airport' param"}), 400

    try:
        # For FlightRadar24, the "airport" param is typically an IATA code (e.g. 'CDG', 'LHR').
        # We call flight_data.get_airport_arrivals(...) ignoring times.
        arrivals = flight_data.get_airport_arrivals(airport)
        if not arrivals:
            return jsonify({"status": "error", "message": "No arrivals found"}), 200

        # Each item might have keys like 'flight', 'airline', 'time', etc.
        # We'll convert them to a consistent format
        result = []
        for arr in arrivals:
            result.append({
                "flight": arr.get("flight", ""),
                "airline": arr.get("airline", ""),
                "time_scheduled": arr.get("time", {}).get("scheduled", ""),
                "time_real": arr.get("time", {}).get("real", ""),
                "airport_from": arr.get("airport", {}).get("origin", ""),
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------------------------------------------------------------
# 6. DEPARTURES by airport (pyflightdata)
# ------------------------------------------------------------------------------
@app.route('/flights/departures', methods=['GET'])
def get_departures():
    """
    GET /flights/departures?airport=CDG
    Ignores 'begin' and 'end' because pyflightdata doesn't support time-based departures.
    """
    airport = request.args.get('airport', '').strip()
    if not airport:
        return jsonify({"error": "Missing 'airport' param"}), 400

    try:
        departures = flight_data.get_airport_departures(airport)
        if not departures:
            return jsonify({"status": "error", "message": "No departures found"}), 200

        result = []
        for dep in departures:
            result.append({
                "flight": dep.get("flight", ""),
                "airline": dep.get("airline", ""),
                "time_scheduled": dep.get("time", {}).get("scheduled", ""),
                "time_real": dep.get("time", {}).get("real", ""),
                "airport_to": dep.get("airport", {}).get("destination", ""),
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------------------------------------------------------------
# 7. Flights by "aircraft" (really flight # in pyflightdata)
# ------------------------------------------------------------------------------
@app.route('/flights/aircraft', methods=['GET'])
def get_flights_by_aircraft():
    """
    GET /flights/aircraft?flight=BA123
    We can't do icao24 in pyflightdata. So we adapt to flight number (ex: 'BA123').
    'begin' and 'end' are ignored as well.
    """
    flight = request.args.get('flight', '').strip()  # changed from 'icao24'
    if not flight:
        return jsonify({"error": "Missing or invalid 'flight' param"}), 400

    try:
        # pyflightdata method: get_history_by_flight_number(...)
        flt_history = flight_data.get_history_by_flight_number(flight)
        if not flt_history:
            return jsonify({"status": "error", "message": "No flight data returned"}), 200

        # Build a result set from flight data
        # Each item might have keys like 'status', 'airport', 'airline', 'flight', ...
        result = []
        for item in flt_history:
            result.append({
                "flight_number": item.get("flight", ""),
                "status": item.get("status", ""),
                "airport_from": item.get("airport", {}).get("origin", ""),
                "airport_to": item.get("airport", {}).get("destination", ""),
                "airline": item.get("airline", ""),
                "time_scheduled": item.get("time", {}).get("scheduled", {}),
                "time_real": item.get("time", {}).get("real", {}),
            })
        return jsonify({"status": "success", "count": len(result), "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------------------------------------------------------------
# 8. Flights by time interval (no direct pyflightdata support -> stub)
# ------------------------------------------------------------------------------
@app.route('/flights/interval', methods=['GET'])
def get_flights_by_interval():
    """
    GET /flights/interval?begin=...&end=...
    Not supported by pyflightdata. We return a placeholder or empty data.
    """
    begin = parse_time(request.args.get('begin', '0'))
    end = parse_time(request.args.get('end', '0'))

    # Just return a stub response
    return jsonify({
        "status": "error",
        "message": "Not supported by pyflightdata. No real-time interval-based data.",
        "begin": begin,
        "end": end
    }), 200

# ------------------------------------------------------------------------------
# 9. Track by "aircraft" (No direct real-time track in pyflightdata -> stub)
# ------------------------------------------------------------------------------
@app.route('/flights/track', methods=['GET'])
def get_track_by_aircraft():
    """
    GET /flights/track?icao24=...&t=0
    There's no direct track-by-ICAO24 in pyflightdata. Return a stub.
    """
    icao24 = request.args.get('icao24', '').strip()
    t_param = request.args.get('t', '0').strip()

    # Return a placeholder
    return jsonify({
        "status": "error",
        "message": "pyflightdata does not provide real-time track by icao24. No data.",
        "icao24_requested": icao24,
        "time_requested": t_param
    }), 200

# ------------------------------------------------------------------------------
# 10. Run the Flask app
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
