from manim import *

import random
import textwrap

import numpy as np

from math import pi, sin, cos

class FinalScene(MovingCameraScene):
    def construct(self):
        main_font = "Helvetica"
        BASE = config.frame_height / 8
        TITLE_SIZE = 40 * BASE
        LABEL_SIZE = 30 * BASE
        QUESTION_SIZE = 64 * BASE
        SMALL_SIZE = 22 * BASE
        CONST_SIZE = 28 * BASE

        PRIMARY_TEXT = "#61D262"
        SECONDARY_TEXT = "#E1DBD5"
        PRIMARY_SHAPE_ACCENT = "#3B447D"
        BG_COLOR = "#031422"

        self.camera.background_color = BG_COLOR


        temp_title = Text("Understanding Diseases: What Makes Us Sick?", font_size=TITLE_SIZE, font=main_font).to_corner(UL, buff=0.5)
        temp_label = Text("Defining the Condition", font_size=LABEL_SIZE, font=main_font).next_to(temp_title, DOWN, buff=0.6, aligned_edge=LEFT)
        
        temp_q = Tex(
            r"A disease is a condition that disturbs the normal working\\",
            r"of the body or mind. It occurs when one or more organs\\",
            r"or organ systems stop functioning properly.",
            font_size=QUESTION_SIZE
        ).next_to(temp_label, DOWN, buff=0.2, aligned_edge=LEFT)
        temp_q.set(width=config.frame_width * 0.5)
        
        temp_div = Line(LEFT, RIGHT, stroke_width=2, color=PRIMARY_SHAPE_ACCENT).next_to(temp_q, DOWN, buff=0.3, aligned_edge=LEFT)
        temp_div.set(width=temp_q.width)

        DIVIDER_Y = temp_div.get_y()

        body_illustration = ImageMobject("../images/ace_disease_1.png")
        body_illustration.set(width=config.frame_width * 0.4)
        body_illustration.move_to(
            RIGHT * (config.frame_width / 2 - body_illustration.width / 2 - 0.5) + UP * (DIVIDER_Y - 2.0),
            aligned_edge=DOWN
        )

        ## Section 1
        title = Text(
            "Understanding Diseases: What Makes Us Sick?",
            font_size=TITLE_SIZE,
            weight=BOLD,
            font=main_font,
            color=PRIMARY_TEXT
        )
        title.to_corner(UL, buff=0.5)

        self.play(
            Write(title),
            run_time=4.73
        )

        self.play(
            FadeIn(body_illustration, shift=UP),
            run_time=2.36
        )

        self.play(
            body_illustration.animate.scale(1.05),
            run_time=2.37
        )

        ## Section 2
        label = Text(
            "Defining the Condition",
            font_size=LABEL_SIZE,
            weight=BOLD,
            font=main_font,
            color=SECONDARY_TEXT
        )
        label.next_to(title, DOWN, buff=0.6, aligned_edge=LEFT)

        self.play(FadeIn(label, shift=RIGHT), run_time=8.8)

        ## Section 3
        question_text = Tex(
            r"A disease is a condition that disturbs the normal working\\",
            r"of the body or mind. It occurs when one or more organs\\",
            r"or organ systems stop functioning properly.",
            substrings_to_isolate=["disturbs the normal working", "organs or organ systems stop functioning properly"],
            font_size=QUESTION_SIZE,
            color=PRIMARY_TEXT,
            tex_environment="flushleft"
        )
        question_text.set(width=config.frame_width * 0.5)
        question_text.next_to(label, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(question_text), run_time=6.0)

        kw_colors = {
            "disturbs the normal working": PRIMARY_SHAPE_ACCENT,
            "organs or organ systems stop functioning properly": PRIMARY_SHAPE_ACCENT
        }
        self.play(
            question_text.animate.set_color_by_tex_to_color_map(kw_colors),
            run_time=3.24
        )

        ## Section 4
        divider = Line(start=LEFT, end=RIGHT, stroke_width=2, color=PRIMARY_SHAPE_ACCENT)
        divider.set(width=question_text.width)
        divider.next_to(question_text, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(Create(divider), run_time=8.4)

        ## Section 5
        main_causes_title = Text(
            "Main Causes",
            font_size=LABEL_SIZE,
            weight=BOLD,
            font=main_font,
            color=PRIMARY_TEXT
        )
        main_causes_title.next_to(divider, DOWN, buff=0.6, aligned_edge=LEFT)

        rule_statement = Tex(
            r"Diseases are primarily caused by Pathogens OR Lifestyle/Environment.",
            font_size=QUESTION_SIZE,
            color=PRIMARY_TEXT,
            tex_environment="flushleft"
        )
        rule_statement.set(width=config.frame_width * 0.5)
        rule_statement.next_to(main_causes_title, DOWN, buff=0.3, aligned_edge=LEFT)

        explanatory_text_content = "Pathogens are disease-causing germs like bacteria, viruses, fungi, protozoa, or worms."
        wrapped_text = "\n".join(textwrap.wrap(explanatory_text_content, width=50))
        explanatory_note = Text(
            wrapped_text,
            font_size=SMALL_SIZE,
            font=main_font,
            color=SECONDARY_TEXT,
            line_spacing=1.5
        )
        explanatory_note.next_to(rule_statement, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(main_causes_title), run_time=3.57)

        self.play(Write(rule_statement), run_time=4.27)

        self.play(FadeIn(explanatory_note, shift=UP * 0.2), run_time=2.86)

        ## Section 6
        pathogen_header = Text(
            "Pathogen Examples",
            font_size=LABEL_SIZE,
            weight=BOLD,
            font=main_font,
            color=PRIMARY_SHAPE_ACCENT
        )

        pathogen_body = Tex(
            r"Bacteria, Viruses, Fungi, Protozoa, Worms",
            font_size=CONST_SIZE,
            color=SECONDARY_TEXT
        )

        pathogen_group = VGroup(pathogen_header, pathogen_body).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )

        pathogen_box = SurroundingRectangle(
            pathogen_group,
            buff=0.3,
            corner_radius=0.1,
            stroke_color=PRIMARY_SHAPE_ACCENT,
            stroke_width=2,
            fill_color=PRIMARY_SHAPE_ACCENT,
            fill_opacity=0.15
        )

        pathogen_panel = Group(pathogen_box, pathogen_group)
        pathogen_panel.to_edge(RIGHT, buff=0.1)
        pathogen_panel.match_y(rule_statement, direction=UP)
        pathogen_panel.shift(DOWN * 1.2)

        self.play(GrowFromCenter(pathogen_box), run_time=2.90)

        self.play(Write(pathogen_group), run_time=2.90)

        self.wait(1.89)

        all_elements = Group(title, label, question_text, divider, main_causes_title, rule_statement, explanatory_note, pathogen_panel, body_illustration)

        self.play(
            all_elements.animate.scale(0.8).move_to(ORIGIN),
            run_time=2.30
        )

        self.play(FadeOut(all_elements), run_time=1.70)
