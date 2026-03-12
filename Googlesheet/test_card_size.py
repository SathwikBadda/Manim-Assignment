from manim import *

class TestSize(ThreeDScene):
    def construct(self):
        c_main_bg = Rectangle(width=3.4, height=4.8)
        pr_main = Rectangle(width=2.4, height=0.5).shift(DOWN * 2)
        grp_main = VGroup(c_main_bg, pr_main)
        
        # Test original gap mapping relative to the newly requested simple 3-card layout
        R = 5.5 / 2
        
        # Helper to bend flat cards
        def bend_into_cylinder(mob, radius=R):
            def map_point(p):
                x, y, z = p
                theta = x / radius
                 
                # Original unbent logic gives:
                return np.array([
                    radius * np.sin(theta),
                    y,
                    radius * np.cos(theta) - radius + z
                ])
            mob.apply_function(map_point)
            return mob
            
        points = VGroup()
        angles = [0, -120 * DEGREES, -240 * DEGREES] # 3 evenly spaced slots
        for a in angles:
            tgt = grp_main.copy()
            tgt.move_to(ORIGIN)
            bend_into_cylinder(tgt, R)
            tgt.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            points.add(tgt)
            
        self.set_camera_orientation(phi=15*DEGREES, theta=-90*DEGREES)
        self.add(points)
        self.wait(1)

