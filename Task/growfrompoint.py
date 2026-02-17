from manim import *

class GrowFromPointShape(Scene):
    def construct(self):
        circle = Circle(radius=1)

        self.play(GrowFromPoint(circle, ORIGIN))
        self.wait()


class GrowFromPointText(Scene):
    def construct(self):
        text = Text("HELLO")

        self.play(GrowFromPoint(text, UP * 3))
        self.wait()

class GrowFromPointImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(1.5)

        self.play(GrowFromPoint(img, DOWN * 3))
        self.wait()
