from flask import Flask, render_template, redirect, url_for, jsonify, request
import os
import logging
from dotenv import load_dotenv
from opensky_api import OpenSkyApi

# Make the Flask app object
app = Flask(__name__)

# Make Opensky Api object
api = OpenSkyApi()
logging.basicConfig(level=logging.INFO)


# Constants
load_dotenv()   # read .env into environment
DEF_LAT = os.getenv("DEF_LAT", "32.89") # Read in, otherwise show DFW airport
DEF_LONG = os.getenv("DEF_LONG", "-97.04")
FALLBACK_RADIU_DEG = 2.0


# Landing page
@app.route("/")
def index():
    return render_template("index.html")

# Redirect from landing to map viewer page
@app.route("/map")
def map_viewer():
    return render_template("map.html", def_lat=DEF_LAT, def_long=DEF_LONG)

# Opensky API call to get flight data within our defined bounding box
@app.route("/get-flights")
def get_flights():
    # Bounding box, based off env lat/long and zoom distance to populate all flights on screen map
    try:
        min_lat = float(request.args.get("min_lat", float(DEF_LAT) - FALLBACK_RADIU_DEG)) # Fall back if needed
        max_lat = float(request.args.get("max_lat", float(DEF_LAT) + FALLBACK_RADIU_DEG))
        min_lon = float(request.args.get("min_lon", float(DEF_LONG) - FALLBACK_RADIU_DEG))
        max_lon = float(request.args.get("max_lon", float(DEF_LONG) + FALLBACK_RADIU_DEG))
    except (TypeError, ValueError):
        return jsonify({"error": "min/max lat/lon must be numbers"}), 400

    # Tuple: [min_latitude, max_latitude, min_longitude, max_longitude] in WGS84 decminal degrees
    bbox = (min_lat, max_lat, min_lon, max_lon)
    
    # Returns a list of state vectors which have aircraft information such as callsign, origin, telem, etc
    try:
        s = api.get_states(bbox=bbox)
    except Exception as exc:
        logging.warning("OpenSky bbox request failed: %s", exc)
        return jsonify({"error:": "OpenSky bbox request failed", "flights": []}), 502
    
    # If we get an empty list/response, show the user there are no flights
    if s is None or not s.states:
        return jsonify({"count": 0, "flights": []})

    # Specifics we want to pull from that list of flight data
    flights = [
        {
            "icao24": sv.icao24,
            "callsign": (sv.callsign or "").strip(),
            "lat": sv.latitude,
            "lon": sv.longitude,
            "alt-meters": sv.geo_altitude,
            "heading": sv.true_track,
            "on_ground": sv.on_ground
        }
        for sv in s.states
    ]

    return jsonify({"count": len(flights), "flights": flights})


# Run the app on whatever host at port 8008
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)