from manim import *

class GrowFromUp(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        self.play(GrowFromEdge(rect, UP))
        self.wait()
        
class GrowFromEdgeUpText(Scene):
    def construct(self):
        text = Text("HELLO")
        self.play(GrowFromEdge(text, UP))
        self.wait()

class GrowFromEdgeUpImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.play(GrowFromEdge(img, UP))
        self.wait()
