import os

import requests
from flask import Flask, request
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
from get_distance import get_grid_times

from config import MAPS_API_KEY
from get_distance import get_grid_times

app = Flask(__name__)
CORS(app)


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@app.route("/geocoding", methods=["GET"])
def geocoding():
    """
    Params:
    - search: string URL encoded address to search for
    Returns:
    - JSON response from the Google Geocoding API
    """

    search = request.args["search"]

    if not search:
        # TODO: add proper error code
        return ("No argument provided.", 500)

    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?key={MAPS_API_KEY}&address={search}"

    response = requests.get(geocoding_url)

    if response.status_code != 200:
        return ("API Error.", response.status_code)

    return (response.json(), 200)


@app.route("/gridtimes", methods=["GET"])
def grid_times():
    """
    Params:
    - starts List[Tuple(float, float)]: Required. List of the latitude and longitude of the desired starting points.
        Supports up to 4 starting points.
    - average_mode str: Optional. Averaging mode used for the different distances from the start points.
        Supports 'max' and 'average'
    Returns:
    - List of Triples containing (Latitude, Longitude, time from start)
    """
    starts = request.args.get("starts")
    average_mode = request.args.get("average_mode", "max")

    if not (average_mode == "max" or average_mode == "average"):
        return "Invalid average_mode argument", 400

    if starts:
        try:
            print(starts)
            starts = eval(starts)
            # Convert the string representation of list of tuples to actual list of tuples
            if isinstance(starts, list) and all(
                isinstance(start, tuple)
                and len(start) == 2
                and all(isinstance(x, float) for x in start)
                for start in starts
            ):
                if len(starts) > 4 or len(starts) <= 0:
                    return "Invalid starts argument", 400
                starts = tuple(starts)
                times = get_grid_times(starts, average_mode)
                return (times, 200)

            else:
                return "Invalid starts argument", 400
        except Exception as e:
            return f"Error: {e}", 400
    else:
        return "No starts argument provided", 400
