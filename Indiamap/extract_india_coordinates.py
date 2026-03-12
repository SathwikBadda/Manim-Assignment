"""
extract_india_coordinates.py

Extracts:
1. India country border
2. All Indian state boundaries

Outputs:
datasets/india_border_coordinates.json
datasets/india_states_coordinates.json
"""

import json
import os

COUNTRY_DATA = "datasets/ne_10m_admin_0_countries.geojson"
STATE_DATA   = "datasets/ne_10m_admin_1_states.geojson"

BORDER_OUTPUT = "datasets/india_border_coordinates.json"
STATE_OUTPUT  = "datasets/india_states_coordinates.json"

INDIA_NAMES = {"India", "Republic of India"}


def get_country_name(props: dict) -> str:
    """Extract country name safely across dataset versions"""
    for key in ("ADMIN", "NAME", "name", "admin", "NAME_LONG"):
        val = props.get(key)
        if val:
            return val
    return ""


def extract_india_border():

    print("\nExtracting India border...")

    with open(COUNTRY_DATA, encoding="utf-8") as f:
        data = json.load(f)

    india_feature = None

    for feature in data["features"]:

        props = feature.get("properties", {})
        name = get_country_name(props)

        if name in INDIA_NAMES:
            india_feature = feature
            break

    if india_feature is None:
        raise ValueError("India not found in country dataset")

    geom = india_feature["geometry"]
    gtype = geom["type"]
    coords = geom["coordinates"]

    if gtype == "Polygon":
        coords = [coords]

    with open(BORDER_OUTPUT, "w") as f:
        json.dump({"type": gtype, "coordinates": coords}, f)

    total_pts = sum(len(ring) for poly in coords for ring in poly)

    print("Border polygons:", len(coords))
    print("Total border points:", total_pts)
    print("Saved:", BORDER_OUTPUT)


def extract_india_states():

    print("\nExtracting Indian states...")

    with open(STATE_DATA, encoding="utf-8") as f:
        data = json.load(f)

    states = {}

    for feature in data["features"]:

        props = feature.get("properties", {})

        admin = props.get("admin") or props.get("ADMIN")

        if admin != "India":
            continue

        state_name = props.get("name") or props.get("NAME")

        geom = feature["geometry"]

        coords = geom["coordinates"]

        gtype = geom["type"]

        if gtype == "Polygon":
            coords = [coords]

        states[state_name] = {
            "type": gtype,
            "coordinates": coords
        }

    with open(STATE_OUTPUT, "w") as f:
        json.dump(states, f)

    print("States extracted:", len(states))
    print("Saved:", STATE_OUTPUT)


def run():

    os.makedirs("datasets", exist_ok=True)

    extract_india_border()

    extract_india_states()

    print("\nExtraction complete.")


if __name__ == "__main__":
    run()