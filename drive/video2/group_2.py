from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#E0F7FA"
        
        card_width = config.frame_width * 0.24
        card_height = card_width * 1.4
        
        def get_image_or_placeholder(filename, color=GRAY):
            try:
                img = ImageMobject(filename)
                return img
            except IOError:
                return Square(color=color, fill_opacity=0.5).add(Text(filename[:-4], font_size=20))
        
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
        raw_title = "Who is doing what?"
        block_width = config.frame_width * 0.06
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
        
        subtitle = Text("Using is, am, are", font="Comic Sans MS", weight=BOLD, font_size=40, color="#333333")
        subtitle.set_stroke(color=BLACK, width=0)
        subtitle.next_to(title_group, DOWN, buff=0.6)
        
        self.play(GrowFromCenter(subtitle, rate_func=rate_functions.ease_out_elastic), run_time=1.2)
        self.wait(4.04)
        
        self.play(FadeOut(subtitle, shift=DOWN), run_time=0.8)
        shrink_anims = [ShrinkToCenter(m) for m in all_blocks]
        self.play(*shrink_anims, run_time=1.88)
        
        ## Section 2
        rule_box = RoundedRectangle(corner_radius=0.3, width=11, height=3.5, color=PINK, stroke_width=8, fill_color=WHITE, fill_opacity=0.95)
        
        badge_star = Star(n=12, outer_radius=0.8, inner_radius=0.6, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=3)
        badge_text = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=32, color=RED).set_stroke(BLACK, 4)
        badge_group = VGroup(badge_star, badge_text).move_to(rule_box.get_corner(UL) + DOWN*0.2 + RIGHT*0.2)
        
        rule_content = MarkupText(
            'We use <span fgcolor="#EF9515"><b>\'am\'</b></span> with <span fgcolor="#EF9515"><b>\'I\'</b></span>. We use <span fgcolor="#EF9515"><b>\'is\'</b></span> with\n'
            '<span fgcolor="#EF9515"><b>one person or thing</b></span> (he, she, it).\n'
            'We use <span fgcolor="#EF9515"><b>\'are\'</b></span> with <span fgcolor="#EF9515"><b>many people or things</b></span>\n'
            '(we, you, they).',
            font="Comic Sans MS", color="#61D262", font_size=32, justify=True, line_spacing=1.5
        )
        rule_content.move_to(rule_box.get_center())
        
        self.play(DrawBorderThenFill(rule_box), run_time=3.0)
        self.play(SpinInFromNothing(badge_group), run_time=2.0)
        self.play(Write(rule_content), run_time=4.5)
        self.play(Indicate(rule_box, color=PINK, scale_factor=1.05), run_time=1.2)
        self.wait(1.04)
        self.play(FadeOut(rule_box), FadeOut(badge_group), FadeOut(rule_content), run_time=1.0)
        
        ## Section 3
        ex_bg = RoundedRectangle(corner_radius=0.5, width=5, height=1.2, color="#FFB74D", fill_opacity=1, stroke_color=WHITE, stroke_width=5).move_to(UP*2.8)
        ex_title = Text("Examples", font="Comic Sans MS", weight=BOLD, font_size=48, color=WHITE).set_stroke("#E65100", 4).move_to(ex_bg)
        
        self.play(GrowFromCenter(VGroup(ex_bg, ex_title), rate_func=rate_functions.ease_out_elastic), run_time=1.432)
        
        card_1_base = RoundedRectangle(corner_radius=card_width * 0.08, width=card_width, height=card_height, color=BLACK, stroke_width=3, fill_color="#FFFDE7", fill_opacity=1)
        card_1_img = get_image_or_placeholder("../images/ing_words_6.png", BLUE)
        card_1_img.height = card_height * 0.45
        card_1_img.move_to(card_1_base.get_center() + UP * (card_height * 0.25))
        card_1_text = MarkupText("I <span fgcolor=\"#FF1493\"><b>am</b></span> reading.", font="Comic Sans MS", font_size=24, color=BLACK)
        card_1_text.next_to(card_1_img, DOWN, buff=0.3)
        card_1_tape = Rectangle(width=1.0, height=0.3, color=PINK, fill_opacity=0.8, stroke_width=0)
        card_1_tape.rotate(5*DEGREES).move_to(card_1_base.get_top())
        card_1 = Group(card_1_base, card_1_img, card_1_text, card_1_tape)
        
        card_2_base = RoundedRectangle(corner_radius=card_width * 0.08, width=card_width, height=card_height, color=BLACK, stroke_width=3, fill_color="#FFFDE7", fill_opacity=1)
        card_2_img = get_image_or_placeholder("../images/ing_words_7.png", BLUE)
        card_2_img.height = card_height * 0.45
        card_2_img.move_to(card_2_base.get_center() + UP * (card_height * 0.25))
        card_2_text = MarkupText("She <span fgcolor=\"#FF1493\"><b>is</b></span> eating.", font="Comic Sans MS", font_size=24, color=BLACK)
        card_2_text.next_to(card_2_img, DOWN, buff=0.3)
        card_2_tape = Rectangle(width=1.0, height=0.3, color=TEAL, fill_opacity=0.8, stroke_width=0)
        card_2_tape.rotate(-7*DEGREES).move_to(card_2_base.get_top())
        card_2 = Group(card_2_base, card_2_img, card_2_text, card_2_tape)
        
        card_3_base = RoundedRectangle(corner_radius=card_width * 0.08, width=card_width, height=card_height, color=BLACK, stroke_width=3, fill_color="#FFFDE7", fill_opacity=1)
        card_3_img = get_image_or_placeholder("../images/ing_words_8.png", BLUE)
        card_3_img.height = card_height * 0.45
        card_3_img.move_to(card_3_base.get_center() + UP * (card_height * 0.25))
        card_3_text = MarkupText("They <span fgcolor=\"#FF1493\"><b>are</b></span> playing.", font="Comic Sans MS", font_size=24, color=BLACK)
        card_3_text.next_to(card_3_img, DOWN, buff=0.3)
        card_3_tape = Rectangle(width=1.0, height=0.3, color=ORANGE, fill_opacity=0.8, stroke_width=0)
        card_3_tape.rotate(3*DEGREES).move_to(card_3_base.get_top())
        card_3 = Group(card_3_base, card_3_img, card_3_text, card_3_tape)
        
        batch_1 = Group(card_1, card_2, card_3)
        batch_1.arrange(RIGHT, buff=0.4)
        batch_1.center()
        batch_1.shift(DOWN * 0.2) # Shift down to avoid header
        
        self.play(LaggedStart(GrowFromCenter(card_1), GrowFromCenter(card_2), GrowFromCenter(card_3), lag_ratio=0.2), run_time=2.032)
        self.wait(1.032)
        self.play(Wiggle(card_1_text, scale_value=1.2), Wiggle(card_2_text, scale_value=1.2), Wiggle(card_3_text, scale_value=1.2), run_time=1.432)
        self.play(FadeOut(batch_1, shift=LEFT), run_time=1.432)
        
        card_4_base = RoundedRectangle(corner_radius=card_width * 0.08, width=card_width, height=card_height, color=BLACK, stroke_width=3, fill_color="#FFFDE7", fill_opacity=1)
        card_4_img = get_image_or_placeholder("../images/ing_words_9.png", BLUE)
        card_4_img.height = card_height * 0.45
        card_4_img.move_to(card_4_base.get_center() + UP * (card_height * 0.25))
        card_4_text = MarkupText("Baby <span fgcolor=\"#FF1493\"><b>is</b></span> crying.", font="Comic Sans MS", font_size=24, color=BLACK)
        card_4_text.next_to(card_4_img, DOWN, buff=0.3)
        card_4_tape = Rectangle(width=1.0, height=0.3, color=PINK, fill_opacity=0.8, stroke_width=0)
        card_4_tape.rotate(-5*DEGREES).move_to(card_4_base.get_top())
        card_4 = Group(card_4_base, card_4_img, card_4_text, card_4_tape)
        
        card_5_base = RoundedRectangle(corner_radius=card_width * 0.08, width=card_width, height=card_height, color=BLACK, stroke_width=3, fill_color="#FFFDE7", fill_opacity=1)
        card_5_img = get_image_or_placeholder("../images/ing_words_10.png", BLUE)
        card_5_img.height = card_height * 0.45
        card_5_img.move_to(card_5_base.get_center() + UP * (card_height * 0.25))
        card_5_text = MarkupText("The birds <span fgcolor=\"#FF1493\"><b>are</b></span> flying.", font="Comic Sans MS", font_size=24, color=BLACK)
        card_5_text.next_to(card_5_img, DOWN, buff=0.3)
        card_5_tape = Rectangle(width=1.0, height=0.3, color=TEAL, fill_opacity=0.8, stroke_width=0)
        card_5_tape.rotate(6*DEGREES).move_to(card_5_base.get_top())
        card_5 = Group(card_5_base, card_5_img, card_5_text, card_5_tape)
        
        batch_2 = Group(card_4, card_5)
        batch_2.arrange(RIGHT, buff=0.8)
        batch_2.center()
        batch_2.shift(DOWN * 0.2)
        
        self.play(LaggedStart(GrowFromCenter(card_4), GrowFromCenter(card_5), lag_ratio=0.2), run_time=2.032)
        self.wait(1.032)
        self.play(Wiggle(card_4_text, scale_value=1.2), Wiggle(card_5_text, scale_value=1.2), run_time=1.432)
        self.play(FadeOut(batch_2, shift=LEFT), run_time=1.432)
        self.play(FadeOut(VGroup(ex_bg, ex_title)), run_time=1.232)
        
        ## Section 4 (Quiz)
        quiz_header = Text("Think about it...", font="Comic Sans MS", weight=BOLD, font_size=40, color="#61D262") # Smaller header
        quiz_header.next_to(header_rect, DOWN, buff=0.4)
        
        quiz_card_1_base = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.5, color=BLACK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
        quiz_card_1_img = get_image_or_placeholder("../images/ing_words_11.png", GRAY)
        quiz_card_1_img.height = 1.5
        quiz_card_1_img.move_to(quiz_card_1_base.get_center() + UP * 0.8)
        quiz_card_1_mark = Text("?", font="Comic Sans MS", font_size=48, color=GRAY)
        quiz_card_1_mark.move_to(quiz_card_1_base.get_center() + DOWN * 0.5)
        quiz_card_1 = Group(quiz_card_1_base, quiz_card_1_img, quiz_card_1_mark)
        
        quiz_card_2_base = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.5, color=BLACK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
        quiz_card_2_img = get_image_or_placeholder("../images/ing_words_12.png", GRAY)
        quiz_card_2_img.height = 1.5
        quiz_card_2_img.move_to(quiz_card_2_base.get_center() + UP * 0.8)
        quiz_card_2_mark = Text("?", font="Comic Sans MS", font_size=48, color=GRAY)
        quiz_card_2_mark.move_to(quiz_card_2_base.get_center() + DOWN * 0.5)
        quiz_card_2 = Group(quiz_card_2_base, quiz_card_2_img, quiz_card_2_mark)
        
        quiz_card_3_base = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.5, color=BLACK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
        quiz_card_3_img = get_image_or_placeholder("../images/ing_words_13.png", GRAY)
        quiz_card_3_img.height = 1.5
        quiz_card_3_img.move_to(quiz_card_3_base.get_center() + UP * 0.8)
        quiz_card_3_mark = Text("?", font="Comic Sans MS", font_size=48, color=GRAY)
        quiz_card_3_mark.move_to(quiz_card_3_base.get_center() + DOWN * 0.5)
        quiz_card_3 = Group(quiz_card_3_base, quiz_card_3_img, quiz_card_3_mark)
        
        quiz_card_4_base = RoundedRectangle(corner_radius=0.2, width=3.0, height=3.5, color=BLACK, stroke_width=3, fill_color=WHITE, fill_opacity=1)
        quiz_card_4_img = get_image_or_placeholder("../images/ing_words_14.png", GRAY)
        quiz_card_4_img.height = 1.5
        quiz_card_4_img.move_to(quiz_card_4_base.get_center() + UP * 0.8)
        quiz_card_4_mark = Text("?", font="Comic Sans MS", font_size=48, color=GRAY)
        quiz_card_4_mark.move_to(quiz_card_4_base.get_center() + DOWN * 0.5)
        quiz_card_4 = Group(quiz_card_4_base, quiz_card_4_img, quiz_card_4_mark)
        
        quiz_group = Group(quiz_card_1, quiz_card_2, quiz_card_3, quiz_card_4)
        quiz_group.arrange(RIGHT, buff=0.3)
        quiz_group.set_width(config.frame_width * 0.95)
        quiz_group.shift(DOWN * 0.8)
        
        self.play(FadeIn(quiz_header), run_time=0.8)
        self.play(FadeIn(quiz_group, shift=UP), run_time=2.0)
        self.wait(3.84)
        
        ## Section 5
        self.wait(3.0)
        
        ## Section 6 (Reveal)
        quiz_ans_1 = MarkupText("He <span fgcolor=\"#61D262\"><b>is</b></span> running.", font="Comic Sans MS", font_size=24, color=BLACK)
        quiz_ans_1.move_to(quiz_card_1_mark.get_center())
        
        quiz_ans_2 = MarkupText("She <span fgcolor=\"#61D262\"><b>is</b></span> singing.", font="Comic Sans MS", font_size=24, color=BLACK)
        quiz_ans_2.move_to(quiz_card_2_mark.get_center())
        
        quiz_ans_3 = MarkupText("They <span fgcolor=\"#61D262\"><b>are</b></span> jumping.", font="Comic Sans MS", font_size=24, color=BLACK)
        quiz_ans_3.move_to(quiz_card_3_mark.get_center())
        
        quiz_ans_4 = MarkupText("It <span fgcolor=\"#61D262\"><b>is</b></span> sleeping.", font="Comic Sans MS", font_size=24, color=BLACK)
        quiz_ans_4.move_to(quiz_card_4_mark.get_center())
        
        reveal_anims = [
            Transform(quiz_card_1_mark, quiz_ans_1),
            Flash(quiz_card_1, color="#EF9515", flash_radius=1.2),
            Transform(quiz_card_2_mark, quiz_ans_2),
            Flash(quiz_card_2, color="#EF9515", flash_radius=1.2),
            Transform(quiz_card_3_mark, quiz_ans_3),
            Flash(quiz_card_3, color="#EF9515", flash_radius=1.2),
            Transform(quiz_card_4_mark, quiz_ans_4),
            Flash(quiz_card_4, color="#EF9515", flash_radius=1.2)
        ]
        
        self.play(LaggedStart(*reveal_anims, lag_ratio=0.5), run_time=4.0)
        self.wait(1.12)
        self.play(FadeOut(quiz_header), FadeOut(quiz_group), run_time=1.0)
        
        ## Section 7
        rays = VGroup(*[AnnularSector(inner_radius=0, outer_radius=10, angle=TAU/40, start_angle=i*TAU/20, color=YELLOW_A, fill_opacity=0.3) for i in range(20)]).move_to(ORIGIN)
        
        star = Star(n=12, outer_radius=2.5, inner_radius=1.2, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=5)
        
        final_txt_outline = Text("Good Job!", font="Comic Sans MS", weight=BOLD, font_size=80, color=RED).set_stroke(WHITE, 10)
        final_txt_fill = Text("Good Job!", font="Comic Sans MS", weight=BOLD, font_size=80, color=RED).set_stroke(RED, 0)
        final_txt = VGroup(final_txt_outline, final_txt_fill).move_to(ORIGIN)
        
        txt_sub = Text("Keep Practicing!", font="Comic Sans MS", weight=BOLD, font_size=40, color="#333333").set_stroke(width=0).next_to(star, DOWN, buff=0.5)
        
        confetti = VGroup()
        for _ in range(50):
            c = Square(side_length=0.15, fill_color=random.choice([RED, BLUE, GREEN, YELLOW, PINK, ORANGE]), fill_opacity=1, stroke_width=0)
            c.move_to(ORIGIN)
            confetti.add(c)
        
        self.play(FadeIn(rays), run_time=1.0)
        self.play(GrowFromCenter(star, rate_func=rate_functions.ease_out_elastic), Rotate(rays, angle=PI/2, rate_func=linear), run_time=1.0)
        self.play(GrowFromCenter(final_txt, rate_func=rate_functions.ease_out_elastic), Rotate(rays, angle=PI/2, rate_func=linear), run_time=1.0)
        
        confetti_anims = [c.animate.shift(np.array([random.uniform(-5, 5), random.uniform(-4, 4), 0])).rotate(random.uniform(0, TAU*2)) for c in confetti]
        
        self.play(
            LaggedStart(*confetti_anims, lag_ratio=0),
            FadeIn(txt_sub, shift=UP),
            Rotate(rays, angle=PI, rate_func=linear),
            run_time=4.0
        )
        self.wait(0.19)
        
        self.play(FadeOut(rays), FadeOut(star), FadeOut(final_txt), FadeOut(txt_sub), FadeOut(confetti), run_time=1.0)
