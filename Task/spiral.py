from manim import *
import numpy as np

class SpiralTracedPath(Scene):
    def construct(self):
        # --------------------------------
        # Create a moving point
        # --------------------------------
        dot = Dot(color=YELLOW)

        # --------------------------------
        # Traced path (records dot motion)
        # --------------------------------
        path = TracedPath(
            dot.get_center,
            stroke_color=BLUE,
            stroke_width=3
        )

        self.add(path, dot)

        # --------------------------------
        # Spiral motion updater
        # --------------------------------
        angle = 0

        def spiral_motion(mob, dt):
            nonlocal angle
            angle += 5 * dt                 # angular speed
            radius = 0.08 * angle            # spiral growth
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            mob.move_to([x, y, 0])

        dot.add_updater(spiral_motion)

        # --------------------------------
        # Run animation
        # --------------------------------
        self.wait(6)

        dot.remove_updater(spiral_motion)
        self.wait()
