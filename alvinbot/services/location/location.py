import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Union, Iterable

# Maps dependencies
import googlemaps

load_dotenv("config.env")
gmaps_client = googlemaps.Client(key=os.environ.get("MAPS_API_KEY"))

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

    return (latitude, longitude)