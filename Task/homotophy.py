from manim import *
import numpy as np

class HomotopyLineToSine(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI],
            y_range=[-2, 2],
            x_length=8,
            y_length=4
        )

        line = axes.plot(lambda x: 0, color=BLUE)
        sine = axes.plot(lambda x: np.sin(x), color=GREEN)

        self.play(Create(axes))
        self.play(Create(line))

        self.play(
            Transform(
                line,
                sine,
                rate_func=smooth,
                run_time=3
            )
        )
        self.wait()


class ExplicitHomotopy(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI],
            y_range=[-2, 2],
            x_length=8,
            y_length=4
        )

        t_tracker = ValueTracker(0)

        def homotopy_curve():
            t = t_tracker.get_value()
            return axes.plot(
                lambda x: (1 - t) * 0 + t * np.sin(x),
                color=YELLOW
            )

        curve = always_redraw(homotopy_curve)

        label = always_redraw(
            lambda: MathTex(
                f"H(x,t), \\; t={t_tracker.get_value():.2f}"
            ).to_edge(UP)
        )

        self.add(axes, curve, label)
        self.play(t_tracker.animate.set_value(1), run_time=4)
        self.wait()

