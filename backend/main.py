import os
import requests

from flask import Flask, request
from pathlib import Path
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

MAPS_API_KEY = os.getenv("MAPS_API_KEY")


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
