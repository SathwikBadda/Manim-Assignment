from manim import *
import numpy as np

class MapPinIcon(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pin_body = None
        self.hole = None

        self._build_parts()

    def _build_parts(self):
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
        pin_body_raw = Union(pin_circle, triangle)
        pin_body_raw.set_fill(WHITE, 1)
        pin_body_raw.set_stroke(width=0)

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

        self.pin_body = Difference(pin_body_raw, hole)
        self.pin_body.shift(DOWN * 0.02)
        
        # We only really have one main component for now, but keeping structure
        self.add(self.pin_body)

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'pin_body'
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in MapPinIcon")

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
