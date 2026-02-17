from manim import *

class UnwriteText(Scene):
    def construct(self):
        text = Text("Welcome to Kplor", font_size=48)
        self.play(Write(text))
        self.wait(0.5)
        self.play(Unwrite(text))
        self.wait()

class UnwriteShape(Scene):
    def construct(self):
        circle = Circle(radius=2)
        self.play(Write(circle))
        self.wait(0.5)
        self.play(Unwrite(circle))
        self.wait()
