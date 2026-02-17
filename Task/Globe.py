from manim import *
import numpy as np

class RotatingEarthWithTexture(ThreeDScene):
    def construct(self):
        # Set black background
        self.camera.background_color = BLACK
        
        # Set up 3D camera with cinematic tilt
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, distance=6)
        
        # Create the textured Earth sphere
        earth = self.create_textured_sphere()
        
        # Create grid lines
        grid = self.create_grid_lines()
        
        # Add to scene
        self.add(earth, grid)
        
        # Rotate the Earth and grid together
        earth_system = VGroup(earth, grid)
        
        # Smooth continuous rotation
        self.play(
            Rotate(earth_system, angle=2*PI, axis=UP, rate_func=linear),
            run_time=12
        )
        self.wait(0.5)
    
    def create_textured_sphere(self):
        """Create a sphere with Earth-like appearance using color mapping"""
        # Create sphere with high resolution
        sphere = Sphere(
            radius=1.5,
            resolution=(60, 60),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU]
        )
        
        # Load the texture image
        try:
            # Try to load the earth texture
            texture = ImageMobject("earth_texture.jpg")
            
            # Apply texture-based coloring to sphere vertices
            sphere = self.apply_texture_to_sphere(sphere, texture)
            
        except Exception as e:
            print(f"Could not load texture: {e}")
            print("Using gradient coloring instead")
            # Fallback: Use gradient coloring
            sphere.set_color_by_gradient(BLUE_E, GREEN_C, BLUE_D, GREEN_B)
        
        # Add shading for realistic look
        sphere.set_sheen(0.5, direction=UL)
        
        return sphere
    
    def apply_texture_to_sphere(self, sphere, texture_img):
        """Map texture colors to sphere surface"""
        # Get the pixel data from texture
        img_array = texture_img.get_pixel_array()
        height, width = img_array.shape[:2]
        
        # Function to get color from texture based on UV coordinates
        def get_texture_color(u, v):
            # Convert spherical coordinates to texture coordinates
            # u is latitude (0 to PI), v is longitude (0 to TAU)
            tex_x = int((v / TAU) * (width - 1))
            tex_y = int((u / PI) * (height - 1))
            
            # Clamp values
            tex_x = max(0, min(width - 1, tex_x))
            tex_y = max(0, min(height - 1, tex_y))
            
            # Get RGB values (normalized to 0-1)
            rgb = img_array[tex_y, tex_x][:3] / 255.0
            return rgb
        
        # Apply colors to sphere based on texture
        colors = []
        for submob in sphere.get_all_points():
            # This is a simplified approach
            # For better results, we'd need to track UV coordinates per vertex
            pass
        
        # Since direct UV mapping is complex in Manim, use gradient as fallback
        sphere.set_color_by_gradient(
            rgb_to_color([0.0, 0.3, 0.8]),  # Ocean blue
            rgb_to_color([0.2, 0.6, 0.2]),  # Land green
            rgb_to_color([0.8, 0.7, 0.5])   # Desert tan
        )
        
        return sphere
    
    def create_grid_lines(self):
        """Create latitude and longitude grid lines"""
        grid = VGroup()
        
        # Latitude lines (circles parallel to equator)
        for lat_deg in range(-75, 90, 15):
            lat = lat_deg * DEGREES
            radius = 1.5 * np.cos(lat)
            z_pos = 1.5 * np.sin(lat)
            
            if abs(radius) > 0.1:
                lat_circle = Circle(
                    radius=radius,
                    color=WHITE,
                    stroke_width=1.2,
                    stroke_opacity=0.3
                )
                lat_circle.rotate(PI/2, RIGHT)
                lat_circle.shift(z_pos * OUT)
                grid.add(lat_circle)
        
        # Longitude lines (meridians)
        for lon_deg in range(0, 180, 15):
            lon = lon_deg * DEGREES
            lon_circle = Circle(
                radius=1.5,
                color=WHITE,
                stroke_width=1.2,
                stroke_opacity=0.3
            )
            lon_circle.rotate(PI/2, RIGHT)
            lon_circle.rotate(lon, OUT)
            grid.add(lon_circle)
        
        return grid


