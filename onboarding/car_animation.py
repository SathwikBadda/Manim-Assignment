from manim import *

class CarDrivingAnimation(Scene):
    def construct(self):
        # Set dark background
        self.camera.background_color = "#0E1117"
        
        # ========================================
        # ROAD SETUP
        # ========================================
        road = Line(
            start=LEFT * 8,
            end=RIGHT * 8,
            color="#4A4A4A",
            stroke_width=12
        )
        road.shift(DOWN * 2.5)
        
        # Dashed lane markings
        num_dashes = 20
        dash_length = 0.4
        gap_length = 0.3
        dashes = VGroup()
        
        total_length = 16
        dash_positions = np.linspace(-8, 8, num_dashes)
        
        for x_pos in dash_positions:
            dash = Line(
                start=LEFT * dash_length / 2,
                end=RIGHT * dash_length / 2,
                color="#FFFF00",
                stroke_width=3
            )
            dash.move_to([x_pos, road.get_y(), 0])
            dashes.add(dash)
        
        # ========================================
        # CAR CONSTRUCTION
        # ========================================
        
        # Car body (main rectangle)
        car_body = Rectangle(
            width=2.0,
            height=0.7,
            fill_color="#E74C3C",
            fill_opacity=1,
            stroke_color="#C0392B",
            stroke_width=3
        )
        
        # Car roof (trapezoid/smaller rectangle)
        car_roof = Polygon(
            [-0.6, 0.35, 0],
            [0.4, 0.35, 0],
            [0.2, 0.85, 0],
            [-0.4, 0.85, 0],
            fill_color="#C0392B",
            fill_opacity=1,
            stroke_color="#A93226",
            stroke_width=3
        )
        
        # Windows
        window = Rectangle(
            width=0.35,
            height=0.3,
            fill_color="#5DADE2",
            fill_opacity=0.7,
            stroke_color="#3498DB",
            stroke_width=2
        )
        window.move_to(car_roof.get_center() + LEFT * 0.25 + DOWN * 0.1)
        
        # Wheels
        wheel_radius = 0.25
        left_wheel = Circle(
            radius=wheel_radius,
            fill_color="#2C3E50",
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=3
        )
        right_wheel = Circle(
            radius=wheel_radius,
            fill_color="#2C3E50",
            fill_opacity=1,
            stroke_color="#1A252F",
            stroke_width=3
        )
        
        # Wheel spokes for rotation visibility
        left_spoke1 = Line(ORIGIN, RIGHT * wheel_radius * 0.7, color="#ECF0F1", stroke_width=2)
        left_spoke2 = Line(ORIGIN, UP * wheel_radius * 0.7, color="#ECF0F1", stroke_width=2)
        right_spoke1 = Line(ORIGIN, RIGHT * wheel_radius * 0.7, color="#ECF0F1", stroke_width=2)
        right_spoke2 = Line(ORIGIN, UP * wheel_radius * 0.7, color="#ECF0F1", stroke_width=2)
        
        left_wheel_group = VGroup(left_wheel, left_spoke1, left_spoke2)
        right_wheel_group = VGroup(right_wheel, right_spoke1, right_spoke2)
        
        # Position wheels
        left_wheel_group.move_to(car_body.get_corner(DL) + RIGHT * 0.5 + DOWN * 0.1)
        right_wheel_group.move_to(car_body.get_corner(DR) + LEFT * 0.5 + DOWN * 0.1)
        
        # Shadow
        shadow = Ellipse(
            width=2.2,
            height=0.3,
            fill_color="#000000",
            fill_opacity=0.3,
            stroke_width=0
        )
        shadow.next_to(car_body, DOWN, buff=0.15)
        
        # Group all car components
        car = VGroup(
            shadow,
            car_body,
            car_roof,
            window,
            left_wheel_group,
            right_wheel_group
        )
        
        # Add glow effect
        glow = car_body.copy()
        glow.set_stroke(color="#E74C3C", width=8, opacity=0.4)
        glow.set_fill(opacity=0)
        car.add(glow)
        
        # Position car off-screen left
        car.shift(LEFT * 10 + DOWN * 2.5)
        
        # ========================================
        # ANIMATION SEQUENCE
        # ========================================
        
        # Fade in road and dashes
        self.play(
            Create(road),
            LaggedStart(*[FadeIn(dash) for dash in dashes], lag_ratio=0.05),
            run_time=1.5
        )
        
        # Wheel rotation tracker
        rotation_tracker = ValueTracker(0)
        
        # Updater for wheel rotation
        def rotate_wheels(mob, dt):
            angle = rotation_tracker.get_value()
            left_wheel_group[1].rotate(angle, about_point=left_wheel_group.get_center())
            left_wheel_group[2].rotate(angle, about_point=left_wheel_group.get_center())
            right_wheel_group[1].rotate(angle, about_point=right_wheel_group.get_center())
            right_wheel_group[2].rotate(angle, about_point=right_wheel_group.get_center())
        
        # Updater for dash movement (parallax effect)
        def move_dashes(mob):
            for dash in mob:
                if dash.get_x() < -8.5:
                    dash.shift(RIGHT * 16)
        
        dashes.add_updater(move_dashes)
        
        # Car driving animation with smooth ease
        drive_distance = 20
        drive_time = 6
        
        # Calculate rotation for wheels based on distance
        wheel_circumference = 2 * PI * wheel_radius
        total_rotations = drive_distance / wheel_circumference
        total_rotation_angle = total_rotations * TAU
        
        self.play(
            car.animate.shift(RIGHT * drive_distance).set_rate_func(smooth),
            rotation_tracker.animate.set_value(total_rotation_angle).set_rate_func(linear),
            run_time=drive_time
        )
        
        # Clean exit
        self.play(
            FadeOut(road),
            FadeOut(dashes),
            run_time=0.5
        )
        
        self.wait(0.5)