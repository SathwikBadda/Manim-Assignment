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
        
        self.play(FadeIn(title, shift=UP), run_time=1.2)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        
        # No grid lines, keeping background plain
        
        v_line_grid = Line([0, title_bottom, 0], [0, -h/2, 0], color=GRAY, stroke_width=1, stroke_opacity=0.3)
        v_line_grid.set_z_index(3)
        self.add(v_line_grid)
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        right_heading = Text(
            "Estimated vs. Actual Difference",
            font=title_font,
            weight=BOLD,
            font_size=40,
            color="#61D262"
        ).scale(0.5)
        right_heading.move_to([w/4, title_bottom - 0.8, 0])
        right_heading.set_z_index(4)
        
        self.play(FadeIn(right_heading), run_time=1.0)
        
        left_heading = Text(
            "Estimate to Nearest Hundreds",
            font=title_font,
            weight=BOLD,
            font_size=40,
            color="#61D262"
        ).scale(0.5)
        left_heading.move_to([-w/4, title_bottom - 0.8, 0])
        left_heading.set_z_index(4)
        
        self.play(FadeIn(left_heading), run_time=1.0)
        
        # Placeholders for transition grouping (they will stay invisible)
        h_header_left = VGroup().set_z_index(0) 
        line_left_1 = VGroup().set_z_index(0)
        
        # No initial HTO headers in Section 1 anymore, we will add them in sub-steps
        
        num_783 = Text("783", font=title_font, font_size=48, color="#FFFFFF").scale(0.5)
        num_783.move_to([-w/4, title_bottom - 1.5, 0])
        num_783.set_z_index(4)
        
        num_232 = Text("232", font=title_font, font_size=48, color="#FFFFFF").scale(0.5)
        num_232.move_to([-w/4, title_bottom - 4.5, 0])
        num_232.set_z_index(4)
        
        self.play(FadeIn(num_783), run_time=0.8)
        self.play(FadeIn(num_232), run_time=0.8)
        
        self.wait(3.6) # Reached 8.4s total for Section 1 (1.2+1.0+1.0+0.8+0.8+3.6 = 8.4)
        
        ## Section 2
        
        reasoning_1 = wrap_text_dynamic(
            "First, let's round 783 to the nearest hundreds.",
            title_font,
            36, # Double font size
            w/2 - 1.0,
            color="#FFFFFF"
        ).scale(0.5)
        reasoning_1.move_to([w/4, -1.8, 0]) # Match group_1 panel position
        reasoning_1.set_z_index(1) # Behind mask
        
        self.play(Write(reasoning_1), run_time=2.35)
        
        highlight_783 = SurroundingRectangle(num_783, buff=0.15, color="#EF9515")
        highlight_783.set_z_index(4)
        
        self.play(Create(highlight_783), run_time=0.9)
        self.play(Indicate(highlight_783), run_time=1.15)
        
        num_800 = Text("800", font=title_font, font_size=48, color="#FFFFFF").scale(0.5)
        num_800.move_to([-w/4, title_bottom - 1.5, 0])
        num_800.set_z_index(4)
        
        self.play(ReplacementTransform(num_783, num_800), run_time=1.85)
        
        explanation_1 = Text(
            "8 is 5 or more, so round up to 800.",
            font=title_font,
            font_size=56,
            color="#FFFFFF"
        ).scale(0.5)
        explanation_1.move_to([-w/4, title_bottom - 2.8, 0])
        explanation_1.set_z_index(4)
        
        self.play(FadeIn(explanation_1), run_time=1.55)
        
        self.play(reasoning_1.animate.shift(LEFT * w/1.5), run_time=1.85)
        self.remove(reasoning_1)
        
        self.wait(0.27) # Reached 9.92s total (2.35+0.9+1.15+1.85+1.55+1.85+0.27 = 9.92)
        
        ## Section 3
        
        reasoning_2 = wrap_text_dynamic(
            "Now, round 232 to the nearest hundreds.",
            title_font,
            36, # Double font size
            w/2 - 1.0,
            color="#FFFFFF"
        ).scale(0.5)
        reasoning_2.move_to([w/4, -1.8, 0])
        reasoning_2.set_z_index(1) # Behind mask
        
        self.play(Write(reasoning_2), run_time=2.35)
        
        highlight_232 = SurroundingRectangle(num_232, buff=0.15, color="#EF9515")
        highlight_232.set_z_index(4)
        
        self.play(Create(highlight_232), run_time=0.9)
        self.play(Indicate(highlight_232), run_time=1.15)
        
        num_200 = Text("200", font=title_font, font_size=48, color="#FFFFFF").scale(0.5)
        num_200.move_to([-w/4, title_bottom - 4.5, 0])
        num_200.set_z_index(4)
        
        self.play(ReplacementTransform(num_232, num_200), run_time=1.85)
        
        explanation_2 = Text(
            "3 is less than 5, so round down to 200.",
            font=title_font,
            font_size=56,
            color="#FFFFFF"
        ).scale(0.5)
        explanation_2.move_to([-w/4, title_bottom - 6.2, 0])
        explanation_2.set_z_index(4)
        
        self.play(FadeIn(explanation_2), run_time=1.55)
        
        self.play(reasoning_2.animate.shift(LEFT * w/1.5), run_time=1.85)
        self.remove(reasoning_2)
        
        self.wait(0.31) # Reached 9.96s total (2.35+0.9+1.15+1.85+1.55+1.85+0.31 = 9.96)
        
        ## Section 4
        
        reasoning_3 = wrap_text_dynamic(
            "Subtract the rounded numbers.",
            title_font,
            36, # Double font size
            w/2 - 1.0,
            color="#FFFFFF"
        ).scale(0.5)
        reasoning_3.move_to([w/4, -1.8, 0])
        reasoning_3.set_z_index(1)
        
        self.play(Write(reasoning_3), run_time=2.257)
        
        # side-by-side coordinates on right panel
        act_x_c = w/4 + 1.2
        est_x_c = w/4 - 1.2
        
        col_header_h_act = Text("H", font=title_font, font_size=14, color="#FFFFFF").move_to([act_x_c - 0.6, title_bottom - 1.5, 0]).set_z_index(4)
        col_header_t_act = Text("T", font=title_font, font_size=14, color="#FFFFFF").move_to([act_x_c, title_bottom - 1.5, 0]).set_z_index(4)
        col_header_o_act = Text("O", font=title_font, font_size=14, color="#FFFFFF").move_to([act_x_c + 0.6, title_bottom - 1.5, 0]).set_z_index(4)
        struct_line_act = Line([act_x_c - 0.9, title_bottom - 1.7, 0], [act_x_c + 0.9, title_bottom - 1.7, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3).set_z_index(3)
        
        col_header_h_est = Text("H", font=title_font, font_size=14, color="#FFFFFF").move_to([est_x_c - 0.6, title_bottom - 1.5, 0]).set_z_index(4)
        col_header_t_est = Text("T", font=title_font, font_size=14, color="#FFFFFF").move_to([est_x_c, title_bottom - 1.5, 0]).set_z_index(4)
        col_header_o_est = Text("O", font=title_font, font_size=14, color="#FFFFFF").move_to([est_x_c + 0.6, title_bottom - 1.5, 0]).set_z_index(4)
        struct_line_est = Line([est_x_c - 0.9, title_bottom - 1.7, 0], [est_x_c + 0.9, title_bottom - 1.7, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3).set_z_index(3)
        
        self.play(
            FadeIn(col_header_h_act), FadeIn(col_header_t_act), FadeIn(col_header_o_act), Create(struct_line_act),
            FadeIn(col_header_h_est), FadeIn(col_header_t_est), FadeIn(col_header_o_est), Create(struct_line_est),
            run_time=0.6
        )
        
        est_num_800_h = Text("8", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c - 0.6, title_bottom - 2.0, 0]).set_z_index(4)
        est_num_800_t = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c, title_bottom - 2.0, 0]).set_z_index(4)
        est_num_800_o = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c + 0.6, title_bottom - 2.0, 0]).set_z_index(4)
        est_num_800_grp = VGroup(est_num_800_h, est_num_800_t, est_num_800_o)
        
        est_num_200_h = Text("2", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c - 0.6, title_bottom - 2.5, 0]).set_z_index(4)
        est_num_200_t = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c, title_bottom - 2.5, 0]).set_z_index(4)
        est_num_200_o = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c + 0.6, title_bottom - 2.5, 0]).set_z_index(4)
        est_num_200_grp = VGroup(est_num_200_h, est_num_200_t, est_num_200_o)
        
        est_minus = Text("-", font=title_font, font_size=20, color="#FFFFFF")
        est_minus.move_to([est_x_c - 1.0, title_bottom - 2.5, 0])
        est_minus.set_z_index(4)
        
        self.play(FadeIn(est_num_800_grp), run_time=1.057)
        self.play(FadeIn(est_num_200_grp), run_time=1.057)
        self.play(FadeIn(est_minus), run_time=0.814)
        
        est_line = Line([est_x_c - 1.2, title_bottom - 2.8, 0], [est_x_c + 1.2, title_bottom - 2.8, 0], stroke_width=2, color="#FFFFFF")
        est_line.set_z_index(4)
        
        self.play(Create(est_line), run_time=0.914)
        
        est_result_h = Text("6", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c - 0.6, title_bottom - 3.2, 0]).set_z_index(4)
        est_result_t = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c, title_bottom - 3.2, 0]).set_z_index(4)
        est_result_o = Text("0", font=title_font, font_size=20, color="#FFFFFF").move_to([est_x_c + 0.6, title_bottom - 3.2, 0]).set_z_index(4)
        est_result_grp = VGroup(est_result_h, est_result_t, est_result_o)
        
        self.play(FadeIn(est_result_grp), run_time=1.457)
        
        self.play(reasoning_3.animate.shift(LEFT * w/1.5), run_time=1.4)
        self.remove(reasoning_3)
        
        self.wait(0.12) # Reached 9.68s total (2.257+0.6+1.057+1.057+0.814+0.914+1.457+1.4+0.12 = 9.68)
        
        ## Section 5
        
        reasoning_4 = wrap_text_dynamic(
            "Now, let's find the actual difference.",
            title_font,
            36, # Double font size
            w/2 - 1.0,
            color="#FFFFFF"
        ).scale(0.5)
        reasoning_4.move_to([w/4, -1.8, 0])
        reasoning_4.set_z_index(1)
        
        self.play(Write(reasoning_4), run_time=2.0)
        
        act_num_783_h = Text("7", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c - 0.6, title_bottom - 2.0, 0]).set_z_index(4)
        act_num_783_t = Text("8", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c, title_bottom - 2.0, 0]).set_z_index(4)
        act_num_783_o = Text("3", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c + 0.6, title_bottom - 2.0, 0]).set_z_index(4)
        act_num_783_grp = VGroup(act_num_783_h, act_num_783_t, act_num_783_o)
        
        act_num_232_h = Text("2", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c - 0.6, title_bottom - 2.5, 0]).set_z_index(4)
        act_num_232_t = Text("3", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c, title_bottom - 2.5, 0]).set_z_index(4)
        act_num_232_o = Text("2", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c + 0.6, title_bottom - 2.5, 0]).set_z_index(4)
        act_num_232_grp = VGroup(act_num_232_h, act_num_232_t, act_num_232_o)
        
        act_minus = Text("-", font=title_font, font_size=20, color="#FFFFFF")
        act_minus.move_to([act_x_c - 1.0, title_bottom - 2.5, 0])
        act_minus.set_z_index(4)
        
        self.play(FadeIn(act_num_783_grp), run_time=0.8)
        self.play(FadeIn(act_num_232_grp), run_time=0.8)
        self.play(FadeIn(act_minus), run_time=0.4)
        
        act_line = Line([act_x_c - 1.2, title_bottom - 2.8, 0], [act_x_c + 1.2, title_bottom - 2.8, 0], stroke_width=2, color="#FFFFFF")
        act_line.set_z_index(4)
        
        self.play(Create(act_line), run_time=0.8)
        
        act_result_h = Text("5", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c - 0.6, title_bottom - 3.2, 0]).set_z_index(4)
        act_result_t = Text("5", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c, title_bottom - 3.2, 0]).set_z_index(4)
        act_result_o = Text("1", font=title_font, font_size=20, color="#FFFFFF").move_to([act_x_c + 0.6, title_bottom - 3.2, 0]).set_z_index(4)
        act_result_grp = VGroup(act_result_h, act_result_t, act_result_o)
        
        self.play(FadeIn(act_result_grp), run_time=1.2)
        
        self.play(reasoning_4.animate.shift(LEFT * w/1.5), run_time=1.4) # Reduced
        self.remove(reasoning_4)
        
        rect_600 = SurroundingRectangle(est_result_grp, buff=0.15, color="#EF9515", stroke_width=2)
        rect_600.set_z_index(4)
        
        rect_551 = SurroundingRectangle(act_result_grp, buff=0.15, color="#EF9515", stroke_width=2)
        rect_551.set_z_index(4)
        
        self.play(
            Create(rect_600),
            Create(rect_551),
            run_time=0.5
        )
        
        self.play(
            Indicate(est_result_grp),
            Indicate(act_result_grp),
            run_time=0.5
        )
        
        self.wait(2.08) # Reached 10.48s total for Section 5 (2.0+0.8+0.8+0.4+0.8+1.2+1.4+0.5+0.5+2.08 = 10.48)
        
        ## Section 6
        
        self.play(FadeOut(v_line_grid), run_time=0.5)
        
        left_elements = VGroup(
            left_heading, 
            explanation_1, 
            explanation_2, 
            num_800, 
            num_200,
            highlight_783,
            highlight_232,
            h_header_left,
            line_left_1
        )
        
        right_panel_group = VGroup(
            right_heading,
            col_header_h_act,
            col_header_t_act,
            col_header_o_act,
            struct_line_act,
            col_header_h_est,
            col_header_t_est,
            col_header_o_est,
            struct_line_est,
            act_num_783_grp,
            act_num_232_grp,
            act_minus,
            act_line,
            est_num_800_grp,
            est_num_200_grp,
            est_minus,
            est_line
        ) # EXCLUDED est_result_grp, act_result_grp, rect_600, rect_551 so they don't exit
        
        self.play(
            left_elements.animate.shift(LEFT * w), 
            right_panel_group.animate.shift(RIGHT * w),
            run_time=1.0 # Reduced
        )
        
        self.play(
            est_result_grp.animate.move_to([-1.5, 0, 0]),
            rect_600.animate.move_to([-1.5, 0, 0]),
            act_result_grp.animate.move_to([1.5, 0, 0]),
            rect_551.animate.move_to([1.5, 0, 0]),
            run_time=1.0
        )
        
        conclusion_text = Text(
            "The estimated difference (600) is close to the actual difference (551).",
            font=title_font,
            font_size=48,
            color="#FFFFFF"
        ).scale(0.5)
        conclusion_text.move_to([0, -2.5, 0])
        conclusion_text.set_z_index(5)
        
        self.play(Write(conclusion_text), run_time=2.5)
        
        self.wait(5.03) # Reached 12.03s total for Section 6 (0.5+1.0+1.0+2.5+5.03+2.0 = 12.03)
        
        self.play(
            FadeOut(rect_600),
            FadeOut(rect_551),
            run_time=2.0
        )
