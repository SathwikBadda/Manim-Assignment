from manim import *

class FadeInText(Scene):
    def construct(self):
        text = Text("Hello Kplor")
        self.play(FadeIn(text))
        self.wait()

class FadeInShape(Scene):
    def construct(self):
        circle = Circle(fill_color=BLUE, fill_opacity=1)
        self.play(FadeIn(circle))
        self.wait()


class FadeInImage(Scene):
    def construct(self):
        img = ImageMobject("img1.png").scale(2)
        self.play(FadeIn(img))
        self.wait()
