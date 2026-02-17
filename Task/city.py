from manim import *
import numpy as np

class EnterpriseBigDataStream(Scene):
    def construct(self):
        # ========================================
        # CONFIGURATION
        # ========================================
        
        # Deep blue night background
        self.camera.background_color = "#1a2f5c"
        
        # ========================================
        # 1. BACKGROUND CLOUDS
        # ========================================
        
        def create_cloud(position, scale=1.0, opacity=0.08):
            """Create a stylized flat cloud using overlapping circles"""
            cloud = VGroup()
            # Create blob-like cloud shape with circles
            circles_config = [
                (0, 0, 0.5),
                (-0.3, -0.1, 0.4),
                (0.3, -0.1, 0.4),
                (-0.15, 0.15, 0.35),
                (0.15, 0.15, 0.35),
            ]
            for x, y, r in circles_config:
                c = Circle(radius=r * scale, fill_opacity=opacity, 
                          fill_color=WHITE, stroke_width=0)
                c.shift(RIGHT * x * scale + UP * y * scale)
                cloud.add(c)
            cloud.move_to(position)
            return cloud
        
        # Add multiple clouds at different positions
        clouds = VGroup()
        cloud_positions = [
            (LEFT * 5 + UP * 2, 1.2, 0.06),
            (RIGHT * 4 + UP * 1.5, 1.5, 0.08),
            (LEFT * 3 + DOWN * 0.5, 1.0, 0.05),
            (RIGHT * 5.5 + UP * 0.8, 1.3, 0.07),
        ]
        
        for pos, scale, opacity in cloud_positions:
            clouds.add(create_cloud(pos, scale, opacity))
        
        self.add(clouds)
        
        # ========================================
        # 2. GROUND LINE
        # ========================================
        
        ground_line = Line(
            start=LEFT * 7 + DOWN * 2.8,
            end=RIGHT * 7 + DOWN * 2.8,
            stroke_color=WHITE,
            stroke_width=2,
            stroke_opacity=0.6
        )
        self.add(ground_line)
        
        # ========================================
        # 3. OFFICE BUILDINGS (LAYERED CITY)
        # ========================================
        
        def create_building(width, height, position, color, windows_config):
            """Create a detailed office building with windows and depth"""
            building = VGroup()
            
            # Main building body
            main_rect = Rectangle(
                width=width,
                height=height,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=1.5,
                stroke_opacity=0.7
            )
            building.add(main_rect)
            
            # Add window strips
            num_rows = windows_config['rows']
            num_cols = windows_config['cols']
            window_width = windows_config['width']
            window_height = windows_config['height']
            window_color = windows_config['color']
            
            windows = VGroup()
            for row in range(num_rows):
                for col in range(num_cols):
                    window = Rectangle(
                        width=window_width,
                        height=window_height,
                        fill_color=window_color,
                        fill_opacity=0.8,
                        stroke_width=0
                    )
                    x_offset = (col - num_cols/2 + 0.5) * (window_width * 1.5)
                    y_offset = (row - num_rows/2 + 0.5) * (window_height * 2)
                    window.shift(RIGHT * x_offset + UP * y_offset)
                    windows.add(window)
            
            building.add(windows)
            building.move_to(position + DOWN * (height/2 - 2.8))
            
            return building
        
        # Left back building (outline style)
        left_back = create_building(
            width=1.2,
            height=2.5,
            position=LEFT * 3.5,
            color="#2d4a7c",
            windows_config={
                'rows': 5,
                'cols': 2,
                'width': 0.15,
                'height': 0.12,
                'color': "#4a7ba7"
            }
        )
        
        # Left front building (dark with colored windows)
        left_front = create_building(
            width=1.0,
            height=2.0,
            position=LEFT * 2.3,
            color="#1a2a4a",
            windows_config={
                'rows': 4,
                'cols': 2,
                'width': 0.12,
                'height': 0.15,
                'color': TEAL
            }
        )
        
        # Right back building (tall blue)
        right_back = create_building(
            width=1.5,
            height=2.3,
            position=RIGHT * 2.8,
            color="#3d5a8c",
            windows_config={
                'rows': 5,
                'cols': 2,
                'width': 0.18,
                'height': 0.12,
                'color': "#4a7ba7"
            }
        )
        
        # Right front building (outline style, shorter)
        right_front = create_building(
            width=1.8,
            height=1.8,
            position=RIGHT * 4.8,
            color="#2d4a7c",
            windows_config={
                'rows': 3,
                'cols': 2,
                'width': 0.15,
                'height': 0.15,
                'color': "#4a7ba7"
            }
        )
        
        # ========================================
        # 4. CENTRAL DATA BUILDING
        # ========================================
        
        central_building = VGroup()
        
        # Main tower body
        tower_width = 1.3
        tower_height = 4.2
        
        # Main rectangle with gradient effect (using multiple layers)
        tower_bg = Rectangle(
            width=tower_width,
            height=tower_height,
            fill_color="#c5d3e8",
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=2,
            stroke_opacity=0.9
        )
        central_building.add(tower_bg)
        
        # Top cap
        top_cap = Rectangle(
            width=tower_width + 0.2,
            height=0.25,
            fill_color=WHITE,
            fill_opacity=0.9,
            stroke_width=0
        )
        top_cap.next_to(tower_bg, UP, buff=0)
        central_building.add(top_cap)
        
        # Add vertical window grid (binary data pattern)
        window_rows = 10
        window_cols = 3
        
        for row in range(window_rows):
            for col in range(window_cols):
                # Alternate between "1" and "0" text
                if (row + col) % 2 == 0:
                    text_content = "1"
                else:
                    text_content = "0"
                
                data_text = Text(
                    text_content,
                    font_size=18,
                    color=WHITE,
                    weight=BOLD
                ).set_opacity(0.5)
                
                x_pos = (col - 1) * 0.35
                y_pos = (row - window_rows/2 + 0.5) * 0.38
                data_text.move_to(RIGHT * x_pos + UP * y_pos)
                central_building.add(data_text)
        
        # Position central building
        central_building.move_to(UP * (tower_height/2 - 2.8))
        
        # Add all buildings
        self.add(left_back, left_front, right_back, right_front, central_building)
        
        # ========================================
        # 5. DATA PARTICLE STREAMS
        # ========================================
        
        # Get the top of the central building
        stream_origin = central_building.get_top()
        
        # Define 6-7 stream paths (fan-like structure)
        num_streams = 7
        stream_angles = np.linspace(-75, 75, num_streams)
        
        all_particles = VGroup()
        
        for stream_idx, angle in enumerate(stream_angles):
            # Create curved bezier path for this stream
            angle_rad = angle * DEGREES
            
            # Control points for bezier curve
            start = stream_origin
            control1 = start + UP * 1.2 + RIGHT * np.sin(angle_rad) * 0.5
            control2 = start + UP * 2.5 + RIGHT * np.sin(angle_rad) * 1.5
            end = start + UP * 3.5 + RIGHT * np.sin(angle_rad) * 2.5
            
            # Create particle types
            particle_shapes = [Circle, Square, RegularPolygon]
            particle_colors = [WHITE, TEAL, "#7dd3c0"]
            
            # Generate multiple particles along this path
            num_particles = 8
            
            for p_idx in range(num_particles):
                # Choose random shape and color
                shape_class = np.random.choice(particle_shapes)
                color = np.random.choice(particle_colors)
                
                if shape_class == RegularPolygon:
                    particle = RegularPolygon(n=6, radius=0.12, fill_color=color, fill_opacity=0.8, stroke_width=0)
                elif shape_class == Square:
                    particle = Square(side_length=0.24, fill_color=color, fill_opacity=0.8, stroke_width=0)
                else:
                    particle = shape_class(radius=0.12, fill_color=color, fill_opacity=0.8, stroke_width=0)
                
                # Initial position at origin
                particle.move_to(start)
                particle.set_opacity(0)
                
                # Create animation along bezier curve
                def create_updater(particle, t_offset, ctrl1, ctrl2, end_point, start_point):
                    def updater(mob, dt):
                        # Calculate current time position
                        if not hasattr(mob, 'time_elapsed'):
                            mob.time_elapsed = t_offset
                        
                        mob.time_elapsed += dt * 0.25  # Speed factor
                        
                        t = mob.time_elapsed % 1.0
                        
                        # Bezier curve calculation
                        pos = (1-t)**3 * start_point + \
                              3*(1-t)**2*t * ctrl1 + \
                              3*(1-t)*t**2 * ctrl2 + \
                              t**3 * end_point
                        
                        mob.move_to(pos)
                        
                        # Fade in and fade out
                        if t < 0.2:
                            mob.set_opacity(t * 4)
                        elif t > 0.8:
                            mob.set_opacity((1 - t) * 5)
                        else:
                            mob.set_opacity(0.8)
                    
                    return updater
                
                # Add updater with time offset
                time_offset = p_idx * 0.15
                particle.add_updater(
                    create_updater(particle, time_offset, control1, 
                                 control2, end, start)
                )
                
                all_particles.add(particle)
        
        # Add all particles
        self.add(all_particles)
        
        # ========================================
        # 6. ANIMATE
        # ========================================
        
        # Let the streams flow for 7 seconds
        self.wait(7)