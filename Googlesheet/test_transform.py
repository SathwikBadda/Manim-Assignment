from manim import *

class TestTransform(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        
        c_left   = Rectangle(width=3.4, height=4.8, fill_color=BLUE, fill_opacity=0.8).shift(LEFT*4)
        c_main   = Rectangle(width=3.4, height=4.8, fill_color=RED, fill_opacity=0.8)
        c_right  = Rectangle(width=3.4, height=4.8, fill_color=GREEN, fill_opacity=0.8).shift(RIGHT*4)
        
        self.add(c_left, c_main, c_right)
        self.wait(1)
        
        R = 5.5
        def bend_into_cylinder(mob, radius=R):
            def map_point(p):
                x, y, z = p
                theta = x / radius
                return np.array([
                    radius * np.sin(theta),
                    y,
                    radius * np.cos(theta) - radius + z
                ])
            mob.apply_function(map_point)
            return mob
            
        cards = [c_main, c_right, c_left]
        angles = [0, -60 * DEGREES, -300 * DEGREES]
        
        target_group = VGroup()
        for g in cards:
            tgt = g.copy()
            tgt.move_to(ORIGIN)
            target_group.add(tgt)
            
        anims = []
        for g, tgt, a in zip(cards, target_group, angles):
            bend_into_cylinder(tgt, R)
            tgt.shift(OUT * -R)
            tgt.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            anims.append(Transform(g, tgt))
            
        self.move_camera(phi=15*DEGREES, theta=-90*DEGREES, zoom=0.85, added_anims=anims, run_time=2)
        self.wait(1)

