import csv
import math
from collections import defaultdict
from enum import Enum
from functools import lru_cache
from typing import Dict, List, Tuple

import numpy as np
import requests
from scipy.interpolate import griddata

from config import GMAPS_API_KEY, GMAPS_CHUNK_SIZE


class GRID_PATHS(Enum):
    XL = ("../data/grids/berlin/grid-step-54.csv", 54)
    L = ("../data/grids/berlin/grid-step-38.csv", 38)
    M = ("../data/grids/berlin/grid-step-27.csv", 27)
    S = ("../data/grids/berlin/grid-step-10.csv", 10)


class GeoPoint:
    def __init__(self, lat: float, lng: float, value: int = None) -> None:
        self.lat = lat
        self.lng = lng
        self.value = value

    def __repr__(self) -> str:
        return f"{{Latitude: {self.lat}, Longitude: {self.lng}, Value: {self.value}}}"

    def __eq__(self, other):
        # Take care different values at the same location are seen as equal
        if isinstance(other, GeoPoint):
            return self.lat == other.lat and self.lng == other.lng
        return False

    def to_dict(self):
        return {"lat": self.lat, "lng": self.lng, "value": self.value}

    def to_tuple(self):
        return (self.lat, self.lng, self.value)


def tuple_to_dict(tup: Tuple[float, float]):
    return {
        "latitude": tup[0],
        "longitude": tup[1],
    }


def dict_to_tuple(d):
    return (d["latitude"], d["longitude"])


def gmaps_route_matrix(
    start: GeoPoint,
    destinations: List[GeoPoint],
    travel_mode: str = "TRANSIT",
    time: str = "2024-04-03T12:00:00Z",
) -> List[GeoPoint]:
    n_chunks = math.ceil(len(destinations) / GMAPS_CHUNK_SIZE)

    geo_points = []
    for i in range(n_chunks):
        current_destinations = destinations[
            i * GMAPS_CHUNK_SIZE : (i + 1) * GMAPS_CHUNK_SIZE
        ]
        req = {
            "origins": [
                {
                    "waypoint": {
                        "location": {
                            "latLng": {
                                "latitude": start.lat,
                                "longitude": start.lng,
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
                                "latitude": dest.lat,
                                "longitude": dest.lng,
                            }
                        }
                    }
                }
                for dest in current_destinations
            ],
            "travelMode": travel_mode,
            "departureTime": time,
        }

        url = f"https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix?key={GMAPS_API_KEY}"
        header = {"X-Goog-FieldMask": "duration,destinationIndex"}

        response = requests.post(url=url, json=req, headers=header)
        if response.status_code != 200:
            print(f"Got response {response.status_code} with body {response.json()}")
        response = response.json()

        for res in response:
            if not ("duration" in res and "destinationIndex" in res):
                print(f"Warning: Empty response.")
                continue
            dest = current_destinations[res["destinationIndex"]]
            duration = int(res["duration"][:-1])

            geo_points.append(GeoPoint(dest.lat, dest.lng, duration))

    return geo_points


# LONG = X
# LAT = Y
def build_grid(
    top_left: GeoPoint,
    bottom_right: GeoPoint,
    num_steps: int,
    top_right: GeoPoint = None,
    bottom_left: GeoPoint = None,
    compute_values: bool = False,
) -> List[GeoPoint]:
    # construct missing points
    if not top_right:
        top_right = GeoPoint(top_left.lat, bottom_right.lng)
    if not bottom_left:
        bottom_left = GeoPoint(bottom_right.lat, top_left.lng)

    # get lengths
    delta_x = top_right.lng - top_left.lng
    assert (
        delta_x > 0
    ), "Longitude of the top right point should be larger than of the top left point"
    delta_y = top_left.lat - bottom_left.lat
    assert (
        delta_y > 0
    ), "Latitude of the top left point should be larger than of the bottom left point"

    x_list = np.linspace(bottom_left.lng, bottom_right.lng, num_steps)
    y_list = np.linspace(bottom_left.lat, top_left.lat, num_steps)

    grid_lng, grid_lat = np.meshgrid(x_list, y_list)

    if not compute_values:
        grid_points = [
            GeoPoint(lat, lng)
            for lat, lng in list(zip(grid_lat.ravel(), grid_lng.ravel()))
        ]
        return grid_points

    if (
        top_left.value is None
        or top_right.value is None
        or bottom_left.value is None
        or bottom_right.value is None
    ):
        raise ValueError(
            "Trying to compute value grid with corners without values. Cannot interpolate between None values."
        )

    geo_points = np.array(
        [
            bottom_left.to_tuple(),
            bottom_right.to_tuple(),
            top_left.to_tuple(),
            top_right.to_tuple(),
        ]
    )
    # interpolate latitude, longitude and value
    grid_vals = griddata(
        geo_points[:, 0:2], geo_points[:, 2], (grid_lng, grid_lat), method="linear"
    )

    grid_points = [
        GeoPoint(lat, lng, val)
        for lat, lng, val in zip(grid_lat.ravel(), grid_lng.ravel(), grid_vals.ravel())
    ]
    return grid_points


