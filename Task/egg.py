from manim import *
import numpy as np

class Egg(VGroup):
    """
    A Manim VGroup representing a simple Egg.
    
    Attributes:
        body (Ellipse): The main egg shape.
        highlight (Ellipse): A subtle shine/reflection to give 3D volume.
    """
    def __init__(self, **kwargs):
        """
        Initializes the Egg object.
        
        Args:
            **kwargs: Arbitrary keyword arguments (e.g., color, opacity) passed to VGroup.
        """
        super().__init__(**kwargs)
        
        # Color constants
        self.EGG_WHITE = "#FFFEF7"   # Off-white for the egg shell
        self.EGG_OUTLINE = "#D4C5B9" # Soft gray-brown for the outline
        
        self.body = None
        self.highlight = None
        
        self._build_parts()

    def _build_parts(self):
        """Constructs the egg's geometry."""
        # Main egg body - a tall ellipse
        self.body = Ellipse(
            width=1.6,
            height=2.2,
            fill_color=self.EGG_WHITE,
            fill_opacity=1,
            stroke_color=self.EGG_OUTLINE,
            stroke_width=4
        )
        
        # Highlight - a smaller, semi-transparent white ellipse
        # This adds a specular highlight effect appearing at the top-left
        self.highlight = Ellipse(
            width=0.4,
            height=0.6,
            fill_color=WHITE,
            fill_opacity=0.3, # Low opacity for subtle shine
            stroke_width=0
        ).shift(LEFT * 0.3 + UP * 0.4)
        
        self.add(self.body, self.highlight)

    def get_subcomponent(self, part_name: str):
        """
        Access subcomponents by name.
        
        Args:
            part_name (str): Name of the component attribute.
            
        Returns:
            VMobject: The requested component.
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Egg")

    def set_color(self, part_name: str, color: str):
        """
        Sets the color of a specific subcomponent while preserving opacity logic.
        """
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     # Maintain reduced opacity for the highlight
                     opacity = 0.3 if "highlight" in part_name else 1
                     component.set_fill(c, opacity=opacity)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """Helper to create animations for specific parts."""
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)


class EggShells(VGroup):
    """
    A Manim VGroup representing cracked egg shells (top and bottom).
    
    Attributes:
        top_shell (Polygon): The upper half of the cracked egg.
        top_inner (Line): The jagged edge of the top shell.
        bottom_shell (Polygon): The lower half of the cracked egg.
        bottom_inner (Line): The jagged edge of the bottom shell.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.EGG_WHITE = "#FFFEF7"
        self.EGG_OUTLINE = "#D4C5B9"
        self.INNER_COLOR = "#FFF8E7" # Slightly darker for the inside of the shell
        
        self.top_shell = None
        self.top_inner = None
        self.bottom_shell = None
        self.bottom_inner = None
        
        self._build_parts()
        
    def _build_parts(self):
        """Constructs the cracked shell geometry."""
        
        # Top shell - custom polygon approximating a cracked dome
        top_points = [
            LEFT * 0.8,
            LEFT * 0.6 + UP * 0.3,
            LEFT * 0.3 + UP * 0.8,
            UP * 1.0,
            RIGHT * 0.3 + UP * 0.8,
            RIGHT * 0.6 + UP * 0.3,
            RIGHT * 0.8,
            RIGHT * 0.5 + DOWN * 0.1, # Crack start right
            LEFT * 0.5 + DOWN * 0.1,  # Crack start left
        ]
        
        self.top_shell = Polygon(
            *top_points,
            fill_color=self.EGG_WHITE,
            fill_opacity=1,
            stroke_color=self.EGG_OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Inner edge of top shell - represents the jagged break line
        self.top_inner = Line(
            start=LEFT * 0.5 + DOWN * 0.1,
            end=RIGHT * 0.5 + DOWN * 0.1,
            stroke_color=self.INNER_COLOR,
            stroke_width=6
        ).move_to(self.top_shell.get_bottom() + UP * 0.05)
        
        # Bottom shell - complementary shape to the top
        bottom_points = [
            LEFT * 0.8,
            LEFT * 0.6 + DOWN * 0.3,
            LEFT * 0.3 + DOWN * 0.7,
            DOWN * 0.9,
            RIGHT * 0.3 + DOWN * 0.7,
            RIGHT * 0.6 + DOWN * 0.3,
            RIGHT * 0.8,
            RIGHT * 0.5 + UP * 0.1, # Crack start right
            LEFT * 0.5 + UP * 0.1,  # Crack start left
        ]
        
        self.bottom_shell = Polygon(
            *bottom_points,
            fill_color=self.EGG_WHITE,
            fill_opacity=1,
            stroke_color=self.EGG_OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Inner edge of bottom shell
        self.bottom_inner = Line(
            start=LEFT * 0.5 + UP * 0.1,
            end=RIGHT * 0.5 + UP * 0.1,
            stroke_color=self.INNER_COLOR,
            stroke_width=6
        ).move_to(self.bottom_shell.get_top() + DOWN * 0.05)
        
        self.add(self.top_shell, self.top_inner, self.bottom_shell, self.bottom_inner)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in EggShells")


class Chicken(VGroup):
    """
    A Manim VGroup representing a cute Chicken character.
    
    Attributes:
        body (Circle): Main body.
        head (Circle): Head.
        tuft1/2/3 (Circle): Feathers on top of the head.
        left/right_wing (Ellipse): Wings.
        beak (Polygon): Orange beak.
        left/right_eye_... (Circle): Detailed eyes with pupils and highlights.
        left/right_foot (Polygon): Feet.
        left/right_blush (Ellipse): Pink cheeks.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.CHICK_YELLOW = "#FFD93D" # Bright yellow
        self.CHICK_DARK = "#F7C02B"   # Darker yellow for wings/details
        self.BEAK_ORANGE = "#FF8B3D"
        self.EYE_BLACK = "#2C2C2C"
        self.FEET_ORANGE = "#FF9E4F"
        self.OUTLINE = "#E0AC2D"
        
        self.body = None
        self.head = None
        self.tuft1 = None
        self.tuft2 = None
        self.tuft3 = None
        self.left_wing = None
        self.right_wing = None
        self.beak = None
        self.left_eye_white = None
        self.left_eye_pupil = None
        self.left_eye_shine = None
        self.right_eye_white = None
        self.right_eye_pupil = None
        self.right_eye_shine = None
        self.left_foot = None
        self.right_foot = None
        self.left_blush = None
        self.right_blush = None
        
        self._build_parts()

    def _build_parts(self):
        """Builds all chicken parts."""
        
        # Body - large circle base
        self.body = Circle(
            radius=0.9,
            fill_color=self.CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        )
        
        # Head - smaller circle stacked on body
        self.head = Circle(
            radius=0.65,
            fill_color=self.CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).shift(UP * 0.9)
        
        # Fluffy tuft on head - three small circles
        self.tuft1 = Circle(
            radius=0.15,
            fill_color=self.CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(UP * 1.5)
        
        self.tuft2 = Circle(
            radius=0.12,
            fill_color=self.CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.15 + UP * 1.45)
        
        self.tuft3 = Circle(
            radius=0.12,
            fill_color=self.CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.15 + UP * 1.45)
        
        # Wings - Teardrop shapes created by rotating ellipses
        self.left_wing = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=self.CHICK_DARK,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).rotate(30 * DEGREES).shift(LEFT * 0.7 + DOWN * 0.1)
        
        self.right_wing = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=self.CHICK_DARK,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).rotate(-30 * DEGREES).shift(RIGHT * 0.7 + DOWN * 0.1)
        
        # Beak - small Triangle
        self.beak = Polygon(
            UP * 0.05,
            LEFT * 0.12 + DOWN * 0.1,
            RIGHT * 0.12 + DOWN * 0.1,
            fill_color=self.BEAK_ORANGE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(UP * 0.75)
        
        # Eyes - layered circles (White -> Pupil -> Shine)
        # Left Eye
        self.left_eye_white = Circle(
            radius=0.18,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.22 + UP * 1.0)
        
        self.left_eye_pupil = Circle(
            radius=0.09,
            fill_color=self.EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.22 + UP * 1.0)
        
        self.left_eye_shine = Circle(
            radius=0.04,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.19 + UP * 1.03)
        
        # Right Eye
        self.right_eye_white = Circle(
            radius=0.18,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.22 + UP * 1.0)
        
        self.right_eye_pupil = Circle(
            radius=0.09,
            fill_color=self.EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.22 + UP * 1.0)
        
        self.right_eye_shine = Circle(
            radius=0.04,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 1.03)
        
        # Feet - Webbed feet using Polygons
        self.left_foot = Polygon(
            UP * 0.05,
            LEFT * 0.2 + DOWN * 0.1,
            LEFT * 0.05 + DOWN * 0.1,
            RIGHT * 0.05 + DOWN * 0.1,
            fill_color=self.FEET_ORANGE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.3 + DOWN * 0.9)
        
        self.right_foot = Polygon(
            UP * 0.05,
            RIGHT * 0.2 + DOWN * 0.1,
            RIGHT * 0.05 + DOWN * 0.1,
            LEFT * 0.05 + DOWN * 0.1,
            fill_color=self.FEET_ORANGE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.3 + DOWN * 0.9)
        
        # Blush marks - semi-transparent pink ellipses
        self.left_blush = Ellipse(
            width=0.25,
            height=0.15,
            fill_color="#FFB6C1",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(LEFT * 0.45 + UP * 0.85)
        
        self.right_blush = Ellipse(
            width=0.25,
            height=0.15,
            fill_color="#FFB6C1",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(RIGHT * 0.45 + UP * 0.85)
        
        # Group - Order determines what is drawn on top
        self.add(
            self.left_foot,
            self.right_foot,
            self.left_wing,
            self.right_wing,
            self.body,
            self.head,
            self.tuft1,
            self.tuft2,
            self.tuft3,
            self.left_eye_white,
            self.left_eye_pupil,
            self.left_eye_shine,
            self.right_eye_white,
            self.right_eye_pupil,
            self.right_eye_shine,
            self.beak,
            self.left_blush,
            self.right_blush
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Chicken")

    def set_color(self, part_name: str, color: str):
        """Sets color with special handling for blush opacity."""
        component = self.get_subcomponent(part_name)
        if component:
             c = ManimColor(color)
             if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     opacity = 0.6 if "blush" in part_name else 1
                     component.set_fill(c, opacity=opacity)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """Animation helper."""
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)
