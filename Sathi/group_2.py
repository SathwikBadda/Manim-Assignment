from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap

import os

class FinalScene(MovingCameraScene):
    def construct(self):
        # ==========================================
        # GLOBAL CONFIGURATION & UI
        # ==========================================
        self.camera.background_color = "#E0F7FA"
        
        card_width = config.frame_width * 0.11  # Reduced card width
        card_height = card_width * 1.25         # Reduced card height

        # --- STATIC HEADER ---
        header_rect = Rectangle(width=config.frame_width, height=1.2, color="#00ACC1", fill_opacity=1)
        header_rect.to_edge(UP, buff=0)
        
        # --- PROCEDURAL FOOTER (Notebook Look) ---
        footer_colors = [RED_D, ORANGE, YELLOW, GREEN_D, BLUE_D, PURPLE_D]
        footer_group = VGroup()
        
        num_circles = int(config.frame_width / 0.4) + 2
        
        for i in range(num_circles):
            c = Circle(radius=0.18, color=WHITE, fill_color=footer_colors[i % len(footer_colors)], fill_opacity=1, stroke_width=4)
            hole = Circle(radius=0.06, color=WHITE, fill_color="#E0F7FA", fill_opacity=1, stroke_width=0)
            footer_group.add(VGroup(c, hole))
            
        footer_group.arrange(RIGHT, buff=0.1)
        footer_group.to_edge(DOWN, buff=0.2)
        
        # Add static UI elements
        self.add(header_rect, footer_group)

        # ==========================================
        # SECTION 1
        # ==========================================
        ## Section 1
        
        # Create and position heading "Let's Practice!" (smaller, inside blue border)
        heading_1 = Text(
            "Let's Practice!",
            font="Comic Sans MS",
            weight=BOLD,
            font_size=38,
            color="#61D262"
        )
        # Move text inside blue border, centered vertically and horizontally
        heading_1.move_to(header_rect.get_center())
        self.add(heading_1)
        self.wait(0.8)
        self.remove(heading_1)

        # ==========================================
        # SECTION 2
        # ==========================================
        ## Section 2
        
        # Create heading "Complete the Train!" (smaller, inside blue border)
        heading_2 = Text(
            "Complete the Train!",
            font="Comic Sans MS",
            weight=BOLD,
            font_size=38,
            color="#EF9515"
        )
        # Move text inside blue border, centered vertically and horizontally
        heading_2.move_to(header_rect.get_center())
        self.add(heading_2)
        self.wait(3.93)
        self.remove(heading_2)

        # ==========================================
        # SECTION 3
        # ==========================================
        ## Section 3
        
        # ==========================================
        # SECTION 3: Train Assembly & Movement
        # ==========================================
        ## Section 3
        
        # 1. Create Train Engine
        train_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/Sathi/train.png")
        train_img.set_height(1.4)
        
        # 2. Create Coaches
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        coaches_list = []
        
        # Spacing constants
        unit_spacing = 2.2 # Distance between centers
        
        for i in range(7):
            # Coach body
            coach = RoundedRectangle(
                corner_radius=0.15,
                width=card_width,
                height=card_height,
                color=BLACK,
                stroke_width=3,
                fill_color="#FFFFFF",
                fill_opacity=1
            )
            
            # Wheels
            w_radius = card_width * 0.18
            wheel_left = Circle(radius=w_radius, color=BLACK, fill_opacity=1, stroke_width=2)
            wheel_right = Circle(radius=w_radius, color=BLACK, fill_opacity=1, stroke_width=2)
            wheel_left.move_to(coach.get_bottom() + LEFT * (card_width * 0.25) + DOWN * 0.1)
            wheel_right.move_to(coach.get_bottom() + RIGHT * (card_width * 0.25) + DOWN * 0.1)
            
            # Text fitting
            label_text = days_of_week[i] if i % 2 == 0 else "?"
            label_color = "#61D262" if i % 2 == 0 else BLACK
            f_size = 24 if i % 2 == 0 else 36 # Larger for ? but constrained
            label = Text(label_text, font="Comic Sans MS", weight=BOLD, font_size=f_size, color=label_color)
            
            # Constraint: Ensure label fits inside
            if label.width > card_width * 0.85:
                label.set_width(card_width * 0.85)
            if label.height > card_height * 0.8:
                label.set_height(card_height * 0.8)
            label.move_to(coach.get_center())
            
            # Assembly: coach, wheel_left, wheel_right, label (NO coupler here, use separate loop)
            coach_group = Group(coach, wheel_left, wheel_right, label)
            coaches_list.append(coach_group)

        # 3. Assemble the Full Train (Engine -> Day 0 -> Day 1 ...)
        # Engine is lead (front), so it's the rightmost.
        # Significantly increase engine height (nearly double coach height)
        train_img.set_height(card_height * 1.8) 
        train_img.move_to(ORIGIN)
        
        # We'll use a Group to arrange them
        # units[0] is Engine, units[1] (Monday) ... units[7] (Sunday)
        units = Group(train_img, *coaches_list)
        # Arrange with buffer for couplers
        units.arrange(LEFT, buff=0.4) 
        
        # Precisely align Engine visual wheels with Coach wheels
        # Coach bottom rect is at center.y - card_height/2.
        # Coach wheels are at center.y - card_height/2 - 0.1.
        # Visual wheel bottom is center.y - card_height/2 - 0.1 - w_radius.
        # Align engine image so its bottom (where its wheels are) matches that level.
        coach_rect = units[1][0]
        # First align image bottom to coach rect bottom
        train_img.align_to(coach_rect, DOWN)
        # Shift down by (0.1 + w_radius) to match coach wheel bottoms
        # (w_radius is card_width * 0.18, card_width is config.frame_width * 0.11)
        w_offset = 0.1 + (card_width * 0.18)
        train_img.shift(DOWN * w_offset)

        # Add Couplers between units - ensure they TOUCH the Rectangles/Engine
        couplers = Group()
        for i in range(len(units)-1):
            lead = units[i]
            follow = units[i+1] # This is a Group (coach_group)
            
            # Start from follow's coach body (index 0)
            f_rect = follow[0]
            
            # Target is lead's body or engine image
            if isinstance(lead, ImageMobject):
                # Engine lead - get its left boundary at the same Y as coach center
                l_target = lead.get_left()
                # Ensure the coupler is perfectly horizontal
                l_target[1] = f_rect.get_center()[1]
                # SLIGHT OVERLAP to ensure it touches (0.1 units)
                l_target += RIGHT * 0.1
            else:
                # Coach body's left edge (units[i][0])
                l_rect = lead[0]
                l_target = l_rect.get_left()
                l_target[1] = f_rect.get_center()[1]
                
            line = Line(f_rect.get_right(), l_target, color=BLACK, stroke_width=4)
            couplers.add(line)
        
        full_train = Group(units, couplers)
        
        # 4. Scale and Initial Position
        full_train.scale(0.7) # Scale down to fit frame
        
        # Start completely off-screen LEFT (Lower position)
        full_train.move_to(LEFT * 12 + DOWN * 1.5)
        self.add(full_train)

        # 5. Animation: Single Unit Move
        # Center the train roughly in the frame (Lower position)
        target_pos = RIGHT * 0.5 + DOWN * 1.5
        
        # Wheel rotation updater
        def rotate_wheels(mob, dt):
            # Find all circles in the train group (wheels)
            for sub in mob.family_members_with_points():
                if isinstance(sub, Circle) and sub.get_stroke_width() < 10: # Filter out couplers/others if any
                    sub.rotate(-6 * dt)

        full_train.add_updater(rotate_wheels)
        
        self.play(
            full_train.animate.move_to(target_pos),
            run_time=6,
            rate_func=linear
        )
        
        full_train.clear_updaters()
        self.wait(2.0)

        # Store references for later transform (Section 4)
        # full_train[0] is Group(Engine, Mon, Tue...)
        # full_train[0][1-7] are the coaches
        coaches_vgroup = Group(*[full_train[0][i] for i in range(1, 8)])
        question_marks = VGroup(*[coaches_vgroup[i][3] for i in range(1, 7, 2)])
        day_labels = VGroup(*[coaches_vgroup[i][3] for i in range(0, 7, 2)])
        self.wait(2.0)

        # ==========================================
        # SECTION 4
        # ==========================================
        ## Section 4
        
        # Reveal missing days with Transform and Flash
        reveal_anims = []
        
        # Create day labels for the question mark positions
        qmark_day_labels = VGroup()
        qmark_index = 0
        for i in range(7):
            if i % 2 != 0:
                # Use the SAME font size (24) as initial labels
                day_label = Text(days_of_week[i], font="Comic Sans MS", weight=BOLD, font_size=24, color="#61D262")
                # Apply same scaling constraints as in make_node (0.7 scale adjusted)
                # Note: internal coach is scaled by 0.7, so we must compensate or set width relative to actual coach
                target_coach = coaches_vgroup[i][0] # The RoundedRectangle
                if day_label.width > target_coach.width * 0.85:
                    day_label.set_width(target_coach.width * 0.85)
                
                day_label.move_to(question_marks[qmark_index].get_center())
                qmark_day_labels.add(day_label)
                qmark_index += 1
        
        # Build reveal animation sequence
        qmark_index = 0
        for i in range(7):
            if i % 2 != 0:
                reveal_anims.append(Transform(question_marks[qmark_index], qmark_day_labels[qmark_index]))
                reveal_anims.append(Flash(coaches_vgroup[i], color="#EF9515", flash_radius=card_width * 0.8))
                qmark_index += 1
        
        self.play(LaggedStart(*reveal_anims, lag_ratio=0.5), run_time=6.0)
        
        # Add wiggle animations to revealed text
        wiggle_anims = []
        qmark_index = 0
        for i in range(7):
            if i % 2 != 0:
                wiggle_anims.append(Wiggle(qmark_day_labels[qmark_index], scale_value=1.15))
                qmark_index += 1
        
        self.play(LaggedStart(*wiggle_anims, lag_ratio=0.3), run_time=2.14)

        # ==========================================
        # SECTION 5
        # ==========================================
        ## Section 5
        
        # Create sunburst effect
        rays = VGroup(*[AnnularSector(inner_radius=0, outer_radius=10, angle=TAU/40, start_angle=i*TAU/20, color="#EF9515", fill_opacity=0.4) for i in range(20)])
        rays.move_to(ORIGIN)
        
        # Create star
        star = Star(n=7, outer_radius=2.5, inner_radius=1.5, color="#EF9515", fill_opacity=1, stroke_color="#4280A7", stroke_width=5)
        star.move_to(ORIGIN)
        
        # Create congratulatory text
        great_job = Text("Great Job!", font="Comic Sans MS", weight=BOLD, font_size=80, color="#61D262")
        great_job.set_stroke("#4280A7", 3)
        great_job.move_to(ORIGIN)
        
        # Create supporting text
        keep_practicing = Text("Keep Practicing!", font="Comic Sans MS", weight=BOLD, font_size=40, color="#FFFFFF")
        keep_practicing.next_to(star, DOWN, buff=0.8)
        
        # Create confetti particles
        confetti = VGroup()
        confetti_colors = ["#61D262", "#EF9515", "#4280A7", "#FFFFFF"]
        for _ in range(50):
            c = Square(side_length=0.15, fill_color=random.choice(confetti_colors), fill_opacity=1, stroke_width=0)
            c.move_to(ORIGIN)
            confetti.add(c)
        
        # Animate sunburst and star growth
        self.play(FadeIn(rays), run_time=0.5)
        self.play(GrowFromCenter(star, rate_func=rate_functions.ease_out_elastic), run_time=1.0)
        self.play(GrowFromCenter(great_job, rate_func=rate_functions.ease_out_elastic), run_time=1.0)
        
        # Rotate rays and explode confetti
        confetti_anims = [c.animate.shift(np.array([random.uniform(-5, 5), random.uniform(-4, 4), 0])).rotate(random.uniform(0, TAU)) for c in confetti]
        
        self.play(
            LaggedStart(*confetti_anims, lag_ratio=0.05),
            Rotate(rays, angle=TAU, rate_func=linear),
            FadeIn(keep_practicing, shift=UP),
            run_time=4.8        )
        
        self.play(Rotate(rays, angle=TAU, rate_func=linear), run_time=3.19)

        # ==========================================
        # SECTION 6
        # ==========================================
        ## Section 6
        
        # Collect all active elements for fade-out
        # Collect all active elements for fade-out (Must be Group because it contains Groups)
        all_elements = Group(header_rect, footer_group, coaches_vgroup, day_labels, question_marks, qmark_day_labels, rays, star, great_job, keep_practicing, confetti)
        
        # Fade out all elements
        self.play(FadeOut(all_elements), run_time=9.24)
