from manim import *

class MoveAlongPathShape(Scene):
    def construct(self):
        path = Circle(radius=2, color=BLUE)
        dot = Dot(color=YELLOW)

        self.add(path, dot)
        self.wait(0.5)

        self.play(
            MoveAlongPath(dot, path),
            run_time=4,
            rate_func=linear
        )

        self.wait()


class MoveAlongPathText(Scene):
    def construct(self):
        path = Arc(radius=2, angle=PI, color=BLUE)
        text = Text("HELLO").scale(0.7)

        self.add(path, text)
        self.wait(0.5)

        self.play(
            MoveAlongPath(text, path),
            run_time=3,
            rate_func=smooth
        )

        self.wait()


class MoveAlongPathImage(Scene):
    def construct(self):
        path = Circle(radius=2)
        img = ImageMobject("example.png")
        img.set_width(1.2)

        self.add(path, img)
        self.wait(0.5)

        self.play(
            MoveAlongPath(img, path),
            run_time=4,
            rate_func=linear
        )

        self.wait()