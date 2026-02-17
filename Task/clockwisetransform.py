from manim import *

class ClockwiseTransformShape(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.add(square)
        self.wait(0.5)

        self.play(ClockwiseTransform(square, circle))
        self.wait()


class ClockwiseTransformText(Scene):
    def construct(self):
        t1 = Text("Hello")
        t2 = Text("World")

        self.add(t1)
        self.play(ClockwiseTransform(t1, t2))
        self.wait()
