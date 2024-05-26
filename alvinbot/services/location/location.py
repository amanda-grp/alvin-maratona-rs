import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Union, Iterable, NewType, Tuple
from math import radians, cos, sin, asin, sqrt

# Maps dependencies
import googlemaps

load_dotenv("config.env")
gmaps_client = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))

EARTH_RADIUS_KM = 6372.8 # Radius of earth in kilometers. Use 3956 for miles.

# Auxiliary type for Coordinate representation
Coordinate = NewType(
    name = "Coordinates",
    tp = Tuple[float, float]
)

def get_haversine_distance(origin_coord_pair: Coordinate, target_coord_pair: Coordinate) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """

    origin_lat, origin_lon = origin_coord_pair
    target_lat, target_lon = target_coord_pair

    # Decimal degrees to Radians conversion
    origin_lon, origin_lat, target_lon, target_lat = map(radians, [origin_lon, origin_lat, target_lon, target_lat])

    # Haversine formula calculation
    dlon = target_lon - origin_lon 
    dlat = target_lat - origin_lat 
    a = sin(dlat/2)**2 + cos(origin_lat) * cos(target_lat) * sin(dlon/2)**2
    conversion_constant = 2 * asin(sqrt(a)) 
    return conversion_constant * EARTH_RADIUS_KM

def encode_address(address: Union[str, Iterable], is_result: bool = False):
    """Turns an address in plain text into a Latitude, Longitude tuple pair

    Parameters
    ----------
    address : str or Iterable (list-like)
        The address in plain text related to the location of interest
        Alternatively, a parsed address result object can be passed

    Returns
    -------
    tuple
        (Latitude, Longitude) pairs for the address looked up
    """

    if is_result == True:
        # extracts metadata present in the address object
        geometry_data = address[0]["geometry"]["location"]
        (latitude, longitude) = (geometry_data["lat"], geometry_data["lng"])

    else:

        result = gmaps_client.geocode(
            address
        )

        geometry_data = result[0]["geometry"]["location"]

        (latitude, longitude) = (geometry_data["lat"], geometry_data["lng"])

    return Coordinate((latitude, longitude))