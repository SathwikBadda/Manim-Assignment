from manim import *
import numpy as np

# ==================== TEST TUBE RACK ICON ====================

class TestTube(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        LIGHT_BLUE = "#5DCED9"
        FILL_WHITE = "#FFFFFF"
        OUTLINE_BLACK = "#000000"
        
        # ------------------------------------------------------
        # 1. TUBE BODY
        # A RoundedRectangle simulating the glass tube.
        # ------------------------------------------------------
        tube_body = RoundedRectangle(
            width=0.6,
            height=2.2,
            corner_radius=0.3,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        )
        
        # ------------------------------------------------------
        # 2. TOP COVER
        # A white rectangle to cover the top round corners of the body,
        # making the top flat/open.
        # ------------------------------------------------------
        top_cover = Rectangle(
            width=0.6,
            height=0.4,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_width=0
        ).align_to(tube_body, UP).shift(DOWN * 0.2)
        
        # ------------------------------------------------------
        # 3. RIM/LIP
        # A small colored rectangle at the top to represent the
        # thickened glass rim of the test tube.
        # ------------------------------------------------------
        tube_lip = Rectangle(
            width=0.7,
            height=0.2,
            fill_color=LIGHT_BLUE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).next_to(tube_body, UP, buff=0)
        
        self.add(tube_body, top_cover, tube_lip)


class TestTubeRack(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        OUTLINE_BLACK = "#000000"
        
        # ------------------------------------------------------
        # 1. VERTICAL SUPPORTS
        # Two vertical lines on either side representing the rack legs.
        # ------------------------------------------------------
        left_line = Line(
            start=UP * 1.3,
            end=DOWN * 1.3,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(LEFT * 1.2)
        
        right_line = Line(
            start=UP * 1.3,
            end=DOWN * 1.3,
            stroke_color=OUTLINE_BLACK,
            stroke_width=6
        ).shift(RIGHT * 1.2)
        
        # ------------------------------------------------------
        # 2. BASE
        # A thicker horizontal line at the bottom connecting the legs.
        # ------------------------------------------------------
        bottom_line = Line(
            start=LEFT * 1.4,
            end=RIGHT * 1.4,
            stroke_color=OUTLINE_BLACK,
            stroke_width=8
        ).shift(DOWN * 1.3)
        
        self.add(left_line, right_line, bottom_line)


class TestTubeRackIcon(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create rack
        rack = TestTubeRack()
        
        # Create two test tubes
        tube1 = TestTube().shift(LEFT * 0.5 + UP * 0.2)
        tube2 = TestTube().shift(RIGHT * 0.5 + UP * 0.2)
        
        tubes = VGroup(tube1, tube2)
        
        self.add(rack, tubes)
        self.rack = rack
        self.tubes = tubes


class TestTubeRackScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text(
            "Test Tube Rack",
            font_size=42,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP, buff=0.8)
        
        # Create icon
        icon = TestTubeRackIcon()
        icon.scale(0.8)
        
        # Animation sequence
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # Draw rack first
        self.play(
            Create(icon.rack),
            run_time=1.5
        )
        self.wait(0.3)
        
        # Tubes slide in from above
        self.play(
            FadeIn(icon.tubes, shift=DOWN * 2),
            run_time=1.2
        )
        
        self.wait(2)


# ==================== ERLENMEYER FLASK ICON ====================

class ErlenmeyerFlask(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        LIGHT_BLUE = "#5DCED9"
        FILL_WHITE = "#FFFFFF"
        OUTLINE_BLACK = "#000000"
        
        # ------------------------------------------------------
        # 1. FLASK OUTLINE
        # A custom Polygon defining the iconic conical shape of the flask.
        # Includes a narrow neck and a wide triangular base.
        # ------------------------------------------------------
        flask_points = [
            [-0.3, 2.0, 0],    # top left of neck
            [-0.3, 0.8, 0],    # bottom left of neck
            [-1.5, -1.5, 0],   # bottom left of body
            [-1.2, -2.0, 0],   # bottom left corner
            [1.2, -2.0, 0],    # bottom right corner
            [1.5, -1.5, 0],    # bottom right of body
            [0.3, 0.8, 0],     # bottom right of neck
            [0.3, 2.0, 0],     # top right of neck
        ]
        
        flask_outline = Polygon(
            *flask_points,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=8
        ).round_corners(radius=0.15)
        
        # ------------------------------------------------------
        # 2. LIQUID CONTENT
        # A smaller Polygon matching the bottom shape of the flask,
        # filled with semi-transparent blue.
        # ------------------------------------------------------
        liquid_points = [
            [-0.28, 0.5, 0],    # top left
            [-1.35, -1.4, 0],   # bottom left of body
            [-1.1, -1.85, 0],   # bottom left corner
            [1.1, -1.85, 0],    # bottom right corner
            [1.35, -1.4, 0],    # bottom right of body
            [0.28, 0.5, 0],     # top right
        ]
        
        liquid = Polygon(
            *liquid_points,
            fill_color=LIGHT_BLUE,
            fill_opacity=0.8,
            stroke_width=0
        ).round_corners(radius=0.12)
        
        # Liquid surface line (wavy or straight)
        liquid_surface = Line(
            start=[-0.28, 0.5, 0],
            end=[0.28, 0.5, 0],
            stroke_color=LIGHT_BLUE,
            stroke_width=4
        )
        
        # ------------------------------------------------------
        # 3. MOLECULE SYMBOL
        # A central gear/molecule icon to represent science.
        # Consists of a central circle connected to smaller peripheral circles.
        # ------------------------------------------------------
        # Create a simple gear-like or molecule structure
        center_circle = Circle(
            radius=0.25,
            fill_color=FILL_WHITE,
            fill_opacity=1,
            stroke_color=OUTLINE_BLACK,
            stroke_width=4
        ).shift(DOWN * 0.5)
        
        # Small peripheral circles (like atoms or gear teeth)
        peripheral_circles = VGroup()
        num_circles = 6
        for i in range(num_circles):
            angle = i * TAU / num_circles
            pos = np.array([
                0.45 * np.cos(angle),
                0.45 * np.sin(angle) - 0.5,
                0
            ])
            small_circle = Circle(
                radius=0.12,
                fill_color=LIGHT_BLUE,
                fill_opacity=1,
                stroke_color=OUTLINE_BLACK,
                stroke_width=3
            ).move_to(pos)
            peripheral_circles.add(small_circle)
        
        # Lines connecting center to peripheral circles
        connecting_lines = VGroup()
        for circle in peripheral_circles:
            line = Line(
                start=center_circle.get_center(),
                end=circle.get_center(),
                stroke_color=OUTLINE_BLACK,
                stroke_width=3
            )
            connecting_lines.add(line)
        
        molecule_icon = VGroup(connecting_lines, peripheral_circles, center_circle)
        
        self.add(flask_outline, liquid, liquid_surface, molecule_icon)
        self.flask_outline = flask_outline
        self.liquid = liquid
        self.liquid_surface = liquid_surface
        self.molecule_icon = molecule_icon


class ErlenmeyerFlaskScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text(
            "Erlenmeyer Flask",
            font_size=42,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP, buff=0.8)
        
        # Create flask
        flask = ErlenmeyerFlask()
        flask.scale(0.7)
        
        # Animation sequence
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # Draw flask outline
        self.play(
            Create(flask.flask_outline),
            run_time=1.5
        )
        self.wait(0.3)
        
        # Liquid rises from bottom
        flask.liquid.save_state()
        flask.liquid.stretch(0, 1, about_edge=DOWN)
        flask.liquid_surface.set_opacity(0)
        
        self.play(
            Restore(flask.liquid),
            flask.liquid_surface.animate.set_opacity(1),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.3)
        
        # Molecule icon appears
        self.play(
            Write(flask.molecule_icon),
            run_time=1.2
        )
        
        # Optional: gentle bubbling animation
        self.play(
            flask.molecule_icon.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)


# ==================== COMBINED SCENE ====================

class LabEquipmentScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text(
            "Laboratory Equipment",
            font_size=48,
            color=BLACK,
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        
        # Create both icons
        test_tube_rack = TestTubeRackIcon().scale(0.6)
        flask = ErlenmeyerFlask().scale(0.55)
        
        # Position icons side by side
        test_tube_rack.shift(LEFT * 3.2)
        flask.shift(RIGHT * 3)
        
        # Labels
        rack_label = Text(
            "Test Tube Rack",
            font_size=24,
            color=BLACK
        ).next_to(test_tube_rack, DOWN, buff=0.5)
        
        flask_label = Text(
            "Erlenmeyer Flask",
            font_size=24,
            color=BLACK
        ).next_to(flask, DOWN, buff=0.5)
        
        # Animation sequence
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Test tube rack animation
        self.play(
            Create(test_tube_rack.rack),
            Write(rack_label),
            run_time=1.2
        )
        self.play(
            FadeIn(test_tube_rack.tubes, shift=DOWN * 1.5),
            run_time=1
        )
        self.wait(0.5)
        
        # Flask animation
        self.play(
            Create(flask.flask_outline),
            Write(flask_label),
            run_time=1.2
        )
        
        # Liquid rises
        flask.liquid.save_state()
        flask.liquid.stretch(0, 1, about_edge=DOWN)
        flask.liquid_surface.set_opacity(0)
        
        self.play(
            Restore(flask.liquid),
            flask.liquid_surface.animate.set_opacity(1),
            run_time=1.3
        )
        
        self.play(
            Write(flask.molecule_icon),
            run_time=1
        )
        
        self.wait(2)


# ==================== QUICK PREVIEW SCENE ====================

class QuickLabPreview(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Create icons
        rack = TestTubeRackIcon().scale(0.7).shift(LEFT * 3.5)
        flask = ErlenmeyerFlask().scale(0.65).shift(RIGHT * 3.5)
        
        # Show both at once
        self.play(
            FadeIn(rack),
            FadeIn(flask),
            run_time=1.5
        )
        
        self.wait(2)