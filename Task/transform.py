from manim import *

class TransformShape(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.add(square)
        self.wait(0.5)

        self.play(Transform(square, circle))
        self.wait()

class TransformText(Scene):
    def construct(self):
        text1 = Text("HELLO")
        text2 = Text("WORLD")

        self.add(text1)
        self.wait(0.5)

        self.play(Transform(text1, text2))
        self.wait()



class FadeTransformImages(Scene):
    def construct(self):
        img1 = ImageMobject("img3.png").set_width(4)
        img2 = ImageMobject("img2.png").set_width(4)

        self.add(img1)
        self.wait(0.5)

        self.play(FadeTransform(img1, img2))
        self.wait()
