from manim import *

class GrowFromLeft(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        self.play(GrowFromEdge(rect, LEFT))
        self.wait()
        
class GrowFromEdgeLeftText(Scene):
    def construct(self):
        text = Text("HELLO")
        self.play(GrowFromEdge(text, LEFT))
        self.wait()

class GrowFromEdgeLeftImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.play(GrowFromEdge(img, LEFT))
        self.wait()
