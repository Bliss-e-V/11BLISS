

import requests

from flask import Flask, request
from get_distance import get_grid_times
from config import MAPS_API_KEY

app = Flask(__name__)


@app.route("/geocoding", methods=["GET"])
def geocoding():
    """
    Params:
    - search: string URL encoded address to search for
    Returns:
    - JSON response from the Google Geocoding API
    """

    print(request.args)
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
def gridtimes():
    """
    Params:
    - start_lat: Latitude of the starting point
    - start_long: Longitude of the starting point
    - top_left_lat: Latitude of the top left grid point
    - top_left_long: Longitude of the top left grid point
    - bottom_right_lat: Latitude of the bottom right grid point
    - bottom_right_long: Longitude of the bottom right point
    - num_steps: Resolution of the grid
    Returns:
    - List of Triples containing (Latitude, Longitude, time from start)
    """

    start_lat = float(request.args["start_lat"])
    start_long = float(request.args["start_long"])
    top_left_lat = float(request.args["top_left_lat"])
    top_left_long = float(request.args["top_left_long"])
    bottom_right_lat = float(request.args["bottom_right_lat"])
    bottom_right_long = float(request.args["bottom_right_long"])
    num_steps = int(request.args["num_steps"])

    times = get_grid_times(
        start_lat,
        start_long,
        top_left_lat,
        top_left_long,
        bottom_right_lat,
        bottom_right_long,
        num_steps,
    )

    return (times, 200)
