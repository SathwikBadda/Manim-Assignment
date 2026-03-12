from manim import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from asset_manim_codes.asset_1 import asset_1
from asset_manim_codes.asset_2 import SpeechBubble
import numpy as np

class FinalScene(ThreeDScene):
    def construct(self):
        ## Section 1
        
        # Initial setup
        primary_text = "#0B2A5B"
        primary_accent = "#F4B400"
        secondary_text = "#1E73BE"
        background_color = "#F4EBD8"
        
        self.camera.background_color = ManimColor(background_color)
        
        # Create asset_1 (staircase)
        staircase = asset_1(
            num_steps=4,
            step_height=1.5,
            platform_width=2.5,
            primary_text_color=primary_text,
            primary_accent_color=primary_accent
        )
        staircase.move_to(ORIGIN).shift(LEFT * 1.0 + DOWN * 0.5)

        platform_1 = staircase.get_platform_at_step(0)
        platform_1_center = staircase.get_platform_center(0)

        
        # Load images
        image_1 = ImageMobject("../images/image_1.png").scale(0.5)
        image_1.set_z_index(2)
        image_1.move_to(platform_1_center + UP * (image_1.height/2-0.5) + RIGHT * 1.1)
        
        image_2_trophy_1 = ImageMobject("../images/image_2.png").scale(0.4).move_to(platform_1_center + UP * 0.7)
        image_2_trophy_1.set_z_index(2)
        
        image_3_crowd = ImageMobject("../images/image_3.png").scale(1.2).move_to(DOWN * 3.3 + RIGHT * 2.5)
        image_3_crowd.set_z_index(2)

        def create_jump_path(start, end, height=2.0, steps=50):
            path = VMobject()
            points = [
                start * (1 - t) + end * t + UP * height * np.sin(t * np.pi)
                for t in np.linspace(0, 1, steps)
            ]
            path.set_points_smoothly(points)
            path.set_stroke(color=ManimColor(primary_accent), width=1)
            return path


        
        
        
        # Entry phase (1.2s for trophy, 1.2s for text, 0.8s for baseline extension)
        text_step_1 = Text(
            "Step 1: Recognition Begins",
            font="Georgia",
            weight=BOLD,
            font_size=15,
            color=ManimColor(primary_text)
        ).move_to(platform_1_center + DOWN * 0.8 + RIGHT * 0.5)
        
        self.play(
            GrowFromEdge(platform_1, RIGHT),
            run_time=0.5
        )
        
        # Trophy 1 fades in with upward drift
        self.play(
            FadeIn(image_2_trophy_1, shift=UP * 0.15),
            run_time=1.2
        )
        
        self.play(
            AddTextLetterByLetter(text_step_1),
            run_time=1.2
        )
        
        
        
        # Core transformation phase
        # Platform 2 and image_1 ascent
        platform_2 = staircase.get_platform_at_step(1)
        platform_2_center = staircase.get_platform_center(1)
        
        riser_1 = staircase.get_riser_between_steps(0, 1)
        self.play(GrowFromEdge(riser_1, DOWN), run_time=0.3)
        self.play(GrowFromEdge(platform_2, RIGHT), run_time=0.5)
        
        start_1 = image_1.get_center()
        end_1 = platform_2_center + UP * (image_1.height/2-0.5) + RIGHT * 1.1
        jump_path_1 = create_jump_path(start_1, end_1)
        
        # Trophy 2 center under wave
        trophy_2_pos = (start_1 + end_1) / 2 + UP * 0.8
        image_2_trophy_2 = ImageMobject("../images/image_2.png").scale(0.4).move_to(trophy_2_pos)
        image_2_trophy_2.set_z_index(2)
        
        self.play(
            Create(jump_path_1),
            MoveAlongPath(image_1, jump_path_1),
            FadeIn(image_2_trophy_2, shift=UP*0.2),
            run_time=1.0,
            rate_func=linear
        )
        
        text_step_2 = Text(
            "Step 2: Consistent Excellence",
            font="Georgia", weight=BOLD, font_size=15, color=ManimColor(primary_text)
        ).move_to(platform_2_center + DOWN * 0.8 + RIGHT * 0.5)
        self.play(AddTextLetterByLetter(text_step_2), run_time=1.0)
        
        # Platform 3 and image_1 ascent
        platform_3 = staircase.get_platform_at_step(2)
        platform_3_center = staircase.get_platform_center(2)
        
        riser_2 = staircase.get_riser_between_steps(1, 2)
        self.play(GrowFromEdge(riser_2, DOWN), run_time=0.3)
        self.play(GrowFromEdge(platform_3, RIGHT), run_time=0.5)
        
        start_2 = image_1.get_center()
        end_2 = platform_3_center + UP * (image_1.height/2-0.5) + RIGHT * 1.1
        jump_path_2 = create_jump_path(start_2, end_2)
        
        # Trophy 3 center under wave
        trophy_3_pos = (start_2 + end_2) / 2 + UP * 0.8
        image_2_trophy_3 = ImageMobject("../images/image_2.png").scale(0.4).move_to(trophy_3_pos)
        image_2_trophy_3.set_z_index(2)
        
        self.play(
            Create(jump_path_2),
            jump_path_1.animate.set_stroke(opacity=0.3),
            MoveAlongPath(image_1, jump_path_2),
            FadeIn(image_2_trophy_3, shift=UP*0.2),
            run_time=1.0,
            rate_func=linear
        )
        
        text_step_3 = Text(
            "Step 3: Outstanding Achievement",
            font="Georgia", weight=BOLD, font_size=15, color=ManimColor(primary_text)
        ).move_to(platform_3_center + DOWN * 0.8 + RIGHT * 0.8)
        self.play(AddTextLetterByLetter(text_step_3), run_time=1.0)
        
        # Platform 4 and image_1 ascent
        platform_4 = staircase.get_platform_at_step(3)
        platform_4_center = staircase.get_platform_center(3)
        
        riser_3 = staircase.get_riser_between_steps(2, 3)
        self.play(GrowFromEdge(riser_3, DOWN), run_time=0.3)
        self.play(GrowFromEdge(platform_4, RIGHT), run_time=0.5)
        
        start_3 = image_1.get_center()
        end_3 = platform_4_center + UP * (image_1.height/2-0.5) + RIGHT * 1.1
        jump_path_3 = create_jump_path(start_3, end_3)
        
        # Trophy 4 center under wave
        trophy_4_pos = (start_3 + end_3) / 2 + UP * 0.8
        image_2_trophy_4 = ImageMobject("../images/image_2.png").scale(0.4).move_to(trophy_4_pos)
        image_2_trophy_4.set_z_index(2)
        
        self.play(
            Create(jump_path_3),
            jump_path_2.animate.set_stroke(opacity=0.3),
            MoveAlongPath(image_1, jump_path_3),
            FadeIn(image_2_trophy_4, shift=UP*0.2),
            run_time=1.0,
            rate_func=linear
        )
        
        # Scale all trophies up
        self.play(
            image_2_trophy_1.animate.scale(1.1),
            image_2_trophy_2.animate.scale(1.1),
            image_2_trophy_3.animate.scale(1.1),
            image_2_trophy_4.animate.scale(1.1),
            run_time=0.5
        )
        
        text_step_4 = Text(
            "Step 4: Highest & Best Student Award",
            font="Georgia", weight=BOLD, font_size=15, color=ManimColor(primary_text)
        ).move_to(platform_4_center + DOWN * 0.8 + RIGHT * 0.8)
        self.play(AddTextLetterByLetter(text_step_4), run_time=1.2)
        
        # Resolution phase
        self.move_camera(zoom=1/1.2, run_time=1.2)
        
        self.play(
            FadeIn(image_3_crowd),
            run_time=1.2
        )
        
        self.play(
            image_3_crowd.animate.shift(UP * 0.0),
            run_time=0.1
        )
        
        # Speech bubbles from crowd
        bubble_1 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_1.move_to(image_3_crowd.get_center() + LEFT * 1.5 + UP * 1.4)
        bubble_1.set_color(primary_accent)
        bubble_1.set_z_index(1)
        text_bubble_1 = Text("How did this student\nachieve so much?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_1.move_to(bubble_1.get_text_anchor("center"))
        text_bubble_1.set_z_index(2)
        
        bubble_2 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_2.move_to(image_3_crowd.get_center() + UP * 1.8)
        bubble_2.set_color(primary_accent)
        bubble_2.set_z_index(1)
        text_bubble_2 = Text("Where did he learn\nall this?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_2.move_to(bubble_2.get_text_anchor("center"))
        text_bubble_2.set_z_index(2)
        
        bubble_3 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_3.move_to(image_3_crowd.get_center() + RIGHT * 1.5 + UP * 1.4)
        bubble_3.set_color(primary_accent)
        bubble_3.set_z_index(1)
        text_bubble_3 = Text("Which school is he\ncoming from?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_3.move_to(bubble_3.get_text_anchor("center"))
        text_bubble_3.set_z_index(2)

        self.play(FadeIn(bubble_1), GrowFromCenter(bubble_2), GrowFromCenter(bubble_3), run_time=0.35)
        self.play(AddTextLetterByLetter(text_bubble_1), AddTextLetterByLetter(text_bubble_2), AddTextLetterByLetter(text_bubble_3), run_time=0.5)
        
        self.wait(0.3)
        
        # Round 2 of bubbles
        bubble_4 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_4.move_to(image_3_crowd.get_center() + LEFT * 1.5 + UP * 1.55 + RIGHT * 0.15)
        bubble_4.set_color(primary_accent)
        bubble_4.set_z_index(3)
        text_bubble_4 = Text("Which college\nshaped him?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_4.move_to(bubble_4.get_text_anchor("center"))
        text_bubble_4.set_z_index(4)
        
        bubble_5 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_5.move_to(image_3_crowd.get_center() + UP * 1.95 + RIGHT * 0.15)
        bubble_5.set_color(primary_accent)
        bubble_5.set_z_index(3)
        text_bubble_5 = Text("I heard he uses\nthe My Sathi app,", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_5.move_to(bubble_5.get_text_anchor("center"))
        text_bubble_5.set_z_index(4)
        
        bubble_6 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_6.move_to(image_3_crowd.get_center() + RIGHT * 1.65 + UP * 1.55)
        bubble_6.set_color(primary_accent)
        bubble_6.set_z_index(3)
        text_bubble_6 = Text("His school uses\nthe My Sathi app,", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_6.move_to(bubble_6.get_text_anchor("center"))
        text_bubble_6.set_z_index(4)
        
        self.play(GrowFromCenter(bubble_4), GrowFromCenter(bubble_5), GrowFromCenter(bubble_6), run_time=0.5)
        self.play(AddTextLetterByLetter(text_bubble_4), AddTextLetterByLetter(text_bubble_5), AddTextLetterByLetter(text_bubble_6), run_time=0.5)
        
        self.wait(0.3)
        
        # Round 3 of bubbles
        bubble_7 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_7.move_to(image_3_crowd.get_center() + LEFT * 1.5 + UP * 1.70 + RIGHT * 0.30)
        bubble_7.set_color(primary_accent)
        bubble_7.set_z_index(5)
        text_bubble_7 = Text("What is this\nMy Sathi app?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_7.move_to(bubble_7.get_text_anchor("center"))
        text_bubble_7.set_z_index(6)
        
        bubble_8 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_8.move_to(image_3_crowd.get_center() + UP * 2.10 + RIGHT * 0.30)
        bubble_8.set_color(primary_accent)
        bubble_8.set_z_index(5)
        text_bubble_8 = Text("How does it\nhelp students?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_8.move_to(bubble_8.get_text_anchor("center"))
        text_bubble_8.set_z_index(6)
        
        bubble_9 = SpeechBubble(width=1.5, height=0.8, pointer_direction="down_left")
        bubble_9.move_to(image_3_crowd.get_center() + RIGHT * 1.80 + UP * 1.70)
        bubble_9.set_color(primary_accent)
        bubble_9.set_z_index(5)
        text_bubble_9 = Text("Is this the secret\nbehind success?", font="Times New Roman", font_size=10, color=ManimColor(secondary_text))
        text_bubble_9.move_to(bubble_9.get_text_anchor("center"))
        text_bubble_9.set_z_index(6)
        
        self.play(GrowFromCenter(bubble_7), GrowFromCenter(bubble_8), GrowFromCenter(bubble_9), run_time=0.5)
        self.play(AddTextLetterByLetter(text_bubble_7), AddTextLetterByLetter(text_bubble_8), AddTextLetterByLetter(text_bubble_9), run_time=0.5)
        
        self.wait(0.3)
        
        self.wait(3.0)
        
        self.play(
            FadeOut(Group(
                staircase, jump_path_1, jump_path_2, jump_path_3, image_2_trophy_1, image_2_trophy_2,
                image_2_trophy_3, image_2_trophy_4, image_3_crowd,
                text_step_1, text_step_2, text_step_3, text_step_4,
                bubble_1, bubble_2, bubble_3, bubble_4, bubble_5, bubble_6, bubble_7, bubble_8, bubble_9,
                text_bubble_1, text_bubble_2, text_bubble_3, text_bubble_4, text_bubble_5, text_bubble_6, text_bubble_7, text_bubble_8, text_bubble_9
            )),
            run_time=0.5
        )
        
        
        # Move person to center and scale
        self.play(
            image_1.animate.move_to(ORIGIN).scale(2.5),
            run_time=1.0,
            rate_func=rate_functions.ease_out_cubic
        )
        
        # Add a spotlight beam from top
        beam = Polygon(
            ORIGIN + UP * 8 + LEFT * 0.5,
            ORIGIN + UP * 8 + RIGHT * 0.5,
            ORIGIN + DOWN * 1.5 + RIGHT * 3.0,
            ORIGIN + DOWN * 1.5 + LEFT * 3.0,
            fill_color=ManimColor("#FFD700"),
            fill_opacity=0.3,
            stroke_width=0
        )
        
        bottom_text_spotlight = Text(
            "Excellence is never accidental. It is shaped by where learning begins",
            font="Times New Roman",
            font_size=32,
            color=ManimColor(primary_text)
        ).move_to(DOWN * 3.5)
        
        self.play(FadeIn(beam), AddTextLetterByLetter(bottom_text_spotlight), run_time=1.0)
        self.play(
            beam.animate.set_opacity(0.5),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.play(FadeOut(beam), FadeOut(image_1), FadeOut(bottom_text_spotlight), run_time=0.5)

        ## Section 2
        
        # Reset camera
        current_zoom = self.camera.zoom
        self.set_camera_orientation(zoom=current_zoom * (1/1.5))
        right_center = ORIGIN
        
        heading = Text("What Makes the Difference?", font="Georgia", weight=BOLD, font_size=24, color=ManimColor(primary_text)).move_to(right_center + UP * 4.0)
        subheading = Text("Understanding the System Behind Success", font="Times New Roman", font_size=26, color=ManimColor(secondary_text)).move_to(right_center + DOWN * 4.0)
        
        self.play(AddTextLetterByLetter(heading), AddTextLetterByLetter(subheading), run_time=1.0)
        
        image_4 = ImageMobject("../images/image_4.png")
        image_4.move_to(right_center)
        image_4.scale(1.3)
        image_4.set_z_index(0)
        
        orbit_icons = []
        for img_name in ["image_5.png", "image_6.png", "image_7.png", "image_8.png"]:
            icon_img = ImageMobject(f"../images/{img_name}")
            icon_img.height = 4.0
            icon_img.move_to(right_center)
            orbit_icons.append(Group(icon_img))
            
        all_icons = Group(*orbit_icons)
        self.add(all_icons)
        
        radius_x_tracker = ValueTracker(4.0)
        radius_y_tracker = ValueTracker(1.5)
        orbit_scale_tracker = ValueTracker(4.0) # start out of frame
        
        t_start = [self.renderer.time]
        ROTATION_SPEED = 1.5
        
        def make_icon_updater(node, base_angle):
            def updater(mob, dt):
                t = self.renderer.time - t_start[0]
                angle = base_angle + t * ROTATION_SPEED
                rx = radius_x_tracker.get_value()
                ry = radius_y_tracker.get_value()
                scale_mult = orbit_scale_tracker.get_value()
                
                eff_rx = rx * scale_mult
                eff_ry = ry * scale_mult
                
                x = right_center[0] + eff_rx * np.cos(angle)
                y = right_center[1] + eff_ry * np.sin(angle)
                mob.move_to(np.array([x, y, 0]))
                
                unscaled_y = ry * np.sin(angle)
                tilt_ratio = ry / rx if rx > 0 else 1
                tilt_factor = np.clip((1.0 - tilt_ratio) / (1.0 - 1.0/2.5), 0, 1)
                depth_frac = (unscaled_y + ry) / (2 * ry) if ry > 0 else 0
                
                target_scale = 1.0 + (0.8 - 1.5 * depth_frac) * tilt_factor
                mob.height = 4.0 * target_scale
                mob.width = 4.0 * target_scale
                
                mob.set_z_index(int(-unscaled_y * 10))
            return updater
            
        base_angles = [PI/2, 0, 3*PI/2, PI]
        
        for node, ba in zip(orbit_icons, base_angles):
            node.add_updater(make_icon_updater(node, ba))
            node.update()
            
        # Entry Phase
        self.play(
            GrowFromCenter(image_4),
            orbit_scale_tracker.animate.set_value(1.0),
            run_time=1.0, 
            rate_func=rate_functions.ease_out_cubic
        )
        
        self.wait(1.5)
        
        # Hold Isometric Orbit
        self.wait(1.5)
        
        self.wait(2.0)
        
        # Explosive Exit completely out of frame
        self.play(
            orbit_scale_tracker.animate.set_value(40.0),
            image_4.animate.scale(25.0).set_opacity(0),
            heading.animate.shift(UP * 15),
            subheading.animate.shift(DOWN * 15),
            run_time=1.5,
            rate_func=rate_functions.ease_in_cubic
        )
        self.wait(0.5)

        self.wait(1.0)


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

    scene_to_render = FinalScene()
    scene_to_render.render()

    file_dir = Path(r"../test_raw_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "Scene_1.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")