from manim import *

class RotateShape(Scene):
    def construct(self):
        square = Square()
        self.add(square)
        self.wait(0.5)

        self.play(Rotate(square, angle=PI/2))
        self.wait()

class RotateText(Scene):
    def construct(self):
        text = Text("ROTATE")
        self.add(text)
        self.wait(0.5)

        self.play(Rotate(text, angle=PI))
        self.wait()


class RotateImage(Scene):
    def construct(self):
        img = ImageMobject("example.png")
        img.set_width(3)

        self.add(img)
        self.wait(0.5)

        self.play(Rotate(img, angle=PI/4))
        self.wait()