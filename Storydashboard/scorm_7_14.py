from manim import *
import numpy as np

class BeakerFill(ThreeDScene):
    def create_beaker(self, bw, bh, bx, by, stroke_w, stroke_col, corner_r):
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
        return beaker_outline, entry_line, left_lip, entry_start

    def construct(self):
        self.camera.background_color = ManimColor("#F8F9FB")

        # ── INITIAL TEXT ───────────────────────────────────────────
        # Scale everything slightly larger to start, then we'll reverse zoom
        self.set_camera_orientation(zoom=1/0.85)
        
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

        beaker_outline, entry_line, left_lip, entry_start = self.create_beaker(bw, bh, bx, by, stroke_w, stroke_col, corner_r)

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
        self.move_camera(
            zoom=1.0,
            added_anims=[
                Create(beaker_outline, lag_ratio=1, run_time=2.2, rate_func=smooth),
                Succession(
                    Wait(0.6),
                    entry_tail_tracker.animate.set_value(left_lip[0]).set_run_time(1.4).set_rate_func(smooth)
                )
            ],
            run_time=2.2
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
        dropped_texts = VGroup()
        beaker_outline.set_z_index(50)

        # 1. COURSE
        text1 = Text("COURSE", font_size=56, color=ManimColor("#1a1a2e"), weight=BOLD)
        text1.move_to([bx, by + bh / 2 + 2.2, 0])
        text1.scale(0.85)
        text1.rotate(15 * DEGREES)
        text1.set_z_index(20)
        text1.set_opacity(0)
        self.add(text1)
        dropped_texts.add(text1)

        target_surface = [bx, liquid_top_y, 0]
        target_bottom1 = [bx, liquid_bot_y + 0.35, 0]

        self.play(
            text1.animate.set_opacity(1).move_to(target_surface).scale(1.0/0.85),
            FadeOut(input_text),
            run_time=0.6,
            rate_func=rush_into
        )
        self.play(
            text1.animate.move_to(target_bottom1).rotate(-15 * DEGREES).set_color(WHITE),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(text1.animate.shift(UP * 0.1), run_time=0.15, rate_func=rate_functions.ease_out_elastic)
        self.play(text1.animate.shift(DOWN * 0.1), run_time=0.15, rate_func=smooth)

        # 2. LLM
        text2 = Text("LLM", font_size=56, color=ManimColor("#1a1a2e"), weight=BOLD)
        text2.move_to([bx, by + bh / 2 + 2.2, 0])
        text2.scale(0.85)
        text2.rotate(-15 * DEGREES)
        text2.set_z_index(21)
        text2.set_opacity(0)
        self.add(text2)
        dropped_texts.add(text2)

        target_bottom2 = [bx, liquid_bot_y + 0.35 + 0.7, 0]

        self.play(
            text2.animate.set_opacity(1).move_to(target_surface).scale(1.0/0.85),
            run_time=0.6,
            rate_func=rush_into
        )
        self.play(
            text2.animate.move_to(target_bottom2).rotate(15 * DEGREES).set_color(WHITE),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(text2.animate.shift(UP * 0.1), run_time=0.15, rate_func=rate_functions.ease_out_elastic)
        self.play(text2.animate.shift(DOWN * 0.1), run_time=0.15, rate_func=smooth)

        # 3. TOOL
        text3 = Text("TOOL", font_size=56, color=ManimColor("#1a1a2e"), weight=BOLD)
        text3.move_to([bx, by + bh / 2 + 2.2, 0])
        text3.scale(0.85)
        text3.rotate(15 * DEGREES)
        text3.set_z_index(22)
        text3.set_opacity(0)
        self.add(text3)
        dropped_texts.add(text3)

        target_bottom3 = [bx, liquid_bot_y + 0.35 + 1.4, 0]

        self.play(
            text3.animate.set_opacity(1).move_to(target_surface).scale(1.0/0.85),
            run_time=0.6,
            rate_func=rush_into
        )
        self.play(
            text3.animate.move_to(target_bottom3).rotate(-15 * DEGREES).set_color(WHITE),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic
        )
        self.play(text3.animate.shift(UP * 0.1), run_time=0.15, rate_func=rate_functions.ease_out_elastic)
        self.play(text3.animate.shift(DOWN * 0.1), run_time=0.15, rate_func=smooth)

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

if __name__ == "__main__":
    config.processes = 4  # Use 4 CPU cores
    config.max_files_cached = 200  # Helps with memory management
    config.progress_bar = "none"
    config.enable_cuda = True
    config.disable_caching = True
    #config.background_color = "#ffffff"
    config.pixel_height = 360
    config.pixel_width = 640
    config.frame_rate = 15
    #config.pixel_height = 180
    #config.pixel_width = 320
    #config.frame_rate = 10
    from pathlib import Path
    import shutil

    scene_to_render = BeakerFill()
    scene_to_render.render()

    file_dir = Path(r"../../../gold_pattern_test_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "scorm_7_14.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")