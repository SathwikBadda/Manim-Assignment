from manim import *
import numpy as np
import os

class AcceleratedOrbit(ThreeDScene):
    def construct(self):
        self.camera.background_color = ManimColor("#F8F9FB")
        
        radius_x_tracker = ValueTracker(5.2)
        radius_y_tracker = ValueTracker(2.4)
        orbit_scale_tracker = ValueTracker(4.0) # Start way outside frame
        
        # ── Central logo (Modern "S/X" geometric shapes) ─────────
        p1 = Polygon(
            [-0.75,  0.75, 0], [ 0.75,  0.75, 0],
            [ 0.75,  0.20, 0], [-0.15,  0.20, 0],
            fill_color=ManimColor("#5CA3FF"), fill_opacity=1, stroke_width=0,
        )
        p2 = Polygon(
            [-0.75, -0.75, 0], [ 0.75, -0.75, 0],
            [ 0.75, -0.20, 0], [ 0.15, -0.20, 0],
            fill_color=ManimColor("#436BFF"), fill_opacity=1, stroke_width=0,
        )
        cross_h = Rectangle(width=1.5, height=0.3,
                            fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cross_v = Rectangle(width=0.3, height=1.5,
                            fill_color=WHITE, fill_opacity=1, stroke_width=0)
        logo = VGroup(p1, p2, cross_h, cross_v)
        logo.move_to(ORIGIN)
        logo.set_opacity(0)
        logo.scale(0.8)
        logo.set_z_index(0) 
        self.add(logo)
        
        # ── Orbit icon builder ────────────────────────────────────
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "images")
        
        img_names = [
            "google_sheets.png",
            "gmail.png",
            "google_drive.png",
            "google_docs.png",
            "google_slides.png",
            "google_calendar.png",
            "google_meet.png",
            "youtube.png"
        ]
        
        n_icons = len(img_names)
        base_angles = [PI/2 + 2*PI*i/n_icons for i in range(n_icons)]
        
        orbit_icons = []
        for i, img_name in enumerate(img_names):
            img_path = os.path.join(images_dir, img_name)
            icon_img = ImageMobject(img_path)
            icon_img.height = 0.85 # Ensure natively right size so no massive icon flash
            icon_img.move_to(ORIGIN)
            node = Group(icon_img)
            orbit_icons.append(node)
            
        all_icons = Group(*orbit_icons)
        self.add(all_icons)
        
        # Trackers for animation flow
        t_start = [0.0]
        base_h = 0.85 
        ROTATION_SPEED = 2.0 # Strict constant speed
        entrance_tracker = ValueTracker(0.0) 
        
        # ── Node Dynamics Updater (Scale, Depth Blur, & Z-Sorting) ───
        def make_icon_updater(node, base_angle):
            def updater(mob, dt):
                t = self.renderer.time - t_start[0]
                # Angle strictly increases linearly
                angle = base_angle + t * ROTATION_SPEED
                
                rx = radius_x_tracker.get_value()
                ry = radius_y_tracker.get_value()
                scale_mult = orbit_scale_tracker.get_value()
                
                # Apply expansion to explicitly explode bounds out of frame
                eff_rx = rx * scale_mult
                eff_ry = ry * scale_mult
                
                x = eff_rx * np.cos(angle)
                y = eff_ry * np.sin(angle)
                mob.move_to(np.array([x, y, 0]))
                
                # Use unscaled radius to gauge isometric depth properly 
                unscaled_y = ry * np.sin(angle)
                tilt_ratio = ry / rx if rx > 0 else 1
                tilt_factor = np.clip((1.0 - tilt_ratio) / (1.0 - 2.4/5.2), 0, 1)
                depth_frac = (unscaled_y + ry) / (2 * ry) if ry > 0 else 0
                
                target_scale = 1.0 + (0.1 - 0.65 * depth_frac) * tilt_factor
                mob.height = base_h * target_scale 
                mob.width = base_h * target_scale
                
                # Set dynamic layer so closer objects physically pop over far ones
                mob.set_z_index(-unscaled_y)
                
                # Emulate depth-of-field lens blur with transparency mapping
                base_opacity = 1.0 - (0.75 * depth_frac * tilt_factor) 
                # Keep mostly opaque when expanding out of the frame
                final_opacity = max(0, min(1, base_opacity + (scale_mult - 1.0)*0.5 ))
                
                master_op = entrance_tracker.get_value()
                #mob[0].set_opacity(final_opacity * master_op) 
                opacity = final_opacity * master_op
                mob.set_opacity(opacity)

            return updater
        
        # Activate realtime dynamics BEFORE PLAY so they immediately warp off-screen
        t_start[0] = self.renderer.time
        for node, ba in zip(orbit_icons, base_angles):
            node.add_updater(make_icon_updater(node, ba))
            node.update()
            
        # ── PHASE 1: Fast Fly In (1.0s) ─────────────
        self.play(
            logo.animate.set_opacity(1).scale(1.25),
            orbit_scale_tracker.animate.set_value(1.0),
            entrance_tracker.animate.set_value(1.0),
            run_time=1.0, 
            rate_func=rate_functions.ease_out_cubic
        )

        # ── PHASE 2: Wait & Spin (1.5s) ──────────────────
        self.wait(1.5)

        # ── PHASE 3: Camera Tilt to Top-Down (1.5s) ──────────────────
        self.play(
            radius_x_tracker.animate.set_value(4.0), 
            radius_y_tracker.animate.set_value(4.0), 
            logo.animate.scale(0.85),
            run_time=1.5,
            rate_func=rate_functions.ease_in_expo,
        )
        
        # ── PHASE 4: Icons burst rapidly out of frame without fade (1.0s) ──────────────────
        self.play(
            orbit_scale_tracker.animate.set_value(5.0),
            logo.animate.scale(1.3),
            run_time=1.0,
            rate_func=rate_functions.ease_in_cubic
        )

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

    scene_to_render = AcceleratedOrbit()
    scene_to_render.render()

    file_dir = Path(r"../../../gold_pattern_test_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "synoptix_20_23.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")
