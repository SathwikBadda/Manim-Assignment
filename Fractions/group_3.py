from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *
import numpy as np

BACKGROUND_COLOR = "#E8F5E9"
LIGHT_GREEN = "#A5D6A7"
DARK_GREEN = "#2E7D32"
MEDIUM_GREEN = "#66BB6A"
PLAYFUL_ORANGE = "#FFB703"
HEADER_COLOR = "#F67E7D"  # Blue Grey
MATH_COLOR = "#74546A"    # Black

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        ## Section 1
        title_text = Tex(
            "Let's Convert ", r"$\frac{3}{4}$", " and ", r"$\frac{5}{8}$", "!",
            font_size=48,
            color=DARK_GREEN
        )
        title_text.set_weight(BOLD)
        title_text.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
        
        self.play(Write(title_text), run_time=3.2)
        
        leaf_accent = ImageMobject("../images/ace_math_2.png").scale(0.36)
        leaf_accent.next_to(title_text, RIGHT, buff=0.15)
        leaf_accent.shift(UP * 0.05)
        
        self.play(GrowFromCenter(leaf_accent), run_time=1.8)
        
        self.title_group = Group(title_text, leaf_accent)
        self.wait(0.26)
        
        ## Section 2
        x_values = np.linspace(-7, 7, 120)
        points = []
        normals = []
        
        for x in x_values:
            y = -2.5 + 5.0 / (1 + np.exp(-0.5 * x))
            p = np.array([x, y, 0])
            points.append(p)
            
            y_next = -2.5 + 5.0 / (1 + np.exp(-0.5 * (x + 0.01)))
            p_next = np.array([x + 0.01, y_next, 0])
            tangent = p_next - p
            tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
            normal = np.array([-tangent[1], tangent[0], 0])
            normals.append(normal)
        
        ribbon_width = 0.6
        upper_edge = []
        lower_edge = []
        
        for p, n in zip(points, normals):
            upper_edge.append(p + n * ribbon_width)
            lower_edge.append(p)
        
        top_poly_points = upper_edge + lower_edge[::-1]
        top_surface = Polygon(*top_poly_points, fill_color=LIGHT_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=2)
        
        side_depth = 0.4
        side_poly_points = lower_edge + [p + DOWN * side_depth for p in lower_edge[::-1]]
        side_surface = Polygon(*side_poly_points, fill_color=DARK_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=1)
        
        belt_group = VGroup(side_surface, top_surface)
        
        self.play(DrawBorderThenFill(belt_group), run_time=2.8)
        
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
        
        self.play(FadeIn(moving_elements), run_time=0.94)
        
        def robust_move_updater(mob, dt):
            speed = 0.5  # Reduced speed (was 1.0)
            self.belt_offsets = (self.belt_offsets + speed * dt) % 14.0
            current_xs = self.belt_offsets - 7.0
            
            for grp, x in zip(self.belt_items, current_xs):
                rivet = grp[0]
                line = grp[1]
                
                y = -2.5 + 5.0 / (1 + np.exp(-0.5 * x))
                p = np.array([x, y, 0])
                
                y_next = -2.5 + 5.0 / (1 + np.exp(-0.5 * (x + 0.1)))
                p_next = np.array([x + 0.1, y_next, 0])
                tangent = p_next - p
                tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
                normal = np.array([-tangent[1], tangent[0], 0])
                
                rivet.move_to(p + DOWN * (side_depth / 2))
                
                l_width = 0.55
                start = p + normal * 0.02
                end = p + normal * 0.58
                line.put_start_and_end_on(start, end)
        
        self.moving.add_updater(robust_move_updater)
        
        self.wait(0.1)
        
        ## Section 3
        stage_x_coords = [-5, -2, 0.5, 3, 5.5]
        anchors = []
        for x in stage_x_coords:
            y = -2.5 + 5.0 / (1 + np.exp(-0.5 * x))
            p = np.array([x, y, 0])
            
            y_n = -2.5 + 5.0 / (1 + np.exp(-0.5 * (x + 0.01)))
            p_n = np.array([x + 0.01, y_n, 0])
            t = p_n - p
            t = t / np.linalg.norm(t)
            n = np.array([-t[1], t[0], 0])
            
            center_top = p + n * (ribbon_width / 2)
            anchors.append(center_top)
        
        stage1_anchor = anchors[0]
        
        stage1_label_title = Tex("Start with Fractions", font_size=28, color=HEADER_COLOR)
        stage1_label_title.set_weight(BOLD)
        
        stage1_label = VGroup(stage1_label_title)
        stage1_label = VGroup(stage1_label_title)
        # 1) keep the text start with functions component up of convey belt itself
        stage1_label.move_to(stage1_anchor + UP * 2.5)
        
        frac1 = Tex(r"$\frac{3}{4}$", font_size=44, color=MATH_COLOR)
        frac2 = Tex(r"$\frac{5}{8}$", font_size=44, color=MATH_COLOR)
        fractions = VGroup(frac1, frac2).arrange(RIGHT, buff=0.4)
        # 1) the fractions 3/4 and 5/8 place it above convey belt like down of start with functions
        fractions.next_to(stage1_label, DOWN, buff=0.2)
        
        self.play(FadeIn(stage1_label, shift=UP * 0.3), run_time=1.5)
        self.play(FadeIn(fractions, shift=UP * 0.3), run_time=2.0)
        
        stage1_group = Group(stage1_label, fractions)
        
        self.wait(1.35)
        
        # -----------------------------------------------------------------
        # FIXED SIDE-BY-SIDE LAYOUT STRATEGY
        # -----------------------------------------------------------------
        # We define a fixed bottom area for these calculations to avoid belt overlap.
        # Screen bottom is y=-4. Belt is roughly y=-2.5 to -1.5 in this region.
        # We'll use y=-1.5 to -3.5 for text.
        
        # 2) The text Find The LCM text is overlapping with convey belt move the text right side 
        # and arrows are also to big make it short and move the numbers 4=2*2 and 8 =2*2*2 right side
        LEFT_COL_X = 0.0   # Moved further right from -0.5 to 0.0
        RIGHT_COL_X = 3.8  # Moved slightly right from 2.5 to 3.8 to keep gap
        TITLE_Y = -1.4     # Moved down from -1.0 to -1.4 to avoid belt overlap
        MATH_Y = -2.5
        
        # --- Stage 2: Find LCM (Left Side) ---
        stage2_label_title = Tex("Find the LCM", font_size=28, color=HEADER_COLOR)
        stage2_label_title.set_weight(BOLD)
        
        stage2_label = VGroup(stage2_label_title)
        stage2_label.move_to(np.array([LEFT_COL_X, TITLE_Y, 0]))
        
        self.play(FadeIn(stage2_label, shift=UP * 0.3), run_time=1.0)
        
        factorization1 = Tex(r"$4 = 2 \times 2$", font_size=36, color=MATH_COLOR)
        factorization2 = Tex(r"$8 = 2 \times 2 \times 2$", font_size=36, color=MATH_COLOR)
        factorizations = VGroup(factorization1, factorization2).arrange(DOWN, buff=0.4)
        factorizations.move_to(np.array([LEFT_COL_X, MATH_Y, 0]))
        
        self.play(FadeIn(factorization1, shift=UP * 0.2), run_time=1.2)
        self.play(FadeIn(factorization2, shift=UP * 0.2), run_time=1.2)
        
        lcm_result = Tex(r"$\text{LCM} = 8$", font_size=44, color=MATH_COLOR)
        lcm_result.set_weight(BOLD)
        # Place LCM result below the arrow center
        # Center X is roughly between LEFT_COL_X and RIGHT_COL_X
        # Y is below the equations
        center_x = (LEFT_COL_X + RIGHT_COL_X) / 2
        lcm_result.move_to(np.array([center_x, -3.5, 0]))
        
        self.play(FadeIn(lcm_result, shift=UP * 0.2), run_time=0.75)
        
        lcm_part = lcm_result.get_part_by_tex("8")
        self.play(lcm_part.animate.scale(1.2).set_color(MATH_COLOR), run_time=0.73)
        
        stage2_group = Group(stage2_label, factorizations, lcm_result)
        
        ## Section 5 (Divide)
        
        # --- Stage 3: Divide by Old Denominators (Right Side) ---
        stage3_label_title = Tex("Divide by Old Denominators", font_size=28, color=HEADER_COLOR)
        stage3_label_title.set_weight(BOLD)
        
        stage3_label = VGroup(stage3_label_title)
        stage3_label.move_to(np.array([RIGHT_COL_X, TITLE_Y, 0]))
        
        self.play(FadeIn(stage3_label, shift=UP * 0.3), run_time=1.587)
        
        div1 = Tex(r"$8 \div 4 = $", r"2", font_size=40, color=MATH_COLOR)
        div1[1].set_color(MATH_COLOR) # Result 2
        
        div2 = Tex(r"$8 \div 8 = $", r"1", font_size=40, color=MATH_COLOR)
        div2[1].set_color(MATH_COLOR) # Result 1
        
        # Manually position divisions to align with factorizations for arrows
        div1.move_to(np.array([RIGHT_COL_X, factorization1.get_y(), 0]))
        div2.move_to(np.array([RIGHT_COL_X, factorization2.get_y(), 0]))
        divisions = VGroup(div1, div2)
        
        # Draw Arrows
        arrow1 = Arrow(start=factorization1.get_right(), end=div1.get_left(), color=PLAYFUL_ORANGE, buff=0.2)
        arrow2 = Arrow(start=factorization2.get_right(), end=div2.get_left(), color=PLAYFUL_ORANGE, buff=0.2)
        
        self.play(
            GrowArrow(arrow1),
            FadeIn(div1, shift=LEFT),
            run_time=1.5
        )
        self.play(
            GrowArrow(arrow2),
            FadeIn(div2, shift=LEFT),
            run_time=1.5
        )
        
        # Magic Numbers Label
        magic_text = Tex("Magic", font_size=36, color=PLAYFUL_ORANGE)
        numbers_text = Tex("Numbers!", font_size=36, color=PLAYFUL_ORANGE)
        magic_label = VGroup(magic_text, numbers_text).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        magic_label.set_weight(BOLD)
        # Beside the results (2 and 1) -> Right of divisions
        magic_label.next_to(divisions, RIGHT, buff=0.5)
        
        self.play(FadeIn(magic_label, shift=LEFT), run_time=1.817)
        
        stage3_group = Group(stage3_label, divisions, magic_label, arrow1, arrow2, factorizations, lcm_result, stage2_label)
        
        ## Section 6
        self.play(
            stage3_group.animate.shift(RIGHT * 10),
            FadeOut(stage3_group),
            run_time=3.5
        )
        
        self.wait(0.75)
