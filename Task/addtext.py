from manim import *

class AddTextLBL(Scene):
    def construct(self):
        text = Text("Welcome to Kplor", font_size=48)
        self.play(AddTextLetterByLetter(text))
        self.wait()
