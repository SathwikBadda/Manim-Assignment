from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#E0F7FA"
        
        card_width = config.frame_width * 0.18
        card_height = card_width * 1.4

        header_rect = Rectangle(width=config.frame_width, height=1.2, color="#00ACC1", fill_opacity=1)
        header_rect.to_edge(UP, buff=0)
        
        footer_colors = [RED_D, ORANGE, YELLOW, GREEN_D, BLUE_D, PURPLE_D]
        footer_group = VGroup()
        
        num_circles = int(config.frame_width / 0.4) + 2
        
        for i in range(num_circles):
            c = Circle(radius=0.18, color=WHITE, fill_color=footer_colors[i % len(footer_colors)], fill_opacity=1, stroke_width=4)
            hole = Circle(radius=0.06, color=WHITE, fill_color="#E0F7FA", fill_opacity=1, stroke_width=0)
            footer_group.add(VGroup(c, hole))
            
        footer_group.arrange(RIGHT, buff=0.1)
        footer_group.to_edge(DOWN, buff=0.2)
        
        self.add(header_rect, footer_group)

        ## Section 1
        raw_title = "Divisibility by 3 & 9"
        
        block_width = config.frame_width * 0.05
        base_buff = block_width * 0.15
        horizontal_margin = 2.0
        
        available_width = config.frame_width - horizontal_margin
        max_chars = int(available_width // (block_width + base_buff))

        title_lines = textwrap.wrap(raw_title, width=max_chars)

        title_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        title_group = VGroup()
        
        global_index = 0
        for line in title_lines:
            line_group = VGroup()
            for char in line:
                if char == " ":
                    spacer = Square(side_length=1)
                    spacer.set_opacity(0)
                    line_group.add(spacer)
                    continue
  
                color = title_colors[global_index % len(title_colors)]
                global_index += 1
                
                block = RoundedRectangle(corner_radius=0.2, width=1, height=1, color=BLACK, stroke_width=4, fill_color=color, fill_opacity=1)
                letter = Text(char, font="Comic Sans MS", weight=BOLD, color=WHITE, font_size=60).set_stroke(BLACK, 2)
                line_group.add(VGroup(block, letter))
            
            line_group.arrange(RIGHT, buff=base_buff)
            line_group.move_to(ORIGIN)
            title_group.add(line_group)

        title_group.arrange(DOWN, buff=0.3)
        title_group.center()
        title_group.shift(UP * (config.frame_height * 0.15))
        
        all_blocks = VGroup()
        for line in title_group:
            for block in line:
                all_blocks.add(block)

        destinations = [m.get_center() for m in all_blocks]
        for m in all_blocks:
            m.shift(UP * 8)
        
        drop_anims = [
            m.animate(rate_func=rate_functions.ease_out_bounce, run_time=1.5).move_to(dest)
            for m, dest in zip(all_blocks, destinations)
        ]
        
        self.play(LaggedStart(*drop_anims, lag_ratio=0.05), run_time=1.5)
        
        subtitle = Text("Look at the sum of digits!", font="Comic Sans MS", weight=BOLD, font_size=40, color="#333333")
        subtitle.set_stroke(color=BLACK, width=0)
        subtitle.next_to(title_group, DOWN, buff=0.6)
        
        self.play(GrowFromCenter(subtitle, rate_func=rate_functions.ease_out_elastic), run_time=1.0)
        
        self.play(FadeOut(subtitle, shift=DOWN), run_time=0.5)
        self.play(LaggedStart(*[ShrinkToCenter(m) for m in all_blocks], lag_ratio=0.05), run_time=0.94)

        ## Section 2
        rule_box = RoundedRectangle(corner_radius=0.3, width=10, height=3.5, color=PINK, stroke_width=8, fill_color=WHITE, fill_opacity=0.95)
        
        badge_star = Star(n=12, outer_radius=0.8, inner_radius=0.6, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=3)
        badge_text = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=32, color=RED).set_stroke(BLACK, 4)
        badge_group = VGroup(badge_star, badge_text).move_to(rule_box.get_corner(UL) + DOWN*0.2 + RIGHT*0.2)

        rule_content = MarkupText(
            'A number is divisible by 3 if the\n'
            '<span fgcolor="#E91E63"><b>sum of its digits</b></span> is\n'
            '<span fgcolor="#E91E63"><b>divisible by 3</b></span>.',
            font="Comic Sans MS", color="#333333", font_size=42, justify=True, line_spacing=1.5
        )
        rule_content.move_to(rule_box.get_center())

        self.play(DrawBorderThenFill(rule_box), run_time=1.0)
        self.play(SpinInFromNothing(badge_group), run_time=1.0)
        self.play(Write(rule_content), run_time=7.0)
        self.play(Indicate(rule_box, color=PINK, scale_factor=1.05), run_time=1.0)
        self.wait(3.1)
        self.play(FadeOut(rule_box), run_time=1.0)
        self.play(FadeOut(badge_group), run_time=1.0)
        self.play(FadeOut(rule_content), run_time=1.58)

        ## Section 3
        card_width_ex = config.frame_width * 0.22
        card_height_ex = card_width_ex * 1.2

        example_1_base = RoundedRectangle(
            corner_radius=0.3,
            width=card_width_ex,
            height=card_height_ex,
            color=BLACK,
            stroke_width=3,
            fill_color="#FFFDE7",
            fill_opacity=1
        )
        example_1_base.shift(LEFT * 3.5)

        example_2_base = RoundedRectangle(
            corner_radius=0.3,
            width=card_width_ex,
            height=card_height_ex,
            color=BLACK,
            stroke_width=3,
            fill_color="#FFFDE7",
            fill_opacity=1
        )
        example_2_base.shift(RIGHT * 3.5)

        tape_1 = Rectangle(width=1.0, height=0.3, color=PINK, fill_opacity=0.8, stroke_width=0)
        tape_1.rotate(random.uniform(-10, 10)*DEGREES).move_to(example_1_base.get_top())

        tape_2 = Rectangle(width=1.0, height=0.3, color=TEAL, fill_opacity=0.8, stroke_width=0)
        tape_2.rotate(random.uniform(-10, 10)*DEGREES).move_to(example_2_base.get_top())

        example_1_group = Group(example_1_base, tape_1)
        example_2_group = Group(example_2_base, tape_2)

        self.play(GrowFromCenter(example_1_group), run_time=1.886)

        target_1_text = Text("3528", font="Comic Sans MS", font_size=36, color=BLACK, weight=BOLD)
        target_1_text.move_to(example_1_base.get_center() + UP * 1.25)
        self.play(FadeIn(target_1_text, shift=DOWN*0.5), run_time=0.943)

        calc_1_line_1 = Text("3 + 5 + 2 + 8", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_1_line_2 = Text("= 18", font="Comic Sans MS", font_size=24, color=BLACK)
        VGroup(calc_1_line_1, calc_1_line_2).arrange(RIGHT, buff=0.15).move_to(example_1_base.get_center() + UP * 0.4)
        
        self.play(Write(calc_1_line_1), run_time=0.943)
        self.play(Write(calc_1_line_2), run_time=1.386)

        calc_1_line_3 = Text("18 ÷ 3 = 6", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_1_line_3.move_to(example_1_base.get_center() + DOWN * 0.2)
        self.play(Write(calc_1_line_3), run_time=1.386)

        conclusion_1 = Text("is divisible\nby 3!", font="Comic Sans MS", font_size=22, color=GREEN, weight=BOLD, line_spacing=1.1)
        conclusion_1.move_to(example_1_base.get_center() + DOWN * 1.0)
        self.play(Write(conclusion_1), run_time=1.386)

        self.play(GrowFromCenter(example_2_group), run_time=1.886)

        target_2_text = Text("1394", font="Comic Sans MS", font_size=36, color=BLACK, weight=BOLD)
        target_2_text.move_to(example_2_base.get_center() + UP * 1.25)
        self.play(FadeIn(target_2_text, shift=DOWN*0.5), run_time=0.943)

        calc_2_line_1 = Text("1 + 3 + 9 + 4", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_2_line_2 = Text("= 17", font="Comic Sans MS", font_size=24, color=BLACK)
        VGroup(calc_2_line_1, calc_2_line_2).arrange(RIGHT, buff=0.15).move_to(example_2_base.get_center() + UP * 0.4)
        
        self.play(Write(calc_2_line_1), run_time=0.943)
        self.play(Write(calc_2_line_2), run_time=1.386)

        calc_2_line_3 = Text("17 ÷ 3 = 5\nremainder 2", font="Comic Sans MS", font_size=22, color=BLACK, line_spacing=1.1)
        calc_2_line_3.move_to(example_2_base.get_center() + DOWN * 0.3)
        self.play(Write(calc_2_line_3), run_time=1.386)

        conclusion_2 = Text("is NOT divisible\nby 3!", font="Comic Sans MS", font_size=22, color=RED, weight=BOLD, line_spacing=1.1)
        conclusion_2.move_to(example_2_base.get_center() + DOWN * 1.1)
        self.play(Write(conclusion_2), run_time=1.386)

        self.wait(1.386)

        self.play(FadeOut(example_1_group), FadeOut(target_1_text), run_time=1.386)
        self.play(FadeOut(calc_1_line_1), run_time=0.586)
        self.play(FadeOut(calc_1_line_2), run_time=0.586)
        self.play(FadeOut(calc_1_line_3), run_time=0.586)
        self.play(FadeOut(conclusion_1), run_time=0.586)
        self.play(FadeOut(example_2_group), FadeOut(target_2_text), run_time=1.386)
        self.play(FadeOut(calc_2_line_1), run_time=0.586)
        self.play(FadeOut(calc_2_line_2), run_time=0.586)
        self.play(FadeOut(calc_2_line_3), run_time=0.586)
        self.play(FadeOut(conclusion_2), run_time=0.586)

        ## Section 4
        rule_box_2 = RoundedRectangle(corner_radius=0.3, width=10, height=3.5, color=PINK, stroke_width=8, fill_color=WHITE, fill_opacity=0.95)
        
        badge_star_2 = Star(n=12, outer_radius=0.8, inner_radius=0.6, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=3)
        badge_text_2 = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=32, color=RED).set_stroke(BLACK, 4)
        badge_group_2 = VGroup(badge_star_2, badge_text_2).move_to(rule_box_2.get_corner(UL) + DOWN*0.2 + RIGHT*0.2)

        rule_content_2 = MarkupText(
            'A number is divisible by 9 if the\n'
            '<span fgcolor="#E91E63"><b>sum of its digits</b></span> is\n'
            '<span fgcolor="#E91E63"><b>divisible by 9</b></span>.',
            font="Comic Sans MS", color="#333333", font_size=42, justify=True, line_spacing=1.5
        )
        rule_content_2.move_to(rule_box_2.get_center())

        self.play(DrawBorderThenFill(rule_box_2), run_time=1.0)
        self.play(SpinInFromNothing(badge_group_2), run_time=1.0)
        self.play(Write(rule_content_2), run_time=7.0)
        self.play(Indicate(rule_box_2, color=PINK, scale_factor=1.05), run_time=1.0)
        self.wait(1.1)
        self.play(FadeOut(rule_box_2), run_time=1.0)
        self.play(FadeOut(badge_group_2), run_time=1.0)
        self.play(FadeOut(rule_content_2), run_time=0.08)

        ## Section 5
        example_3_base = RoundedRectangle(
            corner_radius=0.3,
            width=card_width_ex,
            height=card_height_ex,
            color=BLACK,
            stroke_width=3,
            fill_color="#FFFDE7",
            fill_opacity=1
        )
        example_3_base.shift(LEFT * 3.5)

        example_4_base = RoundedRectangle(
            corner_radius=0.3,
            width=card_width_ex,
            height=card_height_ex,
            color=BLACK,
            stroke_width=3,
            fill_color="#FFFDE7",
            fill_opacity=1
        )
        example_4_base.shift(RIGHT * 3.5)

        tape_3 = Rectangle(width=1.0, height=0.3, color=ORANGE, fill_opacity=0.8, stroke_width=0)
        tape_3.rotate(random.uniform(-10, 10)*DEGREES).move_to(example_3_base.get_top())

        tape_4 = Rectangle(width=1.0, height=0.3, color=PURPLE, fill_opacity=0.8, stroke_width=0)
        tape_4.rotate(random.uniform(-10, 10)*DEGREES).move_to(example_4_base.get_top())

        example_3_group = Group(example_3_base, tape_3)
        example_4_group = Group(example_4_base, tape_4)

        self.play(GrowFromCenter(example_3_group), run_time=1.6)

        target_3_text = Text("9711", font="Comic Sans MS", font_size=36, color=BLACK, weight=BOLD)
        target_3_text.move_to(example_3_base.get_center() + UP * 1.25)
        self.play(FadeIn(target_3_text, shift=DOWN*0.5), run_time=0.8)

        calc_3_line_1 = Text("9 + 7 + 1 + 1", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_3_line_2 = Text("= 18", font="Comic Sans MS", font_size=24, color=BLACK)
        VGroup(calc_3_line_1, calc_3_line_2).arrange(RIGHT, buff=0.15).move_to(example_3_base.get_center() + UP * 0.4)
        
        self.play(Write(calc_3_line_1), run_time=0.8)
        self.play(Write(calc_3_line_2), run_time=1.1)

        calc_3_line_3 = Text("18 ÷ 9 = 2", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_3_line_3.move_to(example_3_base.get_center() + DOWN * 0.2)
        self.play(Write(calc_3_line_3), run_time=1.1)

        conclusion_3 = Text("is divisible\nby 9!", font="Comic Sans MS", font_size=22, color=GREEN, weight=BOLD, line_spacing=1.1)
        conclusion_3.move_to(example_3_base.get_center() + DOWN * 1.0)
        self.play(Write(conclusion_3), run_time=1.1)

        self.play(GrowFromCenter(example_4_group), run_time=1.6)

        target_4_text = Text("5423", font="Comic Sans MS", font_size=36, color=BLACK, weight=BOLD)
        target_4_text.move_to(example_4_base.get_center() + UP * 1.25)
        self.play(FadeIn(target_4_text, shift=DOWN*0.5), run_time=0.8)

        calc_4_line_1 = Text("5 + 4 + 2 + 3", font="Comic Sans MS", font_size=24, color=BLACK)
        calc_4_line_2 = Text("= 14", font="Comic Sans MS", font_size=24, color=BLACK)
        VGroup(calc_4_line_1, calc_4_line_2).arrange(RIGHT, buff=0.15).move_to(example_4_base.get_center() + UP * 0.4)
        
        self.play(Write(calc_4_line_1), run_time=0.8)
        self.play(Write(calc_4_line_2), run_time=1.1)

        calc_4_line_3 = Text("14 ÷ 9 = 1\nremainder 5", font="Comic Sans MS", font_size=22, color=BLACK, line_spacing=1.1)
        calc_4_line_3.move_to(example_4_base.get_center() + DOWN * 0.3)
        self.play(Write(calc_4_line_3), run_time=1.1)

        conclusion_4 = Text("is NOT divisible\nby 9!", font="Comic Sans MS", font_size=22, color=RED, weight=BOLD, line_spacing=1.1)
        conclusion_4.move_to(example_4_base.get_center() + DOWN * 1.1)
        self.play(Write(conclusion_4), run_time=1.1)

        self.wait(1.1)

        self.play(FadeOut(example_3_group), FadeOut(target_3_text), run_time=1.1)
        self.play(FadeOut(calc_3_line_1), run_time=0.3)
        self.play(FadeOut(calc_3_line_2), run_time=0.3)
        self.play(FadeOut(calc_3_line_3), run_time=0.3)
        self.play(FadeOut(conclusion_3), run_time=0.3)
        self.play(FadeOut(example_4_group), FadeOut(target_4_text), run_time=1.1)
        self.play(FadeOut(calc_4_line_1), run_time=0.3)
        self.play(FadeOut(calc_4_line_2), run_time=0.3)
        self.play(FadeOut(calc_4_line_3), run_time=0.3)
        self.play(FadeOut(conclusion_4), run_time=0.3)

        ## Section 6
        rays = VGroup(*[AnnularSector(inner_radius=0, outer_radius=10, angle=TAU/40, start_angle=i*TAU/20, color=YELLOW_A, fill_opacity=0.3) for i in range(20)]).move_to(ORIGIN)
        
        star = Star(n=7, outer_radius=2.5, inner_radius=1.2, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=5)
        
        final_txt_stroke = Text("Great Job!", font="Comic Sans MS", weight=BOLD, font_size=80, color=RED).set_stroke(WHITE, 10)
        final_txt_fill = Text("Great Job!", font="Comic Sans MS", weight=BOLD, font_size=80, color=RED).set_stroke(RED, 0)
        final_txt = VGroup(final_txt_stroke, final_txt_fill).move_to(ORIGIN)
        
        txt_sub = Text("Keep Practicing!", font="Comic Sans MS", weight=BOLD, font_size=40, color="#333333").set_stroke(width=0).next_to(star, DOWN, buff=0.5)
        
        confetti = VGroup()
        for _ in range(50):
            c = Square(side_length=0.15, fill_color=random.choice([RED, BLUE, GREEN, YELLOW, PINK, ORANGE]), fill_opacity=1, stroke_width=0)
            c.move_to(ORIGIN)
            confetti.add(c)

        self.play(FadeIn(rays), run_time=0.5)
        
        self.play(GrowFromCenter(star, rate_func=rate_functions.ease_out_elastic), Rotate(rays, angle=PI/2, rate_func=linear), run_time=1.0)
        self.play(GrowFromCenter(final_txt, rate_func=rate_functions.ease_out_elastic), Rotate(rays, angle=PI/2, rate_func=linear), run_time=1.0)
        
        self.play(
            LaggedStart(*[c.animate.shift(np.array([random.uniform(-5, 5), random.uniform(-4, 4), 0])).rotate(random.uniform(0, TAU*2)) for c in confetti], lag_ratio=0.05),
            FadeIn(txt_sub, shift=UP),
            Rotate(rays, angle=PI, rate_func=linear),
            run_time=1.0
        )

        self.play(FadeOut(rays), run_time=0.3)
        self.play(FadeOut(star), run_time=0.3)
        self.play(FadeOut(final_txt), run_time=0.3)
        self.play(FadeOut(txt_sub), run_time=0.3)
        self.play(FadeOut(confetti), run_time=0.3)
        self.play(FadeOut(header_rect), run_time=0.1)
        self.play(FadeOut(footer_group), run_time=0.1)
