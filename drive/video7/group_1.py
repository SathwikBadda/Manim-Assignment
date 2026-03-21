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
        
        base_font = board_h * 120

        TITLE_SCALE = 0.14
        BODY_SCALE = 0.085
        PARA_SCALE = 0.06
        stroke_dynamic = board_w * 0.025

        self.camera.background_color = "#0f1715"
        self.camera.frame.set(height=frame_h)

        COLOR_BOARD = "#162b20"
        COLOR_FRAME = "#5D4037"
        COLOR_TRAY = "#4E342E"
        COLOR_ROPE = "#A1887F"
        COLOR_TITLE = "#F0F0F0"
        COLOR_BODY = "#E0E0E0"
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

        font_name = "chalkastic"

        def wrap_text_to_width(text_string, font_size, max_width, color):
            words = text_string.split()
            lines = []
            current = ""
            max_width_unscaled = max_width * 2
            for word in words:
                test = current + " " + word if current else word
                t = Text(test, font=font_name, font_size=font_size, color=color)
                if t.width <= max_width_unscaled:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)
            return Text(
                "\n".join(lines),
                font=font_name,
                font_size=font_size,
                color=color,
                line_spacing=1.4
            ).scale(0.5)

        title = Text("Estimating the Product", font=font_name, font_size=base_font * TITLE_SCALE, color=COLOR_TITLE, slant=NORMAL, weight=NORMAL).scale(0.5)
        
        body_text = "To estimate the product, we first round off the numbers being multiplied"
        body = wrap_text_to_width(body_text, base_font * BODY_SCALE, slate.width * 0.85, COLOR_BODY)
        
        para_text = "Round the multiplier and multiplicand to the nearest tens, hundreds, or thousands, depending on the number of digits"
        para = wrap_text_to_width(para_text, base_font * PARA_SCALE, slate.width * 0.85, COLOR_BODY)
        
        def1_text = "The symbol '≈' means 'approximately equal to'"
        def1 = wrap_text_to_width(def1_text, base_font * PARA_SCALE, slate.width * 0.85, COLOR_BODY)
        
        def2_text = "The symbol '=' means 'equal to' or 'actual value'"
        def2 = wrap_text_to_width(def2_text, base_font * PARA_SCALE, slate.width * 0.85, COLOR_BODY)
        
        content = VGroup(title, body, para, def1, def2).arrange(DOWN, buff=0.35)
        content.move_to(slate.get_center() + UP * 0.25)
        content.set_opacity(0)

        system = Group(rope_left, slate, frame, tray, duster, chalk, content)
        pivot = ceiling_left
        full_assembly = Group(system, rope_right)
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
            run_time=2.5,
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
        self.play(Uncreate(snap_line), run_time=0.1)

        first_swing_target = -SWING_MAX_ANGLE
        
        self.play(
            Rotate(system, angle=first_swing_target, about_point=pivot),
            run_time=1.08,
            rate_func=rate_functions.ease_in_out_sine
        )

        system.last_angle = first_swing_target
        
        system.add_updater(swing_updater)
        self.camera.frame.add_updater(camera_breathe)
        chalk.add_updater(chalk_slide)
        
        for text_mob in [title, body, para, def1, def2]:
            text_mob.add_updater(flicker)


        ## Section 2
        self.play(
            UpdateFromAlphaFunc(title, lambda m, alpha: m.set_opacity(alpha)),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=11.23
        )

        ## Section 3
        body_chars = list(body)
        animations_body = [UpdateFromAlphaFunc(c, lambda m, alpha: m.set_opacity(alpha)) for c in body_chars]
        self.play(
            LaggedStart(*animations_body, lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=10.32
        )

        ## Section 4
        para_chars = list(para)
        animations_para = [UpdateFromAlphaFunc(c, lambda m, alpha: m.set_opacity(alpha)) for c in para_chars]
        self.play(
            LaggedStart(*animations_para, lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=15.45
        )

        ## Section 5
        def1_chars = list(def1)
        animations_def1 = [UpdateFromAlphaFunc(c, lambda m, alpha: m.set_opacity(alpha)) for c in def1_chars]
        self.play(
            LaggedStart(*animations_def1, lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=9.11
        )

        def2_chars = list(def2)
        animations_def2 = [UpdateFromAlphaFunc(c, lambda m, alpha: m.set_opacity(alpha)) for c in def2_chars]
        self.play(
            LaggedStart(*animations_def2, lag_ratio=0.15),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=9.11
        )

        ## Section 6
        system.remove_updater(swing_updater)
        self.camera.frame.remove_updater(camera_breathe)
        chalk.remove_updater(chalk_slide)
        
        for text_mob in [title, body, para, def1, def2]:
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
        
        self.play(Transform(rope_left, snap_line_left), run_time=1.0)
        self.play(Uncreate(rope_left), run_time=0.5)
        system.remove(rope_left)

        self.play(
            system.animate.shift(DOWN * frame_h * 1.5).rotate(10*DEGREES),
            run_time=2.63,
            rate_func=rate_functions.ease_in_cubic
        )
