from manim import *

class GrowFromEdgeDownShape(Scene):
    def construct(self):
        rect = Rectangle(height=3, width=2)
        self.play(GrowFromEdge(rect, DOWN))
        self.wait()


class GrowFromEdgeDownText(Scene):
    def construct(self):
        text = Text("HELLO")
        self.play(GrowFromEdge(text, DOWN))
        self.wait()

class GrowFromEdgeDownImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.play(GrowFromEdge(img, DOWN))
        self.wait()