def load_grid(path: str, includes_values: bool = False) -> List[GeoPoint]:
    loaded_grid = []

    with open(path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        # Iterate over the rows and append data to the list
        for row in reader:
            point = GeoPoint(float(row[0]), float(row[1]), int(row[2]) if includes_values else None)
            loaded_grid.append(point)

    return loaded_grid


def save_grid(path: str, grid: List[GeoPoint], includes_values: bool = False) -> None:
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        if includes_values:
            writer.writerow(['Latitude', 'Longitude', 'Value'])
        else:
            writer.writerow(['Latitude', 'Longitude'])

        # Iterate over the grid and write to the csv file
        for point in grid:
            if includes_values:
                writer.writerow((point.lat, point.lng, point.value))
            else:
                writer.writerow((point.lat, point.lng))


def compute_average_value(lists: List[List[GeoPoint]]) -> List[GeoPoint]:
    # Dictionary to store durations for each latitude-longitude pair
    durations_dict = defaultdict(list)

    # Populate the durations dictionary
    for lst in lists:
        for lat, lng, value in [point.to_tuple() for point in lst]:
            durations_dict[(lat, lng)].append(value)

    # Calculate average duration for each latitude-longitude pair
    average_values = {}
    for (lat, lng), values in durations_dict.items():
        average_value = sum(values) / len(values)
        average_values[(lat, lng)] = average_value

    geo_points_average = [
        GeoPoint(lat, lng, value) for (lat, lng), value in average_values.items()
    ]

    return geo_points_average


def compute_max_value(lists: List[List[GeoPoint]]) -> List[GeoPoint]:
    # Dictionary to store durations for each latitude-longitude pair
    durations_dict = defaultdict(list)

    # Populate the durations dictionary
    for lst in lists:
        for lat, lng, value in [point.to_tuple() for point in lst]:
            durations_dict[(lat, lng)].append(value)

    # Calculate average duration for each latitude-longitude pair
    max_values = {}
    for (lat, lng), values in durations_dict.items():
        max_value = max(values)
        max_values[(lat, lng)] = max_value

    geo_points_max = [
        GeoPoint(lat, lng, value) for (lat, lng), value in max_values.items()
    ]

    return geo_points_max


@lru_cache(maxsize=128)
def compute_geo_point_grid(
    starts: Tuple[GeoPoint],
    average_mode: str = "max",
    travel_mode: str = "TRANSIT",
    time: str = "2024-04-03T12:00:00Z",
    super_sample_factor: int = 5,
) -> List[GeoPoint]:
    # Use for dynamic grid sizes
    # if len(starts) > 2:
    #     grid_points, grid_size = load_grid(path=GRID_PATHS.M.value[0]), GRID_PATHS.M.value[1]
    # elif len(starts) > 1:
    #     grid_points, grid_size = load_grid(path=GRID_PATHS.L.value[0]), GRID_PATHS.L.value[1]
    # else:
    #     grid_points, grid_size = load_grid(path=GRID_PATHS.XL.value[0]), GRID_PATHS.XL.value[1]

    grid_points, grid_size = (
        load_grid(path=GRID_PATHS.S.value[0]),
        GRID_PATHS.S.value[1],
    )

    geo_point_grid = [
        gmaps_route_matrix(start, grid_points, time=time, travel_mode=travel_mode)
        for start in starts
    ]
    if len(starts) != 1:
        if average_mode == "max":
            geo_point_grid = compute_max_value(geo_point_grid)
        elif average_mode == "average":
            geo_point_grid = compute_average_value(geo_point_grid)
    else:
        geo_point_grid = geo_point_grid[0]

    if super_sample_factor is None or super_sample_factor <= 1:
        return geo_point_grid

    # compute super sampled grid with interpolated values
    geo_point_grid = np.array(
        sorted(geo_point_grid, key=lambda point: (-point.lat, point.lng))
    ).reshape(grid_size, grid_size, 3)

    super_sampled_geo_point_grid = []
    for col in range(grid_size - 1):
        for row in range(grid_size - 1):
            super_sampled_tile = build_grid(
                top_left=geo_point_grid[row][col],
                bottom_right=geo_point_grid[row + 1][col + 1],
                top_right=geo_point_grid[row][col + 1],
                bottom_left=geo_point_grid[row + 1][col],
                num_steps=super_sample_factor,
                compute_values=True,
            )
            super_sampled_geo_point_grid.extend(super_sampled_tile)

    # remove potential duplicates
    super_sampled_geo_point_grid = list(set(super_sampled_geo_point_grid))
    return super_sampled_geo_point_grid
