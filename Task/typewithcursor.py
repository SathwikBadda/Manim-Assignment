from manim import *

class TypeWithCursorGlow(Scene):
    def construct(self):
        self.camera.background_color = "#020617"

        text = Text(
            "Building Beautiful Animations",
            font_size=48,
            color=BLUE_B
        ).set_glow_factor(0.6)

        cursor = Rectangle(
            height=text.height * 0.9,
            width=0.08,
            fill_color=BLUE_C,
            fill_opacity=1,
            stroke_width=0
        )

        self.play(
            TypeWithCursor(
                text,
                cursor,
                time_per_char=0.06
            )
        )

        self.wait()

