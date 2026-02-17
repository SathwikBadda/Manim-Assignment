"""
Greenery.py

This script creates an educational animation about Ethanol production using Manim.
It visualizes the 5-step process:
1. Harvest (Crops)
2. Grinding
3. Cooking (Fermentation)
4. Distillation
5. Final Fuel (Green Mix)

The animation style is "Greenery" - emphasizing nature, eco-friendliness, and clean energy.
"""
from manim import *
import numpy as np
import textwrap

# ================================
# COLOR CONSTANTS
# ================================
BACKGROUND_COLOR = "#E8F5E9"
LIGHT_GREEN = "#A5D6A7"
DARK_GREEN = "#2E7D32"
MEDIUM_GREEN = "#66BB6A"
YELLOW = "#FDD835"
ORANGE = "#FB8C00"
BROWN = "#6D4C41"
GRAY = "#757575"
LIGHT_GRAY = "#BDBDBD"
BLUE = "#42A5F5"
CREAM = "#FFF9C4"

# ================================
# HELPER FUNCTIONS
# ================================




def create_leaf(scale=1.0):
    """Create a simple leaf shape using Bezier curve"""
    points = [
        ORIGIN,
        UP * 0.3 * scale + RIGHT * 0.1 * scale,
        UP * 0.5 * scale + RIGHT * 0.2 * scale,
        UP * 0.6 * scale,
        UP * 0.5 * scale + LEFT * 0.2 * scale,
        UP * 0.3 * scale + LEFT * 0.1 * scale,
        ORIGIN
    ]
    leaf = VMobject()
    leaf.set_points_as_corners(points)
    leaf.make_smooth()
    leaf.set_fill(MEDIUM_GREEN, opacity=1)
    leaf.set_stroke(DARK_GREEN, width=2)
    return leaf




# ================================
# MAIN ANIMATION SCENE
# ================================


