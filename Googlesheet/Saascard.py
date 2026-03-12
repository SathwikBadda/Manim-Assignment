from manim import *
import numpy as np

class SaaSCardAnimation(ThreeDScene):
    def construct(self):

        # ════════════════════════════════════════════════════════════════
        # SCENE SETUP
        # ════════════════════════════════════════════════════════════════
        self.camera.background_color = "#0a1628"
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.9)

        # ════════════════════════════════════════════════════════════════
        # HELPERS
        # ════════════════════════════════════════════════════════════════
        def make_card(w=3.4, h=4.8, fill="#1a2f4a", stroke="#3ab8f8", sw=1.4, cr=0.32):
            return RoundedRectangle(
                width=w, height=h, corner_radius=cr,
                fill_color=fill, fill_opacity=0.88,
                stroke_color=stroke, stroke_width=sw,
            )

        def make_glow_icon(color="#38bdf8"):
            layers = VGroup()
            for r, op, sw in [(0.75, 0.06, 0), (0.60, 0.0, 0.8), (0.48, 0.14, 1.2), (0.30, 1.0, 0)]:
                c = Circle(radius=r, color=color,
                           fill_opacity=op, stroke_width=sw,
                           stroke_color=color, stroke_opacity=0.6)
                layers.add(c)
            return layers

        def make_lines(color="#38bdf8", n=3):
            grp = VGroup()
            widths = [2.2, 1.6, 1.9]
            opacs  = [0.55, 0.30, 0.42]
            for i in range(n):
                bar = RoundedRectangle(
                    width=widths[i], height=0.14, corner_radius=0.07,
                    fill_color=color, fill_opacity=opacs[i], stroke_width=0
                )
                bar.shift(DOWN * (0.5 + i * 0.38))
                grp.add(bar)
            return grp

        def make_progress(color="#38bdf8", fill_ratio=0.62):
            bg = RoundedRectangle(width=2.4, height=0.25, corner_radius=0.12,
                                  fill_color="#061020", fill_opacity=0.9, stroke_width=0)
            fg_w = 2.4 * fill_ratio
            fg = RoundedRectangle(width=fg_w, height=0.25, corner_radius=0.12,
                                  fill_color=color, fill_opacity=1.0, stroke_width=0)
            fg.align_to(bg, LEFT)
            return VGroup(bg, fg)

        def make_shadow(card):
            s = card.copy()
            s.set_fill("#000000", opacity=0.20)
            s.set_stroke(width=0)
            s.shift(RIGHT * 0.10 + DOWN * 0.16)
            return s

        # ════════════════════════════════════════════════════════════════
        # BUILD THREE CARDS
        # ════════════════════════════════════════════════════════════════
        c_main   = make_card(fill="#1a2f4a", stroke="#38bdf8", sw=1.6)
        sh_main  = make_shadow(c_main)
        ico_main = make_glow_icon("#38bdf8").shift(UP * 1.0)
        lbl_main = Text("Processing", color="#8ecfe8", font_size=20).shift(UP * 0.18)
        ln_main  = make_lines("#38bdf8")
        pr_main  = make_progress("#38bdf8").shift(DOWN * 1.75)
        grp_main = VGroup(sh_main, c_main, ico_main, lbl_main, ln_main, pr_main)

        c_left   = make_card(fill="#142238", stroke="#5ba8e0", sw=1.0)
        sh_left  = make_shadow(c_left)
        ico_left = make_glow_icon("#6ab4e8").shift(UP * 1.0)
        lbl_left = Text("SECURE", color="#6ab4e8", font_size=18, weight=BOLD).shift(UP * 0.18)
        ln_left  = make_lines("#5ba8e0")
        grp_left = VGroup(sh_left, c_left, ico_left, lbl_left, ln_left)

        c_right   = make_card(fill="#142238", stroke="#7c82e8", sw=1.0)
        sh_right  = make_shadow(c_right)
        ico_right = make_glow_icon("#818cf8").shift(UP * 1.0)
        lbl_right = Text("ANALYTICS", color="#818cf8", font_size=18, weight=BOLD).shift(UP * 0.18)
        ln_right  = make_lines("#818cf8")
        grp_right = VGroup(sh_right, c_right, ico_right, lbl_right, ln_right)

        # ════════════════════════════════════════════════════════════════
        # FLAT STARTING POSITIONS
        # ════════════════════════════════════════════════════════════════
        grp_left.move_to(LEFT * 4.0)
        grp_main.move_to(ORIGIN)
        grp_right.move_to(RIGHT * 4.0)

        for g in [grp_left, grp_main, grp_right]:
            g.shift(DOWN * 9)

        self.add(grp_left, grp_right, grp_main)

        # ════════════════════════════════════════════════════════════════
        # PHASE 1 — ENTRY
        # ════════════════════════════════════════════════════════════════
        self.play(
            grp_main.animate.shift(UP * 9),
            run_time=0.75, rate_func=rate_functions.ease_out_cubic,
        )
        self.play(
            grp_left.animate.shift(UP * 9).set_opacity(0.80),
            grp_right.animate.shift(UP * 9).set_opacity(0.80),
            run_time=0.60, rate_func=rate_functions.ease_out_cubic,
        )
        self.wait(0.25)

        # ════════════════════════════════════════════════════════════════
        # PHASE 2 — FORM SLIGHTLY-BENT CYLINDRICAL CAROUSEL
        # ════════════════════════════════════════════════════════════════
        # Tighter radius = smaller gaps between cards
        R = 2.8
        carousel_center = np.array([0, 0, -R])

        def bend_card(mob, radius=R):
            """Slight cylindrical bend: x-positions map to arc on cylinder."""
            def map_point(p):
                x, y, z = p
                theta = x / radius
                return np.array([
                    radius * np.sin(theta),
                    y,
                    radius * np.cos(theta) - radius + z
                ])
            mob.apply_function(map_point)
            return mob

        cards = [grp_main, grp_right, grp_left]
        angles = [0, -120 * DEGREES, -240 * DEGREES]

        target_group = VGroup()
        for g, a in zip(cards, angles):
            tgt = g.copy()
            tgt.shift(ORIGIN - tgt[1].get_center())
            tgt.set_opacity(1.0)
            bend_card(tgt, R)
            tgt.rotate(-a, axis=UP, about_point=carousel_center)
            target_group.add(tgt)

        anims = [Transform(g, tgt) for g, tgt in zip(cards, target_group)]

        # ════════════════════════════════════════════════════════════════
        # CAMERA-AWARE Z-SORTING (fixes layering issue)
        # ════════════════════════════════════════════════════════════════
        # Sort cards by depth relative to camera's actual viewing direction.
        # This ensures near cards always render ON TOP of far cards,
        # even when the camera rotates to different angles.
        def sort_cards_in_scene(dt):
            # Get current camera orientation
            try:
                phi_v = self.camera.phi_tracker.get_value()
                theta_v = self.camera.theta_tracker.get_value()
            except AttributeError:
                try:
                    phi_v = self.camera.get_phi()
                    theta_v = self.camera.get_theta()
                except:
                    phi_v = 20 * DEGREES
                    theta_v = -70 * DEGREES

            # Camera direction vector (from origin toward camera position)
            cam_dir = np.array([
                np.sin(phi_v) * np.cos(theta_v),
                np.sin(phi_v) * np.sin(theta_v),
                np.cos(phi_v)
            ])

            others = [m for m in self.mobjects if m not in cards]
            # Higher dot product = closer to camera = drawn LAST (on top)
            sorted_cards = sorted(cards, key=lambda m: np.dot(m.get_center(), cam_dir))
            self.mobjects = others + sorted_cards

        # Add sorting updater BEFORE the carousel forms
        self.add_updater(sort_cards_in_scene)

        # Camera tilts + cards form carousel (combined, no pause)
        self.move_camera(
            phi=20 * DEGREES,
            theta=-90 * DEGREES,
            zoom=0.68,
            added_anims=anims,
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # ════════════════════════════════════════════════════════════════
        # PHASE 3 — CONTINUOUS FAST CAROUSEL SPIN (no stopping)
        # ════════════════════════════════════════════════════════════════

        # Camera pans right WHILE cards start rotating (seamless transition)
        self.move_camera(
            phi=22 * DEGREES,
            theta=-65 * DEGREES,
            zoom=0.65,
            added_anims=[
                *[Rotate(c, angle=90 * DEGREES, axis=UP, about_point=carousel_center) for c in cards]
            ],
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # Continuous fast rotation — NO PAUSES
        self.play(
            *[Rotate(c, angle=360 * DEGREES, axis=UP, about_point=carousel_center) for c in cards],
            run_time=4.5,
            rate_func=linear,
        )

        # Gentle deceleration to stop
        self.play(
            *[Rotate(c, angle=50 * DEGREES, axis=UP, about_point=carousel_center) for c in cards],
            run_time=1.5,
            rate_func=rate_functions.ease_out_sine,
        )

        self.wait(1.5)