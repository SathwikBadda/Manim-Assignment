from manim import *

class TestDepth(ThreeDScene):
    def construct(self):
        R = 5.5 / 2
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

        c1 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=RED, fill_opacity=1), Text("1"))
        c2 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=GREEN, fill_opacity=1), Text("2"))
        c3 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=BLUE, fill_opacity=1), Text("3"))
        
        cards = [c1, c2, c3]
        angles = [0, -120 * DEGREES, -240 * DEGREES]

        for g, a in zip(cards, angles):
            bend_into_cylinder(g, R)
            g.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            self.add(g)
            
        def print_z(mob):
            mob.set_z_index(mob.get_center()[2])
            print(f"Card z_index: {mob.z_index:.2f}, Z-coord: {mob.get_center()[2]:.2f}")
            
        for card in cards:
            card.add_updater(print_z)

        self.set_camera_orientation(phi=18*DEGREES, theta=-65*DEGREES)
        
        self.play(
            *[Rotate(c, angle=360 * DEGREES, axis=UP, about_point=np.array([0, 0, -R])) for c in cards],
            run_time=0.5,
            rate_func=linear,
        )
