from manim import *
import numpy as np

class PizzaSlice(VGroup):
    def __init__(self, start_angle, end_angle, **kwargs):
        super().__init__(**kwargs)
        
        # Colors matching the image
        CRUST_ORANGE = "#E8A847"
        CRUST_DARK = "#D69132"
        CHEESE_YELLOW = "#F4D58D"
        PEPPERONI_RED = "#E74C3C"
        PEPPERONI_HIGHLIGHT = "#EC7063"
        MUSHROOM_BEIGE = "#C9A663"
        OLIVE_GREEN = "#7D9E5F"
        OUTLINE_DARK = "#4A3C28"
        
        radius = 3.0
        
        # Calculate slice angles
        angle_span = end_angle - start_angle
        
        # ------------------------------------------------------
        # 1. PIZZA SLICE SHAPE
        # Creating a custom polygon to represent a cheese slice.
        # Calculated using trigonometry to create an arc approximation.
        # ------------------------------------------------------
        slice_points = [ORIGIN]
        num_points = 20
        for i in range(num_points + 1):
            angle = start_angle + (angle_span * i / num_points)
            point = np.array([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0
            ])
            slice_points.append(point)
        slice_points.append(ORIGIN)
        
        # Cheese layer
        cheese_slice = Polygon(
            *slice_points,
            fill_color=CHEESE_YELLOW,
            fill_opacity=1,
            stroke_color=OUTLINE_DARK,
            stroke_width=6
        )
        
        # ------------------------------------------------------
        # 2. CRUST DETAIL
        # Using two arcs (outer and inner) to create a thick crust effect.
        # Different colors simulate baking gradients.
        # ------------------------------------------------------
        crust_outer = Arc(
            radius=radius,
            start_angle=start_angle,
            angle=angle_span,
            stroke_color=CRUST_DARK,
            stroke_width=20
        )
        
        crust_inner = Arc(
            radius=radius - 0.15,
            start_angle=start_angle,
            angle=angle_span,
            stroke_color=CRUST_ORANGE,
            stroke_width=14
        )
        
        # ------------------------------------------------------
        # 3. TOPPINGS
        # Adding pepperoni, mushrooms, and olives based on radial positions.
        # ------------------------------------------------------
        # Add highlights on crust
        highlight_positions = [0.2, 0.5, 0.8]
        crust_highlights = VGroup()
        for pos in highlight_positions:
            angle = start_angle + angle_span * pos
            start_point = np.array([
                (radius - 0.25) * np.cos(angle),
                (radius - 0.25) * np.sin(angle),
                0
            ])
            end_point = np.array([
                (radius - 0.05) * np.cos(angle),
                (radius - 0.05) * np.sin(angle),
                0
            ])
            highlight = Line(
                start=start_point,
                end=end_point,
                stroke_color=WHITE,
                stroke_width=4,
                stroke_opacity=0.7
            )
            crust_highlights.add(highlight)
        
        self.add(cheese_slice, crust_outer, crust_inner, crust_highlights)
        
        # Add toppings based on slice position
        mid_angle = (start_angle + end_angle) / 2
        
        # Pepperoni (red circles)
        pepperoni_positions = [
            (radius * 0.5, mid_angle),
            (radius * 0.7, mid_angle + 0.15),
        ]
        
        for r, angle in pepperoni_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            pepperoni = Circle(
                radius=0.25,
                fill_color=PEPPERONI_RED,
                fill_opacity=1,
                stroke_color=OUTLINE_DARK,
                stroke_width=3
            ).move_to(pos)
            
            # Add highlights on pepperoni
            highlight1 = Circle(
                radius=0.06,
                fill_color=PEPPERONI_HIGHLIGHT,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos + UP * 0.08 + LEFT * 0.05)
            
            highlight2 = Circle(
                radius=0.04,
                fill_color=PEPPERONI_HIGHLIGHT,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos + DOWN * 0.07 + RIGHT * 0.08)
            
            self.add(pepperoni, highlight1, highlight2)
        
        # Mushrooms (beige semi-circles)
        mushroom_positions = [
            (radius * 0.65, mid_angle - 0.2),
        ]
        
        for r, angle in mushroom_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            mushroom = Arc(
                radius=0.15,
                start_angle=-PI/2,
                angle=PI,
                fill_color=MUSHROOM_BEIGE,
                fill_opacity=1,
                stroke_color=OUTLINE_DARK,
                stroke_width=3
            ).rotate(angle).move_to(pos)
            
            self.add(mushroom)
        
        # Olives (green ovals)
        olive_positions = [
            (radius * 0.4, mid_angle + 0.25),
        ]
        
        for r, angle in olive_positions:
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            olive = Ellipse(
                width=0.18,
                height=0.25,
                fill_color=OLIVE_GREEN,
                fill_opacity=1,
                stroke_color=OUTLINE_DARK,
                stroke_width=3
            ).move_to(pos)
            
            self.add(olive)


