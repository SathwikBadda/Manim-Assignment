from manim import *

class SpinInShape(Scene):
    def construct(self):
        square = Square()
        self.play(SpinInFromNothing(square))
        self.wait()


class SpinInText(Scene):
    def construct(self):
        text = Text("Kplor")
        self.play(SpinInFromNothing(text))
        self.wait()


class SpinInImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(1.5)
        self.play(SpinInFromNothing(img))
        self.wait()
