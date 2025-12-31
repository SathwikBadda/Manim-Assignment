from manim import *
import numpy as np

class BouncingBallAnimation(Scene):
    def construct(self):
        # Set dark background
        self.camera.background_color = "#0E1117"
        
        # ========================================
        # CONSTANTS & PHYSICS PARAMETERS
        # ========================================
        
        # Motion parameters
        total_duration = 8  # Total animation time
        horizontal_distance = 16  # Total horizontal travel
        
        # Bounce physics
        initial_height = 3.0  # Starting bounce height
        damping_factor = 0.75  # Energy loss per bounce (0-1)
        gravity = 9.8  # Gravity acceleration
        bounce_frequency = 2.0  # Bounces per second approximately
        
        # Visual parameters
        ball_radius = 0.3
        ground_y = -2.5
        
        # ========================================
        # GROUND SETUP
        # ========================================
        
        ground = Line(
            start=LEFT * 10,
            end=RIGHT * 10,
            color="#4A4A4A",
            stroke_width=8
        )
        ground.shift(DOWN * 2.5)
        
        # ========================================
        # BALL CREATION
        # ========================================
        
        # Main ball
        ball = Circle(
            radius=ball_radius,
            fill_color="#FF6B35",
            fill_opacity=1,
            stroke_color="#FF8C42",
            stroke_width=3
        )
        
        # Glow effect
        glow = Circle(
            radius=ball_radius * 1.3,
            fill_color="#FF6B35",
            fill_opacity=0,
            stroke_color="#FF6B35",
            stroke_width=8,
            stroke_opacity=0.4
        )
        
        # Shadow
        shadow = Ellipse(
            width=ball_radius * 2.5,
            height=ball_radius * 0.4,
            fill_color="#000000",
            fill_opacity=0.4,
            stroke_width=0
        )
        shadow.move_to([0, ground_y + 0.05, 0])
        
        # Motion trail
        trail = VGroup()
        trail_length = 15
        
        # Group ball components
        ball_group = VGroup(ball, glow)
        ball_group.move_to([-8, ground_y + ball_radius, 0])
        
        # ========================================
        # PHYSICS FUNCTIONS
        # ========================================
        
        def calculate_bounce_height(t, duration, initial_h, damping):
            """
            Calculate vertical position with damping bounce effect
            Uses exponential decay for realistic energy loss
            """
            # Number of complete bounces so far
            bounce_period = duration / (initial_h / 2)  # Approximate period
            current_bounce = int(t * bounce_frequency)
            
            # Time within current bounce cycle
            cycle_time = (t * bounce_frequency) % 1.0
            
            # Height decreases exponentially with each bounce
            max_height = initial_h * (damping ** current_bounce)
            
            # Parabolic trajectory within each bounce
            # Using physics: h = h_max - (1/2) * g * t^2
            if max_height > 0.1:  # Stop bouncing when too low
                height = max_height * (1 - (2 * cycle_time - 1) ** 2)
            else:
                height = 0
            
            return height
        
        def calculate_squash_stretch(velocity_y, impact_distance):
            """
            Calculate squash and stretch based on vertical motion
            Returns (width_scale, height_scale)
            """
            # Maximum squash/stretch factor
            max_deformation = 0.3
            
            # Squash on impact (when close to ground with downward velocity)
            if impact_distance < ball_radius * 0.5 and velocity_y < 0:
                squash = 1 - max_deformation
                stretch = 1 + max_deformation * 0.7
                return stretch, squash
            
            # Stretch during upward motion
            elif velocity_y > 2:
                stretch = 1 + max_deformation * 0.5
                squash = 1 - max_deformation * 0.3
                return squash, stretch
            
            # Normal shape
            else:
                return 1, 1
        
        # ========================================
        # ANIMATION SETUP
        # ========================================
        
        # Time tracker for physics calculations
        time_tracker = ValueTracker(0)
        
        # Store previous positions for trail
        previous_positions = []
        
        def update_ball(mob):
            """Main updater function for ball position and deformation"""
            t = time_tracker.get_value()
            progress = t / total_duration
            
            # Horizontal motion (linear with ease)
            x_pos = -8 + horizontal_distance * progress
            
            # Vertical motion (bouncing with damping)
            y_offset = calculate_bounce_height(t, total_duration, initial_height, damping_factor)
            y_pos = ground_y + ball_radius + y_offset
            
            # Calculate velocity for squash/stretch (numerical derivative)
            dt = 0.01
            y_next = calculate_bounce_height(t + dt, total_duration, initial_height, damping_factor)
            velocity_y = (y_next - y_offset) / dt
            
            # Distance from ground
            impact_distance = y_pos - ground_y
            
            # Apply squash and stretch
            width_scale, height_scale = calculate_squash_stretch(velocity_y, impact_distance)
            
            # Update ball position
            mob[0].move_to([x_pos, y_pos, 0])
            mob[0].stretch_to_fit_width(ball_radius * 2 * width_scale)
            mob[0].stretch_to_fit_height(ball_radius * 2 * height_scale)
            
            # Update glow
            mob[1].move_to([x_pos, y_pos, 0])
            mob[1].stretch_to_fit_width(ball_radius * 2.6 * width_scale)
            mob[1].stretch_to_fit_height(ball_radius * 2.6 * height_scale)
        
        def update_shadow(mob):
            """Update shadow position and size based on ball height"""
            t = time_tracker.get_value()
            progress = t / total_duration
            
            # Follow ball horizontally
            x_pos = -8 + horizontal_distance * progress
            
            # Calculate ball height for shadow scaling
            y_offset = calculate_bounce_height(t, total_duration, initial_height, damping_factor)
            
            # Shadow scales inversely with height (smaller when higher)
            height_factor = max(0.3, 1 - (y_offset / initial_height) * 0.6)
            shadow_width = ball_radius * 2.5 * height_factor
            
            # Shadow opacity decreases with height
            shadow_opacity = 0.4 * height_factor
            
            mob.move_to([x_pos, ground_y + 0.05, 0])
            mob.stretch_to_fit_width(shadow_width)
            mob.set_fill(opacity=shadow_opacity)
        
        def update_trail(mob):
            """Create motion trail effect"""
            t = time_tracker.get_value()
            progress = t / total_duration
            
            x_pos = -8 + horizontal_distance * progress
            y_offset = calculate_bounce_height(t, total_duration, initial_height, damping_factor)
            y_pos = ground_y + ball_radius + y_offset
            
            # Add new trail dot
            if len(previous_positions) == 0 or np.linalg.norm(
                np.array([x_pos, y_pos]) - np.array(previous_positions[-1])
            ) > 0.2:
                trail_dot = Dot(
                    point=[x_pos, y_pos, 0],
                    radius=0.05,
                    color="#FF6B35",
                    fill_opacity=0.6
                )
                mob.add(trail_dot)
                previous_positions.append([x_pos, y_pos])
                
                # Limit trail length
                if len(mob) > trail_length:
                    mob.remove(mob[0])
                    previous_positions.pop(0)
                
                # Fade trail dots
                for i, dot in enumerate(mob):
                    opacity = 0.6 * (i / len(mob))
                    dot.set_fill(opacity=opacity)
        
        # Add updaters
        ball_group.add_updater(update_ball)
        shadow.add_updater(update_shadow)
        trail.add_updater(update_trail)
        
        # ========================================
        # ANIMATION SEQUENCE
        # ========================================
        
        # Fade in ground
        self.play(Create(ground), run_time=1)
        
        # Add all elements to scene
        self.add(shadow, trail, ball_group)
        
        # Run the animation
        self.play(
            time_tracker.animate.set_value(total_duration),
            rate_func=linear,
            run_time=total_duration
        )
        
        # Clean exit
        self.play(
            FadeOut(ball_group),
            FadeOut(shadow),
            FadeOut(trail),
            FadeOut(ground),
            run_time=0.8
        )
        
        self.wait(0.5)