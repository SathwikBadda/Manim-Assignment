from manim import *

class CircumscribeText(Scene):
    def construct(self):
        text = Text("WELCOME TO KPLOR")
        self.add(text)
        self.wait(0.5)
        self.play(Circumscribe(text))
        self.wait()

class CircumscribeShape(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.wait(0.5)
        self.play(Circumscribe(circle))
        self.wait()

class CircumscribeImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.add(img)
        self.wait(0.5)
        self.play(Circumscribe(img))
        self.wait()
