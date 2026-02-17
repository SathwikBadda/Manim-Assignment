from manim import *

class TracedPathBasic(Scene):
    def construct(self):
        dot = Dot(LEFT * 4)

        path = TracedPath(
            dot.get_center,
            stroke_color=BLUE,
            stroke_width=4
        )

        self.add(path, dot)
        self.play(dot.animate.shift(RIGHT * 8), run_time=3)
        self.wait()



class TracedPathText(Scene):
    def construct(self):
        text = Text("Welcome to Kplor").shift(LEFT * 4)

        path = TracedPath(
            text.get_top,
            stroke_color=BLUE,
            stroke_width=4
        )

        self.add(path, text)
        self.play(text.animate.shift(RIGHT * 8), run_time=3)
        self.wait()



class TracedPathImage(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(1.5).shift(LEFT * 4)

        path = TracedPath(
            img.get_center,
            stroke_color=RED,
            stroke_width=4
        )

        self.add(path, img)
        self.play(img.animate.shift(RIGHT * 8), run_time=3)
        self.wait()


class TracedPathRotate(Scene):
    def construct(self):
        img = ImageMobject("example.png").scale(0.7).shift(RIGHT * 3)

        path = TracedPath(img.get_center, stroke_color=YELLOW)

        self.add(path, img)
        self.play(Rotate(img, angle=TAU, about_point=ORIGIN), run_time=4)
        self.wait()
