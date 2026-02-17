from manim import *

class CreateCircle(Scene):
    def construct(self):
        circle =Circle(radius=2)
        self.play(Create(circle,run_time=3))
        self.wait()

class CreateText(Scene):
    def construct(self):
        text=Text("Welcome to Kplor ",font_size=64)
        self.play(Create(text))
        self.wait()

 ## Create cant be applied for image it fails because it doesnt work on pixels it only works on stokes and VMobject       
class Createimage(Scene):
    def construct(self):
        img=ImageMobject("example.png").scale(2)
        self.play(Create(img))
                  