class CompletePizza(VGroup):
    """
    A class representing a whole pizza made of 8 individual slices.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # ------------------------------------------------------
        # Create 8 perfectly aligned slices
        # ------------------------------------------------------
        num_slices = 8
        slice_angle = TAU / num_slices
        
        slices = VGroup()
        for i in range(num_slices):
            start_angle = i * slice_angle
            end_angle = (i + 1) * slice_angle
            
            slice = PizzaSlice(start_angle, end_angle)
            slices.add(slice)
        
        self.add(slices)
        self.slices = slices


class PizzaScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text(
            "Pizza Icon",
            font_size=48,
            color="#4A3C28",
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        
        # Create complete pizza
        pizza = CompletePizza()
        pizza.scale(0.5)
        
        # Animation: Draw pizza slice by slice
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # Draw all slices simultaneously with rotation
        self.play(
            *[
                Create(slice, run_time=1.5)
                for slice in pizza.slices
            ]
        )
        
        self.wait(1)
        
        # Slice separation animation - one slice pulls out
        # Use the actual slice object to move it, leaving a gap
        pulled_slice = pizza.slices[1]
        
        self.play(
            pulled_slice.animate.shift(UP * 0.8 + LEFT * 0.5).rotate(15 * DEGREES),
            run_time=1.2,
            rate_func=smooth
        )
        
        self.wait(2)


class PizzaAssemblyScene(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        title = Text(
            "Pizza Assembly",
            font_size=42,
            color="#4A3C28",
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        
        pizza = CompletePizza()
        pizza.scale(0.5)
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        # Slices fly in from different directions
        for i, slice in enumerate(pizza.slices):
            angle = i * TAU / 8
            direction = np.array([np.cos(angle), np.sin(angle), 0]) * 5
            slice.shift(direction)
        
        self.play(
            *[
                slice.animate.shift(-slice.get_center() + ORIGIN)
                for slice in pizza.slices
            ],
            run_time=2,
            rate_func=smooth
        )
        
        # Rotate the complete pizza
        self.play(
            Rotate(pizza, angle=TAU, run_time=3, rate_func=linear)
        )
        
        self.wait(1)


class PizzaSliceShowcase(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        
        title = Text(
            "Pizza Varieties",
            font_size=42,
            color="#4A3C28",
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        
        # Create individual slices
        slice1 = PizzaSlice(0, TAU/8).scale(0.4).shift(LEFT * 4)
        slice2 = PizzaSlice(TAU/8, TAU/4).scale(0.4)
        slice3 = PizzaSlice(TAU/4, 3*TAU/8).scale(0.4).shift(RIGHT * 4)
        
        labels = VGroup(
            Text("Slice 1", font_size=24, color="#4A3C28").next_to(slice1, DOWN),
            Text("Slice 2", font_size=24, color="#4A3C28").next_to(slice2, DOWN),
            Text("Slice 3", font_size=24, color="#4A3C28").next_to(slice3, DOWN)
        )
        
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        
        self.play(
            FadeIn(slice1, shift=UP),
            FadeIn(slice2, shift=UP),
            FadeIn(slice3, shift=UP),
            Write(labels),
            run_time=1.5,
            lag_ratio=0.3
        )
        
class PizzaIntegrationScene(Scene):
    """
    Combined scene showing:
    1. A complete pizza appearing.
    2. Exploding into slices that move to corners.
    3. Reassembling back into a whole pizza.
    """
    def construct(self):
        self.camera.background_color = WHITE
        
        # Title
        title = Text(
            "Pizza Integration",
            font_size=42,
            color="#4A3C28",
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=0.8)
        
        # ------------------------------------------------------
        # 1. INITIAL STATE
        # Start with full pizza (Assemble instantly or Create)
        # ------------------------------------------------------
        pizza = CompletePizza()
        pizza.scale(0.5)
        
        self.play(FadeIn(pizza, scale=0.8), run_time=1)
        self.wait(0.5)
        
        # Save state to return to purely for the re-assembly target
        pizza.slices.save_state()
        
        # ------------------------------------------------------
        # 2. EXPLOSION ANIMATION
        # Move slices outwards to corners/edges of the screen.
        # We calculate a vector based on the slice's angle.
        # ------------------------------------------------------
        anims = []
        for i, slice in enumerate(pizza.slices):
            angle = i * TAU / 8
            # Push further out (radius 4.5 ensures they hit edges)
            vect = np.array([np.cos(angle), np.sin(angle), 0]) * 4.5
            # Rotate slightly for dynamic effect
            anims.append(slice.animate.shift(vect).rotate(angle/2))
            
        self.play(*anims, run_time=1.5, rate_func=rate_functions.ease_in_out_quart)
        self.wait(1)
        
        # ------------------------------------------------------
        # 3. ASSEMBLY ANIMATION
        # Restore slices to their original saved state (center).
        # Uses 'ease_out_elastic' for a satisfying snap-back effect.
        # ------------------------------------------------------
        self.play(
            Restore(pizza.slices),
            run_time=2,
            rate_func=rate_functions.ease_out_elastic
        )
        
        self.wait(2)


