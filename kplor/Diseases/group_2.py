from manim import *

import random

import numpy as np

from math import pi, sin, cos
import textwrap

class FinalScene(MovingCameraScene):
    def construct(self):
        # Color Palette
        PRIMARY_TEXT_COLOR = "#61D262"
        SECONDARY_TEXT_COLOR = "#E1DBD5"
        PRIMARY_SHAPE_ACCENT = "#3B447D"
        SECONDARY_SHAPE_ACCENT = "#3774B4"
        BACKGROUND_COLOR = "#031422"

        self.camera.background_color = BACKGROUND_COLOR

        ## Section 1
        title = Tex(
            "Classifying Diseases: How They Spread",
            color=PRIMARY_TEXT_COLOR,
            font_size=44
        ).scale(1.1)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=8.43)

        ## Section 2
        pole_height = 4.5
        pole_width = 0.15
        left_pole = Rectangle(
            height=pole_height,
            width=pole_width,
            fill_color=PRIMARY_SHAPE_ACCENT,
            fill_opacity=1,
            stroke_width=0
        )
        right_pole = Rectangle(
            height=pole_height,
            width=pole_width,
            fill_color=SECONDARY_SHAPE_ACCENT,
            fill_opacity=1,
            stroke_width=0
        )
        pole = VGroup(left_pole, right_pole).arrange(RIGHT, buff=0).move_to(DOWN * 0.5)
        self.play(GrowFromEdge(pole, DOWN), run_time=4.24)
        
        subtitle = Tex(
            "Two Main Categories",
            color=PRIMARY_TEXT_COLOR,
            font_size=32
        ).scale(0.7)
        subtitle.next_to(pole, UP, buff=0.6)
        self.play(Write(subtitle), run_time=4.24)

        ## Section 3
        bar_width = 3.5
        bar_height = 1.2
        gap = 2.2

        pos_top = pole.get_top() + DOWN * 0.6
        pos_mid = pos_top + DOWN * (gap + bar_height)

        def create_bar(pos, color):
            final = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos)
            start = final.copy().stretch_to_fit_width(0.01)
            return start, final

        top_start, top_end = create_bar(pos_top, PRIMARY_SHAPE_ACCENT)
        bot_start, bot_end = create_bar(pos_mid, SECONDARY_SHAPE_ACCENT)

        self.add(top_start, bot_start)

        self.play(
            LaggedStart(
                Transform(top_start, top_end),
                Transform(bot_start, bot_end),
                lag_ratio=0.25
            ),
            run_time=8.88
        )

        bar_1 = top_start
        bar_3 = bot_start

        ## Section 4
        icon_1 = ImageMobject("../images/ace_disease_2.png").scale(0.2).move_to(bar_1.get_left() + RIGHT * 0.5)
        icon_3 = ImageMobject("../images/ace_disease_3.png").scale(0.2).move_to(bar_3.get_left() + RIGHT * 0.5)

        t_1 = Paragraph(
            *textwrap.wrap("Non-Communicable Diseases (NCDs)", width=22),
            "Do NOT Spread",
            font_size=16,
            color=SECONDARY_TEXT_COLOR,
            line_spacing=0.8
        ).next_to(icon_1, RIGHT, buff=0.1)

        t_3 = Paragraph(
            *textwrap.wrap("Communicable Diseases", width=22),
            "DO Spread",
            font_size=16,
            color=SECONDARY_TEXT_COLOR,
            line_spacing=0.8
        ).next_to(icon_3, RIGHT, buff=0.1)

        rows = [(icon_1, t_1), (icon_3, t_3)]

        icon_anims = []
        text_anims = []

        for icon, text in rows:
            self.add(icon)
            icon_anims.append(Rotate(icon, angle=2*PI, axis=UP))
            text_anims.append(Write(text))

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(icon_anim, text_anim)
                    for icon_anim, text_anim in zip(icon_anims, text_anims)
                ],
                lag_ratio=0.2
            ),
            run_time=9.91
        )

        ## Section 5
        def build_branch_and_box(start_point, direction_vec, y_travel, color, label_text):
            p1 = start_point
            p2 = p1 + direction_vec * 0.8
            p3 = p2 + (direction_vec * 0.4) + (UP * y_travel)
            p4 = p3 + direction_vec * 1.2

            l1 = Line(p1, p2, color=color, stroke_width=5)
            l2 = Line(p2, p3, color=color, stroke_width=5)
            l3 = Line(p3, p4, color=color, stroke_width=5)
            branch_group = VGroup(l1, l2, l3)

            box = Rectangle(
                width=2.5,
                height=0.8,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )
            box.next_to(p4, direction_vec, buff=0)

            lbl = Paragraph(
                *textwrap.wrap(label_text, width=18),
                font_size=18,
                line_spacing=0.6,
                color=SECONDARY_TEXT_COLOR
            )
            lbl.move_to(box.get_center())

            grow_edge = RIGHT if direction_vec[0] < 0 else LEFT

            return {
                "branch": branch_group,
                "box": box,
                "label": lbl,
                "grow_edge": grow_edge,
                "segments": [l1, l2, l3]
            }

        le_top, le_bot = bar_1.get_corner(UL), bar_1.get_corner(DL)
        re_top, re_bot = bar_1.get_corner(UR), bar_1.get_corner(DR)
        
        l_starts_1 = [interpolate(le_top, le_bot, t) for t in [0.3, 0.7]]
        r_starts_1 = [interpolate(re_top, re_bot, t) for t in [0.3, 0.7]]

        le_top_3, le_bot_3 = bar_3.get_corner(UL), bar_3.get_corner(DL)
        re_top_3, re_bot_3 = bar_3.get_corner(UR), bar_3.get_corner(DR)
        
        l_starts_3 = [interpolate(le_top_3, le_bot_3, t) for t in [0.3, 0.7]]
        r_starts_3 = [interpolate(re_top_3, re_bot_3, t) for t in [0.3, 0.7]]

        ncd_labels = ["Lifestyle (Diabetes)", "Diet (Cancer)", "Heredity (Asthma)", "Environmental Factors"]
        comm_labels = ["Pathogens (Typhoid)", "Person-to-Person (Flu)", "Direct Contact (Chickenpox)", "Droplet Spread (COVID-19)"]

        # 2 on Left, 2 on Right for each definition
        levels_config = [
            # NCDs Left
            [(l_starts_1[0], LEFT, 0.8, PRIMARY_SHAPE_ACCENT, ncd_labels[0]), (l_starts_1[1], LEFT, -0.6, PRIMARY_SHAPE_ACCENT, ncd_labels[1])],
            # NCDs Right
            [(r_starts_1[0], RIGHT, 0.8, PRIMARY_SHAPE_ACCENT, ncd_labels[2]), (r_starts_1[1], RIGHT, -0.6, PRIMARY_SHAPE_ACCENT, ncd_labels[3])],
            # Comm Left
            [(l_starts_3[0], LEFT, 0.6, SECONDARY_SHAPE_ACCENT, comm_labels[0]), (l_starts_3[1], LEFT, -0.8, SECONDARY_SHAPE_ACCENT, comm_labels[1])],
            # Comm Right
            [(r_starts_3[0], RIGHT, 0.6, SECONDARY_SHAPE_ACCENT, comm_labels[2]), (r_starts_3[1], RIGHT, -0.8, SECONDARY_SHAPE_ACCENT, comm_labels[3])]
        ]

        all_levels_data = []

        for config_pair in levels_config:
            current_level_objects = []
            for conf in config_pair:
                current_level_objects.append(build_branch_and_box(*conf))
            all_levels_data.append(current_level_objects)

        branch_anims = [Create(d['branch']) for level in all_levels_data for d in level]

        self.play(LaggedStart(*branch_anims, lag_ratio=0.15), run_time=11.84)

        ## Section 6
        box_anims = []
        for level_objects in all_levels_data:
            for d in level_objects:
                box_anims.append(GrowFromEdge(d['box'], d['grow_edge']))

        self.play(LaggedStart(*box_anims, lag_ratio=0.15), run_time=5.8)

        label_anims = []
        for level_objects in all_levels_data:
            for d in level_objects:
                label_anims.append(Write(d['label']))

        self.play(LaggedStart(*label_anims, lag_ratio=0.15), run_time=5.8)

        self.wait(0.1)

        ## Section 7
        all_cleanup_anims = []

        for level_objects in reversed(all_levels_data):
            all_cleanup_anims += [Unwrite(d['label']) for d in level_objects]
            all_cleanup_anims += [
                d['box']
                .animate(remover=True)
                .stretch_to_fit_width(0, about_edge=d['grow_edge'])
                for d in level_objects
            ]
            for i in [2, 1, 0]:
                all_cleanup_anims += [Uncreate(d['segments'][i]) for d in level_objects]

        self.play(LaggedStart(*all_cleanup_anims, lag_ratio=0.05), run_time=3.62)

        self.play(
            Unwrite(t_3), Unwrite(t_1),
            FadeOut(icon_3), FadeOut(icon_1),
            run_time=1.62
        )

        self.play(
            LaggedStart(
                Transform(bar_1, bar_1.copy().stretch_to_fit_width(0.01)),
                Transform(bar_3, bar_3.copy().stretch_to_fit_width(0.01)),
                lag_ratio=0.2
            ),
            run_time=1.12
        )

        self.remove(bar_1, bar_3)

        self.play(
            Unwrite(subtitle),
            FadeOut(pole),
            Unwrite(title),
            run_time=1.6
        )

        self.wait(0.62)
