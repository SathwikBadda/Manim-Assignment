from manim import *

class GrowFromCenterShape(Scene):
    def construct(self):
        circle = Circle()
        self.play(GrowFromCenter(circle))
        self.wait()


class GrowFromCenterText(Scene):
    def construct(self):
        text = Text("Kplor")
        self.play(GrowFromCenter(text))
        self.wait()


class GrowFromCenterImage(Scene):
    def construct(self):
        img = ImageMobject("img1.png").scale(2)
        self.play(GrowFromCenter(img))
        self.wait()