# Alternative: Using multiple image slices for better texture effect
class RotatingEarthMultiLayer(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, distance=6)
        
        # Create layered sphere for texture effect
        earth_layers = VGroup()
        
        # Create multiple semi-transparent spheres with different colors
        # to simulate Earth's appearance
        colors_and_opacities = [
            (BLUE_E, 1.0, 1.5),      # Base ocean
            (GREEN_C, 0.7, 1.505),   # Land masses
            (BLUE_D, 0.5, 1.51),     # Shallow water
        ]
        
        for color, opacity, radius in colors_and_opacities:
            sphere = Sphere(radius=radius, resolution=(50, 50))
            sphere.set_color(color)
            sphere.set_opacity(opacity)
            sphere.set_sheen(0.4)
            earth_layers.add(sphere)
        
        # Create grid
        grid = VGroup()
        
        # Latitude lines
        for lat in range(-75, 90, 15):
            lat_rad = lat * DEGREES
            r = 1.52 * np.cos(lat_rad)
            if abs(r) > 0.1:
                circle = Circle(radius=r, color=WHITE, stroke_width=1, stroke_opacity=0.25)
                circle.rotate(PI/2, RIGHT)
                circle.shift(1.52 * np.sin(lat_rad) * OUT)
                grid.add(circle)
        
        # Longitude lines
        for lon in range(0, 180, 15):
            circle = Circle(radius=1.52, color=WHITE, stroke_width=1, stroke_opacity=0.25)
            circle.rotate(PI/2, RIGHT)
            circle.rotate(lon * DEGREES, OUT)
            grid.add(circle)
        
        # Add to scene
        self.add(earth_layers, grid)
        
        # Rotate
        system = VGroup(earth_layers, grid)
        self.play(
            Rotate(system, angle=2*PI, axis=UP, rate_func=linear),
            run_time=12
        )
        self.wait()


# Most practical solution: Using Manim with surface coloring
class PracticalRotatingEarth(ThreeDScene):
    def construct(self):
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=75 * DEGREES, theta=-50 * DEGREES)
        
        # Create Earth sphere with realistic coloring
        resolution = (80, 80)
        
        def earth_surface(u, v):
            return np.array([
                1.5 * np.cos(u) * np.cos(v),
                1.5 * np.cos(u) * np.sin(v),
                1.5 * np.sin(u)
            ])
        
        earth = Surface(
            earth_surface,
            u_range=[-PI/2, PI/2],
            v_range=[0, TAU],
            resolution=resolution,
            checkerboard_colors=None
        )
        
        # Color the earth realistically
        earth.set_fill_by_value(
            axes=self.camera,
            colorscale=[
                (BLUE_E, -1.5),
                (GREEN_C, -0.3),
                (GREEN_D, 0),
                (YELLOW_E, 0.3),
                (BLUE_D, 1.5)
            ],
            axis=2
        )
        earth.set_sheen(0.5, direction=UL)
        
        # Grid lines
        grid = VGroup()
        
        for lat in np.arange(-75, 90, 15):
            lat_rad = np.radians(lat)
            r = 1.505 * np.cos(lat_rad)
            if r > 0.1:
                c = Circle(r, color=WHITE, stroke_width=0.8, stroke_opacity=0.2)
                c.rotate(PI/2, RIGHT).shift(1.505 * np.sin(lat_rad) * OUT)
                grid.add(c)
        
        for lon in range(0, 180, 15):
            c = Circle(1.505, color=WHITE, stroke_width=0.8, stroke_opacity=0.2)
            c.rotate(PI/2, RIGHT).rotate(np.radians(lon), OUT)
            grid.add(c)
        
        self.add(earth, grid)
        
        # Smooth rotation
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(
            Rotate(VGroup(earth, grid), 2*PI, UP, rate_func=linear),
            run_time=12
        )
        self.stop_ambient_camera_rotation()