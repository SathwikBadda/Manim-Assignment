from manim import *
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class FinalScene(ThreeDScene):
    def construct(self):
        config.frame_width = 14.22
        config.frame_height = 8.0
        
        bg_color = "#0F172A"
        primary_text = "#C6C7DC"
        secondary_text = "#A5B4FC"
        tertiary_text = "#94A3B8"
        data_accent = "#22D3EE"
        depth_layer = "#1E1B4B"
        
        self.camera.background_color = bg_color
        
        ## Section 1
        image_9 = ImageMobject("../images/image_9.png")
        image_9.move_to(ORIGIN)
        
        self.play(GrowFromCenter(image_9), run_time=1.0)
        self.wait(2.0)
        
        
        self.play(
            image_9.animate.move_to(np.array([0, 2.8, 0])),
            run_time=3.0
        )
        
        
        scale_anim = Succession(
            image_9.animate.scale(1.05),
            image_9.animate.scale(1.0/1.05),
            run_time=0.4
        )
        self.play(scale_anim, run_time=0.4)
        
        self.wait(0.71)
        
        ## Section 2
        labels_data = [
            ("School", -6.0),
            ("Undergraduate", -2.0),
            ("Postgraduate", 2.0),
            ("Corporate", 6.0)
        ]
        
        
        # Helper to make a card
        def make_card(text, width=2.8, height=1.2):
            bg = RoundedRectangle(
                corner_radius=0.15, width=width, height=height,
                fill_color=depth_layer, fill_opacity=1, 
                stroke_color=tertiary_text, stroke_width=1.5
            )
            lbl = Text(text, font="Georgia", font_size=22, color=primary_text)
            lbl.move_to(bg.get_center())
            return VGroup(bg, lbl)

        cards = VGroup()
        for text, x_pos in labels_data:
            card = make_card(text)
            # Initial position for layout calculation
            card.move_to(np.array([x_pos, -1.2, 0]))
            cards.add(card)
            
        # Connectors using CubicBezier
        connectors = VGroup()
        for i in range(len(cards) - 1):
            if i % 2 == 0:
                start_p = cards[i].get_bottom()
                end_p = cards[i+1].get_bottom()
                direction = DOWN
            else:
                start_p = cards[i].get_top()
                end_p = cards[i+1].get_top()
                direction = UP

            mid_p = (start_p + end_p) / 2 + direction * 0.8
            path = CubicBezier(start_p, mid_p, mid_p, end_p,
                               stroke_width=1.5, stroke_color=data_accent)
            dashed = DashedVMobject(path, num_dashes=12, dashed_ratio=0.5)
            connectors.add(dashed)

        # Animation Sequence
        
        # 1. First card animation
        first_card = cards[0]
        target_pos = first_card.get_center()
        
        # Move to center and scale up
        first_card.move_to(ORIGIN)
        first_card.scale(2.5)
        
        self.play(FadeIn(first_card), run_time=0.8)
        self.wait(0.2)
        
        self.play(
            first_card.animate.scale(0.4).move_to(target_pos),
            run_time=0.8, rate_func=smooth
        )

        # 2. Sequential build
        pipeline_anims = []
        for i in range(len(connectors)):
            anim_conn = Create(connectors[i], run_time=0.5)
            shift_vec = DOWN * 0.5 if i % 2 == 0 else UP * 0.5
            
            anim_card = FadeIn(
                cards[i+1],
                shift=shift_vec,
                scale=0.8,
                rate_func=rate_functions.ease_out_back,
                run_time=0.6
            )
            pipeline_anims.append(AnimationGroup(anim_conn, anim_card, lag_ratio=0.8))

        self.play(LaggedStart(*pipeline_anims, lag_ratio=0.8), run_time=3.0)

        # Compatibility aliases for downstream code
        labels = cards
        connecting_lines = connectors
        sequence_setup = VGroup(cards, connectors)

        # Transition to circular arrangement
        n = len(cards)
        circle_radius = 3.2
        circle_center = np.array([0.0, -0.1, 0])
        circle_positions = [
            circle_center + np.array([
                circle_radius * np.cos(PI / 2 + 2 * PI * i / n),
                circle_radius * np.sin(PI / 2 + 2 * PI * i / n),
                0
            ])
            for i in range(n)
        ]

        self.play(FadeOut(connectors), FadeOut(image_9), run_time=0.5)

        self.play(
            LaggedStart(
                *[cards[i].animate.move_to(circle_positions[i]) for i in range(n)],
                lag_ratio=0.15
            ),
            run_time=2.5, rate_func=smooth,
        )
        self.move_camera(frame_center=circle_center, zoom=4.0, run_time=1.5)

        self.play(FadeOut(cards),run_time=0.5)
        self.move_camera(frame_center=ORIGIN,zoom=1.0,run_time=0.5)
        
        image_icons = [
            ImageMobject("../images/image_10.png"),
            ImageMobject("../images/image_11.png"),
            ImageMobject("../images/image_12.png"),
            ImageMobject("../images/image_13.png")
        ]
        
        support_texts_data = [
            ("Entry Assessment", -3.3),
            ("Exit Assessment", -1.1),
            ("Foundational Literacy", 1.1),
            ("Skill Gap Analysis", 3.3)
        ]
        
        support_texts = []
        for text, x_pos in support_texts_data:
            support = Text(text, font="Times New Roman", font_size=26, color=secondary_text).scale(0.9)
            support_texts.append(support)

        icon_text_anims = []
        start_y = 2.5
        y_gap = 1.5
        icon_x = -2.0
        
        for i, (icon, (_, x_pos)) in enumerate(zip(image_icons, labels_data)):
            target_y = start_y - i * y_gap
            target_icon_pos = np.array([icon_x, target_y, 0])
            icon.save_state()
            icon.move_to(target_icon_pos + RIGHT * 0.5)
            icon.scale(0.01)
            
            text_obj = support_texts[i]
            target_text_pos = np.array([icon_x + 2.5, target_y, 0])
            text_obj.move_to(target_text_pos + UP * 0.2)
            text_obj.set_opacity(0)
            
            icon_text_anims.append(AnimationGroup(
                icon.animate.restore().move_to(target_icon_pos).scale(0.4),
                text_obj.animate.move_to(target_text_pos).set_opacity(0.65),
                lag_ratio=0.5
            ))
        
        self.play(LaggedStart(*icon_text_anims, lag_ratio=0.2), run_time=2.0)
        
        pathway_group = Group(*image_icons, *support_texts)

        # 1. Text items fadeout and move down
        self.play(
            *[text.animate.shift(DOWN * 0.5).fade(1) for text in support_texts],
            run_time=1.0
        )

        # 2. Sequence setup moves out from bottom
        

        # 3. Icons orbit setup
        right_center = LEFT * 3.5 + DOWN * 0.5
        radius_x_tracker = ValueTracker(2.5)
        radius_y_tracker = ValueTracker(2.5)
        orbit_scale_tracker = ValueTracker(1.0)

        t_start = [0.0]
        ROTATION_SPEED = 1.5
        
        base_angles = [0, PI/2, PI, 3*PI/2]

        icon_anims = []
        for i, icon in enumerate(image_icons):
            angle = base_angles[i]
            target_pos = right_center + np.array([2.5 * np.cos(angle), 2.5 * np.sin(angle), 0])
            icon_anims.append(icon.animate.move_to(target_pos).scale_to_fit_width(1.5))
            
        self.play(*icon_anims, run_time=1.0)
        
        t_start[0] = self.renderer.time

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
                
                tilt_factor = np.clip((1.0 - tilt_ratio) / (1.0 - 1.5/4.0), 0, 1)
                depth_frac = (unscaled_y + ry) / (2 * ry) if ry > 0 else 0.5
                
                target_scale = 1.0 + (0.8 - 1.5 * depth_frac) * tilt_factor
                
                mob.width = 1.5 * target_scale * scale_mult

                mob.set_z_index(int(-unscaled_y * 10))
            return updater
            
        base_angles = [PI/2, 0, 3*PI/2, PI]
        
        for node, ba in zip(image_icons, base_angles):
            node.add_updater(make_icon_updater(node, ba))
            
        self.play(
            radius_y_tracker.animate.set_value(1.5),
            run_time=3.0,
            rate_func=rate_functions.ease_in_cubic
        )
        
        # Sphere setup
        sphere = VGroup()
        sphere_radius = 2.0
        
        # Longitudes
        for i in range(0, 180, 15):
            sphere.add(Circle(radius=sphere_radius, color=data_accent, stroke_width=1.5).rotate(i*DEGREES, axis=UP))
        # Latitudes
        for i in range(1, 8): 
            h = -sphere_radius + i * (2*sphere_radius/8)
            r = np.sqrt(sphere_radius**2 - h**2)
            sphere.add(Circle(radius=r, color=data_accent, stroke_width=1.5).rotate(90*DEGREES, axis=RIGHT).shift(UP*h))
            
        sphere.move_to(right_center)
        sphere.set_z_index(5)
        
    
        # ── Phase 2: icons blast outward while sphere lines draw themselves ──
        for icon in image_icons:
            icon.clear_updaters()

        # Create glowing spark copies at current icon positions
        sparks = VGroup()
        for icon in image_icons:
            spark = Circle(
                radius=0.35,
                color=data_accent,
                stroke_width=3,
                fill_opacity=0
            ).move_to(icon.get_center())
            sparks.add(spark)
        self.add(sparks)

        # Animate phase: icons burst outward + fade, sparks pulse, sphere lines draw
        burst_anims = []
        for i, icon in enumerate(image_icons):
            angle = base_angles[i]
            burst_pos = right_center + np.array([
                3.5 * np.cos(angle), 3.5 * np.sin(angle), 0
            ])
            burst_anims.append(
                AnimationGroup(
                    icon.animate.move_to(burst_pos).set_opacity(0),
                    rate_func=rate_functions.ease_in_expo,
                )
            )

        spark_anims = [
            spark.animate.scale(3).set_opacity(0)
            for spark in sparks
        ]

        self.play(
            *burst_anims,
            *spark_anims,
            LaggedStart(*[Create(line) for line in sphere], lag_ratio=0.04),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_cubic
        )

        for icon in image_icons:
            self.remove(icon)
        self.remove(sparks)
            
        # Sphere rotation (slowing down)
        self.play(
            Rotate(sphere, angle=TAU, axis=UP, rate_func=rate_functions.ease_out_expo),
            run_time=2.0
        )

        # Section 3
        pathway_group.remove(*image_icons)
        self.play(pathway_group.animate.set_opacity(0.5), run_time=0.5)
        
        panel = RoundedRectangle(
            width=8.0,
            height=28.0,
            corner_radius=0.1,
            stroke_width=0.8,
            stroke_color=tertiary_text,
            fill_color=depth_layer,
            fill_opacity=1.0
        )
        panel.move_to(RIGHT * 4.0 + DOWN * 5.0)
        
        self.play(DrawBorderThenFill(panel), run_time=1.0)
        
        heading = Text("Designed by Global Leaders", font="Georgia", font_size=20, 
                      color=primary_text, weight=BOLD).scale(0.7)
        heading.move_to(panel.get_top() + DOWN * 0.8)
        
        self.play(
            AddTextLetterByLetter(heading),
            heading.animate.scale(1.0/0.7),
            FadeIn(heading),
            run_time=0.8
        )
        
        # Data Definition for the 3 columns
        india_higher_ed = [
            ("Manish Kumar", "IAS, Former\nCEO, NSDC"),
            ("Prof. Janat Shah", "IIM Udaipur"),
            ("Dr. Pramath Sinha", "Ashoka University"),
            ("Prof. S Sadagopan", "IIIT Bangalore"),
            ("Prashant Bhalla", "Board member,\nEPSI"),
            ("Amit Dasgupta, IFS", "(Retd) Former Indian\nCounsel in Sydney"),
            ("Madan Padaki", "Entrepreneur,\nCo-founder, MeritTrack"),
            ("Mahesh Peri", "Careers 360"),
            ("Prof. Dinesh Singh", "VC, Higher Education\nCouncil, J&K"),
            ("Dr. Sadhana Parashar", "Ex-Senior\nDirector, NTA"),
            ("Bimal Rath", "Think Talent Services"),
            ("Sridhar Rajagopalan", "Educational\nInitiatives"),
            ("Venu Rajamony, IFS", "Former Diplomat &\nPress Sec. to President")
        ]
        
        india_schools = [
            ("Ashok Pandey", "Principal/Director,\nAhlcon International"),
            ("Lt. Gen. S. Kulkarni", "Ex-Director,\nMayo College, Ajmer"),
            ("Ajay Singh", "Principal,\nScindia School"),
            ("S. Sriram", "Principal,\nThe Mann School")
        ]
        
        global_leaders = [
            ("Raanan Haas", "Occ. Psychologist,\nIsrael"),
            ("Yonatan Glaser", "Founder & CEO,\nIsrael Partnerships"),
            ("Kadriye Ercikan", "ETS Global\nResearch, USA"),
            ("Mathew Johnson", "ETS Global\nResearch, USA"),
            ("Liu Lydia", "ETS Global\nResearch, USA"),
            ("Ajay Shukla", "IIT Delhi\nAbu Dhabi"),
            ("Dhanjay Jhurry", "Uniciti Education\nHub, Mauritius"),
            ("Dr. Peninah Aloo", "Masai Mara\nUniversity, Kenya"),
            ("Rahul Govind", "UNSW,\nAustralia"),
            ("Prof. Piyush Sharma", "Curtin Business\nSchool, Australia"),
            ("Dr. Fanta Aw", "CEO at\nNAFSA, US"),
            ("Dr. Eesa M. Bastaki", "Former CEO,\nICT Fund")
        ]

        def generate_grid_group(title_text_str, data_list, num_cols=3):
            group = VGroup()
            dummy_origin = VectorizedPoint(ORIGIN)
            group.add(dummy_origin)
            
            title = Text(title_text_str, font="Georgia", font_size=16, color=secondary_text, weight=BOLD)
            title.move_to(ORIGIN)
            group.add(title)
            
            grid_group = VGroup()
            col_width = 7.4 / num_cols
            row_height = 0.8
            for i, (name, desc) in enumerate(data_list):
                col = i % num_cols
                row = i // num_cols
                x_left = col * col_width - (num_cols * col_width / 2)
                y = -row * row_height
                
                n_text = Text(name, font="Times New Roman", font_size=12, color=primary_text, weight=BOLD)
                d_text = Text(desc, font="Times New Roman", font_size=10, color=tertiary_text)
                d_text.next_to(n_text, DOWN, buff=0.1, aligned_edge=LEFT)
                
                item_group = VGroup(n_text, d_text)
                item_group.move_to(np.array([x_left, y, 0]), aligned_edge=LEFT)
                grid_group.add(item_group)
            
            grid_group.next_to(title, DOWN, buff=0.6)
            grid_group.set_x(0) # center grid horizontally with respect to origin dummy
            group.add(grid_group)
            return group

        he_group = generate_grid_group("India – HigherED", india_higher_ed, 3)
        sch_group = generate_grid_group("India - Schools", india_schools, 3)
        glob_group = generate_grid_group("Global", global_leaders, 3)
        
        # Stack them vertically
        he_group.move_to(panel.get_top() + DOWN * 2.8, coor_mask=np.array([0,1,0]))
        sch_group.next_to(he_group, DOWN, buff=1.0, coor_mask=np.array([0,1,0]))
        glob_group.next_to(sch_group, DOWN, buff=1.0, coor_mask=np.array([0,1,0]))
        
        # Align perfectly to panel's horizontal center using the dummy origin
        for grp in [he_group, sch_group, glob_group]:
            dx = panel.get_center()[0] - grp[0].get_center()[0]
            grp.shift(RIGHT * dx)
        
        # Hide everything initially for camera logic sequence
        he_group.set_opacity(0)
        sch_group.set_opacity(0)
        glob_group.set_opacity(0)
        
        dashboard_content = VGroup(he_group, sch_group, glob_group)
        self.add(dashboard_content)

        # 1. Pan to India Higher Ed
        self.move_camera(
            frame_center=he_group.get_center(),
            zoom=1.4,
            run_time=2.0
        )
        self.play(he_group.animate.set_opacity(1.0), run_time=1.5)
        self.wait(1.0)
        
        # 2. Pan to India Schools
        self.move_camera(
            frame_center=sch_group.get_center(),
            zoom=1.4,
            run_time=1.5
        )
        self.play(sch_group.animate.set_opacity(1.0), run_time=1.0)
        self.wait(1.0)
        
        # 3. Pan to Global
        self.move_camera(
            frame_center=glob_group.get_center(),
            zoom=1.4,
            run_time=1.5
        )
        self.play(glob_group.animate.set_opacity(1.0), run_time=1.0)
        self.wait(1.0)
        
        # Complete full exit of dashboard logic as requested before moving to Section 4
        full_dashboard_group = Group(panel, heading, dashboard_content, sphere, pathway_group)
        
        # Note: We exit directly from pan without a zoom out phase.
        self.play(
            FadeOut(full_dashboard_group, shift=DOWN * 15),
            run_time=1.5,
            rate_func=rate_functions.ease_in_cubic
        )
        
        # We restore camera natively so Section 4 math isn't broken
        self.move_camera(
            frame_center=ORIGIN,
            zoom=1.0,
            run_time=0.1
        )
        self.remove(full_dashboard_group)
        
        ## Section 4
        

        # ------------------------------------------------------------
        # Camera pan (unchanged)
        # ------------------------------------------------------------
        self.move_camera(
            frame_center=self.camera.frame_center + RIGHT * 12,
            run_time=3
        )

        # ------------------------------------------------------------
        # Vertical Difficulty Bar Setup
        # ------------------------------------------------------------
        bar_width = 2.2
        bar_height = 6.0

        bar = Rectangle(
            width=bar_width,
            height=bar_height,
            stroke_color=data_accent,
            stroke_width=2
        )

        bar.move_to(self.camera.frame_center)

        # Start collapsed at bottom for growth animation
        bar_bottom = self.camera.frame_center + LEFT * 2.0 + DOWN * (bar_height / 2)
        bar.stretch_to_fit_height(0.01)
        bar.move_to(bar_bottom, aligned_edge=DOWN)

        # ------------------------------------------------------------
        # Animate Bar Growing Upward
        # ------------------------------------------------------------
        self.play(
            bar.animate.stretch_to_fit_height(bar_height).move_to(self.camera.frame_center+ LEFT * 2.0),
            run_time=1.2,
            rate_func = smooth
        )

        # ------------------------------------------------------------
        # Section Ratios (Natural Bar Feel)
        # ------------------------------------------------------------
        easy_ratio = 0.25
        medium_ratio = 0.45
        hard_ratio = 0.30

        easy_height = bar_height * easy_ratio
        medium_height = bar_height * medium_ratio
        hard_height = bar_height * hard_ratio

        bottom_y = - bar_height / 2
        easy_top = bottom_y + easy_height
        medium_top = easy_top + medium_height
        hard_top = medium_top + hard_height

        # ------------------------------------------------------------
        # Divider Lines
        # ------------------------------------------------------------
        divider_1 = Line(
            [bar.get_center()[0] - bar_width/2, bar.get_center()[1] + easy_top, 0],
            [bar.get_center()[0] + bar_width/2, bar.get_center()[1] + easy_top, 0],
            stroke_width=1,
            color=tertiary_text
        )

        divider_2 = Line(
            [bar.get_center()[0] - bar_width/2, bar.get_center()[1] + medium_top, 0],
            [bar.get_center()[0] + bar_width/2, bar.get_center()[1] + medium_top, 0],
            stroke_width=1,
            color=tertiary_text
        )

        self.play(Create(divider_1), Create(divider_2), run_time=0.6)

        # ------------------------------------------------------------
        # Dense Dot Cluster Generator
        # ------------------------------------------------------------
        def generate_cluster(y_min, y_max, density, fill_color_passed):
            dots = VGroup()
            x_min = bar.get_center()[0]-bar_width/2 + 0.2
            x_max = bar.get_center()[0]+bar_width/2 - 0.2

            for _ in range(density):
                x = np.random.uniform(x_min, x_max)
                y = np.random.uniform(y_min, y_max)

                dot = Circle(
                    radius=0.07,
                    fill_color=fill_color_passed,
                    fill_opacity=1,
                    stroke_width=0
                )
                dot.move_to([x, y, 0])
                dots.add(dot)

            return dots

        easy_cluster = generate_cluster(bar.get_center()[1]+bottom_y, bar.get_center()[1]+easy_top, 18, RED)
        medium_cluster = generate_cluster(bar.get_center()[1]+easy_top, bar.get_center()[1]+medium_top, 55, YELLOW)
        hard_cluster = generate_cluster(bar.get_center()[1]+medium_top, bar.get_center()[1]+hard_top, 28, GREEN)

        # ------------------------------------------------------------
        # Animate Dot Clusters (Staggered Reveal)
        # ------------------------------------------------------------
        self.play(
            LaggedStart(
                FadeIn(easy_cluster),
                FadeIn(medium_cluster),
                FadeIn(hard_cluster),
                lag_ratio=0.25
            ),
            run_time=1.5
        )

        # ------------------------------------------------------------
        # Side Labels
        # ------------------------------------------------------------
        easy_label = Text("Easy", font="Times New Roman", font_size=20, color=secondary_text)
        medium_label = Text("Medium", font="Times New Roman", font_size=20, color=secondary_text)
        hard_label = Text("Hard", font="Times New Roman", font_size=20, color=secondary_text)

        easy_label.next_to([bar.get_center()[0] + bar_width/2, bar.get_center()[1] + bottom_y + easy_height/2, 0], RIGHT, buff=0.6)
        medium_label.next_to([bar.get_center()[0] + bar_width/2, bar.get_center()[1] + easy_top + medium_height/2, 0], RIGHT, buff=0.6)
        hard_label.next_to([bar.get_center()[0] + bar_width/2, bar.get_center()[1] + medium_top + hard_height/2, 0], RIGHT, buff=0.6)

        self.play(
            FadeIn(easy_label),
            FadeIn(medium_label),
            FadeIn(hard_label),
            run_time=0.8
        )

        difficulty_progression = Text("Consistent Difficulty Progression", font="Times New Roman", font_size=28, color=secondary_text).next_to(medium_label,RIGHT,buff=0.4)

        self.play(
            FadeIn(difficulty_progression,shift = DOWN*0.5),
            run_time=0.8
        )


        # ------------------------------------------------------------
        # 1️⃣ Shrink Existing Text From Center
        # ------------------------------------------------------------

        all_text = VGroup(easy_label, medium_label, hard_label,difficulty_progression)

        self.play(
            LaggedStart(
                *[t.animate.scale(0.01) for t in all_text],
                lag_ratio=0.1
            ),
            run_time=0.5
        )

        self.remove(all_text)


        # ------------------------------------------------------------
        # 2️⃣ Topple Bar To The Right (Rotate 90°)
        # ------------------------------------------------------------

        bar_group = VGroup(
            bar,
            divider_1,
            divider_2,
            easy_cluster,
            medium_cluster,
            hard_cluster
        )

        self.play(
            Rotate(bar_group, -PI/2, about_point=bar.get_corner(DOWN+RIGHT)),
            run_time=1.2,
            rate_func=smooth
        )


        # ------------------------------------------------------------
        # 3️⃣ Transform Into Circular Shape + 2 K-Means Clusters
        # ------------------------------------------------------------

        # Target circle boundary
        circle_boundary = Circle(
            radius=2.5,
            stroke_color=data_accent,
            stroke_width=2
        ).move_to(self.camera.frame_center)

        # Generate dense circular clusters
        def circular_cluster(center, radius, n, color):
            dots = VGroup()
            for _ in range(n):
                r = radius * np.sqrt(np.random.uniform(0, 1))
                theta = np.random.uniform(0, TAU)
                x = center[0] + r * np.cos(theta)
                y = center[1] + r * np.sin(theta)

                dot = Circle(
                    radius=0.07,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=0
                )
                dot.move_to([x, y, 0])
                dots.add(dot)
            return dots


        cluster_1 = circular_cluster(self.camera.frame_center + LEFT * 1.2, 0.9, 18, RED)
        cluster_2 = circular_cluster(self.camera.frame_center, 1.2, 55, YELLOW)
        cluster_3 = circular_cluster(self.camera.frame_center + RIGHT * 1.2, 0.9, 28, GREEN)

        circle_group = VGroup(
            circle_boundary,
            VectorizedPoint(self.camera.frame_center).set_opacity(0),
            VectorizedPoint(self.camera.frame_center).set_opacity(0),
            cluster_1,
            cluster_2,
            cluster_3
        )

        self.play(
            Transform(bar_group, circle_group),
            run_time=1.5,
            rate_func=smooth
        )

        self.remove(bar_group)
        self.add(circle_group)


        # ------------------------------------------------------------
        # 4️⃣ Circular Text Layout Around Shape
        # ------------------------------------------------------------

        texts = [
            "Domain Analysis",
            "Behavioral Clustering",
            "Scalability Validations"
        ]

        text_mobjects = VGroup()

        radius = 3.5
        angles = [PI/2, -PI/6, -5*PI/6]
        center = circle_boundary.get_center()

        for txt, angle in zip(texts, angles):
            t = Text(
                txt,
                font="Georgia",
                font_size=26,
                color=secondary_text
            )

            # Start off-screen
            t.move_to(
                center + np.array([
                    8 * np.cos(angle),
                    8 * np.sin(angle),
                    0
                ])
            )

            text_mobjects.add(t)

        self.add(text_mobjects)

        # Animate to circular positions
        self.play(
            *[
                text_mobjects[i].animate.move_to(
                    center + np.array([
                        radius * np.cos(angles[i]),
                        radius * np.sin(angles[i]),
                        0
                    ])
                )
                for i in range(len(text_mobjects))
            ],
            run_time=1.5,
            rate_func=smooth
        )

        ## Section 5
        # ROOT CAUSE: ANY move_camera() call in ThreeDScene permanently breaks
        # ImageMobject rendering. SOLUTION: Reset camera to ORIGIN first, then
        # add images at fixed ORIGIN-relative coordinates. Scroll via group.shift(UP).

        # Step 1: Reset camera to ORIGIN — images render correctly after this
        self.move_camera(frame_center=ORIGIN, zoom=1.0, run_time=0.5)
        self.play(FadeOut(circle_group), FadeOut(text_mobjects), run_time=0.6)

        # ── Grid layout constants (matching test.py) ──────────────────────
        NUM_COLS    = 4
        CELL_W      = 2.2
        CELL_H      = 1.4
        CELL_GAP    = 0.25
        STEP_X      = CELL_W + CELL_GAP
        STEP_Y      = CELL_H + CELL_GAP + 0.35
        total_row_w = NUM_COLS * CELL_W + (NUM_COLS - 1) * CELL_GAP

        PANEL_TOP_Y  = 3.8
        PANEL_WIDTH  = 13.0
        # NOTE: PANEL_HEIGHT is computed dynamically AFTER image counts are known
        # — placeholder value used here, overwritten below once counts are loaded
        _grid1_rows = int(np.ceil(17 / NUM_COLS))   # 5 rows for up to 17 imgs
        _grid2_rows_est = 10                          # overwritten dynamically below
        PANEL_HEIGHT = (
            0.9 + 0.5 +
            _grid1_rows * STEP_Y +
            1.5 +
            0.9 + 0.5 +
            _grid2_rows_est * STEP_Y +
            0.5
        ) + 0.5

        # Step 2: Build panel at ORIGIN-relative coordinates
        long_panel = Rectangle(
            width=PANEL_WIDTH, height=PANEL_HEIGHT,
            fill_color=depth_layer, fill_opacity=1.0,
            stroke_color=tertiary_text, stroke_width=1.5
        )
        long_panel.move_to(np.array([0, PANEL_TOP_Y - PANEL_HEIGHT/2, 0]))
        long_panel.set_z_index(0)

        # Heading 1
        heading_1 = Text(
            "Institutions in Engagement",
            font="Georgia", font_size=32,
            color=primary_text, weight=BOLD
        )
        heading_1.move_to(np.array([0, PANEL_TOP_Y - 0.9, 0]))
        heading_1.set_z_index(5)

        # ── Load institution images (same logic as test.py) ───────────────
        from pathlib import Path as _Path
        image_dir = _Path("../images/Institutions")
        image_files = sorted(
            list(image_dir.glob("*.jpg")) +
            list(image_dir.glob("*.png")) +
            list(image_dir.glob("*.jpeg")),
            key=lambda f: int("".join(filter(str.isdigit, f.name)) or "0")
        )
        total_items = min(17, len(image_files))

        grid1_start_y = PANEL_TOP_Y - 0.9 - 0.5 - CELL_H/2

        all_cards = []
        all_imgs  = []

        for i in range(total_items):
            col = i % NUM_COLS
            row = i // NUM_COLS
            cx  = -total_row_w/2 + col*STEP_X + CELL_W/2
            cy  = grid1_start_y - row*STEP_Y

            # White card backing (same as test.py)
            card = RoundedRectangle(
                width=CELL_W, height=CELL_H,
                corner_radius=0.12,
                stroke_width=0,
                fill_color=WHITE,
                fill_opacity=1.0
            )
            card.move_to(np.array([cx, cy, 0]))
            card.set_z_index(20)
            all_cards.append(card)

            # Image (same scaling logic as test.py)
            try:
                img = ImageMobject(str(image_files[i]))
                scale = min(CELL_W*0.85 / img.width, CELL_H*0.85 / img.height)
                img.scale(scale)
            except Exception:
                img = Text(image_files[i].stem[:12], font="Georgia",
                           font_size=14, color="#222222")
            img.move_to(np.array([cx, cy, 0]))
            img.set_z_index(21)
            all_imgs.append(img)

        # Heading 2
        num_rows_grid1 = int(np.ceil(total_items / NUM_COLS))
        grid1_bottom_y = grid1_start_y - (num_rows_grid1 - 1)*STEP_Y - CELL_H/2

        heading_2 = Text(
            "Institutions in Advanced Engagement",
            font="Georgia", font_size=28,
            color=primary_text, weight=BOLD
        )
        heading_2.move_to(np.array([0, grid1_bottom_y - 1.0, 0]))
        heading_2.set_z_index(5)

        # Grid 2 — load images from `institutions advancement` folder
        adv_dir = _Path("../images/institutions advancement")
        adv_files = sorted(
            list(adv_dir.glob("*.jpg")) +
            list(adv_dir.glob("*.png")) +
            list(adv_dir.glob("*.jpeg")),
            key=lambda f: int("".join(filter(str.isdigit, f.name)) or "0")
        )
        total_adv = min(40, len(adv_files))   # up to 40 images (fill as many as exist)

        # Now that we know actual counts, rebuild PANEL_HEIGHT dynamically
        _g1_rows = int(np.ceil(total_items / NUM_COLS))
        _g2_rows = int(np.ceil(total_adv  / NUM_COLS))
        PANEL_HEIGHT = (
            0.9 + 0.5 +
            _g1_rows * STEP_Y +
            1.5 +
            0.9 + 0.5 +
            _g2_rows * STEP_Y +
            0.5
        ) + 0.5
        # Resize the already-built panel to the correct height
        long_panel.stretch_to_fit_height(PANEL_HEIGHT)
        long_panel.move_to(np.array([0, PANEL_TOP_Y - PANEL_HEIGHT/2, 0]))

        grid2_start_y = heading_2.get_center()[1] - 0.6 - CELL_H/2
        all_cards_2 = []
        all_imgs_2  = []

        for i in range(total_adv):
            col = i % NUM_COLS
            row = i // NUM_COLS
            cx  = -total_row_w/2 + col*STEP_X + CELL_W/2
            cy  = grid2_start_y - row*STEP_Y

            # White card backing — identical pattern to Grid 1
            card2 = RoundedRectangle(
                width=CELL_W, height=CELL_H,
                corner_radius=0.12,
                stroke_width=0,
                fill_color=WHITE,
                fill_opacity=1.0
            )
            card2.move_to(np.array([cx, cy, 0]))
            card2.set_z_index(20)
            all_cards_2.append(card2)

            try:
                img2 = ImageMobject(str(adv_files[i]))
                scale2 = min(CELL_W*0.85 / img2.width, CELL_H*0.85 / img2.height)
                img2.scale(scale2)
            except Exception:
                img2 = Text(adv_files[i].stem[:12], font="Georgia",
                            font_size=14, color="#222222")
            img2.move_to(np.array([cx, cy, 0]))
            img2.set_z_index(21)
            all_imgs_2.append(img2)

        # Build scroll group (includes both grids)
        scroll_group = Group(
            long_panel, heading_1, heading_2,
            *all_cards, *all_imgs,
            *all_cards_2, *all_imgs_2
        )

        # Step 3: Add everything — camera is at ORIGIN, images render correctly
        self.add(long_panel, heading_1, heading_2)
        for card in all_cards:
            self.add(card)
        for img in all_imgs:
            self.add(img)
        for card2 in all_cards_2:
            self.add(card2)
        for img2 in all_imgs_2:
            self.add(img2)   # Grid 2 images added while camera is fixed = renders correctly

        # Initial reveal
        self.play(FadeIn(long_panel), FadeIn(heading_1), run_time=0.8)
        self.play(
            LaggedStart(
                *[FadeIn(c, scale=0.9) for c in all_cards],
                lag_ratio=0.06
            ),
            run_time=2.0
        )
        self.wait(0.3)
        self.play(FadeIn(heading_2), run_time=0.5)
        self.play(
            LaggedStart(
                *[FadeIn(c2, scale=0.9) for c2 in all_cards_2],
                lag_ratio=0.06
            ),
            run_time=2.0
        )
        self.wait(0.5)

        # Step 4: Scroll content UP — camera stays fixed at ORIGIN
        scroll_distance = PANEL_HEIGHT - 8.0 + 1.0
        self.play(
            scroll_group.animate.shift(UP * scroll_distance),
            run_time=9.0,
            rate_func=linear
        )
        self.wait(1.0)


        # Final Zoom out and Summary
        
        # Define Layout
        # Re-bind missing groups for final zoom out
        stakeholders = VGroup(sphere, panel, heading)
        cluster_group = circle_group
        full_panel_group = scroll_group  # alias so the zoom-out block still works
        
        stakeholders.set_opacity(1)
        cluster_group.set_opacity(1)
        self.add(stakeholders, cluster_group)
        # Final zoom-out: NEVER call move_camera() — it breaks ImageMobjects!
        # Instead, scale + move groups; camera stays fixed at ORIGIN.
        summary_center = ORIGIN
        corner_offset_x = 5.5
        corner_offset_y = 2.5

        image_9.move_to(summary_center)
        image_9.scale_to_fit_height(1.2)

        # Scale everything small enough to fit in frame, then place it
        self.play(
            stakeholders.animate.scale_to_fit_height(5).move_to(
                summary_center + UP * corner_offset_y + LEFT * corner_offset_x),
            cluster_group.animate.scale_to_fit_height(3.5).move_to(
                summary_center + DOWN * corner_offset_y),
            full_panel_group.animate.scale_to_fit_height(5).move_to(
                summary_center + UP * corner_offset_y + RIGHT * corner_offset_x),
            FadeIn(image_9),
            run_time=3.5,
            rate_func=rate_functions.ease_in_out_cubic
        )
        
        # 3. Connectors
        connectors = VGroup()
        for target in [stakeholders, cluster_group, full_panel_group]:
            start = image_9.get_center()
            end = target.get_center()
            direction = normalize(end - start)
            line = ArcBetweenPoints(start + direction * 1.5, end - direction * 2.5, angle=PI/4, color=data_accent, stroke_width=3)
            glow = ArcBetweenPoints(start + direction * 1.5, end - direction * 2.5, angle=PI/4, color=data_accent, stroke_width=8, stroke_opacity=0.3)
            connectors.add(VGroup(glow, line))
            
        self.play(LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.1), run_time=1.5)
        self.wait(2.0)



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
