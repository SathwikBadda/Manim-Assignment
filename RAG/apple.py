from manim import *
import numpy as np

# ==========================================================
# APPLE
# ==========================================================

class Apple(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.apple_red = "#C70039" # Darker Red
        self.apple_outline = "#900C3F"
        self.stem_brown = "#8B5A2B"
        self.leaf_green = "#6DBE45"
        
        self.body = None
        self.shine = None
        self.stem = None
        self.leaf = None

        self._build_parts()
        
    def _build_parts(self):
        # --- Apple body (top & bottom dented) ---
        # --- Apple body (wider & more curved) ---
        self.body = VMobject()
        # Adjusted control points for a wider but still curved apple
        self.body.set_points_smoothly([
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
        self.body.set_fill(self.apple_red, opacity=1)
        self.body.set_stroke(self.apple_outline, width=6)

        # Highlight
        self.shine = Ellipse(width=0.45, height=0.7)
        self.shine.set_fill(WHITE, opacity=0.25)
        self.shine.set_stroke(width=0)
        self.shine.shift(UP * 0.2 + LEFT * 0.35)

        # Stem
        # Stem - adjusted for new top position
        self.stem = CubicBezier(
            UP * 1.1,                 # Start lower due to deeper dent
            UP * 1.4 + LEFT * 0.1,
            UP * 1.6 + RIGHT * 0.15,
            UP * 1.8,
            color=self.stem_brown,
            stroke_width=8
        )

        # Leaf - slight position clear
        self.leaf = Ellipse(width=0.55, height=0.25)
        self.leaf.set_fill(self.leaf_green, opacity=1)
        self.leaf.set_stroke("#4CAF50", width=3)
        self.leaf.rotate(25 * DEGREES)
        self.leaf.move_to(UP * 1.45 + RIGHT * 0.45)

        self.add(self.body, self.shine, self.stem, self.leaf)
        self.scale(0.55)   # reduced size

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'body', 'shine', 'stem', 'leaf'
        """
        valid_parts = ["body", "shine", "stem", "leaf"]
        
        if part_name not in valid_parts:
            # Fallback for checking if attributes exist
            if hasattr(self, part_name):
                return getattr(self, part_name)
            raise ValueError(f"Part name must be one of {valid_parts} or a valid attribute")
            
        return getattr(self, part_name, None)

    def set_color(self, part_name: str, color: str):
        """Update the color of a specific part."""
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                # Ensure fill opacity is maintained if it was set
                if part_name == "body":
                    component.set_fill(c, opacity=1)
                elif part_name == "leaf":
                    component.set_fill(c, opacity=1)
                elif part_name == "shine":
                    component.set_fill(c, opacity=0.25)
                    
    def set_scale(self, scale_factor: float):
        """Set scale of the entire apple."""
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
