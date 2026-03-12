from manim import *
import sys
import os
import numpy as np
import random
import itertools

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from manim.utils.rate_functions import ease_in_out_quad, ease_in_out_cubic, ease_out_back


class FinalScene(ThreeDScene):
    def construct(self):

        # ----------------------------
        # COLORS / FONTS (added to avoid errors)
        # ----------------------------
        secondary_accent = "#38bdf8"
        primary_text = WHITE
        body_font = "Arial"

        # ----------------------------
        # STEP 1 — Title Entry
        # ----------------------------
        r1, r2, r3 = 1.5, 2.3, 4

        # Central Image
        image_9 = ImageMobject("../images/image_9.png")
        image_9.height = r1 * 0.4
        image_9.move_to(ORIGIN)
        image_9.set_z_index(10)

        self.play(
            FadeIn(image_9, scale=0.5),
            # FadeOut(button),
            # FadeOut(button_shadow),
            # Uncreate(outer),
            # Uncreate(shadow),
            run_time=0.3,
            rate_func=rate_functions.ease_out_back
        )

        # Reset camera to 2D view
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=1.0)

        image_9.move_to(ORIGIN)
        center_point = ORIGIN

        # ----------------------------
        # STEP 2 — Background Rings
        # ----------------------------
        circle1 = Circle(radius=r1)
        circle2 = Circle(radius=r2)
        circle3 = Circle(radius=r3)

        circle1.set_stroke("#38bdf8", width=1)
        circle2.set_stroke(secondary_accent, width=1)
        circle3.set_stroke(secondary_accent, width=2)

        for c in [circle1, circle2, circle3]:
            c.set_fill(opacity=0)
            c.set_z_index(1)

        self.play(
            LaggedStart(
                GrowFromCenter(circle1),
                GrowFromCenter(circle2),
                GrowFromCenter(circle3),
                lag_ratio=0.2
            ),
            run_time=1.2
        )

        # ----------------------------
        # STEP 3 — Orbit Groups Creation
        # ----------------------------
        def create_orbit_group(radius, text_list):

            elements = []
            count = len(text_list)

            for i, text_str in enumerate(text_list):

                angle = TAU * i / count

                flat_offset = radius * np.array([
                    np.cos(angle),
                    np.sin(angle),
                    0
                ])

                t = 10 * DEGREES
                x, y, z = flat_offset

                tilted_offset = np.array([
                    x * np.cos(t) + z * np.sin(t),
                    y,
                    -x * np.sin(t) + z * np.cos(t)
                ])

                final_position = center_point + tilted_offset

                dot = Circle(radius=0.9)
                dot.set_fill(secondary_accent, opacity=0.9)
                dot.set_stroke("#38bdf8", width=1)
                dot.move_to(center_point).scale(0.01)
                dot.set_z_index(3)

                label = Text(
                    text_str,
                    font_size=40,
                    color=primary_text,
                    weight=BOLD,
                    font=body_font
                ).scale(0.5)

                if len(text_str) > 10:
                    label = Text(
                        text_str.replace(" ", "\n").replace("-", "-\n"),
                        font_size=36,
                        color=primary_text,
                        weight=BOLD,
                        line_spacing=0.8,
                        font=body_font
                    ).scale(0.5)

                label.move_to(center_point).scale(0.01)
                label.set_z_index(5)

                group = Group(dot, label)
                group.rotate(10 * DEGREES, axis=UP, about_point=center_point)

                group.final_position = final_position

                elements.append(group)

            return Group(*elements)

        outer_group = create_orbit_group(r3, ["Security", "Non-Elimination"])
        middle_group = create_orbit_group(r2, ["Fairness"])

        self.add(outer_group, middle_group)

        # ----------------------------
        # STEP 4 — Orbit Entry Animation
        # ----------------------------

        # Middle Orbit
        self.play(
            LaggedStart(
                *[
                    grp.animate.move_to(grp.final_position).scale(70)
                    for grp in middle_group
                ],
                lag_ratio=0.15
            ),
            run_time=0.5,
            rate_func=rate_functions.ease_out_back
        )

        # Outer Orbit
        self.play(
            LaggedStart(
                *[
                    grp.animate.move_to(grp.final_position).scale(110)
                    for grp in outer_group
                ],
                lag_ratio=0.15
            ),
            run_time=0.5,
            rate_func=rate_functions.ease_out_back
        )

        # ----------------------------
        # STEP 5 — Opposite Rotation
        # ----------------------------

        self.wait(1)

        self.play(
            LaggedStart(*[FadeOut(grp, shift=UP * 0.15) for grp in outer_group]),
            LaggedStart(*[FadeOut(grp, shift=UP * 0.15) for grp in middle_group]),
            run_time=0.2
        )

        for grp in outer_group:
            grp.remove(grp[1])

        for grp in middle_group:
            grp.remove(grp[1])

        self.play(
            Rotate(outer_group, angle=-PI/2, about_point=center_point),
            Rotate(middle_group, angle=PI/2, about_point=center_point),
            run_time=1.2,
            rate_func=linear
        )

        # ----------------------------
        # FINAL CAMERA ZOOM
        # ----------------------------

        self.move_camera(
            frame_center=ORIGIN,
            added_anims=[
                FadeOut(image_9),
                FadeOut(outer_group),
                FadeOut(middle_group),
                FadeOut(circle1),
                FadeOut(circle2),
                FadeOut(circle3),
                # FadeOut(outer),
                # FadeOut(shadow)
            ],
            zoom=20,
            run_time=1.1
        )