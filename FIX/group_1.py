from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

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
        stroke_dynamic = board_w * 0.025

        self.camera.background_color = "#0f1715"
        self.camera.frame.set(height=frame_h)

        COLOR_BOARD = "#162b20"
        COLOR_FRAME = "#5D4037"
        COLOR_TRAY = "#4E342E"
        COLOR_ROPE = "#A1887F"
        COLOR_TITLE = "#61D262"
        COLOR_BODY = "#FFFFFF"
        COLOR_MATH = "#61D262"
        COLOR_BOX = "#4280A7"
        
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

        font_name = "Chalkduster"

        def wrap_text_to_width(text_string, font_size, max_width, color):
            words = text_string.split()
            lines = []
            current = ""
            for word in words:
                test = current + " " + word if current else word
                t = Text(test, font=font_name, font_size=font_size, color=color)
                if t.width <= max_width:
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
            )

        import os

        title = wrap_text_to_width("Meet the Metre!", base_font * TITLE_SCALE, slate.width * 0.85, COLOR_TITLE)
        body = wrap_text_to_width("For measuring longer things, we use the Metre.", base_font * BODY_SCALE, slate.width * 0.85, COLOR_BODY)
        para = wrap_text_to_width("Like the length of your classroom wall or a tall tree!", base_font * PARA_SCALE, slate.width * 0.45, COLOR_BODY)

        eq_tex = Tex(
            "1 \\text{ Metre} = 100 \\text{ Centimetres}",
            color=COLOR_BODY,
            font_size=base_font * 0.1
        )
        
        box_eq = SurroundingRectangle(eq_tex, color=COLOR_BOX, buff=0.25, stroke_width=2)
        eq_whole = VGroup(eq_tex, box_eq)

        content = VGroup(title, body, para, eq_whole).arrange(DOWN, buff=0.5)
        
        para.shift(LEFT * 1.5)
        eq_whole.shift(LEFT * 2.0 + DOWN * 0.1)

        image_path = os.path.join(os.path.dirname(__file__), "..", "images", "tree.png")
        tree_img = ImageMobject(image_path)
        
        # Create a smaller square paper
        paper_size = board_h * 0.38
        
        paper = Rectangle(
            width=paper_size, 
            height=paper_size, 
            color="#FCFCF9", 
            fill_opacity=1
        ).set_stroke(width=1, color="#D0D0D0")
        
        # Scale tree image to fill the paper completely (accounting for transparent padding in PNG)
        tree_img.scale_to_fit_height(paper_size * 1.15)
        paper_group = Group(paper, tree_img)
        paper_group.next_to(para, RIGHT, buff=1.0)
        paper_group.align_to(para, direction=UP)
        paper_group.shift(UP * 0.5)
        paper_group.rotate(-3 * DEGREES)
        
        cover = Rectangle(
            width=paper.width + 0.2,
            height=paper.height + 0.2,
            color=COLOR_BOARD,
            fill_opacity=1
        ).set_stroke(width=0)
        cover.move_to(paper_group)
        cover.rotate(-3 * DEGREES)
        paper_group.add(cover)
        
        content.set_opacity(0)

        system = Group(rope_left, slate, frame, tray, duster, chalk, content, paper_group)
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

        def chalk_dust(point):
            dot_count = int(board_w * 3)
            dots = VGroup(*[
                Dot(point + np.random.uniform(-0.2, 0.2, 3), radius=0.03, color=COLOR_MATH)
                for _ in range(dot_count)
            ])
            dots.set_opacity(0.6)
            return AnimationGroup(
                LaggedStart(
                    *[GrowFromCenter(dot) for dot in dots],
                    lag_ratio=0.02
                ),
                dots.animate.shift(UP * 0.3 + RIGHT * 0.1).set_opacity(0),
                run_time=0.8
            )

        ## Section 1
        self.play(
            full_assembly.animate.shift(DOWN * initial_drop_distance),
            run_time=2.5,
            rate_func=rate_functions.ease_out_bounce
        )
        self.wait(2.32)

        ## Section 2
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
        self.play(Uncreate(snap_line), run_time=1.5)
        self.wait(3.32)

        ## Section 3
        first_swing_target = -SWING_MAX_ANGLE
        self.play(
            Rotate(system, angle=first_swing_target, about_point=pivot),
            run_time=1.9,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        system.last_angle = first_swing_target
        system.add_updater(swing_updater)
        self.camera.frame.add_updater(camera_breathe)
        chalk.add_updater(chalk_slide)
        
        for text_mob in [title, body, para]:
            text_mob.add_updater(flicker)
        
        eq_tex.add_updater(flicker)
        
        self.wait(2.5)

        ## Section 4
        title_chars = [title[i] for i in range(len(title))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in title_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.0
        )

        self.wait(1.5)
        
        body_chars = [body[i] for i in range(len(body))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in body_chars], lag_ratio=0.08),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.0
        )

        self.wait(1.5)
        
        para_chars = [para[i] for i in range(len(para))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in para_chars], lag_ratio=0.05),
            cover.animate.set_opacity(0),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.0
        )

        self.wait(6.0)
        
        eq_chars = [eq_tex[i] for i in range(len(eq_tex))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in eq_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.5
        )

        self.wait(3.0)
        
        self.play(
            box_eq.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=3.5
        )

        ## Section 5
        self.wait(4.0)

        ## Section 6
        self.wait(4.0)
        system.remove_updater(swing_updater)
        self.camera.frame.remove_updater(camera_breathe)
        chalk.remove_updater(chalk_slide)
        
        for text_mob in [title, body, para]:
            text_mob.remove_updater(flicker)
        
        eq_tex.remove_updater(flicker)

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
        
        #system.remove(rope_left)
        self.play(Transform(rope_left, snap_line_left), run_time=0.5)
        #self.add(snap_line_left)
        self.play(Uncreate(rope_left), run_time=0.5)
        system.remove(rope_left)

        self.play(
            system.animate.shift(DOWN * frame_h * 1.5).rotate(10*DEGREES),
            run_time=4.0,
            rate_func=rate_functions.ease_in_cubic
        )
        
        
