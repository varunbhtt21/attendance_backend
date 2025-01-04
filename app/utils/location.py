import math

EARTH_RADIUS = 6371000  # meters (approx)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance in meters between two points on the Earth.
    lat1, lon1, lat2, lon2 are in decimal degrees.
    """
    # Convert decimal degrees to radians
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    # Haversine formula
    a = (math.sin(d_lat / 2) ** 2) + math.cos(lat1) * math.cos(lat2) * (math.sin(d_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    distance = EARTH_RADIUS * c
    return distance
