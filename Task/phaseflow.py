from manim import *
import numpy as np



class PhaseFlowWithTrajectory(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4,4], y_range=[-4,4])
        self.add(plane)

        def vf(pos):
            x, y = pos[:2]
            return np.array([y, -x, 0])

        field = ArrowVectorField(vf)
        self.add(field)

        dot = Dot(point=plane.c2p(2, 0), color=RED)

        path = TracedPath(dot.get_center, stroke_color=YELLOW)

        self.add(dot, path)

        self.play(
            MoveAlongPath(
                dot,
                Circle(radius=2),
                run_time=6,
                rate_func=linear
            )
        )
        self.wait()

class TimeDependentPhaseFlow(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-4,4], y_range=[-4,4])
        self.add(plane)

        t = ValueTracker(0)

        def vf(pos):
            x, y = pos[:2]
            a = np.cos(t.get_value())
            return np.array([y, -a * x, 0])

        field = always_redraw(
            lambda: ArrowVectorField(vf, color=BLUE)
        )

        label = always_redraw(
            lambda: MathTex(
                f"a(t) = {np.cos(t.get_value()):.2f}"
            ).to_edge(UP)
        )

        self.add(field, label)
        self.play(t.animate.set_value(2*PI), run_time=6)
        self.wait()


class ColorShiftPhaseFlow(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        t = ValueTracker(0)

        def vf(pos):
            x, y = pos[:2]
            a = np.sin(t.get_value())
            return np.array([y, -a*x, 0])

        field = always_redraw(
            lambda: ArrowVectorField(
                vf,
                color=interpolate_color(
                    BLUE, PURPLE,
                    (np.sin(t.get_value()) + 1) / 2
                ),
                opacity=0.3
            )
        )

        self.add(field)
        self.play(t.animate.set_value(2*PI), run_time=8, rate_func=linear)
        self.wait()