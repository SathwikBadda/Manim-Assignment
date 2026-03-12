from manim import *
import numpy as np

class InstitutionIcon(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.base1 = None
        self.base2 = None
        self.cols = None
        self.cap = None
        self.roof = None

        self._build_parts()

    def _build_parts(self):
        # ------------------------------------------------------
        # BUILDING BLOCKS
        # Constructed using rectangles for steps, columns, and cap,
        # and a Polygon for the roof.
        # ------------------------------------------------------
        self.base1 = Rectangle(width=0.55, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        self.base2 = Rectangle(width=0.50, height=0.03, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        self.base2.next_to(self.base1, UP, buff=0)

        self.cols = VGroup(*[
            Rectangle(width=0.05, height=0.22, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.08)
        self.cols.next_to(self.base2, UP, buff=0)

        self.cap = Rectangle(width=0.50, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        self.cap.next_to(self.cols, UP, buff=0)

        self.roof = Polygon(
            self.cap.get_corner(UL)+LEFT*0.04,
            self.cap.get_top()+UP*0.16,
            self.cap.get_corner(UR)+RIGHT*0.04,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )

        self.add(self.base1, self.base2, self.cols, self.cap, self.roof)
        self.scale(0.8)

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'base1', 'base2', 'cols', 'cap', 'roof'
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in InstitutionIcon")

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
