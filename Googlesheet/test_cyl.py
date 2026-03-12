from manim import *
class TestCyl(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=18 * DEGREES, theta=-90 * DEGREES)
        cards = [Rectangle(width=3.4, height=4.8, fill_opacity=0.8, fill_color=c) 
                 for c in [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]]
        
        R = 6.5
        
        # Bending flat mobjects into a cylinder
        def bend_into_cylinder(mob, radius=R):
            # A completely flat card in the XY plane centered at ORIGIN
            # X coordinate becomes the arc length along the cylinder perimeter
            # Angle theta = x / radius
            # New X = radius * sin(theta)
            # New Z = radius - radius * cos(theta)
            # Y remains Y
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
            
        angles = [0, -60 * DEGREES, -120 * DEGREES, -180 * DEGREES, -240 * DEGREES, -300 * DEGREES]
        
        for i, card in enumerate(cards):
            card.move_to(ORIGIN)
            bend_into_cylinder(card, R)
            
            # Now the card is bent. We rotate it to its spot on the cylinder.
            # Z=0 is the front surface of the cylinder, center is at Z=-R
            card.shift(OUT * -R)
            card.rotate(-angles[i], axis=UP, about_point=np.array([0,0,-R]))
            self.add(card)
            
        carousel = VGroup(*cards)
        self.play(Rotate(carousel, angle=75*DEGREES, axis=UP, about_point=np.array([0,0,-R])))
        self.wait(1)

