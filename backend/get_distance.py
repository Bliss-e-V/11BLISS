import math
from typing import Dict, List, Tuple

import googlemaps
import numpy as np
import requests
import csv
from googlemaps import Client
from config import MAPS_API_KEY

gmaps: Client = googlemaps.Client(key=MAPS_API_KEY)
GMAPS_CHUNK_SIZE: int = 99


def tuple_to_dict(lat, long):
    return {
        "latitude": lat,
        "longitude": long,
    }


def get_time_for_dests(
    start: Dict[str, float],
    destinations: List[Dict[str, float]],
    time: str = "2024-04-03T12:00:00Z",
) -> List[Tuple[float, float, int]]:
    chunks = math.ceil(len(destinations) / GMAPS_CHUNK_SIZE)

    lat_long_time_list = []
    for i in range(chunks):
        current_destinations = destinations[
            i * GMAPS_CHUNK_SIZE : (i + 1) * GMAPS_CHUNK_SIZE
        ]
        req = {
            "origins": [
                {
                    "waypoint": {
                        "location": {
                            "latLng": {
                                "latitude": start["latitude"],
                                "longitude": start["longitude"],
                            }
                        }
                    }
                }
            ],
            "destinations": [
                {
                    "waypoint": {
                        "location": {
                            "latLng": {
                                "latitude": dest["latitude"],
                                "longitude": dest["longitude"],
                            }
                        }
                    }
                }
                for dest in current_destinations
            ],
            "travelMode": "TRANSIT",
            "departureTime": time,
        }

        url = f"https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix?key={MAPS_API_KEY}"
        header = {"X-Goog-FieldMask": "duration,destinationIndex"}

        response = requests.post(url=url, json=req, headers=header)
        if response.status_code != 200:
            print(f"Got response {response.status_code} with body {response.json()}")
        response = response.json()

        # for dest, res in zip(current_destinations, response):
        for res in response:
            if not ("duration" in res and "destinationIndex" in res):
                print(f"Warning: Empty response.")
                continue
            dest = current_destinations[res["destinationIndex"]]

            duration = int(res["duration"][:-1])
            lat_long_time_list.append((dest["latitude"], dest["longitude"], duration))

    return lat_long_time_list


# LONG = X
# LAT = Y
def build_grid(
    top_left: Dict[str, float],
    bottom_right: Dict[str, float],
    num_steps: int,
):
    # construct missing points
    top_right: Dict[str, float] = {
        "longitude": bottom_right["longitude"],
        "latitude": top_left["latitude"],
    }

    bottom_left: Dict[str, float] = {
        "longitude": top_left["longitude"],
        "latitude": bottom_right["latitude"],
    }

    # get lengths
    delta_x = top_right["longitude"] - top_left["longitude"]
    delta_y = top_left["latitude"] - bottom_left["latitude"]
    assert delta_x > 0, delta_y > 0

    assert bottom_left["longitude"] < bottom_right["longitude"]
    assert bottom_left["latitude"] < top_left["latitude"]
    x_list = np.linspace(bottom_left["longitude"], bottom_right["longitude"], num_steps)
    y_list = np.linspace(bottom_left["latitude"], top_left["latitude"], num_steps)

    longs, lats = np.meshgrid(x_list, y_list)
    grid = list(zip(lats.ravel(), longs.ravel()))

    d = [{"latitude": lat, "longitude": lon} for lat, lon in grid]

    return d


def load_grid(path="../data/grid.csv"):

    loaded_grid = []

    with open(path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        # Iterate over the rows and append data to the list
        for row in reader:
            loaded_grid.append(tuple_to_dict(float(row[0]), float(row[1])))

    return loaded_grid


def get_grid_times(
    start_lat,
    start_long,
):
    start = tuple_to_dict(start_lat, start_long)

    grid_points = load_grid()

    times = get_time_for_dests(start, grid_points)

    return times
