from manim import *

class GrowArrowBasic(Scene):
    def construct(self):
        arrow = Arrow(LEFT, RIGHT)

        self.play(GrowArrow(arrow))
        self.wait()

