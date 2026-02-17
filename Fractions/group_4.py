from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *
import numpy as np

CLOUD_WHITE = "#F9FAFC"
SOFT_VIOLET = "#8B7CF6"
SUNNY_ORANGE = "#FFB703"
LEAF_GREEN = "#4CAF50"
GRAPHITE_GRAY = "#444B55"
BLUE = "#42A5F5"
DARK_GREEN = "#2E7D32"
LIGHT_GREEN = "#A5D6A7"

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = CLOUD_WHITE
        
        self.BELT_START = LEFT * 6 + DOWN * 0.5
        self.BELT_END = RIGHT * 6 + UP * 2.5
        self.TEXT_Y = DOWN * 2.5
        
        self.belt_vec = self.BELT_END - self.BELT_START
        self.anchors = [self.BELT_START + self.belt_vec * (i/4) for i in range(5)]
        
        self.create_belt_system()
        self.setup_prior_elements()
        
        ## Section 1
        self.stage_multiply_label_appear()
        
        #self.wait(6.03)
        ## Section 2
        self.multiplication_operations_reveal()
        
        #self.wait(7.7)
        ## Section 3
        self.multiplication_results_transform()
        
        #self.wait(4.92)
        ## Section 4
        self.final_stage_and_icon()
        
        #self.wait(6.0)
        ## Section 5
        self.visual_rest_and_cleanup_begin()
        
        #self.wait(6.13)
        ## Section 6
        self.full_cleanup_phase()
    
    def get_sigmoid_point(self, x):
        x_min, x_max = -6, 6
        y_min, y_max = -2.5, 2.5
        k = 0.5
        x_0 = 0
        sigmoid = 1 / (1 + np.exp(-k * (x - x_0)))
        y = y_min + (y_max - y_min) * sigmoid
        return np.array([x, y, 0])
    
    def create_belt_system(self):
        x_values = np.linspace(-7, 7, 100)
        points = []
        normals = []
        
        for x in x_values:
            p = self.get_sigmoid_point(x)
            points.append(p)
            p_next = self.get_sigmoid_point(x + 0.01)
            tangent = p_next - p
            tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
            normal = np.array([-tangent[1], tangent[0], 0])
            normals.append(normal)
        
        belt_group = VGroup()
        ribbon_width = 0.6
        
        upper_edge = []
        lower_edge = []
        
        for p, n in zip(points, normals):
            upper_edge.append(p + n * ribbon_width)
            lower_edge.append(p)
        
        top_poly_points = upper_edge + lower_edge[::-1]
        top_surface = Polygon(*top_poly_points, fill_color=LIGHT_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=2)
        
        side_depth = 0.4
        side_edge_points = lower_edge
        side_poly_points = side_edge_points + [p + DOWN * side_depth for p in side_edge_points[::-1]]
        side_surface = Polygon(*side_poly_points, fill_color=DARK_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=1)
        
        belt_group.add(side_surface, top_surface)
        
        moving_elements = VGroup()
        num_items = 45
        self.belt_offsets = np.linspace(0, 14, num_items, endpoint=False)
        self.belt_items = []
        
        for i in range(num_items):
            rivet = Circle(radius=0.04, fill_color="#1A3317", stroke_width=0, fill_opacity=0.8)
            line = Line(ORIGIN, RIGHT * ribbon_width, color="#3A5F0B", stroke_width=2, stroke_opacity=0.6)
            grp = VGroup(rivet, line)
            self.belt_items.append(grp)
            moving_elements.add(grp)
        
        self.belt = belt_group
        self.moving = moving_elements
        
        self.play(DrawBorderThenFill(belt_group), run_time=2)
        self.play(FadeIn(moving_elements), run_time=1)
        
        def robust_move_updater(mob, dt):
            speed = 0.5
            self.belt_offsets = (self.belt_offsets + speed * dt) % 14.0
            current_xs = self.belt_offsets - 7.0
            
            for grp, x in zip(self.belt_items, current_xs):
                rivet = grp[0]
                line = grp[1]
                p = self.get_sigmoid_point(x)
                p_next = self.get_sigmoid_point(x + 0.1)
                tangent = p_next - p
                tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
                normal = np.array([-tangent[1], tangent[0], 0])
                rivet.move_to(p + DOWN * (side_depth/2))
                l_width = 0.55
                start = p + normal * 0.02
                end = p + normal * 0.58
                line.put_start_and_end_on(start, end)
        
        self.moving.add_updater(robust_move_updater)
        
        self.anchors = []
        stage_x_coords = [-5, -2, 0.5, 3, 5.5]
        for x in stage_x_coords:
            p = self.get_sigmoid_point(x)
            p_n = self.get_sigmoid_point(x+0.01)
            t = p_n - p
            t = t/np.linalg.norm(t)
            n = np.array([-t[1], t[0], 0])
            center_top = p + n * (ribbon_width/2)
            self.anchors.append(center_top)
    
    def setup_prior_elements(self):
        title = Text("Magic Numbers!", font_size=56, color=DARK_GREEN, weight=BOLD)
        title.to_edge(UP, buff=0.2)
        self.add(title)
        self.title = title
        
        frac_3_4 = Tex(r"$\frac{3}{4}$", font_size=42, color=DARK_GREEN)
        frac_5_8 = Tex(r"$\frac{5}{8}$", font_size=42, color=DARK_GREEN)
        
        # Position them tentatively, but we will move them in the next method
        # and animate them there.
        frac_3_4.move_to(UP * 1.2 + LEFT * 4.5) # Initial position
        frac_5_8.move_to(UP * 1.2 + LEFT * 1.5) # Initial position
        
        # self.add(frac_3_4, frac_5_8) # REMOVED: Animate them later
        self.frac_3_4 = frac_3_4
        self.frac_5_8 = frac_5_8
    
    def stage_multiply_label_appear(self):
        stage_label = Text(
            "Multiply Numerators & Denominators",
            font_size=28, # Adjusted for Text font
            color=SOFT_VIOLET,
            font="Helvetica",
            weight=BOLD
        )
        stage_label.move_to(UP * 2.5 + LEFT * 3.0)
        
        stage_desc = Tex(
            "Apply the magic numbers to both parts of each fraction.",
            font_size=24,
            color=DARK_GREEN
        )
        stage_desc.next_to(stage_label, DOWN, buff=0.3)
        
        stage_group = VGroup(stage_label, stage_desc)
        
        # --- Layout Logic (Feedback 5) ---
        # 1. Position Fractions (Already created in setup)
        # Move 3/4 further left to make room
        self.frac_3_4.move_to(UP * 1.2 + LEFT * 5.0)
        
        # 2. Position Magic Number 2 and Arrow
        self.magic_2 = Tex("2", font_size=38, color=SUNNY_ORANGE)
        self.magic_2.next_to(self.frac_3_4, RIGHT, buff=1.0) # Gap for arrow
        
        arrow_2 = Arrow(start=self.frac_3_4.get_right(), end=self.magic_2.get_left(), buff=0.1, color=SUNNY_ORANGE)
        
        # 3. Position Fraction 5/8 (Right of 2)
        self.frac_5_8.next_to(self.magic_2, RIGHT, buff=1.0)
        
        # 4. Position Magic Number 1 and Arrow
        self.magic_1 = Tex("1", font_size=38, color=SUNNY_ORANGE)
        self.magic_1.next_to(self.frac_5_8, RIGHT, buff=1.0) # Gap for arrow
        
        arrow_1 = Arrow(start=self.frac_5_8.get_right(), end=self.magic_1.get_left(), buff=0.1, color=SUNNY_ORANGE)

        # --- Animation Phase 1 : Text + Fractions ---
        self.play(
            FadeIn(stage_label, shift=UP * 0.3),
            FadeIn(self.frac_3_4, shift=UP * 0.3),
            FadeIn(self.frac_5_8, shift=UP * 0.3),
            run_time=1.5
        )
        
        # --- Animation Phase 2 : Desc + Magic Numbers + Arrows ---
        self.play(
            FadeIn(stage_desc, shift=UP * 0.2),
            FadeIn(self.magic_2),
            FadeIn(self.magic_1),
            GrowArrow(arrow_2),
            GrowArrow(arrow_1),
            run_time=1.5
        )
        
        self.stage_label_multiply = stage_group
        self.arrows = VGroup(arrow_2, arrow_1)
    
    def multiplication_operations_reveal(self):
        expr_3_4 = Tex(
            r"(3 x 2) / (4 x 2)",
            substrings_to_isolate=["3", "4"],
            font_size=34,
            color=DARK_GREEN
        )
        # Move down slightly (e.g., UP * 2.2)
        expr_3_4.move_to(self.anchors[0] + UP * 2.2)
        
        expr_5_8 = Tex(
            r"(5 x 1) / (8 x 1)",
            substrings_to_isolate=["5", "8"],
            font_size=34,
            color=DARK_GREEN
        )
        expr_5_8.move_to(np.array([self.anchors[1][0], expr_3_4.get_y(), 0]))
        
        self.add(expr_3_4, expr_5_8)
        
        num_3 = expr_3_4.get_part_by_tex("3")
        den_4 = expr_3_4.get_part_by_tex("4")
        num_5 = expr_5_8.get_part_by_tex("5")
        den_8 = expr_5_8.get_part_by_tex("8")
        
        animations = [
            GrowFromCenter(expr_3_4),
            GrowFromCenter(expr_5_8)
        ]
        
        self.play(
            LaggedStart(*animations, lag_ratio=0.3),
            run_time=3.6
        )
        
        self.play(num_3.animate.set_color(BLUE), run_time=1.0)
        self.play(den_4.animate.set_color(SUNNY_ORANGE), run_time=1.0)
        self.play(num_5.animate.set_color(BLUE), run_time=1.0)
        self.play(den_8.animate.set_color(SUNNY_ORANGE), run_time=1.0)
        
        self.expr_3_4 = expr_3_4
        self.expr_5_8 = expr_5_8
    
    def multiplication_results_transform(self):
        intermediate_3_4 = Tex(
            r"$3 \times 2 = 6 \quad 4 \times 2 = 8$",
            font_size=28,
            color=DARK_GREEN
        )
        intermediate_3_4.move_to(self.anchors[0] + UP * 2.2)
        
        self.play(FadeIn(intermediate_3_4), run_time=1.0)
        
        # Bottom Right: Sandwich results between title and desc
        # final_label target is at DOWN * 1.2 + RIGHT * 3.0
        # We'll move results to be just below final_label (DOWN * 1.8)
        result_3_4 = Tex(r"$\frac{6}{8}$", font_size=38, color=DARK_GREEN)
        result_3_4.move_to(DOWN * 1.8 + RIGHT * 2.5)
        
        self.play(ReplacementTransform(intermediate_3_4, result_3_4), run_time=1.0)
        
        intermediate_5_8 = Tex(
            r"$5 \times 1 = 5 \quad 8 \times 1 = 8$",
            font_size=28,
            color=DARK_GREEN
        )
        intermediate_5_8.move_to(self.anchors[1] + UP * 2.2)
        
        self.play(FadeIn(intermediate_5_8), run_time=1.0)
        
        result_5_8 = Tex(r"$\frac{5}{8}$", font_size=38, color=DARK_GREEN)
        result_5_8.move_to(DOWN * 1.8 + RIGHT * 3.5)
        
        self.play(ReplacementTransform(intermediate_5_8, result_5_8), run_time=1.0)
        
        self.play(
            Indicate(result_3_4, color=SUNNY_ORANGE),
            run_time=0.4
        )
        self.play(
            Indicate(result_5_8, color=SUNNY_ORANGE),
            run_time=0.42
        )
        
        self.result_3_4 = result_3_4
        self.result_5_8 = result_5_8
    
    def final_stage_and_icon(self):
        final_label = Text(
            "Our New Like Fractions!",
            font_size=32, # Adjusted for Text font
            color=SOFT_VIOLET,
            font="Helvetica",
            weight=BOLD
        )
        # Move UP further (closer to belt) - DOWN * 1.2
        final_label.move_to(DOWN * 1.2 + RIGHT * 3.0)
        
        final_desc = Tex(
            "Both fractions now share the same denominator (8)!",
            font_size=24,
            color=DARK_GREEN
        )
        # Move desc below the results
        # Results are at y ~ -1.8
        final_desc.next_to(self.result_3_4, DOWN, buff=0.5).set_x(final_label.get_x())
        
        self.play(FadeIn(final_label, shift=UP * 0.3), run_time=1.5)
        self.play(FadeIn(final_desc, shift=UP * 0.2), run_time=1.0)
        
        denom_box_3_4 = SurroundingRectangle(
            self.result_3_4.get_part_by_tex("8"),
            color=SUNNY_ORANGE,
            stroke_width=2,
            buff=0.1
        )
        
        denom_box_5_8 = SurroundingRectangle(
            self.result_5_8.get_part_by_tex("8"),
            color=SUNNY_ORANGE,
            stroke_width=2,
            buff=0.1
        )
        
        self.play(FadeIn(denom_box_3_4), run_time=0.8)
        self.play(FadeIn(denom_box_5_8), run_time=0.8)
        
        # icon = ImageMobject("../images/ace_math_3.png")
        # icon.scale(0.35)
        # icon.move_to(UP * 2.2 + RIGHT * 3.5)
        
        # self.play(GrowFromCenter(icon), run_time=1.9)
        
        self.final_label = final_label
        self.final_desc = final_desc
        self.denom_box_3_4 = denom_box_3_4
        self.denom_box_5_8 = denom_box_5_8
        # self.icon = icon
    
    def visual_rest_and_cleanup_begin(self):
        self.play(
            Indicate(self.result_3_4, color=LEAF_GREEN),
            run_time=1.0
        )
        self.play(
            Indicate(self.result_5_8, color=LEAF_GREEN),
            run_time=1.0
        )
        
        
        # self.play(FadeOut(self.icon), run_time=0.5)
        self.play(FadeOut(self.final_label), run_time=0.5)
        self.play(FadeOut(self.final_desc), run_time=0.5)
        self.play(FadeOut(self.denom_box_3_4), run_time=0.5)
        self.play(FadeOut(self.denom_box_5_8), run_time=0.5)
        
        self.play(
            self.result_3_4.animate.shift(DOWN * 2.0).set_opacity(0),
            run_time=0.73
        )
        self.play(
            self.result_5_8.animate.shift(DOWN * 2.0).set_opacity(0),
            run_time=0.73
        )
    
    def full_cleanup_phase(self):
        # Group all top elements for simultaneous creative exit (Feedback 6)
        top_elements = VGroup(
            self.stage_label_multiply,
            self.expr_3_4,
            self.expr_5_8,
            self.frac_3_4,
            self.frac_5_8,
            self.magic_2,
            self.magic_1,
            self.arrows
        )
        
        # Creative Exit: Shrink and Fade Out together
        self.play(
            FadeOut(top_elements, shift=UP * 2, scale=0.5),
            run_time=1.0
        )
        # self.play(FadeOut(self.stage_label_multiply), run_time=0.5)
        # self.play(FadeOut(self.expr_3_4), run_time=0.5)
        # self.play(FadeOut(self.expr_5_8), run_time=0.5)
        # self.play(FadeOut(self.frac_3_4), run_time=0.5)
        # self.play(FadeOut(self.frac_5_8), run_time=0.5)
        # self.play(FadeOut(self.magic_2), run_time=0.5)
        # self.play(FadeOut(self.magic_1), run_time=0.5)
        # self.play(FadeOut(self.arrows), run_time=0.5)
        
        self.moving.remove_updater(lambda m, dt: None)
        
        self.play(Uncreate(self.belt), run_time=0.6)
        self.play(FadeOut(self.moving), run_time=0.1)
        self.play(FadeOut(self.title), run_time=0.1)
