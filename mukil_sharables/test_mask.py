from manim import *

def create_star_mask(scale_factor=1.0):
    pts = [
        np.array([-30, -30, 0]),
        np.array([30, -30, 0]),
        np.array([30, 30, 0]),
        np.array([-30, 30, 0]),
        np.array([-30, -30, 0]), # close outer
    ]
    # inner boundary (CW)
    star_pts = []
    outer = 3.2 * scale_factor
    inner = 0.45 * scale_factor
    for i in range(4):
        # outer spike
        angle_out = - (i * 90 * DEGREES - 90 * DEGREES) # negative to go CW
        star_pts.append(np.array([outer * np.cos(angle_out),
                                outer * np.sin(angle_out), 0]))
        # inner notch
        angle_in = angle_out - 45 * DEGREES
        star_pts.append(np.array([inner * np.cos(angle_in),
                                inner * np.sin(angle_in), 0]))
    
    star_pts.append(star_pts[0]) # close inner
    pts.extend(star_pts)
    return Polygon(*pts, fill_color="#050b14", fill_opacity=0.95, stroke_width=0)

class TestMask(Scene):
    def construct(self):
        c = Circle(radius=2, color=RED, fill_opacity=1)
        self.add(c)
        mask = create_star_mask(1.0)
        self.add(mask)
        self.wait(1)
        # Try scaling
        self.play(mask.animate.scale(3), run_time=1)
        self.wait(1)

