from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#2C3336"
        
        w = config.frame_width
        h = config.frame_height
        title_font = "Comic Sans MS"
        
        def wrap_text_dynamic(text, font_name, font_size, max_width, color="#FFFFFF", **kwargs):
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_text = Text(" ".join(current_line), font=font_name, font_size=font_size, **kwargs)
                if test_text.width > max_width and len(current_line) > 1:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            vg = VGroup(*[Text(line, font=font_name, font_size=font_size, color=color, **kwargs) for line in lines])
            vg.arrange(DOWN, buff=0.15)
            return vg
        
        ## Section 1
        
        title_string = "Multiplying Larger Numbers"
        title = Text(
            title_string,
            font=title_font,
            weight=BOLD,
            font_size=32,
            color="#61D262"
        )
        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)
        
        self.play(FadeIn(title, shift=UP), run_time=0.867)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        grid_offset = 0.5
        center_y_of_grid = screen_bottom + available_height/2 - grid_offset
        
        v_line_grid = Line([0, title_bottom, 0], [0, -h/2, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3)
        grid_lines = VGroup(v_line_grid)
        grid_lines.set_z_index(3)
        
        self.play(Create(grid_lines), run_time=0.567)
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        top_right_anchor = np.array([w/4, (title_bottom+center_y_of_grid)/2, 0])
        
        y_labels = title_bottom - 1.2
        y_top = title_bottom - 1.9
        y_bot = title_bottom - 2.5
        y_line1 = title_bottom - 2.9
        y_p1 = title_bottom - 3.4
        y_p2 = title_bottom - 4.0
        y_line2 = title_bottom - 4.4
        y_ans = title_bottom - 5.0
        
        x_Th = -w/4 - 0.7
        x_H = -w/4 - 0.2
        x_T = -w/4 + 0.3
        x_O = -w/4 + 0.8
        
        place_value_labels = VGroup(
            Text("Th", font=title_font, font_size=18, color="#FFFFFF").move_to([x_Th, y_labels, 0]),
            Text("H", font=title_font, font_size=18, color="#FFFFFF").move_to([x_H, y_labels, 0]),
            Text("T", font=title_font, font_size=18, color="#FFFFFF").move_to([x_T, y_labels, 0]),
            Text("O", font=title_font, font_size=18, color="#FFFFFF").move_to([x_O, y_labels, 0])
        ).set_z_index(3)
        self.play(Write(place_value_labels), run_time=0.567)
        
        n1 = Text("1", font=title_font, font_size=24, color="#FFFFFF").move_to([x_H, y_top, 0])
        n4_1 = Text("4", font=title_font, font_size=24, color="#FFFFFF").move_to([x_T, y_top, 0])
        n4_2 = Text("4", font=title_font, font_size=24, color="#FFFFFF").move_to([x_O, y_top, 0])
        problem_top = VGroup(n1, n4_1, n4_2).set_z_index(3)
        
        n2 = Text("2", font=title_font, font_size=24, color="#FFFFFF").move_to([x_T, y_bot, 0])
        n8 = Text("8", font=title_font, font_size=24, color="#FFFFFF").move_to([x_O, y_bot, 0])
        problem_bottom = VGroup(n2, n8).set_z_index(3)
        
        mult_symbol = Text("×", font=title_font, font_size=24, color="#FFFFFF").move_to([x_Th, y_bot, 0]).set_z_index(3)
        
        self.play(Write(problem_top), run_time=0.467)
        self.play(Write(VGroup(mult_symbol, problem_bottom)), run_time=0.467)
        
        problem_line = Line(
            [-w/4 - 1.0, y_line1, 0],
            [-w/4 + 1.2, y_line1, 0],
            stroke_width=2,
            color="#FFFFFF"
        ).set_z_index(3)
        self.play(Create(problem_line), run_time=0.367)
        
        right_heading = Text(
            "Step-by-Step Multiplication",
            font=title_font,
            weight=BOLD,
            font_size=20,
            color="#61D262"
        )
        right_heading.move_to([w/4, title_bottom - 0.8, 0])
        
        self.play(Write(right_heading), run_time=0.567)
        
        right_line = Line(
            [w/4 - 1.5, title_bottom - 1.3, 0],
            [w/4 + 1.5, title_bottom - 1.3, 0],
            stroke_width=1,
            color=GRAY,
            stroke_opacity=0.5
        )
        self.play(Create(right_line), run_time=0.367)
        
        self.wait(0.477)
        
        ## Section 2
        
        step1_panel = wrap_text_dynamic(
            "Step 1: Multiply by the ones digit.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step1_panel.move_to([w/4, -1.5, 0])
        step1_panel.set_z_index(1)
        
        self.play(Write(step1_panel), run_time=1.789)
        
        digit_144_rect = SurroundingRectangle(problem_top, buff=0.1, color="#EF9515").set_z_index(3)
        digit_8_rect = SurroundingRectangle(problem_bottom[1], buff=0.1, color="#EF9515").set_z_index(3)
        
        self.play(Create(digit_144_rect), Create(digit_8_rect), run_time=1.389)
        
        p1_2 = Text("2", font=title_font, font_size=24, color="#FFFFFF").move_to([x_O, y_p1, 0])
        p1_5 = Text("5", font=title_font, font_size=24, color="#FFFFFF").move_to([x_T, y_p1, 0])
        p1_1_h = Text("1", font=title_font, font_size=24, color="#FFFFFF").move_to([x_H, y_p1, 0])
        p1_1_th = Text("1", font=title_font, font_size=24, color="#FFFFFF").move_to([x_Th, y_p1, 0])
        p1_11 = VGroup(p1_1_th, p1_1_h)
        partial_product_1 = VGroup(p1_11, p1_5, p1_2).set_z_index(3)
        
        self.play(Write(p1_2), run_time=0.8)
        
        carry_3_t = Text("3", font=title_font, font_size=14, color="#EF9515").next_to(problem_top[1], UP, buff=0.15).set_z_index(3)
        self.play(FadeIn(carry_3_t), run_time=0.5)
        
        self.play(Write(p1_5), run_time=0.8)
        
        carry_3_h = Text("3", font=title_font, font_size=14, color="#EF9515").next_to(problem_top[0], UP, buff=0.15).set_z_index(3)
        self.play(FadeIn(carry_3_h), run_time=0.5)
        
        self.play(Write(p1_11), run_time=0.8)
        
        self.wait(4.633)
        
        self.play(step1_panel.animate.shift(LEFT*w/1.5), run_time=1.919)
        self.remove(step1_panel)
        
        ## Section 3
        
        step2_panel = wrap_text_dynamic(
            "Step 2: Multiply by the tens digit.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step2_panel.move_to([w/4, -1.5, 0])
        step2_panel.set_z_index(1)
        
        self.play(Write(step2_panel), run_time=2.583)
        
        self.play(FadeOut(digit_8_rect), FadeOut(digit_144_rect), FadeOut(carry_3_t), FadeOut(carry_3_h), run_time=0.5)
        
        digit_2_rect = SurroundingRectangle(problem_bottom[0], buff=0.1, color="#EF9515").set_z_index(3)
        digit_144_rect_2 = SurroundingRectangle(problem_top, buff=0.1, color="#EF9515").set_z_index(3)
        self.play(Create(digit_2_rect), Create(digit_144_rect_2), run_time=1.0)
        
        p2_0 = Text("0", font=title_font, font_size=24, color="#FFFFFF").move_to([x_O, y_p2, 0])
        p2_0.set_color("#EF9515")
        p2_8_t = Text("8", font=title_font, font_size=24, color="#FFFFFF").move_to([x_T, y_p2, 0])
        p2_8_h = Text("8", font=title_font, font_size=24, color="#FFFFFF").move_to([x_H, y_p2, 0])
        p2_2_th = Text("2", font=title_font, font_size=24, color="#FFFFFF").move_to([x_Th, y_p2, 0])
        partial_product_2 = VGroup(p2_2_th, p2_8_h, p2_8_t, p2_0).set_z_index(3)
        
        self.play(Write(p2_0), run_time=0.6)
        self.play(Write(p2_8_t), run_time=0.6)
        self.play(Write(p2_8_h), run_time=0.6)
        self.play(Write(p2_2_th), run_time=0.6)
        
        self.play(Indicate(p2_0, color="#EF9515"), run_time=1.0)
        
        self.wait(4.334)
        
        self.play(step2_panel.animate.shift(LEFT*w/1.5), run_time=2.713)
        self.remove(step2_panel)
        
        ## Section 4
        
        step3_panel = wrap_text_dynamic(
            "Step 3: Add the partial products.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step3_panel.move_to([w/4, -1.5, 0])
        step3_panel.set_z_index(1)
        
        self.play(Write(step3_panel), run_time=1.981)
        
        self.play(FadeOut(digit_2_rect), FadeOut(digit_144_rect_2), run_time=0.5)
        
        products_highlight = SurroundingRectangle(
            VGroup(partial_product_1, partial_product_2),
            buff=0.15,
            color="#EF9515"
        )
        products_highlight.set_z_index(3)
        
        self.play(Create(products_highlight), run_time=1.481)
        
        addition_line = Line(
            [-w/4 - 1.0, y_line2, 0],
            [-w/4 + 1.2, y_line2, 0],
            stroke_width=2,
            color="#FFFFFF"
        )
        addition_line.set_z_index(3)
        self.play(Create(addition_line), run_time=1.181)
        
        ans_4 = Text("4", font=title_font, font_size=24, color="#FFFFFF").move_to([x_Th, y_ans, 0])
        ans_0 = Text("0", font=title_font, font_size=24, color="#FFFFFF").move_to([x_H, y_ans, 0])
        ans_3 = Text("3", font=title_font, font_size=24, color="#FFFFFF").move_to([x_T, y_ans, 0])
        ans_2 = Text("2", font=title_font, font_size=24, color="#FFFFFF").move_to([x_O, y_ans, 0])
        final_answer = VGroup(ans_4, ans_0, ans_3, ans_2).set_z_index(3)
        
        self.play(Write(ans_2), run_time=0.4)
        self.play(Write(ans_3), run_time=0.4)
        
        add_carry_1_h = Text("1", font=title_font, font_size=14, color="#EF9515").next_to(p1_1_h, UP, buff=0.15).set_z_index(3)
        self.play(FadeIn(add_carry_1_h), run_time=0.4)
        
        self.play(Write(ans_0), run_time=0.4)
        
        add_carry_1_th = Text("1", font=title_font, font_size=14, color="#EF9515").next_to(p1_1_th, UP, buff=0.15).set_z_index(3)
        self.play(FadeIn(add_carry_1_th), run_time=0.4)
        
        self.play(Write(ans_4), run_time=0.4)
        
        self.wait(4.076)
        
        self.play(step3_panel.animate.shift(LEFT*w/1.5), run_time=2.111)
        self.remove(step3_panel)
        
        ## Section 5
        
        self.wait(3.0)
        
        ## Section 6
        
        fade_out_group = VGroup(
            place_value_labels,
            problem_top,
            problem_bottom,
            mult_symbol,
            problem_line,
            partial_product_1,
            partial_product_2,
            add_carry_1_h,
            add_carry_1_th,
            products_highlight,
            addition_line,
            right_heading,
            right_line,
            grid_lines
        )
        
        self.play(FadeOut(fade_out_group), run_time=1.0)
        
        final_answer_centered = Text("4032", font=title_font, font_size=40, color="#FFFFFF")
        final_answer_centered.move_to([0, 1.5, 0])
        final_answer_centered.set_z_index(5)
        
        self.play(ReplacementTransform(final_answer, final_answer_centered), run_time=1.0)
        
        highlight_box = SurroundingRectangle(final_answer_centered, buff=0.2, color="#EF9515").set_z_index(5)
        self.play(Create(highlight_box), run_time=0.8)
        self.play(final_answer_centered.animate.scale(1.2), run_time=0.8)
        
        concluding_group = VGroup(
            Text("So, ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("144", font=title_font, font_size=20, color="#EF9515"),
            Text(" × ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("28", font=title_font, font_size=20, color="#EF9515"),
            Text(" = ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("4032", font=title_font, font_size=20, color="#EF9515"),
            Text(",", font=title_font, font_size=20, color="#FFFFFF")
        ).arrange(RIGHT, buff=0.05).move_to([0, 0.3, 0]).set_z_index(5)
        
        self.play(Write(concluding_group), run_time=2.0)
        
        self.wait(7.39)
        
        self.play(FadeOut(VGroup(title, final_answer_centered, highlight_box, concluding_group)), run_time=1.0)
