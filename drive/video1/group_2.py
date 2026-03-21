from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        H = config.frame_height
        W = config.frame_width

        LAYOUT = {
            "header_title_size": 48 * (H / 8.0),
            "header_sub_size": 24 * (H / 8.0),
            "card_text_size": 20 * (H / 8.0),
            "header_strip_height": H * 0.18,
            "header_strip_width": W * 0.85,
            "content_margin_x": W * 0.05,
            "tiny_buff": H * 0.015,
            "small_buff": H * 0.03,
            "medium_buff": H * 0.05,
            "large_buff": H * 0.1,
            "section_spacing": H * 0.03,
            "theme": {
                "background_color": "#2C3336",
                "header_bg": "#4280A7",
                "text_primary": "#61D262",
                "text_secondary": "#FFFFFF",
                "highlight": "#EF9515",
            }
        }

        self.camera.background_color = LAYOUT["theme"]["background_color"]

        title_font = "Bubblegum Sans"
        body_font = "Source Sans 3"

        ## Section 1

        title = Text(
            "Articles: a, an",
            font_size=LAYOUT["header_title_size"],
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        subtitle = Text(
            "When to use 'a' and 'an'?",
            font_size=LAYOUT["header_sub_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        )

        header_group = VGroup(title, subtitle).arrange(DOWN, buff=LAYOUT["small_buff"])

        header_bg = RoundedRectangle(
            width=LAYOUT["header_strip_width"],
            height=LAYOUT["header_strip_height"],
            corner_radius=0.2,
            fill_color=LAYOUT["theme"]["header_bg"],
            fill_opacity=1,
            stroke_width=0
        )

        header_bg.scale(0.05)
        header_bg.move_to(ORIGIN)

        header_group.move_to(header_bg.get_center())
        header_full = VGroup(header_bg, header_group)

        self.play(header_bg.animate.scale(20), run_time=1.2)

        self.play(
            title.animate.shift(DOWN * LAYOUT["small_buff"]).set_opacity(1),
            run_time=1.0
        )

        self.play(Write(subtitle), run_time=0.55)

        self.play(
            header_full.animate.to_edge(UP, buff=0.25),
            run_time=0.97        )

        ## Section 2

        concept_bg = RoundedRectangle(
            width=W * 0.9,
            height=H * 0.35, # Increased height slightly to accommodate larger text
            corner_radius=0.2,
            fill_color="#232D3F", # Darker color for better contrast
            fill_opacity=1,
            stroke_width=0
        )

        concept_bg.next_to(header_bg, DOWN, buff=LAYOUT["section_spacing"])
        concept_bg.set_x(0)
        concept_bg.scale(0.001, about_edge=LEFT)

        concept_title = Text(
            "The Sound Rule!",
            font_size=LAYOUT["header_title_size"] * 0.6,
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        concept_desc_1 = Tex(
            "We use 'a' before words that begin with a consonant sound.",
            substrings_to_isolate=["consonant sound"],
            font_size=LAYOUT["card_text_size"] * 1.3, # Increased font size
            color=LAYOUT["theme"]["text_secondary"]
        )

        concept_desc_2 = Tex(
            "We use 'an' before words that begin with a vowel sound.",
            substrings_to_isolate=["vowel sound"],
            font_size=LAYOUT["card_text_size"] * 1.3, # Increased font size
            color=LAYOUT["theme"]["text_secondary"]
        )

        concept_group = VGroup(concept_title, concept_desc_1, concept_desc_2).arrange(DOWN, buff=LAYOUT["small_buff"])

        self.play(concept_bg.animate.scale(1000, about_edge=LEFT), run_time=1.2)

        concept_group.move_to(concept_bg.get_center())

        self.play(Write(concept_title), run_time=0.8)

        self.play(AddTextLetterByLetter(concept_desc_1), run_time=2.5)

        consonant_part = concept_desc_1.get_part_by_tex("consonant sound")
        self.play(consonant_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.6)

        self.play(AddTextLetterByLetter(concept_desc_2), run_time=2.5)

        vowel_part = concept_desc_2.get_part_by_tex("vowel sound")
        self.play(vowel_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.6)


        self.play(concept_bg.animate.scale(0.001, about_edge=LEFT).set_opacity(0), run_time=0.33)

        self.play(FadeOut(concept_group), run_time=0.1)

        ## Section 3

        self.wait(4.61)

        ## Section 4

        doll_img = ImageMobject("../images/articles_2.png")
        doll_img.scale_to_fit_width(W * 0.14) # Further reduced size

        doll_position = np.array([-W * 0.28, H * 0.15, 0]) # Lowered from header
        doll_img.move_to(doll_position)

        self.play(GrowFromCenter(doll_img), run_time=1.238)

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(doll_img).scale(0.6),
            run_time=1.038
        )

        doll_txt = Tex(
            "a doll",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_primary"]
        )
        doll_txt.next_to(doll_img, DOWN, buff=0.25)

        self.play(Write(doll_txt), run_time=0.838)

        doll_txt_new = Tex(
            "Doll starts with a 'd' sound.\\\\ 'd' is a consonant.\\\\ So we say: a doll.", # More wrapping
            substrings_to_isolate=["'d'", "a doll"],
            font_size=LAYOUT["card_text_size"] * 0.85,
            color=LAYOUT["theme"]["text_secondary"]
        )
        doll_txt_new.next_to(doll_img, DOWN, buff=0.25)

        self.play(ReplacementTransform(doll_txt, doll_txt_new), run_time=0.838)

        doll_d_part = doll_txt_new.get_part_by_tex("'d'")
        doll_article_part = doll_txt_new.get_part_by_tex("a doll")

        self.play(doll_d_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.637)

        self.play(doll_article_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.637)

        self.wait(1.038)

        self.play(Restore(self.camera.frame), run_time=1.917)

        ## Section 5

        cup_img = ImageMobject("../images/articles_3.png")
        cup_img.scale_to_fit_width(W * 0.14) # Further reduced size

        cup_position = np.array([W * 0.28, H * 0.15, 0]) # Lowered from header
        cup_img.move_to(cup_position)

        self.play(GrowFromCenter(cup_img), run_time=1.237)

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(cup_img).scale(0.6),
            run_time=1.037
        )

        cup_txt = Tex(
            "a cup",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_primary"]
        )
        cup_txt.next_to(cup_img, DOWN, buff=0.25)

        self.play(Write(cup_txt), run_time=0.837)

        cup_txt_new = Tex(
            "Cup starts with a 'c' sound.\\\\ 'c' is a consonant.\\\\ So we say: a cup.", # More wrapping
            substrings_to_isolate=["'c'", "a cup"],
            font_size=LAYOUT["card_text_size"] * 0.85,
            color=LAYOUT["theme"]["text_secondary"]
        )
        cup_txt_new.next_to(cup_img, DOWN, buff=0.25)

        self.play(ReplacementTransform(cup_txt, cup_txt_new), run_time=0.837)

        cup_c_part = cup_txt_new.get_part_by_tex("'c'")
        cup_article_part = cup_txt_new.get_part_by_tex("a cup")

        self.play(cup_c_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.637)

        self.play(cup_article_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.637)

        self.wait(1.037)

        self.play(Restore(self.camera.frame), run_time=2.458)

        ## Section 6

        umbrella_img = ImageMobject("../images/articles_4.png")
        umbrella_img.scale_to_fit_width(W * 0.14) # Further reduced size

        umbrella_position = np.array([-W * 0.28, -H * 0.28, 0]) # Lowered to avoid overlap with doll text
        umbrella_img.move_to(umbrella_position)

        self.play(GrowFromCenter(umbrella_img), run_time=1.438)

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(umbrella_img).scale(0.6),
            run_time=1.238
        )

        umbrella_txt = Tex(
            "an umbrella",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_primary"]
        )
        umbrella_txt.next_to(umbrella_img, DOWN, buff=0.25)

        self.play(Write(umbrella_txt), run_time=1.038)

        umbrella_txt_new = Tex(
            "Umbrella starts with an 'u' sound.\\\\ 'u' is a vowel.\\\\ So we say: an umbrella.", # More wrapping
            substrings_to_isolate=["'u'", "an umbrella"],
            font_size=LAYOUT["card_text_size"] * 0.8,
            color=LAYOUT["theme"]["text_secondary"]
        )
        umbrella_txt_new.next_to(umbrella_img, DOWN, buff=0.25)

        self.play(ReplacementTransform(umbrella_txt, umbrella_txt_new), run_time=1.038)

        umbrella_u_part = umbrella_txt_new.get_part_by_tex("'u'")
        umbrella_article_part = umbrella_txt_new.get_part_by_tex("an umbrella")

        self.play(umbrella_u_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.838)

        self.play(umbrella_article_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.838)

        self.wait(1.238)

        self.play(Restore(self.camera.frame), run_time=3.678)

        ## Section 7

        orange_img = ImageMobject("../images/articles_5.png")
        orange_img.scale_to_fit_width(W * 0.14) # Further reduced size

        orange_position = np.array([W * 0.28, -H * 0.28, 0]) # Lowered to avoid overlap with cup text
        orange_img.move_to(orange_position)

        self.play(GrowFromCenter(orange_img), run_time=1.337)

        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.move_to(orange_img).scale(0.6),
            run_time=1.137
        )

        orange_txt = Tex(
            "an orange",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_primary"]
        )
        orange_txt.next_to(orange_img, DOWN, buff=0.25)

        self.play(Write(orange_txt), run_time=0.938)

        orange_txt_new = Tex(
            "Orange starts with an 'o' sound.\\\\ 'o' is a vowel.\\\\ So we say: an orange.", # More wrapping
            substrings_to_isolate=["'o'", "an orange"],
            font_size=LAYOUT["card_text_size"] * 0.8,
            color=LAYOUT["theme"]["text_secondary"]
        )
        orange_txt_new.next_to(orange_img, DOWN, buff=0.25)

        self.play(ReplacementTransform(orange_txt, orange_txt_new), run_time=0.938)

        orange_o_part = orange_txt_new.get_part_by_tex("'o'")
        orange_article_part = orange_txt_new.get_part_by_tex("an orange")

        self.play(orange_o_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.738)

        self.play(orange_article_part.animate.set_color(LAYOUT["theme"]["highlight"]), run_time=0.738)

        self.wait(1.137)

        self.play(Restore(self.camera.frame), run_time=2.647)

        ## Section 8

        doll_group = Group(doll_img, doll_txt_new)
        cup_group = Group(cup_img, cup_txt_new)
        umbrella_group = Group(umbrella_img, umbrella_txt_new)
        orange_group = Group(orange_img, orange_txt_new)

        doll_absorb = doll_group.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        cup_absorb = cup_group.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        umbrella_absorb = umbrella_group.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        orange_absorb = orange_group.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)

        self.play(
            LaggedStart(doll_absorb, cup_absorb, umbrella_absorb, orange_absorb, lag_ratio=0.2),
            run_time=3.3
        )

        self.play(
            Flash(header_bg, color=LAYOUT["theme"]["header_bg"], line_length=0.2, num_lines=12),
            run_time=1.3
        )

        self.play(
            header_full.animate.shift(UP * config.frame_height),
            run_time=3.16
        )
