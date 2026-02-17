from manim import *

class GrowFromRight(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        self.play(GrowFromEdge(rect, RIGHT))
        self.wait()

class GrowFromEdgeRightText(Scene):
    def construct(self):
        text = Text("HELLO")
        self.play(GrowFromEdge(text, RIGHT))
        self.wait()

class GrowFromEdgeRightImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.play(GrowFromEdge(img, RIGHT))
        self.wait()
