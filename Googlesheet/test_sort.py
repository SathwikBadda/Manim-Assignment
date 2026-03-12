from manim import *

class TestSort(ThreeDScene):
    def construct(self):
        # ════════════════════════════════════════════════════════════════
        # PHASE 2 — CAROUSEL FORMATION + EXTRA CARDS + 3D CAMERA TILT
        # ════════════════════════════════════════════════════════════════

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

        cards = [Rectangle(width=3.4, height=4.8, fill_opacity=1, fill_color=c) for c in [RED, GREEN, BLUE]]
        angles = [0, -120 * DEGREES, -240 * DEGREES]

        target_group = VGroup()
        for g, a in zip(cards, angles):
            tgt = g.copy()
            tgt.move_to(ORIGIN)
            target_group.add(tgt)
            
        anims = []
        for g, tgt, a in zip(cards, target_group, angles):
            bend_into_cylinder(tgt, R)
            tgt.rotate(-a, axis=UP, about_point=np.array([0, 0, -R]))
            anims.append(Transform(g, tgt))

        carousel = VGroup(*cards)
        self.add(carousel)
        
        # KEY FIX: Continuous Z-Index sorting based on camera distance
        # Manim draws objects in the order they appear in the VGroup.
        # So we just re-sort the VGroup's sub-mobjects every frame based on their Z coordinate.
        def z_index_sort(mob):
            # The cards are [0,1,2]. We sort them by the Z-coordinate of their center point.
            # In Manim's 3D, deeper objects have a more negative Z coordinate.
            # We want to draw deep objects first, so we sort ascending by Z.
            mob.submobjects.sort(key=lambda m: m.get_center()[2])
            
        carousel.add_updater(z_index_sort)

        self.move_camera(
            phi=18 * DEGREES,
            theta=-65 * DEGREES,
            zoom=0.88,
            added_anims=anims,
            run_time=0.1
        )
        
        self.play(
            Rotate(carousel, angle=360 * DEGREES, axis=UP, about_point=np.array([0, 0, -R])),
            run_time=4.0,
            rate_func=linear,
        )

        
        self.wait(1.0)
