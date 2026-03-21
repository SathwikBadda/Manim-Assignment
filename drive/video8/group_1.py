from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        frame_w = config.frame_width
        frame_h = config.frame_height
        
        board_w = frame_w * 0.7
        board_h = frame_h * 0.6
        
        rope_length = board_h * 0.35
        initial_drop_distance = frame_h * 1.2
        
        base_font = board_h * 60

        TITLE_SCALE = 0.14
        BODY_SCALE = 0.085
        PARA_SCALE = 0.06
        EXAMPLE_SCALE = 0.20
        stroke_dynamic = board_w * 0.025

        self.camera.background_color = "#0f1715"
        self.camera.frame.set(height=frame_h)

        COLOR_BOARD = "#162b20"
        COLOR_FRAME = "#5D4037"
        COLOR_TRAY = "#4E342E"
        COLOR_ROPE = "#A1887F"
        COLOR_PRIMARY_TEXT = "#61D262"
        COLOR_SECONDARY_TEXT = "#FFFFFF"
        COLOR_SECONDARY_ACCENT = "#EF9515"
        COLOR_PRIMARY_ACCENT = "#4280A7"
        COLOR_MATH = "#FFFDD0"
        
        SWING_MAX_ANGLE = 6.0 * DEGREES
        SWING_SPEED = 2.0
        DAMPING_FACTOR = 0.15

        slate = Rectangle(width=board_w, height=board_h, color=COLOR_BOARD, fill_opacity=1).set_stroke(width=0)
        frame = Rectangle(width=board_w + 0.4, height=board_h + 0.4, color=COLOR_FRAME).set_fill(opacity=0).set_stroke(width=12)
        tray = Rectangle(width=board_w + 0.4, height=0.3, color=COLOR_TRAY, fill_opacity=1).next_to(frame, DOWN, buff=0)
        
        left_anchor = frame.get_corner(UL) + RIGHT * 0.4
        ceiling_left = left_anchor + UP * rope_length
        rope_left = Line(ceiling_left, left_anchor, color=COLOR_ROPE, stroke_width=4)
        
        right_anchor = frame.get_corner(UR) + LEFT * 0.4
        ceiling_right = right_anchor + UP * rope_length
        rope_right = Line(ceiling_right, right_anchor, color=COLOR_ROPE, stroke_width=4)

        duster = VGroup(
            RoundedRectangle(corner_radius=0.05, width=1.0, height=0.12, color="#3E2723", fill_opacity=1),
            RoundedRectangle(corner_radius=0.05, width=1.0, height=0.18, color="#8D6E63", fill_opacity=1)
        ).arrange(UP, buff=0)
        
        chalk_width = board_w * 0.07
        chalk_height = board_h * 0.015
        chalk = Rectangle(width=chalk_width, height=chalk_height, color="#FFFFFF", fill_opacity=1).set_stroke(width=0)
        props_group = VGroup(duster, chalk).arrange(RIGHT, buff=0.4).next_to(tray, UP, buff=0.05).shift(RIGHT * 1.5)

        font_name = "Chalktastic"

        def wrap_text_dynamic(text_string, font_size, max_width, color="#FFFFFF"):
            words = text_string.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_text = Text(" ".join(current_line), font=font_name, font_size=font_size)
                if test_text.width > max_width and len(current_line) > 1:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            
            return Text(
                "\n".join(lines),
                font=font_name,
                font_size=font_size,
                color=color,
                line_spacing=1.4
            )

        wrap_text_to_width = wrap_text_dynamic

        title = Text("Divisibility Rules: Quick Checks!", font=font_name, font_size=base_font * TITLE_SCALE, color=COLOR_PRIMARY_TEXT)
        body_text_1 = wrap_text_to_width("Seeing if one number can be divided by another perfectly, without any leftovers!", base_font * BODY_SCALE, slate.width * 0.85, COLOR_SECONDARY_TEXT)
        
        content = VGroup(title, body_text_1).arrange(DOWN, buff=0.5).move_to(slate).shift(UP * 0.8)
        title.set_opacity(0)
        body_text_1.set_opacity(0)
        
        rule_2_text = Text("If the last digit is 0, 2, 4, 6, or 8, it's divisible by 2.", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT)
        rule_2_text.set_opacity(0)
        
        ex_24 = Text("24", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_24.set_opacity(0)
        
        ex_437 = Text("437", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_437.set_opacity(0)
        
        rule_5_text = Text("If the last digit is 0 or 5, it's divisible by 5.", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT)
        rule_5_text.set_opacity(0)
        
        ex_1670 = Text("1670", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_1670.set_opacity(0)
        
        ex_2342 = Text("2342", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_2342.set_opacity(0)
        
        rule_10_text = Text("If the last digit is 0, it's divisible by 10.", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT)
        rule_10_text.set_opacity(0)
        
        ex_390 = Text("390", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_390.set_opacity(0)
        
        ex_4585 = Text("4585", font=font_name, font_size=base_font * EXAMPLE_SCALE, color=COLOR_SECONDARY_TEXT)
        ex_4585.set_opacity(0)
        
        ex_24[-1].set_color(COLOR_SECONDARY_ACCENT)
        ex_437[-1].set_color(COLOR_SECONDARY_ACCENT)
        ex_1670[-1].set_color(COLOR_SECONDARY_ACCENT)
        ex_2342[-1].set_color(COLOR_SECONDARY_ACCENT)
        ex_390[-1].set_color(COLOR_SECONDARY_ACCENT)
        ex_4585[-1].set_color(COLOR_SECONDARY_ACCENT)
        
        def create_tick():
            return Text("✓", font=font_name, font_size=base_font * EXAMPLE_SCALE * 0.65, color=GREEN)

        def create_cross():
            return Text("✗", font=font_name, font_size=base_font * EXAMPLE_SCALE * 0.65, color=RED)

        system = VGroup(rope_left, slate, frame, tray, duster, chalk, content, rule_2_text, ex_24, ex_437, rule_5_text, ex_1670, ex_2342, rule_10_text, ex_390, ex_4585)

        pivot = ceiling_left

        full_assembly = VGroup(system, rope_right)
        full_assembly.shift(UP * initial_drop_distance)
        
        self.add(full_assembly)

        system.swing_time = 0
        system.last_angle = 0

        def swing_updater(mob, dt):
            mob.swing_time += dt
            decay = np.exp(-DAMPING_FACTOR * mob.swing_time)
            oscillation = np.cos(SWING_SPEED * mob.swing_time)
            
            target_angle = -1 * decay * SWING_MAX_ANGLE * oscillation
            
            change = target_angle - mob.last_angle
            
            mob.rotate(change, about_point=pivot)
            
            mob.last_angle = target_angle

        def flicker(mob, dt):
            direction = LEFT if np.random.random() < 0.5 else RIGHT
            mob.shift(direction * np.random.uniform(0.001, 0.002))

        self.camera.frame_time = 0
        
        def camera_breathe(frame, dt):
            self.camera.frame_time += dt
            
            scale_factor = 1 + 0.0003 * np.sin(self.camera.frame_time * 0.8)
            frame.set_height(frame_h * scale_factor)
            
            target_center = system.get_center()
            current_center = frame.get_center()
            new_center = current_center + (target_center - current_center) * 2 * dt
            frame.move_to(new_center)

        def chalk_slide(mob, dt):
            current_angle = system.last_angle
            slide_sensitivity = 1.5
            mob.shift(LEFT * current_angle * slide_sensitivity * dt)

        ## Section 1

        self.play(
            full_assembly.animate.shift(DOWN * initial_drop_distance),
            run_time=2.0,
            rate_func=rate_functions.ease_out_bounce
        )
        
        r_start = rope_right.get_start()
        r_end = rope_right.get_end()
        jagged_points = [r_start]
        
        for t in np.linspace(0.1, 0.9, 8):
            base_point = r_start + (r_end - r_start) * t
            noise_dir = [LEFT, RIGHT][np.random.randint(0, 2)]
            noise = noise_dir * 0.15
            jagged_points.append(base_point + noise)
        jagged_points.append(r_end)
        
        snap_line = VMobject().set_points_as_corners(jagged_points)
        snap_line.set_color(COLOR_ROPE).set_stroke(width=3)
        
        self.remove(rope_right)
        self.add(snap_line)
        self.play(Uncreate(snap_line), run_time=0.15)

        first_swing_target = -SWING_MAX_ANGLE
        
        self.play(
            Rotate(system, angle=first_swing_target, about_point=pivot),
            run_time=0.5,
            rate_func=rate_functions.ease_in_out_sine
        )

        system.last_angle = first_swing_target
        
        system.add_updater(swing_updater)
        self.camera.frame.add_updater(camera_breathe)
        chalk.add_updater(chalk_slide)
        
        for text_mob in [title, body_text_1, rule_2_text, ex_24, ex_437, rule_5_text, ex_1670, ex_2342, rule_10_text, ex_390, ex_4585]:
            text_mob.add_updater(flicker)

        self.wait(1.12)

        ## Section 2

        title_chars = [title[i] for i in range(len(title))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in title_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.5
        )

        body_text_1_chars = [body_text_1[i] for i in range(len(body_text_1))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in body_text_1_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=11.1
        )

        ## Section 3

        rule_2_text.move_to(body_text_1.get_center())
        
        rule_2_chars = [rule_2_text[i] for i in range(len(rule_2_text))]
        self.play(
            body_text_1.animate.set_opacity(0),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.5
        )
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in rule_2_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=3.0
        )

        ex_24.next_to(rule_2_text, DOWN, buff=0.3).shift(LEFT * 2.5)
        ex_437.next_to(rule_2_text, DOWN, buff=0.3).shift(RIGHT * 2.5)
        
        ex_24_chars = [ex_24[i] for i in range(len(ex_24))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_24_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.0
        )

        self.play(
            ex_24.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.4
        )
        tick_24 = create_tick().next_to(ex_24, RIGHT, buff=0.4); tick_24.add_updater(flicker); system.add(tick_24)
        self.play(
            Create(tick_24),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.4
        )

        ex_437_chars = [ex_437[i] for i in range(len(ex_437))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_437_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.0
        )

        self.play(
            ex_437.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.4
        )
        cross_437 = create_cross().next_to(ex_437, RIGHT, buff=0.4); cross_437.add_updater(flicker); system.add(cross_437)
        self.play(
            Create(cross_437),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.4
        )

        self.wait(11.38)

        ## Section 4

        rule_5_text.move_to(body_text_1.get_center())
        
        rule_5_chars = [rule_5_text[i] for i in range(len(rule_5_text))]
        self.play(
            rule_2_text.animate.set_opacity(0),
            ex_24.animate.set_opacity(0),
            ex_437.animate.set_opacity(0),
            tick_24.animate.set_opacity(0),
            cross_437.animate.set_opacity(0),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.5
        )
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in rule_5_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.3
        )

        ex_1670.next_to(rule_5_text, DOWN, buff=0.3).shift(LEFT * 2.5)
        ex_2342.next_to(rule_5_text, DOWN, buff=0.3).shift(RIGHT * 2.5)
        
        ex_1670_chars = [ex_1670[i] for i in range(len(ex_1670))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_1670_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.8
        )

        self.play(
            ex_1670.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.35
        )
        tick_1670 = create_tick().next_to(ex_1670, RIGHT, buff=0.4); tick_1670.add_updater(flicker); system.add(tick_1670)
        self.play(
            Create(tick_1670),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.35
        )

        ex_2342_chars = [ex_2342[i] for i in range(len(ex_2342))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_2342_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.8
        )

        self.play(
            ex_2342.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.35
        )
        cross_2342 = create_cross().next_to(ex_2342, RIGHT, buff=0.4); cross_2342.add_updater(flicker); system.add(cross_2342)
        self.play(
            Create(cross_2342),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.35
        )

        self.wait(8.04)

        ## Section 5

        rule_10_text.move_to(body_text_1.get_center())
        
        rule_10_chars = [rule_10_text[i] for i in range(len(rule_10_text))]
        self.play(
            rule_5_text.animate.set_opacity(0),
            ex_1670.animate.set_opacity(0),
            ex_2342.animate.set_opacity(0),
            tick_1670.animate.set_opacity(0),
            cross_2342.animate.set_opacity(0),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.5
        )
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in rule_10_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.9
        )

        ex_390.next_to(rule_10_text, DOWN, buff=0.3).shift(LEFT * 2.5)
        ex_4585.next_to(rule_10_text, DOWN, buff=0.3).shift(RIGHT * 2.5)
        
        ex_390_chars = [ex_390[i] for i in range(len(ex_390))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_390_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.6
        )

        self.play(
            ex_390.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.325
        )
        tick_390 = create_tick().next_to(ex_390, RIGHT, buff=0.4); tick_390.add_updater(flicker); system.add(tick_390)
        self.play(
            Create(tick_390),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.325
        )

        ex_4585_chars = [ex_4585[i] for i in range(len(ex_4585))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in ex_4585_chars], lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.6
        )

        self.play(
            ex_4585.animate.scale(1.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.325
        )
        cross_4585 = create_cross().next_to(ex_4585, RIGHT, buff=0.4); cross_4585.add_updater(flicker); system.add(cross_4585)
        self.play(
            Create(cross_4585),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.325
        )

        self.wait(6.33)

        ## Section 6

        system.remove_updater(swing_updater)
        self.camera.frame.remove_updater(camera_breathe)
        chalk.remove_updater(chalk_slide)
        
        for text_mob in [title, body_text_1, rule_2_text, ex_24, ex_437, rule_5_text, ex_1670, ex_2342, rule_10_text, ex_390, ex_4585]:
            text_mob.remove_updater(flicker)

        l_start = rope_left.get_start()
        l_end = rope_left.get_end()
        jagged_points_left = [l_start]
        
        for t in np.linspace(0.1, 0.9, 8):
            base_point = l_start + (l_end - l_start) * t
            noise_dir = [LEFT, RIGHT][np.random.randint(0, 2)]
            noise = noise_dir * 0.15
            jagged_points_left.append(base_point + noise)
        jagged_points_left.append(l_end)
        
        snap_line_left = VMobject().set_points_as_corners(jagged_points_left)
        snap_line_left.set_color(COLOR_ROPE).set_stroke(width=3)
        
        self.play(Transform(rope_left, snap_line_left), run_time=0.15)
        self.remove(rope_left)

        fade_animations = [
            FadeOut(title, shift=DOWN*0.2),
            FadeOut(body_text_1, shift=DOWN*0.2),
            FadeOut(rule_2_text, shift=DOWN*0.2),
            FadeOut(ex_24, shift=DOWN*0.2),
            FadeOut(ex_437, shift=DOWN*0.2),
            FadeOut(rule_5_text, shift=DOWN*0.2),
            FadeOut(ex_1670, shift=DOWN*0.2),
            FadeOut(ex_2342, shift=DOWN*0.2),
            FadeOut(rule_10_text, shift=DOWN*0.2),
            FadeOut(ex_390, shift=DOWN*0.2),
            FadeOut(ex_4585, shift=DOWN*0.2),
            FadeOut(tick_24, shift=DOWN*0.2),
            FadeOut(cross_437, shift=DOWN*0.2),
            FadeOut(tick_1670, shift=DOWN*0.2),
            FadeOut(cross_2342, shift=DOWN*0.2),
            FadeOut(tick_390, shift=DOWN*0.2),
            FadeOut(cross_4585, shift=DOWN*0.2)
        ]
        
        self.play(
            *fade_animations,
            update_during_animation=True,
            run_time=0.475        )

        self.play(
            system.animate.shift(DOWN * frame_h * 1.5).rotate(10 * DEGREES),
            run_time=2.525,
            rate_func=rate_functions.ease_in_cubic
        )
