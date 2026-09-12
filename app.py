from flask import Flask, render_template, redirect, url_for
import os
from dotenv import load_dotenv

# Make the Flask app object
app = Flask(__name__)


# Constants
load_dotenv()   # read .env into environment
DEF_LAT = os.getenv("DEF_LAT", "32.89") # Read in, otherwise show DFW airport
DEF_LONG = os.getenv("DEF_LONG", "-97.04")


# Landing page
@app.route("/")
def index():
    return render_template("index.html")

# Redirect from landing to map viewer page
@app.route("/map")
def map_viewer():
    return render_template("map.html", def_lat=DEF_LAT, def_long=DEF_LONG)


# Run the app on whatever host at port 8008
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)