from manim import *

class FocusOnText(Scene):
    def construct(self):
        text = Text("IMPORTANT POINT")
        self.add(text)
        self.wait(0.5)
        self.play(FocusOn(text))
        self.wait()

class FocusOnShape(Scene):
    def construct(self):
        circle = Circle()
        square = Square().shift(RIGHT * 3)

        self.add(circle, square)
        self.wait(0.5)
        self.play(FocusOn(circle))
        self.wait()

class FocusOnImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.add(img)
        self.wait(0.5)
        self.play(FocusOn(img))
        self.wait()
