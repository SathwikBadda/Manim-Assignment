from manim import *
class TestCar(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=18 * DEGREES, theta=-90 * DEGREES)
        cards = [Rectangle(width=3.4, height=4.8, fill_opacity=0.8, fill_color=c) 
                 for c in [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]]
        
        angles = [0, -60 * DEGREES, -120 * DEGREES, -180 * DEGREES, -240 * DEGREES, -300 * DEGREES]
        R = 6.5
        
        for i, (card, angle) in enumerate(zip(cards, angles)):
            x = R * np.sin(angle)
            z = R * np.cos(angle) - R 
            card.move_to(np.array([x, 0, z]))
            card.rotate(-angle, axis=UP)
            
            # The cards also need a slight curve to actually look like a cylinder
            # But we can just use flat cards like original for now
            self.add(card)
            
        # Rotate whole
        carousel = VGroup(*cards)
        self.play(Rotate(carousel, angle=75*DEGREES, axis=UP, about_point=np.array([0,0,-R])))
        self.wait(1)

