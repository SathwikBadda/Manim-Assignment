"""
RAG DOCUMENTATION MODULE: Manim Animation - GAAP & Principle of Regularity
==========================================================================
Description:
This script generates a comprehensive, multi-part explainer video scene focusing on 
U.S. GAAP (Generally Accepted Accounting Principles), specifically isolating the 
"Principle of Regularity."

RAG Parsing & Chunking Strategy:
- The file is divided into 5 distinct visual parts using heavy comment borders. 
  A vector database should ideally chunk this document along these boundaries.
- Asset Fallbacks: External assets (SVGs, PNGs) are wrapped in `try/except` blocks 
  to ensure compilation safety. Fallbacks use Manim core shapes (Rectangles, Triangles).
- Advanced Mechanics: Look for "RAG Context" tags to find implementations of 
  `ValueTracker`, `add_updater`, custom mathematical orbits, and complex `Succession` animations.

Core Manim Concepts Demonstrated:
1. MovingCameraScene frame manipulation.
2. SVG rendering with fallback geometry.
3. Parametric mathematical orbits using trigonometry (sin/cos).
4. Custom timeline/path traversal using `ValueTracker` and `CubicBezier`.
5. Particle-like stream generation with randomized sinusoidal floating effects.
"""

from manim import *
import numpy as np
import random
import os

