from manim import *
import numpy as np

class RabbitToCarrotTransform(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#F5F5F0"
        
        # Create shadow (stays on ground, not part of transform)
        shadow = self.create_shadow()
        shadow.shift(DOWN * 2.8)
        
        # Create rabbit
        rabbit = self.create_rabbit()
        rabbit.shift(DOWN * 0.5)
        
        # Create carrot (same size/position for smooth transform)
        carrot = self.create_carrot()
        carrot.shift(DOWN * 0.5)
        
        # Phase 1: Rabbit appears with shadow
        self.play(
            FadeIn(shadow, scale=0.8),
            FadeIn(rabbit, scale=0.8),
            run_time=1.2
        )
        self.wait(0.5)
        
        # Phase 2: Subtle idle animation - gentle bounce
        self.play(
            rabbit.animate.shift(UP * 0.1),
            shadow.animate.scale(0.95),
            run_time=0.4,
            rate_func=smooth
        )
        self.play(
            rabbit.animate.shift(DOWN * 0.1),
            shadow.animate.scale(1/0.95),
            run_time=0.4,
            rate_func=smooth
        )
        self.wait(0.3)
        
        # Phase 3: Transform rabbit into carrot
        # Shadow morphs slightly to match carrot shape
        carrot_shadow = self.create_shadow(width=1.2, height=0.3)
        carrot_shadow.shift(DOWN * 2.8)
        
        self.play(
            Transform(rabbit, carrot),
            Transform(shadow, carrot_shadow),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Phase 4: Final hold with subtle wiggle
        self.wait(0.5)
        self.play(
            rabbit.animate.rotate(5 * DEGREES),
            run_time=0.3,
            rate_func=there_and_back
        )
        self.wait(1)
    
    def create_shadow(self, width=2.0, height=0.4):
        """
        Creates a soft ground shadow using an ellipse.
        
        Args:
            width: Shadow width
            height: Shadow height (flattened)
        
        Returns:
            Ellipse object representing shadow
        """
        shadow = Ellipse(
            width=width,
            height=height,
            fill_color=BLACK,
            fill_opacity=0.15,
            stroke_width=0
        )
        return shadow
    
    def create_rabbit(self):
        """
        Creates a rabbit using basic Manim shapes.
        Components: body, head, ears, eyes, nose, tail
        
        Returns:
            VGroup containing all rabbit parts
        """
        # Color palette
        RABBIT_BODY = "#F0E6D2"
        RABBIT_INNER_EAR = "#FFB6C1"
        RABBIT_EYE = "#2C3E50"
        RABBIT_NOSE = "#FF6B9D"
        RABBIT_TAIL = "#FFFFFF"
        OUTLINE = "#8B7355"
        
        # Body - main oval
        body = Ellipse(
            width=1.8,
            height=2.2,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(DOWN * 0.3)
        
        # Head - circle
        head = Circle(
            radius=0.7,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(UP * 0.9)
        
        # Left ear - elongated ellipse
        left_ear_outer = Ellipse(
            width=0.35,
            height=1.2,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).rotate(20 * DEGREES).shift(LEFT * 0.35 + UP * 1.8)
        
        left_ear_inner = Ellipse(
            width=0.18,
            height=0.8,
            fill_color=RABBIT_INNER_EAR,
            fill_opacity=1,
            stroke_width=0
        ).rotate(20 * DEGREES).shift(LEFT * 0.35 + UP * 1.7)
        
        # Right ear - elongated ellipse
        right_ear_outer = Ellipse(
            width=0.35,
            height=1.2,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).rotate(-20 * DEGREES).shift(RIGHT * 0.35 + UP * 1.8)
        
        right_ear_inner = Ellipse(
            width=0.18,
            height=0.8,
            fill_color=RABBIT_INNER_EAR,
            fill_opacity=1,
            stroke_width=0
        ).rotate(-20 * DEGREES).shift(RIGHT * 0.35 + UP * 1.7)
        
        # Left eye
        left_eye = Circle(
            radius=0.12,
            fill_color=RABBIT_EYE,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.25 + UP * 1.0)
        
        # Right eye
        right_eye = Circle(
            radius=0.12,
            fill_color=RABBIT_EYE,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 1.0)
        
        # Nose - small triangle
        nose = Polygon(
            UP * 0.1,
            LEFT * 0.08 + DOWN * 0.05,
            RIGHT * 0.08 + DOWN * 0.05,
            fill_color=RABBIT_NOSE,
            fill_opacity=1,
            stroke_width=0
        ).shift(UP * 0.7)
        
        # Mouth - small curves
        mouth_left = Arc(
            radius=0.15,
            start_angle=-PI/2,
            angle=-PI/3,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.08 + UP * 0.6)
        
        mouth_right = Arc(
            radius=0.15,
            start_angle=-PI/2,
            angle=-2*PI/3,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.08 + UP * 0.6)
        
        # Tail - fluffy circle
        tail = Circle(
            radius=0.3,
            fill_color=RABBIT_TAIL,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.8 + DOWN * 1.2)
        
        # Whiskers
        whisker_left1 = Line(
            start=LEFT * 0.5 + UP * 0.8,
            end=LEFT * 1.0 + UP * 0.9,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        whisker_left2 = Line(
            start=LEFT * 0.5 + UP * 0.7,
            end=LEFT * 1.0 + UP * 0.7,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        whisker_right1 = Line(
            start=RIGHT * 0.5 + UP * 0.8,
            end=RIGHT * 1.0 + UP * 0.9,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        whisker_right2 = Line(
            start=RIGHT * 0.5 + UP * 0.7,
            end=RIGHT * 1.0 + UP * 0.7,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        
        # Feet - small ovals at bottom
        left_foot = Ellipse(
            width=0.4,
            height=0.25,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.4 + DOWN * 1.4)
        
        right_foot = Ellipse(
            width=0.4,
            height=0.25,
            fill_color=RABBIT_BODY,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.4 + DOWN * 1.4)
        
        # Group all parts - order matters for layering
        rabbit_group = VGroup(
            tail,  # Back layer
            body,
            left_foot,
            right_foot,
            head,
            left_ear_outer,
            left_ear_inner,
            right_ear_outer,
            right_ear_inner,
            left_eye,
            right_eye,
            nose,
            mouth_left,
            mouth_right,
            whisker_left1,
            whisker_left2,
            whisker_right1,
            whisker_right2
        )
        
        return rabbit_group
    
    def create_carrot(self):
        """
        Creates a carrot using basic Manim shapes.
        Components: carrot body, leafy top
        
        Returns:
            VGroup containing all carrot parts
        """
        # Color palette
        CARROT_ORANGE = "#FF8C42"
        CARROT_DARK = "#E67332"
        LEAF_GREEN = "#7CBB5F"
        LEAF_DARK = "#5A9F3F"
        OUTLINE = "#8B5A3C"
        
        # Carrot body - elongated triangle/polygon
        carrot_points = [
            UP * 0.8,           # Top center
            LEFT * 0.6 + UP * 0.6,   # Top left
            LEFT * 0.3 + DOWN * 1.5,  # Bottom left
            DOWN * 1.8,         # Bottom point
            RIGHT * 0.3 + DOWN * 1.5, # Bottom right
            RIGHT * 0.6 + UP * 0.6,   # Top right
        ]
        
        carrot_body = Polygon(
            *carrot_points,
            fill_color=CARROT_ORANGE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Carrot texture lines - diagonal stripes
        texture_lines = VGroup()
        for i in range(5):
            y_pos = 0.5 - i * 0.5
            line = Line(
                start=LEFT * 0.4 + UP * y_pos,
                end=RIGHT * 0.4 + UP * (y_pos - 0.1),
                stroke_color=CARROT_DARK,
                stroke_width=2,
                stroke_opacity=0.6
            )
            texture_lines.add(line)
        
        # Leafy top - multiple leaf shapes
        leaves = VGroup()
        
        # Center leaf
        center_leaf = Ellipse(
            width=0.3,
            height=1.0,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=LEAF_DARK,
            stroke_width=3
        ).shift(UP * 1.5)
        
        # Left leaf
        left_leaf = Ellipse(
            width=0.25,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=LEAF_DARK,
            stroke_width=3
        ).rotate(30 * DEGREES).shift(LEFT * 0.35 + UP * 1.3)
        
        # Right leaf
        right_leaf = Ellipse(
            width=0.25,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=LEAF_DARK,
            stroke_width=3
        ).rotate(-30 * DEGREES).shift(RIGHT * 0.35 + UP * 1.3)
        
        # Far left leaf
        far_left_leaf = Ellipse(
            width=0.2,
            height=0.6,
            fill_color=LEAF_GREEN,
            fill_opacity=0.9,
            stroke_color=LEAF_DARK,
            stroke_width=2
        ).rotate(50 * DEGREES).shift(LEFT * 0.55 + UP * 1.1)
        
        # Far right leaf
        far_right_leaf = Ellipse(
            width=0.2,
            height=0.6,
            fill_color=LEAF_GREEN,
            fill_opacity=0.9,
            stroke_color=LEAF_DARK,
            stroke_width=2
        ).rotate(-50 * DEGREES).shift(RIGHT * 0.55 + UP * 1.1)
        
        leaves.add(
            far_left_leaf,
            far_right_leaf,
            left_leaf,
            right_leaf,
            center_leaf
        )
        
        # Small highlights on carrot for shine
        highlight1 = Ellipse(
            width=0.15,
            height=0.3,
            fill_color=WHITE,
            fill_opacity=0.4,
            stroke_width=0
        ).shift(LEFT * 0.15 + UP * 0.3)
        
        highlight2 = Ellipse(
            width=0.12,
            height=0.25,
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_width=0
        ).shift(RIGHT * 0.1 + DOWN * 0.2)
        
        # Group all parts - order matters for layering
        carrot_group = VGroup(
            carrot_body,
            texture_lines,
            highlight1,
            highlight2,
            leaves
        )
        
        return carrot_group


