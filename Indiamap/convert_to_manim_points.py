"""
convert_to_manim_points.py

Converts:
1. India border coordinates
2. India state coordinates

from lon/lat → Manim coordinate space.

Outputs
───────
datasets/india_manim_points.json
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.geo_utils import ring_to_manim_points, filter_bbox

BORDER_INPUT = "datasets/india_border_coordinates.json"
STATE_INPUT  = "datasets/india_states_coordinates.json"

OUTPUT_PATH = "datasets/india_manim_points.json"


def convert_border():

    print("\nConverting India border...")

    with open(BORDER_INPUT) as f:
        data = json.load(f)

    raw_coords = data["coordinates"]

    rings = []

    for polygon in raw_coords:
        outer_ring = polygon[0]
        rings.append(outer_ring)

    filtered = filter_bbox(rings)

    if not filtered:
        filtered = rings

    manim_polygons = [ring_to_manim_points(r) for r in filtered]

    print("Border rings:", len(manim_polygons))

    return manim_polygons


def convert_states():

    print("\nConverting Indian states...")

    with open(STATE_INPUT) as f:
        states_data = json.load(f)

    states_manim = {}

    total_states = 0
    total_points = 0

    for state_name, state in states_data.items():

        polygons = state["coordinates"]

        state_rings = []

        for polygon in polygons:
            outer_ring = polygon[0]
            state_rings.append(outer_ring)

        manim_rings = [ring_to_manim_points(r) for r in state_rings]

        states_manim[state_name] = manim_rings

        total_states += 1
        total_points += sum(len(r) for r in manim_rings)

    print("States converted:", total_states)
    print("Total state points:", total_points)

    return states_manim


def convert():

    border = convert_border()

    states = convert_states()

    os.makedirs("datasets", exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(
            {
                "border": border,
                "states": states
            },
            f
        )

    print("\nSaved Manim dataset:", OUTPUT_PATH)


if __name__ == "__main__":
    convert()