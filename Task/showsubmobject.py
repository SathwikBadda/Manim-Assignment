from manim import *

class ShowTextOneByOne(Scene):
    def construct(self):
        text = Text("HELLO")

        self.play(ShowSubmobjectsOneByOne(text))
        self.wait()

class ShowShapesOneByOne(Scene):
    def construct(self):
        shapes = VGroup(
            Circle(),
            Square(),
            Triangle()
        ).arrange(RIGHT, buff=1.5)

        self.play(ShowSubmobjectsOneByOne(shapes))
        self.wait()

class ShowImagesOneByOne(Scene):
    def construct(self):
        imgs = Group(
            ImageMobject("img1.png").scale(0.5),
            ImageMobject("img2.png").scale(0.5),
            ImageMobject("img3.png").scale(0.5),
        ).arrange(RIGHT, buff=1)

        self.play(ShowSubmobjectsOneByOne(imgs))
        self.wait()
