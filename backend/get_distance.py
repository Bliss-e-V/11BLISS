import csv
import math
from collections import defaultdict
from enum import Enum
from typing import Dict, List, Tuple
from functools import lru_cache

import numpy as np
import requests

from config import MAPS_API_KEY

GMAPS_CHUNK_SIZE: int = 99


class GRID_PATHS(Enum):
    XL = "../data/grid_step-54.csv"
    L = "../data/grid_step-38.csv"
    M = "../data/grid_step-27.csv"
    S = "../data/grid_step-10.csv"


def tuple_to_dict(tup: Tuple[float, float]):
    return {
        "latitude": tup[0],
        "longitude": tup[1],
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


def load_grid(path: str = "../data/grid.csv"):
    loaded_grid = []

    with open(path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        # Iterate over the rows and append data to the list
        for row in reader:
            loaded_grid.append(tuple_to_dict((float(row[0]), float(row[1]))))

    return loaded_grid


def compute_average_duration(lists: List[List[Tuple[float, float, int]]]):
    # Dictionary to store durations for each latitude-longitude pair
    durations_dict = defaultdict(list)

    # Populate the durations dictionary
    for lst in lists:
        for lat, lon, duration in lst:
            durations_dict[(lat, lon)].append(duration)

    # Calculate average duration for each latitude-longitude pair
    average_durations = {}
    for (lat, lon), durations in durations_dict.items():
        average_duration = sum(durations) / len(durations)
        average_durations[(lat, lon)] = average_duration

    times = [(lat, lon, duration) for (lat, lon), duration in average_durations.items()]

    return times


def compute_max_duration(lists: List[List[Tuple[float, float, int]]]):
    # Dictionary to store durations for each latitude-longitude pair
    durations_dict = defaultdict(list)

    # Populate the durations dictionary
    for lst in lists:
        for lat, lon, duration in lst:
            durations_dict[(lat, lon)].append(duration)

    # Calculate average duration for each latitude-longitude pair
    max_durations = {}
    for (lat, lon), durations in durations_dict.items():
        max_duration = max(durations)
        max_durations[(lat, lon)] = max_duration

    times = [(lat, lon, duration) for (lat, lon), duration in max_durations.items()]

    return times


@lru_cache(maxsize=128)
def get_grid_times(starts: Tuple[Tuple[float, float]], average_mode: str = "max"):
    print("Getting grid times")
    starts = [tuple_to_dict(start) for start in starts]

    grid_points = load_grid(path=GRID_PATHS.M.value)
    # if len(starts) > 2:
    #     grid_points = load_grid(path=GRID_PATHS.M.value)
    # elif len(starts) > 1:
    #     grid_points = load_grid(path=GRID_PATHS.L.value)
    # else:
    #     grid_points = load_grid(path=GRID_PATHS.XL.value)

    times = [get_time_for_dests(start, grid_points) for start in starts]
    if len(starts) == 1:
        return times[0]

    if average_mode == "max":
        times = compute_max_duration(times)
    elif average_mode == "average":
        times = compute_average_duration(times)

    return times
