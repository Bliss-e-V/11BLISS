import os

import requests
from flask import Flask, request
from flask_cors import CORS

from config import GMAPS_API_KEY
from get_distance import GeoPoint, compute_geo_point_grid

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

    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?key={GMAPS_API_KEY}&address={search}"

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

    average_mode = request.args.get("average_mode", "max")
    if not (average_mode == "max" or average_mode == "average"):
        return "Invalid average_mode argument", 400

    starts = request.args.get("starts")
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
                starts = tuple([GeoPoint(start[0], start[1]) for start in starts])
                geo_point_grid = compute_geo_point_grid(starts, average_mode)
                return (geo_point_grid, 200)

            else:
                return "Invalid starts argument", 400
        except Exception as e:
            return f"Error: {e}", 400
    else:
        return "No starts argument provided", 400
