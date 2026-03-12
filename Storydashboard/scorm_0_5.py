from manim import *
import numpy as np
import random

class IntroScene(ThreeDScene):
    def construct(self):
        self.camera.background_color = ManimColor("#F8F9FB")
        
        # ── BACKGROUND PARTICLES ─────────────────────────────────────────
        # Drifting grey and light blue circles
        particles = VGroup()
        colors = [ManimColor("#E0E5EC"), ManimColor("#D0E0FF")]
        for _ in range(30):
            c = Circle(
                radius=random.uniform(0.05, 0.2), 
                stroke_width=0, 
                fill_color=random.choice(colors), 
                fill_opacity=random.uniform(0.3, 0.7)
            )
            c.move_to([random.uniform(-8, 8), random.uniform(-5, 5), 0])
            
            # Attach random velocity for drifting
            c.velocity = np.array([random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), 0])
            particles.add(c)
            
        def update_particles(mob, dt):
            for p in mob:
                p.shift(p.velocity * dt)
                # Wrap around screen
                if p.get_x() > 8: p.set_x(-8)
                if p.get_x() < -8: p.set_x(8)
                if p.get_y() > 5: p.set_y(-5)
                if p.get_y() < -5: p.set_y(5)
                
        particles.add_updater(update_particles)
        self.add(particles)
        
        # ── MAIN TEXT: "SCORM" ───────────────────────────────────────────
        # Note: Reduced font size to avoid overlapping the dialogue boxes
        scorm_text = Text("SCORM", font_size=150, weight=HEAVY, color=ManimColor("#1a1a2e"))
        scorm_text.move_to(DOWN * 1.5)
        
        # The blue stripe cutting through the lower half
        stripe = Rectangle(width=scorm_text.width * 1.05, height=0.45, color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        stripe.move_to(scorm_text.get_center() + DOWN * 0.35)
        
        # Fix overlapping: stripe behind text
        stripe.set_z_index(1)
        scorm_text.set_z_index(2)
        
        main_logo = VGroup(stripe, scorm_text)
        main_logo.scale(0.001) # Start invisible for pop-in
        self.add(main_logo)
        
        # ── BUBBLES ──────────────────────────────────────────────────────
        # Ellipsis bubble (small, light grey) top left
        # Scaled down significantly to avoid overlap
        ellipsis_bg = RoundedRectangle(width=1.0, height=0.6, corner_radius=0.3, fill_color=ManimColor("#FFFFFF"), stroke_color=ManimColor("#1a1a2e"), stroke_width=2.5)
        # Pointing to the bottom right
        ellipsis_tail = Polygon([0.1, -0.2, 0], [0.3, -0.5, 0], [0.2, -0.2, 0], fill_color=ManimColor("#FFFFFF"), stroke_color=ManimColor("#1a1a2e"), stroke_width=2.5)
        
        # To mask the tail stroke running into the bubble:
        mask = Line([0.12, -0.3, 0], [0.18, -0.3, 0], color=WHITE, stroke_width=3)
        
        ellipsis_dots = VGroup(*[Circle(radius=0.035, fill_color=ManimColor("#1a1a2e"), fill_opacity=1, stroke_width=0) for _ in range(3)])
        ellipsis_dots.arrange(RIGHT, buff=0.08)
        # Make middle dot red per the screenshot
        ellipsis_dots[1].set_fill(ManimColor("#FF4D4D"))
        ellipsis_dots.move_to(ellipsis_bg.get_center())
        
        ellipsis_bubble = VGroup(ellipsis_bg, ellipsis_tail, mask, ellipsis_dots)
        # Shifted to the left corner exactly over 'S'
        # scorm_text.get_top() is the center top. scorm_text is 'SCORM'. The 'S' is on the far left.
        ellipsis_bubble.move_to(scorm_text.get_top() + UP * 1.4 + LEFT * 2.8)
        ellipsis_bubble.scale(0.001)
        self.add(ellipsis_bubble)
        
        # Main question bubble 1
        # Shrunk down and text size reduced heavily to fully avoid overlap
        q_bg_1 = RoundedRectangle(width=4.5, height=1.3, corner_radius=0.65, fill_color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        q_tail_1 = Polygon([-0.1, -0.5, 0], [-0.3, -0.9, 0], [0.1, -0.6, 0], fill_color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        q_text_1 = MarkupText("Can you create\n<b>SCORM</b> courses?", font_size=21, color=WHITE)
        q_text_1.move_to(q_bg_1.get_center())
        
        q_bubble_1 = VGroup(q_bg_1, q_tail_1, q_text_1)
        q_bubble_1.move_to(scorm_text.get_top() + UP * 1.5 + RIGHT * 1.2)
        
        # Store center to lock scaled and flipped replacements to exactly the same axis
        q_bubble_center = q_bubble_1.get_center()
        q_bubble_1.scale(0.001)
        self.add(q_bubble_1)
        
        # Main question bubble 2 (Replacement for rotation animation)
        # Uses exact same dimensions but updated text
        q_bg_2 = RoundedRectangle(width=4.6, height=1.3, corner_radius=0.65, fill_color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        q_tail_2 = Polygon([-0.1, -0.5, 0], [-0.3, -0.9, 0], [0.1, -0.6, 0], fill_color=ManimColor("#1565E0"), fill_opacity=1, stroke_width=0)
        q_text_2 = MarkupText("How can I create\n<b>SCORM</b> courses?!", font_size=21, color=WHITE)
        q_text_2.move_to(q_bg_2.get_center())
        
        q_bubble_2 = VGroup(q_bg_2, q_tail_2, q_text_2)
        q_bubble_2.move_to(q_bubble_center)
        # Pre-rotate it initially off camera so it can untwist as it scales in
        q_bubble_2.rotate(-35 * DEGREES).scale(0.001)
        self.add(q_bubble_2)
        
        # ── ANIMATION SEQUENCE ───────────────────────────────────────────
        self.wait(0.5)
        
        # Pop in SCORM logo
        self.play(
            main_logo.animate.scale(1000).set_rate_func(rate_functions.ease_out_elastic),
            run_time=0.9
        )
        self.wait(0.6)
        
        # Pop in ellipsis
        self.play(
            ellipsis_bubble.animate.scale(1000).set_rate_func(rate_functions.ease_out_elastic),
            run_time=0.7
        )
        self.wait(0.8)
        
        # Remove ellipsis
        self.play(
            ellipsis_bubble.animate.scale(0.001),
            run_time=0.2
        )
        self.remove(ellipsis_bubble)
        self.wait(0.2)
        
        # Pop in main question 1
        self.play(
            q_bubble_1.animate.scale(1000).set_rate_func(rate_functions.ease_out_elastic),
            run_time=0.8
        )
        self.wait(1.5)
        
        # ── HIGH SPEED BUBBLE FLIP ANIMATION ─────────────────────────────
        # The first bubble violently flies out and spins like a shrinking balloon
        self.play(
            q_bubble_1.animate.scale(0.001).rotate(35 * DEGREES),
            run_time=0.25,
            rate_func=rate_functions.ease_in_cubic
        )
        
        self.remove(q_bubble_1)
        
        # The second bubble immediately explodes into frame while unspinning
        self.play(
            q_bubble_2.animate.scale(1000).rotate(35 * DEGREES), 
            run_time=0.35,
            rate_func=rate_functions.ease_out_elastic
        )
        
        self.wait(2.0)
        
        # ── EXIT ANIMATION ───────────────────────────────────────────────
        # First, dialogue box expands, rotates 60 degrees, and fades out.
        self.play(
            q_bubble_2.animate.scale(3).rotate(-60 * DEGREES).set_opacity(0),
            run_time=0.6,
            rate_func=rate_functions.ease_in_cubic
        )
        self.remove(q_bubble_2)
        
        # Afterwards, the logo and particles move left and exit the frame.
        self.play(
            scorm_text.animate.shift(LEFT * 15),
            stripe.animate.shift(LEFT * 5),
            particles.animate.shift(LEFT * 15),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_cubic
        )
        
        self.wait(0.5)

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

    scene_to_render = IntroScene()
    scene_to_render.render()

    file_dir = Path(r"../../../gold_pattern_test_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "scorm_0_5.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")