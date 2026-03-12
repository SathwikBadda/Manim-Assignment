from manim import *

class AlignTest(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        cards = [Rectangle(width=3.4, height=4.8) for _ in range(3)]
        
        # Test original gap mapping relative to the newly requested simple 3-card layout
        R = 5.5 / 2 # Use a slightly tighter rotation radius for just 3 models
        
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
        for g, a in zip(cards, angles):
            tgt = g.copy()
            tgt.move_to(ORIGIN)
            bend_into_cylinder(tgt, R)
            tgt.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            points.add(tgt)
            
        self.add(points)
        self.move_camera(phi=15*DEGREES)
        self.wait(1)

