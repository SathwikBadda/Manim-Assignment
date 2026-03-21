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
            "Multiplication by 2-Digit Numbers",
            font=title_font,
            weight=BOLD,
            font_size=32,
            color="#FFFFFF"
        )
        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)
        
        self.play(FadeIn(title, shift=UP), run_time=1.2)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        
        v_line_grid = Line([0, title_bottom, 0], [0, -h/2, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3)
        v_line_grid.set_z_index(3)
        
        self.play(Create(v_line_grid), run_time=0.8)
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        center_y_of_grid = screen_bottom + available_height/2 - 0.5
        top_left_anchor = np.array([-w/4, (title_bottom + center_y_of_grid)/2, 0])
        
        n5 = Text("5", font=title_font, font_size=24, color="#FFFFFF")
        n3 = Text("3", font=title_font, font_size=24, color="#FFFFFF")
        num_53 = VGroup(n5, n3).arrange(RIGHT, buff=0.15)
        num_53.set_z_index(3).move_to(top_left_anchor + LEFT*0.8 + DOWN*0.3)
        
        mult_symbol = Text("×", font=title_font, font_size=24, color="#FFFFFF")
        mult_symbol.set_z_index(3)
        mult_symbol.next_to(num_53, RIGHT, buff=0.4)
        
        n1 = Text("1", font=title_font, font_size=24, color="#FFFFFF")
        n6 = Text("6", font=title_font, font_size=24, color="#FFFFFF")
        num_16 = VGroup(n1, n6).arrange(RIGHT, buff=0.15)
        num_16.set_z_index(3).move_to(top_left_anchor + LEFT*0.8 + DOWN*0.9)
        
        horiz_line_1 = Line(
            top_left_anchor + LEFT*1.2 + DOWN*1.3,
            top_left_anchor + RIGHT*0.4 + DOWN*1.3,
            stroke_width=2,
            color="#FFFFFF"
        ).set_z_index(3)
        
        self.play(Write(num_53), run_time=0.6)
        self.play(Write(mult_symbol), run_time=0.4)
        self.play(Write(num_16), run_time=0.6)
        self.play(Create(horiz_line_1), run_time=0.5)
        
        right_heading = Text(
            "Multiply Step by Step",
            font=title_font,
            weight=BOLD,
            font_size=22,
            color="#FFFFFF"
        )
        right_heading.move_to([w/4, (title_bottom + center_y_of_grid)/2 + 0.5, 0])
        right_heading.set_z_index(3)
        
        self.play(Write(right_heading), run_time=1.12)
        
        self.wait(0.28)
        
        ## Section 2
        
        panel1_text = wrap_text_dynamic(
            "Step 1: Multiply by the ones digit.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        panel1_text.move_to([w/4, -1.6, 0])
        panel1_text.set_z_index(1)
        
        self.play(Write(panel1_text), run_time=2.32)
        
        digit_6_rect = SurroundingRectangle(
            num_16[1],
            buff=0.1,
            color="#EF9515"
        )
        digit_6_rect.set_z_index(3)
        
        num_53_rect = SurroundingRectangle(
            num_53,
            buff=0.1,
            color="#EF9515"
        )
        num_53_rect.set_z_index(3)
        
        self.play(Create(digit_6_rect), Create(num_53_rect), run_time=1.32)
        
        product_318 = Text("318", font=title_font, font_size=24, color="#FFFFFF")
        product_318.move_to(top_left_anchor + LEFT*0.8 + DOWN*1.7)
        product_318.set_z_index(3)
        
        self.play(Write(product_318[-1]), run_time=0.8)
        
        carried_1 = Text("1", font=title_font, font_size=16, color="#EF9515")
        carried_1.next_to(num_53[0], UP, buff=0.25)
        carried_1.set_z_index(3)
        
        self.play(FadeIn(carried_1), run_time=0.84)
        
        self.play(Write(product_318[0:2]), run_time=1.0)
        
        self.wait(8.1)
        
        ## Section 3
        
        self.play(panel1_text.animate.shift(LEFT*w/1.5), run_time=1.767)
        self.remove(panel1_text)
        
        panel2_text = wrap_text_dynamic(
            "Step 2: Multiply by the tens digit.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        panel2_text.move_to([w/4, -1.6, 0])
        panel2_text.set_z_index(1)
        
        self.play(Write(panel2_text), run_time=2.267)
        
        self.play(FadeOut(digit_6_rect), FadeOut(num_53_rect), FadeOut(carried_1), run_time=0.5)

        digit_1_rect = SurroundingRectangle(
            num_16[0],
            buff=0.1,
            color="#EF9515"
        )
        digit_1_rect.set_z_index(3)
        
        num_53_rect_2 = SurroundingRectangle(
            num_53,
            buff=0.1,
            color="#EF9515"
        )
        num_53_rect_2.set_z_index(3)
        
        self.play(Create(digit_1_rect), Create(num_53_rect_2), run_time=0.767)
        
        product_530 = Text("530", font=title_font, font_size=24, color="#FFFFFF")
        product_530.next_to(product_318, DOWN, buff=0.3)
        product_530.align_to(product_318, RIGHT)
        product_530.set_z_index(3)
        
        product_530[2].set_color("#EF9515")
        
        self.play(Write(product_530[2]), run_time=0.5)
        self.play(Write(product_530[1]), run_time=0.5)
        self.play(Write(product_530[0]), run_time=0.5)
        
        self.play(Indicate(product_530[2], color="#EF9515"), run_time=1.267)
        
        self.wait(7.182)
        
        ## Section 4
        
        self.play(panel2_text.animate.shift(LEFT*w/1.5), run_time=1.533)
        self.remove(panel2_text)
        
        panel3_text = wrap_text_dynamic(
            "Step 3: Add the partial products.",
            title_font,
            18,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        panel3_text.move_to([w/4, -1.5, 0])
        panel3_text.set_z_index(1)
        
        self.play(Write(panel3_text), run_time=1.981)
        
        self.play(FadeOut(digit_1_rect), FadeOut(num_53_rect_2), run_time=0.5)
        
        partial_products_rect = SurroundingRectangle(
            VGroup(product_318, product_530),
            buff=0.15,
            color="#EF9515"
        )
        partial_products_rect.set_z_index(3)
        
        self.play(Create(partial_products_rect), run_time=1.033)
        
        horiz_line_2 = Line(
            top_left_anchor + LEFT*1.2 + DOWN*2.7,
            top_left_anchor + RIGHT*0.4 + DOWN*2.7,
            stroke_width=2,
            color="#FFFFFF"
        )
        horiz_line_2.set_z_index(3)
        
        self.play(Create(horiz_line_2), run_time=0.833)
        
        sum_result = Text("848", font=title_font, font_size=24, color="#FFFFFF")
        sum_result.move_to(top_left_anchor + LEFT*0.8 + DOWN*3.3)
        sum_result.set_z_index(3)
        
        self.play(Write(sum_result[2]), run_time=0.4)
        self.play(Write(sum_result[1]), run_time=0.4)
        self.play(Write(sum_result[0]), run_time=0.4)
        
        self.wait(6.06)
        
        ## Section 5
        
        self.wait(3.0)
        
        ## Section 6
        
        self.play(panel3_text.animate.shift(LEFT*w/1.5), run_time=1.5)
        self.remove(panel3_text)
        
        fade_out_group = VGroup(
            num_53,
            mult_symbol,
            num_16,
            horiz_line_1,
            product_318,
            product_530,
            partial_products_rect,
            horiz_line_2,
            sum_result,
            right_heading,
            v_line_grid
        )
        
        self.play(FadeOut(fade_out_group), run_time=1.0)
        
        sum_result_final = Text("848", font=title_font, font_size=32, color="#FFFFFF")
        sum_result_final.move_to([0, 2.0, 0])
        sum_result_final.set_z_index(5)
        
        self.add(sum_result_final)
        
        result_highlight = SurroundingRectangle(sum_result_final, buff=0.15, color="#EF9515")
        result_highlight.set_z_index(4)
        
        self.play(Create(result_highlight), run_time=0.8)
        self.play(sum_result_final.animate.scale(1.2), run_time=0.8)
        
        conclusion_group = VGroup(
            Text("So, ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("53", font=title_font, font_size=20, color="#EF9515"),
            Text(" × ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("16", font=title_font, font_size=20, color="#EF9515"),
            Text(" = ", font=title_font, font_size=20, color="#FFFFFF"),
            Text("848", font=title_font, font_size=20, color="#EF9515"),
            Text(",", font=title_font, font_size=20, color="#FFFFFF")
        ).arrange(RIGHT, buff=0.05)
        
        conclusion_group.move_to([0, 0.8, 0])
        conclusion_group.set_z_index(5)
        
        self.play(Write(conclusion_group), run_time=2.0)
        
        self.wait(7.97)
        
        fade_final_group = VGroup(
            title,
            sum_result_final,
            result_highlight,
            conclusion_group
        )
        
        self.play(FadeOut(fade_final_group), run_time=1.0)
