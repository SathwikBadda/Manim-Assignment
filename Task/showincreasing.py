from manim import *

class IncreasingText(Scene):
    def construct(self):
        text = Text("Welcome")

        self.play(ShowIncreasingSubsets(text))
        self.wait()

class IncreasingShapes(Scene):
    def construct(self):
        shapes = VGroup(
            Circle(),
            Square(),
            Triangle()
        ).arrange(RIGHT, buff=1)

        self.play(ShowIncreasingSubsets(shapes))
        self.wait()




class IncreasingImages(Scene):
    def construct(self):
        imgs = Group(
            ImageMobject("img1.png").scale(0.5),
            ImageMobject("img2.png").scale(0.5),
            ImageMobject("img3.png").scale(0.5),
        ).arrange(RIGHT, buff=1)

        self.play(ShowIncreasingSubsets(imgs))
        self.wait()

