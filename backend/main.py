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
    Returns:
    - List of Triples containing (Latitude, Longitude, time from start)
    """

    start_lat = float(request.args["start_lat"])
    start_long = float(request.args["start_long"])

    times = get_grid_times(
        start_lat,
        start_long,
    )

    return (times, 200)