class CombinedGAAPScene(MovingCameraScene):
    """
    RAG Context: Main Manim Scene class. Inherits from `MovingCameraScene` to allow 
    zooming in on specific diagram nodes in Part 1.
    """
    def construct(self):

        # ==========================================================
        # ---------------- GLOBAL / BRAND COLORS -------------------
        # ==========================================================
        # RAG Context: Centralized branding variables. Useful for maintaining 
        # color consistency across B2B or corporate explainer videos.
        self.camera.background_color = "#ffffff"

        CLIENT_BLUE = "#084993"
        CLIENT_ORANGE = "#ed8c32"

        LIGHT_BLUE = "#85c2e0"
        MID_BLUE = "#4e88bc"
        SANDY = "#f1a65b"

        WHITE = "#ffffff"
        LIGHT_GRAY = "#E6E6E6"

        FONT_MAIN = "Avenir"

        # ==========================================================
        # ---------------- PART 1: GAAP PRINCIPLES -----------------
        # RAG Context: Introduces the acronym GAAP over a US Map, then transitions 
        # into a hexagonal node diagram showing the 6 core principles.
        # ==========================================================
        
        # ---------------- MAP ----------------
        try:
            # Attempts to load a specific SVG map; falls back to a rounded rectangle.
            us_map = SVGMobject("us_map.svg")
        except:
            us_map = RoundedRectangle(width=8, height=4.5, corner_radius=1)

        us_map.set_fill("#F8FAFC", opacity=0)
        us_map.set_stroke("#D3D3D3", width=1.5)

        us_map.scale_to_fit_width(config.frame_width * 0.65)
        us_map.move_to(LEFT * 0.6)

        self.play(Create(us_map), run_time=2.0, rate_func=linear)
        self.play(us_map.animate.set_fill("#F8FAFC", opacity=1), run_time=0.4)
        
        # ---------------- GAAP CIRCLES ----------------
        radius = config.frame_width * 0.045

        c0 = Circle(radius=radius, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        t0 = Text("G", font=FONT_MAIN, weight=BOLD, font_size=54, color=CLIENT_BLUE).move_to(c0)
        g0 = Group(c0, t0)

        c1 = Circle(radius=radius, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        t1 = Text("A", font=FONT_MAIN, weight=BOLD, font_size=54, color=CLIENT_BLUE).move_to(c1)
        g1 = Group(c1, t1)

        c2 = Circle(radius=radius, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        t2 = Text("A", font=FONT_MAIN, weight=BOLD, font_size=54, color=CLIENT_BLUE).move_to(c2)
        g2 = Group(c2, t2)

        c3 = Circle(radius=radius, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        t3 = Text("P", font=FONT_MAIN, weight=BOLD, font_size=54, color=CLIENT_BLUE).move_to(c3)
        g3 = Group(c3, t3)

        gaap = Group(g0, g1, g2, g3)
        gaap.arrange(RIGHT, buff=0.4)
        gaap.move_to(us_map.get_center())

        # Store target positions for the "fly in" animation
        tgt0 = g0.get_center()
        tgt1 = g1.get_center()
        tgt2 = g2.get_center()
        tgt3 = g3.get_center()

        # Shift off-screen initially
        g0.shift(DOWN * 7)
        g1.shift(DOWN * 7)
        g2.shift(DOWN * 7)
        g3.shift(DOWN * 7)

        # Staggered fly-in with a slight overshoot for a dynamic feel
        self.play(g0.animate.move_to(tgt0 + UP * 0.6), run_time=0.45)
        self.play(g0.animate.move_to(tgt0), run_time=0.3)
        self.play(g1.animate.move_to(tgt1), run_time=0.55)
        self.play(g2.animate.move_to(tgt2 + UP * 0.6), run_time=0.45)
        self.play(g2.animate.move_to(tgt2), run_time=0.3)
        self.play(g3.animate.move_to(tgt3), run_time=0.55)

        # ---------------- INTRO TITLE ----------------
        intro_title = Text(
            "Key Principles of U.S. GAAP",
            font=FONT_MAIN,
            weight=BOLD,
            font_size=42,
            color=CLIENT_BLUE
        )
        intro_title.to_edge(UP, buff=0.35)
        self.play( LaggedStart( *[ FadeIn(char, shift=UP * 0.15, rate_func=rate_functions.ease_out_back) for char in intro_title ], lag_ratio=0.05 ), run_time=1.4 )
        intro_underline = Line(
            intro_title.get_left(),
            intro_title.get_right(),
            color=CLIENT_ORANGE,
            stroke_width=5
        ).next_to(intro_title, DOWN, buff=0.12)

        self.play(Create(intro_underline), run_time=1.0)

        # Scale down the map and text to make room for the hexagon
        center_group = Group(us_map, gaap)
        self.play(center_group.animate.scale(0.32).shift(DOWN * 0.5), run_time=0.8)
        hex_center = center_group.get_center()

        # ---------------- HEXAGON ----------------
        """
        RAG Context: Generates 6 placeholder circles arranged in a perfect hexagon using 
        polar coordinates (radius and angle `TAU/6`). This is a highly reusable pattern 
        for creating radial diagrams.
        """
        hex_radius = 2.8
        circles = Group()

        a0 = 0 * TAU / 6
        hc0 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc0.move_to(hex_center + np.array([hex_radius * np.cos(a0), hex_radius * np.sin(a0), 0]))
        circles.add(hc0)

        a1 = 1 * TAU / 6
        hc1 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc1.move_to(hex_center + np.array([hex_radius * np.cos(a1), hex_radius * np.sin(a1), 0]))
        circles.add(hc1)

        a2 = 2 * TAU / 6
        hc2 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc2.move_to(hex_center + np.array([hex_radius * np.cos(a2), hex_radius * np.sin(a2), 0]))
        circles.add(hc2)

        a3 = 3 * TAU / 6
        hc3 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc3.move_to(hex_center + np.array([hex_radius * np.cos(a3), hex_radius * np.sin(a3), 0]))
        circles.add(hc3)

        a4 = 4 * TAU / 6
        hc4 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc4.move_to(hex_center + np.array([hex_radius * np.cos(a4), hex_radius * np.sin(a4), 0]))
        circles.add(hc4)

        a5 = 5 * TAU / 6
        hc5 = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
        hc5.move_to(hex_center + np.array([hex_radius * np.cos(a5), hex_radius * np.sin(a5), 0]))
        circles.add(hc5)

        self.play(
            LaggedStart(
                GrowFromCenter(hc0), GrowFromCenter(hc1), GrowFromCenter(hc2),
                GrowFromCenter(hc3), GrowFromCenter(hc4), GrowFromCenter(hc5),
                lag_ratio=0.1
            ),
            run_time=1.0
        )
        self.play(Rotate(circles, angle=-TAU, about_point=hex_center), run_time=1.4, rate_func=linear)

        # ---------------- PILLS ----------------
        # RAG Context: Transforms the circular placeholders into distinct UI "Pills" with labels.
        pills = Group()
        texts = Group()
        icons = Group()

        pill0 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc0)
        pills.add(pill0)
        txt0 = Text("Regularity", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill0)
        texts.add(txt0)
        icon0 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill0, UP, buff=0.18)
        icons.add(icon0)

        pill1 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc1)
        pills.add(pill1)
        txt1 = Text("Consistency", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill1)
        texts.add(txt1)
        icon1 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill1, UP, buff=0.18)
        icons.add(icon1)

        pill2 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc2)
        pills.add(pill2)
        txt2 = Text("Sincerity", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill2)
        texts.add(txt2)
        icon2 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill2, UP, buff=0.18)
        icons.add(icon2)

        pill3 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc3)
        pills.add(pill3)
        txt3 = Text("Prudence", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill3)
        texts.add(txt3)
        icon3 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill3, UP, buff=0.18)
        icons.add(icon3)

        pill4 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc4)
        pills.add(pill4)
        txt4 = Text("Going Concern", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill4)
        texts.add(txt4)
        icon4 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill4, UP, buff=0.18)
        icons.add(icon4)

        pill5 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(hc5)
        pills.add(pill5)
        txt5 = Text("Full Disclosure", font=FONT_MAIN, weight=MEDIUM, font_size=20, color=CLIENT_BLUE).move_to(pill5)
        texts.add(txt5)
        icon5 = Circle(radius=0.18, color=CLIENT_ORANGE, fill_opacity=1).next_to(pill5, UP, buff=0.18)
        icons.add(icon5)

        self.play(
            ReplacementTransform(hc0, pill0), ReplacementTransform(hc1, pill1),
            ReplacementTransform(hc2, pill2), ReplacementTransform(hc3, pill3),
            ReplacementTransform(hc4, pill4), ReplacementTransform(hc5, pill5),
            FadeIn(txt0), FadeIn(txt1), FadeIn(txt2), FadeIn(txt3), FadeIn(txt4), FadeIn(txt5),
            run_time=1.2
        )
        self.play(
            LaggedStart(
                FadeIn(icon0, scale=0.5), FadeIn(icon1, scale=0.5), FadeIn(icon2, scale=0.5),
                FadeIn(icon3, scale=0.5), FadeIn(icon4, scale=0.5), FadeIn(icon5, scale=0.5),
                lag_ratio=0.15
            ),
            run_time=0.9
        )

        # ---------------- ZOOM INTO EACH NODE ----------------
        """
        RAG Context: Leverages `MovingCameraScene` to pan the camera frame directly 
        to the center of each specific VGroup (node), momentarily pausing, and resetting.
        """
        node0 = Group(pill0, txt0, icon0)
        node1 = Group(pill1, txt1, icon1)
        node2 = Group(pill2, txt2, icon2)
        node3 = Group(pill3, txt3, icon3)
        node4 = Group(pill4, txt4, icon4)
        node5 = Group(pill5, txt5, icon5)
        nodes = Group(node0, node1, node2, node3, node4, node5)

        original_width = self.camera.frame.width
        original_center = self.camera.frame.get_center()

        self.play(self.camera.frame.animate.move_to(node0.get_center()).set(width=3.2), run_time=0.5)
        self.play(self.camera.frame.animate.move_to(node1.get_center()).set(width=3.2), run_time=0.5)
        self.play(self.camera.frame.animate.move_to(node2.get_center()).set(width=3.2), run_time=0.5)
        self.play(self.camera.frame.animate.move_to(node3.get_center()).set(width=3.2), run_time=0.5)
        self.play(self.camera.frame.animate.move_to(node4.get_center()).set(width=3.2), run_time=0.5)
        self.play(self.camera.frame.animate.move_to(node5.get_center()).set(width=3.2), run_time=0.5)

        self.play(
            self.camera.frame.animate.move_to(original_center).set(width=original_width),
            run_time=1.4
        )

        # ---------------- ORBIT & EXIT ----------------
        """
        RAG Context: Uses a `ValueTracker` combined with `add_updater` to calculate 
        real-time polar coordinates, creating a smooth orbital animation for the nodes 
        before fading them out.
        """
        orbit_tracker = ValueTracker(0)

        def add_orbit_updater(node, center):
            # Calculate initial distance (r) and starting angle (sa)
            d = node.get_center() - center
            sa = np.arctan2(d[1], d[0])
            r = np.linalg.norm(d)
            node.add_updater(lambda m: m.move_to(center + np.array([
                r * np.cos(sa + orbit_tracker.get_value()), 
                r * np.sin(sa + orbit_tracker.get_value()), 
                0
            ])))

        add_orbit_updater(node0, hex_center)
        add_orbit_updater(node1, hex_center)
        add_orbit_updater(node2, hex_center)
        add_orbit_updater(node3, hex_center)
        add_orbit_updater(node4, hex_center)
        add_orbit_updater(node5, hex_center)

        self.play(
            orbit_tracker.animate.set_value(-TAU),
            FadeOut(Group(center_group, nodes, intro_title, intro_underline)),
            run_time=2.0,
            rate_func=linear
        )
        self.wait(0.33)


        # ==========================================================
        # ---------------- PART 2: PRINCIPLE OF REGULARITY ---------
        # RAG Context: Simple persistent title setup for the remainder of the scene.
        # ==========================================================
        reg_title = Text(
            "Principle of Regularity",
            font=FONT_MAIN,
            weight=BOLD,
            color=CLIENT_BLUE
        ).scale(0.8)
        reg_title.to_edge(UP, buff=0.4)

        reg_underline = Line(
            reg_title.get_left(),
            reg_title.get_right(),
            color=CLIENT_ORANGE,
            stroke_width=6
        ).next_to(reg_title, DOWN, buff=0.15)

        self.play( LaggedStart( *[FadeIn(char, shift=DOWN * 0.15, rate_func=rate_functions.ease_out_back) for char in reg_title], lag_ratio=0.05 ), run_time=2.6 )
        self.play(Create(reg_underline), run_time=2.2)
        self.wait(3.53)


        # ==========================================================
        # ---------------- PART 3: EXAMPLE PATH --------------------
        # RAG Context: Uses `CubicBezier` to draw a custom winding path. 
        # Demonstrates complex tracking where Mobjects follow a mathematical curve.
        # ==========================================================
        path = CubicBezier(
            LEFT*5 + DOWN*0.5,
            LEFT*2 + UP*2,
            RIGHT*1 + DOWN*2,
            RIGHT*5 + UP*0.3
        )

        dotted_path = DashedVMobject(
            path,
            num_dashes=22,
            dashed_ratio=0.65
        ).set_color(CLIENT_BLUE).set_stroke(width=8)

        self.play(Create(dotted_path), run_time=1.1)

        # ---------------- CONES + FLAGS ----------------
        # Place milestones along the Bezier curve using `point_from_proportion`.
        props = np.linspace(0.1, 0.9, 8)
        markers = Group()

        def get_cone():
            try: return ImageMobject("cone.png").scale(0.2)
            except:
                cone = Triangle(fill_color=CLIENT_ORANGE, fill_opacity=1, stroke_width=0).scale(0.16)
                base = Rectangle(height=0.05, width=0.18, fill_color=GREY_B, fill_opacity=1, stroke_width=0).next_to(cone, DOWN, buff=0)
                return VGroup(cone, base)

        def get_flag():
            try: return ImageMobject("flag.png").scale(0.2)
            except: return Square(side_length=0.16, color=CLIENT_BLUE, fill_opacity=1)

        for i, prop in enumerate(props):
            m = get_cone() if i % 2 == 0 else get_flag()
            m.move_to(path.point_from_proportion(prop) + (DOWN * 0.28 if i % 2 == 0 else UP * 0.35))
            markers.add(m)

        self.play(LaggedStart(*[FadeIn(m) for m in markers], lag_ratio=0.08), run_time=1.1)

        # ---------------- ACCOUNTANT ICON ----------------
        def accountant():
            body = Circle(radius=0.13, color=CLIENT_BLUE, fill_opacity=1)
            briefcase = Square(side_length=0.12, color=CLIENT_ORANGE, fill_opacity=1).next_to(body, DOWN, buff=0)
            return VGroup(body, briefcase)

        # ---------------- STREAM & DEVIATION ----------------
        """
        RAG Context: Advanced timing logic. Multiple accountant icons spawn at intervals 
        and traverse the Bezier path. One specific icon (the "deviator") breaks off the 
        path midway and triggers a red cross animation.
        """
        acc_time = ValueTracker(0)
        path_run_time = 2.0
        spawn_interval = 0.35
        deviation_proportion = 0.45

        acc0, acc1, acc2, acc3, acc4, acc5 = [accountant() for _ in range(6)]
        all_accountants = VGroup(acc0, acc1, acc2, acc3, acc4, acc5)
        deviator = acc3

        def setup_updater(mob, index, is_deviator=False):
            mob.spawn_time = index * spawn_interval
            def updater(m, dt):
                time_since_spawn = acc_time.get_value() - m.spawn_time
                if time_since_spawn < 0:
                    m.set_opacity(0)
                    return
                progress = time_since_spawn / path_run_time
                if not is_deviator and progress > 1:
                    m.set_opacity(0)
                    return
                m.set_opacity(1)
                m.move_to(path.point_from_proportion(min(progress, 1.0)))
            mob.add_updater(updater)

        setup_updater(acc0, 0)
        setup_updater(acc1, 1)
        setup_updater(acc2, 2)
        setup_updater(deviator, 3, is_deviator=True)
        setup_updater(acc4, 4)
        setup_updater(acc5, 5)

        all_accountants.remove(deviator)
        self.add(all_accountants, deviator)

        # Move time forward until the deviator is precisely at the break-off point
        deviation_time = deviator.spawn_time + (deviation_proportion * path_run_time)
        self.play(acc_time.animate.set_value(deviation_time), run_time=2.7, rate_func=linear)

        # Deviator breaks logic
        deviator.clear_updaters()
        deviation_anim = deviator.animate.shift(UP*1.6 + RIGHT*1.6)

        cross = VGroup(
            Line(UP*0.5 + LEFT*0.5, DOWN*0.5 + RIGHT*0.5, stroke_width=8),
            Line(UP*0.5 + RIGHT*0.5, DOWN*0.5 + LEFT*0.5, stroke_width=8)
        ).set_color(RED)
        cross.move_to(deviator.get_center() + RIGHT*0.7 + UP*0.1 + (UP*1.6 + RIGHT*1.6))
        
        # RAG Context: Uses `Succession` and `AnimationGroup` to chain sequential actions 
        # (shifting off path -> drawing red cross -> fading both out) while background time continues.
        deviation_duration = 0.7
        fade_out_duration = 0.5
        deviation_sequence = Succession(
            AnimationGroup(deviation_anim, FadeIn(cross), run_time=deviation_duration),
            AnimationGroup(FadeOut(deviator), FadeOut(cross), run_time=fade_out_duration)
        )
        
        total_sequence_duration = deviation_duration + fade_out_duration

        self.play(
            deviation_sequence,
            acc_time.animate(run_time=1.3, rate_func=linear)
            .set_value(acc_time.get_value() + 1.2),
        )

        # Finish running the rest of the accountants to the end of the path
        last_spawn_time = 5 * spawn_interval
        total_duration = last_spawn_time + path_run_time
        remaining_time = total_duration - acc_time.get_value()

        if remaining_time > 0:
            self.play(acc_time.animate.set_value(total_duration), run_time=1.1, rate_func=linear)

        self.play(FadeOut(Group(dotted_path, markers, all_accountants)), run_time=0.67)


        # ==========================================================
        # ---------------- PART 4: DOCUMENTS STREAM ----------------
        # RAG Context: Spawns streams of documents flying out of buildings. Uses 
        # custom `CubicBezier` paths generated on the fly with random noise for a dynamic feel.
        # ==========================================================
        try:
            tower = ImageMobject("tower.png").scale(0.6)
            factory = ImageMobject("factory.png").scale(0.6)
            block = ImageMobject("corporate.png").scale(0.6)
        except:
            tower = Rectangle(height=2.6, width=2.2, fill_color=LIGHT_BLUE, fill_opacity=1, stroke_width=0)
            factory = Rectangle(height=2.6, width=2.2, fill_color=SANDY, fill_opacity=1, stroke_width=0)
            block = Rectangle(height=2.6, width=2.2, fill_color=MID_BLUE, fill_opacity=1, stroke_width=0)

        buildings = VGroup(tower, factory, block)
        buildings.arrange(DOWN, buff=1)
        buildings.scale_to_fit_height(5)
        buildings.next_to(reg_underline, DOWN, buff=0.9)
        buildings.set_z_index(10)

        final_tower = tower.copy()
        final_factory = factory.copy()
        final_block = block.copy()

        tower.scale(0.01)
        factory.scale(0.01)
        block.scale(0.01)

        self.play(
            LaggedStart(
                Transform(tower, final_tower),
                Transform(factory, final_factory),
                Transform(block, final_block),
                lag_ratio=0.25,
                run_time=1.4
            )
        )

        def create_document():
            try: return ImageMobject("document.png").scale(0.25)
            except:
                paper = Rectangle(height=0.8, width=0.55, fill_color=WHITE, fill_opacity=1, stroke_color=CLIENT_ORANGE, stroke_width=2)
                dollar = Text("$", font=FONT_MAIN, weight=BOLD, color=CLIENT_BLUE).scale(0.45)
                lines = VGroup(
                    Line(LEFT * 0.18, RIGHT * 0.18).shift(DOWN * 0.15),
                    Line(LEFT * 0.18, RIGHT * 0.18).shift(DOWN * 0.28)
                ).set_color(GREY_B)
                return VGroup(paper, dollar, lines)

        documents = VGroup()
        doc_time = ValueTracker(0)
        self.add(doc_time)
        doc_time.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))

        def create_single_document_anim(building):
            doc = create_document()
            documents.add(doc)
            start = building.get_center() + RIGHT * (building.width * 0.25)
            doc.move_to(start)
            end = start + RIGHT * 7 + UP * random.uniform(-0.5, 0.5)
            c1 = start + RIGHT * 2 + UP * random.uniform(-0.6, 0.6)
            c2 = start + RIGHT * 4 + UP * random.uniform(-0.6, 0.6)
            doc_path = CubicBezier(start, c1, c2, end)

            phase = random.uniform(0, 2*np.pi)
            doc.add_updater(lambda m, ph=phase: m.shift(UP * np.sin(doc_time.get_value() * 3 + ph) * 0.002))

            return Succession(
                FadeIn(doc, scale=0.8),
                MoveAlongPath(doc, doc_path, run_time=1.8, rate_func=linear),
                FadeOut(doc, shift=RIGHT * 0.5)
            )

        animations = [
            LaggedStart(*[create_single_document_anim(tower) for _ in range(5)], lag_ratio=0.15),
            LaggedStart(*[create_single_document_anim(factory) for _ in range(5)], lag_ratio=0.15),
            LaggedStart(*[create_single_document_anim(block) for _ in range(5)], lag_ratio=0.15)
        ]

        self.play(AnimationGroup(*animations, lag_ratio=0.10), run_time=2.2)
        doc_time.clear_updaters()

        # --- SMOOTH TRANSITION FROM PART 4 to 5 ---

        # 1. Fade out stream/buildings, move factory left
        target_factory_pos = factory.copy().to_edge(LEFT, buff=1.5)
        
        self.play(
            FadeOut(documents),
            FadeOut(tower, scale=0.8),
            FadeOut(block, scale=0.8),
            factory.animate.move_to(target_factory_pos),
            run_time=1.0
        )
        
        center_building = factory # factory is now on the left

        # 2. Camera zooms in on the remaining building
        self.play(
            self.camera.frame.animate.move_to(center_building.get_center()).set(width=center_building.width * 2.5),
            run_time=0.5
        )

        # 3. Building transforms into a single large document (on the left)
        doc_main = create_document()
        doc_main.scale_to_fit_height(center_building.height)
        doc_main.move_to(center_building.get_center())

        self.play(
            Transform(center_building, doc_main),
            run_time=0.5
        )

        # 4. That document splits into two (on the left)
        doc1 = center_building
        doc2 = doc1.copy()
        self.add(doc2)

        gap = 0.1
        offset = doc1.height / 2 + gap

        self.play(
            AnimationGroup(
                # Camera (slightly earlier feel)
                self.camera.frame.animate.scale(2),

                # Split (with easing feel)
                doc1.animate.shift(UP * offset),
                doc2.animate.shift(DOWN * offset),

                lag_ratio=0.1  
            ),
            run_time=1.0,  
            rate_func=rate_functions.ease_out_cubic  # 🔥 key change
        )

        self.wait(0.5)

        # ==========================================================
        # ---------------- PART 5: REGULATORS ----------------------
        # ==========================================================

        def create_badge(label):
            try:
                return ImageMobject(f"{label.lower()}.png").scale(0.5)
            except:
                badge = RoundedRectangle(
                    width=2.2,
                    height=1.3,
                    corner_radius=0.25,
                    fill_color=CLIENT_BLUE,
                    fill_opacity=1,
                    stroke_width=0
                )
                text = Text(
                    label,
                    font=FONT_MAIN,
                    weight=BOLD,
                    color=WHITE
                ).scale(0.45).move_to(badge.get_center())
                return VGroup(badge, text)

        # Create badges (hidden initially)
        fasb = create_badge("FASB")
        sec = create_badge("SEC")

        badges = VGroup(fasb, sec)
        badges.arrange(DOWN, buff=0.6)
        badges.move_to(ORIGIN)

        badges.set_opacity(0)
        self.add(badges)
        
        # 5. Zoom out, and fly the two documents to the center to become badges
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width),
            doc1.animate.scale_to_fit_height(fasb.height).move_to(fasb.get_center()),
            doc2.animate.scale_to_fit_height(sec.height).move_to(sec.get_center()),
            run_time=2.8,
            rate_func=smooth
        )

        # 6. Morph documents into badges
        self.play(
            Transform(doc1, fasb),
            Transform(doc2, sec),
            run_time=1.3
        )

        # Ensure badges visible
        badges.set_opacity(1)

        # ==========================================================
        # ---------------- CALENDAR (MONTH PEEL CLEAN) -------------
        # ==========================================================

        calendar_center = RIGHT * 4

        W, H = 1.4, 1.2
        FLAP_COLOR = "#EBEBEB"
        months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

        def create_page(month_str):
            # Base page
            bg = Polygon(
                [-W/2, H/2, 0], [W/2, H/2, 0],
                [W/2, -H/2, 0], [-W/2, -H/2, 0],
                fill_color=WHITE, fill_opacity=1,
                stroke_width=1, stroke_color=CLIENT_BLUE
            )

            # Header
            header_h = 0.35
            header = Polygon(
                [-W/2, H/2, 0], [W/2, H/2, 0],
                [W/2, H/2-header_h, 0], [-W/2, H/2-header_h, 0],
                fill_color=CLIENT_ORANGE, fill_opacity=1,
                stroke_width=0
            )

            # ONLY MONTH TEXT (removed day)
            month_text = Text(
                month_str,
                font=FONT_MAIN,
                weight=BOLD,
                color=WHITE
            ).scale(0.5)

            month_text.move_to(np.array([0, H/2 - header_h/2, 0]))

            # Rings (kept for design consistency)
            ring1 = Circle(radius=0.04, fill_color=CLIENT_BLUE, stroke_width=0).move_to(np.array([-W/4, H/2 - header_h/2, 0]))
            ring2 = Circle(radius=0.04, fill_color=CLIENT_BLUE, stroke_width=0).move_to(np.array([W/4, H/2 - header_h/2, 0]))

            page = VGroup(bg, header, month_text, ring1, ring2)
            page.move_to(calendar_center)

            return page


        # Create pages
        pages = [create_page(m) for m in months]
        current_static = pages[0]

        self.play(FadeIn(current_static, scale=0.8), run_time=0.7)


        # ---------------- PEEL ENGINE ----------------
        def get_updater(dynamic_group, flap, flat_orig):
            def updater(mob, alpha):
                d = alpha * (W + H + 0.6)
                dynamic_group.submobjects = []

                if d <= 0.01:
                    for sm in flat_orig:
                        dynamic_group.add(sm.copy())
                    flap.set_opacity(0)
                    return

                if d >= W + H:
                    flap.set_opacity(0)
                    return

                flap.set_opacity(1)

                A = np.array([-W/2, H/2, 0]) + calendar_center
                B = np.array([W/2, H/2, 0]) + calendar_center
                C = np.array([W/2, -H/2, 0]) + calendar_center
                D = np.array([-W/2, -H/2, 0]) + calendar_center

                P1 = np.array([-W/2 + d, -H/2, 0]) + calendar_center if d <= W else np.array([W/2, -H/2 + (d - W), 0]) + calendar_center
                P2 = np.array([-W/2, -H/2 + d, 0]) + calendar_center if d <= H else np.array([-W/2 + (d - H), H/2, 0]) + calendar_center

                peeled_verts = [P1]
                if d > W: peeled_verts.append(C)
                peeled_verts.append(D)
                if d > H: peeled_verts.append(A)
                peeled_verts.append(P2)

                def reflect_point(pt, p1, p2):
                    L = p2 - p1
                    if np.linalg.norm(L) < 1e-6:
                        return pt
                    L_norm = L / np.linalg.norm(L)
                    v = pt - p1
                    proj_len = np.dot(v, L_norm)
                    return p1 + proj_len * L_norm - (v - proj_len * L_norm)

                flap_verts = [reflect_point(pt, P1, P2) for pt in peeled_verts]
                flap.become(Polygon(*flap_verts))
                flap.set_fill(FLAP_COLOR, 1)
                flap.set_stroke("#A0A0A0", 1)

            return updater


        # ---------------- EXECUTE PEEL (ALL 12 STACKED) ----------------
        stack = VGroup(current_static)

        for i in range(len(pages) - 1):
            next_static = pages[i+1]

            # subtle depth offset
            next_static.shift(DOWN * 0.01 * (i+1))
            next_static.scale(0.998)

            self.add(next_static)
            self.bring_to_front(current_static)

            dynamic_group = VGroup()
            flat_orig = list(current_static.family_members_with_points())

            self.add(dynamic_group)
            flap = Polygon([0,0,0], [1,0,0], [0,1,0])
            self.add(flap)

            self.remove(current_static)

            self.play(
                UpdateFromAlphaFunc(
                    dynamic_group,
                    get_updater(dynamic_group, flap, flat_orig)
                ),
                run_time=0.13,
                rate_func=smooth
            )

            self.remove(dynamic_group, flap)

            stack.add(current_static)
            current_static = next_static

        # Add final page
        stack.add(current_static)


       # ---------------- CLEAN FADE OUT (FULL FIX) ----------------
        calendar_group = VGroup(*pages)

        self.wait(1.3)

        self.play(
            FadeOut(
                VGroup(
                    badges,
                    reg_title,
                    reg_underline,
                    calendar_group
                ),
                shift=DOWN * 0.2
            ),
            run_time=1.0
        )