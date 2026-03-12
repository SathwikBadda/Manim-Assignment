from manim import *
from manim.utils.rate_functions import ease_in_out_quad, ease_in_out_cubic, ease_out_back, ease_out_quad, ease_in_quad, ease_in_back, ease_in_expo

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from asset_manim_codes.asset_4 import AcademicIntelligenceDashboard
from asset_manim_codes.asset_5 import Asset5
from asset_manim_codes.asset_6 import SWOTMatrix
from asset_manim_codes.asset_7 import DecisionSignPost

import numpy as np
import random
from PIL import Image as PILImage
import tempfile

# ── Helper: load image with black-background removed (transparent PNG) ──
_TEMP_ICON_DIR = tempfile.mkdtemp()

def load_transparent_icon(path, threshold=60):
    """
    Convert dark/black backgrounds to transparent and save as temp PNG.
    This version is more robust to off-black backgrounds.
    """
    img = PILImage.open(path).convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        # Calculate brightness
        brightness = (r + g + b) / 3
        # If pixel is dark enough, make it transparent
        if brightness < threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    out_path = os.path.join(_TEMP_ICON_DIR, os.path.basename(path))
    img.save(out_path)
    return out_path

class FinalScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        
        ## Section 1
        
        bg = Rectangle(width=config.frame_width, height=config.frame_height, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        bg.set_z_index(0)
        self.add(bg)
        
        
        pathway_line = VMobject()
        pathway_line.set_points_smoothly([
            LEFT * 4.0 + DOWN * 4.0,
            LEFT * 1.5,
            RIGHT * 4.0 + UP * 4.0
        ])
        pathway_line.set_color("#F97316")
        pathway_line.set_stroke(width=2)
        pathway_line.set_z_index(1)

        heading = Text("Start the My Sathi Journey", font="Georgia", font_size=32, color="#C6C7DC")
        heading.move_to(UP * 3.5)
        heading.set_z_index(2)
        
        self.play(AddTextLetterByLetter(heading), run_time=2.4)
        # Fade heading out immediately after showing it so it never bleeds into zoomed views
        self.play(FadeOut(heading), run_time=0.6)
        
        
        
        self.move_camera(frame_center=pathway_line.get_start(), zoom=2.5, run_time=1.5)
        
        
        
        ## Section 2
        
        milestone_1_node = Circle(radius=0.5, fill_color="#F97316", fill_opacity=0.8, stroke_width=2)
        milestone_1_node.move_to(pathway_line.point_from_proportion(0.3))
        milestone_1_node.set_z_index(3)
        #self.add(milestone_1_node)
        
        milestone_1_label = Text("Classes 8–10", font="Georgia", font_size=24, color="#C6C7DC").scale(1/2.5)
        
        milestone_1_label.move_to(milestone_1_node.get_center())
        milestone_1_label.set_z_index(4)
        #self.add(milestone_1_label)
        
        self.move_camera(
            frame_center=milestone_1_node.get_center(),
            added_anims=[Create(pathway_line)],
            run_time=3.0
        )

        # ── Classes 8-10: icons hidden perfectly behind circle leveraging scale and z_index ──
        milestone_center = milestone_1_node.get_center()
        DISPLAY_SCALE = 0.22

        corner_offsets_1 = [
            np.array([-1.6,  0.9, 0]),   # top-left
            np.array([ 1.6,  0.9, 0]),   # top-right
            np.array([-1.6, -0.9, 0]),   # bottom-left
            np.array([ 1.6, -0.9, 0]),   # bottom-right
            np.array([ 0.0,  1.2, 0]),   # top-center
        ]

        icon_labels_text = [
            "Aptitude",
            "Logical Reasoning",
            "Verbal Ability",
            "Personality Insights",
            "Early Career Awareness",
        ]

        icons_1        = []
        target_poses_1 = []

        for i, img_num in enumerate([26, 27, 28, 29, 30]):
            offset     = corner_offsets_1[i]
            target_pos = milestone_center + offset

            # Always load with black background removed
            clean_path = load_transparent_icon(f"../images/image_{img_num}.png")
            icon = ImageMobject(clean_path)
            icon.scale(DISPLAY_SCALE)
            icon.move_to(milestone_center)  # Start at center of circle
            icon.set_opacity(0)
            icon.set_z_index(5)
            icons_1.append(icon)
            self.add(icon)
            target_poses_1.append(target_pos.copy())

        self.play(GrowFromCenter(milestone_1_node), run_time=1.2, rate_func=ease_out_back)
        self.play(AddTextLetterByLetter(milestone_1_label), run_time=1.2)
        self.play(pathway_line.animate.set_stroke(width=0.1), run_time=0.5)

        # ── Burst: ALL icons fly out simultaneously from circle center ──
        def make_burst(icon, target_pos):
            start = milestone_center.copy()
            end   = target_pos.copy()
            def updater(mob, alpha):
                t = smooth(alpha)
                mob.move_to(start + t * (end - start))
                mob.set_opacity(t)
            return UpdateFromAlphaFunc(icon, updater, run_time=1.0)

        burst_anims = []
        for icon, target_pos in zip(icons_1, target_poses_1):
            burst_anims.append(make_burst(icon, target_pos))

        self.play(AnimationGroup(*burst_anims, lag_ratio=0.0), run_time=1.0)
        self.wait(1.0)

        # ── Collapse: ALL icons fly back simultaneously to circle center ──
        def make_collapse(icon, target_pos):
            start = target_pos.copy()
            end   = milestone_center.copy()
            def updater(mob, alpha):
                t = smooth(alpha)
                mob.move_to(start + t * (end - start))
                mob.set_opacity(1 - t)
            return UpdateFromAlphaFunc(icon, updater, run_time=0.8)

        collapse_anims = []
        for icon, target_pos in zip(icons_1, target_poses_1):
            collapse_anims.append(make_collapse(icon, target_pos))

        self.play(AnimationGroup(*collapse_anims, lag_ratio=0.0), run_time=0.8)

        self.play(pathway_line.animate.set_stroke(width=2.0), run_time=0.5)
        self.remove(*icons_1)
        icons_1 = []
        
        
        self.wait(1.9)
        
        ## Section 3
        
        self.play(
            milestone_1_node.animate.set_opacity(0.5),
            milestone_1_label.animate.set_opacity(0.5),
            run_time=1.0
        )
        
        milestone_2_node = Circle(radius=0.5, fill_color="#F97316", fill_opacity=0.8, stroke_width=2)
        milestone_2_node.move_to(pathway_line.point_from_proportion(0.65))
        milestone_2_node.set_z_index(3)
        
        milestone_2_label = Text("Classes 11–12", font="Georgia", font_size=24, color="#C6C7DC").scale(1/2.5)
        milestone_2_label.move_to(milestone_2_node.get_center())
        milestone_2_label.set_z_index(4)
        
        self.move_camera(
            frame_center=milestone_2_node.get_center(),
            run_time=2.0
        )
        
        # ── Classes 11-12: icons hidden perfectly behind circle leveraging scale and z_index ──
        milestone_2_center = milestone_2_node.get_center()

        corner_offsets_2 = [
            np.array([-1.6,  0.9, 0]),   # top-left
            np.array([ 1.6,  0.9, 0]),   # top-right
            np.array([-1.9,  0.0, 0]),   # left-center
            np.array([ 1.9,  0.0, 0]),   # right-center
            np.array([-1.6, -0.9, 0]),   # bottom-left
            np.array([ 1.6, -0.9, 0]),   # bottom-right
        ]

        icon_labels_text_2 = [
            "Critical Thinking",
            "Creativity",
            "Communication",
            "Collaboration",
            "Interview Readiness",
            "Profile Building",
        ]

        icons_2        = []
        target_poses_2 = []

        for i, img_num in enumerate([31, 32, 33, 34, 35, 36]):
            offset     = corner_offsets_2[i]
            target_pos = milestone_2_center + offset

            # Always load with black background removed
            clean_path = load_transparent_icon(f"../images/image_{img_num}.png")
            icon = ImageMobject(clean_path)
            icon.scale(DISPLAY_SCALE)
            icon.move_to(milestone_2_center)  # Start at center of circle
            icon.set_opacity(0)
            icon.set_z_index(5)
            icons_2.append(icon)
            self.add(icon)
            target_poses_2.append(target_pos.copy())

        self.play(GrowFromCenter(milestone_2_node), run_time=1.2, rate_func=ease_out_back)
        self.play(AddTextLetterByLetter(milestone_2_label), run_time=1.2)
        self.play(pathway_line.animate.set_stroke(width=0.1), run_time=0.5)

        # ── Burst: ALL icons fly out simultaneously from circle center ──
        def make_burst_2(icon, target_pos):
            start = milestone_2_center.copy()
            end   = target_pos.copy()
            def updater(mob, alpha):
                t = smooth(alpha)
                mob.move_to(start + t * (end - start))
                mob.set_opacity(t)
            return UpdateFromAlphaFunc(icon, updater, run_time=1.0)

        burst_anims_2 = []
        for icon, target_pos in zip(icons_2, target_poses_2):
            burst_anims_2.append(make_burst_2(icon, target_pos))

        self.play(AnimationGroup(*burst_anims_2, lag_ratio=0.0), run_time=1.0)
        self.wait(1.0)

        # ── Collapse: ALL icons fly back simultaneously to circle center ──
        def make_collapse_2(icon, target_pos):
            start = target_pos.copy()
            end   = milestone_2_center.copy()
            def updater(mob, alpha):
                t = smooth(alpha)
                mob.move_to(start + t * (end - start))
                mob.set_opacity(1 - t)
            return UpdateFromAlphaFunc(icon, updater, run_time=0.8)

        collapse_anims_2 = []
        for icon, target_pos in zip(icons_2, target_poses_2):
            collapse_anims_2.append(make_collapse_2(icon, target_pos))

        self.play(AnimationGroup(*collapse_anims_2, lag_ratio=0.0), run_time=0.8)

        self.play(pathway_line.animate.set_stroke(width=2.0), run_time=0.5)
        self.remove(*icons_2)
        icons_2 = []
        
        self.wait(1.0)
        
        ## Section 4
        
        self.play(
            milestone_1_node.animate.set_opacity(0.5),
            milestone_2_node.animate.set_opacity(0.5),
            run_time=1.0
        )
        
        milestone_3_node = Circle(radius=0.5, fill_color="#F97316", fill_opacity=0.8, stroke_width=2)
        milestone_3_node.move_to(pathway_line.point_from_proportion(0.9))
        milestone_3_node.set_z_index(2)
        # NOTE: milestone_3_label is intentionally never added to the scene
        # so "College & Career" text cannot appear during the zoom-in.
        milestone_3_label = None

        self.move_camera(
            frame_center=milestone_3_node.get_center(),
            run_time=2.0
        )

        # Fade out the two labels from earlier milestones before zooming
        self.play(
            FadeOut(milestone_1_label),
            FadeOut(milestone_2_label),
            run_time=0.4
        )

        self.play(GrowFromCenter(milestone_3_node), run_time=1.2, rate_func=ease_out_back)
        # Zoom in on the 3rd circle — no text in scene so nothing bleeds through
        self.move_camera(frame_center=milestone_3_node.get_center(), zoom=20.0, run_time=1.2)
        self.wait(2.0)
        
        ## Section 5
        
        self.play(
            FadeOut(milestone_1_node),
            FadeOut(milestone_1_label),
            FadeOut(milestone_2_node),
            FadeOut(milestone_2_label),
            FadeOut(milestone_3_node),
            # milestone_3_label is None (never shown), so skip it
            FadeOut(pathway_line),
            run_time=1.0
        )
        
        self.move_camera(zoom=1.0, frame_center=ORIGIN, run_time=1.5)
        
        # --- Part 1: Outcomes for Students ---
        
        title_students = Text("Outcomes for Students", font="Georgia", font_size=36, color="#C6C7DC")
        title_students.to_edge(UP, buff=1.0)
        
        swot = SWOTMatrix(stroke_color="#F97316",label_color="#093F72")
        swot.scale_to_fit_height(3.5)
        swot.move_to(LEFT * 3.2)
        swot.rotate(20*DEGREES, axis=UP)
        
        decision_post = DecisionSignPost(labels=["Post-school Courses","College for Admission","Career Path"],stroke_color=
                                         "#F97316",depth_offset=0.1)
        decision_post.scale_to_fit_height(3.5)
        decision_post.move_to(RIGHT * 3.2)
        decision_post.rotate(-20*DEGREES, axis=UP)
        
        # Entrance
        self.play(
            FadeIn(title_students, shift=DOWN),
            GrowFromPoint(swot, point=np.array([-config.frame_width/2, -config.frame_height/2, 0])),
            GrowFromPoint(decision_post, point=np.array([config.frame_width/2, -config.frame_height/2, 0])),
            run_time=1.5,
            rate_func=ease_out_back
        )
        self.wait(1.5)
        
        # Exit (Burst)
        self.play(FadeOut(title_students, shift=UP), run_time=0.5)
        
        icons_to_burst = [swot, decision_post]
        animations = []
        for i, icon in enumerate(icons_to_burst):
            dev_x = random.uniform(-0.5, 0.5)
            dev_y = random.uniform(-0.5, 0.5)
            
            # Bias direction outwards based on position
            if icon.get_center()[0] < 0: dev_x = -abs(dev_x) - 0.2
            else: dev_x = abs(dev_x) + 0.2
            
            length = np.sqrt(dev_x**2 + dev_y**2)
            if length == 0: length = 1
            dev_dir = RIGHT * (dev_x / length) + UP * (dev_y / length)
            
            anim = icon.animate.scale(8).shift(dev_dir * 15).set_opacity(0)
            animations.append(anim)
            
        self.play(
            AnimationGroup(*animations, lag_ratio=0.4),
            run_time=1.5,
            rate_func=ease_in_out_quad
        )
        self.remove(swot, decision_post)
        
        # --- Part 2: Value For Institutions ---
        
        title_institutions = Text("Value For Institutions", font="Georgia", font_size=36, color="#C6C7DC")
        title_institutions.to_edge(UP, buff=1.0)
        
        dashboard = AcademicIntelligenceDashboard()
        dashboard_bg = RoundedRectangle(width=dashboard.width+0.2, height=dashboard.height+0.2, corner_radius=0.2, fill_color=WHITE, fill_opacity=1, stroke_color="#6795C9", stroke_width=2)
        dashboard_group = VGroup(dashboard_bg, dashboard)
        dashboard_group.scale_to_fit_height(3.5)
        dashboard_group.move_to(LEFT * 3.2)
        dashboard_group.rotate(20*DEGREES, axis=UP)
        
        asset_5 = Asset5(color_data={(0,1):0.7,(0,2):0.3,(0,3):0.5})
        asset_5.scale_to_fit_height(3.5)
        asset_5.move_to(RIGHT * 3.2)
        asset_5.rotate(-20*DEGREES, axis=UP)
        
        # Entrance
        self.play(
            FadeIn(title_institutions, shift=DOWN),
            GrowFromPoint(dashboard_group, point=np.array([-config.frame_width/2, -config.frame_height/2, 0])),
            GrowFromPoint(asset_5, point=np.array([config.frame_width/2, -config.frame_height/2, 0])),
            run_time=1.5,
            rate_func=ease_out_back
        )
        self.wait(1.5)
        
        # Exit (Burst)
        self.play(FadeOut(title_institutions, shift=UP), run_time=0.5)
        
        icons_to_burst_2 = [dashboard_group, asset_5]
        animations_2 = []
        for i, icon in enumerate(icons_to_burst_2):
            dev_x = random.uniform(-0.5, 0.5)
            dev_y = random.uniform(-0.5, 0.5)
            
            if icon.get_center()[0] < 0: dev_x = -abs(dev_x) - 0.2
            else: dev_x = abs(dev_x) + 0.2
            
            length = np.sqrt(dev_x**2 + dev_y**2)
            if length == 0: length = 1
            dev_dir = RIGHT * (dev_x / length) + UP * (dev_y / length)
            
            anim = icon.animate.scale(8).shift(dev_dir * 15).set_opacity(0)
            animations_2.append(anim)
            
        self.play(
            AnimationGroup(*animations_2, lag_ratio=0.4),
            run_time=1.5,
            rate_func=ease_in_out_quad
        )
        self.remove(dashboard_group, asset_5)

        ## Section 6
        
        texts = [
            "Your Next Step",
            "Register for SATHI Empanelment",
            "Nominate Institutional SPOC",
            "Begin Onboarding & Orientation",
            "Empanel Today. Build Future-Ready Students."
        ]
        
        colors = ["#6165AA", "#263CAA", "#7C592B", "#7C560E", "#19191D"]
        fonts = ["Georgia", "Times New Roman", "Times New Roman", "Times New Roman", "Georgia"]
        font_sizes = [36, 32, 32, 32, 36]
        
        logo = ImageMobject("../images/image_37.png")
        logo.scale(1.0)
        logo.move_to(UP * 1.5)
        logo.set_z_index(2)
        
        last_text = None
        
        for i, (text_str, color, font, f_size) in enumerate(zip(texts, colors, fonts, font_sizes)):
            text_obj = Text(text_str, font=font, font_size=f_size, color=color)
            text_obj.set_z_index(2)
            
            if i == len(texts) - 1:
                text_obj.next_to(logo, DOWN, buff=0.5)
                last_text = text_obj
                
                self.play(
                    AnimationGroup(
                        FadeIn(logo, shift=UP*0.15),
                        LaggedStart(*[FadeIn(char, shift=UP*0.15) for char in text_obj], lag_ratio=0.02),
                        lag_ratio=0.1
                    ),
                    run_time=2.0,
                    rate_func=smooth
                )
            else:
                text_obj.move_to(ORIGIN)
                self.play(
                    LaggedStart(*[FadeIn(char, shift=UP*0.15) for char in text_obj], lag_ratio=0.02),
                    run_time=2.0,
                    rate_func=smooth
                )
            
            self.wait(0.6)
            
            if i < len(texts) - 1:
                self.play(
                    LaggedStart(*[FadeOut(char, shift=UP*0.2) for char in text_obj], lag_ratio=0.015),
                    run_time=1.0,
                    rate_func=smooth
                )
        
        self.wait(2.0)
        
        self.play(
            FadeOut(bg),
            FadeOut(logo),
            FadeOut(last_text),
            run_time=2.0
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

    scene_to_render = FinalScene()
    scene_to_render.render()

    file_dir = Path(r"../test_raw_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "Scene_4.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")