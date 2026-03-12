from manim import *
import numpy as np

class Rabbit(VGroup):
    """
    A Manim VGroup representing a stylized Rabbit character.
    
    This class encapsulates all the geometric shapes required to draw a rabbit,
    providing methods to access and manipulate individual parts.
    
    Attributes:
        body (Ellipse): The main body of the rabbit.
        head (Circle): The head of the rabbit.
        left_ear_outer (Ellipse): The outer part of the left ear.
        left_ear_inner (Ellipse): The inner pink part of the left ear.
        right_ear_outer (Ellipse): The outer part of the right ear.
        right_ear_inner (Ellipse): The inner pink part of the right ear.
        left_eye (Circle): The left eye.
        right_eye (Circle): The right eye.
        nose (Polygon): The nose triangle.
        mouth_left (Arc): The left curve of the mouth.
        mouth_right (Arc): The right curve of the mouth.
        tail (Circle): The fluffy tail.
        whisker_left1/2 (Line): Whiskers on the left side.
        whisker_right1/2 (Line): Whiskers on the right side.
        left_foot (Ellipse): The left foot.
        right_foot (Ellipse): The right foot.
    """
    def __init__(self, **kwargs):
        """
        Initializes the Rabbit object by creating all its subcomponents and adding them to the VGroup.
        
        Args:
            **kwargs: Arbitrary keyword arguments passed to the VGroup constructor.
        """
        super().__init__(**kwargs)
        
        # Color palette definitions for easy theme adjustment
        self.RABBIT_BODY = "#F0E6D2"      # Beige body color
        self.RABBIT_INNER_EAR = "#FFB6C1" # Pink for inner ears
        self.RABBIT_EYE = "#2C3E50"       # Dark blue/black for eyes
        self.RABBIT_NOSE = "#FF6B9D"      # Pink nose
        self.RABBIT_TAIL = "#FFFFFF"      # White tail
        self.OUTLINE = "#8B7355"          # Brown outline color
        
        # Initialize component references to None
        self.body = None
        self.head = None
        self.left_ear_outer = None
        self.left_ear_inner = None
        self.right_ear_outer = None
        self.right_ear_inner = None
        self.left_eye = None
        self.right_eye = None
        self.nose = None
        self.mouth_left = None
        self.mouth_right = None
        self.tail = None
        self.whisker_left1 = None
        self.whisker_left2 = None
        self.whisker_right1 = None
        self.whisker_right2 = None
        self.left_foot = None
        self.right_foot = None
        
        # Build and assemble the rabbit structure
        self._build_parts()

    def _build_parts(self):
        """
        Constructs the geometric shapes for the rabbit and adds them to the VGroup.
        The order of addition determines the z-index (layering) of the parts.
        """
        # Body - main oval shape, shifted slightly down
        self.body = Ellipse(
            width=1.8,
            height=2.2,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).shift(DOWN * 0.3)
        
        # Head - circle placed on top of the body
        self.head = Circle(
            radius=0.7,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).shift(UP * 0.9)
        
        # Left ear - elongated and rotated
        self.left_ear_outer = Ellipse(
            width=0.35,
            height=1.2,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).rotate(20 * DEGREES).shift(LEFT * 0.35 + UP * 1.8)
        
        self.left_ear_inner = Ellipse(
            width=0.18,
            height=0.8,
            fill_color=self.RABBIT_INNER_EAR,
            fill_opacity=1,
            stroke_width=0
        ).rotate(20 * DEGREES).shift(LEFT * 0.35 + UP * 1.7)
        
        # Right ear - mirrored rotation
        self.right_ear_outer = Ellipse(
            width=0.35,
            height=1.2,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=3
        ).rotate(-20 * DEGREES).shift(RIGHT * 0.35 + UP * 1.8)
        
        self.right_ear_inner = Ellipse(
            width=0.18,
            height=0.8,
            fill_color=self.RABBIT_INNER_EAR,
            fill_opacity=1,
            stroke_width=0
        ).rotate(-20 * DEGREES).shift(RIGHT * 0.35 + UP * 1.7)
        
        # Eyes - simple filled circles
        self.left_eye = Circle(
            radius=0.12,
            fill_color=self.RABBIT_EYE,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.25 + UP * 1.0)
        
        self.right_eye = Circle(
            radius=0.12,
            fill_color=self.RABBIT_EYE,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 1.0)
        
        # Nose - downward pointing triangle
        self.nose = Polygon(
            UP * 0.1,
            LEFT * 0.08 + DOWN * 0.05,
            RIGHT * 0.08 + DOWN * 0.05,
            fill_color=self.RABBIT_NOSE,
            fill_opacity=1,
            stroke_width=0
        ).shift(UP * 0.7)
        
        # Mouth - two small arcs curving outwards
        self.mouth_left = Arc(
            radius=0.15,
            start_angle=-PI/2,
            angle=-PI/3,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.08 + UP * 0.6)
        
        self.mouth_right = Arc(
            radius=0.15,
            start_angle=-PI/2,
            angle=-2*PI/3,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.08 + UP * 0.6)
        
        # Tail - circle at the back bottom right
        self.tail = Circle(
            radius=0.3,
            fill_color=self.RABBIT_TAIL,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.8 + DOWN * 1.2)
        
        # Whiskers - lines extending from the nose area
        self.whisker_left1 = Line(
            start=LEFT * 0.5 + UP * 0.8,
            end=LEFT * 1.0 + UP * 0.9,
            stroke_color=self.OUTLINE,
            stroke_width=1.5
        )
        self.whisker_left2 = Line(
            start=LEFT * 0.5 + UP * 0.7,
            end=LEFT * 1.0 + UP * 0.7,
            stroke_color=self.OUTLINE,
            stroke_width=1.5
        )
        self.whisker_right1 = Line(
            start=RIGHT * 0.5 + UP * 0.8,
            end=RIGHT * 1.0 + UP * 0.9,
            stroke_color=self.OUTLINE,
            stroke_width=1.5
        )
        self.whisker_right2 = Line(
            start=RIGHT * 0.5 + UP * 0.7,
            end=RIGHT * 1.0 + UP * 0.7,
            stroke_color=self.OUTLINE,
            stroke_width=1.5
        )
        
        # Feet - small ellipses at the base
        self.left_foot = Ellipse(
            width=0.4,
            height=0.25,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.4 + DOWN * 1.4)
        
        self.right_foot = Ellipse(
            width=0.4,
            height=0.25,
            fill_color=self.RABBIT_BODY,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.4 + DOWN * 1.4)
        
        # Group all parts - order matters for correct visual stacking (painters algorithm)
        self.add(
            self.tail,  # Tail goes behind
            self.body,
            self.left_foot,
            self.right_foot,
            self.head,
            self.left_ear_outer,
            self.left_ear_inner,
            self.right_ear_outer,
            self.right_ear_inner,
            self.left_eye,
            self.right_eye,
            self.nose,
            self.mouth_left,
            self.mouth_right,
            self.whisker_left1,
            self.whisker_left2,
            self.whisker_right1,
            self.whisker_right2
        )

    def get_subcomponent(self, part_name: str):
        """
        Retrieves a subcomponent by its name.

        Args:
            part_name (str): The name of the attribute (e.g., "head", "left_ear_inner").

        Returns:
            VMobject: The request subcomponent.

        Raises:
            ValueError: If the part name does not exist.
        """
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Rabbit")

    def set_color(self, part_name: str, color: str):
        """
        Sets the color of a specific subcomponent.
        
        Args:
            part_name (str): The name of the part to color.
            color (str): The hex color code or Manim color constant.
        """
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                # Ensure fill opacity is maintained if it was originally filled
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """
        Creates an animation object for manipulating a specific part.
        
        Args:
            part_name (str): The name of the part to animate.
            animation_type (str): Type of animation ("Indicate", "Wiggle", "Flash").
            **kwargs: Additional arguments for the animation constructor.
            
        Returns:
            Animation: A Manim Animation object ready to be played.
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
        else:
            return Wait(0.1)


class Carrot(VGroup):
    """
    A Manim VGroup representing a stylized Carrot.
    
    Attributes:
        carrot_body (Polygon): The main orange body.
        texture_lines (VGroup): Lines adding texture to the carrot body.
        leaves (VGroup): The green leafy top.
        highlight1 (Ellipse): Primary shine highlight.
        highlight2 (Ellipse): Secondary shine highlight.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Color palette
        self.CARROT_ORANGE = "#FF8C42"
        self.CARROT_DARK = "#E67332"
        self.LEAF_GREEN = "#7CBB5F"
        self.LEAF_DARK = "#5A9F3F"
        self.OUTLINE = "#8B5A3C"
        
        self.carrot_body = None
        self.texture_lines = None
        self.leaves = None
        self.highlight1 = None
        self.highlight2 = None

        self._build_parts()
        
    def _build_parts(self):
        """Builds the carrot geometry."""
        
        # Carrot body - elongated shape defined by points
        carrot_points = [
            UP * 0.8,           # Top center
            LEFT * 0.6 + UP * 0.6,   # Top left
            LEFT * 0.3 + DOWN * 1.5,  # Bottom left
            DOWN * 1.8,         # Bottom point
            RIGHT * 0.3 + DOWN * 1.5, # Bottom right
            RIGHT * 0.6 + UP * 0.6,   # Top right
        ]
        
        self.carrot_body = Polygon(
            *carrot_points,
            fill_color=self.CARROT_ORANGE,
            fill_opacity=1,
            stroke_color=self.OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Texture lines - diagonal stripes for detail
        self.texture_lines = VGroup()
        for i in range(5):
            y_pos = 0.5 - i * 0.5
            line = Line(
                start=LEFT * 0.4 + UP * y_pos,
                end=RIGHT * 0.4 + UP * (y_pos - 0.1),
                stroke_color=self.CARROT_DARK,
                stroke_width=2,
                stroke_opacity=0.6
            )
            self.texture_lines.add(line)
        
        # Leafy top - composed of multiple rotated ellipses
        self.leaves = VGroup()
        
        # Center leaf
        center_leaf = Ellipse(
            width=0.3,
            height=1.0,
            fill_color=self.LEAF_GREEN,
            fill_opacity=1,
            stroke_color=self.LEAF_DARK,
            stroke_width=3
        ).shift(UP * 1.5)
        
        # Side leaves
        left_leaf = Ellipse(
            width=0.25,
            height=0.8,
            fill_color=self.LEAF_GREEN,
            fill_opacity=1,
            stroke_color=self.LEAF_DARK,
            stroke_width=3
        ).rotate(30 * DEGREES).shift(LEFT * 0.35 + UP * 1.3)
        
        right_leaf = Ellipse(
            width=0.25,
            height=0.8,
            fill_color=self.LEAF_GREEN,
            fill_opacity=1,
            stroke_color=self.LEAF_DARK,
            stroke_width=3
        ).rotate(-30 * DEGREES).shift(RIGHT * 0.35 + UP * 1.3)
        
        # Outer smaller leaves
        far_left_leaf = Ellipse(
            width=0.2,
            height=0.6,
            fill_color=self.LEAF_GREEN,
            fill_opacity=0.9,
            stroke_color=self.LEAF_DARK,
            stroke_width=2
        ).rotate(50 * DEGREES).shift(LEFT * 0.55 + UP * 1.1)
        
        far_right_leaf = Ellipse(
            width=0.2,
            height=0.6,
            fill_color=self.LEAF_GREEN,
            fill_opacity=0.9,
            stroke_color=self.LEAF_DARK,
            stroke_width=2
        ).rotate(-50 * DEGREES).shift(RIGHT * 0.55 + UP * 1.1)
        
        self.leaves.add(
            far_left_leaf,
            far_right_leaf,
            left_leaf,
            right_leaf,
            center_leaf
        )
        
        # Highlights to add volume/shine
        self.highlight1 = Ellipse(
            width=0.15,
            height=0.3,
            fill_color=WHITE,
            fill_opacity=0.4,
            stroke_width=0
        ).shift(LEFT * 0.15 + UP * 0.3)
        
        self.highlight2 = Ellipse(
            width=0.12,
            height=0.25,
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_width=0
        ).shift(RIGHT * 0.1 + DOWN * 0.2)
        
        # Assemble
        self.add(
            self.carrot_body,
            self.texture_lines,
            self.highlight1,
            self.highlight2,
            self.leaves
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Carrot")

    def set_color(self, part_name: str, color: str):
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     # Maintain reduced opacity for highlights
                     opacity = 0.4 if "highlight" in part_name else 1
                     component.set_fill(c, opacity=opacity)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        """Returns an animation for a specific part."""
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
