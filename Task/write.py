from manim import *

class WriteText(Scene):
    def construct(self):
        
        text1 = Text("Hello")
        text2 = Text("World").next_to(text1, DOWN)
        self.play(Write(text1))
        self.play(Write(text2))
        
        self.wait(2)

class WriteCircle(Scene):
    def construct(self):
        circle = Circle(radius=2)
        self.play(Write(circle))
        self.wait()