class EthanolAnimation(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BACKGROUND_COLOR
        
        # ---------------------------------------------------------------------
        # LAYOUT CONFIGURATION
        # ---------------------------------------------------------------------
        # Define start and end points for the conveyor belt
        self.BELT_START = LEFT * 6 + DOWN * 0.5
        self.BELT_END = RIGHT * 6 + UP * 2.5
        # Y-coordinate for explanatory text
        self.TEXT_Y = DOWN * 2.5
        
        # Calculate anchors
        self.belt_vec = self.BELT_END - self.BELT_START
        self.anchors = [self.BELT_START + self.belt_vec * (i/4) for i in range(5)]
        
        # Background decorative leaves
        self.add_background_leaves()
        
        # Title Section
        self.show_title()
        
        # ---------------------------------------------------------------------
        # ANIMATION SEQUENCE
        # ---------------------------------------------------------------------
        
        # 1. Create the main conveyor belt structure
        self.create_belt_system()
        
        # Production stages
        self.wait(0.5)
        self.stage_1_crops()
        self.wait(1)
        self.stage_2_grinding()
        self.wait(1)
        self.stage_3_cooking()
        self.wait(1)
        self.stage_4_distillation()
        self.wait(1)
        self.stage_5_fuel()
        self.wait(2)

        # Cleanup Animation (Reverse Order)
        self.play(FadeOut(self.stage5_group), run_time=1.0)
        self.play(FadeOut(self.stage4_group), run_time=1.0)
        self.play(FadeOut(self.stage3_group), run_time=1.0)
        self.play(FadeOut(self.stage2_group), run_time=1.0)
        self.play(FadeOut(self.stage1_group), run_time=1.0)
        
        # Vanish belt at last
        # Vanish belt at last
        self.play(Uncreate(self.belt), FadeOut(self.moving), run_time=2.0)
        
        self.wait(1)
    
    def add_background_leaves(self):
        """Add decorative background leaves"""
        bg_leaves = VGroup()
        
        # Create several faint leaves in background
        positions = [
            UP * 3 + LEFT * 5,
            UP * 2.5 + RIGHT * 5,
            DOWN * 2 + LEFT * 6,
            UP * 1 + LEFT * 3,
            DOWN * 1.5 + RIGHT * 4
        ]
        
        for pos in positions:
            leaf = create_leaf(scale=1.5)
            leaf.set_fill(LIGHT_GREEN, opacity=0.2)
            leaf.set_stroke(width=0)
            leaf.move_to(pos)
            leaf.rotate(np.random.random() * TAU)
            bg_leaves.add(leaf)
        
        self.add(bg_leaves)
    
    def show_title(self):
        """Animate the title"""
        # Main title
        title_ethanol = Text("Ethanol:", font_size=48, color=DARK_GREEN, weight=BOLD)
        title_power = Text("The Power of Plants!", font_size=36, color=YELLOW, weight=BOLD)
        title_power.set_stroke(DARK_GREEN, width=1.5, background=True)
        
        title = VGroup(title_ethanol, title_power).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        title.to_edge(UP, buff=0.2).to_edge(LEFT, buff=0.5)
        
        # Drop shadow
        shadow = title.copy()
        shadow.set_color(DARK_GREEN)
        shadow.set_opacity(0.3)
        shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
        
        # Leaf decorations
        leaf1 = create_leaf(scale=0.5)
        leaf1.next_to(title, RIGHT, buff=0.2).shift(UP * 0.3)
        
        leaf2 = create_leaf(scale=0.4)
        leaf2.next_to(title, RIGHT, buff=0.5).shift(DOWN * 0.2)
        leaf2.rotate(PI/3)
        
        # Animate
        self.play(FadeIn(shadow))
        self.play(Write(title), run_time=2)
        self.play(
            GrowFromCenter(leaf1),
            GrowFromCenter(leaf2),
            run_time=0.8
        )
        
        self.title_group = VGroup(shadow, title, leaf1, leaf2)
        self.title_group = VGroup(shadow, title, leaf1, leaf2)
    
    def get_sigmoid_point(self, x):
        """Calculate point on the sigmoid belt curve"""
        # S-curve parameters
        # Start (left, low) -> End (right, high)
        x_min, x_max = -6, 6
        y_min, y_max = -2.5, 2.5
        
        # Logistic function
        k = 0.5 # Steepness
        x_0 = 0 # Midpoint
        
        sigmoid = 1 / (1 + np.exp(-k * (x - x_0)))
        y = y_min + (y_max - y_min) * sigmoid
        
        return np.array([x, y, 0])

    def create_belt_system(self):
        """
        Create and animate the Conveyor Belt System.
        
        This function:
        1. Calculates points along a sigmoid curve.
        2. Computes normal vectors to create a thick "ribbon" (the top surface).
        3. Extrudes the ribbon downwards to create a 3D-like side surface.
        4. Adds moving "rivets" or track lines that follow the curve using a ValueTracker loop.
        """
        # Generate x-values for the curve
        x_values = np.linspace(-7, 7, 100) 
        # Calculate points and tangents for geometry
        points = []
        normals = []
        
        for x in x_values:
            p = self.get_sigmoid_point(x)
            points.append(p)
            
            # Normal calculation for thickness
            p_next = self.get_sigmoid_point(x + 0.01)
            tangent = p_next - p
            # Normalize tangent
            tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
            # Rotate 90 degrees to get normal in 2D plane (x,y)
            normal = np.array([-tangent[1], tangent[0], 0])
            normals.append(normal)
            
        belt_group = VGroup()
        
        # 1. Top Surface (Ribbon defined by P and P + normal*width)
        ribbon_width = 0.6
        
        # Construct polygon points
        upper_edge = []
        lower_edge = []
        
        for p, n in zip(points, normals):
            upper_edge.append(p + n * ribbon_width)
            lower_edge.append(p)
            
        top_poly_points = upper_edge + lower_edge[::-1]
        top_surface = Polygon(*top_poly_points, fill_color=LIGHT_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=2)
        
        # 2. Side Surface (Extruded down from lower edge)
        # Lower edge is 'p' (the main curve line)
        side_depth = 0.4
        side_edge_points = lower_edge # This is just points[]
        
        side_poly_points = side_edge_points + [p + DOWN * side_depth for p in side_edge_points[::-1]]
        side_surface = Polygon(*side_poly_points, fill_color=DARK_GREEN, fill_opacity=1, stroke_color=DARK_GREEN, stroke_width=1)
        
        belt_group.add(side_surface, top_surface)
        
        # 3. Moving Elements (Rivets + Tracks)
        # Use a ValueTracker to animate the position along the curve parameter
        # This ensures they stay spaced and follow curve exactly
        
        moving_elements = VGroup()
        # Create a set of lines and rivets
        num_items = 45 
        
        # We'll use a virtual 'offset' for each item
        # We won't add an updater to individual items to shift X
        # Instead we'll add an updater to the GROUP to redraw? Or update positions.
        
        # Let's create them at initial positions
        self.belt_offsets = np.linspace(0, 14, num_items, endpoint=False) # Spanning -7 to 7 is width 14
        self.belt_items = []
        
        for i in range(num_items):
            # Create Rivet
            rivet = Circle(radius=0.04, fill_color="#1A3317", stroke_width=0, fill_opacity=0.8)
            # Create Track Line
            line = Line(ORIGIN, RIGHT * ribbon_width, color="#3A5F0B", stroke_width=2, stroke_opacity=0.6)
            
            grp = VGroup(rivet, line)
            self.belt_items.append(grp)
            moving_elements.add(grp)
            
        self.belt = belt_group
        self.moving = moving_elements
        
        # Animate creation
        self.play(DrawBorderThenFill(belt_group), run_time=2)
        self.play(FadeIn(moving_elements), run_time=1)
        
        # Robust Updater for Moving Elements
        # This function runs every frame to update positions of rivets/lines
        def robust_move_updater(mob, dt):
            # Advance offsets
            speed = 1.0
            self.belt_offsets = (self.belt_offsets + speed * dt) % 14.0 # Wrap at 14 width
            
            # Map offsets to X coordinates
            # Range -7 to 7. Offset 0 -> -7. Offset 14 -> 7.
            current_xs = self.belt_offsets - 7.0
            
            for grp, x in zip(self.belt_items, current_xs):
                rivet = grp[0]
                line = grp[1]
                
                # Get Geometry at X
                p = self.get_sigmoid_point(x)
                p_next = self.get_sigmoid_point(x + 0.1)
                tangent = p_next - p
                tangent = tangent / (np.linalg.norm(tangent) + 1e-6)
                normal = np.array([-tangent[1], tangent[0], 0])
                
                # Position Rivet
                rivet.move_to(p + DOWN * (side_depth/2))
                
                # Position Line
                l_width = 0.55
                start = p + normal * 0.02
                end = p + normal * 0.58
                line.put_start_and_end_on(start, end)
                
        self.moving.add_updater(robust_move_updater)
        
        # UPDATE ANCHORS based on new belt path (center of top surface)
        self.anchors = []
        stage_x_coords = [-5, -2, 0.5, 3, 5.5]
        for x in stage_x_coords:
            p = self.get_sigmoid_point(x)
            # Find normal roughly
            p_n = self.get_sigmoid_point(x+0.01)
            t = p_n - p
            t = t/np.linalg.norm(t)
            n = np.array([-t[1], t[0], 0])
            
            center_top = p + n * (ribbon_width/2)
            self.anchors.append(center_top)
    
    def get_text_pos(self, step_index):
        """Calculate text position below correspondin stage"""
        # x matches anchor, y is fixed
        x = self.anchors[step_index][0]
        return np.array([x, self.TEXT_Y[1], 0])

    def create_stage_label(self, idx, title_text, desc_text):
        """
        Generic method to create and position stage labels.
        
        - Wraps description text automatically.
        - Determines placement (Above/Below) based on belt height at anchor.
        """
        anchor = self.anchors[idx]
        
        # 1. Create Title
        # Check if title has a number prefix "X. Title"
        # We can split it or just display as is. 
        # User's previous code split "1. Harvest" and "Energy Crops".
        # Let's try to keep it simple: generic title + Wrapped Description
        
        # If title has newline, split it
        if '\n' in title_text:
            parts = title_text.split('\n')
            t1 = Text(parts[0], font_size=24, color=DARK_GREEN, weight=BOLD)
            t2 = Text(parts[1], font_size=24, color=DARK_GREEN, weight=BOLD)
            step_label = VGroup(t1, t2).arrange(DOWN, center=True)
        else:
            step_label = Text(title_text, font_size=24, color=DARK_GREEN, weight=BOLD)
            
        # 2. Wrap Description
        wrapper = textwrap.TextWrapper(width=30)
        wrapped_desc = wrapper.fill(text=desc_text)
        
        step_desc = Text(
            wrapped_desc,
            font_size=16, color=DARK_GREEN, line_spacing=1.2
        )
        
        # Group them
        step_text = VGroup(step_label, step_desc).arrange(DOWN, buff=0.1)
        
        # 3. Smart Placement
        # If anchor is low (y < -0.5), place ABOVE. Else BELOW.
        if anchor[1] < -0.5:
            # Place Above
            step_text.move_to(anchor + UP * 2.5) 
            # Harvest specifically was UP * 3.3, maybe we need dynamic offset?
            # Let's use a safe margin.
            if idx == 0: # Harvest is very low
                 step_text.move_to(anchor + UP * 3.3)
            else:
                 step_text.move_to(anchor + UP * 2.5)
        else:
            # Place Below
            step_text.move_to(anchor + DOWN * 1.8)
            
            # Special case for stage 3 or 4 if needed?
            # Standardizing to DOWN * 1.8 seems safe for others (Grinding, Cooking, etc)
        
        return step_text

    def stage_1_crops(self):
        """
        Stage 1: Harvest Energy Crops.
        
        - Spawns corn plants and a tractor.
        - Uses simple scaling and positioning relative to belt anchors.
        """
        idx = 0
        anchor = self.anchors[idx]
        
        # Create corn image (Replaces diagram)
        # corn1 = create_corn_plant()
        # corn1.scale(0.6)
        # corn1.next_to(anchor, UP, buff=0)
        # corn1.move_to(anchor + UP * 1.0 + LEFT * 0.3) 
        
        # corn2 = create_corn_plant()
        # corn2.scale(0.5) 
        # corn2.next_to(corn1, RIGHT, buff=-0.1, aligned_edge=DOWN)
        # corn2.shift(DOWN * 0.05)
        
        # REPLACEMENT: Single Corn Image
        crops_img = ImageMobject("images/corn.png").scale_to_fit_height(2.4)
        # Fix placement: Align bottom to anchor and sink slightly
        crops_img.move_to(anchor, DOWN).shift(DOWN * 0.4)

        
        
        # Label (Generic)
        step_text = self.create_stage_label(
            idx, 
            "1. Harvest\nEnergy Crops", 
            "Farmers grow corn/sugarcane containing natural sugars."
        )
        
        # Animate
        self.play(FadeIn(step_text, shift=UP * 0.5), run_time=1)
        self.play(FadeIn(crops_img, shift=UP), run_time=1.5)

        
        self.stage1_group = Group(step_text, crops_img)
    
    def stage_2_grinding(self):
        """
        Stage 2: Grinding Process.
        
        - Introduces the grinder machine with rotating gears.
        - Gears are animated using a continuous updater (dt).
        """
        idx = 1
        anchor = self.anchors[idx]
        
        # REPLACEMENT: Grinder Image
        grinder = ImageMobject("images/grinder.png").scale_to_fit_height(3.0)
        # Fix placement: Align bottom to anchor and sink slightly
        grinder.move_to(anchor, DOWN).shift(DOWN * 0.4)
        
        # Label (Generic)
        step_text = self.create_stage_label(
            idx, 
            "2. Grinding", 
            "Milling machine grinds kernels into fine powder."
        )
        
        # Animate
        self.play(FadeIn(step_text, shift=UP * 0.5), run_time=1)
        self.play(FadeIn(grinder, shift=DOWN), run_time=1)

        
        self.stage2_group = Group(step_text, grinder)
    

    def stage_3_cooking(self):
        """
        Stage 3: Cooking & Fermentation.
        
        - Displays a cooking vat, flask, water beaker, and yeast packet.
        - Features complex continuous animations:
            - Flowing water stream (CubicBezier with stroke opacity wiggling).
            - Falling yeast particles (Circles moving along line with reset).
            - Rising steam and bubbles.
        """
        idx = 2
        anchor = self.anchors[idx]
        
        # REPLACEMENT: Cooking Vat Image
        vat = ImageMobject("images/cooking_vat.png").scale_to_fit_height(3.0)
        # Fix placement: Align bottom to anchor and sink slightly
        vat.move_to(anchor, DOWN).shift(DOWN * 0.4)
        
        step_text = self.create_stage_label(
            idx, 
            "3. Cooking", 
            "Mix with water & yeast to create 'raw' ethanol."
        )
        
        self.play(FadeIn(step_text, shift=UP * 0.5), run_time=1)
        # Only fade in Vat, no other items
        self.play(FadeIn(vat, shift=DOWN), run_time=1)
        
        self.wait(3)
        
        self.stage3_group = Group(step_text, vat)
    
    def stage_4_distillation(self):
        """
        Stage 4: Purification/Distillation.
        
        - Shows the distillation column where alcohol is purified.
        - Simple fade-in animation.
        """
        idx = 3
        anchor = self.anchors[idx]
        
        # REPLACEMENT: Purifying Image
        col = ImageMobject("images/purfifying.png").scale_to_fit_height(2.8)
        # Fix placement: Align bottom to anchor and sink slightly
        col.move_to(anchor, DOWN).shift(DOWN * 0.4)
        
        step_text = self.create_stage_label(
            idx, 
            "4. Purifying", 
            "Heating creates 100% pure high-power alcohol."
        )
        
        # Animate
        self.play(FadeIn(step_text, shift=UP * 0.5), run_time=1)
        self.play(FadeIn(col, shift=DOWN), run_time=1)
        
        self.stage4_group = Group(step_text, col)
    
    def stage_5_fuel(self):
        """
        Stage 5: Final Green Fuel.
        
        - Displays the fuel pump and a car.
        - Represents the end product: Ethanol-blended fuel.
        """
        idx = 4
        anchor = self.anchors[idx]
        
        # REPLACEMENT: Petrol Pump Image
        pump = ImageMobject("images/petrol_pump.png").scale_to_fit_height(2.5)
        # Fix placement: Align bottom to anchor and sink slightly (More to fix car)
        pump.move_to(anchor, DOWN).shift(DOWN * 0.55)
        
        step_text = self.create_stage_label(
            idx, 
            "5. Green Mix", 
            "Mixed with petrol (E20) for cleaner cars."
        )
        
        # Animate
        self.play(FadeIn(step_text, shift=UP * 0.5), run_time=1)
        self.play(FadeIn(pump, shift=DOWN), run_time=1)
        
        self.stage5_group = Group(step_text, pump)