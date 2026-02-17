from manim import *
import numpy as np

# ==========================================================
# ICON BASE
# ==========================================================

class TerminalIcon(VGroup):
    def __init__(self, bg_color, inner_icon: VMobject):
        super().__init__()
        self.time = 0.0

        # ------------------------------------------------------
        # BACKGROUND CIRCLE
        # A colored circle that serves as the base for the icon.
        # ------------------------------------------------------
        self.circle = Circle(
            radius=0.3,
            fill_color=bg_color,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        )

        inner_icon.move_to(self.circle.get_center())
        self.inner_icon = inner_icon

        self.add(self.circle, inner_icon)

    # ------------------------------------------------------
    # POP-IN ANIMATION
    # An animation method to make the icon appear with a 
    # scale-up effect (pop).
    # ------------------------------------------------------
    def pop_in(self):
        self.save_state()
        self.scale(0.5)
        return AnimationGroup(
            FadeIn(self),
            self.animate.restore(),
        )

    # ------------------------------------------------------
    # FLOAT ANIMATION
    # Adds an idle floating motion to the icon using a sin wave updater.
    # 'phase' allows each icon to float slightly differently.
    # ------------------------------------------------------
    def float(self, phase=0):
        def updater(m, dt):
            self.time += dt
            m.shift(UP * 0.002 * np.sin(self.time * 2 + phase))
        self.add_updater(updater)


# ==========================================================
# ICON SHAPES (PURE MANIM)
# ==========================================================

class RupeeIcon(Text):
    def __init__(self):
        super().__init__("₹", font_size=32, color=WHITE, weight=BOLD)


class FemaleIcon(Text):
    def __init__(self):
        super().__init__("♀", font_size=36, color=WHITE, weight=BOLD)


class HeartIcon(Text):
    def __init__(self):
        super().__init__("❤", font_size=28, color=WHITE)


class GraduationCapIcon(VGroup):
    def __init__(self):
        super().__init__()

        # ------------------------------------------------------
        # TOP DIAMOND
        # The flat top part of the mortarboard.
        # ------------------------------------------------------
        top_diamond = Polygon(
            UP * 0.12,
            RIGHT * 0.35,
            DOWN * 0.12,
            LEFT * 0.35,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        top_diamond.shift(UP * 0.1)

        # ------------------------------------------------------
        # SKULL CAP
        # The part of the hat that sits on the head.
        # Created by merging a Rectangle and an Ellipse.
        # ------------------------------------------------------
        cap_rect = Rectangle(
            width=0.28,
            height=0.18,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )

        cap_bottom = Ellipse(
            width=0.28,
            height=0.08,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        cap_bottom.move_to(cap_rect.get_bottom())

        skull_cap = Union(cap_rect, cap_bottom)
        skull_cap.set_fill(WHITE, 1)
        skull_cap.set_stroke(width=0)
        skull_cap.move_to(top_diamond.get_center() + DOWN * 0.12)

        # ------------------------------------------------------
        # TASSEL
        # The hanging thread decoration.
        # Modeled with a CubicBezier curve for a natural drape.
        # ------------------------------------------------------
        center_point = top_diamond.get_center()
        right_corner = top_diamond.get_vertices()[1]

        tassel_curve = CubicBezier(
            center_point,
            center_point + RIGHT * 0.15,
            right_corner + UP * 0.05 + LEFT * 0.05,
            right_corner + DOWN * 0.02,
            color=WHITE,
            stroke_width=2
        )

        tassel_line = Line(
            tassel_curve.get_end(),
            tassel_curve.get_end() + DOWN * 0.18,
            color=WHITE,
            stroke_width=2
        )

        tassel_knot = Circle(
            radius=0.02,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(center_point)

        tassel_end = Circle(
            radius=0.03,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(tassel_line.get_end())

        self.add(
            skull_cap,
            top_diamond,
            tassel_curve,
            tassel_line,
            tassel_knot,
            tassel_end
        )


class InstitutionIcon(VGroup):
    def __init__(self):
        super().__init__()

        # ------------------------------------------------------
        # BUILDING BLOCKS
        # Constructed using rectangles for steps, columns, and cap,
        # and a Polygon for the roof.
        # ------------------------------------------------------
        base1 = Rectangle(width=0.55, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        base2 = Rectangle(width=0.50, height=0.03, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        base2.next_to(base1, UP, buff=0)

        cols = VGroup(*[
            Rectangle(width=0.05, height=0.22, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.08)
        cols.next_to(base2, UP, buff=0)

        cap = Rectangle(width=0.50, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cap.next_to(cols, UP, buff=0)

        roof = Polygon(
            cap.get_corner(UL)+LEFT*0.04,
            cap.get_top()+UP*0.16,
            cap.get_corner(UR)+RIGHT*0.04,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )

        self.add(base1, base2, cols, cap, roof)
        self.scale(0.8)


class MapPinIcon(VGroup):
    def __init__(self):
        super().__init__()

        pin_radius = 0.10

        # ------------------------------------------------------
        # PIN BODY
        # Merging a Circle (head) and inverted Triangle (point).
        # ------------------------------------------------------
        # CIRCLE
        pin_circle = Circle(
            radius=pin_radius,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        pin_circle.move_to(UP * 0.06)

        # TRIANGLE
        triangle = Triangle(
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        triangle.stretch_to_fit_width(pin_radius * 1.8)
        triangle.stretch_to_fit_height(pin_radius * 2.0)
        triangle.rotate(PI)
        triangle.move_to(pin_circle.get_center() + DOWN * 0.10)

        # MERGE BODY
        pin_body = Union(pin_circle, triangle)
        pin_body.set_fill(WHITE, 1)
        pin_body.set_stroke(width=0)

        # ------------------------------------------------------
        # HOLE
        # Subtracting a smaller circle from the center to create the hole.
        # ------------------------------------------------------
        hole = Circle(
            radius=0.04,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        hole.move_to(pin_circle.get_center())

        final_pin = Difference(pin_body, hole)
        final_pin.shift(DOWN * 0.02)

        self.add(final_pin)


# ==========================================================
# MAIN SCENE
# ==========================================================

class RagIcons(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#1E3A8A"

        # ------------------------------------------------------
        # 1. ICON SETUP
        # Create all 6 icons and group them together.
        # ------------------------------------------------------
        icons = VGroup(
            TerminalIcon("#FF6B35", RupeeIcon()),
            TerminalIcon("#4A90E2", GraduationCapIcon()),
            TerminalIcon("#50C878", InstitutionIcon()),
            TerminalIcon("#9B59B6", MapPinIcon()),
            TerminalIcon("#E91E63", FemaleIcon()),
            TerminalIcon("#FF9800", HeartIcon()),
        )

        # ------------------------------------------------------
        # 2. POSITIONING
        # Arrange icons horizontally in a single line at the center.
        # ------------------------------------------------------
        icons.arrange(RIGHT, buff=0.8)
        icons.move_to(ORIGIN)

        # ------------------------------------------------------
        # 3. ANIMATION
        # Animate them popping in one by one using LaggedStart.
        # ------------------------------------------------------
        self.play(
            LaggedStart(*[icon.pop_in() for icon in icons], lag_ratio=0.5),
            run_time=4
        )

        # ------------------------------------------------------
        # 4. IDLE MOTION
        # Add a gentle floating animation to all icons.
        # ------------------------------------------------------
        for i, icon in enumerate(icons):
            icon.float(phase=i*PI/3)

        self.wait(7)