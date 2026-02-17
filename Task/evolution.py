from manim import *
import numpy as np

class TransportationEvolution(Scene):
    def construct(self):
        # Set background color - soft sky gradient
        self.camera.background_color = "#E8F4F8"
        
        # Title
        title = Text(
            "Evolution of Transportation",
            font_size=42,
            color="#2C3E50",
            weight=BOLD
        ).to_edge(UP, buff=0.4)
        
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # ==================== LAND TRANSPORT ====================
        
        # Position: Bottom center
        land_pos = DOWN * 2
        
        # 1. Walking Human
        human = self.create_human()
        human.shift(land_pos)
        
        self.play(FadeIn(human, shift=LEFT), run_time=0.8)
        
        # Walking animation
        for _ in range(2):
            self.play(
                Rotate(human[2], angle=20 * DEGREES, about_point=human[2].get_top()),  # Left leg
                Rotate(human[3], angle=-20 * DEGREES, about_point=human[3].get_top()),  # Right leg
                run_time=0.3,
                rate_func=there_and_back
            )
        
        self.wait(0.3)
        
        # 2. Human → Bicycle
        bicycle = self.create_bicycle()
        bicycle.shift(land_pos)
        
        self.play(
            ReplacementTransform(human, bicycle),
            run_time=1.2,
            rate_func=smooth
        )
        
        # Bicycle wheels rotate
        self.play(
            Rotate(bicycle[0], angle=TAU),  # Front wheel
            Rotate(bicycle[1], angle=TAU),  # Back wheel
            run_time=1.0,
            rate_func=linear
        )
        
        self.wait(0.3)
        
        # 3. Bicycle → Motorcycle
        motorcycle = self.create_motorcycle()
        motorcycle.shift(land_pos)
        
        self.play(
            ReplacementTransform(bicycle, motorcycle),
            run_time=1.2,
            rate_func=smooth
        )
        
        # Motorcycle vibration
        for _ in range(3):
            self.play(
                motorcycle.animate.shift(UP * 0.03),
                run_time=0.1
            )
            self.play(
                motorcycle.animate.shift(DOWN * 0.03),
                run_time=0.1
            )
        
        self.wait(0.3)
        
        # 4. Motorcycle → Car
        car = self.create_car()
        car.shift(land_pos)
        
        self.play(
            ReplacementTransform(motorcycle, car),
            run_time=1.3,
            rate_func=smooth
        )
        
        # Car settles with bounce
        self.play(
            car.animate.shift(UP * 0.1),
            run_time=0.2
        )
        self.play(
            car.animate.shift(DOWN * 0.1),
            run_time=0.2
        )
        
        self.wait(0.3)
        
        # Move car down and dim
        self.play(
            car.animate.shift(DOWN * 0.5).set_opacity(0.4),
            run_time=0.8
        )
        
        # ==================== SEA TRANSPORT ====================
        
        # Position: Center
        sea_pos = DOWN * 0.5
        
        # 1. Boat
        boat = self.create_boat()
        boat.shift(sea_pos)
        
        self.play(FadeIn(boat, shift=RIGHT), run_time=0.8)
        
        # Floating animation
        def float_updater(mob, dt):
            mob.shift(UP * 0.15 * np.sin(self.renderer.time * 3) * dt)
        
        boat.add_updater(float_updater)
        self.wait(1.5)
        boat.remove_updater(float_updater)
        
        self.wait(0.3)
        
        # 2. Boat → Ship
        ship = self.create_ship()
        ship.shift(sea_pos)
        
        self.play(
            ReplacementTransform(boat, ship),
            run_time=1.3,
            rate_func=smooth
        )
        
        # Smoke animation
        smoke = self.create_smoke()
        smoke.shift(sea_pos + UP * 1.2)
        
        self.play(
            FadeIn(smoke, shift=UP * 0.3, scale=0.8),
            run_time=0.8
        )
        self.play(
            FadeOut(smoke, shift=UP * 0.5),
            run_time=0.8
        )
        
        self.wait(0.3)
        
        # 3. Ship → Submarine
        submarine = self.create_submarine()
        submarine.shift(sea_pos)
        
        self.play(
            ReplacementTransform(ship, submarine),
            run_time=1.3,
            rate_func=smooth
        )
        
        # Submarine submerges
        self.play(
            submarine.animate.shift(DOWN * 0.3),
            run_time=0.8,
            rate_func=smooth
        )
        
        self.wait(0.3)
        
        # Move submarine up and dim
        self.play(
            submarine.animate.shift(UP * 0.8).set_opacity(0.4),
            run_time=0.8
        )
        
        # ==================== AIR TRANSPORT ====================
        
        # Position: Top center
        air_pos = UP * 1.5
        
        # 1. Wright Brothers Plane
        wright_plane = self.create_wright_plane()
        wright_plane.shift(air_pos)
        
        self.play(FadeIn(wright_plane, shift=DOWN), run_time=0.8)
        
        # No propeller animation for static/side-view plane
        self.wait(2.0)
        
        self.wait(0.3)
        
        # 2. Wright Plane → Airplane
        airplane = self.create_airplane()
        airplane.shift(air_pos)
        
        self.play(
            ReplacementTransform(wright_plane, airplane),
            run_time=1.3,
            rate_func=smooth
        )
        
        # Propeller rotation
        self.play(
            Rotate(airplane[5], angle=4 * TAU),  # Propeller
            run_time=1.2,
            rate_func=linear
        )
        
        self.wait(0.3)
        
        # 3. Airplane → Jet
        jet = self.create_jet()
        jet.shift(air_pos)
        
        self.play(
            ReplacementTransform(airplane, jet),
            run_time=1.3,
            rate_func=smooth
        )
        
        # Speed lines
        speed_lines = self.create_speed_lines()
        speed_lines.shift(air_pos + LEFT * 1.5)
        
        self.play(
            FadeIn(speed_lines, shift=LEFT),
            run_time=0.5
        )
        self.play(
            FadeOut(speed_lines, shift=LEFT * 2),
            run_time=0.5
        )
        
        self.wait(0.3)
        
        # Jet accelerates upward and off-screen
        self.play(
            jet.animate.shift(UP * 6 + RIGHT * 2).rotate(30 * DEGREES),
            run_time=2.0,
            rate_func=smooth
        )
        
        self.wait(1)
        
        # Fade out remaining objects
        self.play(
            FadeOut(car),
            FadeOut(submarine),
            FadeOut(title),
            run_time=0.8
        )
        
        self.wait(0.5)
    
    # ==================== LAND TRANSPORT CREATORS ====================
    
    def create_human(self):
        """Creates a simple stick figure"""
        HEAD_COLOR = "#FFD1A4"
        BODY_COLOR = "#4A90E2"
        
        head = Circle(
            radius=0.15,
            fill_color=HEAD_COLOR,
            fill_opacity=1,
            stroke_color="#8B6F47",
            stroke_width=2
        ).shift(UP * 0.4)
        
        body = Line(
            start=UP * 0.25,
            end=DOWN * 0.3,
            stroke_color=BODY_COLOR,
            stroke_width=6
        )
        
        left_leg = Line(
            start=DOWN * 0.3,
            end=LEFT * 0.15 + DOWN * 0.65,
            stroke_color=BODY_COLOR,
            stroke_width=5
        )
        
        right_leg = Line(
            start=DOWN * 0.3,
            end=RIGHT * 0.15 + DOWN * 0.65,
            stroke_color=BODY_COLOR,
            stroke_width=5
        )
        
        left_arm = Line(
            start=UP * 0.1,
            end=LEFT * 0.2 + DOWN * 0.1,
            stroke_color=BODY_COLOR,
            stroke_width=4
        )
        
        right_arm = Line(
            start=UP * 0.1,
            end=RIGHT * 0.2 + DOWN * 0.1,
            stroke_color=BODY_COLOR,
            stroke_width=4
        )
        
        return VGroup(head, body, left_leg, right_leg, left_arm, right_arm)
    
    def create_bicycle(self):
        """Creates a detailed vector-style bicycle"""
        # Colors
        TIRE_COLOR = "#2C3E50"  # Dark grey/black
        RIM_COLOR = "#ECF0F1"   # Light grey/white
        FRAME_COLOR = "#E74C3C" # Red
        SEAT_COLOR = "#2C3E50"
        HANDLE_COLOR = "#2C3E50"
        
        # Dimensions
        wheel_radius = 0.35
        tire_thickness = 0.08
        
        # --- Wheels ---
        def create_wheel():
            tire = Annulus(
                inner_radius=wheel_radius - tire_thickness,
                outer_radius=wheel_radius,
                fill_color=TIRE_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            rim = Circle(
                radius=wheel_radius - tire_thickness,
                stroke_color=RIM_COLOR,
                stroke_width=2,
                fill_opacity=0
            )
            spokes = VGroup(*[
                Line(
                    start=ORIGIN,
                    end=UP * (wheel_radius - tire_thickness),
                    stroke_color=RIM_COLOR,
                    stroke_width=1
                ).rotate(angle)
                for angle in np.arange(0, TAU, TAU/8)
            ])
            return VGroup(tire, rim, spokes)

        front_wheel = create_wheel().shift(RIGHT * 0.75)
        back_wheel = create_wheel().shift(LEFT * 0.75)
        
        # --- Frame ---
        # Main triangle points
        bottom_bracket = ORIGIN + DOWN * 0.15
        seat_post_top = ORIGIN + UP * 0.4
        head_tube_top = RIGHT * 0.55 + UP * 0.45
        rear_axle = back_wheel.get_center()
        
        # Frame tubes
        frame = VGroup(
            # Seat tube
            Line(bottom_bracket, seat_post_top, stroke_color=FRAME_COLOR, stroke_width=8),
            # Down tube
            Line(head_tube_top, bottom_bracket, stroke_color=FRAME_COLOR, stroke_width=8),
            # Top tube
            Line(seat_post_top, head_tube_top, stroke_color=FRAME_COLOR, stroke_width=8),
            # Seat stays
            Line(seat_post_top, rear_axle, stroke_color=FRAME_COLOR, stroke_width=6),
            # Chain stays
            Line(bottom_bracket, rear_axle, stroke_color=FRAME_COLOR, stroke_width=6),
            # Fork
            Line(head_tube_top, front_wheel.get_center(), stroke_color=FRAME_COLOR, stroke_width=6)
        )
        
        # --- Components ---
        # Seat
        seat = RoundedRectangle(
            width=0.3,
            height=0.1,
            corner_radius=0.05,
            fill_color=SEAT_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(seat_post_top + UP * 0.05 + LEFT * 0.05)
        
        # Handlebars
        handlebars = VGroup(
            Line(head_tube_top, head_tube_top + UP * 0.15, stroke_color=HANDLE_COLOR, stroke_width=6), # Stem
            Line(head_tube_top + UP * 0.15, head_tube_top + UP * 0.2 + RIGHT * 0.1, stroke_color=HANDLE_COLOR, stroke_width=6),
            Line(head_tube_top + UP * 0.15, head_tube_top + UP * 0.15 + LEFT * 0.15, stroke_color=HANDLE_COLOR, stroke_width=6) # Bar
        )
        
        # Crankset
        crank = VGroup(
            Circle(radius=0.08, fill_color="#7F8C8D", fill_opacity=1),
            Line(ORIGIN, DOWN * 0.15, stroke_color="#7F8C8D", stroke_width=4), # Crank arm
            Rectangle(width=0.1, height=0.04, fill_color="#BDC3C7", fill_opacity=1).shift(DOWN * 0.15) # Pedal
        ).shift(bottom_bracket)
        
        return VGroup(back_wheel, front_wheel, frame, seat, handlebars, crank)
    
    def create_motorcycle(self):
        """Creates a detailed vector-style motorcycle"""
        # Colors
        TIRE_COLOR = "#2C3E50"
        RIM_COLOR = "#95A5A6"
        BODY_COLOR = "#E67E22"  # Orange-ish/Yellow
        SEAT_COLOR = "#2C3E50"
        ENGINE_COLOR = "#bdc3c7"
        EXHAUST_COLOR = "#7F8C8D"
        
        # Dimensions
        wheel_radius = 0.35
        tire_thickness = 0.1
        
        # --- Wheels ---
        def create_moto_wheel():
            tire = Annulus(
                inner_radius=wheel_radius - tire_thickness,
                outer_radius=wheel_radius,
                fill_color=TIRE_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            # Mag wheel style
            rim = Circle(
                radius=0.15,
                fill_color=RIM_COLOR,
                fill_opacity=1,
                stroke_width=0
            )
            spokes = VGroup(*[
                Line(
                    start=ORIGIN,
                    end=UP * (wheel_radius - tire_thickness),
                    stroke_color=RIM_COLOR,
                    stroke_width=6
                ).rotate(angle)
                for angle in np.arange(0, TAU, TAU/5)
            ])
            return VGroup(tire, rim, spokes)

        front_wheel = create_moto_wheel().shift(RIGHT * 0.85)
        back_wheel = create_moto_wheel().shift(LEFT * 0.85)
        
        # --- Body ---
        # Main body shape (tank + side panel)
        body_points = [
            LEFT * 0.4 + UP * 0.2,   # Seat start
            RIGHT * 0.3 + UP * 0.2,  # Seat end / Tank start
            RIGHT * 0.6 + UP * 0.5,  # Tank top front
            RIGHT * 0.3 + UP * 0.5,  # Tank top back
            LEFT * 0.4 + UP * 0.4,   # Tail top
        ]
        
        # Tank
        tank = RoundedRectangle(
            width=0.7,
            height=0.35,
            corner_radius=0.1,
            fill_color=BODY_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(RIGHT * 0.25 + UP * 0.35)
        
        # Seat
        seat = RoundedRectangle(
            width=0.7,
            height=0.15,
            corner_radius=0.05,
            fill_color=SEAT_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(LEFT * 0.35 + UP * 0.28)
        
        # Engine block
        engine = VGroup(
            RoundedRectangle(
                width=0.5,
                height=0.4,
                corner_radius=0.05,
                fill_color=ENGINE_COLOR,
                fill_opacity=1,
                stroke_color="#7F8C8D",
                stroke_width=2
            ),
            # Cooling fins
            *[Line(LEFT*0.2 + UP*y, RIGHT*0.2 + UP*y, stroke_color="#7F8C8D", stroke_width=1) 
              for y in np.linspace(-0.15, 0.15, 5)]
        ).shift(ORIGIN)
        
        # Frame connection
        frame_connectors = VGroup(
            Line(back_wheel.get_center(), UP * 0.25, stroke_color="#34495E", stroke_width=6),
            Line(front_wheel.get_center(), UP * 0.4 + RIGHT * 0.4, stroke_color="#34495E", stroke_width=6) # Forks
        )
        
        # Exhaust
        exhaust = Polygon(
            LEFT * 0.2 + DOWN * 0.1,
            LEFT * 1.0 + DOWN * 0.1,
            LEFT * 1.0 + UP * 0.05,
            LEFT * 0.2 + UP * 0.05,
            fill_color=EXHAUST_COLOR,
            fill_opacity=1,
            stroke_width=0
        ).shift(DOWN * 0.1 + RIGHT * 0.1)
        
        # Headlight
        headlight = Sector(
    radius=0.15,
            angle=PI,
            start_angle=-PI/2,
            fill_color="#F1C40F",
            fill_opacity=0.8,
            stroke_width=0
        ).shift(RIGHT * 0.65 + UP * 0.45)
        
        # Handlebars
        handlebars = Line(
            start=RIGHT * 0.45 + UP * 0.4,
            end=RIGHT * 0.35 + UP * 0.55,
            stroke_color="#34495E",
            stroke_width=5
        )

        return VGroup(
            back_wheel, front_wheel, 
            engine, exhaust, 
            frame_connectors, 
            tank, seat, headlight, handlebars
        )
    
    def create_car(self):
        """Creates a car"""
        CAR_BODY = "#E74C3C"
        CAR_DARK = "#C0392B"
        WHEEL_COLOR = "#2C3E50"
        WINDOW_COLOR = "#85C1E9"
        
        # Wheels
        front_wheel = Circle(
            radius=0.25,
            fill_color=WHEEL_COLOR,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=3
        ).shift(RIGHT * 0.6 + DOWN * 0.35)
        
        back_wheel = Circle(
            radius=0.25,
            fill_color=WHEEL_COLOR,
            fill_opacity=1,
            stroke_color=BLACK,
            stroke_width=3
        ).shift(LEFT * 0.6 + DOWN * 0.35)
        
        # Body
        body = RoundedRectangle(
            width=1.8,
            height=0.6,
            corner_radius=0.15,
            fill_color=CAR_BODY,
            fill_opacity=1,
            stroke_color=CAR_DARK,
            stroke_width=4
        )
        
        # Roof
        roof_points = [
            LEFT * 0.4 + UP * 0.3,
            LEFT * 0.2 + UP * 0.6,
            RIGHT * 0.3 + UP * 0.6,
            RIGHT * 0.5 + UP * 0.3,
        ]
        roof = Polygon(
            *roof_points,
            fill_color=CAR_BODY,
            fill_opacity=1,
            stroke_color=CAR_DARK,
            stroke_width=4
        ).round_corners(radius=0.1)
        
        # Windows
        left_window = Polygon(
            LEFT * 0.35 + UP * 0.35,
            LEFT * 0.2 + UP * 0.55,
            LEFT * 0.05 + UP * 0.55,
            LEFT * 0.05 + UP * 0.35,
            fill_color=WINDOW_COLOR,
            fill_opacity=0.7,
            stroke_width=0
        )
        
        right_window = Polygon(
            RIGHT * 0.05 + UP * 0.35,
            RIGHT * 0.05 + UP * 0.55,
            RIGHT * 0.25 + UP * 0.55,
            RIGHT * 0.45 + UP * 0.35,
            fill_color=WINDOW_COLOR,
            fill_opacity=0.7,
            stroke_width=0
        )
        
        return VGroup(body, roof, front_wheel, back_wheel, left_window, right_window)
    
    # ==================== SEA TRANSPORT CREATORS ====================
    
    def create_boat(self):
        """Creates a simple boat"""
        BOAT_COLOR = "#8B4513"
        SAIL_COLOR = "#ECF0F1"
        
        # Hull
        hull_points = [
            LEFT * 0.6 + DOWN * 0.1,
            LEFT * 0.5 + DOWN * 0.4,
            RIGHT * 0.5 + DOWN * 0.4,
            RIGHT * 0.6 + DOWN * 0.1,
        ]
        hull = Polygon(
            *hull_points,
            fill_color=BOAT_COLOR,
            fill_opacity=1,
            stroke_color="#654321",
            stroke_width=3
        ).round_corners(radius=0.1)
        
        # Mast
        mast = Line(
            start=DOWN * 0.1,
            end=UP * 0.8,
            stroke_color=BOAT_COLOR,
            stroke_width=5
        )
        
        # Sail
        sail = Polygon(
            ORIGIN + UP * 0.7,
            RIGHT * 0.4 + UP * 0.4,
            RIGHT * 0.4 + UP * 0.1,
            fill_color=SAIL_COLOR,
            fill_opacity=0.9,
            stroke_color="#BDC3C7",
            stroke_width=2
        )
        
        return VGroup(hull, mast, sail)
    
    def create_ship(self):
        """Creates a detailed cargo ship"""
        HULL_BOTTOM_COLOR = "#E74C3C"  # Red bottom
        HULL_TOP_COLOR = "#2C3E50"     # Dark top
        CABIN_COLOR = "#ECF0F1"        # White/light grey
        CONTAINER_COLORS = ["#F1C40F", "#3498DB", "#E67E22"] # Yellow, Blue, Orange
        
        # Hull
        hull_bottom = Polygon(
            LEFT * 0.8 + DOWN * 0.4,
            RIGHT * 0.8 + DOWN * 0.4,
            RIGHT * 1.0 + DOWN * 0.1,
            LEFT * 0.9 + DOWN * 0.1,
            fill_color=HULL_BOTTOM_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        hull_top = Polygon(
            LEFT * 0.9 + DOWN * 0.1,
            RIGHT * 1.0 + DOWN * 0.1,
            RIGHT * 1.0 + UP * 0.2,
            LEFT * 0.9 + UP * 0.2,
            fill_color=HULL_TOP_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Cabin / Bridge
        cabin = VGroup(
            RoundedRectangle(width=0.4, height=0.5, corner_radius=0.05, fill_color=CABIN_COLOR, fill_opacity=1, stroke_width=0),
            RoundedRectangle(width=0.5, height=0.1, corner_radius=0.02, fill_color=CABIN_COLOR, fill_opacity=1, stroke_width=0).shift(UP * 0.25), # Roof
            # Windows
            VGroup(*[
                Rectangle(width=0.08, height=0.08, fill_color="#3498DB", fill_opacity=1, stroke_width=0).shift(LEFT * 0.12 + i * RIGHT * 0.12)
                for i in range(3)
            ]).shift(UP * 0.15)
        ).shift(RIGHT * 0.6 + UP * 0.45)
        
        # Containers
        containers = VGroup()
        for i in range(3): # Stacks
            for j in range(2): # Height
                if not (i == 2 and j == 1): # Skip one to make it uneven
                    c = RoundedRectangle(
                        width=0.35, 
                        height=0.2, 
                        corner_radius=0.02,
                        fill_color=CONTAINER_COLORS[(i+j)%3], 
                        fill_opacity=1,
                        stroke_color=BLACK,
                        stroke_width=1
                    ).shift(LEFT * 0.6 + RIGHT * i * 0.38 + UP * 0.3 + UP * j * 0.2)
                    containers.add(c)
        
        # Small details
        radar = Line(UP*0.2, DOWN*0.1, stroke_width=2).shift(RIGHT * 0.6 + UP * 0.75)
        
        return VGroup(hull_bottom, hull_top, cabin, containers, radar)
    
    def create_smoke(self):
        """Creates smoke puffs"""
        SMOKE_COLOR = "#BDC3C7"
        
        smoke = VGroup()
        for i in range(3):
            puff = Circle(
                radius=0.15 - i * 0.03,
                fill_color=SMOKE_COLOR,
                fill_opacity=0.6 - i * 0.15,
                stroke_width=0
            ).shift(UP * i * 0.2)
            smoke.add(puff)
        
        return smoke
    
    def create_submarine(self):
        """Creates a submarine"""
        SUB_COLOR = "#F39C12"
        WINDOW_COLOR = "#3498DB"
        PERISCOPE_COLOR = "#7F8C8D"
        
        # Main body - elongated capsule
        body = Ellipse(
            width=1.8,
            height=0.7,
            fill_color=SUB_COLOR,
            fill_opacity=1,
            stroke_color="#D68910",
            stroke_width=4
        )
        
        # Conning tower
        tower = RoundedRectangle(
            width=0.5,
            height=0.35,
            corner_radius=0.1,
            fill_color=SUB_COLOR,
            fill_opacity=1,
            stroke_color="#D68910",
            stroke_width=3
        ).shift(UP * 0.5)
        
        # Periscope
        periscope = Line(
            start=UP * 0.67,
            end=UP * 1.1,
            stroke_color=PERISCOPE_COLOR,
            stroke_width=4
        )
        
        # Windows
        window1 = Circle(
            radius=0.12,
            fill_color=WINDOW_COLOR,
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(LEFT * 0.4)
        
        window2 = Circle(
            radius=0.12,
            fill_color=WINDOW_COLOR,
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.2)
        
        # Propeller
        propeller = Line(
            start=LEFT * 0.9 + UP * 0.15,
            end=LEFT * 0.9 + DOWN * 0.15,
            stroke_color=PERISCOPE_COLOR,
            stroke_width=3
        )
        
        return VGroup(body, tower, periscope, window1, window2, propeller)
    
    # ==================== AIR TRANSPORT CREATORS ====================
    
    def create_bird(self):
        """Creates a simple bird"""
        BIRD_COLOR = "#3498DB"
        BEAK_COLOR = "#F39C12"
        
        # Body
        body = Ellipse(
            width=0.5,
            height=0.3,
            fill_color=BIRD_COLOR,
            fill_opacity=1,
            stroke_color="#2980B9",
            stroke_width=3
        )
        
        # Left wing
        left_wing = Arc(
            radius=0.4,
            start_angle=PI/4,
            angle=PI/2,
            stroke_color=BIRD_COLOR,
            stroke_width=6
        ).shift(LEFT * 0.25 + UP * 0.05)
        
        # Right wing
        right_wing = Arc(
            radius=0.4,
            start_angle=PI/4,
            angle=PI/2,
            stroke_color=BIRD_COLOR,
            stroke_width=6
        ).flip(RIGHT).shift(RIGHT * 0.25 + UP * 0.05)
        
        # Head
        head = Circle(
            radius=0.12,
            fill_color=BIRD_COLOR,
            fill_opacity=1,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.3)
        
        # Beak
        beak = Polygon(
            RIGHT * 0.42,
            RIGHT * 0.55 + UP * 0.03,
            RIGHT * 0.55 + DOWN * 0.03,
            fill_color=BEAK_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        return VGroup(body, left_wing, right_wing, head, beak)
    
    def create_wright_plane(self):
        """Creates a Wright Brothers style flyer"""
        WOOD_COLOR = "#D35400"
        WING_COLOR = "#F5CBA7"
        
        # Side view: Wings are lines/thin rects
        # 1. Main Wings (Biplane)
        # Assuming facing RIGHT
        wings = VGroup(
            Line(LEFT*0.8 + UP*0.3, RIGHT*0.8 + UP*0.3, stroke_color=WOOD_COLOR, stroke_width=4), # Top
            Line(LEFT*0.8 + DOWN*0.3, RIGHT*0.8 + DOWN*0.3, stroke_color=WOOD_COLOR, stroke_width=4) # Bottom
        )
        
        # 2. Struts (Vertical connectors)
        struts = VGroup(*[
            Line(UP*0.3 + RIGHT*x, DOWN*0.3 + RIGHT*x, stroke_color=WOOD_COLOR, stroke_width=2)
            for x in [-0.6, -0.2, 0.2, 0.6]
        ])
        
        # 3. Elevator (Canard) - In front (RIGHT side for consistency with other vehicles)
        # Structure extending forward
        elevator_frame = VGroup(
            Line(RIGHT*0.8 + UP*0.3, RIGHT*1.6 + UP*0.1, stroke_color=WOOD_COLOR, stroke_width=2),
            Line(RIGHT*0.8 + DOWN*0.3, RIGHT*1.6 + DOWN*0.1, stroke_color=WOOD_COLOR, stroke_width=2)
        )
        elevator_surfaces = VGroup(
            Line(RIGHT*1.4, RIGHT*1.8, stroke_color=WING_COLOR, stroke_width=4).shift(UP*0.1),
            Line(RIGHT*1.4, RIGHT*1.8, stroke_color=WING_COLOR, stroke_width=4).shift(DOWN*0.1)
        )
        
        # 4. Rudder - In back (LEFT side)
        rudder_frame = VGroup(
            Line(LEFT*0.8 + UP*0.3, LEFT*1.4 + UP*0.1, stroke_color=WOOD_COLOR, stroke_width=2),
            Line(LEFT*0.8 + DOWN*0.3, LEFT*1.4 + DOWN*0.1, stroke_color=WOOD_COLOR, stroke_width=2)
        )
        rudder_surface = Line(UP*0.2, DOWN*0.2, stroke_color=WING_COLOR, stroke_width=4).shift(LEFT*1.4)
        
        # 5. Pilot / Engine (Visual mass in center)
        pilot = Rectangle(width=0.3, height=0.15, fill_color=WOOD_COLOR, fill_opacity=1).shift(DOWN*0.22)
        
        return VGroup(wings, struts, elevator_frame, elevator_surfaces, rudder_frame, rudder_surface, pilot)
    
    def create_airplane(self):
        """Creates a classic biplane"""
        FUSELAGE_COLOR = "#C0392B"
        WING_COLOR = "#ECF0F1"
        STRUT_COLOR = "#2C3E50"
        
        # Fuselage
        fuselage = RoundedRectangle(
            width=1.4,
            height=0.4,
            corner_radius=0.1,
            fill_color=FUSELAGE_COLOR,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Cockpit
        cockpit = Sector(
            radius=0.2,
            angle=PI,
            start_angle=0,
            fill_color="#3498DB",
            fill_opacity=0.6,
            stroke_width=0
        ).shift(UP * 0.2 + LEFT * 0.1)
        
        # Wings (Biplane)
        top_wing = RoundedRectangle(
            width=1.6,
            height=0.15,
            corner_radius=0.05,
            fill_color=WING_COLOR,
            fill_opacity=1,
            stroke_color=STRUT_COLOR,
            stroke_width=2
        ).shift(UP * 0.35 + LEFT * 0.1)
        
        bottom_wing = RoundedRectangle(
            width=1.4,
            height=0.15,
            corner_radius=0.05,
            fill_color=WING_COLOR,
            fill_opacity=1,
            stroke_color=STRUT_COLOR,
            stroke_width=2
        ).shift(DOWN * 0.15 + LEFT * 0.1)
        
        # Struts
        wing_struts = VGroup(
            Line(UP*0.35 + LEFT*0.5, DOWN*0.15 + LEFT*0.5, stroke_color=STRUT_COLOR, stroke_width=3),
            Line(UP*0.35 + RIGHT*0.4, DOWN*0.15 + RIGHT*0.4, stroke_color=STRUT_COLOR, stroke_width=3)
        )
        
        # Tail
        tail = VGroup(
            Polygon(
                LEFT*0.7, LEFT*1.1 + UP*0.3, LEFT*0.8 + UP*0.3, LEFT*0.6,
                fill_color=FUSELAGE_COLOR, fill_opacity=1, stroke_width=0
            ), # Vertical
             Polygon(
                LEFT*0.7, LEFT*1.0 + DOWN*0.1, LEFT*1.0 + UP*0.1,
                fill_color=FUSELAGE_COLOR, fill_opacity=1, stroke_width=0
            ) # Horizontal
        )
        
        # Landing Gear
        gear = VGroup(
             Line(DOWN*0.2 + RIGHT*0.3, DOWN*0.4 + RIGHT*0.35, stroke_color=STRUT_COLOR, stroke_width=3),
             Circle(radius=0.1, fill_color="#2C3E50", fill_opacity=1).shift(DOWN*0.5 + RIGHT*0.35)
        )
        
        # Propeller
        propeller = VGroup(
             Ellipse(width=0.1, height=0.8, fill_color="#7F8C8D", fill_opacity=0.8).shift(RIGHT * 0.75)
        )
        
        return VGroup(tail, fuselage, cockpit, bottom_wing, top_wing, wing_struts, gear, propeller)
    
    def create_jet(self):
        """Creates a modern jet"""
        JET_COLOR = "#2C3E50"
        WING_COLOR = "#7F8C8D"
        ENGINE_COLOR = "#34495E"
        
        # Fuselage - sleeker
        fuselage = RoundedRectangle(
            width=1.4,
            height=0.35,
            corner_radius=0.175,
            fill_color=JET_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=3
        )
        
        # Sharp wings
        left_wing = Polygon(
            LEFT * 0.2 + DOWN * 0.18,
            LEFT * 0.9 + DOWN * 0.3,
            LEFT * 0.3 + DOWN * 0.18,
            fill_color=WING_COLOR,
            fill_opacity=1,
            stroke_color="#5D6D7E",
            stroke_width=3
        )
        
        right_wing = Polygon(
            RIGHT * 0.2 + DOWN * 0.18,
            RIGHT * 0.9 + DOWN * 0.3,
            RIGHT * 0.3 + DOWN * 0.18,
            fill_color=WING_COLOR,
            fill_opacity=1,
            stroke_color="#5D6D7E",
            stroke_width=3
        )
        
        # Engines under wings
        left_engine = Ellipse(
            width=0.15,
            height=0.25,
            fill_color=ENGINE_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=2
        ).shift(LEFT * 0.5 + DOWN * 0.35)
        
        right_engine = Ellipse(
            width=0.15,
            height=0.25,
            fill_color=ENGINE_COLOR,
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=2
        ).shift(RIGHT * 0.5 + DOWN * 0.35)
        
        # Cockpit
        cockpit = Circle(
            radius=0.1,
            fill_color="#3498DB",
            fill_opacity=0.8,
            stroke_color="#2980B9",
            stroke_width=2
        ).shift(RIGHT * 0.5 + UP * 0.08)
        
        # Nose cone
        nose = Polygon(
            RIGHT * 0.7,
            RIGHT * 0.95 + UP * 0.1,
            RIGHT * 0.95 + DOWN * 0.1,
            fill_color="#1A252F",
            fill_opacity=1,
            stroke_width=0
        )
        
        return VGroup(fuselage, left_wing, right_wing, left_engine, right_engine, cockpit, nose)
    
    def create_speed_lines(self):
        """Creates speed lines for jet"""
        lines = VGroup()
        for i in range(5):
            line = Line(
                start=ORIGIN,
                end=LEFT * (0.4 + i * 0.1),
                stroke_color="#BDC3C7",
                stroke_width=3 - i * 0.4,
                stroke_opacity=0.7 - i * 0.12
            ).shift(UP * (0.2 - i * 0.1))
            lines.add(line)
        
        return lines