from manim import *
import numpy as np

class GraduationCapIcon(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.top_diamond = None
        self.skull_cap = None
        self.tassel_curve = None
        self.tassel_line = None
        self.tassel_knot = None
        self.tassel_end = None

        self._build_parts()
        
    def _build_parts(self):
        # ------------------------------------------------------
        # TOP DIAMOND
        # The flat top part of the mortarboard.
        # ------------------------------------------------------
        self.top_diamond = Polygon(
            UP * 0.12,
            RIGHT * 0.35,
            DOWN * 0.12,
            LEFT * 0.35,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        self.top_diamond.shift(UP * 0.1)

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

        self.skull_cap = Union(cap_rect, cap_bottom)
        self.skull_cap.set_fill(WHITE, 1)
        self.skull_cap.set_stroke(width=0)
        self.skull_cap.move_to(self.top_diamond.get_center() + DOWN * 0.12)

        # ------------------------------------------------------
        # TASSEL
        # The hanging thread decoration.
        # Modeled with a CubicBezier curve for a natural drape.
        # ------------------------------------------------------
        center_point = self.top_diamond.get_center()
        right_corner = self.top_diamond.get_vertices()[1]

        self.tassel_curve = CubicBezier(
            center_point,
            center_point + RIGHT * 0.15,
            right_corner + UP * 0.05 + LEFT * 0.05,
            right_corner + DOWN * 0.02,
            color=WHITE,
            stroke_width=2
        )

        self.tassel_line = Line(
            self.tassel_curve.get_end(),
            self.tassel_curve.get_end() + DOWN * 0.18,
            color=WHITE,
            stroke_width=2
        )

        self.tassel_knot = Circle(
            radius=0.02,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(center_point)

        self.tassel_end = Circle(
            radius=0.03,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(self.tassel_line.get_end())

        self.add(
            self.skull_cap,
            self.top_diamond,
            self.tassel_curve,
            self.tassel_line,
            self.tassel_knot,
            self.tassel_end
        )

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'skull_cap', 'top_diamond', 'tassel_curve', etc.
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in GraduationCapIcon")

    def set_color(self, part_name: str, color: str):
        """Update the color of a specific part."""
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                # Ensure fill opacity is maintained if it was set
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1)

    def set_scale(self, scale_factor: float):
        """Set scale of the entire icon."""
        self.scale(scale_factor)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """
        Returns an animation for a specific part.
        animation_type: 'Indicate', 'Wiggle', 'Flash', 'FadeIn', 'FadeOut'
        """
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        elif animation_type == "FadeIn":
            return FadeIn(component, **kwargs)
        elif animation_type == "FadeOut":
            return FadeOut(component, **kwargs)
        else:
            return Wait(0.1)
