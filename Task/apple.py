from manim import *
import numpy as np


# ==========================================================
# APPLE
# ==========================================================

class Apple(VGroup):
    def __init__(self):
        super().__init__()

        apple_red = "#C70039" # Darker Red
        apple_outline = "#900C3F"
        stem_brown = "#8B5A2B"
        leaf_green = "#6DBE45"

        # --- Apple body (top & bottom dented) ---
        # --- Apple body (wider & more curved) ---
        body = VMobject()
        # Adjusted control points for a wider but still curved apple
        body.set_points_smoothly([
            UP * 1.1,                           # Center Top dent
            UP * 1.6 + LEFT * 0.6,              # Top Left Peak
            LEFT * 1.35 + UP * 0.8,             # Top Left Widest (Wider)
            LEFT * 1.2 + DOWN * 0.8,            # Bottom Left
            DOWN * 1.5 + LEFT * 0.4,            # Bottom Left Lobes (Deep curve)
            DOWN * 1.0,                         # Center Bottom dent
            DOWN * 1.5 + RIGHT * 0.4,           # Bottom Right Lobes (Deep curve)
            RIGHT * 1.2 + DOWN * 0.8,           # Bottom Right
            RIGHT * 1.35 + UP * 0.8,            # Top Right Widest (Wider)
            UP * 1.6 + RIGHT * 0.6,             # Top Right Peak
            UP * 1.1                            # Center Top dent
        ])
        body.set_fill(apple_red, opacity=1)
        body.set_stroke(apple_outline, width=6)

        # Highlight
        shine = Ellipse(width=0.45, height=0.7)
        shine.set_fill(WHITE, opacity=0.25)
        shine.set_stroke(width=0)
        shine.shift(UP * 0.2 + LEFT * 0.35)

        # Stem
        # Stem - adjusted for new top position
        stem = CubicBezier(
            UP * 1.1,                 # Start lower due to deeper dent
            UP * 1.4 + LEFT * 0.1,
            UP * 1.6 + RIGHT * 0.15,
            UP * 1.8,
            color=stem_brown,
            stroke_width=8
        )

        # Leaf - slight position clear
        leaf = Ellipse(width=0.55, height=0.25)
        leaf.set_fill(leaf_green, opacity=1)
        leaf.set_stroke("#4CAF50", width=3)
        leaf.rotate(25 * DEGREES)
        leaf.move_to(UP * 1.45 + RIGHT * 0.45)

        self.add(body, shine, stem, leaf)
        self.scale(0.55)   # reduced size


# ==========================================================
# SCENE
# ==========================================================

class AppleBounce(Scene):
    def construct(self):
        self.camera.background_color = "#F4F7FA"

        # Ground
        ground_y = -2.5
        ground = Line(LEFT * 6, RIGHT * 6, stroke_width=6, color=GRAY)
        ground.move_to(DOWN * 2.5)

        apple = Apple()
        apple.move_to(UP * 3)

        self.add(ground, apple)

        # --- Calculate landing Y (no overlap) ---
        apple_bottom = apple.get_bottom()[1]
        landing_y = apple.get_y() - (apple_bottom - ground_y)

        # --- Fall ---
        self.play(
            apple.animate.move_to([0, landing_y, 0]),
            rate_func=rate_functions.ease_in_quad,
            run_time=1.4
        )

        # --- Bounce (squash & stretch) ---
        # 1. Main Squash (Impact)
        self.play(
            apple.animate.scale([1.35, 0.7, 1]).move_to([0, landing_y - 0.2, 0]),
            run_time=0.1
        )
        # 2. Rebound Stretch (Upward energy)
        self.play(
            apple.animate.scale([0.85, 1.2, 1]).move_to([0, landing_y + 0.6, 0]),
            run_time=0.25
        )
        # 3. Second Fall
        self.play(
            apple.animate.scale([1.05, 0.95, 1]).move_to([0, landing_y, 0]),
            rate_func=rate_functions.ease_in_quad,
            run_time=0.2
        )
        # 4. Second Squash (Smaller)
        self.play(
             apple.animate.scale([1.1, 0.9, 1]).move_to([0, landing_y - 0.05, 0]),
             run_time=0.1
        )
        # 5. Second Rebound (Smaller)
        self.play(
            apple.animate.scale([0.98, 1.02, 1]).move_to([0, landing_y + 0.1, 0]),
             run_time=0.15
        )
        # 6. Final Land
        self.play(
            apple.animate.move_to([0, landing_y, 0]),
            rate_func=rate_functions.ease_out_quad,
            run_time=0.1
        )

        # Settle - Transform to original shape at landing position
        # Create a target apple that is uncompressed and at the correct position
        target_apple = Apple().move_to([0, landing_y, 0])
        self.play(Transform(apple, target_apple), run_time=0.2)
        self.wait(1)