## 1:23 -1:25 Introducing Google Vids

from manim import *
import numpy as np
import os

class GoogleWorkspace(Scene):
    def construct(self):
        self.camera.background_color = ManimColor("#FFFFFF")

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
            "youtube.png",
        ]
        img_paths = [os.path.join(images_dir, name) for name in img_names]

        def make_icon(filepath, size=0.9):
            img = ImageMobject(filepath)
            img.height = size
            return img

        # Build all icons using Group instead of VGroup for ImageMobjects
        icons = Group(*[make_icon(p) for p in img_paths])

        # 3x3 Grid definitions
        d_x, d_y = 0.5, 0.5
        dot_positions = [
            np.array([-d_x, d_y, 0]),  # Top-Left
            np.array([0, d_y, 0]),     # Top-Center
            np.array([d_x, d_y, 0]),   # Top-Right
            np.array([-d_x, 0, 0]),    # Mid-Left
            np.array([d_x, 0, 0]),     # Mid-Right
            np.array([-d_x, -d_y, 0]), # Bottom-Left
            np.array([0, -d_y, 0]),    # Bottom-Center
            np.array([d_x, -d_y, 0]),  # Bottom-Right
        ]
        center_dot_pos = ORIGIN

        # Create grey dots
        dots = VGroup()
        for pos in dot_positions + [center_dot_pos]:
            dot = Circle(radius=0.15, fill_color=ManimColor("#5F6368"), fill_opacity=1, stroke_width=0)
            dot.move_to(pos)
            dots.add(dot)

        # 1. Dots appear
        self.play(FadeIn(dots, shift=UP*0.2), run_time=1.0)
        self.wait(0.4)

        # Dest positions for exploded grid
        R_x, R_y = 2.4, 2.4
        positions = [
            np.array([-R_x, R_y, 0]),  # 0: Sheets (Top-Left)
            np.array([0, R_y, 0]),     # 1: Gmail (Top-Center)
            np.array([R_x, R_y, 0]),   # 2: Drive (Top-Right)
            np.array([-R_x, 0, 0]),    # 3: Docs (Mid-Left)
            np.array([R_x, 0, 0]),     # 4: Slides (Mid-Right)
            np.array([-R_x, -R_y, 0]), # 5: Calendar (Bottom-Left)
            np.array([0, -R_y, 0]),    # 6: Meet (Bottom-Center)
            np.array([R_x, -R_y, 0]),  # 7: Vids/Youtube (Bottom-Right)
        ]

        # Stack icons at their corresponding dot positions initially
        for i, icon in enumerate(icons):
            icon.move_to(dot_positions[i])
            icon.set_opacity(0)
            icon.scale(0.2)

        self.add(icons)

        # 2. Explode! Dots turn into icons
        explode_anims = []
        for i, (icon, pos) in enumerate(zip(icons, positions)):
            explode_anims.append(icon.animate.set_opacity(1).scale(1/0.2).move_to(pos))
            explode_anims.append(dots[i].animate.set_opacity(0).scale(0.1).move_to(pos))
        
        # Center dot vanishes
        explode_anims.append(dots[8].animate.scale(0).set_opacity(0))

        self.play(
            AnimationGroup(*explode_anims),
            run_time=1.2,
            rate_func=rate_functions.ease_out_back # Bouncy explosion
        )
        self.wait(0.3)

        # Slight settle: gentle scale pulse
        self.play(
            *[icon.animate.scale(1.08) for icon in icons],
            run_time=0.25, rate_func=there_and_back
        )
        self.wait(0.2)

        # Build "Google Workspace" text with Google colors
        google_letters = [
            ("G", "#4285F4"), ("o", "#DB4437"), ("o", "#F4B400"),
            ("g", "#4285F4"), ("l", "#0F9D58"), ("e", "#DB4437"),
        ]

        google_text = VGroup()
        for letter, color in google_letters:
            t = Text(letter, font_size=72, color=ManimColor(color), weight=BOLD)
            google_text.add(t)
        google_text.arrange(RIGHT, buff=0.01)

        workspace_text = Text(" Workspace", font_size=72, color=ManimColor("#5F6368"), weight=BOLD)

        full_text = VGroup(google_text, workspace_text)
        full_text.arrange(RIGHT, buff=0.0)
        full_text.move_to(ORIGIN)
        full_text.set_opacity(0)
        full_text.scale(0.6)

        self.add(full_text)

        # PHASE 3: Collapse to center and INSTANTLY reveal text
        collapse_anims = []
        for icon in icons:
            # Icons rush to center and disappear
            collapse_anims.append(
                icon.animate(rate_func=rate_functions.ease_in_back, run_time=0.6).move_to(ORIGIN).scale(0.1).set_opacity(0),
            )

        # Play collapse
        self.play(AnimationGroup(*collapse_anims))
        
        # INSTANT pop of text
        self.play(
            full_text.animate.set_opacity(1).scale(1/0.6),
            run_time=0.5,
            rate_func=rate_functions.ease_out_back,
        )

        self.wait(1.5)
