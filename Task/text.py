from manim import *

# Render config
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#F6E15F"


class CroppedZoomTypography(Scene):
    def construct(self):
        TEXT_COLOR = BLACK
        FONT_SIZE = 120

        # -----------------------------
        # CREATE TEXT OBJECTS
        # -----------------------------
        t1 = Text("We’re", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR)
        t2 = Text("excited", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR)
        t3 = Text("to", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR)

        # -----------------------------
        # 1. "We’re" ZOOM IN → ZOOM OUT
        # -----------------------------
        t1.scale(0.1)
        t1.move_to(ORIGIN)
        self.add(t1)

        self.play(
            t1.animate.scale(15),
            run_time=1.2,
            rate_func=rate_functions.ease_out_cubic,
        )

        self.play(
            t1.animate.scale(1 / 1.5),
            run_time=0.8,
            rate_func=smooth,
        )

        # Normalize (important)
        self.remove(t1)
        t1 = Text("We’re", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR)
        self.add(t1)

        self.wait(0.3)

        # -----------------------------
        # 2. "excited" POP + RECENTER
        # -----------------------------
        g12 = VGroup(t1, t2).arrange(RIGHT, buff=0.25).move_to(ORIGIN)

        t1_target_pos = g12[0].get_center()
        t2_target_pos = g12[1].get_center()

        t2.scale(0.1)
        t2.move_to(t2_target_pos)
        self.add(t2)

        self.play(
            t1.animate.move_to(t1_target_pos),
            t2.animate.scale(12),
            run_time=1.5,
            rate_func=there_and_back_with_pause,
        )

        # Clean final state
        self.remove(t1, t2)
        t1 = Text("We’re", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR).move_to(t1_target_pos)
        t2 = Text("excited", font_size=FONT_SIZE, weight=BOLD, color=TEXT_COLOR).move_to(t2_target_pos)
        self.add(t1, t2)

        self.wait(0.3)

        # -----------------------------
        # 3. "to" SLIDE IN + RECENTER
        # -----------------------------
        g123 = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.25).move_to(ORIGIN)

        t1_final = g123[0].get_center()
        t2_final = g123[1].get_center()
        t3_final = g123[2].get_center()

        t3.move_to(t3_final + RIGHT * 2)
        t3.set_opacity(0)
        self.add(t3)

        self.play(
            t1.animate.move_to(t1_final),
            t2.animate.move_to(t2_final),
            t3.animate.move_to(t3_final).set_opacity(1),
            run_time=1.0,
            rate_func=rate_functions.ease_out_expo,
        )

        self.wait(1)