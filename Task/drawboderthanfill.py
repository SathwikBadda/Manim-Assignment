from manim import *

class DrawBorderThenFillCircle(Scene):
    def construct(self):
        circle = Circle(
            stroke_color=BLUE,
            fill_color=BLUE,
            fill_opacity=1
        )

        self.play(DrawBorderThenFill(circle))
        self.wait()

class DrawText(Scene):
    def construct(self):
        text = Text(
            "Welcome to Kplor",
            fill_color=YELLOW,
            fill_opacity=1
        )
        self.play(DrawBorderThenFill(text))
        self.wait()
