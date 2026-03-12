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
        
    
        # Transform to sphere
        self.play(
            orbit_scale_tracker.animate.set_value(0.0),
            FadeIn(sphere),
            run_time=1.0
        )
        
        for icon in image_icons:
            icon.clear_updaters()
            self.remove(icon)
            
        # Sphere rotation (slowing down)
        self.play(
            Rotate(sphere, angle=TAU, axis=UP, rate_func=rate_functions.ease_out_expo),
            run_time=2.0
        )
        
        ## Section 3
        
        panel = RoundedRectangle(
            width=6,
            height=6.72,
            corner_radius=0.1,
            stroke_width=0.8,
            stroke_color=tertiary_text,
            fill_color=depth_layer,
            fill_opacity=1.0
        )
        panel.next_to(sphere,RIGHT,buff=0.4)
        #self.add(panel)
        
        self.play(DrawBorderThenFill(panel), run_time=1.0)
        
        heading = Text("Designed by Global Leaders", font="Georgia", font_size=18, 
                      color=primary_text, weight=BOLD).scale(0.7)
        heading.move_to(panel.get_top()+DOWN*0.5)
        #self.add(heading)
        
        self.play(
            AddTextLetterByLetter(heading),
            heading.animate.scale(1.0/0.7),
            FadeIn(heading),
            run_time=0.8
        )
        
        list_items_data = [
            "Academic Heads & Chairpersons",
            "Advisory Board Members",
            "Policy & Research Experts",
            "International Institutional Partners"
        ]
        y_coords = [0.5, 0.1, -0.3, -0.7]
        
        list_items = []
        dots = []
        
        for i, (item_text, y_pos) in enumerate(zip(list_items_data, y_coords)):
            dot = Circle(radius=0.08, stroke_width=0.6, stroke_color=tertiary_text, 
                        fill_opacity=1.0)
            dot.move_to(np.array([panel.get_left()[0]+0.8, y_pos, 0]))
            dots.append(dot)
            #self.add(dot)
            
            item = Text(item_text, font="Times New Roman", font_size=14, 
                       color=secondary_text)
            item.next_to(dot, RIGHT, buff=0.2)
            list_items.append(item)
            #self.add(item)
        
        item_anims = []
        for i, (item, dot) in enumerate(zip(list_items, dots)):
            item_anims.append(
                AnimationGroup(
                    FadeIn(dot),
                    FadeIn(item),
                    lag_ratio=0.0,
                    run_time=0.5
                )
            )
        
        self.play(LaggedStart(*item_anims, lag_ratio=0.8), run_time=3.2)
        
        list_content = VGroup(*list_items, *dots)
        
        def scroll_updater(mob, dt):
            t = self.renderer.time
            scroll_distance = 0.3 * t
            scroll_wrapped = scroll_distance % 2.4
            mob.move_to(np.array([0, -scroll_wrapped, 0]), aligned_edge=ORIGIN)
        
        list_content.add_updater(scroll_updater)
        
        #Add other newly created items in this as well
        stakeholders = VGroup(sphere, panel,heading)
        
        self.wait(1.88)
        
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

        # Generate two dense circular clusters
        def circular_cluster(center, radius, n):
            dots = VGroup()
            for _ in range(n):
                r = radius * np.sqrt(np.random.uniform(0, 1))
                theta = np.random.uniform(0, TAU)
                x = center[0] + r * np.cos(theta)
                y = center[1] + r * np.sin(theta)

                dot = Circle(
                    radius=0.07,
                    fill_color=primary_text,
                    fill_opacity=1,
                    stroke_width=0
                )
                dot.move_to([x, y, 0])
                dots.add(dot)
            return dots


        cluster_1 = circular_cluster(self.camera.frame_center + LEFT * 1.2, 1.2, 40)
        cluster_2 = circular_cluster(self.camera.frame_center + RIGHT * 1.2, 1.2, 40)

        circle_group = VGroup(circle_boundary, cluster_1, cluster_2)

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

        cluster_group = VGroup(circle_group, cluster_1, cluster_2)

        ## Section 5
        self.move_camera(
            frame_center=self.camera.frame_center + DOWN * 8,
            run_time=3
        )
        

        # Create the long scrolling panel
        panel_width = 10.0
        panel_height = 22.0
        
        long_panel = Rectangle(
            width=panel_width,
            height=panel_height,
            fill_color=depth_layer,
            fill_opacity=1.0,
            stroke_color=tertiary_text,
            stroke_width=1.5
        )
        
        long_panel.move_to(self.camera.frame_center + DOWN*long_panel.height/2)

        # Content Group
        content_group = VGroup()
        
        # Heading 1: Institutions in Engagement
        heading_1 = Text("Institutions in Engagement", font="Georgia", font_size=32, color=primary_text, weight=BOLD)
        heading_1.move_to(long_panel.get_top() + DOWN * 1.0)
        content_group.add(heading_1)
        
        
        
        # Grid 1 placeholders
        grid_1 = VGroup()
        for i in range(8): # 2 rows of 4
            placeholder = RoundedRectangle(width=1.5, height=1.2, corner_radius=0.1, color=secondary_text, stroke_width=1.0)
            placeholder.set_fill(color=bg_color, opacity=0.3)
            
            # Placeholder icon graphic (simple circle)
            icon_ph = Circle(radius=0.3, color=data_accent, stroke_width=1.5)
            item = VGroup(placeholder, icon_ph)
            
            row = i // 4
            col = i % 4
            # Center grid horizontally
            x = (col - 1.5) * 2.0
            y = -row * 1.8
            item.next_to(heading_1, DOWN, buff=0.3)
            item.shift(DOWN * (1.5+y) + RIGHT * x)
            grid_1.add(item)
        content_group.add(grid_1)
        
        # Heading 2: Institutions in Advanced Engagement
        heading_2 = Text("Institutions in Advanced Engagement", font="Georgia", font_size=32, color=primary_text, weight=BOLD)
        heading_2.move_to(grid_1.get_bottom() + DOWN * 2.5)
        content_group.add(heading_2)
        
        # Grid 2 placeholders
        grid_2 = VGroup()
        for i in range(12): # 3 rows of 4
            placeholder = RoundedRectangle(width=1.5, height=1.2, corner_radius=0.1, color=secondary_text, stroke_width=1.0)
            placeholder.set_fill(color=bg_color, opacity=0.3)
            
            # Placeholder icon graphic (simple square)
            icon_ph = Square(side_length=0.5, color=data_accent, stroke_width=1.5)
            item = VGroup(placeholder, icon_ph)
            
            row = i // 4
            col = i % 4
            x = (col - 1.5) * 2.0
            y = -row * 1.8
            item.next_to(heading_2, DOWN, buff=0.3)
            item.shift(DOWN * (1.5 + y) + RIGHT * x)
            grid_2.add(item)
        content_group.add(grid_2)
        
        full_panel_group = VGroup(long_panel, content_group)
        
        
        
        # Camera zoom to reveal first portion
        self.move_camera(
            frame_center=heading_1.get_center() + DOWN * 1.0,
            zoom=1.3,
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_quad
        )

        # Animate appearance
        self.play(FadeIn(full_panel_group), run_time=1.5)
        self.wait(0.5)
        
        # Pan downwards to reveal next portion
        self.move_camera(
            frame_center=heading_2.get_center() + DOWN * 2.0,
            run_time=2.0,
            rate_func=linear
        )
        self.wait(0.5)

        self.move_camera(
            frame_center=long_panel.get_bottom() + DOWN * 5.0,
            run_time=1.0,
            rate_func=rate_functions.ease_in_out_quad
        )
        
        
        # Final Zoom out and Summary
        
        # Define Layout
        summary_center = long_panel.get_bottom() + DOWN * 5.0
        corner_offset_x = 6.0
        corner_offset_y = 3.5
        
        self.move_camera(frame_center = summary_center, zoom = 0.5, run_time = 0.5)
        image_9.move_to(self.camera.frame_center).scale(2.0)

        # 2. Animate Transition
        self.play(
            #pathway_summary.animate.scale_to_fit_height(5).move_to(summary_center + UP * corner_offset_y + LEFT * corner_offset_x),
            stakeholders.animate.scale_to_fit_height(7).move_to(summary_center + UP * corner_offset_y + LEFT * corner_offset_x),
            cluster_group.animate.scale_to_fit_height(5).move_to(summary_center + DOWN * corner_offset_y),
            full_panel_group.animate.scale_to_fit_height(7).move_to(summary_center + UP * corner_offset_y + RIGHT * corner_offset_x),
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

    file_dir = Path(r"../test_raw_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "Scene_2.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")