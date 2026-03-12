#!/usr/bin/env python3
"""
run_pipeline.py
One-shot script that runs the full India-map pipeline:
  1. Download the Natural Earth GeoJSON dataset
  2. Extract India's border coordinates
  3. Convert coordinates to Manim space
  4. Render the Manim animation

Run from the project root:
    python run_pipeline.py
"""

import subprocess
import sys
import os


def run(cmd: list[str], label: str):
    print(f"\n{'='*60}")
    print(f"  STEP: {label}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, check=True)
    return result


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    run([sys.executable, "download_datasets.py"],
        "Download Natural Earth dataset")

    run([sys.executable, "extract_india_coordinates.py"],
        "Extract India border coordinates")

    run([sys.executable, "convert_to_manim_points.py"],
        "Convert coordinates to Manim space")

    run(
        ["manim", "-ql", "india_scene.py", "IndiaOutline"],
        "Render Manim animation (low quality — fast preview)",
    )

    print("\n✅  Pipeline complete!")
    print("For high-quality render, run:")
    print("  manim -pqh manim_scenes/india_outline_scene.py IndiaOutline\n")


if __name__ == "__main__":
    main()
