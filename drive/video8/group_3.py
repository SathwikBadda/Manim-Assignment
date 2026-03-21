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
            "More Divisibility Rules!",
            font_size=LAYOUT["header_title_size"],
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        subtitle = Text(
            "Look for patterns in groups of digits or combined rules!",
            font_size=LAYOUT["header_sub_size"] * 2,
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        ).scale(0.5)

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

        self.play(header_bg.animate.scale(20), run_time=0.9)

        self.play(
            title.animate.shift(DOWN * LAYOUT["small_buff"]).set_opacity(1),
            run_time=0.7
        )

        self.play(Write(subtitle), run_time=0.7)

        self.play(
            self.camera.frame.animate.scale(1.05),
            run_time=0.3
        )

        self.play(
            self.camera.frame.animate.scale(1.0),
            run_time=0.3        )

        self.play(
            header_full.animate.to_edge(UP, buff=0.25),
            run_time=0.1        )

        ## Section 2

        content_bg = RoundedRectangle(
            width=W * 0.9,
            height=H * 0.2,
            corner_radius=0.2,
            fill_color="#3A4A5A",
            fill_opacity=1,
            stroke_width=0
        )

        content_bg.next_to(header_bg, DOWN, buff=LAYOUT["section_spacing"])
        content_bg.set_x(0)
        content_bg.scale(0.001, about_edge=LEFT)

        content_text = Text(
            "Sometimes we look at the last few digits, or combine rules!",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        )

        self.play(content_bg.animate.scale(1000, about_edge=LEFT), run_time=1.867)

        content_text.move_to(content_bg.get_center())
        self.add(content_text)

        self.play(AddTextLetterByLetter(content_text), run_time=7.367)

        self.play(
            content_bg.animate.scale(0.001, about_edge=LEFT),
            FadeOut(content_text),
            run_time=1.137
        )

        ## Section 3
        self.camera.frame.save_state()

        num_5200 = Text(
            "5200",
            font_size=LAYOUT["header_title_size"] * 1.5,
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        num_5200_pos = np.array([-W * 0.25, H * 0.10, 0])
        num_5200.move_to(num_5200_pos)

        self.play(GrowFromCenter(num_5200), run_time=2.643)

        self.play(
            self.camera.frame.animate.move_to(num_5200).scale(0.5),
            run_time=2.943
        )

        self.play(
            num_5200[-2:].animate.set_color(LAYOUT["theme"]["highlight"]),
            run_time=2.443
        )

        rule_text_5200 = Text(
            "Rule for 4: Last two digits are 00 or divisible by 4.",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"00": LAYOUT["theme"]["highlight"]}
        )

        rule_text_5200.next_to(num_5200, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(rule_text_5200), run_time=3.443)

        explanation_5200 = Text(
            "'00' is divisible by 4. So 5200 is divisible by 4!",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"'00'": LAYOUT["theme"]["highlight"]}
        )

        explanation_5200.next_to(rule_text_5200, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(explanation_5200), run_time=3.943)

        self.play(Restore(self.camera.frame), run_time=2.743)

        self.wait(1.503)

        ## Section 4
        self.camera.frame.save_state()

        num_8512 = Text(
            "8512",
            font_size=LAYOUT["header_title_size"] * 1.5,
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        num_8512_pos = np.array([W * 0.25, H * 0.10, 0])
        num_8512.move_to(num_8512_pos)

        self.play(GrowFromCenter(num_8512), run_time=2.0)

        self.play(
            self.camera.frame.animate.move_to(num_8512).scale(0.5),
            run_time=2.3
        )

        self.play(
            num_8512[-2:].animate.set_color(LAYOUT["theme"]["highlight"]),
            run_time=1.6
        )

        rule_text_8512 = Text(
            "Rule for 4: Last two digits are 00 or divisible by 4.",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"00": LAYOUT["theme"]["highlight"]}
        )

        rule_text_8512.next_to(num_8512, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(rule_text_8512), run_time=2.6)

        explanation_8512 = Text(
            "'12' is divisible by 4. So 8512 is divisible by 4!",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"'12'": LAYOUT["theme"]["highlight"]}
        )

        explanation_8512.next_to(rule_text_8512, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(explanation_8512), run_time=3.2)

        self.play(Restore(self.camera.frame), run_time=2.1)

        self.wait(0.84)

        ## Section 5

        self.camera.frame.save_state()

        num_324 = Text(
            "324",
            font_size=LAYOUT["header_title_size"] * 1.5,
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        num_324_pos = np.array([-W * 0.25, -H * 0.25, 0])
        num_324.move_to(num_324_pos)

        self.play(GrowFromCenter(num_324), run_time=2.056)

        self.play(
            self.camera.frame.animate.move_to(num_324).scale(0.5),
            run_time=2.256
        )

        self.play(
            num_324[-1:].animate.set_color(LAYOUT["theme"]["highlight"]),
            run_time=1.656
        )

        digit_sum_324 = Text(
            "3+2+4=9",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"4": LAYOUT["theme"]["highlight"]}
        )

        digit_sum_324.next_to(num_324, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(digit_sum_324), run_time=2.056)

        self.play(
            digit_sum_324[-1:].animate.set_color(LAYOUT["theme"]["highlight"]),
            run_time=1.656
        )

        rule_text_324 = Text(
            "Rule for 6: Divisible by both 2 AND 3.",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        )

        rule_text_324.next_to(digit_sum_324, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(rule_text_324), run_time=2.656)

        explanation_324 = Text(
            "324 is divisible by 2 and 3. So 324 is divisible by 6!",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        )

        explanation_324.next_to(rule_text_324, DOWN, buff=LAYOUT["small_buff"])

        self.play(Write(explanation_324), run_time=3.356)

        self.play(Restore(self.camera.frame), run_time=2.156)

        self.wait(0.906)

        ## Section 6
        self.camera.frame.save_state()

        num_5192 = Text(
            "5192",
            font_size=LAYOUT["header_title_size"] * 1.5,
            color=LAYOUT["theme"]["text_primary"],
            font=title_font
        )

        num_5192_pos = np.array([W * 0.25, -H * 0.25, 0])
        num_5192.move_to(num_5192_pos)

        self.play(GrowFromCenter(num_5192), run_time=2.2)

        self.play(
            self.camera.frame.animate.move_to(num_5192).scale(0.5),
            run_time=2.4
        )

        self.play(
            num_5192[-3:].animate.set_color(LAYOUT["theme"]["highlight"]),
            run_time=1.8
        )

        division_5192 = Text(
            "192 ÷ 8 = 24",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"192": LAYOUT["theme"]["highlight"]}
        )

        division_5192.next_to(num_5192, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(division_5192), run_time=2.2)

        rule_text_5192 = Text(
            "Rule for 8: Last three digits form a number divisible by 8.",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font
        )

        rule_text_5192.next_to(division_5192, DOWN, buff=LAYOUT["medium_buff"])

        self.play(Write(rule_text_5192), run_time=3.0)

        explanation_5192 = Text(
            "'192' is divisible by 8. So 5192 is divisible by 8!",
            font_size=LAYOUT["card_text_size"],
            color=LAYOUT["theme"]["text_secondary"],
            font=body_font,
            t2c={"'192'": LAYOUT["theme"]["highlight"]}
        )

        explanation_5192.next_to(rule_text_5192, DOWN, buff=LAYOUT["small_buff"])

        self.play(Write(explanation_5192), run_time=3.4)

        self.play(Restore(self.camera.frame), run_time=2.3)

        self.wait(1.04)

        ## Section 7

        example_1 = Group(num_5200, rule_text_5200, explanation_5200)
        example_2 = Group(num_8512, rule_text_8512, explanation_8512)
        example_3 = Group(num_324, digit_sum_324, rule_text_324, explanation_324)
        example_4 = Group(num_5192, division_5192, rule_text_5192, explanation_5192)

        anim_1 = example_1.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        anim_2 = example_2.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        anim_3 = example_3.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)
        anim_4 = example_4.animate.move_to(header_bg.get_center()).scale(0.05).set_opacity(0)

        self.play(
            LaggedStart(anim_1, anim_2, anim_3, anim_4, lag_ratio=0.2),
            run_time=3.5
        )

        self.play(
            Flash(header_bg, color=LAYOUT["theme"]["highlight"], line_length=0.2, num_lines=12),
            run_time=0.8
        )

        self.play(
            header_full.animate.shift(UP * config.frame_height),
            run_time=0.88
        )

if __name__ == "__main__":
    config.processes = 4  # Use 4 CPU cores
    config.max_files_cached = 200  # Helps with memory management
    config.progress_bar = "none"
    config.enable_cuda = True
    config.disable_caching = True
    #config.background_color = "#ffffff"
    config.pixel_height = 360
    config.pixel_width = 640
    config.frame_rate = 15
    #config.pixel_height = 180
    #config.pixel_width = 320
    #config.frame_rate = 10
    from pathlib import Path
    import shutil

    scene_to_render = FinalScene()
    scene_to_render.render()

    file_dir = Path(r"../manim_raw_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "group_3.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")