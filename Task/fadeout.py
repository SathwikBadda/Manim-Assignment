from manim import *

class FadeOutText(Scene):
    def construct(self):
        text = Text("Goodbye Kplor")
        self.add(text)
        self.wait(0.5)
        self.play(FadeOut(text))
        self.wait()

class FadeOutShape(Scene):
    def construct(self):
        square = Square(fill_color=BLUE, fill_opacity=1)
        self.add(square)
        self.wait(0.5)
        self.play(FadeOut(square))
        self.wait()

class FadeOutImage(Scene):
    def construct(self):
        img = ImageMobject("img1.png").scale(2)
        self.add(img)
        self.wait(0.5)
        self.play(FadeOut(img))
        self.wait()
