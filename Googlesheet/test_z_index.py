from manim import *

class TestScene(ThreeDScene):
    def construct(self):
        globe = Sphere(radius=2).set_fill(BLUE, opacity=1).set_stroke(width=0)
        globe.set_z_index(10)
        
        text = Text("Hello World", font_size=50)
        text.set_z_index(0)
        text.shift(UP * 0.5)
        
        self.play(FadeIn(globe))
        self.play(FadeIn(text))
        self.wait(1)
