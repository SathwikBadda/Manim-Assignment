from manim import *

class CounterclockwiseTransformShape(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.add(square)
        self.wait(0.5)

        self.play(CounterclockwiseTransform(square, circle))
        self.wait()


class CounterclockwiseTransformText(Scene):
    def construct(self):
        t1 = Text("A")
        t2 = Text("B")

        self.add(t1)
        self.play(CounterclockwiseTransform(t1, t2))
        self.wait()
