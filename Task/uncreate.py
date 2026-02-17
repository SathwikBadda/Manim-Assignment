from manim import *

class UncreateCircle(Scene):
    def construct(self):
        circle=Circle(radius=2)
        self.play(Create(circle))
        self.wait(0.5)
        self.play(Uncreate(circle,rate_func=linear))
        self.wait(2)

class UncreateText(Scene):
    def construct(self):
        text = Text("Welcome to Kplor", font_size=48)
        self.play(Create(text))
        self.wait(0.5)
        self.play(Uncreate(text))
        self.wait(1)



