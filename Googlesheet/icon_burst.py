from manim import *
import numpy as np
import random
import os

class IconBurst(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE
        
        # ── SCENE 1: CHECKMARK TO SUNBURST ───────────────────────────────
        
        # The blue circle that acts as the checkmark box AND the blue space in the sunburst
        check_bg = Circle(radius=1.5, color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        check_bg.scale(0.001)
        check_bg.set_z_index(-10) # Base layer
        
        # Thick white checkmark
        check_mark = VGroup(
            Line([-0.4, -0.2, 0], [0.1, -0.7, 0], color=WHITE, stroke_width=20),
            Line([0.1, -0.7, 0], [0.8, 0.4, 0], color=WHITE, stroke_width=20)
        )
        check_mark.shift(DOWN * 0.1)
        check_mark.scale(0.001)
        check_mark.set_z_index(-5)
        
        # Outer rotating arc
        arc = Arc(radius=1.75, angle=PI*1.5, color=ManimColor("#1565E0"), stroke_width=12)
        arc.set_z_index(-5)
        
        # The white petals that will emerge and form the sunburst rays
        n_petals = 6
        petals = VGroup()
        for i in range(n_petals):
            angle = i * (2 * PI / n_petals)
            # Make the white rays the same width as the blue spacing
            petal = Sector(radius=1.1, angle=PI/6, start_angle=angle, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            petals.add(petal)
        
        petals.set_z_index(-9) 
        petals.scale(0.001)
        petals.move_to(ORIGIN)
        
        self.add(check_bg, check_mark, petals)
        
        # 1. Pop in check_bg and check_mark cleanly
        self.play(
            check_bg.animate.scale(1000).set_rate_func(rate_functions.ease_out_elastic), 
            check_mark.animate.scale(1000).set_rate_func(rate_functions.ease_out_elastic),
            FadeIn(arc),
            run_time=0.6
        )
        
        # 2. Rotate arc rapidly around the checkmark
        self.play(
            Rotate(arc, angle=2 * PI, about_point=ORIGIN),
            run_time=0.6,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.remove(arc)
        
        # 3. Checkmark shrinks into the center while Petals emerge
        # This gives the magical "flower from within the box" effect
        self.play(
            check_mark.animate.scale(0.001),
            petals.animate.scale(1000), 
            run_time=0.35,
            rate_func=rate_functions.ease_out_back
        )
        self.remove(check_mark)
        
        # The combination of check_bg (blue circle) and petals (white sectors)
        # IS the sunburst!
        sunburst = VGroup(check_bg, petals)
        
        # Add rotation to sunburst
        def update_sunburst(mob, dt):
            mob.rotate(dt * 0.5)
            
        sunburst.add_updater(update_sunburst)
        
        # 4. The "flower" expands massively to become the sunburst background!
        # When scaled x30, petals radius is 33, check_bg is 45. Both are far 
        # beyond the 16:9 screen diagonal, so they look like infinite straight rays!
        self.play(
            sunburst.animate.scale(30),
            run_time=0.9,
            rate_func=rate_functions.ease_in_out_cubic
        )
        
        # ── ICON BURST ANIMATION ─────────────────────────────────────────
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "images")
        
        img_names = [
            "gmail.png", "google_calendar.png", "google_docs.png", 
            "google_drive.png", "google_meet.png", "google_sheets.png", 
            "google_slides.png", "youtube.png"
        ]
        
        icons_to_burst = []
        for img_name in img_names:
            img_path = os.path.join(images_dir, img_name)
            icon_img = ImageMobject(img_path)
            # Increased initial base size per user feedback
            icon_img.height = 0.85 
            icon_img.move_to(ORIGIN)
            icon_img.set_z_index(10)
            icon_img.scale(0.001) # Start invisible
            self.add(icon_img)
            icons_to_burst.append(icon_img)
        
        self.wait(0.2)
        
        # Animate all icons violently bursting off-center concurrently
        animations = []
        for i, icon in enumerate(icons_to_burst):
            icon.rotate(PI/4 if i % 2 == 0 else -PI/4)
            
            # Deviate from straight line randomly
            dev_x = random.uniform(-1.0, 1.0)
            dev_y = random.uniform(-1.0, 1.0)
            
            # Normalize to ensure extreme outward trajectory
            length = np.sqrt(dev_x**2 + dev_y**2)
            dev_dir = RIGHT * (dev_x / length) + UP * (dev_y / length)
            
            # Shift a massive distance alongside scaling to create off-center explosion
            anim = icon.animate.scale(30000).rotate(-PI/4).shift(dev_dir * 25)
            animations.append(anim)
            
        self.play(
            AnimationGroup(*animations, lag_ratio=0.15),
            run_time=8.0,
            rate_func=rate_functions.smooth
        )
        
        for icon in icons_to_burst:
            self.remove(icon)
            
        self.wait(1.5)
