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
        EXAMPLE_SCALE = 0.05
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

        title = Text("Understanding 'Are'", font=font_name, font_size=base_font * TITLE_SCALE, color=COLOR_PRIMARY_TEXT)
        body_text_1 = wrap_text_to_width("'Are' is used with anything that is plural. It is used with:", base_font * BODY_SCALE, slate.width * 0.85, COLOR_SECONDARY_ACCENT)
        list_items = VGroup(
            Text("'we'", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT),
            Text("'these'", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT),
            Text("'you'", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT),
            Text("'they'", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT),
            Text("'names (more than one)'", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        body = VGroup(body_text_1, list_items).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        content = VGroup(title, body).arrange(DOWN, buff=0.5).move_to(slate)
        title.set_opacity(0)
        body.set_opacity(0)
        
        para_text = "The rules of 'are' apply when referring to multiple people or things, or when using specific pronouns."
        para = wrap_text_to_width(para_text, base_font * PARA_SCALE, slate.width * 0.9, COLOR_SECONDARY_TEXT)
        para.next_to(title, DOWN, buff=0.5)
        para.set_opacity(0)

        paper_size = board_h * 0.38
        paper = Rectangle(
            width=paper_size,
            height=paper_size,
            color="#FCFCF9",
            fill_opacity=1
        ).set_stroke(width=1, color="#D0D0D0")
        
        img_9 = ImageMobject("../images/verbs_9.png")
        img_9.scale_to_fit_height(paper_size * 0.9)
        
        paper_group = Group(paper, img_9)
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

        paper_group.next_to(para, DOWN, buff=0.3)
        paper_group.set_opacity(0)
        

        system = Group(rope_left, slate, frame, tray, duster, chalk, content, para, paper_group)

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
        
        for text_mob in [title, body, para]:
            text_mob.add_updater(flicker)

        self.wait(0.49)

        ## Section 2
        title_chars = [title[i] for i in range(len(title))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in title_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.0
        )

        body_0_chars = [body[0][i] for i in range(len(body[0]))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in body_0_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.0
        )

        body_1_chars = [body[1][i] for i in range(len(body[1]))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in body_1_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.5
        )

        self.wait(7.6)

        ## Section 3
        
        self.play(
            Uncreate(body),
            update_during_animation=True, suspend_mobject_updating=False, run_time=1.0
        )

        para_chars = [para[i] for i in range(len(para))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in para_chars], lag_ratio=0.1),
            paper_group.animate.set_opacity(1),
            cover.animate.set_opacity(0),
            update_during_animation=True, suspend_mobject_updating=False, run_time=1.3
        )

        self.wait(3.0)    

        self.play(
            paper_group.animate.set_opacity(0),
            cover.animate.set_opacity(1),
            Uncreate(para),
            update_during_animation=True, suspend_mobject_updating=False, run_time=1.2
        )

        ## Section 4

        # ------------------------------------------------
        # EXAMPLES (DYNAMIC TEMPLATE POSITIONS)
        # ------------------------------------------------
        
        example_data_list = [
            {"text": "We are sisters", "path": "../images/verbs_10.png"},
            {"text": "These are cats", "path": "../images/verbs_11.png"},
            {"text": "You are a good cook", "path": "../images/verbs_12.png"},
            {"text": "They are going to a party", "path": "../images/verbs_13.png"},
            {"text": "The birds are flying", "path": "../images/verbs_14.png"}
        ]
        
        gallery_elements = Group()
        
        for item in example_data_list:
            ex_text = wrap_text_dynamic(item["text"], base_font * EXAMPLE_SCALE, board_w / 3 - 0.5, color=COLOR_SECONDARY_TEXT)
            ex_text.set_opacity(0)
            img = ImageMobject(item["path"]).scale_to_fit_height(board_h * 0.25)
            # Center text over image
            container = Group(ex_text, img).arrange(DOWN, buff=0.1)
            gallery_elements.add(container)
            
        # Dynamically arrange based on number of items (wrap to next row if more than 3)
        cols = 3 if len(gallery_elements) >= 3 else len(gallery_elements)
        gallery_elements.arrange_in_grid(cols=cols, buff=(1.0, 0.4))
        
        # Position dynamically below the title
        gallery_elements.next_to(title, DOWN, buff=0.3)
        
        # Auto-scale to ensure it doesn't overlap or go out of bounds
        max_board_width = board_w * 0.9
        max_board_height = board_h * 0.7
        
        if gallery_elements.height > max_board_height:
            gallery_elements.scale_to_fit_height(max_board_height)
        if gallery_elements.width > max_board_width:
            gallery_elements.scale_to_fit_width(max_board_width)
            
        # Dynamic rendering
        for el in gallery_elements:
            el_text = el[0]
            el_img = el[1]
            chars = list(el_text)
            
            self.play(
                LaggedStart(*[c.animate.set_opacity(1) for c in chars], lag_ratio=0.1) if chars else Wait(0.1),
                GrowFromCenter(el_img),
                update_during_animation=True,
                suspend_mobject_updating=False,
                run_time=1.8
            )
            self.play(
                Wiggle(el_text),
                update_during_animation=True,
                suspend_mobject_updating=False,
                run_time=0.4
            )

        self.wait(2.31)

        ## Section 5

        system.remove_updater(swing_updater)
        self.camera.frame.remove_updater(camera_breathe)
        chalk.remove_updater(chalk_slide)
        
        for text_mob in [title, body, para]:
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
        
        self.play(Transform(rope_left, snap_line_left), run_time=0.3)
        fade_out_animations = [Uncreate(rope_left)]
        for el in gallery_elements:
            fade_out_animations.append(ShrinkToCenter(el[1]))
            fade_out_animations.append(FadeOut(el[0], shift=DOWN*0.2))
            
        self.play(
            *fade_out_animations,
            update_during_animation=True,
            run_time=0.3
        )
        system.remove(rope_left)

        self.play(
            system.animate.shift(DOWN * frame_h * 1.5).rotate(10 * DEGREES),
            run_time=9.25,
            rate_func=rate_functions.ease_in_cubic
        )
