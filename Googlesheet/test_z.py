from manim import *

class TestZ(ThreeDScene):
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

        c1 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=RED, fill_opacity=1), Text("A"))
        c2 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=GREEN, fill_opacity=1))
        c3 = VGroup(Rectangle(width=3.4, height=4.8, fill_color=BLUE, fill_opacity=1))
        
        cards = [c1, c2, c3]
        angles = [0, -120 * DEGREES, -240 * DEGREES]

        for g, a in zip(cards, angles):
            bend_into_cylinder(g, R)
            g.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            
        carousel = VGroup(*cards)
        self.add(carousel)
        
        # KEY FIX: Assign native z_index property continuously
        for card in cards:
            card.add_updater(lambda mob: mob.set_z_index(mob.get_center()[2]))

        self.set_camera_orientation(phi=18*DEGREES, theta=-65*DEGREES)
        
        self.play(
            Rotate(carousel, angle=360 * DEGREES, axis=UP, about_point=np.array([0, 0, -R])),
            run_time=2.0,
            rate_func=linear,
        )
        self.wait(1.0)
