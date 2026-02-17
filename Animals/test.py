from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *
import numpy as np

class FinalScene(MovingCameraScene):
    def construct(self):
        # ==========================================
        # GLOBAL CONFIGURATION
        # ==========================================
        self.camera.background_color = "#F9FAFC"
        
        # --- STATIC HEADER ---
        header_rect = Rectangle(width=config.frame_width, height=1.2, color="#3FA9F5", fill_opacity=1)
        header_rect.to_edge(UP, buff=0)
        
        # --- STATIC FOOTER (Notebook Binding) ---
        footer_colors = ["#FFB703", "#3FA9F5", "#FFB703", "#3FA9F5", "#FFB703", "#3FA9F5"]
        footer_group = VGroup()
        num_circles = int(config.frame_width / 0.4) + 2
        
        for i in range(num_circles):
            c = Circle(radius=0.18, color=WHITE, fill_color=footer_colors[i % len(footer_colors)], fill_opacity=1, stroke_width=4)
            hole = Circle(radius=0.06, color=WHITE, fill_color="#F9FAFC", fill_opacity=1, stroke_width=0)
            footer_group.add(VGroup(c, hole))
        
        footer_group.arrange(RIGHT, buff=0.1)
        footer_group.to_edge(DOWN, buff=0.2)
        
        self.add(header_rect, footer_group)

        # ==========================================
        # SECTION 1: TITLE BLOCKS AND SUBTITLE
        # ==========================================
        ## Section 1
        
        title_text = "Herbivores and Their Tools!"
        title_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE]
        title_group = VGroup()
        
        for char, color in zip(title_text, title_colors):
            block = RoundedRectangle(corner_radius=0.2, width=0.8, height=0.8, color=BLACK, stroke_width=3, fill_color=color, fill_opacity=1)
            letter = Text(char, font="Comic Sans MS", weight=BOLD, color=WHITE, font_size=48).set_stroke(BLACK, 1)
            title_group.add(VGroup(block, letter))
        
        title_group.arrange(RIGHT, buff=0.1).shift(UP*2.5)
        
        final_positions = [m.get_center() for m in title_group]
        for m in title_group:
            m.shift(UP * 7)
        
        anims = [m.animate(rate_func=rate_functions.ease_out_bounce, run_time=1.5).move_to(final_positions[i]) for i, m in enumerate(title_group)]
        self.play(LaggedStart(*anims, lag_ratio=0.08), run_time=4.24)
        
        subtitle = Text("Body parts for eating plants", font="Comic Sans MS", weight=BOLD, font_size=28, color="#444B55")
        subtitle.set_stroke(color=BLACK, width=0)
        subtitle.next_to(title_group, DOWN, buff=0.4)
        
        self.play(FadeIn(subtitle), run_time=1.92)

        # ==========================================
        # SECTION 2: RULE CARD
        # ==========================================
        ## Section 2
        
        rule_box = RoundedRectangle(corner_radius=0.3, width=9, height=2.8, color="#3FA9F5", stroke_width=2, fill_color="#3FA9F5", fill_opacity=1)
        rule_box.shift(DOWN*0.5)
        
        badge_star = Star(n=5, outer_radius=0.5, inner_radius=0.3, color="#FFB703", fill_opacity=1, stroke_color="#FFB703", stroke_width=2)
        badge_text = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=20, color=WHITE).set_stroke(BLACK, 1)
        badge_group = VGroup(badge_star, badge_text).move_to(rule_box.get_corner(UR) + DOWN*0.4 + LEFT*0.4)
        
        rule_content = Text("Herbivores have special body parts that help them eat plants easily!", font="Comic Sans MS", color="#444B55", font_size=36)
        rule_content.move_to(rule_box.get_center())
        rule_content.scale_to_fit_width(rule_box.width - 1.2)
        
        self.play(GrowFromCenter(rule_box, rate_func=rate_functions.ease_out_back), run_time=2.0)
        self.play(GrowFromCenter(badge_group), run_time=1.5)
        self.play(FadeIn(rule_content), run_time=2.5)

        # ==========================================
        # SECTION 3: COW CARD ENTRY
        # ==========================================
        ## Section 3
        
        cow_image = ImageMobject("../images/aced_science_6.png")
        
        cow_card_bg = RoundedRectangle(corner_radius=0.25, width=2.6, height=3.4, color=BLACK, stroke_width=2, fill_color="#DFDBE6", fill_opacity=1)
        cow_image.scale_to_fit_height(cow_card_bg.height*0.6)
        cow_card_bg.shift(LEFT*4.5 + DOWN*1.5)
        
        cow_image.move_to(cow_card_bg.get_center() + UP*0.6)
        
        cow_text = Text("Cows have sharp front teeth for biting and strong back teeth for grinding grass.", font="Comic Sans MS", color="#444B55", font_size=20)

        #--> Implement a wraparound logic instead
        cow_text.scale_to_fit_width(cow_card_bg.width - 0.4)
        cow_text.move_to(cow_card_bg.get_center() + DOWN*1.0)
        
        cow_card = Group(cow_card_bg, cow_image, cow_text)
        
        self.play(cow_card.animate.shift(RIGHT*1.5), run_time=3.5)
        self.play(FadeIn(cow_text), run_time=3.61)

        # ==========================================
        # SECTION 4: COW CARD PHRASE EMPHASIS
        # ==========================================
        ## Section 4
        
        sharp_phrase = Text("sharp front teeth", font="Comic Sans MS", color="#FFB703", font_size=20, weight=BOLD)
        sharp_phrase.next_to(cow_text, DOWN, buff = 0.4).shift(LEFT*0.8)
        
        strong_phrase = Text("strong back teeth", font="Comic Sans MS", color="#FFB703", font_size=20, weight=BOLD)
        strong_phrase.next_to(cow_text, DOWN, buff = 0.4).shift(RIGHT*0.5)
        
        self.play(sharp_phrase.animate.scale(1.3).set_color("#FFB703"), rate_func=rate_functions.ease_out_bounce, run_time=2.0)
        self.play(sharp_phrase.animate.scale(1/1.3), run_time=0.5)
        
        self.play(strong_phrase.animate.scale(1.3).set_color("#FFB703"), rate_func=rate_functions.ease_out_bounce, run_time=2.0)
        self.play(strong_phrase.animate.scale(1/1.3), run_time=0.81)

        # ==========================================
        # SECTION 5: ELEPHANT AND GIRAFFE CARDS
        # ==========================================
        ## Section 5
        
        elephant_image = ImageMobject("../images/aced_science_7.png")
        elephant_image.scale_to_fit_height(2.2)
        
        elephant_card_bg = RoundedRectangle(corner_radius=0.25, width=4.5, height=5.5, color=BLACK, stroke_width=2, fill_color="#FBEDDA", fill_opacity=1)
        elephant_card_bg.shift(RIGHT*3.5 + DOWN*1.5)
        
        elephant_image.move_to(elephant_card_bg.get_center() + UP*1.2)
        
        elephant_text = Text("Elephants use their long trunks to pull out leaves and grass.", font="Comic Sans MS", color="#444B55", font_size=20)
        elephant_text.scale_to_fit_width(elephant_card_bg.width - 0.4)
        elephant_text.move_to(elephant_card_bg.get_center() + DOWN*1.5)
        
        elephant_card = Group(elephant_card_bg, elephant_image, elephant_text)
        
        self.play(elephant_card.animate.shift(LEFT*3.5), run_time=1.0)
        
        long_trunks_phrase = Text("long trunks", font="Comic Sans MS", color="#FFB703", font_size=20, weight=BOLD)
        long_trunks_phrase.move_to(elephant_card_bg.get_center() + DOWN*1.4)
        
        self.play(FadeIn(elephant_text), run_time=1.5)
        self.play(long_trunks_phrase.animate.scale(1.3).set_color("#FFB703"), rate_func=rate_functions.ease_out_bounce, run_time=1.5)
        self.play(long_trunks_phrase.animate.scale(1/1.3), run_time=0.5)
        
        giraffe_image = ImageMobject("../images/aced_science_8.png")
        giraffe_image.scale_to_fit_height(2.2)
        
        giraffe_card_bg = RoundedRectangle(corner_radius=0.25, width=4.5, height=5.5, color=BLACK, stroke_width=2, fill_color="#DFDBE6", fill_opacity=1)
        giraffe_card_bg.shift(LEFT*3.5 + DOWN*4.5)
        
        giraffe_image.move_to(giraffe_card_bg.get_center() + UP*1.2)
        
        giraffe_text = Text("Giraffes use their long necks to reach leaves on tall trees.", font="Comic Sans MS", color="#444B55", font_size=20)
        giraffe_text.scale_to_fit_width(giraffe_card_bg.width - 0.4)
        giraffe_text.move_to(giraffe_card_bg.get_center() + DOWN*1.5)
        
        giraffe_card = Group(giraffe_card_bg, giraffe_image, giraffe_text)
        
        self.play(giraffe_card.animate.shift(RIGHT*3.5), run_time=1.0)
        
        long_necks_phrase = Text("long necks", font="Comic Sans MS", color="#FFB703", font_size=20, weight=BOLD)
        long_necks_phrase.move_to(giraffe_card_bg.get_center() + DOWN*1.4)
        
        self.play(FadeIn(giraffe_text), run_time=1.01)
        self.play(long_necks_phrase.animate.scale(1.3).set_color("#FFB703"), rate_func=rate_functions.ease_out_bounce, run_time=0.1)
        self.play(long_necks_phrase.animate.scale(1/1.3), run_time=0.1)

        # ==========================================
        # SECTION 6: FINAL STATE
        # ==========================================
        ## Section 6
        
        self.wait(7.2)
