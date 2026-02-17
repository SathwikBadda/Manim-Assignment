from manim import *
import numpy as np

# ==========================================================
# LIGHTBULB ICON
# ==========================================================

class LightbulbIcon(VGroup):
    def __init__(self):
        super().__init__()

        bulb_yellow = "#FFC800"
        stroke_color = WHITE
        base_gray = "#4B5563"

        # --- Bulb body ---
        body = VMobject()
        p_bl = DOWN * 1.3 + LEFT * 0.35
        p_tl = DOWN * 0.6 + LEFT * 0.45
        p_l = LEFT * 1.05
        p_top = UP * 1.15
        p_r = RIGHT * 1.05
        p_tr = DOWN * 0.6 + RIGHT * 0.45
        p_br = DOWN * 1.3 + RIGHT * 0.35

        body.set_points_as_corners([p_bl, p_tl])
        body.add_cubic_bezier_curve(p_tl, p_tl + UP*0.5, p_l + DOWN*0.5, p_l)
        body.add_cubic_bezier_curve(p_l, p_l + UP*0.8, p_top + LEFT*0.6, p_top)
        body.add_cubic_bezier_curve(p_top, p_top + RIGHT*0.6, p_r + UP*0.8, p_r)
        body.add_cubic_bezier_curve(p_r, p_r + DOWN*0.5, p_tr + UP*0.5, p_tr)
        body.add_line_to(p_br)
        body.add_line_to(p_bl)

        body.set_fill(bulb_yellow, 1)
        body.set_stroke(stroke_color, 8)

        # Highlight
        # Removed as per user request ("remove the gray line appearing at top")

        # Rays
        rays = VGroup()
        for deg in [160, 125, 90, 55, 20]:
            angle = deg * DEGREES
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            ray = Line(
                direction * 1.5,
                direction * 1.9,
                stroke_width=8,
                color=stroke_color
            )
            ray.set_cap_style(CapStyleType.ROUND)
            ray.shift(UP * 0.1)
            rays.add(ray)

        # Base
        base = VGroup(
            RoundedRectangle(width=0.75, height=0.3, corner_radius=0.1),
            RoundedRectangle(width=0.65, height=0.2, corner_radius=0.1),
            RoundedRectangle(width=0.55, height=0.15, corner_radius=0.05),
        )
        base[0].move_to(DOWN * 1.45)
        base[1].move_to(DOWN * 1.65)
        base[2].move_to(DOWN * 1.82)

        for b in base:
            b.set_fill(base_gray, 1)
            b.set_stroke(stroke_color, 4)

        tip = Polygon(
            DOWN*1.9 + LEFT*0.15,
            DOWN*1.9 + RIGHT*0.15,
            DOWN*2.05,
            fill_color=base_gray,
            fill_opacity=1,
            stroke_width=0
        )

        self.add(rays, body, base, tip)


# ==========================================================
# BRAIN ICON
# ==========================================================

class BrainIcon(VGroup):
    def __init__(self):
        super().__init__()

        # Styling
        stroke_color = WHITE # Using White for visibility on dark background
        stroke_width = 8
        
        # --- Left Hemisphere Construction ---
        
        # 1. Outer Contour
        # Coordinates from prompt: Start(0.1, 2), Bulge1(-2, 1.5), Bulge2(-2, -1), Close(0.1, -1.5)
        # We need smooth curves between these points.
        
        outer = VMobject()
        p_start = np.array([0.1, 2.0, 0])
        p_bulge_top = np.array([-2.2, 1.5, 0]) # Adjusted slightly for roundness
        p_bulge_bot = np.array([-2.2, -1.0, 0])
        p_end = np.array([0.1, -1.5, 0])
        
        outer.set_points_smoothly([
            p_start,
            p_bulge_top,
            np.array([-2.5, 0.2, 0]), # Extra mid-point to guide the "C" shape
            p_bulge_bot,
            p_end
        ])
        
        # 2. Internal Folds
        
        # Fold 1 (Top): Horizontal "U" shape near y=1
        fold1 = VMobject()
        fold1.set_points_smoothly([
            np.array([-0.5, 1.0, 0]),
            np.array([-1.0, 0.8, 0]),
            np.array([-1.5, 1.0, 0])
        ])
        
        # Fold 2 (Middle): Distinct "S" shaped curve centered around x=-1, y=0
        fold2 = CubicBezier(
            np.array([-0.5, 0.5, 0]),   # Start
            np.array([-2.0, 0.5, 0]),   # Control 1
            np.array([-0.2, -0.5, 0]),  # Control 2
            np.array([-1.5, -0.5, 0])   # End
        )
        
        # Fold 3 (Bottom): Small hooked line near y=-1
        fold3 = VMobject()
        fold3.set_points_smoothly([
            np.array([-0.6, -1.0, 0]),
            np.array([-1.0, -1.3, 0]),
            np.array([-1.4, -1.1, 0])
        ])
        
        left_hemi = VGroup(outer, fold1, fold2, fold3)
        
        # Apply strict styling
        left_hemi.set_stroke(
            color=stroke_color,
            width=stroke_width,
            opacity=1
        )
        # Set joint type and cap style for all paths
        for path in left_hemi:
            path.set_stroke(opacity=1) # Ensure opacity
            # Manim's set_joint_type isn't always exposed directly on VMobject depending on version,
            # but usually it handles it via OpenGL or cairo backend defaults.
            # We will try to set caps manually if needed, but rounding is requested.
            # The user explicitly asked for "joint_type=LineJointType.ROUND".
            try:
                path.joint_type = LineJointType.ROUND
            except AttributeError:
                pass
            
            try:
                path.set_cap_style(CapStyleType.ROUND)
            except (AttributeError, NameError):
                pass

        # --- Right Hemisphere ---
        # Mirroring across Y-axis (x=0)
        # Since we started at x=0.1, there will be a 0.2 gap naturally.
        right_hemi = left_hemi.copy().flip(RIGHT)
        
        self.add(left_hemi, right_hemi)


# ==========================================================
# SCENE
# ==========================================================

class IconsScene(Scene):
    def construct(self):
        title = Text("Animated Icons", font_size=48).to_edge(UP)
        self.play(Write(title))

        bulb = LightbulbIcon().scale(0.6).shift(LEFT * 3.5)
        bulb_label = Text("Innovation", font_size=24).next_to(bulb, DOWN)

        brain = BrainIcon().scale(0.6).shift(RIGHT * 3.5)
        brain_label = Text("Creativity", font_size=24).next_to(brain, DOWN)

        self.play(Create(bulb), Write(bulb_label), run_time=2)
        # Animate brain halves simultaneously
        self.play(Create(brain, lag_ratio=0), Write(brain_label), run_time=2)

        self.play(
            bulb.animate.scale(1.1),
            brain.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=1
        )

        self.wait(2)