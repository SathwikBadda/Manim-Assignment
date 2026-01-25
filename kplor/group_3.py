from manim import *

import random

import numpy as np

from math import pi, sin, cos

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # Deterministic color definitions
        FONT_COLOR_1 = ManimColor("#000000")
        FONT_COLOR_2 = ManimColor("#9AA4B2")
        FONT_COLOR_3 = ManimColor("#B96606")
        ACCENT_COLOR_1 = ManimColor("#00ADEE")
        ACCENT_COLOR_2 = ManimColor("#F8CF0A")
        HIGHLIGHT_COLOR = ManimColor("#B96606")

        ## Section 1
        title = Text(
            "Real-World Applications – Branching Specialization Tree",
            font_size=32,
            color=ManimColor("#1a1a2e"),
            weight=BOLD
        ).to_edge(UP, buff=0.5)
        title.set_width(0.65 * self.camera.frame_width)
        
        self.play(Write(title), run_time=4)
        self.wait(10.15)
        
        ## Section 2
        root_box = RoundedRectangle(
            width=0.25 * self.camera.frame_width,
            height=0.1 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#2980B9"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(DOWN * 3.5)
        
        root_shadow = RoundedRectangle(
            width=0.26 * self.camera.frame_width,
            height=0.105 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#1a5276"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(DOWN * 3.5 + DOWN * 0.05 + LEFT * 0.05)
        root_shadow.set_z_index(0)
        
        root_text = Text(
            "ANALYTICS IN ACTION",
            font_size=24,
            color=WHITE,
            weight=BOLD
        ).move_to(root_box.get_center())
        
        compass_circle_outer = Circle(
            radius=0.15,
            fill_opacity=0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(root_box.get_center() + RIGHT * 0.8)
        
        compass_circle_inner = Circle(
            radius=0.05,
            fill_opacity=0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=1.5
        ).move_to(root_box.get_center() + RIGHT * 0.8)
        
        compass_line_v = Line(
            root_box.get_center() + RIGHT * 0.8 + UP * 0.15,
            root_box.get_center() + RIGHT * 0.8 + DOWN * 0.15,
            color=ManimColor("#3498DB"),
            stroke_width=1.5
        )
        
        compass_line_h = Line(
            root_box.get_center() + RIGHT * 0.8 + LEFT * 0.15,
            root_box.get_center() + RIGHT * 0.8 + RIGHT * 0.15,
            color=ManimColor("#3498DB"),
            stroke_width=1.5
        )
        
        root_group = VGroup(
            root_shadow,
            root_box,
            root_text,
            compass_circle_outer,
            compass_circle_inner,
            compass_line_v,
            compass_line_h
        )
        
        self.play(FadeIn(root_group), run_time=0.6)
        self.wait(1.0)
        
        pulse_animations = []
        for i in range(11):
            scale_factor = 1.01 + 0.01 * np.sin(i * np.pi / 5)
            pulse_animations.append(
                root_group.animate.scale(scale_factor)
            )
        
        self.play(Succession(*pulse_animations), run_time=13.47)
        
        ## Section 3
        vertical_line = Line(
            root_box.get_top(),
            root_box.get_top() + UP * (0.2 * self.camera.frame_height),
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        self.play(Create(vertical_line), run_time=0.8)
        
        left_branch_end = root_box.get_top() + UP * (0.2 * self.camera.frame_height) + LEFT * (0.2 * self.camera.frame_width)
        right_branch_end = root_box.get_top() + UP * (0.2 * self.camera.frame_height) + RIGHT * (0.2 * self.camera.frame_width)
        
        left_branch = CubicBezier(
            root_box.get_top() + UP * (0.2 * self.camera.frame_height),
            root_box.get_top() + UP * (0.25 * self.camera.frame_height) + LEFT * (0.1 * self.camera.frame_width),
            root_box.get_top() + UP * (0.15 * self.camera.frame_height) + LEFT * (0.15 * self.camera.frame_width),
            left_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        right_branch = CubicBezier(
            root_box.get_top() + UP * (0.2 * self.camera.frame_height),
            root_box.get_top() + UP * (0.25 * self.camera.frame_height) + RIGHT * (0.1 * self.camera.frame_width),
            root_box.get_top() + UP * (0.15 * self.camera.frame_height) + RIGHT * (0.15 * self.camera.frame_width),
            right_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        self.play(
            Create(left_branch),
            Create(right_branch),
            run_time=0.8
        )
        
        left_secondary_box = RoundedRectangle(
            width=0.18 * self.camera.frame_width,
            height=0.08 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#5DADE2"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(left_branch_end)
        
        left_secondary_shadow = RoundedRectangle(
            width=0.185 * self.camera.frame_width,
            height=0.085 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#1a5276"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(left_branch_end + DOWN * 0.05 + LEFT * 0.05)
        left_secondary_shadow.set_z_index(0)
        
        left_secondary_text = Text(
            "Marketing & Customer\nAnalytics",
            font_size=18,
            color=WHITE,
            weight=BOLD
        ).move_to(left_secondary_box.get_center())
        
        left_secondary_group = VGroup(
            left_secondary_shadow,
            left_secondary_box,
            left_secondary_text
        )
        
        right_secondary_box = RoundedRectangle(
            width=0.18 * self.camera.frame_width,
            height=0.08 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#AF7AC5"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(right_branch_end)
        
        right_secondary_shadow = RoundedRectangle(
            width=0.185 * self.camera.frame_width,
            height=0.085 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#4a235a"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(right_branch_end + DOWN * 0.05 + RIGHT * 0.05)
        right_secondary_shadow.set_z_index(0)
        
        right_secondary_text = Text(
            "Finance & Operations\nAnalytics",
            font_size=18,
            color=WHITE,
            weight=BOLD
        ).move_to(right_secondary_box.get_center())
        
        right_secondary_group = VGroup(
            right_secondary_shadow,
            right_secondary_box,
            right_secondary_text
        )
        
        self.play(
            FadeIn(left_secondary_group),
            FadeIn(right_secondary_group),
            run_time=0.4
        )
        
        self.wait(15.59)
        
        ## Section 4
        left_upper_branch_end = left_branch_end + UP * (0.15 * self.camera.frame_height) + LEFT * (0.15 * self.camera.frame_width)
        left_lower_branch_end = left_branch_end + DOWN * (0.05 * self.camera.frame_height) + LEFT * (0.1 * self.camera.frame_width)
        
        left_upper_branch = CubicBezier(
            left_secondary_box.get_top(),
            left_secondary_box.get_top() + UP * (0.08 * self.camera.frame_height) + LEFT * (0.08 * self.camera.frame_width),
            left_secondary_box.get_top() + UP * (0.1 * self.camera.frame_height) + LEFT * (0.12 * self.camera.frame_width),
            left_upper_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        left_lower_branch = CubicBezier(
            left_secondary_box.get_top(),
            left_secondary_box.get_top() + UP * (0.04 * self.camera.frame_height) + LEFT * (0.06 * self.camera.frame_width),
            left_secondary_box.get_top() + DOWN * (0.02 * self.camera.frame_height) + LEFT * (0.08 * self.camera.frame_width),
            left_lower_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        right_upper_branch_end = right_branch_end + UP * (0.15 * self.camera.frame_height) + RIGHT * (0.15 * self.camera.frame_width)
        right_lower_branch_end = right_branch_end + DOWN * (0.05 * self.camera.frame_height) + RIGHT * (0.1 * self.camera.frame_width)
        
        right_upper_branch = CubicBezier(
            right_secondary_box.get_top(),
            right_secondary_box.get_top() + UP * (0.08 * self.camera.frame_height) + RIGHT * (0.08 * self.camera.frame_width),
            right_secondary_box.get_top() + UP * (0.1 * self.camera.frame_height) + RIGHT * (0.12 * self.camera.frame_width),
            right_upper_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        right_lower_branch = CubicBezier(
            right_secondary_box.get_top(),
            right_secondary_box.get_top() + UP * (0.04 * self.camera.frame_height) + RIGHT * (0.06 * self.camera.frame_width),
            right_secondary_box.get_top() + DOWN * (0.02 * self.camera.frame_height) + RIGHT * (0.08 * self.camera.frame_width),
            right_lower_branch_end,
            color=ManimColor("#8E44AD"),
            stroke_width=2,
            stroke_opacity=0.4
        )
        
        self.play(
            Create(left_upper_branch),
            Create(left_lower_branch),
            Create(right_upper_branch),
            Create(right_lower_branch),
            run_time=1.585
        )
        
        left_upper_tertiary_box = RoundedRectangle(
            width=0.16 * self.camera.frame_width,
            height=0.07 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#A9CCE3"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(left_upper_branch_end)
        
        left_upper_tertiary_shadow = RoundedRectangle(
            width=0.165 * self.camera.frame_width,
            height=0.075 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#1a5276"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(left_upper_branch_end + DOWN * 0.05 + LEFT * 0.05)
        left_upper_tertiary_shadow.set_z_index(0)
        
        left_upper_tertiary_text = Text(
            "Customer\nSegmentation",
            font_size=16,
            color=ManimColor("#1a1a2e"),
            weight=BOLD
        ).move_to(left_upper_tertiary_box.get_center())
        
        left_upper_tertiary_group = VGroup(
            left_upper_tertiary_shadow,
            left_upper_tertiary_box,
            left_upper_tertiary_text
        )
        
        left_lower_tertiary_box = RoundedRectangle(
            width=0.16 * self.camera.frame_width,
            height=0.07 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#A9CCE3"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(left_lower_branch_end)
        
        left_lower_tertiary_shadow = RoundedRectangle(
            width=0.165 * self.camera.frame_width,
            height=0.075 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#1a5276"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(left_lower_branch_end + DOWN * 0.05 + LEFT * 0.05)
        left_lower_tertiary_shadow.set_z_index(0)
        
        left_lower_tertiary_text = Text(
            "Demand\nForecasting",
            font_size=16,
            color=ManimColor("#1a1a2e"),
            weight=BOLD
        ).move_to(left_lower_tertiary_box.get_center())
        
        left_lower_tertiary_group = VGroup(
            left_lower_tertiary_shadow,
            left_lower_tertiary_box,
            left_lower_tertiary_text
        )
        
        right_upper_tertiary_box = RoundedRectangle(
            width=0.16 * self.camera.frame_width,
            height=0.07 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#D7BDE2"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(right_upper_branch_end)
        
        right_upper_tertiary_shadow = RoundedRectangle(
            width=0.165 * self.camera.frame_width,
            height=0.075 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#4a235a"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(right_upper_branch_end + DOWN * 0.05 + RIGHT * 0.05)
        right_upper_tertiary_shadow.set_z_index(0)
        
        right_upper_tertiary_text = Text(
            "Risk\nAssessment",
            font_size=16,
            color=ManimColor("#1a1a2e"),
            weight=BOLD
        ).move_to(right_upper_tertiary_box.get_center())
        
        right_upper_tertiary_group = VGroup(
            right_upper_tertiary_shadow,
            right_upper_tertiary_box,
            right_upper_tertiary_text
        )
        
        right_lower_tertiary_box = RoundedRectangle(
            width=0.16 * self.camera.frame_width,
            height=0.07 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#D7BDE2"),
            fill_opacity=1.0,
            stroke_color=ManimColor("#3498DB"),
            stroke_width=2
        ).move_to(right_lower_branch_end)
        
        right_lower_tertiary_shadow = RoundedRectangle(
            width=0.165 * self.camera.frame_width,
            height=0.075 * self.camera.frame_height,
            corner_radius=0.1,
            fill_color=ManimColor("#4a235a"),
            fill_opacity=0.35,
            stroke_width=0
        ).move_to(right_lower_branch_end + DOWN * 0.05 + RIGHT * 0.05)
        right_lower_tertiary_shadow.set_z_index(0)
        
        right_lower_tertiary_text = Text(
            "Supply Chain\nOptimization",
            font_size=16,
            color=ManimColor("#1a1a2e"),
            weight=BOLD
        ).move_to(right_lower_tertiary_box.get_center())
        
        right_lower_tertiary_group = VGroup(
            right_lower_tertiary_shadow,
            right_lower_tertiary_box,
            right_lower_tertiary_text
        )
        
        self.play(
            FadeIn(left_upper_tertiary_group),
            FadeIn(left_lower_tertiary_group),
            FadeIn(right_upper_tertiary_group),
            FadeIn(right_lower_tertiary_group),
            run_time=1.185
        )
        
        self.wait(2.285)
        
        retract_left_upper = Succession(
            left_upper_branch.animate.set_opacity(0),
            left_upper_tertiary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        retract_left_lower = Succession(
            left_lower_branch.animate.set_opacity(0),
            left_lower_tertiary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        retract_right_upper = Succession(
            right_upper_branch.animate.set_opacity(0),
            right_upper_tertiary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        retract_right_lower = Succession(
            right_lower_branch.animate.set_opacity(0),
            right_lower_tertiary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        self.play(
            retract_left_upper,
            retract_left_lower,
            retract_right_upper,
            retract_right_lower,
            run_time=1.985
        )
        
        retract_primary_left = Succession(
            left_branch.animate.set_opacity(0),
            left_secondary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        retract_primary_right = Succession(
            right_branch.animate.set_opacity(0),
            right_secondary_group.animate.scale(0.1).set_opacity(0),
            run_time=1.385
        )
        
        self.play(
            retract_primary_left,
            retract_primary_right,
            vertical_line.animate.set_opacity(0),
            run_time=1.985
        )
        
        self.play(
            root_box.animate.set_fill(ManimColor("#5DADE2")),
            run_time=1.585
        )
        
        final_pulse_animations = []
        for i in range(5):
            scale_factor = 1.0 + 0.02 * np.sin(i * np.pi / 2.5)
            final_pulse_animations.append(
                root_group.animate.scale(scale_factor)
            )
        
        self.play(Succession(*final_pulse_animations), run_time=2.295)
