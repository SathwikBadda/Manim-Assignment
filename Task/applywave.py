from manim import *

class ApplyWaveShape(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyWave(square))
        self.wait()

class ApplyWaveText(Scene):
    def construct(self):
        text = Text("HELLO MANIM")
        self.play(ApplyWave(text))
        self.wait()


class ApplyWaveImage(Scene):
    def construct(self):
        img = ImageMobject("img3.png").scale(2)
        self.play(ApplyWave(img))
        self.wait()
