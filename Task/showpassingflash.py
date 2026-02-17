from manim import *



class ShowPassingFlashCircle(Scene):
    def construct(self):
        # Base circle (thin & dim)
        circle = Circle(
            radius=2,
            stroke_width=2,
            color=BLUE,
            stroke_opacity=0.3
        )

        self.add(circle)
        self.wait(0.5)

        # Flash copy (thick & bright)
        flash_circle = circle.copy()
        flash_circle.set_stroke(
            color=YELLOW,
            width=10,
            opacity=1
        )

        self.play(
            ShowPassingFlash(
                flash_circle,
                time_width=0.35
            ),
            run_time=2
        )

        self.wait()



class ShowPassingFlashText(Scene):
    def construct(self):
        text = Text("HELLO")
        self.add(text)
        self.wait(0.5)

        self.play(ShowPassingFlash(text.copy()))
        self.wait()


class ShowPassingFlashImageFixed(Scene):
    def construct(self):
        img = ImageMobject("example.png")
        img.set_width(4)

        border = SurroundingRectangle(img, color=YELLOW, stroke_width=4)

        self.add(img)
        self.wait(0.5)

        self.play(ShowPassingFlash(border))
        self.wait()

