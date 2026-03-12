from manim import *
import numpy as np

"""
This script defines a detailed Rocket VGroup and a Flame effect using Manim.
It demonstrates how to assemble a vehicle from geometric primitives like
RoundedRectangles and Polygons. The accompanying scene animates a complete
launch sequence, including engine ignition, flame flickering, and a camera
follow shot as the rocket ascends.
"""

# ==========================================================
# ROCKET
# ==========================================================

class Rocket(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.body = None
        self.nose = None
        self.left_fin = None
        self.right_fin = None
        self.porthole = None
        self.glare = None
        self.nozzle = None
        
        self._build_parts()

    def _build_parts(self):
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
        self.body = RoundedRectangle(
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
        self.nose = Polygon(
            self.body.get_top() + UP * nose_height,  # Top point (peak)
            self.body.get_top() + LEFT * 0.5,         # Bottom-left
            self.body.get_top() + RIGHT * 0.5,        # Bottom-right
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
        # Left fin: 4-point quadrilateral
        self.left_fin = Polygon(
            self.body.get_left() + UP * 0.3,          # top-inner
            self.body.get_left() + LEFT * 0.8 + UP * 0.1,  # top-outer
            self.body.get_left() + LEFT * 0.7 + DOWN * 0.9,  # bottom-outer (sharp point)
            self.body.get_left() + DOWN * 0.6,       # bottom-inner
            fill_color=red_orange,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # Right fin: mirrored
        self.right_fin = Polygon(
            self.body.get_right() + UP * 0.3,
            self.body.get_right() + RIGHT * 0.8 + UP * 0.1,
            self.body.get_right() + RIGHT * 0.7 + DOWN * 0.9,
            self.body.get_right() + DOWN * 0.6,
            fill_color=red_orange,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # ===== PORTHOLE =====
        # Yellow circle with white glare highlight
        self.porthole = Circle(
            radius=0.25,
            fill_color=yellow,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        ).move_to(self.body.get_center() + UP * 0.4)

        # White glare (smaller circle offset to upper-left)
        self.glare = Circle(
            radius=0.08,
            fill_color=white,
            fill_opacity=0.9,
            stroke_width=0
        ).move_to(self.porthole.get_center() + UP * 0.08 + LEFT * 0.08)

        # ===== ENGINE NOZZLE =====
        # Dark grey trapezoid at the bottom
        self.nozzle = Polygon(
            self.body.get_bottom() + LEFT * 0.25 + UP * 0.05,
            self.body.get_bottom() + RIGHT * 0.25 + UP * 0.05,
            self.body.get_bottom() + RIGHT * 0.18 + DOWN * 0.25,
            self.body.get_bottom() + LEFT * 0.18 + DOWN * 0.25,
            fill_color=dark_grey,
            fill_opacity=1,
            stroke_color=dark_blue,
            stroke_width=8
        )

        # Add all parts to VGroup
        self.add(self.left_fin, self.right_fin)  # Fins behind
        self.add(self.body)                  # Main body
        self.add(self.nose)                  # Nose on top
        self.add(self.porthole, self.glare)       # Porthole with glare
        self.add(self.nozzle)                # Nozzle at bottom

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'body', 'nose', 'left_fin', 'right_fin', 'porthole', 'glare', 'nozzle'
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Rocket")

    def set_color(self, part_name: str, color: str):
        """Update the color of a specific part."""
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                # Ensure fill opacity is maintained if it was set
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1 if part_name != 'glare' else 0.9)

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


# ==========================================================
# FLAME
# ==========================================================

class Flame(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.flame_outer = None
        self.flame_middle = None
        self.flame_inner = None
        
        self._build_parts()
        
    def _build_parts(self):
        # ------------------------------------------------------
        # Teardrop flame using stretched circles
        # Outer layer: Orange teardrop (stretched vertically)
        # ------------------------------------------------------
        self.flame_outer = Circle(
            radius=0.35,
            fill_color="#ff8c42",
            fill_opacity=0.9,
            stroke_width=0
        ).stretch(2.0, dim=1)  # Stretch vertically to create teardrop
        
        # Middle layer: Yellow-orange
        self.flame_middle = Circle(
            radius=0.28,
            fill_color="#ffc857",
            fill_opacity=1,
            stroke_width=0
        ).stretch(1.8, dim=1).shift(UP * 0.1)
        
        # ------------------------------------------------------
        # Inner core: Bright yellow
        # The hottest part of the flame, centered and slightly higher.
        # ------------------------------------------------------
        self.flame_inner = Circle(
            radius=0.18,
            fill_color="#ffff99",
            fill_opacity=1,
            stroke_width=0
        ).stretch(1.6, dim=1).shift(UP * 0.15)

        self.add(self.flame_outer, self.flame_middle, self.flame_inner)

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'flame_outer', 'flame_middle', 'flame_inner'
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Flame")

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """
        Returns an animation for a specific part.
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
