from manim import *

class AnimatedBoundaryText(Scene):
    def construct(self):
        text = Text("Welcome to Kplor", font_size=48)
        boundary = AnimatedBoundary(text)
        self.add(text)
        self.add(boundary)
        self.wait(3)

class AnimatedBoundaryShape(Scene):
    def construct(self):
        circle = Circle(radius=2)
        boundary = AnimatedBoundary(circle, colors=[BLUE, GREEN, YELLOW])
        self.add(circle, boundary)
        self.wait(3)


## for image animatedBoundary doesnt work in v0.19.0 we will get an error of stroke_width 
class AnimatedBoundaryImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(2)

        boundary = AnimatedBoundary(img)   
           

        self.add(img, boundary)
        self.wait(3)

