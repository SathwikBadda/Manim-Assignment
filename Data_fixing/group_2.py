from manim import *
import numpy as np
from math import pi, sin, cos
import random

class HexagonalKnowledgeStructure(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#001d3d" # Dark Blue Background
        
        # Enhanced Color Palette
        DEEP_BLUE = ManimColor("#1A365D")
        PRIMARY_BLUE = ManimColor("#2C5282")
        ACCENT_BLUE = ManimColor("#4299E1")
        LIGHT_BLUE = ManimColor("#90CDF4")
        TEAL = ManimColor("#319795")
        CYAN = ManimColor("#00B5D8")
        ORANGE = ManimColor("#DD6B20")
        PURPLE = ManimColor("#805AD5")
        GREEN = ManimColor("#38A169")
        GOLD = ManimColor("#D69E2E")
        WHITE = ManimColor("#FFFFFF")
        DARK_GRAY = ManimColor("#2D3748")
        LIGHT_GRAY = ManimColor("#E2E8F0")
        
        config.frame_width = 14.222
        config.frame_height = 8
        frame_width = config.frame_width
        frame_height = config.frame_height
        
        # ===== SCENE 1: OPENING SEQUENCE (0-15s) =====
        # 10s Grid -> Collapse -> Gradient Background -> Title
        
        # Titles defined here but animated later
        main_title = Text(
            "Course Learning Outcomes",
            font="Montserrat",
            font_size=52,
            weight=BOLD,
            gradient=(WHITE, LIGHT_BLUE)
        )
        
        subtitle = Text(
            "A Hexagonal Knowledge Structure",
            font="Montserrat",
            font_size=28,
            color=LIGHT_GRAY
        )
        subtitle.next_to(main_title, DOWN, buff=0.3)
        title_group = VGroup(main_title, subtitle)
        title_group.move_to(ORIGIN)
        
        # ===== MOVING HEXAGONAL GRID BACKGROUND =====
        # Infinite scrolling background with alternating columns
        # Improved honeycomb packing (non-overlapping)
        
        grid_hexagons = VGroup()
        
        # Packing params
        # Flat-topped hexagons (default orientation)
        # Width (point-to-point) = 2*R
        # Height (flat-to-flat) = sqrt(3)*R
        
        hex_radius = 0.4 # Smaller size as requested
        hex_width = 2 * hex_radius
        hex_height = np.sqrt(3) * hex_radius
        
        # Spacing
        # Honeycomb packing:
        # Horiz distance between centers = 1.5 * R
        # Vert distance between centers = sqrt(3) * R
        
        horiz_spacing = 1.55 * hex_radius # Slight buff for gap
        vert_spacing = hex_height * 1.05 # Slight buff
        
        cols = int(frame_width / horiz_spacing) + 6 # Ensure cover
        rows = int(frame_height / vert_spacing) + 6
        
        colors = [TEAL, BLUE, GREEN, LIGHT_GRAY, ACCENT_BLUE]
        
        # Create grid columns
        grid_columns = []
        
        for col in range(cols):
            column_group = VGroup()
            direction = UP if col % 2 != 0 else DOWN
            
            # X Calculation
            x_pos = (col - cols/2) * horiz_spacing
            
            for row in range(rows):
                # Y Calculation
                y_pos = (row - rows/2) * vert_spacing
                
                # Offset odd columns
                if col % 2 != 0:
                    y_pos += vert_spacing / 2
                
                # Randomized color but UNIFORM size
                hex_obj = RegularPolygon(
                    n=6,
                    radius=hex_radius, # Fixed radius
                    stroke_color=random.choice(colors),
                    stroke_width=2,
                    stroke_opacity=random.uniform(0.1, 0.3),
                    fill_color=random.choice(colors),
                    fill_opacity=random.uniform(0.05, 0.15)
                )
                hex_obj.move_to([x_pos, y_pos, -2]) # Behind everything
                column_group.add(hex_obj)
            
            # Store direction and speed
            column_group.direction = direction
            column_group.speed = 0.5
            grid_columns.append(column_group)
            grid_hexagons.add(column_group)
            
        self.add(grid_hexagons)
        
        # Update function for infinite vertical scroll
        def grid_updater(mob, dt):
            for col_group in mob:
                direction = col_group.direction
                speed = col_group.speed
                col_group.shift(direction * speed * dt)
                
                # Check for wrap-around
                # total height of column is roughly rows * vert_spacing
                # We need to wrap individual elements or the whole column?
                # Moving individual elements is tricky if they are in a VGroup column.
                # Easiest: Move elements.
                
                for hex_obj in col_group:
                    # Boundaries with buffer
                    top_bound = frame_height/2 + hex_height
                    bottom_bound = -frame_height/2 - hex_height
                    
                    if direction is DOWN:
                        if hex_obj.get_top()[1] < bottom_bound:
                             # Move to top of stack
                             # Find highest Y in this column? Or just shift by total height?
                             # Total height covered ~ rows * vert_spacing
                             hex_obj.shift(UP * (rows * vert_spacing))
                    else: # UP
                        if hex_obj.get_bottom()[1] > top_bound:
                             hex_obj.shift(DOWN * (rows * vert_spacing))
                             
        grid_hexagons.add_updater(grid_updater)
        # Shimmer effect updater
        def shimmer_updater(mob, dt):
            # Randomly change opacity of a few cells
            for _ in range(5):
                hex_obj = random.choice(random.choice(grid_hexagons))
                # Gentle flicker
                hex_obj.set_stroke(opacity=random.uniform(0.3, 0.6))
                
        grid_hexagons.add_updater(shimmer_updater)
        
        # Run grid animation for 10 seconds
        self.wait(10)
        
        grid_hexagons.remove_updater(shimmer_updater)
        grid_hexagons.remove_updater(grid_updater)
        
        # ===== TRANSITION: COLLAPSE & EXPAND =====
        
        # 1. Collapse Grid to Center
        # Animate all columns moving to ORIGIN and fading/scaling down
        self.play(
            grid_hexagons.animate.scale(0.01).move_to(ORIGIN).set_opacity(0),
            run_time=1.5,
            rate_func=smooth
        )
        self.remove(grid_hexagons)
        
        # 2. Form Single Hexagon
        large_hex = RegularPolygon(
            n=6,
            radius=0.1, # Start small
            fill_color=DEEP_BLUE,
            fill_opacity=1,
            stroke_color=ACCENT_BLUE,
            stroke_width=3
        )
        large_hex.move_to(ORIGIN)
        
        self.play(
            large_hex.animate.scale(40).set_stroke(width=10), # Expand huge
            run_time=1.0,
            rate_func=rush_from
        )
        
        # 3. Transform to Gradient Background
        gradient_bg = Rectangle(
            width=frame_width,
            height=frame_height,
            fill_opacity=1
        )
        gradient_bg.set_fill(color=[DEEP_BLUE, PRIMARY_BLUE], opacity=1)
        # Note: Manim's Gradient is set via set_color_by_gradient logic for some Mobjects, 
        # or fill_color=[colors]. Rectangle shading can be achieved this way.
        
        self.play(
            ReplacementTransform(large_hex, gradient_bg),
            run_time=1.5
        )
        
        # Set this as the new static background
        self.add(gradient_bg)
        self.bring_to_back(gradient_bg)
        
        # ===== TITLE ENTRANCE =====
        # Now appear on top of the new background
        self.play(
            Write(main_title, run_time=1.5),
        )
        self.play(
            FadeIn(subtitle, shift=UP*0.2),
            run_time=1
        )
        
        self.wait(2)
        
        # Move titles to top
        self.play(
            title_group.animate.scale(0.7).to_edge(UP, buff=0.4),
            run_time=1.2
        )
        
        # ===== SCENE 2: CENTRAL HEXAGON EMERGENCE =====
        # "At the very center, we have business analytics..."
        
        # Background is already Gradient Rect, so no need to dim grid_hexagons (removed)
        # Maybe dim the gradient slightly? Nah, looks good.
        
        
        # Create central hexagon with glow layers
        central_radius = 0.9 # Reduced from 1.2
        
        # Multiple glow layers for depth
        glow_layers = VGroup()
        for i in range(4):
            glow = RegularPolygon(
                n=6,
                radius=central_radius + (i * 0.15),
                fill_color=ACCENT_BLUE,
                fill_opacity=0.08 / (i + 1),
                stroke_width=0
            )
            glow_layers.add(glow)
        
        # Main central hexagon
        central_hex = RegularPolygon(
            n=6,
            radius=central_radius,
            fill_color=PRIMARY_BLUE,
            fill_opacity=0.95,
            stroke_color=DEEP_BLUE,
            stroke_width=4
        )
        
        # Inner decorative hexagon
        inner_hex = RegularPolygon(
            n=6,
            radius=central_radius * 0.85,
            stroke_color=CYAN,
            stroke_width=2,
            stroke_opacity=0.4,
            fill_opacity=0
        )
        
        # Central icon: ImageMobject
        icon_nodes = Group()
        # Using business-analytics.png for center
        image_path = "/Users/sathwikbadda/Assigment/Manim-Assignment/kplor/media/images/group_2/"
        try:
            central_icon = ImageMobject(image_path + "business-analytics.png")
            central_icon.scale_to_fit_height(1.0) # Fit inside radius 1.2
            icon_nodes.add(central_icon)
        except:
            # Fallback if image fails
            fallback_circle = Circle(radius=0.5, color=WHITE)
            icon_nodes.add(fallback_circle)

        icon_group = icon_nodes
        # icon_group.scale(0.8) # Already scaled appropriately
        
        # Central text
        central_text = Text(
            "BUSINESS\nANALYTICS",
            font="Montserrat",
            font_size=24, # Reduced font size
            color=WHITE,
            weight=BOLD,
            line_spacing=0.8
        )
        
        # Text Box for Center
        central_text_bg = RoundedRectangle(
            corner_radius=0.1,
            height=central_text.height + 0.2,
            width=central_text.width + 0.3,
            fill_color=DEEP_BLUE,
            fill_opacity=0.8,
            stroke_color=WHITE, # Using stroke logic later or default
            stroke_width=1
        )
        central_text_bg.set_stroke(color=PRIMARY_BLUE)
        central_text_bg.next_to(central_hex, DOWN, buff=0) # Attached to bottom
        central_text.move_to(central_text_bg.get_center())
        
        # Assemble central structure
        # Must be Group because it contains ImageMobject (non-VMobject)
        central_assembly = Group(
            glow_layers,
            central_hex,
            inner_hex,
            icon_group,
            central_text_bg,
            central_text
        )
        central_assembly.move_to(ORIGIN + DOWN * 0.3)
        
        # Animate emergence - MOVED TO AFTER SURROUNDING NODES
        # self.play(
        #     LaggedStartMap(GrowFromCenter, glow_layers, lag_ratio=0.2),
        #     run_time=1.5
        # )
        # ... (rest moved later)
        
        # Add gentle rotation to icon network
        # No rotation for image
        # icon_group.add_updater(rotate_icon_updater)
        
        # Pulsing glow effect
        def pulse_glow_updater(mob, dt):
            scale = 1 + 0.05 * np.sin(self.renderer.time * 2)
            mob[0].become(VGroup(*[
                RegularPolygon(
                    n=6,
                    radius=central_radius + (i * 0.15),
                    fill_color=ACCENT_BLUE,
                    fill_opacity=(0.08 / (i + 1)) * scale,
                    stroke_width=0
                ).move_to(central_assembly.get_center())
                for i in range(4)
            ]))
        
        self.wait(6.5)
        
        # ===== SCENE 3: SIX SURROUNDING HEXAGONS (24-45s) =====
        # "Around this core, six vital areas emerge..."
        
        # Define the six competencies
        # Define the six competencies
        competencies = [
            {
                "title": "Data Collection\n& Cleaning",
                "icon_name": "data-collection.png",
                "color": TEAL,
                "angle": 90,
                "icon_type": "database"
            },
            {
                "title": "Statistical\nAnalysis",
                "icon_name": "data-cleaning.png", # Using cleaning icon for stats (closest fit)
                "color": PURPLE,
                "angle": 30,
                "icon_type": "chart"
            },
            {
                "title": "Predictive\nModeling",
                "icon_name": "predictive-models.png",
                "color": ORANGE,
                "angle": -30,
                "icon_type": "crystal_ball"
            },
            {
                "title": "Machine Learning\n& AI",
                "icon_name": "artificial-intelligence.png",
                "color": GOLD,
                "angle": -90,
                "icon_type": "brain"
            },
            {
                "title": "Data Visualization\n& Dashboards",
                "icon_name": "data-Visualisation.png",
                "color": GREEN,
                "angle": -150,
                "icon_type": "dashboard"
            },
            {
                "title": "SQL & Database\nManagement",
                "icon_name": "sql.png",
                "color": ACCENT_BLUE,
                "angle": 150,
                "icon_type": "sql"
            }
        ]
        
        surrounding_hexagons = Group()
        connection_lines = VGroup()
        
        hex_radius = 0.65 # Reduced from 0.85
        orbit_radius = 2.8 # Adjusted for spacing
        
        for idx, comp in enumerate(competencies):
            angle_rad = comp["angle"] * DEGREES
            
            # Position
            hex_pos = central_assembly.get_center() + orbit_radius * np.array([
                np.cos(angle_rad),
                np.sin(angle_rad),
                0
            ])
            
            # Glow layer
            glow = RegularPolygon(
                n=6,
                radius=hex_radius + 0.15,
                fill_color=comp["color"],
                fill_opacity=0.12,
                stroke_width=0
            )
            glow.move_to(hex_pos)
            
            # Main hexagon
            hexagon = RegularPolygon(
                n=6,
                radius=hex_radius,
                fill_color=comp["color"],
                fill_opacity=0.25,
                stroke_color=comp["color"],
                stroke_width=3
            )
            hexagon.move_to(hex_pos)
            
            # Inner accent
            inner_accent = RegularPolygon(
                n=6,
                radius=hex_radius * 0.85,
                stroke_color=WHITE,
                stroke_width=1.5,
                stroke_opacity=0.6,
                fill_opacity=0
            )
            inner_accent.move_to(hex_pos)
            
            # Create icon based on type
            # Load specific image
            try:
                icon = ImageMobject(image_path + comp["icon_name"])
                icon.scale_to_fit_height(0.65) # Adjusted size for better fit inside hex
            except:
                icon = Text(comp["icon_type"], font_size=20, color=WHITE)
            
            icon.move_to(hex_pos + UP * 0.1)
            
            title_text = Text(
                comp["title"],
                font="Montserrat",
                font_size=12, # Reduced font size
                color=WHITE, # Changed to WHITE as requested
                weight=BOLD,
                line_spacing=0.7
            )
            
            # Text Box
            text_bg = RoundedRectangle(
                corner_radius=0.1,
                height=title_text.height + 0.15,
                width=title_text.width + 0.2,
                fill_color=DEEP_BLUE,
                fill_opacity=0.9,
                stroke_color=comp["color"],
                stroke_width=1
            )
            # Connect to edge: Position below hexagon with 0 buff
            text_bg.next_to(hexagon, DOWN, buff=0)
            title_text.move_to(text_bg.get_center())
            
            # Connection line from center to hexagon - Start from edge of central hex
            # Vector from center to hex
            vec = hex_pos - central_assembly.get_center()
            unit_vec = vec / np.linalg.norm(vec)
            start_point = central_assembly.get_center() + unit_vec * (central_radius + 0.1) # Start at edge + small buff
            
            connection = Line(
                start_point,
                hex_pos,
                color=comp["color"],
                stroke_width=3,
                stroke_opacity=0.4
            )
            
            # Use Group for mixed content (Shapes + Image)
            hex_group = Group(glow, hexagon, inner_accent, icon, text_bg, title_text)
            surrounding_hexagons.add(hex_group)
            connection_lines.add(connection)
        
        # Animate surrounding hexagons appearing with Camera Focus and Isolation
        for i, hex_group in enumerate(surrounding_hexagons):
            # 1. Move Camera to Node
            self.play(
                self.camera.frame.animate.move_to(hex_group.get_center()).set(width=5.0), # Zoom closer
                run_time=1.0
            )
            
            # 2. Fade out others if they exist (Isolation)
            # Fade out previous nodes that might be visible
            if i > 0:
                self.play(
                    *[surrounding_hexagons[j].animate.set_opacity(0.15) for j in range(i)],
                    run_time=0.3
                )

            # 3. Reveal Node
            self.play(
                GrowFromCenter(hex_group[0]),  # glow
                GrowFromCenter(hex_group[1]),  # hexagon
                run_time=0.5
            )
            self.play(
                Create(hex_group[2]),  # inner accent
                FadeIn(hex_group[3], scale=0.5),  # icon
                FadeIn(hex_group[4]), # Text Box
                Write(hex_group[5]),  # text
                run_time=0.6
            )
            self.wait(0.5)
            
        # Restore all nodes opacity before expanding
        self.play(
            surrounding_hexagons.animate.set_opacity(1),
            run_time=0.5
        )

        # ===== CENTER REVEAL =====
        # "Shift the camera to center and display Business Analytics"
        
        self.play(
            self.camera.frame.animate.move_to(central_assembly.get_center()).set(width=8.0), # Zoom out slightly for center
            run_time=1.5
        )
        
        # Animate Central Emergence (Moved from earlier)
        self.play(
            LaggedStartMap(GrowFromCenter, glow_layers, lag_ratio=0.2),
            run_time=1.5
        )
        self.play(
            GrowFromCenter(central_hex),
            run_time=1.2
        )
        self.play(
            Create(inner_hex),
            run_time=0.8
        )
        self.play(
            FadeIn(icon_nodes, scale=0.5),
            run_time=1.5
        )
        self.play(
            Write(central_text),
            run_time=1
        )
        
        # Create Connections (Now that both ends exist)
        self.play(
            LaggedStartMap(Create, connection_lines, lag_ratio=0.1),
            run_time=1.5
        )

        self.wait(1.0)
        
        # Zoom Out to Full View
        self.play(
             self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width),
             run_time=2.0
        )
        
        self.wait(1)
        
        # ===== SCENE 4: INTERCONNECTED SYSTEM (45-57s) =====
        # "These competencies are deeply interconnected..."
        
        # Create interconnecting lines between adjacent hexagons
        inter_connections = VGroup()
        
        for i in range(6):
            next_i = (i + 1) % 6
            
            # Line between adjacent hexagons
            start_pos = surrounding_hexagons[i].get_center()
            end_pos = surrounding_hexagons[next_i].get_center()
            
            inter_line = Line(
                start_pos,
                end_pos,
                color=LIGHT_BLUE,
                stroke_width=2,
                stroke_opacity=0.3
            )
            inter_connections.add(inter_line)
        
        # Animate interconnections
        self.play(
            LaggedStartMap(Create, inter_connections, lag_ratio=0.2),
            run_time=2.5
        )
        
        # Energy pulses traveling along connections
        energy_dots = VGroup()
        
        for line in connection_lines:
            dot = Dot(color=CYAN, radius=0.08)
            dot.move_to(line.get_start())
            energy_dots.add(dot)
        
        self.play(
            LaggedStartMap(FadeIn, energy_dots, lag_ratio=0.1),
            run_time=0.8
        )
        
        # Animate dots traveling from center to hexagons
        animations = []
        for dot, line in zip(energy_dots, connection_lines):
            animations.append(
                MoveAlongPath(dot, line, rate_func=smooth)
            )
        
        self.play(
            *animations,
            run_time=2.5
        )
        
        # Fade out energy dots
        self.play(
            FadeOut(energy_dots),
            run_time=0.5
        )
        
        
        # Camera Tour Logic Removed (Merged with appearance loop)
        
        self.wait(2) # Replaces long wait
        
        # ===== SCENE 5: UNIFIED PULSE (57-70s) =====
        
        # ===== SCENE 5: UNIFIED PULSE (57-70s) =====
        # "They pulse with a shared vitality..."
        
        # Create pulsing animation for entire system
        # Must be Group because composed of Groups
        entire_system = Group(
            central_assembly,
            surrounding_hexagons,
            connection_lines,
            inter_connections
        )
        
        # Synchronized pulse effect
        self.play(
            entire_system.animate.scale(1.06),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.play(
            entire_system.animate.scale(1.04),
            rate_func=there_and_back,
            run_time=1.2
        )
        
        # Color wave through hexagons
        for i in range(6):
            self.play(
                surrounding_hexagons[i][1].animate.set_fill(opacity=0.5),
                surrounding_hexagons[i][0].animate.set_fill(opacity=0.25),
                run_time=0.2
            )
            self.play(
                surrounding_hexagons[i][1].animate.set_fill(opacity=0.25),
                surrounding_hexagons[i][0].animate.set_fill(opacity=0.12),
                run_time=0.2
            )
        
        self.wait(7)
        
        # ===== SCENE 6: UNIFIED KNOWLEDGE SYSTEM (70-82s) =====
        # "Together, they form a unified knowledge system..."
        
        # Unity label appears
        # Unity Label REMOVED as requested
        # unity_label = Text(...)
        # unity_label.to_edge(DOWN, buff=0.8)
        
        # self.play(
        #     Write(unity_label),
        #     run_time=1.5
        # )
        
        # Final emphasizing pulse
        self.play(
            entire_system.animate.scale(1.08),
            central_hex.animate.set_fill(opacity=1),
            rate_func=there_and_back,
            run_time=2
        )
        
        # Gentle zoom out to reveal complete structure
        self.play(
            self.camera.frame.animate.scale(1.1),
            run_time=2.5
        )
        
        self.wait(5)
        
        # Final hold
        self.wait(2)

