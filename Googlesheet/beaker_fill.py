from manim import *
import numpy as np

class BeakerFill(MovingCameraScene):
    def construct(self):
        self.camera.background_color = ManimColor("#F8F9FB")

        # ── INITIAL TEXT ───────────────────────────────────────────
        # Scale everything slightly larger to start, then we'll reverse zoom
        self.camera.frame.scale(0.85)
        
        input_text = Text("eLearning", font_size=72, color=ManimColor("#1a1a2e"), weight=BOLD)
        input_text.move_to(ORIGIN)
        input_text.set_opacity(0)
        self.add(input_text)

        self.play(input_text.animate.set_opacity(1), run_time=0.8, rate_func=smooth)
        self.wait(0.5)

        # ── BEAKER GEOMETRY (Single Snaking Line from Left) ───────────
        bw = 5.0   # inner width
        bh = 3.8   # inner height
        bx = 0.0   # center x
        by = -0.3  # center y
        stroke_w = 3.5
        stroke_col = ManimColor("#222244")
        corner_r = 0.35

        # Precise snaking coordinates from left edge 
        entry_start = [-14.0, by + bh / 2 + 0.38, 0]
        left_lip = [bx - bw / 2 - 0.30, by + bh / 2 + 0.38, 0]
        left_top = [bx - bw / 2 - 0.05, by + bh / 2, 0]
        left_bot_corner_start = [bx - bw / 2 - 0.05, by - bh / 2 + corner_r, 0]
        left_bot_corner_end = [bx - bw / 2, by - bh / 2, 0]
        right_bot_corner_start = [bx + bw / 2, by - bh / 2, 0]
        right_bot_corner_end = [bx + bw / 2 + 0.05, by - bh / 2 + corner_r, 0]
        right_top = [bx + bw / 2 + 0.05, by + bh / 2, 0]
        right_lip = [bx + bw / 2 + 0.30, by + bh / 2 + 0.38, 0]

        entry_line = Line(entry_start, left_lip, stroke_color=stroke_col, stroke_width=stroke_w)
        left_flare = ArcBetweenPoints(left_lip, left_top, angle=-PI/3, stroke_color=stroke_col, stroke_width=stroke_w)
        left_side = Line(left_top, left_bot_corner_start, stroke_color=stroke_col, stroke_width=stroke_w)
        left_arc = ArcBetweenPoints(left_bot_corner_start, left_bot_corner_end, angle=PI/2.5, stroke_color=stroke_col, stroke_width=stroke_w)
        bottom_bar = Line(left_bot_corner_end, right_bot_corner_start, stroke_color=stroke_col, stroke_width=stroke_w)
        right_arc = ArcBetweenPoints(right_bot_corner_start, right_bot_corner_end, angle=PI/2.5, stroke_color=stroke_col, stroke_width=stroke_w)
        right_side = Line(right_bot_corner_end, right_top, stroke_color=stroke_col, stroke_width=stroke_w)
        right_flare = ArcBetweenPoints(right_top, right_lip, angle=-PI/3, stroke_color=stroke_col, stroke_width=stroke_w)

        beaker_outline = VGroup(
            entry_line, left_flare, left_side, left_arc, 
            bottom_bar, right_arc, right_side, right_flare
        )

        # ── PHASE 1: Zoom out & Draw Snaking line simultaneously ──────
        # Animate the tail of the line catching up and vanishing into the lip
        entry_tail_tracker = ValueTracker(entry_start[0])
        def update_entry_line(mob):
            start_x = entry_tail_tracker.get_value()
            if start_x >= left_lip[0] - 0.01:
                mob.set_opacity(0)
            else:
                mob.put_start_and_end_on([start_x, left_lip[1], 0], left_lip)
                
        entry_line.add_updater(update_entry_line)

        # We start the zoom out perfectly synced with the line coming in
        self.play(
            Create(beaker_outline, lag_ratio=1, run_time=2.2, rate_func=smooth),
            self.camera.frame.animate.scale(1.0 / 0.85).set_run_time(2.2),
            Succession(
                Wait(0.6),
                entry_tail_tracker.animate.set_value(left_lip[0]).set_run_time(1.4).set_rate_func(smooth)
            )
        )
        
        entry_line.remove_updater(update_entry_line)
        self.remove(entry_line)
        beaker_outline.remove(entry_line)
        self.wait(0.3)

        # ── PHASE 2: Dynamic Liquid Fill ─────────────────────────────
        liquid_color = ManimColor("#1565E0")
        liquid_top_y = by + bh / 2 - 0.15
        liquid_bot_y = by - bh / 2 + 0.08
        
        liquid_level = ValueTracker(liquid_bot_y)

        def get_wave_poly():
            y_level = liquid_level.get_value()
            if y_level <= liquid_bot_y + 0.01:
                return Rectangle(width=bw-0.12, height=0.01).move_to([bx, liquid_bot_y, 0]).set_color(liquid_color).set_opacity(0)
            
            pts = []
            n_pts = 60
            width = bw - 0.12
            amplitude = 0.07 
            n_waves = 4
            phase = self.renderer.time * 2 # Continuous rippling
            
            for k in range(n_pts + 1):
                t = k / n_pts
                x = bx - width / 2 + t * width
                y = y_level + amplitude * np.sin(t * n_waves * 2 * PI - phase)
                pts.append([x, y, 0])
            
            pts.append([bx + width / 2, liquid_bot_y, 0])
            pts.append([bx - width / 2, liquid_bot_y, 0])
            return Polygon(*pts, fill_color=liquid_color, fill_opacity=1, stroke_width=0)

        # Water will stay cleanly rendered through always_redraw, solving the disappearing bug
        wave_liquid = always_redraw(get_wave_poly)
        
        # We explicitly layer the text above the liquid before it turns white
        self.remove(input_text, beaker_outline)
        self.add(wave_liquid, beaker_outline, input_text)

        self.play(
            liquid_level.animate.set_value(liquid_top_y),
            run_time=2.2, rate_func=smooth,
        )

        # Initial text submerses to white
        self.play(
            input_text.animate.set_color(WHITE),
            run_time=0.4, rate_func=smooth,
        )
        self.wait(0.4)

        # ── PHASE 3: Drop Tilted Texts (COURSE, LLM, TOOL) ───────────────
        words = ["COURSE", "LLM", "TOOL"]
        dropped_texts = VGroup()
        
        # We need a small pop up impact animation for each drop, but only on the first do we fade eLearning
        for i, word in enumerate(words):
            # Reduced font size slightly to fit nicely without overlapping edges
            drop_text = Text(word, font_size=56, color=ManimColor("#1a1a2e"), weight=BOLD)
            # Start high above
            drop_text.move_to([bx, by + bh / 2 + 2.2, 0])
            drop_text.scale(0.85)
            # Alternate the initial tilt
            tilt_angle = 15 * DEGREES if i % 2 == 0 else -15 * DEGREES
            drop_text.rotate(tilt_angle)
            drop_text.set_z_index(20 + i) # Ensure later drops are on top
            drop_text.set_opacity(0)
            self.add(drop_text)
            
            # Reveal text natively natively
            self.play(drop_text.animate.set_opacity(1), run_time=0.4, rate_func=smooth)
            
            # The physics:
            # 1. Fast drop to water surface
            # 2. Slow drag to the bottom, slowly leveling out to horizontal
            water_surface_y = liquid_top_y
            
            # Adjust final stacking heights
            # COURSE will be at the bottom, LLM resting on it, TOOL resting on top
            # Base of beaker is liquid_bot_y. Give some padding. Add less offset since texts are smaller
            final_target_y = liquid_bot_y + 0.35 + i * 0.7
            
            drop_target_surface = [bx, water_surface_y, 0]
            drop_target_bottom = [bx, final_target_y, 0]
            
            # Animation 1: Rush to surface
            # For the first drop, fade out 'eLearning'
            if i == 0:
                self.play(
                    drop_text.animate.move_to(drop_target_surface).scale(1.0 / 0.85),
                    FadeOut(input_text, run_time=0.2), 
                    run_time=0.4,
                    rate_func=rush_into,
                )
            else:
                self.play(
                    drop_text.animate.move_to(drop_target_surface).scale(1.0 / 0.85),
                    run_time=0.4,
                    rate_func=rush_into,
                )
                
            # Animation 2: Water drag (slowed down descent, rotating back to horizontal 0)
            # Reverse the tilt angle to reach 0
            # Increased run_time to make floating slower
            self.play(
                drop_text.animate
                    .move_to(drop_target_bottom)
                    .rotate(-tilt_angle) # Level out flat horizontally
                    .set_color(WHITE),
                run_time=1.6,
                rate_func=rate_functions.ease_out_cubic # The "drag" float down
            )
            
            # Slight impact pop at the bottom
            self.play(
                drop_text.animate.shift(UP * 0.1),
                run_time=0.15, rate_func=rate_functions.ease_out_elastic,
            )
            self.play(
                drop_text.animate.shift(DOWN * 0.1),
                run_time=0.2, rate_func=smooth,
            )
            
            # Re-layer so it's perfectly in the beaker
            self.remove(drop_text, beaker_outline)
            self.add(drop_text, beaker_outline)
            
            dropped_texts.add(drop_text)
            self.wait(0.2)
            
        self.wait(0.5)
        
        # ── PHASE 4: Remove Beaker / Pan Camera ─────────────────────────
        # Animate the beaker, water going DOWN out of frame
        # Keep the texts, shifting them UP slightly to center them and returning them to their dark color
        
        # Stop the water always_redraw so we can organically shift it away
        wave_liquid.clear_updaters()
        
        self.play(
            beaker_outline.animate.shift(DOWN * 6),
            wave_liquid.animate.shift(DOWN * 6),
            dropped_texts.animate.shift(UP * 1.5).scale(1.2).set_color(ManimColor("#1a1a2e")), 
            run_time=1.3,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        self.wait(1.5)
