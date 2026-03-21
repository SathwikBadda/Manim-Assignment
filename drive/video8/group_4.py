from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

original_Text = Text
def ScaledText(text, **kwargs):
    fsize = kwargs.get("font_size", 48)
    kwargs["font_size"] = fsize * 2
    return original_Text(text, **kwargs).scale(0.5)
Text = ScaledText

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

        title_string = "Divisibility by 11: A Special Rule"
        title = Text(
            title_string,
            font=title_font,
            font_size=32,
            color="#61D262"
        )
        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)
        
        self.play(FadeIn(title, shift=UP), run_time=1.867)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        grid_offset = 0.5
        center_y_of_grid = screen_bottom + available_height/2 - grid_offset
        
        v_line_grid = Line([0, title_bottom, 0], [0, -h/2, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3)
        grid_lines = VGroup(v_line_grid)
        grid_lines.set_z_index(3)
        
        self.play(Create(grid_lines), run_time=1.567)
        
        left_panel_anchor = np.array([-w/4, (title_bottom + center_y_of_grid)/2, 0])
        right_panel_anchor = np.array([w/4, (title_bottom + center_y_of_grid)/2, 0])
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        self.wait(1.507)

        ## Section 2

        left_heading = Text(
            "Check 95469 for Divisibility by 11",
            font=title_font,
            font_size=20,
            color="#61D262"
        )
        left_heading.move_to(left_panel_anchor + UP*1.0)
        left_heading.set_z_index(3)
        
        self.play(FadeIn(left_heading, shift=UP), run_time=1.257)
        
        number_text = Text(
            "95469",
            font=title_font,
            font_size=48,
            color="#FFFFFF"
        )
        number_text.move_to(left_panel_anchor + DOWN*0.5)
        number_text.set_z_index(3)
        
        self.play(FadeIn(number_text), run_time=0.857)
        
        digit_9_1 = Text("9", font=title_font, font_size=48, color="#FFFFFF")
        digit_9_1.move_to(left_panel_anchor + DOWN*0.5 + LEFT*2.0)
        digit_9_1.set_z_index(3)
        
        digit_5 = Text("5", font=title_font, font_size=48, color="#FFFFFF")
        digit_5.move_to(left_panel_anchor + DOWN*0.5 + LEFT*1.2)
        digit_5.set_z_index(3)
        
        digit_4 = Text("4", font=title_font, font_size=48, color="#FFFFFF")
        digit_4.move_to(left_panel_anchor + DOWN*0.5 + LEFT*0.4)
        digit_4.set_z_index(3)
        
        digit_6 = Text("6", font=title_font, font_size=48, color="#FFFFFF")
        digit_6.move_to(left_panel_anchor + DOWN*0.5 + RIGHT*0.4)
        digit_6.set_z_index(3)
        
        digit_9_2 = Text("9", font=title_font, font_size=48, color="#FFFFFF")
        digit_9_2.move_to(left_panel_anchor + DOWN*0.5 + RIGHT*1.2)
        digit_9_2.set_z_index(3)
        
        self.play(FadeOut(number_text), run_time=0.357)
        
        self.play(FadeIn(digit_9_1), run_time=0.857)
        self.play(FadeIn(digit_5), run_time=0.857)
        self.play(FadeIn(digit_4), run_time=0.857)
        self.play(FadeIn(digit_6), run_time=0.857)
        self.play(FadeIn(digit_9_2), run_time=0.857)
        
        label_1 = Text("1st-odd", font=title_font, font_size=14, color="#EF9515")
        label_1.move_to(digit_9_1.get_bottom() + DOWN*0.5)
        label_1.set_z_index(3)
        
        label_2 = Text("2nd-even", font=title_font, font_size=14, color="#61D262")
        label_2.move_to(digit_5.get_bottom() + DOWN*0.5)
        label_2.set_z_index(3)
        
        label_3 = Text("3rd-odd", font=title_font, font_size=14, color="#EF9515")
        label_3.move_to(digit_4.get_bottom() + DOWN*0.5)
        label_3.set_z_index(3)
        
        label_4 = Text("4th-even", font=title_font, font_size=14, color="#61D262")
        label_4.move_to(digit_6.get_bottom() + DOWN*0.5)
        label_4.set_z_index(3)
        
        label_5 = Text("5th-odd", font=title_font, font_size=14, color="#EF9515")
        label_5.move_to(digit_9_2.get_bottom() + DOWN*0.5)
        label_5.set_z_index(3)
        
        self.play(FadeIn(label_1), run_time=0.657)
        self.play(FadeIn(label_2), run_time=0.657)
        self.play(FadeIn(label_3), run_time=0.657)
        self.play(FadeIn(label_4), run_time=0.657)
        self.play(FadeIn(label_5), run_time=0.657)
        
        self.wait(5.327)

        ## Section 3

        right_heading = Text(
            "Steps to Check Divisibility by 11",
            font=title_font,
            font_size=20,
            color="#61D262"
        )
        right_heading.move_to(right_panel_anchor + UP*1.2)
        right_heading.set_z_index(3)
        
        self.play(Write(right_heading), run_time=1.486)
        
        sep_line = Line(
            right_panel_anchor + LEFT*1.2 + DOWN*0.3,
            right_panel_anchor + RIGHT*1.2 + DOWN*0.3,
            stroke_width=1,
            color=GRAY,
            stroke_opacity=0.3
        )
        sep_line.set_z_index(3)
        
        self.play(Create(sep_line), run_time=1.286)
        
        step1_panel = wrap_text_dynamic(
            "Step 1: Identify Odd and Even Places",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step1_panel.move_to(right_panel_anchor + DOWN*1.5)
        step1_panel.set_z_index(1)
        
        self.play(Write(step1_panel), run_time=2.486)
        
        odd_boxes = VGroup(
            SurroundingRectangle(digit_9_1, buff=0.15, color="#EF9515", stroke_width=2),
            SurroundingRectangle(digit_4, buff=0.15, color="#EF9515", stroke_width=2),
            SurroundingRectangle(digit_9_2, buff=0.15, color="#EF9515", stroke_width=2)
        )
        odd_boxes.set_z_index(3)
        
        even_boxes = VGroup(
            SurroundingRectangle(digit_5, buff=0.15, color="#61D262", stroke_width=2),
            SurroundingRectangle(digit_6, buff=0.15, color="#61D262", stroke_width=2)
        )
        even_boxes.set_z_index(3)
        
        self.play(Create(odd_boxes), run_time=1.686)
        self.play(Create(even_boxes), run_time=1.686)
        
        self.wait(1.986)
        
        self.play(step1_panel.animate.shift(LEFT*w/1.5), run_time=2.066)
        self.remove(step1_panel)

        ## Section 4

        step2_panel = wrap_text_dynamic(
            "Step 2: Sum of Digits in Odd Places",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step2_panel.move_to(right_panel_anchor + DOWN*1.5)
        step2_panel.set_z_index(1)
        
        self.play(Write(step2_panel), run_time=3.06)
        
        calc_odd = Text(
            "9 + 4 + 9 = 22",
            font=title_font,
            font_size=24,
            color="#FFFFFF"
        )
        calc_odd.move_to(right_panel_anchor + DOWN*2.5)
        calc_odd.set_z_index(3)
        
        self.play(FadeIn(calc_odd), run_time=2.76)
        
        odd_highlight = SurroundingRectangle(calc_odd, buff=0.15, color="#EF9515", stroke_width=2)
        odd_highlight.set_z_index(3)
        
        self.play(Create(odd_highlight), run_time=2.56)
        
        self.wait(3.56)
        
        self.play(step2_panel.animate.shift(LEFT*w/1.5), run_time=3.07)
        self.remove(step2_panel)
        self.remove(calc_odd)
        self.remove(odd_highlight)

        ## Section 5

        step3_panel = wrap_text_dynamic(
            "Step 3: Sum of Digits in Even Places",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step3_panel.move_to(right_panel_anchor + DOWN*1.5)
        step3_panel.set_z_index(1)
        
        self.play(Write(step3_panel), run_time=3.28)
        
        calc_even = Text(
            "5 + 6 = 11",
            font=title_font,
            font_size=24,
            color="#FFFFFF"
        )
        calc_even.move_to(right_panel_anchor + DOWN*2.5)
        calc_even.set_z_index(3)
        
        self.play(FadeIn(calc_even), run_time=2.98)
        
        even_highlight = SurroundingRectangle(calc_even, buff=0.15, color="#61D262", stroke_width=2)
        even_highlight.set_z_index(3)
        
        self.play(Create(even_highlight), run_time=2.78)
        
        self.wait(3.78)
        
        self.play(step3_panel.animate.shift(LEFT*w/1.5), run_time=3.42)
        self.remove(step3_panel)
        self.remove(calc_even)
        self.remove(even_highlight)

        ## Section 6

        step4_panel = wrap_text_dynamic(
            "Step 4: Find the Difference",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step4_panel.move_to(right_panel_anchor + DOWN*1.5)
        step4_panel.set_z_index(1)
        
        self.play(Write(step4_panel), run_time=2.75)
        
        calc_diff = Text(
            "22 - 11 = 11",
            font=title_font,
            font_size=24,
            color="#FFFFFF"
        )
        calc_diff.move_to(right_panel_anchor + DOWN*2.5)
        calc_diff.set_z_index(3)
        
        self.play(FadeIn(calc_diff), run_time=2.45)
        
        diff_highlight = SurroundingRectangle(calc_diff, buff=0.15, color="#EF9515", stroke_width=2)
        diff_highlight.set_z_index(3)
        
        self.play(Create(diff_highlight), run_time=2.25)
        self.play(calc_diff.animate.scale(1.15), run_time=2.05)
        
        self.wait(2.75)
        
        self.play(step4_panel.animate.shift(LEFT*w/1.5), run_time=2.78)
        self.remove(step4_panel)
        self.remove(calc_diff)
        self.remove(diff_highlight)

        ## Section 7

        step5_panel = wrap_text_dynamic(
            "Step 5: Check if Difference is Divisible by 11",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        step5_panel.move_to(right_panel_anchor + DOWN*1.5)
        step5_panel.set_z_index(1)
        
        self.play(Write(step5_panel), run_time=2.6)
        
        calc_final = Text(
            "11 ÷ 11 = 1",
            font=title_font,
            font_size=24,
            color="#FFFFFF"
        )
        calc_final.move_to(right_panel_anchor + DOWN*2.3)
        calc_final.set_z_index(3)
        
        self.play(FadeIn(calc_final), run_time=2.1)
        
        confirm_text = Text(
            "Yes, 11 is divisible by 11!",
            font=title_font,
            font_size=18,
            color="#61D262"
        )
        confirm_text.move_to(right_panel_anchor + DOWN*3.0)
        confirm_text.set_z_index(3)
        
        self.play(FadeIn(confirm_text), run_time=2.1)
        
        final_highlight = SurroundingRectangle(calc_final, buff=0.15, color="#61D262", stroke_width=2)
        final_highlight.set_z_index(3)
        
        self.play(Create(final_highlight), run_time=1.9)
        
        self.wait(2.6)
        
        self.play(step5_panel.animate.shift(LEFT*w/1.5), run_time=2.64)
        self.remove(step5_panel)
        self.remove(calc_final)
        self.remove(confirm_text)
        self.remove(final_highlight)

        ## Section 8

        result_panel = Text(
            "Result: Divisible by 11!",
            font=title_font,
            font_size=36,
            color="#61D262",
            weight=BOLD
        )
        result_panel.move_to(right_panel_anchor + DOWN*1.5)
        result_panel.set_z_index(3)
        
        self.play(Write(result_panel), run_time=3.245)
        
        left_cleanup = VGroup(left_heading, digit_9_1, digit_5, digit_4, digit_6, digit_9_2, label_1, label_2, label_3, label_4, label_5, odd_boxes, even_boxes)
        
        right_cleanup = VGroup(right_heading, sep_line)
        
        self.play(left_cleanup.animate.shift(LEFT*w/1.5), run_time=3.545)
        self.play(right_cleanup.animate.shift(RIGHT*w/1.5), FadeOut(grid_lines), run_time=3.545)
        
        self.wait(2.245)

        self.play(result_panel.animate.move_to([0, 1.0, 0]), run_time=2.729)
        
        conclusion = VGroup(
            Text("So, the number", font=title_font, font_size=30, color="#FFFFFF"),
            Text("95469", font=title_font, font_size=30, color="#EF9515"),
            Text("IS", font=title_font, font_size=30, color="#FFFFFF"),
            Text("divisible", font=title_font, font_size=30, color="#EF9515"),
            Text("by 11!", font=title_font, font_size=30, color="#FFFFFF")
        ).arrange(RIGHT, buff=0.25)
        
        conclusion.move_to([0, -0.5, 0])
        conclusion.set_z_index(3)
        
        self.play(FadeIn(conclusion, shift=UP), run_time=2.729)
        
        self.wait(3.229)
        
        self.play(FadeOut(title), run_time=1.729)
        self.play(FadeOut(result_panel), run_time=1.729)
        self.play(FadeOut(conclusion), run_time=1.729)
        
        self.wait(1.709)
