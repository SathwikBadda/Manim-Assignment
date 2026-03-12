from manim import *
import numpy as np

"""
This script defines a detailed PizzaSlice and CompletePizza VGroup using Manim.
It demonstrates constructing a complex illustration from geometric primitives
like Arcs and Polygons, including details for crust and toppings.
The scenes showcase assembly, explosion, and re-integration animations.
"""

class PizzaSlice(VGroup):
    def __init__(self, start_angle: float, end_angle: float, **kwargs):
        super().__init__(**kwargs)
        
        self.start_angle = start_angle
        self.end_angle = end_angle
        
        # Colors matching the image
        self.CRUST_ORANGE = "#E8A847"
        self.CRUST_DARK = "#D69132"
        self.CHEESE_YELLOW = "#F4D58D"
        self.PEPPERONI_RED = "#E74C3C"
        self.PEPPERONI_HIGHLIGHT = "#EC7063"
        self.MUSHROOM_BEIGE = "#C9A663"
        self.OLIVE_GREEN = "#7D9E5F"
        self.OUTLINE_DARK = "#4A3C28"
        
        self.radius = 3.0
        
        # Subcomponents
        self.cheese_slice = None
        self.crust_outer = None
        self.crust_inner = None
        self.crust_highlights = None
        self.toppings = None  # VGroup containing all toppings
        self.pepperonis = None
        self.mushrooms = None
        self.olives = None

        self._build_parts()
        
    def _build_parts(self):
        angle_span = self.end_angle - self.start_angle
        
        # ------------------------------------------------------
        # 1. PIZZA SLICE SHAPE
        # Creating a custom polygon to represent a cheese slice.
        # Calculated using trigonometry to create an arc approximation.
        # ------------------------------------------------------
        slice_points = [ORIGIN]
        num_points = 20
        for i in range(num_points + 1):
            angle = self.start_angle + (angle_span * i / num_points)
            point = np.array([
                self.radius * np.cos(angle),
                self.radius * np.sin(angle),
                0
            ])
            slice_points.append(point)
        slice_points.append(ORIGIN)
        
        # Cheese layer
        self.cheese_slice = Polygon(
            *slice_points,
            fill_color=self.CHEESE_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE_DARK,
            stroke_width=6
        )
        
        # ------------------------------------------------------
        # 2. CRUST DETAIL
        # Using two arcs (outer and inner) to create a thick crust effect.
        # Different colors simulate baking gradients.
        # ------------------------------------------------------
        self.crust_outer = Arc(
            radius=self.radius,
            start_angle=self.start_angle,
            angle=angle_span,
            stroke_color=self.CRUST_DARK,
            stroke_width=20
        )
        
        self.crust_inner = Arc(
            radius=self.radius - 0.15,
            start_angle=self.start_angle,
            angle=angle_span,
            stroke_color=self.CRUST_ORANGE,
            stroke_width=14
        )
        
        # ------------------------------------------------------
        # 3. TOPPINGS
        # Adding pepperoni, mushrooms, and olives based on radial positions.
        # ------------------------------------------------------
        # Add highlights on crust
        highlight_positions = [0.2, 0.5, 0.8]
        self.crust_highlights = VGroup()
        for pos in highlight_positions:
            angle = self.start_angle + angle_span * pos
            start_point = np.array([
                (self.radius - 0.25) * np.cos(angle),
                (self.radius - 0.25) * np.sin(angle),
                0
            ])
            end_point = np.array([
                (self.radius - 0.05) * np.cos(angle),
                (self.radius - 0.05) * np.sin(angle),
                0
            ])
            highlight = Line(
                start=start_point,
                end=end_point,
                stroke_color=WHITE,
                stroke_width=4,
                stroke_opacity=0.7
            )
            self.crust_highlights.add(highlight)
        
        self.add(self.cheese_slice, self.crust_outer, self.crust_inner, self.crust_highlights)
        
        # Toppings Groups
        self.toppings = VGroup()
        self.pepperonis = VGroup()
        self.mushrooms = VGroup()
        self.olives = VGroup()

        # Add toppings based on slice position
        mid_angle = (self.start_angle + self.end_angle) / 2
        
        # Pepperoni (red circles)
        pepperoni_positions = [
            (self.radius * 0.5, mid_angle),
            (self.radius * 0.7, mid_angle + 0.15),
        ]
        
        for r, angle in pepperoni_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            pepperoni = Circle(
                radius=0.25,
                fill_color=self.PEPPERONI_RED,
                fill_opacity=1,
                stroke_color=self.OUTLINE_DARK,
                stroke_width=3
            ).move_to(pos)
            
            # Add highlights on pepperoni
            highlight1 = Circle(
                radius=0.06,
                fill_color=self.PEPPERONI_HIGHLIGHT,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos + UP * 0.08 + LEFT * 0.05)
            
            highlight2 = Circle(
                radius=0.04,
                fill_color=self.PEPPERONI_HIGHLIGHT,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos + DOWN * 0.07 + RIGHT * 0.08)
            
            pep_group = VGroup(pepperoni, highlight1, highlight2)
            self.pepperonis.add(pep_group)
            self.toppings.add(pep_group)
        
        # Mushrooms (beige semi-circles)
        mushroom_positions = [
            (self.radius * 0.65, mid_angle - 0.2),
        ]
        
        for r, angle in mushroom_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            mushroom = Arc(
                radius=0.15,
                start_angle=-PI/2,
                angle=PI,
                fill_color=self.MUSHROOM_BEIGE,
                fill_opacity=1,
                stroke_color=self.OUTLINE_DARK,
                stroke_width=3
            ).rotate(angle).move_to(pos)
            
            self.mushrooms.add(mushroom)
            self.toppings.add(mushroom)
        
        # Olives (green ovals)
        olive_positions = [
            (self.radius * 0.4, mid_angle + 0.25),
        ]
        
        for r, angle in olive_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            olive = Ellipse(
                width=0.18,
                height=0.25,
                fill_color=self.OLIVE_GREEN,
                fill_opacity=1,
                stroke_color=self.OUTLINE_DARK,
                stroke_width=3
            ).move_to(pos)
            
            self.olives.add(olive)
            self.toppings.add(olive)
            
        self.add(self.toppings)

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        part_name: 'cheese_slice', 'crust_outer', 'crust_inner', 'toppings', 'pepperonis', 'mushrooms', 'olives'
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in PizzaSlice")

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


class CompletePizza(VGroup):
    """
    A class representing a whole pizza made of 8 individual slices.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.slices = None
        self._build_parts()

    def _build_parts(self):
        # ------------------------------------------------------
        # Create 8 perfectly aligned slices
        # ------------------------------------------------------
        num_slices = 8
        slice_angle = TAU / num_slices
        
        self.slices = VGroup()
        for i in range(num_slices):
            start_angle = i * slice_angle
            end_angle = (i + 1) * slice_angle
            
            slice = PizzaSlice(start_angle, end_angle)
            self.slices.add(slice)
        
        self.add(self.slices)
        
    def get_slice(self, index: int):
        """Get a specific slice by index (0-7)."""
        if 0 <= index < len(self.slices):
             return self.slices[index]
        return None
        
    def get_subcomponent(self, part_name: str):
         """
         Access subcomponents.
         part_name: 'slices'
         """
         if hasattr(self, part_name):
            return getattr(self, part_name)
         raise ValueError(f"Part name {part_name} not found in CompletePizza")
    
    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
         # basic delegation
         component = self.get_subcomponent(part_name)
         if not component:
             return Wait(0.1)
         
         if animation_type == "Indicate":
            return Indicate(component, **kwargs)
         return Wait(0.1)
