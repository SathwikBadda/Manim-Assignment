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
            "Estimating the Product: Examples",
            font=title_font,
            font_size=32,
            color="#61D262"
        )
        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)
        
        self.play(FadeIn(title, shift=UP), run_time=2.0)
        
        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2
        available_height = title_bottom - screen_bottom
        grid_offset = 0.5
        center_y_of_grid = screen_bottom + available_height/2 - grid_offset
        
        v_line_grid = Line([-1.0, title_bottom, 0], [-1.0, -h/2, 0], stroke_width=1, color=GRAY, stroke_opacity=0.3)
        grid_lines = VGroup(v_line_grid)
        grid_lines.set_z_index(3)
        
        self.play(Create(grid_lines), run_time=1.5)
        
        left_mask = Rectangle(width=w/2+0.5, height=h, fill_color="#2C3336", fill_opacity=1, stroke_width=0)
        left_mask.move_to([-w/4, 0, 0])
        left_mask.set_z_index(2)
        self.add(left_mask)
        
        problem1 = Text(
            "Estimate the product of 891 x 12",
            font=title_font,
            font_size=20,
            color="#FFFFFF"
        )
        problem1.move_to([-w/4, center_y_of_grid + 1.0, 0])
        problem1.set_z_index(3)
        
        problem2 = Text(
            "Estimate the product of 4428 x 36",
            font=title_font,
            font_size=20,
            color="#FFFFFF"
        )
        problem2.move_to([-w/4, center_y_of_grid - 0.5, 0])
        problem2.set_z_index(3)
        
        self.play(FadeIn(problem1, shift=UP), run_time=1.5)
        self.play(FadeIn(problem2, shift=UP), run_time=1.5)
        
        self.wait(3.54)
        
        ## Section 2
        
        top_right_anchor = np.array([w/4, (title_bottom + center_y_of_grid)/2, 0])
        
        example1_heading = Text(
            "Example 1: 891 x 12",
            font=title_font,
            font_size=22,
            color="#61D262"
        )
        example1_heading.move_to(top_right_anchor + UP*1.2)
        example1_heading.set_z_index(3)
        
        self.play(FadeIn(example1_heading, shift=UP), run_time=1.0)
        
        panel1_text = wrap_text_dynamic("Round 891 to the nearest hundreds (900).", title_font, 18, w/2 - 1.0)
        panel1_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel1_text.set_z_index(3)
        self.play(FadeIn(panel1_text, shift=UP), run_time=1.5)
        
        rect891 = SurroundingRectangle(problem1, buff=0.15, color="#EF9515"); rect891.set_z_index(3)
        self.play(Create(rect891), run_time=0.8)
        
        base_layout1 = Text("   891", font=title_font, font_size=20, color="#FFFFFF")
        base_layout1.move_to(top_right_anchor + LEFT*1.0 + DOWN*0.3); base_layout1.set_z_index(3)
        self.play(FadeIn(base_layout1), run_time=0.8)
        
        arrow1 = Arrow(start=top_right_anchor + LEFT*0.2 + DOWN*0.3, end=top_right_anchor + RIGHT*0.8 + DOWN*0.3, color=WHITE, buff=0.1); arrow1.set_z_index(3)
        self.play(Create(arrow1), run_time=0.5)

        num900_1 = Text("900", font=title_font, font_size=20, color="#FFFFFF")
        num900_1.move_to(top_right_anchor + RIGHT*1.5 + DOWN*0.3); num900_1.set_z_index(3)
        self.play(FadeIn(num900_1), run_time=0.8)
        
        self.wait(0.8)
        self.play(FadeOut(panel1_text), FadeOut(rect891), run_time=0.5)
        
        panel2_text = wrap_text_dynamic("Round 12 to the nearest tens (10).", title_font, 18, w/2 - 1.0)
        panel2_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel2_text.set_z_index(3)
        self.play(FadeIn(panel2_text, shift=UP), run_time=1.5)
        
        rect12 = SurroundingRectangle(problem1, buff=0.15, color="#EF9515"); rect12.set_z_index(3)
        self.play(Create(rect12), run_time=0.8)
        
        base_layout2 = Text(" x  12", font=title_font, font_size=20, color="#FFFFFF")
        base_layout2.move_to(top_right_anchor + LEFT*1.0 + DOWN*0.8); base_layout2.set_z_index(3)
        self.play(FadeIn(base_layout2), run_time=0.8)

        arrow2 = Arrow(start=top_right_anchor + LEFT*0.2 + DOWN*0.8, end=top_right_anchor + RIGHT*0.8 + DOWN*0.8, color=WHITE, buff=0.1); arrow2.set_z_index(3)
        self.play(Create(arrow2), run_time=0.5)

        num10_1 = Text("x 10", font=title_font, font_size=20, color="#FFFFFF")
        num10_1.move_to(top_right_anchor + RIGHT*1.5 + DOWN*0.8); num10_1.set_z_index(3)
        self.play(FadeIn(num10_1), run_time=0.8)
        
        self.wait(0.8)
        self.play(FadeOut(panel2_text), FadeOut(rect12), run_time=0.5)
        self.wait(3.35)
        
        ## Section 3
        
        panel3_text = wrap_text_dynamic("Estimated Product: 900 x 10 = 9000", title_font, 20, w/2 - 1.0, color="#FFFFFF")
        panel3_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel3_text.set_z_index(3)
        self.play(FadeIn(panel3_text, shift=UP), run_time=2.0)
        
        line_est = Line(top_right_anchor + RIGHT*0.8 + DOWN*1.1, top_right_anchor + RIGHT*2.2 + DOWN*1.1, stroke_width=2, color="#FFFFFF"); line_est.set_z_index(3)
        self.play(Create(line_est), run_time=1.0)

        num9000 = Text("9000", font=title_font, font_size=22, color="#FFFFFF")
        num9000.move_to(top_right_anchor + RIGHT*1.5 + DOWN*1.5); num9000.set_z_index(3)
        self.play(FadeIn(num9000), run_time=1.5)
        
        self.wait(2.0)
        self.play(FadeOut(panel3_text), run_time=0.5)
        
        self.wait(7.24)
        
        ## Section 4
        
        panel4_text = wrap_text_dynamic("Multiply 891 by 2", title_font, 18, w/2 - 1.0)
        panel4_text.move_to(top_right_anchor + LEFT*3.2 + DOWN*1.1); panel4_text.set_z_index(3)
        self.play(FadeIn(panel4_text, shift=RIGHT), run_time=1.7)
        
        line1 = Line(top_right_anchor + LEFT*1.6 + DOWN*1.1, top_right_anchor + LEFT*0.2 + DOWN*1.1, stroke_width=2, color="#FFFFFF"); line1.set_z_index(3)
        self.play(Create(line1), run_time=0.5)
        
        partial1 = Text("  1782", font=title_font, font_size=18, color="#FFFFFF")
        partial1.move_to(top_right_anchor + LEFT*1.0 + DOWN*1.6); partial1.set_z_index(3)
        self.play(FadeIn(partial1), run_time=1.0)
        
        self.wait(1.4)
        self.play(FadeOut(panel4_text), run_time=0.5)
        
        panel5_text = wrap_text_dynamic("Multiply 891 by 10", title_font, 18, w/2 - 1.0)
        panel5_text.move_to(top_right_anchor + LEFT*3.2 + DOWN*1.6); panel5_text.set_z_index(3)
        self.play(FadeIn(panel5_text, shift=RIGHT), run_time=1.7)
        
        partial2 = Text(" 8910", font=title_font, font_size=18, color="#FFFFFF")
        partial2.move_to(top_right_anchor + LEFT*1.0 + DOWN*2.1); partial2.set_z_index(3)
        self.play(FadeIn(partial2), run_time=1.0)
        
        self.wait(1.4)
        self.play(FadeOut(panel5_text), run_time=0.5)
        
        panel6_text = wrap_text_dynamic("Add partial products: 1782 + 8910 = 10692", title_font, 18, w/2 - 1.0)
        panel6_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel6_text.set_z_index(3)
        self.play(FadeIn(panel6_text, shift=UP), run_time=2.2)
        
        line2 = Line(top_right_anchor + LEFT*1.6 + DOWN*2.4, top_right_anchor + LEFT*0.2 + DOWN*2.4, stroke_width=2, color="#FFFFFF"); line2.set_z_index(3)
        self.play(Create(line2), run_time=1.0)
        
        result1 = Text("10692", font=title_font, font_size=18, color="#FFFFFF")
        result1.move_to(top_right_anchor + LEFT*1.0 + DOWN*2.9); result1.set_z_index(3)
        self.play(FadeIn(result1), run_time=1.0)
        
        self.wait(1.7)
        self.play(FadeOut(panel6_text), run_time=0.5)
        
        self.wait(11.93)
        
        ## Section 5
        
        comparison1 = wrap_text_dynamic(
            "Estimated: 9000 ≈ Actual: 10692",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        comparison1.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0])
        comparison1.set_z_index(3)
        
        self.play(FadeIn(comparison1, shift=UP), run_time=3.08)
        
        self.wait(3.58)
        
        self.play(FadeOut(comparison1), run_time=2.28)
        
        cleanup_group = VGroup(
            line1, partial1, partial2, line2, result1,
            example1_heading, num900_1, num10_1, num9000, base_layout1, base_layout2, arrow1, arrow2, line_est
        )
        
        self.play(cleanup_group.animate.shift(RIGHT*8), run_time=2.58)
        self.remove(cleanup_group)
        
        self.wait(2.02)
        
        ## Section 6
        
        example2_heading = Text(
            "Example 2: 4428 x 36",
            font=title_font,
            font_size=22,
            color="#61D262"
        )
        example2_heading.move_to(top_right_anchor + UP*1.2)
        example2_heading.set_z_index(3)
        
        self.play(FadeIn(example2_heading, shift=UP), run_time=1.2)
        
        panel7_text = wrap_text_dynamic("Round 4428 to the nearest thousands (4000).", title_font, 18, w/2 - 1.0)
        panel7_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel7_text.set_z_index(3)
        self.play(FadeIn(panel7_text, shift=UP), run_time=1.7)
        
        rect4428 = SurroundingRectangle(problem2, buff=0.15, color="#EF9515"); rect4428.set_z_index(3)
        self.play(Create(rect4428), run_time=1.0)
        
        base_layout3 = Text("  4428", font=title_font, font_size=20, color="#FFFFFF")
        base_layout3.move_to(top_right_anchor + LEFT*1.0 + DOWN*0.3); base_layout3.set_z_index(3)
        self.play(FadeIn(base_layout3), run_time=1.0)
        
        arrow3 = Arrow(start=top_right_anchor + LEFT*0.2 + DOWN*0.3, end=top_right_anchor + RIGHT*0.8 + DOWN*0.3, color=WHITE, buff=0.1)
        arrow3.set_z_index(3)
        self.play(Create(arrow3), run_time=0.5)

        num4000 = Text("4000", font=title_font, font_size=20, color="#FFFFFF")
        num4000.move_to(top_right_anchor + RIGHT*1.5 + DOWN*0.3); num4000.set_z_index(3)
        self.play(FadeIn(num4000), run_time=1.0)
        
        self.wait(1.0)
        self.play(FadeOut(panel7_text), FadeOut(rect4428), run_time=0.5)
        
        panel8_text = wrap_text_dynamic("Round 36 to the nearest tens (40).", title_font, 18, w/2 - 1.0)
        panel8_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel8_text.set_z_index(3)
        self.play(FadeIn(panel8_text, shift=UP), run_time=1.7)
        
        rect36 = SurroundingRectangle(problem2, buff=0.15, color="#EF9515"); rect36.set_z_index(3)
        self.play(Create(rect36), run_time=1.0)
        
        base_layout4 = Text(" x  36", font=title_font, font_size=20, color="#FFFFFF")
        base_layout4.move_to(top_right_anchor + LEFT*1.0 + DOWN*0.8); base_layout4.set_z_index(3)
        self.play(FadeIn(base_layout4), run_time=1.0)
        
        arrow4 = Arrow(start=top_right_anchor + LEFT*0.2 + DOWN*0.8, end=top_right_anchor + RIGHT*0.8 + DOWN*0.8, color=WHITE, buff=0.1)
        arrow4.set_z_index(3)
        self.play(Create(arrow4), run_time=0.5)

        num40 = Text("x 40", font=title_font, font_size=20, color="#FFFFFF")
        num40.move_to(top_right_anchor + RIGHT*1.5 + DOWN*0.8); num40.set_z_index(3)
        self.play(FadeIn(num40), run_time=1.0)
        
        self.wait(1.0)
        self.play(FadeOut(panel8_text), FadeOut(rect36), run_time=0.5)
        
        panel9_text = wrap_text_dynamic("Estimated Product: 4000 x 40 = 1,60,000", title_font, 20, w/2 - 1.0, color="#FFFFFF")
        panel9_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel9_text.set_z_index(3)
        self.play(FadeIn(panel9_text, shift=UP), run_time=2.2)
        
        line_est2 = Line(top_right_anchor + RIGHT*0.8 + DOWN*1.1, top_right_anchor + RIGHT*2.2 + DOWN*1.1, stroke_width=2, color="#FFFFFF")
        line_est2.set_z_index(3)
        self.play(Create(line_est2), run_time=1.0)

        num160000 = Text("1,60,000", font=title_font, font_size=22, color="#FFFFFF")
        num160000.move_to(top_right_anchor + RIGHT*1.5 + DOWN*1.5); num160000.set_z_index(3)
        self.play(FadeIn(num160000), run_time=1.7)
        
        self.wait(2.2)
        self.play(FadeOut(panel9_text), run_time=0.5)
        
        self.wait(4.07)
        
        ## Section 7
        
        panel10_text = wrap_text_dynamic("Multiply 4428 by 6", title_font, 18, w/2 - 1.0)
        panel10_text.move_to(top_right_anchor + LEFT*3.2 + DOWN*1.1); panel10_text.set_z_index(3)
        self.play(FadeIn(panel10_text, shift=RIGHT), run_time=1.724)
        
        line3 = Line(top_right_anchor + LEFT*1.8 + DOWN*1.1, top_right_anchor + LEFT*0.0 + DOWN*1.1, stroke_width=2, color="#FFFFFF"); line3.set_z_index(3)
        self.play(Create(line3), run_time=0.5)
        
        partial3 = Text("  26568", font=title_font, font_size=18, color="#FFFFFF")
        partial3.move_to(top_right_anchor + LEFT*1.0 + DOWN*1.6); partial3.set_z_index(3)
        self.play(FadeIn(partial3), run_time=1.024)
        
        self.wait(1.424)
        self.play(FadeOut(panel10_text), run_time=0.5)
        
        panel11_text = wrap_text_dynamic("Multiply 4428 by 30", title_font, 18, w/2 - 1.0)
        panel11_text.move_to(top_right_anchor + LEFT*3.2 + DOWN*1.6); panel11_text.set_z_index(3)
        self.play(FadeIn(panel11_text, shift=RIGHT), run_time=1.724)
        
        partial4 = Text(" 132840", font=title_font, font_size=18, color="#FFFFFF")
        partial4.move_to(top_right_anchor + LEFT*1.0 + DOWN*2.1); partial4.set_z_index(3)
        self.play(FadeIn(partial4), run_time=1.024)
        
        self.wait(1.424)
        self.play(FadeOut(panel11_text), run_time=0.5)
        
        panel12_text = wrap_text_dynamic("Add partial products: 26568 + 132840 = 1,59,408", title_font, 18, w/2 - 1.0)
        panel12_text.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0]); panel12_text.set_z_index(3)
        self.play(FadeIn(panel12_text, shift=UP), run_time=2.224)
        
        line4 = Line(top_right_anchor + LEFT*1.8 + DOWN*2.4, top_right_anchor + LEFT*0.0 + DOWN*2.4, stroke_width=2, color="#FFFFFF"); line4.set_z_index(3)
        self.play(Create(line4), run_time=1.024)
        
        result2 = Text("1,59,408", font=title_font, font_size=18, color="#FFFFFF")
        result2.move_to(top_right_anchor + LEFT*1.0 + DOWN*2.9); result2.set_z_index(3)
        self.play(FadeIn(result2), run_time=1.024)
        
        self.wait(1.724)
        self.play(FadeOut(panel12_text), run_time=0.5)
        
        self.wait(12.214)
        
        ## Section 8
        
        comparison2 = wrap_text_dynamic(
            "Estimated: 1,60,000 ≈ Actual: 1,59,408",
            title_font,
            20,
            w/2 - 1.0,
            color="#FFFFFF"
        )
        comparison2.move_to([-w/4 + w/2 + 0.1, center_y_of_grid - 2.5, 0])
        comparison2.set_z_index(3)
        
        self.play(FadeIn(comparison2, shift=UP), run_time=3.21)
        
        self.wait(3.71)
        
        self.play(FadeOut(comparison2), run_time=2.41)
        
        cleanup_group2 = VGroup(
            line3, partial3, partial4, line4, result2,
            example2_heading, num4000, num40, num160000, base_layout3, base_layout4, arrow3, arrow4, line_est2
        )
        
        self.play(cleanup_group2.animate.shift(RIGHT*8), run_time=2.71)
        self.remove(cleanup_group2)
        
        self.wait(2.12)
        
        ## Section 9
        
        self.play(
            problem1.animate.shift(LEFT*8),
            problem2.animate.shift(LEFT*8),
            FadeOut(grid_lines),
            run_time=1.512
        )
        self.remove(problem1, problem2)
        
        self.wait(0.513)
        
        concluding_text = wrap_text_dynamic(
            "Estimating helps us find answers quickly and check if our actual answer is reasonable!",
            title_font,
            24,
            w - 1.0,
            color="#FFFFFF"
        )
        concluding_text.move_to([0, 0, 0])
        concluding_text.set_z_index(3)
        
        self.play(FadeIn(concluding_text, shift=UP), run_time=2.513)
        self.wait(2.013)
        
        colored_concluding_text = wrap_text_dynamic(
            "Estimating helps us find answers quickly and check if our actual answer is reasonable!",
            title_font,
            24,
            w - 1.0,
            color="#FFFFFF",
            t2c={"Estimating": "#EF9515", "quickly": "#EF9515", "reasonable": "#EF9515"}
        )
        colored_concluding_text.move_to([0, 0, 0])
        colored_concluding_text.set_z_index(3)
        
        self.play(Transform(concluding_text, colored_concluding_text), run_time=1.5)
        
        self.wait(2.673)
        
        self.play(
            FadeOut(title),
            FadeOut(concluding_text),
            run_time=1.512
        )
        
        self.wait(2.073)
