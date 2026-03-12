from manim import *

class TestIndiv(ThreeDScene):
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
            self.add(g)
            
        for card in cards:
            card.add_updater(lambda mob: mob.set_z_index(-mob.get_center()[2])) # Note: deeper is more negative, we want drawn last so less negative z is higher z_index? Actually Manim sorts by z_index ascending. So highest z_index drawn last (in front). 
            # In 3D, camera is at +Z looking at -Z. High Z coordinate means closer to camera, so drawn last.
            # wait, mob.get_center()[2] is its Z coordinate.
            # Z=0 is center. Z=+1 is close. So z_index = mob.get_center()[2] works perfectly.
            # Wait, earlier I did `lamda mob: mob.set_z_index(mob.get_center()[2])` and that worked.

        self.set_camera_orientation(phi=18*DEGREES, theta=-65*DEGREES)
        
        self.play(
            *[Rotate(c, angle=360 * DEGREES, axis=UP, about_point=np.array([0, 0, -R])) for c in cards],
            run_time=2.0,
            rate_func=linear,
        )
        self.wait(1.0)
