from manim import *

class IndicateText(Scene):
    def construct(self):
        text = Text("Welcome to Kplor")
        self.add(text)
        self.wait(0.5)

        self.play(Indicate(text))
        self.wait()

class IndicateShape(Scene):
    def construct(self):
        circle = Circle()
        

        self.add(circle)
        self.wait(0.5)

        self.play(Indicate(circle))
        self.wait()

class IndicateImage(Scene):
    def construct(self):
        img = ImageMobject("example.png")
        img.set_width(4)   # 🔑 always size images explicitly

        self.add(img)
        self.wait(0.5)

        self.play(Indicate(img))
        self.wait()
