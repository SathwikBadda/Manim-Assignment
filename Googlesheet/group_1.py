from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

class FinalScene(MovingCameraScene):
    def construct(self):
        H = config.frame_height
        W = config.frame_width
        
        LAYOUT = {
            "header_title_size": 48 * (H / 8.0),
            "header_sub_size": 24 * (H / 8.0),
            "section_title_size": 32 * (H / 8.0),
            "section_desc_size": 20 * (H / 8.0),
            "card_text_size": 22 * (H / 8.0),
            "header_strip_height": H * 0.3,
            "header_strip_width": W,
            "content_margin_x": W * 0.05,
            "card_img_height": H * 0.25,
            "tiny_buff": H * 0.015,
            "small_buff": H * 0.03,
            "medium_buff": H * 0.05,
            "large_buff": H * 0.1,
            "section_spacing": H * 0.03,
            "theme": {
                "background_color": "#f0edd3",
                "header_bg": "#2C3336",
                "content_bg": "#2B2E4A",
                "text_primary": "#61D262",
                "text_secondary": "#FFFFFF",
                "highlight": "#EF9515",
                "accent": "#4280A7",
            }
        }
        
        self.camera.background_color = "#f0edd3"

        title_font = "Bubblegum Sans"
        body_font = "Baloo Bhai 2"
        
        ## Section 1
        header_bg = RoundedRectangle(
            width=LAYOUT["header_strip_width"] - LAYOUT["content_margin_x"],
            height=LAYOUT["header_strip_height"],
            corner_radius=0.2,
            fill_color=LAYOUT["theme"]["header_bg"],
            fill_opacity=1,
            stroke_width=0
        )
        header_bg.to_edge(UP, buff=0)
        header_bg.scale(0.001, about_edge=LEFT)
        
        title_text = Text(
            "Measuring Length!",
            font_size=LAYOUT["header_title_size"],
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )
        title_text.shift(UP * LAYOUT["small_buff"]).set_opacity(0)
        
        subtitle_text = Text(
            "How long or short things are.",
            font_size=LAYOUT["header_sub_size"]*2,
            color=LAYOUT["theme"]["text_primary"],
            font=body_font
        ).scale(0.5)
        
        header_group = VGroup(title_text, subtitle_text).arrange(DOWN, buff=LAYOUT["small_buff"])
        
        
        self.play(header_bg.animate.scale(1000, about_edge=LEFT), run_time=1.0)
        header_group.move_to(header_bg.get_center())

        self.play(
            title_text.animate.shift(DOWN * LAYOUT["small_buff"]).set_opacity(1),
            run_time=2.0
        )
        self.play(
            Write(subtitle_text),
            run_time=2.0
        )
        
        ## Section 2
        explanation_text = Text(
            "We learn how to find the length of objects.",
            font_size=LAYOUT["section_desc_size"]*2,
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        ).scale(0.5)
        explanation_text.next_to(subtitle_text, DOWN, buff=LAYOUT["small_buff"])
        
        self.play(Write(explanation_text), run_time=2.0)
        self.wait(1.41)
        
        ## Section 3
        content_bg = RoundedRectangle(
            width=W - (LAYOUT["content_margin_x"]),
            height=H * 0.25,
            corner_radius=0.2,
            fill_color=LAYOUT["theme"]["content_bg"],
            fill_opacity=1,
            stroke_width=0
        )
        content_bg.next_to(header_bg, DOWN, buff=LAYOUT["section_spacing"])
        content_bg.set_x(0)
        content_bg.scale(0.001, about_edge=LEFT)
        
        section_title = Text(
            "Why Standard Units?",
            font_size=LAYOUT["section_title_size"],
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )
        
        section_desc_1 = Text(
            "Earlier, we used hands or feet",
            font_size=LAYOUT["section_desc_size"]*2,
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        ).scale(0.5)

        section_desc_2 = Text(
            "But everyone's hands are different sizes! So, measurements could be different!",
            font_size=LAYOUT["section_desc_size"]*2,
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        ).scale(0.5)

        
        content_group = VGroup(section_title, section_desc_1, section_desc_2).arrange(DOWN, buff=LAYOUT["small_buff"])
        
        
        self.play(content_bg.animate.scale(1000, about_edge=LEFT), run_time=1.0)
        content_group.move_to(content_bg.get_center())

        self.play(Write(section_title), run_time=2.3)
        self.play(AddTextLetterByLetter(section_desc_1), run_time=2.0)
        self.play(AddTextLetterByLetter(section_desc_2), run_time=2.0)
        
        ## Section 4
        card_width_limit = W * 0.25
        
        card_data = [
            {"img": "../images/ace_disease_1.png", "text": "This sharpener is 3 cm long.", "keyword": "3 cm"},
            {"img": "../images/ace_disease_2.png", "text": "This pencil is 10 cm long.", "keyword": "10 cm"},
            {"img": "../images/ace_disease_3.png", "text": "This eraser is 4 cm long.", "keyword": "4 cm"},
        ]
        
        cards = []
        card_images = []
        card_texts = []
        
        for item in card_data:
            img = ImageMobject(item["img"])
            img.scale_to_fit_width(W * 0.18)

            txt = Tex(
                item["text"],
                substrings_to_isolate=[item["keyword"]],
                font_size=LAYOUT["card_text_size"],
                color=LAYOUT["theme"]["text_primary"]
            )
            txt.target_keyword = item["keyword"]
            
            card_images.append(img)
            card_texts.append(txt)
            
        img_width = W * 0.18
        gap = LAYOUT["large_buff"] + img_width
        grid_positions = [LEFT * gap, ORIGIN, RIGHT * gap]
        
        for i, img in enumerate(card_images):
            img.move_to(grid_positions[i])
            
        for i, txt in enumerate(card_texts):
            txt.next_to(card_images[0], DOWN, buff=LAYOUT["tiny_buff"])
            txt.set_x(grid_positions[i][0])
            
        for img, txt in zip(card_images, card_texts):
            cards.append(Group(img, txt))
        
        cards_group = Group(*cards)
        cards_group.next_to(content_bg, DOWN, buff=LAYOUT["section_spacing"]).shift(UP*LAYOUT["small_buff"])
        
        
        grid_animations = []
        for img, txt in zip(card_images, card_texts):
            grid_animations.append(
                AnimationGroup(
                    GrowFromCenter(img),
                    Write(txt),
                    lag_ratio=0.2
                )
            )
        
        self.play(LaggedStart(*grid_animations, lag_ratio=0.3), run_time=5)
        self.wait(3.52)
        
        ## Section 5
        highlight_animations = []
        for txt in card_texts:
            keyword = txt.target_keyword
            part = txt.get_part_by_tex(keyword)
            if part:
                highlight_animations.append(
                    part.animate.set_color(LAYOUT["theme"]["highlight"]).scale(1.15)
                )
        
        self.play(LaggedStart(*highlight_animations, lag_ratio=0.2), run_time=4)
        self.wait(3.9)
        
        ## Section 6
        self.play(
            FadeOut(section_title, shift=UP),
            run_time=1.2
        )
        self.play(
            FadeOut(section_desc_1, shift=UP),
            FadeOut(section_desc_2, shift=UP),
            run_time=1.2
        )
        
        absorb_animations = []
        target_point = header_bg.get_center()
        
        for card in cards:
            anim = card.animate.move_to(target_point).scale(0.05).set_opacity(0)
            absorb_animations.append(anim)
        
        self.play(LaggedStart(*absorb_animations, lag_ratio=0.1), run_time=1.0)
        
        self.play(
            Flash(header_bg, color=WHITE, line_length=0.2, num_lines=12),
            run_time=1.5
        )
        
        self.play(
            content_bg.animate.stretch_to_fit_width(0).set_opacity(0),
            run_time=0.8        
        )
        
        self.play(
            VGroup(header_bg, header_group, explanation_text).animate.shift(UP * config.frame_height),
            run_time=1.0
        )
