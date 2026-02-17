from manim import *

class FlashPoint(Scene):
    def construct(self):
        dot = Dot()
        self.add(dot)
        self.play(Flash(dot))
        self.wait()


class FlashShape(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.wait(0.5)
        self.play(Flash(circle))
        self.wait()



class FlashText(Scene):
    def construct(self):
        text = Text("IMPORTANT")
        self.add(text)
        self.wait(0.5)
        self.play(Flash(text))
        self.wait()


class FlashImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)
        self.add(img)
        self.wait(0.5)
        self.play(Flash(img))
        self.wait()
