import googlemaps
from googlemaps import Client
import numpy as np
import requests
from typing import Tuple, List, Dict

from main import MAPS_API_KEY


gmaps: Client = googlemaps.Client(key=MAPS_API_KEY)


def get_time_for_dests(
    start: Dict[str, float], destinations: List[Dict[str, float]], time: str = "2024-04-03T12:00:00Z"
) -> List[Tuple[float, float, int]]:

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
            for dest in destinations
        ],
        "travelMode": "TRANSIT",
        "departureTime": time,
    }

    url = f"https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix?key={KEY}"
    header = {
        "X-Goog-FieldMask": "duration"
    }

    response = requests.post(url=url, json=req, headers=header)
    assert response.status_code == 200, f"Got response {response.status_code}"
    response = response.json()
    print(response)
    
    d = []
    for dest, res in zip(destinations, response):
        
        if not 'duration' in res:
            print(f"Empty response for {dest}.")
            continue

        duration = int(res['duration'][:-1])
        d.append((dest['latitude'], dest['longitude'], duration))

    return d


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


def get_grid_times(start_lat, start_long, top_left_lat, top_left_long, bottom_right_lat, bottom_right_long, num_steps):

    start = {
        "longitude": start_long,
        "latitude": start_lat,
    }

    top_left = {
        "longitude": top_left_long,
        "latitude": top_left_lat,
    }

    bottom_right = {
        "longitude": bottom_right_long,
        "latitude": bottom_right_lat,
    }

    grid_points = build_grid(top_left, bottom_right, num_steps=num_steps)
    print("len", len(grid_points))

    times = get_time_for_dests(start, grid_points)

    return times
