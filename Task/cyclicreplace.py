from manim import *

class CyclicReplaceShapes(Scene):
    def construct(self):
        a = Circle().shift(LEFT * 3)
        b = Square()
        c = Triangle().shift(RIGHT * 3)

        self.add(a, b, c)
        self.wait(0.5)

        self.play(CyclicReplace(a, b, c))
        self.wait()

class CyclicReplaceText(Scene):
    def construct(self):
        t1 = Text("A").shift(LEFT * 3)
        t2 = Text("B")
        t3 = Text("C").shift(RIGHT * 3)

        self.add(t1, t2, t3)
        self.wait(0.5)

        self.play(CyclicReplace(t1, t2, t3))
        self.wait()


class CyclicReplaceImages(Scene):
    def construct(self):
        img1 = ImageMobject("example.png").set_width(2).shift(LEFT * 3)
        img2 = ImageMobject("img2.png").set_width(2)
        img3 = ImageMobject("img3.png").set_width(2).shift(RIGHT * 3)

        self.add(img1, img2, img3)
        self.wait(0.5)

        self.play(CyclicReplace(img1, img2, img3))
        self.wait()
