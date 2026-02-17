from manim import *
import numpy as np

class SmoothTravelingWave(Scene):
    """
    Optimized version with better performance and smoother gradients
    """
    def construct(self):
        self.camera.background_color = BLACK
        time_tracker = ValueTracker(0)
        
        # Create gradient mesh
        gradient = always_redraw(
            lambda: self.create_wave_gradient_mesh(time_tracker.get_value())
        )
        
        self.add(gradient)
        
        # Long smooth animation
        self.play(
            time_tracker.animate.set_value(TAU * 10),
            rate_func=linear,
            run_time=60
        )
    
    def create_wave_gradient_mesh(self, t):
        """
        Creates a mesh-based gradient with traveling wave boundary.
        More efficient than strip-based approach.
        """
        width = config.frame_width
        height = config.frame_height
        
        # Resolution for smooth gradients
        x_res = 100  # Horizontal resolution
        y_res = 80   # Vertical resolution
        
        mesh_group = VGroup()
        
        x_step = width / x_res
        y_step = height / y_res
        
        for i in range(x_res):
            for j in range(y_res):
                # Position
                x = -width/2 + i * x_step
                y = -height/2 + j * y_step
                
                # Calculate wave boundary at this x position
                wave_y = (
                    1.5 * np.sin(0.6 * x - 0.7 * t) +
                    0.9 * np.sin(0.9 * x + 0.5 * t + 1.5) +
                    0.5 * np.sin(1.3 * x - 0.3 * t + 3.0)
                )
                
                # Determine if this cell is above or below the wave
                # Add smooth transition zone
                transition_width = 1.5
                distance_from_wave = y - wave_y
                
                # Smooth transition factor (0 = below, 1 = above)
                if distance_from_wave < -transition_width:
                    blend = 0
                elif distance_from_wave > transition_width:
                    blend = 1
                else:
                    # Smooth interpolation in transition zone
                    blend = (distance_from_wave + transition_width) / (2 * transition_width)
                
                # Vertical gradient within each region
                y_norm = (y + height/2) / height
                
                # Bottom region color (cyan gradient)
                cyan_color = interpolate_color(
                    ManimColor("#00e5ff"),  # Bright cyan
                    ManimColor("#18ffff"),  # Light cyan
                    y_norm
                )
                
                # Top region color (blue gradient)
                blue_color = interpolate_color(
                    ManimColor("#2979ff"),  # Bright blue
                    ManimColor("#0d47a1"),  # Dark navy
                    y_norm
                )
                
                # Blend between regions based on wave position
                final_color = interpolate_color(cyan_color, blue_color, blend)
                
                # Create cell
                cell = Rectangle(
                    width=x_step * 1.01,
                    height=y_step * 1.01,
                    fill_color=final_color,
                    fill_opacity=1,
                    stroke_width=0
                ).move_to([x + x_step/2, y + y_step/2, 0])
                
                mesh_group.add(cell)
        
        return mesh_group


