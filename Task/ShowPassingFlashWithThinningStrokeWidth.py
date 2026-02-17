from manim import *

class FlashThinText(Scene):
    def construct(self):
        text = Text(
            "ENERGY FLOW",
            stroke_width=2,
            color=BLUE
        )

        self.add(text)
        self.wait(0.5)

        flash = text.copy().set_stroke(
            color=YELLOW,
            width=8
        )

        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                flash,
                time_width=0.4
            ),
            run_time=2
        )

        self.wait()

class FlashThinCircle(Scene):
    def construct(self):
        circle = Circle(
            radius=2,
            color=BLUE,
            stroke_width=2,
            stroke_opacity=0.3
        )

        self.add(circle)
        self.wait(0.5)

        flash = circle.copy().set_stroke(
            color=YELLOW,
            width=10
        )

        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                flash,
                time_width=0.35
            ),
            run_time=2
        )

        self.wait()

class FlashThinImage(Scene):
    def construct(self):
        img = ImageMobject("example.png")
        img.set_width(4)

        border = SurroundingRectangle(
            img,
            color=BLUE,
            stroke_width=2
        )

        self.add(img, border)
        self.wait(0.5)

        flash_border = border.copy().set_stroke(
            color=YELLOW,
            width=10
        )

        self.play(
            ShowPassingFlashWithThinningStrokeWidth(
                flash_border,
                time_width=0.4
            ),
            run_time=2
        )

        self.wait()