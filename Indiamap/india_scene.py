"""
india_outline_scene.py
Draws India outline and all states with different colors.
"""

from manim import *
import json
import numpy as np
import os
import random


class IndiaOutline(Scene):

    DATA_PATH = "datasets/india_manim_points.json"

    def construct(self):

        if not os.path.exists(self.DATA_PATH):
            raise FileNotFoundError("Run dataset pipeline first")

        with open(self.DATA_PATH) as f:
            data = json.load(f)

        border_data = data["border"]
        states_data = data["states"]

        # ─────────────────────────────────────────────
        # Build India border
        # ─────────────────────────────────────────────

        border_mobs = []

        for ring in border_data:

            pts = np.array(ring)

            mob = VMobject()
            mob.set_points_as_corners(pts)

            mob.set_stroke(color=WHITE, width=3)
            mob.set_fill(opacity=0)

            border_mobs.append(mob)

        border_group = VGroup(*border_mobs)

        # ─────────────────────────────────────────────
        # Build States
        # ─────────────────────────────────────────────

        state_group = VGroup()

        for state_name, rings in states_data.items():

            state_color = random_bright_color()

            for ring in rings:

                pts = np.array(ring)

                if len(pts) < 3:
                    continue

                state = VMobject()
                state.set_points_as_corners(pts)

                state.set_fill(state_color, opacity=0.8)
                state.set_stroke(BLACK, width=1)

                state_group.add(state)

        # ─────────────────────────────────────────────
        # Title
        # ─────────────────────────────────────────────

        title = Text("India States Map", font_size=36, color=YELLOW)
        title.to_edge(UP)

        self.play(FadeIn(title))

        # ─────────────────────────────────────────────
        # Draw India border first
        # ─────────────────────────────────────────────

        self.play(Create(border_group), run_time=4)

        self.wait(0.5)

        # ─────────────────────────────────────────────
        # Draw states sequentially
        # ─────────────────────────────────────────────

        self.play(
            LaggedStart(
                *[FadeIn(state, scale=0.9) for state in state_group],
                lag_ratio=0.02
            ),
            run_time=4
        )

        self.wait(2)