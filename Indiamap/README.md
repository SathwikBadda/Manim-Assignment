# India Map Animation with Manim

Generates and animates the **outline of India** using pure geographic coordinate data and [Manim](https://www.manim.community/). No SVG files or raster images are used — the border is drawn entirely from longitude/latitude coordinates sourced from the Natural Earth dataset.

---

## Project Structure

```
india_map_manim/
├── datasets/                          # Generated data files
│   ├── ne_110m_admin_0_countries.geojson
│   ├── india_border_coordinates.json
│   └── india_manim_points.json
│
├── scripts/
│   ├── download_datasets.py           # Step 1 – acquire dataset
│   ├── extract_india_coordinates.py   # Step 2 – isolate India
│   └── convert_to_manim_points.py     # Step 3 – transform coordinates
│
├── manim_scenes/
│   └── india_outline_scene.py         # Step 4 – render animation
│
├── utils/
│   └── geo_utils.py                   # Coordinate math helpers
│
├── run_pipeline.py                    # One-shot runner
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# System dependencies (Ubuntu/Debian)
sudo apt install libpango1.0-dev libcairo2-dev pkg-config ffmpeg

# Python packages
pip install -r requirements.txt
```

---

## Running the Full Pipeline

```bash
python run_pipeline.py
```

This runs all four steps automatically.

---

## Step-by-Step Breakdown

### Step 1 — Download / Prepare Dataset (`download_datasets.py`)

Acquires the **Natural Earth 110m Admin 0 Countries** dataset, which contains polygon geometries for every country in the world.

- Tries to download from Natural Earth's CDN first.
- Falls back to the shapefile bundled with the `geopandas`/`pyogrio` package if offline.
- Saves a unified GeoJSON to `datasets/ne_110m_admin_0_countries.geojson`.

```bash
python scripts/download_datasets.py
```

---

### Step 2 — Extract India Coordinates (`extract_india_coordinates.py`)

Scans the GeoJSON for the feature where the country name is `"India"`, extracts its `Polygon` or `MultiPolygon` geometry, normalises the format, and writes it to `datasets/india_border_coordinates.json`.

```bash
python scripts/extract_india_coordinates.py
```

---

### Step 3 — Convert to Manim Space (`convert_to_manim_points.py`)

Transforms each `[longitude, latitude]` pair into a Manim canvas coordinate `[x, y, 0]`.

The mapping centres and scales India so it fills the Manim frame using the bounding box:

| Axis | Real-world range | Manim range (approx) |
|------|-----------------|----------------------|
| lon  | 68°E – 97.5°E   | –6 to +6             |
| lat  | 8°N – 37.5°N    | –3.75 to +3.75       |

Output: `datasets/india_manim_points.json`

```bash
python scripts/convert_to_manim_points.py
```

---

### Step 4 — Render Animation (`india_outline_scene.py`)

Two scenes are available:

| Scene class       | Description                              |
|-------------------|------------------------------------------|
| `IndiaOutline`    | Draws the border, then fills with blue.  |
| `IndiaOutlineZoom`| Same, then zooms into the centre.        |

```bash
# Low quality (fast preview)
manim -ql manim_scenes/india_outline_scene.py IndiaOutline

# High quality (1080p)
manim -qh manim_scenes/india_outline_scene.py IndiaOutline

# With auto-preview
manim -pqh manim_scenes/india_outline_scene.py IndiaOutline
```

Output video: `media/videos/india_outline_scene/*/IndiaOutline.mp4`

---

## How the Coordinate Conversion Works

```
longitude → x = (lon − centre_lon) × scale
latitude  → y = (lat − centre_lat) × scale

where scale = min(canvas_width / lon_span, canvas_height / lat_span)
```

This preserves the geographic aspect ratio so India does not look stretched.

---

## Constraints

- ❌ No SVG files
- ❌ No raster images  
- ✅ Pure geographic coordinate pipeline  
- ✅ Offline-capable (uses bundled Natural Earth data)
