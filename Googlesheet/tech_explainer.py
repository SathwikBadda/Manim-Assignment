## 8-12 sec Tech Product Video


from manim import *
import numpy as np

class TechExplainer(MovingCameraScene):
    def construct(self):
        self.camera.background_color = ManimColor("#0d1b2a")

        # --- Glow orb builder ---
        def make_glow_orb(pos=ORIGIN):
            group = VGroup()
            n = 35
            for i in range(n, 0, -1):
                r = 0.05 + i * 0.055
                alpha = 0.025 * ((1 - i / n) ** 2.2) + 0.002
                t = i / n
                color = interpolate_color(ManimColor("#FFFF44"), ManimColor("#FF6600"), t)
                c = Circle(radius=r, fill_color=color, fill_opacity=alpha, stroke_width=0)
                group.add(c)
            # Solid hot core
            core = Circle(radius=0.07, fill_color=ManimColor("#FFFFFF"), fill_opacity=1.0, stroke_width=0)
            group.add(core)
            group.move_to(pos)
            return group

        # Orbit params
        orbit_radius = 2.8
        center = np.array([-1.1, 0.1, 0])

        def orbit_pos(angle):
            return center + np.array([
                orbit_radius * np.cos(angle),
                orbit_radius * np.sin(angle),
                0
            ])

        # Feature definitions
        features = [
            {"color": ManimColor("#6C5CE7"), "label": "Secure login",    "angle": np.pi * 0.85},
            {"color": ManimColor("#00B4D8"), "label": "Registration",     "angle": np.pi * 0.50},
            {"color": ManimColor("#C77DFF"), "label": "User management",  "angle": np.pi * 0.15},
        ]

        def make_feature_card(color, label, icon_scale=0.55):
            icon = RoundedRectangle(
                corner_radius=0.15,
                width=0.9 * icon_scale / 0.55,
                height=0.9 * icon_scale / 0.55,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0,
            )
            # Simple icon decoration: small inner shape
            inner = RoundedRectangle(
                corner_radius=0.06,
                width=0.38 * icon_scale / 0.55,
                height=0.3 * icon_scale / 0.55,
                fill_color=interpolate_color(color, WHITE, 0.35),
                fill_opacity=0.9,
                stroke_width=0,
            )
            inner.move_to(icon.get_center())
            icon_group = VGroup(icon, inner)

            text = Text(label, font_size=32, color=ManimColor("#E8EDF2"), weight=BOLD)
            row = VGroup(icon_group, text)
            row.arrange(RIGHT, buff=0.28)
            return row

        # Build feature rows
        feature_rows = []
        for i, f in enumerate(features):
            row = make_feature_card(f["color"], f["label"])
            feature_rows.append(row)

        # Arrange feature rows vertically, left-aligned
        feature_list = VGroup(*feature_rows)
        feature_list.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        feature_list.move_to(ORIGIN)

        # Start orb at Top
        start_angle = 0.5 * np.pi
        orb_pos = orbit_pos(start_angle)
        orb = make_glow_orb(orb_pos)
        
        # Smooth Solid Comet Ribbon Tail
        particles = VGroup()
        self.add(particles)
        
        current_global_scale = [1.0] 
        last_pos = [orb_pos]
        
        def update_particles(mob, dt):
            if dt == 0: return
            current_pos = orb.get_center()
            prev = last_pos[0]
            
            dist = np.linalg.norm(current_pos - prev)
            steps = max(1, int(dist / 0.015)) 
            
            xs = np.linspace(prev[0], current_pos[0], steps)
            ys = np.linspace(prev[1], current_pos[1], steps)
            
            for i in range(steps):
                interpolated_pos = np.array([xs[i], ys[i], 0])
                r = np.random.uniform(0.08, 0.12) * current_global_scale[0]
                alpha_base = np.random.uniform(0.25, 0.45)
                color = np.random.choice(["#FFFF88", "#FFAA00", "#FF6600"])
                
                p = Circle(radius=r, fill_color=ManimColor(color), fill_opacity=alpha_base, stroke_width=0)
                p.move_to(interpolated_pos)
                mob.add(p)
                
            last_pos[0] = current_pos
                
            to_remove = []
            for sub in mob:
                op = sub.get_fill_opacity() - (dt * 2.0) 
                if op <= 0:
                    to_remove.append(sub)
                else:
                    sub.set_fill(opacity=op)
                    sub.scale(max(0.01, 1 - (dt * 3.5)))
                    
            mob.remove(*to_remove)
            
        particles.add_updater(update_particles)
        self.add(orb)

        # Setup trackers
        angle_tracker = ValueTracker(start_angle)
        time_tracker = ValueTracker(0.0)

        def update_orb(m):
            a = angle_tracker.get_value()
            t = time_tracker.get_value()
            
            progress = (a - start_angle) / (2 * np.pi)
            progress = np.clip(progress, 0, 1)
            
            base_scale = 1.0 + 2.0 * progress
            pulse = 0.08 * np.sin(t * 12)
            new_scale = base_scale + pulse
            
            current_global_scale[0] = new_scale
            
            new_orb = make_glow_orb(ORIGIN)
            new_orb.scale(new_scale)
            new_orb.move_to(orbit_pos(a))
            m.become(new_orb)

        orb.add_updater(update_orb)

        # Prep feature icons
        for row in feature_rows:
            row.set_opacity(0)
            row.scale(0.8)
            self.add(row)

        orbit_len = 6.0 # Fast sweep

        # Hardcode precisely timed jump triggers matching the orb swept trajectory
        # 1. Top Feature (Secure login) triggered when orb wraps around: delay ~ 5.2s
        # 2. Mid Feature (Registration) triggered when orb ascends right side: delay ~ 4.4s
        # 3. Bot Feature (User MgMT) triggered when orb reaches bottom right: delay ~ 3.5s
        # Oh wait, they pass from Bottom to Top as it goes up the right side!
        # So we trigger indices [2], [1], [0] sequentially!
        
        # Or wait, the original user timeline had them appearing [0], [1], [2] every second.
        # Let's preserve the original `delay` order but scale it realistically!
        # Orb reaches the top-right features around 5s, mid around 4s, bot around 3.5s
        
        pop_delays = [2.0, 3.2, 4.4] # Using the classic timing order for visual continuity!

        pop_anims = []
        for i, delay in enumerate(pop_delays):
            # Succession allows us to Wait perfectly before triggering the bounce animation
            # ease_out_elastic creates a highly-satisfying mechanical POP/bouncing zoom overshoot.
            anim = Succession(
                Wait(delay),
                feature_rows[i].animate(rate_func=rate_functions.ease_out_elastic, run_time=0.85).set_opacity(1).scale(1 / 0.8)
            )
            pop_anims.append(anim)

        # Single continuous sweep! The features will pop dynamically when perfectly synchronized.
        self.play(
            angle_tracker.animate(run_time=orbit_len, rate_func=linear).set_value(2.5 * np.pi), # Finish cleanly exactly at top. (1 Full rotation)
            time_tracker.animate(run_time=orbit_len, rate_func=linear).set_value(orbit_len),
            *pop_anims
        )

        self.wait(0.3)

        # Remove orb updater and sweep LEFT horizontally
        orb.remove_updater(update_orb)
        
        # Clear comet particles safely
        particles.remove_updater(update_particles)
        
        # Synchronized Camera Pan Exit:
        cam_dest = self.camera.frame.get_center() + LEFT * 12
        orb_dest = orb.get_center() + LEFT * 22
        
        self.play(
            orb.animate.move_to(orb_dest),
            self.camera.frame.animate.move_to(cam_dest),
            FadeOut(particles, run_time=0.4), # Fade tail out quickly
            run_time=2.2,
            rate_func=smooth
        )

        # --- PHASE 3: Transform to Dashboard ---
        w = 9.2
        h = 5.8
        
        dash_bg = RoundedRectangle(
            corner_radius=0.18, width=w, height=h,
            fill_color=ManimColor("#0C295A"), fill_opacity=1, stroke_width=0
        )
        # Position dashboard directly inside the new camera view
        dash_bg.move_to(cam_dest)
        
        header_line = Line(
            dash_bg.get_left() + RIGHT*0.05 + UP*(h/2 - 0.55),
            dash_bg.get_right() + LEFT*0.05 + UP*(h/2 - 0.55),
            color=ManimColor("#1A478C"), stroke_width=2
        )
        
        dots = VGroup(*[Circle(radius=0.065, fill_color=ManimColor("#E81CFF"), fill_opacity=1, stroke_width=0) for _ in range(3)])
        dots.arrange(RIGHT, buff=0.15)
        dots.move_to(dash_bg.get_top() + DOWN*0.28 + LEFT*(w/2 - 0.45))
        
        search_bar = RoundedRectangle(
            corner_radius=0.08, width=2.6, height=0.22,
            fill_color=ManimColor("#194C9C"), fill_opacity=1, stroke_width=0
        )
        search_bar.move_to(dash_bg.get_top() + DOWN*0.28 + RIGHT*(w/2 - 1.6))
        
        search_in_line = Line(search_bar.get_left() + RIGHT*0.1, search_bar.get_left() + RIGHT*1.4, color=ManimColor("#E81CFF"), stroke_width=3)
        mag = Circle(radius=0.045, color=WHITE, stroke_width=1.5)
        mag_handle = Line(mag.get_bottom()+RIGHT*0.02, mag.get_bottom()+RIGHT*0.07+DOWN*0.05, color=WHITE, stroke_width=1.5)
        mag_glass = VGroup(mag, mag_handle).move_to(search_bar.get_right() + LEFT*0.45)
        cross = VGroup(Line(UL*0.05, DR*0.05, color=WHITE, stroke_width=1.5), Line(UR*0.05, DL*0.05, color=WHITE, stroke_width=1.5))
        cross.move_to(search_bar.get_right() + LEFT*0.15)
        url_bar = VGroup(search_bar, search_in_line, mag_glass, cross)

        dash_left = dash_bg.get_left()[0]
        dash_right = dash_bg.get_right()[0]
        dash_top = header_line.get_center()[1]
        dash_bottom = dash_bg.get_bottom()[1]
        pad = 0.35 
        
        content_left = dash_left + pad
        content_right = dash_right - pad
        content_top = dash_top - pad + 0.1
        content_bottom = dash_bottom + pad
        
        content_w = content_right - content_left
        content_h = content_top - content_bottom
        
        left_w = content_w * 0.28
        left_h = content_h
        left_panel = RoundedRectangle(corner_radius=0.15, width=left_w, height=left_h, fill_color=ManimColor("#227EE3"), fill_opacity=1, stroke_width=0)
        left_panel.move_to(np.array([content_left + left_w/2, content_bottom + left_h/2, 0]))
        
        inner_pad = 0.22
        right_w = content_w - left_w - inner_pad
        right_area_left = content_left + left_w + inner_pad
        
        top_h = content_h * 0.45
        top_wide = RoundedRectangle(corner_radius=0.15, width=right_w, height=top_h, fill_color=ManimColor("#1CB5E0"), fill_opacity=1, stroke_width=0)
        top_wide.move_to(np.array([right_area_left + right_w/2, content_top - top_h/2, 0]))
        
        bot_h = content_h - top_h - inner_pad
        bot_area_top = content_top - top_h - inner_pad
        
        purple_w = right_w * 0.38
        bot_purple = RoundedRectangle(corner_radius=0.15, width=purple_w, height=bot_h, fill_color=ManimColor("#8B5CF6"), fill_opacity=1, stroke_width=0)
        bot_purple.move_to(np.array([right_area_left + purple_w/2, bot_area_top - bot_h/2, 0]))
        
        teal_w = right_w * 0.38
        teal_left = right_area_left + purple_w + inner_pad
        bot_teal = RoundedRectangle(corner_radius=0.15, width=teal_w, height=bot_h, fill_color=ManimColor("#0EA5E9"), fill_opacity=1, stroke_width=0)
        bot_teal.move_to(np.array([teal_left + teal_w/2, bot_area_top - bot_h/2, 0]))
        
        lines_left = teal_left + teal_w + inner_pad
        lines_w = right_w - purple_w - teal_w - (2 * inner_pad)
        sidebar_blocks = VGroup(*[
            RoundedRectangle(corner_radius=0.06, width=lines_w, height=(bot_h - (3 * 0.22))/4, fill_color=ManimColor("#1B54B3"), fill_opacity=1, stroke_width=0)
            for _ in range(4)
        ])
        sidebar_blocks.arrange(DOWN, buff=0.22)
        sidebar_blocks.move_to(np.array([lines_left + lines_w/2, bot_area_top - bot_h/2, 0]))

        dashboard = VGroup(
            dash_bg, header_line, dots, url_bar,
            left_panel, top_wide, bot_purple, bot_teal, sidebar_blocks
        )

        # The dashboard appears! It sweeps in smoothly to the new camera frame.
        self.play(
            FadeIn(dashboard, shift=UP*0.5, scale=0.95),
            run_time=1.5,
            rate_func=smooth,
        )

        self.wait(1.5)
