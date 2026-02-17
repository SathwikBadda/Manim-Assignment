from manim import *

class RemoveTextLBL(Scene):
    def construct(self):
        text = Text("Welcome to Kplor", font_size=48)
        self.add(text)
        self.wait(0.5)
        self.play(RemoveTextLetterByLetter(text))
        self.wait()
