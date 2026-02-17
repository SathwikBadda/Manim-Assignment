from manim import *

class WiggleText(Scene):
    def construct(self):
        text = Text("IMPORTANT")
        self.add(text)
        self.wait(0.5)
        self.play(Wiggle(text))
        self.wait()

class WiggleShape(Scene):
    def construct(self):
        circle = Circle()
        square = Square().shift(RIGHT * 3)

        self.add(circle, square)
        self.wait(0.5)
        self.play(Wiggle(circle))
        self.wait(0.5)
        self.play(Wiggle(square))
        self.wait()


class WiggleImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(0.5)

        self.add(img)
        self.wait(0.5)
        self.play(Wiggle(img))
        self.wait()
