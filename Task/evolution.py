from manim import *
import numpy as np

class Human(VGroup):
    """
    A Manim VGroup representing a simple Stick Figure Human.
    
    Attributes:
        head (Circle): The head.
        body (Line): The torso.
        left/right_leg (Line): Legs.
        left/right_arm (Line): Arms in a neutral position.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HEAD_COLOR = "#FFD1A4" # Skin tone
        self.BODY_COLOR = "#4A90E2" # Blue clothes
        
        self.head = None
        self.body = None
        self.left_leg = None
        self.right_leg = None
        self.left_arm = None
        self.right_arm = None
        
        self._build_parts()
        
    def _build_parts(self):
        # Simply geometry: Circle for head, Lines for body/limbs
        self.head = Circle(
            radius=0.15,
            fill_color=self.HEAD_COLOR,
            fill_opacity=1,
            stroke_color="#8B6F47",
            stroke_width=2
        ).shift(UP * 0.4)
        
        self.body = Line(
            start=UP * 0.25,
            end=DOWN * 0.3,
            stroke_color=self.BODY_COLOR,
            stroke_width=6
        )
        
        self.left_leg = Line(
            start=DOWN * 0.3,
            end=LEFT * 0.15 + DOWN * 0.65,
            stroke_color=self.BODY_COLOR,
            stroke_width=5
        )
        
        self.right_leg = Line(
            start=DOWN * 0.3,
            end=RIGHT * 0.15 + DOWN * 0.65,
            stroke_color=self.BODY_COLOR,
            stroke_width=5
        )
        
        self.left_arm = Line(
            start=UP * 0.1,
            end=LEFT * 0.2 + DOWN * 0.1,
            stroke_color=self.BODY_COLOR,
            stroke_width=4
        )
        
        self.right_arm = Line(
            start=UP * 0.1,
            end=RIGHT * 0.2 + DOWN * 0.1,
            stroke_color=self.BODY_COLOR,
            stroke_width=4
        )
        
        self.add(self.head, self.body, self.left_leg, self.right_leg, self.left_arm, self.right_arm)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Human")

class Bicycle(VGroup):
    """
    A Manim VGroup representing a Bicycle.
    
    Attributes:
        front/back_wheel (VGroup): Wheels with spokes.
        frame (VGroup): The triangular frame structure.
        seat (RoundedRectangle): The seat.
        handlebars (VGroup): Steering handles.
        crank (VGroup): Pedals and crankset.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TIRE_COLOR = "#2C3E50"
        self.RIM_COLOR = "#ECF0F1"
        self.FRAME_COLOR = "#E74C3C" # Red frame
        self.SEAT_COLOR = "#2C3E50"
        self.HANDLE_COLOR = "#2C3E50"
        
        self.front_wheel = None
        self.back_wheel = None
        self.frame = None
        self.seat = None
        self.handlebars = None
        self.crank = None
        
        self._build_parts()
        
    def _build_parts(self):
        wheel_radius = 0.35
        tire_thickness = 0.08
        
        def create_wheel():
            """Helper to create a unified wheel object"""
            tire = Annulus(
                inner_radius=wheel_radius - tire_thickness,
                outer_radius=wheel_radius,
                fill_color=self.TIRE_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            rim = Circle(
                radius=wheel_radius - tire_thickness,
                stroke_color=self.RIM_COLOR,
                stroke_width=2,
                fill_opacity=0
            )
            # Create spokes using rotated lines
            spokes = VGroup(*[
                Line(
                    start=ORIGIN,
                    end=UP * (wheel_radius - tire_thickness),
                    stroke_color=self.RIM_COLOR,
                    stroke_width=1
                ).rotate(angle)
                for angle in np.arange(0, TAU, TAU/8)
            ])
            return VGroup(tire, rim, spokes)

        self.front_wheel = create_wheel().shift(RIGHT * 0.75)
        self.back_wheel = create_wheel().shift(LEFT * 0.75)
        
        # Frame Geometry Points
        bottom_bracket = ORIGIN + DOWN * 0.15
        seat_post_top = ORIGIN + UP * 0.4
        head_tube_top = RIGHT * 0.55 + UP * 0.45
        rear_axle = self.back_wheel.get_center()
        
        # Bicycle Diamond Frame
        self.frame = VGroup(
            Line(bottom_bracket, seat_post_top, stroke_color=self.FRAME_COLOR, stroke_width=8), # Seat tube
            Line(head_tube_top, bottom_bracket, stroke_color=self.FRAME_COLOR, stroke_width=8), # Down tube
            Line(seat_post_top, head_tube_top, stroke_color=self.FRAME_COLOR, stroke_width=8),   # Top tube
            Line(seat_post_top, rear_axle, stroke_color=self.FRAME_COLOR, stroke_width=6),       # Seat stays
            Line(bottom_bracket, rear_axle, stroke_color=self.FRAME_COLOR, stroke_width=6),      # Chain stays
            Line(head_tube_top, self.front_wheel.get_center(), stroke_color=self.FRAME_COLOR, stroke_width=6) # Fork
        )
        
        # Seat
        self.seat = RoundedRectangle(
            width=0.3,
            height=0.1,
            corner_radius=0.05,
            fill_color=self.SEAT_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(seat_post_top + UP * 0.05 + LEFT * 0.05)
        
        # Handlebars
        self.handlebars = VGroup(
            Line(head_tube_top, head_tube_top + UP * 0.15, stroke_color=self.HANDLE_COLOR, stroke_width=6),
            Line(head_tube_top + UP * 0.15, head_tube_top + UP * 0.2 + RIGHT * 0.1, stroke_color=self.HANDLE_COLOR, stroke_width=6),
            Line(head_tube_top + UP * 0.15, head_tube_top + UP * 0.15 + LEFT * 0.15, stroke_color=self.HANDLE_COLOR, stroke_width=6)
        )
        
        # Crankset
        self.crank = VGroup(
            Circle(radius=0.08, fill_color="#7F8C8D", fill_opacity=1),
            Line(ORIGIN, DOWN * 0.15, stroke_color="#7F8C8D", stroke_width=4), # Crank arm
            Rectangle(width=0.1, height=0.04, fill_color="#BDC3C7", fill_opacity=1).shift(DOWN * 0.15) # Pedal
        ).shift(bottom_bracket)
        
        self.add(self.back_wheel, self.front_wheel, self.frame, self.seat, self.handlebars, self.crank)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Bicycle")


class Motorcycle(VGroup):
    """
    A Manim VGroup representing a Motorcycle.
    
    Attributes:
        front/back_wheel (VGroup): Thicker wheels.
        tank (RoundedRectangle): Fuel tank.
        seat (RoundedRectangle): Seat.
        engine (VGroup): Engine block with cooling fins.
        exhaust (Polygon): Exhaust pipe.
        headlight (Sector): Front light.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.TIRE_COLOR = "#2C3E50"
        self.RIM_COLOR = "#95A5A6"
        self.BODY_COLOR = "#E67E22" # Orange body
        self.SEAT_COLOR = "#2C3E50"
        self.ENGINE_COLOR = "#bdc3c7"
        self.EXHAUST_COLOR = "#7F8C8D"
        
        self.front_wheel = None
        self.back_wheel = None
        self.tank = None
        self.seat = None
        self.engine = None
        self.exhaust = None
        self.frame_connectors = None
        self.headlight = None
        self.handlebars = None
        
        self._build_parts()
        
    def _build_parts(self):
        wheel_radius = 0.35
        tire_thickness = 0.1 # Thicker tires than bicycle
        
        def create_moto_wheel():
            tire = Annulus(
                inner_radius=wheel_radius - tire_thickness,
                outer_radius=wheel_radius,
                fill_color=self.TIRE_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            rim = Circle(
                radius=0.15,
                fill_color=self.RIM_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            spokes = VGroup(*[
                Line(
                    start=ORIGIN,
                    end=UP * (wheel_radius - tire_thickness),
                    stroke_color=self.RIM_COLOR,
                    stroke_width=6
                ).rotate(angle)
                for angle in np.arange(0, TAU, TAU/5)
            ])
            return VGroup(tire, rim, spokes)

        self.front_wheel = create_moto_wheel().shift(RIGHT * 0.85)
        self.back_wheel = create_moto_wheel().shift(LEFT * 0.85)
        
        # Tank - Rounded rectangle for modern look
        self.tank = RoundedRectangle(
            width=0.7,
            height=0.35,
            corner_radius=0.1,
            fill_color=self.BODY_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 0.35)
        
        # Seat
        self.seat = RoundedRectangle(
            width=0.7,
            height=0.15,
            corner_radius=0.05,
            fill_color=self.SEAT_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.35 + UP * 0.28)
        
        # Engine block with cooling fins (lines)
        self.engine = VGroup(
            RoundedRectangle(
                width=0.5,
                height=0.4,
                corner_radius=0.05,
                fill_color=self.ENGINE_COLOR,
                fill_opacity=1,
                stroke_color="#7F8C8D",
                stroke_width=2
            ),
            *[Line(LEFT*0.2 + UP*y, RIGHT*0.2 + UP*y, stroke_color="#7F8C8D", stroke_width=1) 
              for y in np.linspace(-0.15, 0.15, 5)]
        ).shift(ORIGIN)
        
        # Frame connection lines
        self.frame_connectors = VGroup(
            Line(self.back_wheel.get_center(), UP * 0.25, stroke_color="#34495E", stroke_width=6),
            Line(self.front_wheel.get_center(), UP * 0.4 + RIGHT * 0.4, stroke_color="#34495E", stroke_width=6)
        )
        
        # Exhaust pipe
        self.exhaust = Polygon(
            LEFT * 0.2 + DOWN * 0.1,
            LEFT * 1.0 + DOWN * 0.1,
            LEFT * 1.0 + UP * 0.05,
            LEFT * 0.2 + UP * 0.05,
            fill_color=self.EXHAUST_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(DOWN * 0.1 + RIGHT * 0.1)
        
        # Headlight beam area
        self.headlight = Sector(
            radius=0.15,
            angle=PI,
            start_angle=-PI/2,
            fill_color="#F1C40F",
            fill_opacity=0.8,
            stroke_width=0
        ).shift(RIGHT * 0.65 + UP * 0.45)
        
        # Handlebars
        self.handlebars = Line(
            start=RIGHT * 0.45 + UP * 0.4,
            end=RIGHT * 0.35 + UP * 0.55,
            stroke_color="#34495E",
            stroke_width=5
        )

        self.add(
            self.back_wheel, self.front_wheel, 
            self.engine, self.exhaust, 
            self.frame_connectors, 
            self.tank, self.seat, self.headlight, self.handlebars
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Motorcycle")


class Car(VGroup):
    """
    A Manim VGroup representing a Car.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.CAR_BODY = "#E74C3C"
        self.CAR_DARK = "#C0392B"
        self.WHEEL_COLOR = "#2C3E50"
        self.WINDOW_COLOR = "#85C1E9"
        
        self.body = None
        self.roof = None
        self.front_wheel = None
        self.back_wheel = None
        self.left_window = None
        self.right_window = None
        
        self._build_parts()

    def _build_parts(self):
        # Wheels
        self.front_wheel = Circle(
            radius=0.25,
            fill_color=self.WHEEL_COLOR,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=3
        ).shift(RIGHT * 0.6 + DOWN * 0.35)
        
        self.back_wheel = Circle(
            radius=0.25,
            fill_color=self.WHEEL_COLOR,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=3
        ).shift(LEFT * 0.6 + DOWN * 0.35)
        
        # Main chassis
        self.body = RoundedRectangle(
            width=1.8,
            height=0.6,
            corner_radius=0.15,
            fill_color=self.CAR_BODY,
            fill_opacity=1,
            stroke_color=self.CAR_DARK,
            stroke_width=4
        )
        
        # Roof section
        self.roof = Polygon(
            LEFT * 0.4 + UP * 0.3,
            LEFT * 0.2 + UP * 0.6,
            RIGHT * 0.3 + UP * 0.6,
            RIGHT * 0.5 + UP * 0.3,
            fill_color=self.CAR_BODY,
            fill_opacity=1,
            stroke_color=self.CAR_DARK,
            stroke_width=4
        ).round_corners(radius=0.1)
        
        # Windows matching the roof slope
        self.left_window = Polygon(
            LEFT * 0.35 + UP * 0.35,
            LEFT * 0.2 + UP * 0.55,
            LEFT * 0.05 + UP * 0.55,
            LEFT * 0.05 + UP * 0.35,
            fill_color=self.WINDOW_COLOR,
            fill_opacity=0.7,
            stroke_width=0
        )
        
        self.right_window = Polygon(
            RIGHT * 0.05 + UP * 0.35,
            RIGHT * 0.05 + UP * 0.55,
            RIGHT * 0.25 + UP * 0.55,
            RIGHT * 0.45 + UP * 0.35,
            fill_color=self.WINDOW_COLOR,
            fill_opacity=0.7,
            stroke_width=0
        )
        
        self.add(self.body, self.roof, self.front_wheel, self.back_wheel, self.left_window, self.right_window)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Car")


class Boat(VGroup):
    """
    A Manim VGroup representing a Sailboat.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BOAT_COLOR = "#8B4513"
        self.SAIL_COLOR = "#ECF0F1"
        
        self.hull = None
        self.mast = None
        self.sail = None
        
        self._build_parts()
        
    def _build_parts(self):
        # Hull - Trapezoid
        hull_points = [
            LEFT * 0.6 + DOWN * 0.1,
            LEFT * 0.5 + DOWN * 0.4,
            RIGHT * 0.5 + DOWN * 0.4,
            RIGHT * 0.6 + DOWN * 0.1,
        ]
        self.hull = Polygon(
            *hull_points,
            fill_color=self.BOAT_COLOR,
            fill_opacity=1,
            stroke_color="#654321",
            stroke_width=3
        ).round_corners(radius=0.1)
        
        # Mast - Vertical line
        self.mast = Line(
            start=DOWN * 0.1,
            end=UP * 0.8,
            stroke_color=self.BOAT_COLOR,
            stroke_width=5
        )
        
        # Sail - Triangle
        self.sail = Polygon(
            ORIGIN + UP * 0.7,
            RIGHT * 0.4 + UP * 0.4,
            RIGHT * 0.4 + UP * 0.1,
            fill_color=self.SAIL_COLOR,
            fill_opacity=0.9,
            stroke_color="#BDC3C7",
            stroke_width=2
        )
        
        self.add(self.hull, self.mast, self.sail)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Boat")


class Ship(VGroup):
    """
    A Manim VGroup representing a Cargo Ship/Tanker.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HULL_BOTTOM_COLOR = "#E74C3C" # Waterline red
        self.HULL_TOP_COLOR = "#2C3E50"
        self.CABIN_COLOR = "#ECF0F1"
        self.CONTAINER_COLORS = ["#F1C40F", "#3498DB", "#E67E22"]
        
        self.hull_bottom = None
        self.hull_top = None
        self.cabin = None
        self.containers = None
        self.radar = None
        
        self._build_parts()

    def _build_parts(self):
        # Two-tone hull
        self.hull_bottom = Polygon(
            LEFT * 0.8 + DOWN * 0.4,
            RIGHT * 0.8 + DOWN * 0.4,
            RIGHT * 1.0 + DOWN * 0.1,
            LEFT * 0.9 + DOWN * 0.1,
            fill_color=self.HULL_BOTTOM_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        self.hull_top = Polygon(
            LEFT * 0.9 + DOWN * 0.1,
            RIGHT * 1.0 + DOWN * 0.1,
            RIGHT * 1.0 + UP * 0.2,
            LEFT * 0.9 + UP * 0.2,
            fill_color=self.HULL_TOP_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Cabin with windows
        self.cabin = VGroup(
            RoundedRectangle(width=0.4, height=0.5, corner_radius=0.05, fill_color=self.CABIN_COLOR, fill_opacity=1, stroke_width=0),
            RoundedRectangle(width=0.5, height=0.1, corner_radius=0.02, fill_color=self.CABIN_COLOR, fill_opacity=1, stroke_width=0).shift(UP * 0.25),
            VGroup(*[
                Rectangle(width=0.08, height=0.08, fill_color="#3498DB", fill_opacity=1, stroke_width=0).shift(LEFT * 0.12 + i * RIGHT * 0.12)
                for i in range(3)
            ]).shift(UP * 0.15)
        ).shift(RIGHT * 0.6 + UP * 0.45)
        
        # Cargo containers stacked
        self.containers = VGroup()
        for i in range(3):
            for j in range(2):
                if not (i == 2 and j == 1):
                    c = RoundedRectangle(
                        width=0.35, 
                        height=0.2, 
                        corner_radius=0.02,
                        fill_color=self.CONTAINER_COLORS[(i+j)%3], 
                        fill_opacity=1,
                        stroke_color=BLACK,
                        stroke_width=1
                    ).shift(LEFT * 0.6 + RIGHT * i * 0.38 + UP * 0.3 + UP * j * 0.2)
                    self.containers.add(c)
        
        self.radar = Line(UP*0.2, DOWN*0.1, stroke_width=2).shift(RIGHT * 0.6 + UP * 0.75)
        
        self.add(self.hull_bottom, self.hull_top, self.cabin, self.containers, self.radar)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Ship")


class Submarine(VGroup):
    """
    A Manim VGroup representing a Submarine.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SUB_COLOR = "#F39C12" # Traditional yellow submarine
        self.WINDOW_COLOR = "#3498DB"
        self.PERISCOPE_COLOR = "#7F8C8D"
        
        self.body = None
        self.tower = None
        self.periscope = None
        self.window1 = None
        self.window2 = None
        self.propeller = None
        
        self._build_parts()

    def _build_parts(self):
        # Body
        self.body = Ellipse(
            width=1.8,
            height=0.7,
            fill_color=self.SUB_COLOR,
            fill_opacity=1,
            stroke_color="#D68910",
            stroke_width=4
        )
        
        # Conning tower
        self.tower = RoundedRectangle(
            width=0.5,
            height=0.35,
            corner_radius=0.1,
            fill_color=self.SUB_COLOR,
            fill_opacity=1,
            stroke_color="#D68910",
            stroke_width=3
        ).shift(UP * 0.5)
        
        # Periscope
        self.periscope = Line(
            start=UP * 0.67,
            end=UP * 1.1,
            stroke_color=self.PERISCOPE_COLOR,
            stroke_width=4
        )
        
        # Portholes
        self.window1 = Circle(
            radius=0.12,
            fill_color=self.WINDOW_COLOR,
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(LEFT * 0.4)
        
        self.window2 = Circle(
            radius=0.12,
            fill_color=self.WINDOW_COLOR,
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.2)
        
        # Propeller blades
        self.propeller = Line(
            start=LEFT * 0.9 + UP * 0.15,
            end=LEFT * 0.9 + DOWN * 0.15,
            stroke_color=self.PERISCOPE_COLOR,
            stroke_width=3
        )
        
        self.add(self.body, self.tower, self.periscope, self.window1, self.window2, self.propeller)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Submarine")


class Bird(VGroup):
    """
    A Manim VGroup representing a stylized Bird.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BIRD_COLOR = "#3498DB"
        self.BEAK_COLOR = "#F39C12"
        
        self.body = None
        self.left_wing = None
        self.right_wing = None
        self.head = None
        self.beak = None
        
        self._build_parts()
        
    def _build_parts(self):
        self.body = Ellipse(
            width=0.5,
            height=0.3,
            fill_color=self.BIRD_COLOR,
            fill_opacity=1,
            stroke_color="#2980B9",
            stroke_width=3
        )
        
        # Wings created with Arcs for flapping look
        self.left_wing = Arc(
            radius=0.4,
            start_angle=PI/4,
            angle=PI/2,
            stroke_color=self.BIRD_COLOR,
            stroke_width=6
        ).shift(LEFT * 0.25 + UP * 0.05)
        
        self.right_wing = Arc(
            radius=0.4,
            start_angle=PI/4,
            angle=PI/2,
            stroke_color=self.BIRD_COLOR,
            stroke_width=6
        ).flip(RIGHT).shift(RIGHT * 0.25 + UP * 0.05)
        
        self.head = Circle(
            radius=0.12,
            fill_color=self.BIRD_COLOR,
            fill_opacity=1,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.3)
        
        self.beak = Polygon(
            RIGHT * 0.42,
            RIGHT * 0.55 + UP * 0.03,
            RIGHT * 0.55 + DOWN * 0.03,
            fill_color=self.BEAK_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        self.add(self.body, self.left_wing, self.right_wing, self.head, self.beak)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Bird")


class WrightPlane(VGroup):
    """
    A Manim VGroup representing a Wright Brothers Flyer.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.WOOD_COLOR = "#D35400"
        self.WING_COLOR = "#F5CBA7"
        
        self.wings = None
        self.struts = None
        self.elevator_frame = None
        self.elevator_surfaces = None
        self.rudder_frame = None
        self.rudder_surface = None
        self.pilot = None
        
        self._build_parts()
        
    def _build_parts(self):
        # Biplane main wings
        self.wings = VGroup(
            Line(LEFT*0.8 + UP*0.3, RIGHT*0.8 + UP*0.3, stroke_color=self.WOOD_COLOR, stroke_width=4), 
            Line(LEFT*0.8 + DOWN*0.3, RIGHT*0.8 + DOWN*0.3, stroke_color=self.WOOD_COLOR, stroke_width=4)
        )
        
        # Vertical struts between wings
        self.struts = VGroup(*[
            Line(UP*0.3 + RIGHT*x, DOWN*0.3 + RIGHT*x, stroke_color=self.WOOD_COLOR, stroke_width=2)
            for x in [-0.6, -0.2, 0.2, 0.6]
        ])
        
        # Forward Elevator (Canard wings)
        self.elevator_frame = VGroup(
            Line(RIGHT*0.8 + UP*0.3, RIGHT*1.6 + UP*0.1, stroke_color=self.WOOD_COLOR, stroke_width=2),
            Line(RIGHT*0.8 + DOWN*0.3, RIGHT*1.6 + DOWN*0.1, stroke_color=self.WOOD_COLOR, stroke_width=2)
        )
        
        self.elevator_surfaces = VGroup(
            Line(RIGHT*1.4, RIGHT*1.8, stroke_color=self.WING_COLOR, stroke_width=4).shift(UP*0.1),
            Line(RIGHT*1.4, RIGHT*1.8, stroke_color=self.WING_COLOR, stroke_width=4).shift(DOWN*0.1)
        )
        
        # Rear Rudder
        self.rudder_frame = VGroup(
            Line(LEFT*0.8 + UP*0.3, LEFT*1.4 + UP*0.1, stroke_color=self.WOOD_COLOR, stroke_width=2),
            Line(LEFT*0.8 + DOWN*0.3, LEFT*1.4 + DOWN*0.1, stroke_color=self.WOOD_COLOR, stroke_width=2)
        )
        self.rudder_surface = Line(UP*0.2, DOWN*0.2, stroke_color=self.WING_COLOR, stroke_width=4).shift(LEFT*1.4)
        
        self.pilot = Rectangle(width=0.3, height=0.15, fill_color=self.WOOD_COLOR, fill_opacity=1).shift(DOWN*0.22)
        
        self.add(self.wings, self.struts, self.elevator_frame, self.elevator_surfaces, self.rudder_frame, self.rudder_surface, self.pilot)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in WrightPlane")


class Airplane(VGroup):
    """
    A Manim VGroup representing a Classic Biplane.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FUSELAGE_COLOR = "#C0392B"
        self.WING_COLOR = "#ECF0F1"
        self.STRUT_COLOR = "#2C3E50"
        
        self.fuselage = None
        self.cockpit = None
        self.top_wing = None
        self.bottom_wing = None
        self.wing_struts = None
        self.tail = None
        self.gear = None
        self.propeller = None
        
        self._build_parts()

    def _build_parts(self):
        self.fuselage = RoundedRectangle(
            width=1.4,
            height=0.4,
            corner_radius=0.1,
            fill_color=self.FUSELAGE_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        self.cockpit = Sector(
            radius=0.2,
            angle=PI,
            start_angle=0,
            fill_color="#3498DB",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(UP * 0.2 + LEFT * 0.1)
        
        # Biplane wings
        self.top_wing = RoundedRectangle(
            width=1.6,
            height=0.15,
            corner_radius=0.05,
            fill_color=self.WING_COLOR,
            fill_opacity=1,
            stroke_color=self.STRUT_COLOR,
            stroke_width=2
        ).shift(UP * 0.35 + LEFT * 0.1)
        
        self.bottom_wing = RoundedRectangle(
            width=1.4,
            height=0.15,
            corner_radius=0.05,
            fill_color=self.WING_COLOR,
            fill_opacity=1,
            stroke_color=self.STRUT_COLOR,
            stroke_width=2
        ).shift(DOWN * 0.15 + LEFT * 0.1)
        
        self.wing_struts = VGroup(
            Line(UP*0.35 + LEFT*0.5, DOWN*0.15 + LEFT*0.5, stroke_color=self.STRUT_COLOR, stroke_width=3),
            Line(UP*0.35 + RIGHT*0.4, DOWN*0.15 + RIGHT*0.4, stroke_color=self.STRUT_COLOR, stroke_width=3)
        )
        
        self.tail = VGroup(
            Polygon(
                LEFT*0.7, LEFT*1.1 + UP*0.3, LEFT*0.8 + UP*0.3, LEFT*0.6,
                fill_color=self.FUSELAGE_COLOR, fill_opacity=1, stroke_width=0
            ), 
             Polygon(
                LEFT*0.7, LEFT*1.0 + DOWN*0.1, LEFT*1.0 + UP*0.1,
                fill_color=self.FUSELAGE_COLOR, fill_opacity=1, stroke_width=0
            ) 
        )
        
        # Landing gear
        self.gear = VGroup(
             Line(DOWN*0.2 + RIGHT*0.3, DOWN*0.4 + RIGHT*0.35, stroke_color=self.STRUT_COLOR, stroke_width=3),
             Circle(radius=0.1, fill_color="#2C3E50", fill_opacity=1).shift(DOWN*0.5 + RIGHT*0.35)
        )
        
        self.propeller = VGroup(
             Ellipse(width=0.1, height=0.8, fill_color="#7F8C8D", fill_opacity=0.8).shift(RIGHT * 0.75)
        )
        
        self.add(self.tail, self.fuselage, self.cockpit, self.bottom_wing, self.top_wing, self.wing_struts, self.gear, self.propeller)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Airplane")


class Jet(VGroup):
    """
    A Manim VGroup representing a Modern Fighter Jet.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.JET_COLOR = "#2C3E50" # Dark gray stealth color
        self.WING_COLOR = "#7F8C8D"
        self.ENGINE_COLOR = "#34495E"
        
        self.fuselage = None
        self.left_wing = None
        self.right_wing = None
        self.left_engine = None
        self.right_engine = None
        self.cockpit = None
        self.nose = None
        
        self._build_parts()
        
    def _build_parts(self):
        # Streamlined fuselage
        self.fuselage = RoundedRectangle(
            width=1.4,
            height=0.35,
            corner_radius=0.175,
            fill_color=self.JET_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=3
        )
        
        # Swept back wings
        self.left_wing = Polygon(
            LEFT * 0.2 + DOWN * 0.18,
            LEFT * 0.9 + DOWN * 0.3,
            LEFT * 0.3 + DOWN * 0.18,
            fill_color=self.WING_COLOR,
            fill_opacity=1,
            stroke_color="#5D6D7E",
            stroke_width=3
        )
        
        self.right_wing = Polygon(
            RIGHT * 0.2 + DOWN * 0.18,
            RIGHT * 0.9 + DOWN * 0.3,
            RIGHT * 0.3 + DOWN * 0.18,
            fill_color=self.WING_COLOR,
            fill_opacity=1,
            stroke_color="#5D6D7E",
            stroke_width=3
        )
        
        # Engines mounted under wings
        self.left_engine = Ellipse(
            width=0.15,
            height=0.25,
            fill_color=self.ENGINE_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=2
        ).shift(LEFT * 0.5 + DOWN * 0.35)
        
        self.right_engine = Ellipse(
            width=0.15,
            height=0.25,
            fill_color=self.ENGINE_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=2
        ).shift(RIGHT * 0.5 + DOWN * 0.35)
        
        self.cockpit = Circle(
            radius=0.1,
            fill_color="#3498DB",
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.5 + UP * 0.08)
        
        # Pointed nose cone
        self.nose = Polygon(
            RIGHT * 0.7,
            RIGHT * 0.95 + UP * 0.1,
            RIGHT * 0.95 + DOWN * 0.1,
            fill_color="#1A252F",
            fill_opacity=1,
            stroke_width=0
        )
        
        self.add(self.fuselage, self.left_wing, self.right_wing, self.left_engine, self.right_engine, self.cockpit, self.nose)

    def get_subcomponent(self, part_name: str):
        """Access subcomponents by name."""
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Jet")

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
         """Generalized animation helper that can be added to any of these classes."""
         component = self.get_subcomponent(part_name)
         if not component:
             return Wait(0.1)
         
         if animation_type == "Indicate":
            return Indicate(component, **kwargs)
         elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
         elif animation_type == "Flash":
             return Flash(component, **kwargs)
         else:
             return Wait(0.1)
