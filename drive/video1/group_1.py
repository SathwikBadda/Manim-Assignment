from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#E0F7FA"
        
        # ==========================================
        # STATIC UI LAYER
        # ==========================================
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
        
        block_width = config.frame_width * 0.06
        base_buff = block_width * 0.15
        
        title_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        raw_words = ["English", "Alphabet"]
        title_group = VGroup()
        
        global_index = 0
        for word in raw_words:
            word_group = VGroup()
            for char in word:
                color = title_colors[global_index % len(title_colors)]
                global_index += 1
                
                block = RoundedRectangle(corner_radius=0.2, width=1, height=1, color=BLACK, stroke_width=4, fill_color=color, fill_opacity=1)
                letter = Text(char, font="Comic Sans MS", weight=BOLD, color=WHITE, font_size=60).set_stroke(BLACK, 2)
                word_group.add(VGroup(block, letter))
            
            word_group.arrange(RIGHT, buff=base_buff)
            title_group.add(word_group)
        
        title_group.arrange(DOWN, buff=0.5)
        title_group.center()
        title_group.shift(UP * 1.5) # Moved up slightly to make room for subtitle
        
        all_blocks = VGroup(*[b for wg in title_group for b in wg])
        
        destinations = [m.get_center() for m in all_blocks]
        for m in all_blocks:
            m.shift(UP * 8)
        
        drop_anims = [
            m.animate(rate_func=rate_functions.ease_out_bounce, run_time=1.532).move_to(dest)
            for m, dest in zip(all_blocks, destinations)
        ]
        
        self.play(LaggedStart(*drop_anims, lag_ratio=0.05), run_time=1.532)
        
        subtitle = Text("Vowels and Consonants", font="Comic Sans MS", weight=BOLD, font_size=40, color="#333333")
        subtitle.set_stroke(color=BLACK, width=0)
        subtitle.next_to(title_group, DOWN, buff=0.6)
        
        self.play(GrowFromCenter(subtitle, rate_func=rate_functions.ease_out_elastic), run_time=0.632)
        self.wait(0.082)
        
        self.play(FadeOut(subtitle, shift=DOWN), *[ShrinkToCenter(m) for m in title_group], run_time=0.602)

        ## Section 2
        
        rule_box = RoundedRectangle(corner_radius=0.3, width=10, height=3.5, color="#E91E63", stroke_width=8, fill_color=WHITE, fill_opacity=0.95)
        rule_box.move_to(UP * 0.5) # Lowered to avoid header
        
        badge_star = Star(n=12, outer_radius=0.8, inner_radius=0.6, color=YELLOW, fill_opacity=1, stroke_color=ORANGE, stroke_width=3)
        badge_text = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=32, color=RED).set_stroke(BLACK, 4)
        badge_group = VGroup(badge_star, badge_text).move_to(rule_box.get_corner(UL) + DOWN*0.2 + RIGHT*0.2)
        
        rule_line1 = Text("The English alphabet has 26 letters.", font="Comic Sans MS", color="#333333", font_size=36)
        rule_line1.next_to(rule_box.get_top(), DOWN, buff=0.5)
        
        rule_line2_base = "5 are Vowels: "
        rule_line2_vowels = "A, E, I, O, U"
        rule_line2 = Text(rule_line2_base, font="Comic Sans MS", color="#333333", font_size=36)
        rule_line2_colored = Text(rule_line2_vowels, font="Comic Sans MS", color="#E91E63", font_size=36, weight=BOLD)
        rule_line2_group = VGroup(rule_line2, rule_line2_colored).arrange(RIGHT, buff=0.1)
        rule_line2_group.next_to(rule_line1, DOWN, buff=0.4)
        
        rule_line3 = Text("21 are Consonants: the rest!", font="Comic Sans MS", color="#333333", font_size=36)
        rule_line3.next_to(rule_line2_group, DOWN, buff=0.4)
        
        self.play(DrawBorderThenFill(rule_box), run_time=1.5)
        self.play(SpinInFromNothing(badge_group), run_time=1.5)
        
        self.play(Write(rule_line1), run_time=1.5)
        self.play(Write(rule_line2), run_time=1.5)
        self.play(Write(rule_line2_colored), run_time=1.5)
        self.play(Write(rule_line3), run_time=1.5)
        
        self.play(Indicate(rule_box, color="#E91E63", scale_factor=1.05), run_time=1.5)
        self.wait(0.35)

        rule_section_content = VGroup(rule_box, badge_group, rule_line1, rule_line2_group, rule_line3)
        self.play(FadeOut(rule_section_content, shift=DOWN*2), run_time=1.5)
        self.wait(0.5)

        ## Section 3
        
        rule_line4_base = Text("'a' and 'an' are called Articles.", font="Comic Sans MS", color="#333333", font_size=40)
        rule_line4_base.move_to(UP * 0.5)
        
        rule_line5_text1 = Text("They are used before ", font="Comic Sans MS", color="#333333", font_size=36)
        rule_line5_text2 = Text("ONE", font="Comic Sans MS", color="#E91E63", font_size=48, weight=BOLD)
        rule_line5_text3 = Text(" noun.", font="Comic Sans MS", color="#333333", font_size=36)
        rule_line5_group = VGroup(rule_line5_text1, rule_line5_text2, rule_line5_text3).arrange(RIGHT, buff=0.25)
        rule_line5_group.next_to(rule_line4_base, DOWN, buff=0.6)
        
        apple_img = ImageMobject("../images/articles_1.png")
        apple_img.scale(0.18)
        apple_img.next_to(rule_line5_group, RIGHT, buff=0.3)
        
        articles_content = Group(rule_line4_base, rule_line5_group)
        articles_content.add(apple_img)
        articles_content.center() # Ensure it's perfectly centered in frame
        
        self.play(FadeIn(rule_line4_base, shift=UP), run_time=1.0)
        self.play(Write(rule_line5_group), run_time=1.5)
        self.play(GrowFromCenter(apple_img), run_time=1.0)
        self.wait(5.94)

        ## Section 4
        
        self.play(FadeOut(articles_content), run_time=8.07)
