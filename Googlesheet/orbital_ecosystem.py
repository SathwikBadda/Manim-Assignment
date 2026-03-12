from manim import *
import numpy as np


class OrbitalEcosystem(Scene):
    def construct(self):
        self.camera.background_color = ManimColor("#F0EEF8")

        # ── Soft background rings ──────────────────────────────────
        rings = VGroup()
        for r, op in [(4.8, 0.10), (3.5, 0.12), (2.4, 0.09)]:
            ring = Circle(radius=r, fill_color=ManimColor("#C8B8F0"),
                          fill_opacity=op, stroke_width=0)
            rings.add(ring)
        self.add(rings)

        # ── Central logo (Slack-style rounded square with cross) ───
        center_bg = RoundedRectangle(
            corner_radius=0.28, width=1.85, height=1.85,
            fill_color=WHITE, fill_opacity=1, stroke_width=0,
        )

        # Slack-style hash cross icon (4 colored rounded bars)
        bar_configs = [
            (ManimColor("#E01E5A"), [-0.28,  0.28, 0], 0),    # top-left  H
            (ManimColor("#ECB22E"), [ 0.28,  0.28, 0], 0),    # top-right H
            (ManimColor("#2EB67D"), [-0.28, -0.28, 0], 0),    # bot-left  H
            (ManimColor("#36C5F0"), [ 0.28, -0.28, 0], 0),    # bot-right H
        ]
        logo_pieces = VGroup()
        for color, pos, _ in bar_configs:
            bar = RoundedRectangle(
                corner_radius=0.10, width=0.22, height=0.55,
                fill_color=color, fill_opacity=1, stroke_width=0,
            )
            bar.move_to(np.array(pos))
            logo_pieces.add(bar)

        # Horizontal bars crossing
        for color, pos, _ in bar_configs:
            bar = RoundedRectangle(
                corner_radius=0.10, width=0.55, height=0.22,
                fill_color=color, fill_opacity=1, stroke_width=0,
            )
            bar.move_to(np.array(pos))
            logo_pieces.add(bar)

        center_logo = VGroup(center_bg, logo_pieces)
        center_logo.move_to(ORIGIN)

        # ── Orbit icon builder ────────────────────────────────────
        import os
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

        def make_orbit_icon(img_name, size=0.8):
            img_path = os.path.join(images_dir, img_name)
            icon = ImageMobject(img_path)
            icon.height = size
            return icon
            
        n_icons = len(img_names)
        orbit_r = 3.0
        base_angles = [PI / 2 + 2 * PI * i / n_icons for i in range(n_icons)]

        orbit_icons = []
        for i, img_name in enumerate(img_names):
            icon = make_orbit_icon(img_name)
            angle = base_angles[i]
            icon.move_to(np.array([orbit_r * np.cos(angle),
                                   orbit_r * np.sin(angle), 0]))
            icon.set_opacity(0)
            orbit_icons.append(icon)

        all_icons = Group(*orbit_icons)

        self.add(center_logo, all_icons)
        center_logo.set_opacity(0)

        # ── PHASE 1: Fade in center, then icons ───────────────────
        self.play(
            center_logo.animate.set_opacity(1),
            run_time=0.9, rate_func=smooth,
        )

        self.play(
            LaggedStart(
                *[icon.animate.set_opacity(1) for icon in orbit_icons],
                lag_ratio=0.10,
            ),
            run_time=1.4, rate_func=smooth,
        )
        self.wait(0.3)

        # ── PHASE 2: Continuous smooth orbit with updaters ────────
        orbit_speed = 0.32   # radians per second
        t_start = self.renderer.time

        def make_updater(icon, base_angle):
            def updater(mob, dt):
                t = self.renderer.time - t_start
                angle = base_angle + t * orbit_speed
                mob.move_to(np.array([
                    orbit_r * np.cos(angle),
                    orbit_r * np.sin(angle),
                    0
                ]))
            return updater

        updaters = []
        for icon, base_angle in zip(orbit_icons, base_angles):
            u = make_updater(icon, base_angle)
            icon.add_updater(u)
            updaters.append(u)

        # Let orbit run for 5.5 seconds
        self.wait(5.5)

        # ── PHASE 3: Icons collapse into center ───────────────────
        for icon, u in zip(orbit_icons, updaters):
            icon.remove_updater(u)

        self.play(
            LaggedStart(
                *[icon.animate.move_to(ORIGIN).scale(0.05).set_opacity(0)
                  for icon in orbit_icons],
                lag_ratio=0.06,
            ),
            run_time=1.2, rate_func=smooth,
        )

        # Final pulse on center logo
        self.play(
            center_logo.animate.scale(1.12),
            run_time=0.25, rate_func=smooth,
        )
        self.play(
            center_logo.animate.scale(1 / 1.12),
            run_time=0.25, rate_func=smooth,
        )
        self.wait(0.8)
