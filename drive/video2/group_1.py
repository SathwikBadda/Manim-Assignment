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
        BODY_SCALE = 0.12
        PARA = 0.08
        EXAMPLE_SCALE = 0.07 # Slightly smaller for 3-col grid
        
        self.camera.background_color = "#0f1715"
        self.camera.frame.set(height=frame_h)
        
        COLOR_BOARD = "#162b20"
        COLOR_FRAME = "#5D4037"
        COLOR_TRAY = "#4E342E"
        COLOR_ROPE = "#A1887F"
        COLOR_PRIMARY_TEXT = "#61D262"
        COLOR_SECONDARY_TEXT = "#FFFFFF"
        COLOR_SECONDARY_ACCENT = "#EF9515"
        
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
        
        duster_img = ImageMobject("../images/ing_words_1.png")
        duster_img.scale_to_fit_height(board_h * 0.08)
        
        chalk_img = ImageMobject("../images/ing_words_2.png")
        chalk_img.scale_to_fit_height(board_h * 0.08)
        
        props_group = Group(duster_img, chalk_img).arrange(RIGHT, buff=0.3).next_to(tray, UP, buff=0.05).shift(RIGHT * 1.5)
        
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
        
        title = Text("Actions Happening Now!", font=font_name, font_size=base_font * TITLE_SCALE, color=COLOR_PRIMARY_TEXT)
        title.set_opacity(0)
        
        body_text = wrap_text_dynamic("We add '-ing' to action words to show that the action is taking place while we are talking about it.", base_font * BODY_SCALE, slate.width * 0.85, COLOR_PRIMARY_TEXT)
        body_text.set_opacity(0)
        
        content = VGroup(title, body_text).arrange(DOWN, buff=0.5).move_to(slate)
        
        system = Group(rope_left, slate, frame, tray, props_group, content)
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
        props_group.add_updater(chalk_slide)
        
        for text_mob in [title, body_text]:
            text_mob.add_updater(flicker)
        
        self.wait(0.33)
        
        ## Section 2
        
        title_chars = [title[i] for i in range(len(title))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in title_chars], lag_ratio=0.1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=2.0
        )
        
        body_chars = [body_text[i] for i in range(len(body_text))]
        self.play(
            LaggedStart(*[c.animate.set_opacity(1) for c in body_chars], lag_ratio=0.08),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=8.54
        )
        
        ## Section 3
        
        # Global alignment: Create unrotated groups first for perfect baselines
        word_1 = Text("cry", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_PRIMARY_TEXT)
        suffix_1 = Text("ing", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT).set_opacity(0)
        word_pair_1 = VGroup(word_1, suffix_1).arrange(RIGHT, buff=0.01, aligned_edge=UP)
        
        word_2_start = Text("dance", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_PRIMARY_TEXT).set_opacity(0)
        
        word_3_root = Text("fly", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_PRIMARY_TEXT).set_opacity(0)
        suffix_3 = Text("ing", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT).set_opacity(0)
        word_pair_3 = VGroup(word_3_root, suffix_3).arrange(RIGHT, buff=0.01, aligned_edge=UP)
        
        # Horizontal arrangement unrotated
        words_group = VGroup(word_pair_1, word_2_start, word_pair_3).arrange(RIGHT, buff=1.0)
        
        # Apply global tilt and move to center
        words_group.rotate(-15 * DEGREES).move_to(slate)
        
        self.add(words_group)
        
        # Word 1 Appears
        word_1.set_opacity(0) # Start hidden for animation
        self.play(
            FadeOut(title),
            FadeOut(body_text),
            word_1.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.2
        )
        title.remove_updater(flicker)
        body_text.remove_updater(flicker)
        
        # Suffix 1 Appears
        self.play(
            suffix_1.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.8
        )
        system.add(word_pair_1)
        
        # Word 2 Appears
        self.play(
            word_2_start.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.2
        )
        
        # Word 2 spelling fix to danc + ing
        word_2_new = Text("danc", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_PRIMARY_TEXT)
        suffix_2 = Text("ing", font=font_name, font_size=base_font * BODY_SCALE, color=COLOR_SECONDARY_ACCENT).set_opacity(0)
        # Precise alignment unrotated - Use UP to avoid descender offset, then nudge to match visually
        word_pair_2 = VGroup(word_2_new, suffix_2).arrange(RIGHT, buff=0.01, aligned_edge=UP)
        suffix_2.shift(DOWN * 0.05) # Nudge to match "danc" baseline perfectly
        word_pair_2.rotate(-15 * DEGREES).move_to(word_2_start)
        
        self.play(
            suffix_2.animate.set_opacity(1),
            ReplacementTransform(word_2_start, word_2_new),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.8
        )
        system.add(word_pair_2)
        
        # Word 3 Appears
        self.play(
            word_3_root.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=1.2
        )
        
        # Suffix 3 Appears
        self.play(
            suffix_3.animate.set_opacity(1),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=0.8
        )
        system.add(word_pair_3)
        
        self.wait(2.71)
        
        ## Section 4
        
        # Permanently remove Title and Body text from system to prevent overlap during exit
        system.remove(content)
        self.remove(content)
        
        # Pre-calculated scaled elements - Remove black backgrounds
        # Note: Do NOT use set_opacity(0) here as it may overwrite the alpha mask during animation
        img_1 = ImageMobject("../images/ing_words_3.png").scale_to_fit_height(board_h * 0.35).rotate(-15 * DEGREES)
        img_1.pixel_array = img_1.pixel_array.copy() # Avoid shared reference issues
        img_2 = ImageMobject("../images/ing_words_4.png").scale_to_fit_height(board_h * 0.35).rotate(-15 * DEGREES)
        img_3 = ImageMobject("../images/ing_words_5.png").scale_to_fit_height(board_h * 0.35).rotate(-15 * DEGREES)
        
        # Manim common trick: make black transparent
        for img in [img_1, img_2, img_3]:
            # Simple thresholding on pixel_array for older Manim versions
            pa = img.pixel_array
            # pa is a numpy array of shape (H, W, 4)
            # Find dark pixels (R+G+B < threshold) - use robust threshold (80)
            mask = np.all(pa[:, :, :3] < 80, axis=2)
            pa[mask, 3] = 0 # Set alpha to 0
            img.pixel_array = pa
        
        # Reduced font size (1.2x base)
        text_1_full = Tex("Baby is crying.", substrings_to_isolate=["crying"], font_size=base_font * EXAMPLE_SCALE * 1.2, color=COLOR_PRIMARY_TEXT).rotate(-15 * DEGREES)
        text_2_full = Tex("I am dancing.", substrings_to_isolate=["dancing"], font_size=base_font * EXAMPLE_SCALE * 1.2, color=COLOR_PRIMARY_TEXT).rotate(-15 * DEGREES)
        text_3_full = Tex("The birds are flying.", substrings_to_isolate=["flying"], font_size=base_font * EXAMPLE_SCALE * 1.2, color=COLOR_PRIMARY_TEXT).rotate(-15 * DEGREES)
        
        for t, s in [(text_1_full, "crying"), (text_2_full, "dancing"), (text_3_full, "flying")]:
            t.get_part_by_tex(s).set_color(COLOR_SECONDARY_ACCENT)
        
        # Grid positions (slanted layout) - Moved towards center
        left_corner = slate.get_center() + LEFT * 3.5 + UP * 0.3
        middle_pos = slate.get_center() + UP * 0.1
        right_corner = slate.get_center() + RIGHT * 3.5 + DOWN * 0.1
        
        # Complete columns (Vertical: Word -> Image -> Sentence)
        # We create temporary ghost columns to get the final positions
        col_1_target = Group(word_pair_1.copy(), img_1.copy().set_opacity(1), text_1_full.copy().set_opacity(1)).arrange(DOWN, buff=0.3).move_to(left_corner)
        col_2_target = Group(word_pair_2.copy(), img_2.copy().set_opacity(1), text_2_full.copy().set_opacity(1)).arrange(DOWN, buff=0.3).move_to(middle_pos)
        col_3_target = Group(word_pair_3.copy(), img_3.copy().set_opacity(1), text_3_full.copy().set_opacity(1)).arrange(DOWN, buff=0.3).move_to(right_corner)
        
        # Apply positions to real objects
        img_1.move_to(col_1_target[1])
        text_1_full.move_to(col_1_target[2])
        img_2.move_to(col_2_target[1])
        text_2_full.move_to(col_2_target[2])
        img_3.move_to(col_3_target[1])
        text_3_full.move_to(col_3_target[2])
        
        # Add others to system
        system.add(img_1, img_2, img_3, text_1_full, text_2_full, text_3_full)
        
        # Step 1: Words move to corners FAST (1.0s)
        self.play(
            word_pair_1.animate.move_to(col_1_target[0]),
            word_pair_2.animate.move_to(col_2_target[0]),
            word_pair_3.animate.move_to(col_3_target[0]),
            run_time=1.0
        )
        
        # Step 2: Content fades in for the remaining 8.96s (Total 9.96s)
        # Use FadeIn for images to PRESERVE the per-pixel alpha mask
        self.play(
            FadeIn(img_1),
            FadeIn(img_2),
            FadeIn(img_3),
            FadeIn(text_1_full),
            FadeIn(text_2_full),
            FadeIn(text_3_full),
            update_during_animation=True,
            suspend_mobject_updating=False,
            run_time=8.96
        )
        
        ## Section 5
        
        self.wait(3.0)
        
        ## Section 6
        
        system.remove_updater(swing_updater)
        self.camera.frame.remove_updater(camera_breathe)
        props_group.remove_updater(chalk_slide)
        
        for text_mob in [title, body_text]:
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
        
        self.play(Uncreate(rope_left), run_time=0.15)
        
        # No need to fade out images anymore, they are in 'system'
        
        self.play(
            system.animate.shift(DOWN * frame_h * 1.5).rotate(10 * DEGREES),
            run_time=3.04,
            rate_func=rate_functions.ease_in_cubic
        )
