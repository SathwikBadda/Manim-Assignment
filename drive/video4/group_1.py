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
        
        title = Text(
            "Estimating the Difference",
            font=title_font,
            weight=BOLD,
            font_size=64,
            color="#61D262"
        ).scale(0.5)
        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)
        
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        
        v_line_grid = Line([0, title_bottom, 0], [0, -h/2, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3)
        grid_lines = VGroup(v_line_grid)
        grid_lines.set_z_index(3)
        
        self.play(Create(grid_lines), run_time=1.0)
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        right_heading = Text(
            "What is Estimation?",
            font=title_font,
            weight=BOLD,
            font_size=22,
            color="#61D262"
        )
        right_heading.move_to([w/4, title_bottom - 0.8, 0])
        right_heading.set_z_index(4)
        
        self.play(FadeIn(right_heading), run_time=1.2)
        
        explanation_text_1 = wrap_text_dynamic(
            "When we don't need an exact answer, we can find a close one quickly! This is called Estimation.",
            title_font,
            16,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        explanation_text_1.move_to([w/4, title_bottom - 2.2, 0])
        explanation_text_1.set_z_index(4)
        
        self.play(Write(explanation_text_1), run_time=3.5)
        
        explanation_text_2 = wrap_text_dynamic(
            "Remember: The rule for rounding numbers to estimate is the same as when we add them.",
            title_font,
            16,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        explanation_text_2.move_to([w/4, title_bottom - 3.6, 0])
        explanation_text_2.set_z_index(4)
        
        self.play(Write(explanation_text_2), run_time=3.24)
        
        self.wait(2.45) # Reduced from 2.55 to reach 12.89s total
        
        ## Section 2
        
        self.play(FadeOut(right_heading), FadeOut(explanation_text_1), FadeOut(explanation_text_2), run_time=1.0)
        
        left_heading = Text(
            "Estimate to Nearest Tens",
            font=title_font,
            weight=BOLD,
            font_size=40,
            color="#61D262"
        ).scale(0.5)
        left_heading.move_to([-w/4, title_bottom - 0.8, 0])
        left_heading.set_z_index(4)
        
        self.play(FadeIn(left_heading), run_time=1.0)
        
        num_69 = Text("69", font=title_font, font_size=72, color="#FFFFFF").scale(0.5)
        num_69.move_to([-w/4, title_bottom - 1.5, 0])
        num_69.set_z_index(4)
        
        num_51 = Text("51", font=title_font, font_size=72, color="#FFFFFF").scale(0.5)
        num_51.move_to([-w/4, title_bottom - 4.5, 0])
        num_51.set_z_index(4)
        
        self.play(FadeIn(num_69), run_time=0.8)
        self.play(FadeIn(num_51), run_time=0.8)
        
        right_heading_2 = Text(
            "Estimated vs. Actual Difference",
            font=title_font,
            weight=BOLD,
            font_size=40,
            color="#61D262"
        ).scale(0.5)
        right_heading_2.move_to([w/4, title_bottom - 0.8, 0])
        right_heading_2.set_z_index(4)
        
        self.play(FadeIn(right_heading_2), run_time=1.0)
        
        act_x_c = w/4 + 1.2
        est_x_c = w/4 - 1.2
        
        col_header_t_act = Text("T", font=title_font, font_size=16, color="#FFFFFF").move_to([act_x_c - 0.3, title_bottom - 1.6, 0]).set_z_index(4)
        col_header_o_act = Text("O", font=title_font, font_size=16, color="#FFFFFF").move_to([act_x_c + 0.3, title_bottom - 1.6, 0]).set_z_index(4)
        struct_line_act = Line([act_x_c - 0.7, title_bottom - 1.8, 0], [act_x_c + 0.7, title_bottom - 1.8, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3).set_z_index(3)
        
        col_header_t_est = Text("T", font=title_font, font_size=16, color="#FFFFFF").move_to([est_x_c - 0.3, title_bottom - 1.6, 0]).set_z_index(4)
        col_header_o_est = Text("O", font=title_font, font_size=16, color="#FFFFFF").move_to([est_x_c + 0.3, title_bottom - 1.6, 0]).set_z_index(4)
        struct_line_est = Line([est_x_c - 0.7, title_bottom - 1.8, 0], [est_x_c + 0.7, title_bottom - 1.8, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3).set_z_index(3)
        
        self.play(
            FadeIn(col_header_t_act), FadeIn(col_header_o_act), Create(struct_line_act),
            FadeIn(col_header_t_est), FadeIn(col_header_o_est), Create(struct_line_est),
            run_time=0.6
        )
        
        self.wait(0.37) # Added to reach 5.57s total for Section 2
        
        
        ## Section 3
        
        reasoning_panel_1 = wrap_text_dynamic(
            "Round 69 to the nearest tens.",
            title_font,
            24,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        reasoning_panel_1.move_to([w/4, -1.8, 0])
        reasoning_panel_1.set_z_index(1)
        
        self.play(Write(reasoning_panel_1), run_time=2.433)
        
        highlight_69 = SurroundingRectangle(num_69, buff=0.2, color="#EF9515")
        highlight_69.set_z_index(4)
        
        self.play(Create(highlight_69), run_time=0.933)
        self.play(Indicate(highlight_69), run_time=1.633)
        
        num_70 = Text("70", font=title_font, font_size=72, color="#FFFFFF").scale(0.5)
        num_70.move_to([-w/4, title_bottom - 1.5, 0])
        num_70.set_z_index(4)
        
        self.play(ReplacementTransform(num_69, num_70), run_time=1.933)
        
        explanation_69 = Text(
            "9 is 5 or more, so round up to 70.",
            font=title_font,
            font_size=56,
            color="#FFFFFF"
        ).scale(0.5)
        explanation_69.move_to([-w/4, title_bottom - 3.2, 0])
        explanation_69.set_z_index(4)
        
        self.play(FadeIn(explanation_69), run_time=1.433)
        
        self.play(reasoning_panel_1.animate.shift(LEFT*w/1.5), run_time=1.875) # Reduced to reach 10.24s total
        self.remove(reasoning_panel_1)
        
        ## Section 4
        
        reasoning_panel_2 = wrap_text_dynamic(
            "Round 51 to the nearest tens.",
            title_font,
            24,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        reasoning_panel_2.move_to([w/4, -1.8, 0])
        reasoning_panel_2.set_z_index(1)
        
        self.play(Write(reasoning_panel_2), run_time=2.067)
        
        highlight_51 = SurroundingRectangle(num_51, buff=0.2, color="#EF9515")
        highlight_51.set_z_index(4)
        
        self.play(Create(highlight_51), run_time=0.767)
        self.play(Indicate(highlight_51), run_time=1.467)
        
        num_50 = Text("50", font=title_font, font_size=72, color="#FFFFFF").scale(0.5)
        num_50.move_to([-w/4, title_bottom - 4.5, 0])
        num_50.set_z_index(4)
        
        self.play(ReplacementTransform(num_51, num_50), run_time=1.767)
        
        explanation_51 = Text(
            "1 is less than 5, so round down to 50.",
            font=title_font,
            font_size=56,
            color="#FFFFFF"
        ).scale(0.5)
        explanation_51.move_to([-w/4, title_bottom - 6.2, 0])
        explanation_51.set_z_index(4)
        
        self.play(FadeIn(explanation_51), run_time=1.267)
        
        self.play(reasoning_panel_2.animate.shift(LEFT*w/1.5), run_time=1.525) # Reduced to reach 8.86s total
        self.remove(reasoning_panel_2)
        
        ## Section 5
        
        reasoning_panel_3 = wrap_text_dynamic(
            "Subtract the rounded numbers.",
            title_font,
            24,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        reasoning_panel_3.move_to([w/4, -1.8, 0])
        reasoning_panel_3.set_z_index(1)
        
        self.play(Write(reasoning_panel_3), run_time=2.214)
        
        est_num_70_t = Text("7", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c - 0.3, title_bottom - 2.1, 0]).set_z_index(4)
        est_num_70_o = Text("0", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c + 0.3, title_bottom - 2.1, 0]).set_z_index(4)
        est_num_70_grp = VGroup(est_num_70_t, est_num_70_o)
        
        est_num_50_t = Text("5", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c - 0.3, title_bottom - 2.8, 0]).set_z_index(4)
        est_num_50_o = Text("0", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c + 0.3, title_bottom - 2.8, 0]).set_z_index(4)
        est_num_50_grp = VGroup(est_num_50_t, est_num_50_o)
        
        est_minus = Text("-", font=title_font, font_size=32, color="#FFFFFF")
        est_minus.move_to([est_x_c - 0.8, title_bottom - 2.8, 0])
        est_minus.set_z_index(4)
        
        self.play(FadeIn(est_num_70_grp), run_time=1.014)
        self.play(FadeIn(est_num_50_grp), run_time=1.014)
        self.play(FadeIn(est_minus), run_time=0.814)
        
        est_line = Line([est_x_c - 1.1, title_bottom - 3.2, 0], [est_x_c + 1.1, title_bottom - 3.2, 0], stroke_width=2, color="#FFFFFF")
        est_line.set_z_index(4)
        
        self.play(Create(est_line), run_time=0.914)
        
        est_result_t = Text("2", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c - 0.3, title_bottom - 3.7, 0]).set_z_index(4)
        est_result_o = Text("0", font=title_font, font_size=32, color="#FFFFFF").move_to([est_x_c + 0.3, title_bottom - 3.7, 0]).set_z_index(4)
        est_result_grp = VGroup(est_result_t, est_result_o)
        
        self.play(FadeIn(est_result_grp), run_time=1.214)
        
        self.play(reasoning_panel_3.animate.shift(LEFT*w/1.5), run_time=1.606) # Reduced to reach 8.79s total
        self.remove(reasoning_panel_3)
        
        ## Section 6
        
        reasoning_panel_4 = wrap_text_dynamic(
            "Now, let's find the actual difference.",
            title_font,
            24,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        reasoning_panel_4.move_to([w/4, -1.8, 0])
        reasoning_panel_4.set_z_index(1)
        
        self.play(Write(reasoning_panel_4), run_time=1.8)
        
        act_num_69_t = Text("6", font=title_font, font_size=32, color="#FFFFFF").move_to([act_x_c - 0.3, title_bottom - 2.1, 0]).set_z_index(4)
        act_num_69_o = Text("9", font=title_font, font_size=32, color="#FFFFFF").move_to([act_x_c + 0.3, title_bottom - 2.1, 0]).set_z_index(4)
        act_num_69_grp = VGroup(act_num_69_t, act_num_69_o)
        
        act_num_51_t = Text("5", font=title_font, font_size=32, color="#FFFFFF").move_to([act_x_c - 0.3, title_bottom - 2.8, 0]).set_z_index(4)
        act_num_51_o = Text("1", font=title_font, font_size=32, color="#FFFFFF").move_to([act_x_c + 0.3, title_bottom - 2.8, 0]).set_z_index(4)
        act_num_51_grp = VGroup(act_num_51_t, act_num_51_o)
        
        act_minus = Text("-", font=title_font, font_size=32, color="#FFFFFF")
        act_minus.move_to([act_x_c - 0.8, title_bottom - 2.8, 0])
        act_minus.set_z_index(4)
        
        self.play(
            FadeIn(act_num_69_grp),
            FadeIn(act_num_51_grp),
            FadeIn(act_minus),
            run_time=0.6 # Parallelized and reduced
        )
        
        self.play(Create(act_line), run_time=0.4)
        
        self.play(FadeIn(act_result_grp), run_time=0.8)
        
        self.play(reasoning_panel_4.animate.shift(LEFT*w/1.5), run_time=0.6) # Reduced
        self.remove(reasoning_panel_4)
        
        highlight_20 = SurroundingRectangle(est_result_grp, buff=0.2, color="#EF9515")
        highlight_20.set_z_index(4)
        
        highlight_18 = SurroundingRectangle(act_result_grp, buff=0.2, color="#EF9515")
        highlight_18.set_z_index(4)
        
        self.play(
            Create(highlight_20),
            Create(highlight_18),
            run_time=0.5
        )
        self.play(
            Indicate(highlight_20),
            Indicate(highlight_18),
            run_time=0.5
        )
        
        self.play(FadeOut(grid_lines), FadeOut(v_line_grid), run_time=0.3)
        
        self.wait(0.3) # Added to reach 7.4s total for Section 6
        
        # Scale to match
        left_panel_group = VGroup(
            left_heading,
            num_70,
            num_50,
            num_69,
            num_51,
            highlight_69,
            highlight_51,
            explanation_69,
            explanation_51
        )
        
        right_panel_group = VGroup(
            right_heading_2,
            col_header_t_act,
            col_header_o_act,
            struct_line_act,
            col_header_t_est,
            col_header_o_est,
            struct_line_est,
            act_num_69_grp,
            act_num_51_grp,
            act_minus,
            act_line,
            est_num_70_grp,
            est_num_50_grp,
            est_minus,
            est_line
        )
        
        self.play(
            left_panel_group.animate.shift(LEFT*w),
            right_panel_group.animate.shift(RIGHT*w),
            run_time=0.8
        ) # Parallelized and reduced
        
        self.play(
            est_result_grp.animate.move_to([-1.5, 0, 0]),
            highlight_20.animate.move_to([-1.5, 0, 0]),
            act_result_grp.animate.move_to([1.5, 0, 0]),
            highlight_18.animate.move_to([1.5, 0, 0]),
            run_time=0.8
        ) # Reduced to reach 7.4s total for Section 6
        
        ## Section 7
        
        conclusion_text = Text(
            "The estimated difference (20) is close to the actual difference (18).",
            font=title_font,
            font_size=40,
            color="#FFFFFF"
        ).scale(0.5)
        conclusion_text.move_to([0, -2.5, 0])
        conclusion_text.set_z_index(5)
        
        self.play(Write(conclusion_text), run_time=3.5)
        
        self.wait(4.74) # Increased to reach 10.24s total (10.24 - 3.5 - 2.0 = 4.74)
        
        self.play(
            FadeOut(highlight_20),
            FadeOut(highlight_18),
            run_time=2.0
        )
