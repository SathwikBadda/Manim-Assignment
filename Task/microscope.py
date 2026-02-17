from manim import *

class MicroscopeIcon(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Define colors
        LIGHT_BLUE = "#5DCED9"
        OUTLINE_BLACK = "#000000"
        FILL_WHITE = "#FFFFFF"
        
        # ------------------------------------------------------
        # 1. BASE
        # A trapezoidal platform created using a Polygon with 4 points.
        # Acts as the foundation of the microscope.
        # ------------------------------------------------------
        base_points = [
            [-1.8, -2.5, 0],   # bottom left
            [1.8, -2.5, 0],    # bottom right
            [1.2, -2.0, 0],    # top right
            [-1.2, -2.0, 0]    # top left
        ]
        base = Polygon(
            *base_points,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        )
        
        # Base detail - small triangle cutout
        base_triangle = Polygon(
            [0, -2.3, 0],      # top
            [-0.3, -2.5, 0],   # bottom left
            [0.3, -2.5, 0],    # bottom right
            fill_color=LIGHT_BLUE,
            fill_opacity=1,
            stroke_width=0
        )
        
        # ------------------------------------------------------
        # 2. ARM
        # The curved neck of the microscope.
        # Constructed using two concentric Arcs for outline and
        # an AnnularSector for the white solid fill.
        # ------------------------------------------------------
        # Create the main arm arc
        arm_outer = Arc(
            radius=1.5,
            start_angle=PI/6,
            angle=4*PI/3,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(LEFT * 0.3 + DOWN * 0.5)
        
        arm_inner = Arc(
            radius=1.1,
            start_angle=PI/6,
            angle=4*PI/3,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(LEFT * 0.3 + DOWN * 0.5)
        
        # Fill the arm with white
        arm_fill = AnnularSector(
            inner_radius=1.1,
            outer_radius=1.5,
            angle=4*PI/3,
            start_angle=PI/6,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.3 + DOWN * 0.5)
        
        # 3. ADJUSTMENT KNOB - Circle at the joint
        knob = Circle(
            radius=0.35,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(LEFT * 0.5 + UP * 0.8)
        
        # ------------------------------------------------------
        # 4. EYEPIECE/BODY
        # The tube containing the lenses.
        # Modeled as a rotated RoundedRectangle.
        # ------------------------------------------------------
        eyepiece = RoundedRectangle(
            width=0.8,
            height=1.8,
            corner_radius=0.15,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).rotate(-35 * DEGREES).shift(LEFT * 1.0 + UP * 1.8)
        
        # Eyepiece accent - light blue rectangles at ends
        eyepiece_accent_top = RoundedRectangle(
            width=0.8,
            height=0.4,
            corner_radius=0.15,
            fill_color=LIGHT_BLUE,
            fill_opacity=1,
            stroke_width=0
        ).rotate(-35 * DEGREES).shift(LEFT * 1.35 + UP * 2.45)
        
        eyepiece_accent_bottom = RoundedRectangle(
            width=0.8,
            height=0.4,
            corner_radius=0.15,
            fill_color=LIGHT_BLUE,
            fill_opacity=1,
            stroke_width=0
        ).rotate(-35 * DEGREES).shift(LEFT * 0.65 + UP * 1.15)
        
        # 5. OBJECTIVE LENS - Slanted tube (bottom part)
        objective = RoundedRectangle(
            width=0.7,
            height=1.4,
            corner_radius=0.15,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).rotate(35 * DEGREES).shift(RIGHT * 0.9 + UP * 0.3)
        
        # Objective accent - light blue rectangle at top
        objective_accent = RoundedRectangle(
            width=0.7,
            height=0.35,
            corner_radius=0.15,
            fill_color=LIGHT_BLUE,
            fill_opacity=1,
            stroke_width=0
        ).rotate(35 * DEGREES).shift(RIGHT * 0.55 + UP * 0.85)
        
        # ------------------------------------------------------
        # 6. STAGE
        # The horizontal platform where slides are placed.
        # Consists of a simple Line and a thin Rectangle.
        # ------------------------------------------------------
        stage = Line(
            start=LEFT * 1.5 + DOWN * 0.3,
            end=RIGHT * 1.8 + DOWN * 0.3,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        )
        
        # Stage platform detail
        stage_platform = Rectangle(
            width=3.3,
            height=0.15,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(RIGHT * 0.15 + DOWN * 0.3)
        
        # Add all components in correct order (back to front)
        self.add(base)
        self.add(base_triangle)
        self.add(arm_fill)
        self.add(arm_outer, arm_inner)
        self.add(stage_platform)
        self.add(eyepiece)
        self.add(eyepiece_accent_top, eyepiece_accent_bottom)
        self.add(objective)
        self.add(objective_accent)
        self.add(knob)


class MicroscopeScene(Scene):
    def construct(self):
        # Set white background
        self.camera.background_color = WHITE
        
        # Create microscope icon
        microscope = MicroscopeIcon()
        microscope.scale(0.8)
        
        # Title
        title = Text(
            "Microscope Icon",
            font_size=48,
            color=BLACK
        ).to_edge(UP, buff=0.5)
        
        # Animate title
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # ------------------------------------------------------
        # Assembly Animation
        # Animates the microscope parts appearing one by one,
        # generally building from bottom (base) to top (eyepiece).
        # ------------------------------------------------------
        parts = microscope.submobjects
        
        # Base and platform (indices 0, 1)
        self.play(
            DrawBorderThenFill(parts[0]),  # base
            FadeIn(parts[1]),  # base triangle
            run_time=0.8
        )
        
        # Arm (indices 2, 3, 4)
        self.play(
            FadeIn(parts[2]),  # arm fill
            Create(parts[3]),  # arm outer
            Create(parts[4]),  # arm inner
            run_time=1.2
        )
        
        # Stage (index 5)
        self.play(
            DrawBorderThenFill(parts[5]),  # stage
            run_time=0.6
        )
        
        # Eyepiece with accents (indices 6, 7, 8)
        self.play(
            DrawBorderThenFill(parts[6]),  # eyepiece
            FadeIn(parts[7]),  # top accent
            FadeIn(parts[8]),  # bottom accent
            run_time=0.8
        )
        
        # Objective with accent (indices 9, 10)
        self.play(
            DrawBorderThenFill(parts[9]),  # objective
            FadeIn(parts[10]),  # accent
            run_time=0.8
        )
        
        # Knob (index 11)
        self.play(
            DrawBorderThenFill(parts[11]),  # knob
            run_time=0.5
        )
        
        # Final pause
        self.wait(1)
        
        # Optional: Rotate for 3D effect
        self.play(
            Rotate(microscope, angle=PI/12, axis=UP),
            run_time=1.5,
            rate_func=there_and_back
        )
        
        self.wait(2)


class SimpleMicroscopeScene(Scene):
    """Simpler version with all-at-once creation"""
    def construct(self):
        self.camera.background_color = WHITE
        
        microscope = MicroscopeIcon()
        microscope.scale(0.9)
        
        title = Text(
            "Microscope",
            font_size=42,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP, buff=0.8)
        
        # Simple all-at-once animation
        self.play(
            Write(title),
            DrawBorderThenFill(microscope),
            run_time=2
        )
        
        self.wait(2)