from manim import *
import numpy as np


# ==========================================================
# ROCKET
# ==========================================================

class Rocket(VGroup):
    def __init__(self):
        super().__init__()

        # Colors
        dark_blue = "#1a1a4b"
        white = WHITE
        red_orange = "#e65a41"
        yellow = "#f3d35b"
        dark_grey = "#3a3a3a"

        # ------------------------------------------------------
        # ===== MAIN BODY =====
        # RoundedRectangle with 3:1 height-to-width ratio (approx 1.0 x 3.0)
        # This forms the fuselage of the rocket.
        # ------------------------------------------------------
        body = RoundedRectangle(
            height=3.0,
            width=1.0,
            corner_radius=0.15,
            fill_color=white,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # ===== NOSE CONE =====
        # Bullet-shaped nose: triangle pointing upward, sitting on top of body
        nose_height = 0.5
        nose = Polygon(
            body.get_top() + UP * nose_height,  # Top point (peak)
            body.get_top() + LEFT * 0.5,         # Bottom-left
            body.get_top() + RIGHT * 0.5,        # Bottom-right
            fill_color=red_orange,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # ------------------------------------------------------
        # ===== FINS (Wings) =====
        # Two mirrored 4-point polygons (quadrilaterals) with sharp outer points
        # created using relative coordinates from the body's edges.
        # ------------------------------------------------------
        fin_x_offset = body.get_width() / 2
        fin_start_y = body.get_center()[1] - 0.5
        fin_bottom_y = body.get_bottom()[1] - 0.8

        # Left fin: 4-point quadrilateral
        left_fin = Polygon(
            body.get_left() + UP * 0.3,          # top-inner
            body.get_left() + LEFT * 0.8 + UP * 0.1,  # top-outer
            body.get_left() + LEFT * 0.7 + DOWN * 0.9,  # bottom-outer (sharp point)
            body.get_left() + DOWN * 0.6,       # bottom-inner
            fill_color=red_orange,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # Right fin: mirrored
        right_fin = Polygon(
            body.get_right() + UP * 0.3,
            body.get_right() + RIGHT * 0.8 + UP * 0.1,
            body.get_right() + RIGHT * 0.7 + DOWN * 0.9,
            body.get_right() + DOWN * 0.6,
            fill_color=red_orange,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # ===== PORTHOLE =====
        # Yellow circle with white glare highlight
        porthole = Circle(
            radius=0.25,
            fill_color=yellow,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        ).move_to(body.get_center() + UP * 0.4)

        # White glare (smaller circle offset to upper-left)
        glare = Circle(
            radius=0.08,
            fill_color=white,
            fill_opacity=0.9,
            stroke_width=0
        ).move_to(porthole.get_center() + UP * 0.08 + LEFT * 0.08)

        # ===== ENGINE NOZZLE =====
        # Dark grey trapezoid at the bottom
        nozzle = Polygon(
            body.get_bottom() + LEFT * 0.25 + UP * 0.05,
            body.get_bottom() + RIGHT * 0.25 + UP * 0.05,
            body.get_bottom() + RIGHT * 0.18 + DOWN * 0.25,
            body.get_bottom() + LEFT * 0.18 + DOWN * 0.25,
            fill_color=dark_grey,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # Add all parts to VGroup
        self.add(left_fin, right_fin)  # Fins behind
        self.add(body)                  # Main body
        self.add(nose)                  # Nose on top
        self.add(porthole, glare)       # Porthole with glare
        self.add(nozzle)                # Nozzle at bottom


# ==========================================================
# FLAME
# ==========================================================

class Flame(VGroup):
    def __init__(self):
        super().__init__()

        # ------------------------------------------------------
        # Teardrop flame using stretched circles
        # Outer layer: Orange teardrop (stretched vertically)
        # ------------------------------------------------------
        flame_outer = Circle(
            radius=0.35,
            fill_color="#ff8c42",
            fill_opacity=0.9,
            stroke_width=0
        ).stretch(2.0, dim=1)  # Stretch vertically to create teardrop
        
        # Middle layer: Yellow-orange
        flame_middle = Circle(
            radius=0.28,
            fill_color="#ffc857",
            fill_opacity=1,
            stroke_width=0
        ).stretch(1.8, dim=1).shift(UP * 0.1)
        
        # ------------------------------------------------------
        # Inner core: Bright yellow
        # The hottest part of the flame, centered and slightly higher.
        # ------------------------------------------------------
        flame_inner = Circle(
            radius=0.18,
            fill_color="#ffff99",
            fill_opacity=1,
            stroke_width=0
        ).stretch(1.6, dim=1).shift(UP * 0.15)

        self.add(flame_outer, flame_middle, flame_inner)


# ==========================================================
# SCENE
# ==========================================================

class RocketLaunchScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#2B8C9E"

        # Create rocket and single centered flame
        rocket = Rocket().shift(DOWN * 2.5)
        flame = Flame().move_to(rocket.get_bottom() + DOWN * 0.5).set_opacity(0)
        self.add(rocket, flame)

        # ------------------------------------------------------
        # ===== ANIMATION SEQUENCE =====
        # Phase 1: Create the entire rocket
        # Draws lines and fills shapes to introduce the rocket.
        # ------------------------------------------------------
        self.play(
            Create(rocket, run_time=2),
            rate_func=smooth
        )
        self.wait(0.5)

        # Phase 2: Ignite flame with GrowFromCenter
        self.play(
            GrowFromCenter(flame),
            run_time=0.6
        )
        self.wait(0.3)

        # ------------------------------------------------------
        # Phase 3: Flame flickers
        # Simulates unstable combustion by scaling the flame up and down.
        # ------------------------------------------------------
        for _ in range(2):
            self.play(
                flame.animate.scale(1.15),
                run_time=0.15
            )
            self.play(
                flame.animate.scale(0.9),
                run_time=0.15
            )

        # ------------------------------------------------------
        # Launch Sequence
        # 1. Attach flame to rocket via updater (so it moves with it).
        # 2. Wiggle the rocket to simulate engine rumbling.
        # 3. Scale up flame for takeoff power.
        # ------------------------------------------------------
        flame.add_updater(lambda m: m.move_to(rocket.get_bottom() + DOWN * 0.5))

        # Launch with Wiggle effect on rocket
        self.play(
            Wiggle(rocket, scale_value=1.05, rotation_angle=0.05),
            flame.animate.scale(1.3),
            run_time=0.4
        )
        self.wait(0.2)

        # ------------------------------------------------------
        # Phase 5: Liftoff!
        # Moves both the rocket and the camera upwards.
        # The camera moves slower than the rocket to let it move up the frame.
        # ------------------------------------------------------
        self.play(
            rocket.animate.shift(UP * 10),
            self.camera.frame.animate.shift(UP * 5),
            flame.animate.set_opacity(1).scale(0.8),
            run_time=4,
            rate_func=smooth
        )
        # Flame flicker during ascent
        for _ in range(3):
            self.play(
                flame.animate.scale(1.2),
                run_time=0.15
            )
            self.play(
                flame.animate.scale(0.8),
                run_time=0.15
            )

        # Phase 6: Continue rising and fade out
        self.play(
            rocket.animate.shift(UP * 5),
            self.camera.frame.animate.shift(UP * 3),
            flame.animate.scale(0.5),
            run_time=2,
            rate_func=linear
        )

        # Phase 7: Fade out as rocket leaves
        self.play(
            FadeOut(rocket),
            FadeOut(flame),
            run_time=1
        )

        self.wait(1)