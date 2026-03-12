from manim import *
import numpy as np


class GoogleAIPlasmaBackground(Scene):
    def construct(self):
        
        # --- PLUGIN FUNCTION START ---
        # You can copy this function into any other Scene's construct method.
        # It encapsulates the entire plasma background logic.
        def add_plasma_background(
            scene: Scene,
            bg_color: str = "#0b1220", # CHANGE: Background color of the scene
            blob_colors: list = [      # CHANGE: Base colors for the 3 plasma blobs
                ["#4285f4", "#ea4335", "#fbbc04", "#34a853"],
                ["#ea4335", "#fbbc04", "#34a853", "#4285f4"],
                ["#fbbc04", "#34a853", "#4285f4", "#ea4335"]
            ],
            max_radius: float = 6.0,   # CHANGE: Controls the maximum radius of the plasma circles
            motion_speed: float = 1.0, # CHANGE: Controls the speed of the motion and color cycling
            run_time: float = 60.0     # CHANGE: Controls how long the animation plays
        ):
            # Set the background color
            scene.camera.background_color = bg_color
            
            # Time tracker for smooth animation
            time_tracker = ValueTracker(0)

            def create_plasma_blob(base_colors, color_phase_offset, motion_scale, motion_phase):
                """Creates a soft glowing plasma blob using concentric circles"""
                num_layers = 70
                blob = VGroup()
                
                for i in range(num_layers):
                    # Calculate radius and opacity for this layer
                    radius_factor = (i + 1) / num_layers
                    # Use the max_radius parameter here
                    radius = max_radius * radius_factor
                    
                    # Exponential opacity falloff for soft glow
                    opacity = (1 - radius_factor) ** 2.5 * 0.4
                    
                    # Create circle
                    circle = Circle(radius=radius)
                    circle.set_stroke(width=0)
                    circle.set_fill(opacity=opacity)
                    
                    # Store layer index for color calculation
                    circle.layer_index = i
                    circle.num_layers = num_layers
                    
                    blob.add(circle)
                
                # Store parameters in the blob
                blob.base_colors = base_colors
                blob.color_phase_offset = color_phase_offset
                blob.motion_scale = motion_scale
                blob.motion_phase = motion_phase
                
                return blob

            def update_plasma_blob(blob, t, motion_scale, motion_phase, color_phase_offset):
                """Updates blob position and colors based on time"""
                # Calculate smooth drifting motion, applying motion_speed parameter
                t_scaled = t * motion_speed
                x_offset = motion_scale * 2.5 * np.sin(0.3 * t_scaled + motion_phase[0])
                y_offset = motion_scale * 2.0 * np.cos(0.25 * t_scaled + motion_phase[1])
                
                # Move entire blob
                blob.move_to([x_offset, y_offset, 0])
                
                # Update colors for each layer
                for circle in blob:
                    # Color cycling through the base colors
                    color_cycle_speed = 0.4 * motion_speed
                    color_time = t_scaled * color_cycle_speed + color_phase_offset
                    
                    # Determine which color pair to blend between
                    num_colors = len(blob.base_colors)
                    color_index = color_time % num_colors
                    color_idx_1 = int(np.floor(color_index)) % num_colors
                    color_idx_2 = (color_idx_1 + 1) % num_colors
                    
                    # Blend factor between the two colors
                    blend = color_index - np.floor(color_index)
                    
                    # Get colors
                    color_1 = ManimColor(blob.base_colors[color_idx_1])
                    color_2 = ManimColor(blob.base_colors[color_idx_2])
                    
                    # Interpolate color
                    interpolated_color = interpolate_color(color_1, color_2, blend)
                    
                    # Add radial variation (outer layers shift color phase slightly)
                    layer_factor = circle.layer_index / circle.num_layers
                    phase_shift = layer_factor * 0.3
                    
                    # Secondary color blend for depth
                    color_idx_3 = (color_idx_2 + 1) % num_colors
                    color_3 = ManimColor(blob.base_colors[color_idx_3])
                    
                    final_color = interpolate_color(
                        interpolated_color,
                        color_3,
                        phase_shift * np.sin(t_scaled * 0.5 + layer_factor * TAU)
                    )
                    
                    circle.set_fill(final_color)

            # Define configurations for each of our blobs
            blob_configs = [
                {"colors": blob_colors[0 % len(blob_colors)], "color_phase": 0.0, "motion_scale": 1.0, "motion_phase": (0, 1.5)},
                {"colors": blob_colors[1 % len(blob_colors)], "color_phase": 2.0, "motion_scale": 0.8, "motion_phase": (3.0, 4.5)},
                {"colors": blob_colors[2 % len(blob_colors)], "color_phase": 4.0, "motion_scale": 1.2, "motion_phase": (1.5, 0.5)},
            ]

            blobs = VGroup()
            
            # Create and configure updaters for multiple plasma blobs
            for config in blob_configs:
                blob = create_plasma_blob(
                    base_colors=config["colors"],
                    color_phase_offset=config["color_phase"],
                    motion_scale=config["motion_scale"],
                    motion_phase=config["motion_phase"]
                )
                
                # Python late binding in lambdas requires us to use default arguments `c=config`
                blob.add_updater(
                    lambda m, c=config: update_plasma_blob(
                        m, time_tracker.get_value(),
                        motion_scale=c["motion_scale"],
                        motion_phase=c["motion_phase"],
                        color_phase_offset=c["color_phase"]
                    )
                )
                blobs.add(blob)

            # Add blobs to scene
            scene.add(blobs)
            
            # Animate the time tracker for continuous motion
            scene.play(
                time_tracker.animate.set_value(TAU * 5),
                rate_func=linear,
                run_time=run_time
            )
        # --- PLUGIN FUNCTION END ---

        # ------------------------------------------------------------- #
        # Usage Example: You can change the optional parameters below   #
        # to customize the look and feel of the plasma background.      #
        # ------------------------------------------------------------- #
        add_plasma_background(
            scene=self, 
            bg_color="#0b1220", 
            blob_colors=[
                ["#4285f4", "#ea4335", "#fbbc04", "#34a853"],
                ["#ea4335", "#fbbc04", "#34a853", "#4285f4"],
                ["#fbbc04", "#34a853", "#4285f4", "#ea4335"]
            ],
            max_radius=6.0, 
            motion_speed=1.0, 
            run_time=60.0
        )

