"""
geo_utils.py
Helper functions for coordinate transformation and polygon handling.
"""

import numpy as np


# --- Bounding box of mainland India (approximate) ---
# lon: 68°E – 97°E   lat: 8°N – 37°N
LON_MIN, LON_MAX = 68.0, 97.5
LAT_MIN, LAT_MAX = 8.0,  37.5

# Target Manim canvas size (units)
CANVAS_WIDTH  = 12.0
CANVAS_HEIGHT = 7.5


def lon_lat_to_manim(lon: float, lat: float) -> list:
    """
    Map a (lon, lat) coordinate to Manim canvas space,
    centred at the origin, preserving aspect ratio.
    """
    lon_range = LON_MAX - LON_MIN
    lat_range = LAT_MAX - LAT_MIN

    scale = min(CANVAS_WIDTH / lon_range, CANVAS_HEIGHT / lat_range)

    x = (lon - (LON_MIN + LON_MAX) / 2) * scale
    y = (lat - (LAT_MIN + LAT_MAX) / 2) * scale

    return [round(x, 6), round(y, 6), 0.0]


def ring_to_manim_points(ring: list) -> list:
    """Convert a GeoJSON coordinate ring to a list of Manim points."""
    return [lon_lat_to_manim(lon, lat) for lon, lat in ring]


def filter_bbox(rings: list, lon_min=60, lon_max=100, lat_min=5, lat_max=40) -> list:
    """
    Keep only rings whose centroid falls within the bounding box.
    Useful for excluding distant island chains / territories.
    """
    kept = []
    for ring in rings:
        lons = [pt[0] for pt in ring]
        lats = [pt[1] for pt in ring]
        c_lon = np.mean(lons)
        c_lat = np.mean(lats)
        if lon_min <= c_lon <= lon_max and lat_min <= c_lat <= lat_max:
            kept.append(ring)
    return kept
