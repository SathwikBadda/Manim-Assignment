from manim import *
import numpy as np

class EggToChickenTransform(Scene):
    def construct(self):
        # Set background color - light, child-friendly
        self.camera.background_color = "#FFF9F0"
        
        # Create shadow (stays on ground, not part of transform)
        shadow = self.create_shadow()
        shadow.shift(DOWN * 2.5)
        
        # Create egg
        egg = self.create_egg()
        egg.shift(DOWN * 0.3)
        
        # Create chicken (same size/position for smooth transform)
        chicken = self.create_chicken()
        chicken.shift(DOWN * 0.3)
        
        # Phase 1: Egg appears with shadow
        self.play(
            FadeIn(shadow, scale=0.9),
            FadeIn(egg, scale=0.8),
            run_time=1.0
        )
        self.wait(0.5)
        
        # Phase 2: Egg wobbles (about to hatch)
        for _ in range(3):
            self.play(
                Rotate(egg, angle=10 * DEGREES, about_point=egg.get_bottom()),
                run_time=0.2
            )
            self.play(
                Rotate(egg, angle=-20 * DEGREES, about_point=egg.get_bottom()),
                run_time=0.2
            )
            self.play(
                Rotate(egg, angle=10 * DEGREES, about_point=egg.get_bottom()),
                run_time=0.2
            )
        
        self.wait(0.3)
        
        # Phase 3: Create crack lines on egg
        cracks = self.create_cracks()
        cracks.move_to(egg.get_center())
        
        self.play(
            Create(cracks),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Phase 4: Egg splits into two halves
        top_shell, bottom_shell = self.create_egg_shells()
        top_shell.move_to(egg.get_center() + UP * 0.3)
        bottom_shell.move_to(egg.get_center() + DOWN * 0.3)
        
        # Remove egg and cracks, add shells
        self.play(
            FadeOut(egg),
            FadeOut(cracks),
            FadeIn(top_shell),
            FadeIn(bottom_shell),
            run_time=0.3
        )
        
        # Shells move apart
        self.play(
            top_shell.animate.shift(UP * 1.2 + LEFT * 0.5).rotate(20 * DEGREES),
            bottom_shell.animate.shift(DOWN * 0.3 + RIGHT * 0.5).rotate(-15 * DEGREES),
            run_time=0.8,
            rate_func=smooth
        )
        
        self.wait(0.2)
        
        # Phase 5: Transform into chicken (chicken appears in place)
        chicken_shadow = self.create_shadow(width=1.8, height=0.35)
        chicken_shadow.shift(DOWN * 2.5)
        
        self.play(
            FadeIn(chicken, scale=0.6),
            Transform(shadow, chicken_shadow),
            run_time=0.8
        )
        
        # Shells fall away
        self.play(
            FadeOut(top_shell, shift=UP * 0.5 + LEFT * 0.5),
            FadeOut(bottom_shell, shift=DOWN * 0.5 + RIGHT * 0.5),
            run_time=0.5
        )
        
        # Phase 6: Chicken bounce
        self.play(
            chicken.animate.shift(UP * 0.2),
            shadow.animate.scale(0.9),
            run_time=0.25,
            rate_func=smooth
        )
        self.play(
            chicken.animate.shift(DOWN * 0.2),
            shadow.animate.scale(1/0.9),
            run_time=0.3,
            rate_func=smooth
        )
        
        # Small second bounce
        self.play(
            chicken.animate.shift(UP * 0.1),
            shadow.animate.scale(0.95),
            run_time=0.2,
            rate_func=smooth
        )
        self.play(
            chicken.animate.shift(DOWN * 0.1),
            shadow.animate.scale(1/0.95),
            run_time=0.25,
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # Phase 7: Happy chirp animation - wings flap
        self.play(
            chicken[4].animate.rotate(20 * DEGREES),  # Left wing
            chicken[5].animate.rotate(-20 * DEGREES),  # Right wing
            run_time=0.3,
            rate_func=there_and_back
        )
        
        self.wait(1.5)
    
    def create_shadow(self, width=1.8, height=0.35):
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
            fill_opacity=0.12,
            stroke_width=0
        )
        return shadow
    
    def create_egg(self):
        """
        Creates an egg using an ellipse.
        
        Returns:
            VGroup containing egg shape
        """
        # Colors
        EGG_WHITE = "#FFFEF7"
        EGG_OUTLINE = "#D4C5B9"
        
        # Main egg body - tall ellipse
        egg_body = Ellipse(
            width=1.6,
            height=2.2,
            fill_color=EGG_WHITE,
            fill_opacity=1,
            stroke_color=EGG_OUTLINE,
            stroke_width=4
        )
        
        # Subtle highlight for 3D effect
        highlight = Ellipse(
            width=0.4,
            height=0.6,
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_width=0
        ).shift(LEFT * 0.3 + UP * 0.4)
        
        egg_group = VGroup(egg_body, highlight)
        return egg_group
    
    def create_cracks(self):
        """
        Creates crack lines on the egg.
        
        Returns:
            VGroup containing crack lines
        """
        CRACK_COLOR = "#8B7355"
        
        cracks = VGroup()
        
        # Main vertical crack
        crack1 = Line(
            start=UP * 0.5,
            end=DOWN * 0.8,
            stroke_color=CRACK_COLOR,
            stroke_width=3
        )
        
        # Branch cracks
        crack2 = Line(
            start=UP * 0.2 + LEFT * 0.1,
            end=LEFT * 0.4 + UP * 0.5,
            stroke_color=CRACK_COLOR,
            stroke_width=2.5
        )
        
        crack3 = Line(
            start=ORIGIN,
            end=RIGHT * 0.5,
            stroke_color=CRACK_COLOR,
            stroke_width=2.5
        )
        
        crack4 = Line(
            start=DOWN * 0.3 + RIGHT * 0.05,
            end=RIGHT * 0.3 + DOWN * 0.7,
            stroke_color=CRACK_COLOR,
            stroke_width=2
        )
        
        crack5 = Line(
            start=DOWN * 0.5 + LEFT * 0.05,
            end=LEFT * 0.35 + DOWN * 0.6,
            stroke_color=CRACK_COLOR,
            stroke_width=2
        )
        
        cracks.add(crack1, crack2, crack3, crack4, crack5)
        return cracks
    
    def create_egg_shells(self):
        """
        Creates two egg shell halves.
        
        Returns:
            Tuple of (top_shell, bottom_shell)
        """
        EGG_WHITE = "#FFFEF7"
        EGG_OUTLINE = "#D4C5B9"
        INNER_COLOR = "#FFF8E7"
        
        # Top shell - curved polygon
        top_points = [
            LEFT * 0.8,
            LEFT * 0.6 + UP * 0.3,
            LEFT * 0.3 + UP * 0.8,
            UP * 1.0,
            RIGHT * 0.3 + UP * 0.8,
            RIGHT * 0.6 + UP * 0.3,
            RIGHT * 0.8,
            RIGHT * 0.5 + DOWN * 0.1,
            LEFT * 0.5 + DOWN * 0.1,
        ]
        
        top_shell = Polygon(
            *top_points,
            fill_color=EGG_WHITE,
            fill_opacity=1,
            stroke_color=EGG_OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Inner edge of top shell (jagged break)
        top_inner = Line(
            start=LEFT * 0.5 + DOWN * 0.1,
            end=RIGHT * 0.5 + DOWN * 0.1,
            stroke_color=INNER_COLOR,
            stroke_width=6
        ).move_to(top_shell.get_bottom() + UP * 0.05)
        
        top_shell_group = VGroup(top_shell, top_inner)
        
        # Bottom shell
        bottom_points = [
            LEFT * 0.8,
            LEFT * 0.6 + DOWN * 0.3,
            LEFT * 0.3 + DOWN * 0.7,
            DOWN * 0.9,
            RIGHT * 0.3 + DOWN * 0.7,
            RIGHT * 0.6 + DOWN * 0.3,
            RIGHT * 0.8,
            RIGHT * 0.5 + UP * 0.1,
            LEFT * 0.5 + UP * 0.1,
        ]
        
        bottom_shell = Polygon(
            *bottom_points,
            fill_color=EGG_WHITE,
            fill_opacity=1,
            stroke_color=EGG_OUTLINE,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Inner edge of bottom shell
        bottom_inner = Line(
            start=LEFT * 0.5 + UP * 0.1,
            end=RIGHT * 0.5 + UP * 0.1,
            stroke_color=INNER_COLOR,
            stroke_width=6
        ).move_to(bottom_shell.get_top() + DOWN * 0.05)
        
        bottom_shell_group = VGroup(bottom_shell, bottom_inner)
        
        return top_shell_group, bottom_shell_group
    
    def create_chicken(self):
        """
        Creates a baby chicken using basic shapes.
        Components: body, head, wings, beak, eyes, feet
        
        Returns:
            VGroup containing all chicken parts
        """
        # Color palette
        CHICK_YELLOW = "#FFD93D"
        CHICK_DARK = "#F7C02B"
        BEAK_ORANGE = "#FF8B3D"
        EYE_BLACK = "#2C2C2C"
        FEET_ORANGE = "#FF9E4F"
        OUTLINE = "#E0AC2D"
        
        # Body - large circle
        body = Circle(
            radius=0.9,
            fill_color=CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        )
        
        # Head - slightly smaller circle
        head = Circle(
            radius=0.65,
            fill_color=CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(UP * 0.9)
        
        # Fluffy tuft on head - small circles
        tuft1 = Circle(
            radius=0.15,
            fill_color=CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(UP * 1.5)
        
        tuft2 = Circle(
            radius=0.12,
            fill_color=CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.15 + UP * 1.45)
        
        tuft3 = Circle(
            radius=0.12,
            fill_color=CHICK_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.15 + UP * 1.45)
        
        # Left wing - teardrop shape (ellipse rotated)
        left_wing = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=CHICK_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).rotate(30 * DEGREES).shift(LEFT * 0.7 + DOWN * 0.1)
        
        # Right wing
        right_wing = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=CHICK_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).rotate(-30 * DEGREES).shift(RIGHT * 0.7 + DOWN * 0.1)
        
        # Beak - small triangle
        beak = Polygon(
            UP * 0.05,
            LEFT * 0.12 + DOWN * 0.1,
            RIGHT * 0.12 + DOWN * 0.1,
            fill_color=BEAK_ORANGE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(UP * 0.75)
        
        # Left eye
        left_eye_white = Circle(
            radius=0.18,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.22 + UP * 1.0)
        
        left_eye_pupil = Circle(
            radius=0.09,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.22 + UP * 1.0)
        
        left_eye_shine = Circle(
            radius=0.04,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.19 + UP * 1.03)
        
        # Right eye
        right_eye_white = Circle(
            radius=0.18,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.22 + UP * 1.0)
        
        right_eye_pupil = Circle(
            radius=0.09,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.22 + UP * 1.0)
        
        right_eye_shine = Circle(
            radius=0.04,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 1.03)
        
        # Feet - small triangular shapes
        left_foot = Polygon(
            UP * 0.05,
            LEFT * 0.2 + DOWN * 0.1,
            LEFT * 0.05 + DOWN * 0.1,
            RIGHT * 0.05 + DOWN * 0.1,
            fill_color=FEET_ORANGE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.3 + DOWN * 0.9)
        
        right_foot = Polygon(
            UP * 0.05,
            RIGHT * 0.2 + DOWN * 0.1,
            RIGHT * 0.05 + DOWN * 0.1,
            LEFT * 0.05 + DOWN * 0.1,
            fill_color=FEET_ORANGE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.3 + DOWN * 0.9)
        
        # Blush marks - pink circles
        left_blush = Ellipse(
            width=0.25,
            height=0.15,
            fill_color="#FFB6C1",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(LEFT * 0.45 + UP * 0.85)
        
        right_blush = Ellipse(
            width=0.25,
            height=0.15,
            fill_color="#FFB6C1",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(RIGHT * 0.45 + UP * 0.85)
        
        # Group all parts - order matters for layering
        chicken_group = VGroup(
            left_foot,
            right_foot,
            left_wing,
            right_wing,
            body,
            head,
            tuft1,
            tuft2,
            tuft3,
            left_eye_white,
            left_eye_pupil,
            left_eye_shine,
            right_eye_white,
            right_eye_pupil,
            right_eye_shine,
            beak,
            left_blush,
            right_blush
        )
        
        return chicken_group


