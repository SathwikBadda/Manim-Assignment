from manim import *
import numpy as np

class CaterpillarToButterflyMetamorphosis(Scene):
    def construct(self):
        # Set background color - soft sky blue
        self.camera.background_color = "#E8F4F8"
        
        # Create shadow (stays on ground throughout)
        shadow = self.create_shadow()
        shadow.shift(DOWN * 2.8)
        
        # Create caterpillar
        caterpillar = self.create_caterpillar()
        caterpillar.shift(DOWN * 0.5)
        
        # Create cocoon (same center for smooth transform)
        cocoon = self.create_cocoon()
        cocoon.shift(DOWN * 0.5)
        
        # Create butterfly (same center for smooth transform)
        butterfly = self.create_butterfly()
        butterfly.shift(DOWN * 0.5)
        
        # ==================== STAGE 1: CATERPILLAR ====================
        
        # Phase 1: Caterpillar appears
        self.play(
            FadeIn(shadow, scale=0.9),
            FadeIn(caterpillar, shift=LEFT * 2),
            run_time=1.2
        )
        self.wait(0.5)
        
        # Phase 2: Caterpillar wiggles/crawls
        for _ in range(2):
            self.play(
                caterpillar.animate.shift(RIGHT * 0.15),
                run_time=0.3
            )
            # Slight vertical wiggle
            self.play(
                caterpillar.animate.shift(UP * 0.05),
                run_time=0.15
            )
            self.play(
                caterpillar.animate.shift(DOWN * 0.05),
                run_time=0.15
            )
        
        self.wait(0.5)
        
        # Phase 3: Caterpillar prepares (antenna wiggle)
        self.play(
            caterpillar[0].animate.rotate(10 * DEGREES),  # Left antenna
            caterpillar[1].animate.rotate(-10 * DEGREES),  # Right antenna
            rate_func=there_and_back,
            run_time=0.6
        )
        
        self.wait(0.3)
        
        # ==================== STAGE 2: COCOON ====================
        
        # Phase 4: Transform to cocoon
        cocoon_shadow = self.create_shadow(width=1.5, height=0.3)
        cocoon_shadow.shift(DOWN * 2.8)
        
        self.play(
            Transform(caterpillar, cocoon),
            Transform(shadow, cocoon_shadow),
            run_time=1.8,
            rate_func=smooth
        )
        
        self.wait(0.8)
        
        # Phase 5: Cocoon pulses (butterfly forming inside)
        for _ in range(3):
            self.play(
                caterpillar.animate.scale(1.08),
                run_time=0.5,
                rate_func=smooth
            )
            self.play(
                caterpillar.animate.scale(1/1.08),
                run_time=0.5,
                rate_func=smooth
            )
        
        self.wait(0.5)
        
        # Phase 6: Cocoon shakes (emergence)
        for _ in range(4):
            self.play(
                caterpillar.animate.rotate(8 * DEGREES),
                run_time=0.15
            )
            self.play(
                caterpillar.animate.rotate(-16 * DEGREES),
                run_time=0.15
            )
            self.play(
                caterpillar.animate.rotate(8 * DEGREES),
                run_time=0.15
            )
        
        self.wait(0.3)
        
        # ==================== STAGE 3: BUTTERFLY ====================
        
        # Phase 7: Transform to butterfly
        butterfly_shadow = self.create_shadow(width=2.2, height=0.4)
        butterfly_shadow.shift(DOWN * 2.8)
        
        self.play(
            Transform(caterpillar, butterfly),
            Transform(shadow, butterfly_shadow),
            run_time=2.0,
            rate_func=smooth
        )
        
        self.wait(0.8)
        
        # Phase 8: Butterfly wing flaps
        for _ in range(3):
            self.play(
                caterpillar[2].animate.rotate(-15 * DEGREES, about_point=caterpillar[2].get_right()),  # Left top wing
                caterpillar[3].animate.rotate(15 * DEGREES, about_point=caterpillar[3].get_left()),   # Right top wing
                caterpillar[4].animate.rotate(-12 * DEGREES, about_point=caterpillar[4].get_right()),  # Left bottom wing
                caterpillar[5].animate.rotate(12 * DEGREES, about_point=caterpillar[5].get_left()),   # Right bottom wing
                run_time=0.4,
                rate_func=smooth
            )
            self.play(
                caterpillar[2].animate.rotate(15 * DEGREES, about_point=caterpillar[2].get_right()),
                caterpillar[3].animate.rotate(-15 * DEGREES, about_point=caterpillar[3].get_left()),
                caterpillar[4].animate.rotate(12 * DEGREES, about_point=caterpillar[4].get_right()),
                caterpillar[5].animate.rotate(-12 * DEGREES, about_point=caterpillar[5].get_left()),
                run_time=0.4,
                rate_func=smooth
            )
        
        self.wait(0.5)
        
        # Phase 9: Butterfly floats upward
        self.play(
            caterpillar.animate.shift(UP * 2),
            shadow.animate.scale(0.7).set_opacity(0.06),
            run_time=2.5,
            rate_func=smooth
        )
        
        # Final wing flap in the air
        self.play(
            caterpillar[2].animate.rotate(-20 * DEGREES, about_point=caterpillar[2].get_right()),
            caterpillar[3].animate.rotate(20 * DEGREES, about_point=caterpillar[3].get_left()),
            caterpillar[4].animate.rotate(-15 * DEGREES, about_point=caterpillar[4].get_right()),
            caterpillar[5].animate.rotate(15 * DEGREES, about_point=caterpillar[5].get_left()),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(1.5)
    
    def create_shadow(self, width=2.0, height=0.35):
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
    
    def create_caterpillar(self):
        """
        Creates a caterpillar using multiple circles.
        Components: antenna, body segments, face
        
        Returns:
            VGroup containing all caterpillar parts
        """
        # Color palette
        CATERPILLAR_GREEN = "#7BC043"
        CATERPILLAR_DARK = "#5A9932"
        ANTENNA_GREEN = "#5A9932"
        EYE_BLACK = "#2C2C2C"
        OUTLINE = "#4A7C2F"
        
        # Antenna - left
        left_antenna = Line(
            start=ORIGIN,
            end=LEFT * 0.25 + UP * 0.4,
            stroke_color=ANTENNA_GREEN,
            stroke_width=4
        ).shift(LEFT * 0.95 + UP * 0.3)
        
        left_antenna_tip = Circle(
            radius=0.08,
            fill_color=ANTENNA_GREEN,
            fill_opacity=1,
            stroke_width=0
        ).move_to(left_antenna.get_end())
        
        # Antenna - right
        right_antenna = Line(
            start=ORIGIN,
            end=RIGHT * 0.25 + UP * 0.4,
            stroke_color=ANTENNA_GREEN,
            stroke_width=4
        ).shift(LEFT * 0.65 + UP * 0.3)
        
        right_antenna_tip = Circle(
            radius=0.08,
            fill_color=ANTENNA_GREEN,
            fill_opacity=1,
            stroke_width=0
        ).move_to(right_antenna.get_end())
        
        # Body segments - 7 circles
        segments = VGroup()
        segment_positions = [
            LEFT * 0.8,           # Head
            LEFT * 0.5,
            LEFT * 0.2,
            RIGHT * 0.1,
            RIGHT * 0.4,
            RIGHT * 0.7,
            RIGHT * 1.0,          # Tail
        ]
        
        for i, pos in enumerate(segment_positions):
            # Alternate sizes for natural look
            if i == 0:  # Head slightly larger
                radius = 0.35
            elif i == len(segment_positions) - 1:  # Tail smaller
                radius = 0.28
            else:
                radius = 0.32
            
            # Alternate colors
            color = CATERPILLAR_GREEN if i % 2 == 0 else CATERPILLAR_DARK
            
            segment = Circle(
                radius=radius,
                fill_color=color,
                fill_opacity=1,
                stroke_color=OUTLINE,
                stroke_width=3
            ).shift(pos)
            
            segments.add(segment)
        
        # Eyes on head (first segment)
        left_eye = Circle(
            radius=0.08,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.88 + UP * 0.08)
        
        right_eye = Circle(
            radius=0.08,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.72 + UP * 0.08)
        
        # Smile - small arc
        smile = Arc(
            radius=0.12,
            start_angle=-PI,
            angle=PI,
            stroke_color=OUTLINE,
            stroke_width=2.5
        ).shift(LEFT * 0.8 + DOWN * 0.05)
        
        # Group all parts
        caterpillar_group = VGroup(
            left_antenna,
            right_antenna,
            left_antenna_tip,
            right_antenna_tip,
            segments,
            left_eye,
            right_eye,
            smile
        )
        
        return caterpillar_group
    
    def create_cocoon(self):
        """
        Creates a cocoon using an ellipse.
        Components: main body, texture lines
        
        Returns:
            VGroup containing cocoon shape
        """
        # Color palette
        COCOON_BROWN = "#B8956A"
        COCOON_DARK = "#9C7A4E"
        OUTLINE = "#7D6240"
        
        # Main cocoon body - vertical oval
        cocoon_body = Ellipse(
            width=1.4,
            height=2.0,
            fill_color=COCOON_BROWN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=4
        )
        
        # Texture lines - horizontal curves
        texture_lines = VGroup()
        num_lines = 6
        for i in range(num_lines):
            y_pos = 0.7 - i * 0.28
            
            line = Arc(
                radius=0.8,
                start_angle=-PI/6,
                angle=PI/3,
                stroke_color=COCOON_DARK,
                stroke_width=2.5,
                stroke_opacity=0.7
            ).shift(UP * y_pos)
            
            texture_lines.add(line)
        
        # Silk attachment point at top
        silk_strand = Line(
            start=UP * 1.0,
            end=UP * 1.5,
            stroke_color=COCOON_DARK,
            stroke_width=3,
            stroke_opacity=0.5
        )
        
        # Highlight for 3D effect
        highlight = Ellipse(
            width=0.4,
            height=0.6,
            fill_color=WHITE,
            fill_opacity=0.2,
            stroke_width=0
        ).shift(LEFT * 0.25 + UP * 0.3)
        
        # Group all parts
        cocoon_group = VGroup(
            cocoon_body,
            highlight,
            texture_lines,
            silk_strand
        )
        
        return cocoon_group
    
    def create_butterfly(self):
        """
        Creates a butterfly using ellipses and arcs.
        Components: wings (4), body, antenna, patterns
        
        Returns:
            VGroup containing all butterfly parts
        """
        # Color palette
        WING_PINK = "#FF6B9D"
        WING_BLUE = "#4ECDC4"
        WING_YELLOW = "#FFE66D"
        BODY_BROWN = "#8B6F47"
        ANTENNA_BROWN = "#6B5537"
        EYE_BLACK = "#2C2C2C"
        OUTLINE = "#5A4632"
        
        # Antenna - left
        left_antenna = Arc(
            radius=0.4,
            start_angle=PI/2,
            angle=PI/3,
            stroke_color=ANTENNA_BROWN,
            stroke_width=4
        ).shift(LEFT * 0.15 + UP * 0.5)
        
        left_antenna_tip = Circle(
            radius=0.08,
            fill_color=ANTENNA_BROWN,
            fill_opacity=1,
            stroke_width=0
        ).move_to(left_antenna.get_start())
        
        # Antenna - right
        right_antenna = Arc(
            radius=0.4,
            start_angle=PI/2,
            angle=2*PI/3,
            stroke_color=ANTENNA_BROWN,
            stroke_width=4
        ).shift(RIGHT * 0.15 + UP * 0.5)
        
        right_antenna_tip = Circle(
            radius=0.08,
            fill_color=ANTENNA_BROWN,
            fill_opacity=1,
            stroke_width=0
        ).move_to(right_antenna.get_start())
        
        # Top wings - left
        left_top_wing = Ellipse(
            width=1.8,
            height=1.4,
            fill_color=WING_PINK,
            fill_opacity=0.9,
            stroke_color=OUTLINE,
            stroke_width=4
        ).rotate(30 * DEGREES).shift(LEFT * 1.0 + UP * 0.3)
        
        # Top wing pattern - left
        left_top_pattern1 = Circle(
            radius=0.25,
            fill_color=WING_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 1.2 + UP * 0.5)
        
        left_top_pattern2 = Circle(
            radius=0.18,
            fill_color=WING_BLUE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.7 + UP * 0.2)
        
        # Top wings - right
        right_top_wing = Ellipse(
            width=1.8,
            height=1.4,
            fill_color=WING_PINK,
            fill_opacity=0.9,
            stroke_color=OUTLINE,
            stroke_width=4
        ).rotate(-30 * DEGREES).shift(RIGHT * 1.0 + UP * 0.3)
        
        # Top wing pattern - right
        right_top_pattern1 = Circle(
            radius=0.25,
            fill_color=WING_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 1.2 + UP * 0.5)
        
        right_top_pattern2 = Circle(
            radius=0.18,
            fill_color=WING_BLUE,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.7 + UP * 0.2)
        
        # Bottom wings - left
        left_bottom_wing = Ellipse(
            width=1.4,
            height=1.1,
            fill_color=WING_BLUE,
            fill_opacity=0.9,
            stroke_color=OUTLINE,
            stroke_width=4
        ).rotate(20 * DEGREES).shift(LEFT * 0.8 + DOWN * 0.5)
        
        # Bottom wing pattern - left
        left_bottom_pattern = Circle(
            radius=0.15,
            fill_color=WING_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.9 + DOWN * 0.4)
        
        # Bottom wings - right
        right_bottom_wing = Ellipse(
            width=1.4,
            height=1.1,
            fill_color=WING_BLUE,
            fill_opacity=0.9,
            stroke_color=OUTLINE,
            stroke_width=4
        ).rotate(-20 * DEGREES).shift(RIGHT * 0.8 + DOWN * 0.5)
        
        # Bottom wing pattern - right
        right_bottom_pattern = Circle(
            radius=0.15,
            fill_color=WING_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.9 + DOWN * 0.4)
        
        # Body - elongated oval
        body = Ellipse(
            width=0.35,
            height=1.2,
            fill_color=BODY_BROWN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        )
        
        # Body segments - horizontal lines
        body_segments = VGroup()
        for i in range(4):
            y_pos = 0.3 - i * 0.25
            segment_line = Line(
                start=LEFT * 0.15 + UP * y_pos,
                end=RIGHT * 0.15 + UP * y_pos,
                stroke_color=OUTLINE,
                stroke_width=2
            )
            body_segments.add(segment_line)
        
        # Head
        head = Circle(
            radius=0.22,
            fill_color=BODY_BROWN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(UP * 0.65)
        
        # Eyes
        left_eye = Circle(
            radius=0.06,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.08 + UP * 0.68)
        
        right_eye = Circle(
            radius=0.06,
            fill_color=EYE_BLACK,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.08 + UP * 0.68)
        
        # Group all parts - order matters for layering
        butterfly_group = VGroup(
            left_antenna,
            right_antenna,
            left_top_wing,
            right_top_wing,
            left_bottom_wing,
            right_bottom_wing,
            left_top_pattern1,
            left_top_pattern2,
            right_top_pattern1,
            right_top_pattern2,
            left_bottom_pattern,
            right_bottom_pattern,
            body,
            body_segments,
            head,
            left_eye,
            right_eye,
            left_antenna_tip,
            right_antenna_tip
        )
        
        return butterfly_group


