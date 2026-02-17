from manim import *

class ScreenRectangleBasic(Scene):
    def construct(self):
        screen_rect = ScreenRectangle(
            height=4,
            stroke_color=YELLOW,
            stroke_width=6
        )

        self.play(Create(screen_rect))
        self.wait(1)
        self.play(FadeOut(screen_rect))



class AutoFitTextInside(Scene):
    def construct(self):
        screen_rect = ScreenRectangle(height=3)

        inside_text = Text(
            "This text automatically fits inside the rectangle",
            font_size=48
        )

        inside_text.scale_to_fit_width(screen_rect.width * 0.9)
        inside_text.move_to(screen_rect)

        self.play(Create(screen_rect))
        self.play(FadeIn(inside_text))
        self.wait()



class TextOutsideScreenRectangle(Scene):
    def construct(self):
        screen_rect = ScreenRectangle(height=3)

        top_text = Text("Explanation", font_size=36).next_to(
            screen_rect, UP, buff=0.3
        )

        bottom_text = Text("Example / Note", font_size=32).next_to(
            screen_rect, DOWN, buff=0.3
        )

        self.play(Create(screen_rect))
        self.play(Write(top_text), Write(bottom_text))
        self.wait()


class InsideOutsideText(Scene):
    def construct(self):
        screen_rect = ScreenRectangle(height=2.5)

        inside_text = Text("E = mc²", font_size=56)
        inside_text.scale_to_fit_width(screen_rect.width * 0.8)
        inside_text.move_to(screen_rect)

        outside_text = Text(
            "Energy–Mass Relation",
            font_size=32
        ).next_to(screen_rect, UP)

        self.play(Create(screen_rect))
        self.play(Write(inside_text))
        self.play(FadeIn(outside_text))
        self.wait()