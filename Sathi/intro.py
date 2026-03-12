from manim import *
import numpy as np
import random

class AbstractTrajectoriesOfExcellence(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE
        
        run_time = 7.0
        
        start_x = -9.0
        end_x = 9.0
        
        # We scale progress from start_x up to ~6.0 for our curve dynamics
        def y_center(x):
            p = np.clip((x - start_x) / (15.0), 0, 1)
            # Starts around -3.5 (bottom-left), ends around +2.5 (top-right)
            base_y = -3.5 + 6.0 * (p ** 1.1)
            # Wavy trajectory movement (like a road path)
            wave = 0.5 * np.sin(0.9 * x) + 0.1 * np.cos(0.4 * x)
            return base_y + wave
            
        def path_width(x):
            p = np.clip((x - start_x) / (15.0), 0, 1)
            # Path goes from narrow to wide
            return 0.15 + 0.55 * p
            
        def ball_radius(x):
            p = np.clip((x - start_x) / (15.0), 0, 1)
            # Start from very small, end at somewhat less size
            return 0.04 + 0.14 * p

        # 4 parallel bands
        band_offsets = [-1.5, -0.5, 0.5, 1.5]
        col_spacing = 0.35  # Tighter spacing for continuous path, but adjusted by opacities
        speed = 2.5 
        
        # The front of the stream is positioned slightly left of center to begin
        front_x = -5.0
        
        # Ensure we have enough columns to last the entire 7 seconds
        min_x = start_x - speed * run_time - col_spacing * 2
        num_cols = int((front_x - min_x) / col_spacing) + 1
        
        dots = VGroup()
        for col in range(num_cols):
            base_x = front_x - col * col_spacing
            for i, offset_idx in enumerate(band_offsets):
                # Stagger the x position slightly based on the row to look organic
                staggered_x = base_x + (col_spacing * 0.4 if i % 2 != 0 else 0)
                
                dot = Circle(radius=0.1, fill_color=ORANGE, stroke_width=0)
                dot.base_x = staggered_x
                dot.band_offset = offset_idx
                # Varied opacities: mostly solid, with a few lighter ones for depth
                dot.base_opacity = random.choices(
                    [0.15, 0.4, 0.7, 1.0], 
                    weights=[1, 2, 3, 20]
                )[0]
                dots.add(dot)
                
        self.add(dots)
        
        time_tracker = ValueTracker(0)
        
        def master_updater(mob, dt):
            t = time_tracker.get_value()
            fade_in_x = -7.5  # Introduce dots softly at the edge
            
            for dot in mob:
                current_x = dot.base_x + speed * t
                
                # Render logic based on bounds
                if current_x < start_x or current_x > end_x:
                    dot.set_opacity(0)
                else:
                    # Smooth fade in for dots entering from the left edge
                    entrance_fade = np.clip((current_x - start_x) / (fade_in_x - start_x), 0, 1)
                    dot.set_opacity(dot.base_opacity * entrance_fade)
                    
                    # Calculate new metrics strictly mathematically
                    y_c = y_center(current_x)
                    w = path_width(current_x)
                    r = ball_radius(current_x)
                    
                    # Apply
                    current_y = y_c + dot.band_offset * w
                    dot.move_to([current_x, current_y, 0])
                    # Add subtle depth: fainter dots are slightly smaller
                    scale_mult = 1.0 if dot.base_opacity > 0.5 else 0.85
                    dot.scale_to_fit_height(r * 2 * scale_mult)

        dots.add_updater(master_updater)
        
        # Start camera slightly zoomed and panned towards bottom-left
        self.camera.frame.set_width(12)
        self.camera.frame.move_to([-1.0, -1.0, 0])
        
        # Single continuous animation tracking exact 7 seconds run_time
        self.play(
            time_tracker.animate.increment_value(run_time),
            self.camera.frame.animate.set_width(config.frame_width).move_to(ORIGIN),
            run_time=run_time,
            rate_func=linear
        )

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 2: Bouncing Game & Steps (Run Time: ~5.8s)
        # ══════════════════════════════════════════════════════════════════

        # 1. Grab hero ball from the end of the wavy path
        hero_ball = Circle(radius=0.18, fill_color=ORANGE, stroke_width=0, fill_opacity=1)
        hero_ball.move_to([8.0, y_center(8.0) + 1.5 * path_width(8.0), 0])
        self.add(hero_ball)
        
        dots.clear_updaters()
        new_camera_center = UP * 10
        
        # Grade markers perfectly inside the safe frame
        grade_8 = Text("8th Grade", font_size=20, color=GRAY, weight=BOLD)
        grade_8.move_to(new_camera_center + DOWN * 3.4 + LEFT * 5.5)
        
        grade_10 = Text("10th Grade", font_size=20, color=GRAY, weight=BOLD)
        grade_10.move_to(new_camera_center + UP * 3.2 + LEFT * 5.5)
        
        # 2. Setup the steps
        step_names = [
            "Aptitude", 
            "Logical Reasoning", 
            "Verbal Ability", 
            "Personality Insights", 
            "Early Career Awareness"
        ]
        
        steps = VGroup()
        # Evenly spaced steps representing a staircase
        step_positions = [
            new_camera_center + DOWN * 2.50 + LEFT * 3.0,
            new_camera_center + DOWN * 1.25 + LEFT * 1.5,
            new_camera_center + ORIGIN,
            new_camera_center + UP * 1.25 + RIGHT * 1.5,
            new_camera_center + UP * 2.50 + RIGHT * 3.0
        ]
        
        for name, pos in zip(step_names, step_positions):
            text = Text(name, font_size=16, color=DARK_GRAY, weight=BOLD)
            rect = RoundedRectangle(corner_radius=0.2, height=0.5, width=max(2.5, text.width + 0.6), fill_color="#E0E0E0", fill_opacity=1, stroke_color=GRAY, stroke_width=1)
            text.move_to(rect.get_center())
            step = VGroup(rect, text)
            step.move_to(pos)
            steps.add(step)
            
        # Target position to land on the first step
        first_step_rect, first_step_text = steps[0]
        ball_radius = 0.22
        target_pos = steps[0].get_top() + UP * (ball_radius + 0.05)
        
        # 3. Initial Swoop: Camera shifts up as the hero ball leaps from the track to Step 1
        tracker_initial = ValueTracker(0)
        start_pos_initial = hero_ball.get_center()
        
        hero_ball.set_fill(color="#FFB300")
        
        def initial_swoop(mob):
            alpha = tracker_initial.get_value()
            if alpha == 0: return # Prevent flicker frame
            x = np.interp(alpha, [0, 1], [start_pos_initial[0], target_pos[0]])
            # Parabola for gravity bounce (+2.0 peak height modifier from base track)
            y = np.interp(alpha, [0, 1], [start_pos_initial[1], target_pos[1]]) + 2.0 * 4 * alpha * (1 - alpha)
            curr_r = np.interp(alpha, [0, 1], [0.18, 0.22])
            mob.stretch_to_fit_height(curr_r * 2).stretch_to_fit_width(curr_r * 2)
            mob.move_to([x, y, 0])
            
        hero_ball.add_updater(initial_swoop)
        
        self.play(
            self.camera.frame.animate.move_to(new_camera_center),
            tracker_initial.animate.set_value(1),
            FadeIn(steps[0], shift=UP*0.5),
            FadeOut(dots),
            run_time=1.2,
            rate_func=linear
        )
        hero_ball.remove_updater(initial_swoop)
        self.add(grade_8, grade_10)
        
        # Snap to avoid floating point drift
        hero_ball.stretch_to_fit_height(ball_radius * 2).stretch_to_fit_width(ball_radius * 2).move_to(target_pos)

        def bounce_impact(step_idx, target_steps=steps, custom_color="#1D428A"):
            step = target_steps[step_idx]
            rect, text = step
            new_color = custom_color
            
            original_h = ball_radius * 2
            original_w = ball_radius * 2
            squash = 0.15 + (original_h * 0.1)
            
            # Impact
            self.play(
                hero_ball.animate.stretch_to_fit_height(original_h * 0.8).stretch_to_fit_width(original_w * 1.1).shift(DOWN * squash),
                rect.animate.set_fill(new_color, opacity=1).set_stroke(new_color).shift(DOWN * 0.15),
                text.animate.set_color(WHITE).shift(DOWN * 0.15),
                run_time=0.1,
                rate_func=linear
            )
            # Recover
            self.play(
                hero_ball.animate.stretch_to_fit_height(original_h).stretch_to_fit_width(original_w).shift(UP * squash),
                rect.animate.shift(UP * 0.15),
                text.animate.shift(UP * 0.15),
                run_time=0.15,
                rate_func=linear
            )
            
        bounce_impact(0)

        # 4. Ball jumps from step to step (Steps 2 to 5)
        for i in range(1, len(steps)):
            
            # Show the step right before jumping
            self.play(FadeIn(steps[i], shift=UP*0.2), run_time=0.25)
            
            prev_radius = ball_radius
            ball_radius += 0.03 # Size increases for every jump
            target_pos = steps[i].get_top() + UP * (ball_radius + 0.05)
            
            start_pos_iter = hero_ball.get_center()
            tracker_jump = ValueTracker(0)
            
            # Correctly bind iteration values directly to prevent python closure bugs
            def jump_update(mob, t=tracker_jump, s_pos=start_pos_iter, t_pos=target_pos, p_r=prev_radius, c_r=ball_radius):
                alpha = t.get_value()
                x = np.interp(alpha, [0, 1], [s_pos[0], t_pos[0]])
                # True physics parabola instead of circle arc
                y = np.interp(alpha, [0, 1], [s_pos[1], t_pos[1]]) + 1.2 * 4 * alpha * (1 - alpha)
                curr_r = np.interp(alpha, [0, 1], [p_r, c_r])
                
                mob.stretch_to_fit_height(curr_r * 2).stretch_to_fit_width(curr_r * 2)
                mob.move_to([x, y, 0])
                
            hero_ball.add_updater(jump_update)
            # Turn previous step back to gray smoothly as ball jumps
            prev_rect, prev_text = steps[i-1]
            # Animate the tracker to drive the parabolic jump
            self.play(
                tracker_jump.animate.set_value(1), 
                prev_rect.animate.set_style(fill_color="#E0E0E0", fill_opacity=1, stroke_color=GRAY),
                prev_text.animate.set_color(DARK_GRAY),
                run_time=0.45, rate_func=linear
            )
            hero_ball.remove_updater(jump_update)
            
            # Snap to avoid floating point drift
            hero_ball.stretch_to_fit_height(ball_radius * 2).stretch_to_fit_width(ball_radius * 2).move_to(target_pos)
            
            # Execute impact squash and color change
            bounce_impact(i)

        # ══════════════════════════════════════════════════════════════════
        #  PHASE 3: Higher Education Readiness (Run Time: ~8.6s)
        # ══════════════════════════════════════════════════════════════════
        
        new_camera_center_3 = new_camera_center + UP * 5.5
        
        grade_11_12 = Text("11th - 12th Grade", font_size=20, color=GRAY, weight=BOLD)
        grade_11_12.move_to(new_camera_center_3 + UP * 3.2 + LEFT * 5.5)
        
        step_names_3 = [
            "Critical Thinking", 
            "Creativity", 
            "Communication", 
            "Collaboration"
        ]
        
        steps_3 = VGroup()
        # Steps representing a staircase inclined LEFT and UP
        step_positions_3 = [
            new_camera_center_3 + DOWN * 1.5 + RIGHT * 1.0,
            new_camera_center_3 + DOWN * 0.2 + LEFT * 1.0,
            new_camera_center_3 + UP * 1.1 + LEFT * 3.0,
            new_camera_center_3 + UP * 2.4 + LEFT * 1.0 # slight zigzag back towards center
        ]
        
        for name, pos in zip(step_names_3, step_positions_3):
            text = Text(name, font_size=16, color=DARK_GRAY, weight=BOLD)
            rect = RoundedRectangle(corner_radius=0.2, height=0.5, width=max(2.5, text.width + 0.6), fill_color="#E0E0E0", fill_opacity=1, stroke_color=GRAY, stroke_width=1)
            text.move_to(rect.get_center())
            step = VGroup(rect, text)
            step.move_to(pos)
            steps_3.add(step)
            
        target_pos_3 = steps_3[0].get_top() + UP * (ball_radius + 0.05)
        start_pos_3 = hero_ball.get_center()
        tracker_initial_3 = ValueTracker(0)
        
        def initial_swoop_3(mob):
            alpha = tracker_initial_3.get_value()
            if alpha == 0: return
            x = np.interp(alpha, [0, 1], [start_pos_3[0], target_pos_3[0]])
            # Parabola for gravity bounce (+1.5 peak height modifier)
            y = np.interp(alpha, [0, 1], [start_pos_3[1], target_pos_3[1]]) + 1.5 * 4 * alpha * (1 - alpha)
            curr_r = np.interp(alpha, [0, 1], [ball_radius, ball_radius + 0.03])
            mob.stretch_to_fit_height(curr_r * 2).stretch_to_fit_width(curr_r * 2)
            mob.move_to([x, y, 0])
            
        hero_ball.add_updater(initial_swoop_3)
        
        self.play(
            self.camera.frame.animate.move_to(new_camera_center_3),
            tracker_initial_3.animate.set_value(1),
            FadeIn(steps_3[0], shift=UP*0.5),
            FadeIn(grade_11_12),
            grade_10.animate.move_to(new_camera_center_3 + DOWN * 3.4 + LEFT * 5.5),
            steps[-1][0].animate.set_style(fill_color="#E0E0E0", fill_opacity=1, stroke_color=GRAY),
            steps[-1][1].animate.set_color(DARK_GRAY),
            run_time=1.5,
            rate_func=linear
        )
        hero_ball.remove_updater(initial_swoop_3)
        
        ball_radius += 0.03
        hero_ball.stretch_to_fit_height(ball_radius * 2).stretch_to_fit_width(ball_radius * 2).move_to(target_pos_3)
        
        bounce_impact(0, target_steps=steps_3)
        
        # Jumps for Phase 3 (Steps 2 to 4)
        for i in range(1, len(steps_3)):
            self.play(FadeIn(steps_3[i], shift=UP*0.2), run_time=0.25)
            
            prev_radius = ball_radius
            ball_radius += 0.03 # Size increases for every jump
            target_pos = steps_3[i].get_top() + UP * (ball_radius + 0.05)
            
            start_pos_iter = hero_ball.get_center()
            tracker_jump = ValueTracker(0)
            
            def jump_update_3(mob, t=tracker_jump, s_pos=start_pos_iter, t_pos=target_pos, p_r=prev_radius, c_r=ball_radius):
                alpha = t.get_value()
                x = np.interp(alpha, [0, 1], [s_pos[0], t_pos[0]])
                y = np.interp(alpha, [0, 1], [s_pos[1], t_pos[1]]) + 1.2 * 4 * alpha * (1 - alpha)
                curr_r = np.interp(alpha, [0, 1], [p_r, c_r])
                mob.stretch_to_fit_height(curr_r * 2).stretch_to_fit_width(curr_r * 2)
                mob.move_to([x, y, 0])
                
            hero_ball.add_updater(jump_update_3)
            
            # Revert the previous step to gray
            prev_rect, prev_text = steps_3[i-1]
            self.play(
                tracker_jump.animate.set_value(1), 
                prev_rect.animate.set_style(fill_color="#E0E0E0", fill_opacity=1, stroke_color=GRAY),
                prev_text.animate.set_color(DARK_GRAY),
                run_time=0.45, rate_func=linear
            )
            hero_ball.remove_updater(jump_update_3)
            
            hero_ball.stretch_to_fit_height(ball_radius * 2).stretch_to_fit_width(ball_radius * 2).move_to(target_pos)
            bounce_impact(i, target_steps=steps_3)