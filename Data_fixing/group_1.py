from manim import *
import random
import numpy as np
from math import pi, sin, cos

class EnhancedAnalyticsJourney(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#001d3d" # Dark Blue Background
        
        # Enhanced Color Palette (Dark Mode Adapted)
        DARK_BLUE = ManimColor("#FFFFFF") # Renamed/Reused for Main Text (White for visibility)
        # Keeping variable name DARK_BLUE for minimal refactor, but it now represents WHITE/LIGHT text
        # Alternatively, could rename variables, but that requires massive refactor. 
        # Better approach: redefine DARK_BLUE to WHITE and ensure contrast elsewhere.
        
        # Or better: keep DARK_BLUE as actual dark blue for strokes, and introduce TEXT_COLOR
        # But looking at usage, DARK_BLUE is mainly text/strokes against white.
        # Let's override it to WHITE for text visibility.
        DARK_BLUE = ManimColor("#FFFFFF") 
        
        ACTUAL_DARK_BLUE = ManimColor("#1A2332") # For elements that still need to be dark (if any) or shadows
        BLUE = ManimColor("#3498DB")
        LIGHT_BLUE = ManimColor("#5DADE2")
        ACCENT_BLUE = ManimColor("#00ADEE")
        GREEN = ManimColor("#27AE60")
        ORANGE = ManimColor("#E67E22")
        PURPLE = ManimColor("#9B59B6")
        GRAY = ManimColor("#7F8C8D")
        LIGHT_GRAY = ManimColor("#ECF0F1")
        WHITE = ManimColor("#FFFFFF")
        
        # Frame configuration
        config.frame_width = 14.222
        config.frame_height = 8
        frame_width = config.frame_width
        frame_width = config.frame_width
        frame_height = config.frame_height
        
        # ===== BINARY RAIN BACKGROUND =====
        # Create falling 0s and 1s
        binary_group = VGroup()
        for i in range(150): # Increased density from 50 to 150
            x_pos = random.uniform(-frame_width/1.5, frame_width/1.5) # Spread wider than frame
            y_pos = random.uniform(-frame_height/2, frame_height/2)
            
            char = Text(
                random.choice(["0", "1"]),
                font="ISOCPEUR", # Monospace-ish font or default
                font_size=20,
                color=ManimColor("#4cc9f0"), # Cyan/Teal
                fill_opacity=random.uniform(0.1, 0.3)
            )
            char.move_to([x_pos, y_pos, -1]) # Behind everything
            
            # Additional attributes for animation
            char.fall_speed = random.uniform(1.0, 2.5) # Reduced speed (approx half of prev 2.0-5.0)
            binary_group.add(char)
            
        def rain_updater(mob, dt):
            for char in mob:
                char.shift(DOWN * char.fall_speed * dt)
                if char.get_top()[1] < -frame_height/2:
                    char.move_to([
                        char.get_x(),
                        frame_height/2 + random.uniform(0.1, 1.0),
                        -1
                    ])
                    # Randomize char on reset
                    # Note: Changing text content on the fly is expensive in Manim, 
                    # better to just move the object.
        
        binary_group.add_updater(rain_updater)
        self.add(binary_group) # Add immediately
        self.bring_to_back(binary_group)
        # "Well, welcome to our course on business analytics..."
        
        # Animated title with gradient effect
        title_text = Text(
            "Business Analytics Journey",
            font="Montserrat",
            font_size=48,
            weight=BOLD,
            
            gradient=(WHITE, LIGHT_BLUE) # Light gradient for dark background
        )
        
        max_width = 0.85 * frame_width
        if title_text.width > max_width:
            title_text.scale(max_width / title_text.width)
        
        # Start at CENTER (ORIGIN) instead of UP
        title_text.move_to(ORIGIN) 
        
        # Subtitle
        subtitle = Text(
            "From Raw Data to Strategic Impact",
            font="Montserrat",
            font_size=24,
            color=LIGHT_GRAY # Light Gray for subtitle
        )
        subtitle.next_to(title_text, DOWN, buff=0.3)
        
        # Animate title entrance
        self.play(
            FadeIn(title_text, shift=DOWN*0.3),
            run_time=1.5
        )
        self.play(
            Write(subtitle),
            run_time=1.2
        )
        self.wait(1)
        
        self.wait(1)
        
        # Move title up and fade subtitle
        self.play(
            title_text.animate.scale(0.7).to_edge(UP, buff=0.3),
            FadeOut(subtitle),
            run_time=1.5
        )
        
        # ===== SCENE 2: RAW DATA INTRODUCTION (17-32s) =====
        
        # ===== SCENE 2: RAW DATA INTRODUCTION (17-32s) =====
        # "Our journey begins with raw data..."
        
        # Clear path animations
        # self.play(
        #     FadeOut(path_glow),
        #     FadeOut(path),
        #     run_time=0.5
        # )
        
        # Create database icon - enhanced 3D look
        # Icon name: database.svg
        db_layers = VGroup()
        for i in range(4):
            layer = RoundedRectangle(
                width=1.2 - i*0.15,
                height=0.35,
                corner_radius=0.12,
                fill_color=BLUE,
                fill_opacity=0.8 - i*0.1,
                stroke_color=WHITE, # White stroke for visibility
                stroke_width=2
            )
            if i > 0:
                layer.next_to(db_layers[-1], UP, buff=0.08)
            db_layers.add(layer)
        
        # Add data lines inside database
        db_icon = VGroup(db_layers)
        db_icon.scale(1.5)
        db_icon.move_to(ORIGIN) # Start at center
        
        # "Raw Data" label
        # Revert position and color as requested
        raw_data_label = Text(
            "Raw Data",
            font="Montserrat",
            font_size=28,
            weight=BOLD,
            color=DARK_BLUE
        )
        raw_data_label.next_to(db_icon, UP, buff=0.4)
        
        # Animate database appearance
        self.play(
            LaggedStartMap(FadeIn, db_layers, lag_ratio=0.2),
            run_time=1.5
        )
        self.play(
            Write(raw_data_label),
            run_time=1.5
        )
        
        # Floating data particles
        data_particles = VGroup()
        particle_data = [
            "143", "A71", "9.2%", "USD", "2024",
            "Q3", "87K", "4.5", "TRUE", "XYZ"
        ]
        
        for i, text in enumerate(particle_data):
            particle_text = Text(
                text,
                font="Montserrat",
                font_size=16,
                color=BLACK, # Keep black if on beige background, checks out
                weight=MEDIUM
            )
            
            # Add colored circle background as requested
            particle_bg = Circle(
                radius=0.4,
                fill_color=ManimColor("#efd6ac"), # Beige color
                fill_opacity=1,
                stroke_width=0
            )
            
            particle = VGroup(particle_bg, particle_text)
            
            angle = i * (2*PI/len(particle_data))
            radius = 2.8 # Increase radius to orbit outside the label area
            x = db_icon.get_center()[0] + radius * np.cos(angle)
            y = db_icon.get_center()[1] + radius * np.sin(angle)
            particle.move_to([x, y, 0])
            data_particles.add(particle)
        
        # Animate particles with drift
        self.play(
            LaggedStartMap(FadeIn, data_particles, shift=UP*0.3, lag_ratio=0.1),
            run_time=2
        )
        
        # Orbital animation with Individual Vanishing
        # Pre-calculate vanish thresholds
        initial_particle_angles = [i * (2*PI/len(particle_data)) for i in range(len(particle_data))]
        vanish_thresholds = []
        
        for init_angle in initial_particle_angles:
            # Angle needed to reach PI/2 from start
            # (PI/2 - init) % 2PI gives positive angle to reach top
            angle_to_top = (PI/2 - init_angle) % (2*PI)
            # Add 1 full lap (2*PI)
            total_rot = 2*PI + angle_to_top
            vanish_thresholds.append(total_rot)
            
        orbit_radius = 2.8
        center_point = db_icon.get_center()
        max_rotation_anim = 4.5 * PI # Enough to cover 1 lap + max remainder (approx 4PI)

        def orbit_and_vanish(mob, alpha):
            current_rot = alpha * max_rotation_anim
            for i, particle in enumerate(mob):
                # Calculate position
                theta = initial_particle_angles[i] + current_rot
                new_x = center_point[0] + orbit_radius * np.cos(theta)
                new_y = center_point[1] + orbit_radius * np.sin(theta)
                particle.move_to([new_x, new_y, 0])
                
                # Check vanish condition
                if current_rot >= vanish_thresholds[i]:
                     particle.set_opacity(0) # Vanish
                else:
                     particle.set_opacity(1)

        self.play(
            UpdateFromAlphaFunc(data_particles, orbit_and_vanish),
            run_time=8,
            rate_func=linear
        )
        # data_particles.remove_updater(update_particles_complex) # No longer needed
        
        # New Sequence: Vanish particles FIRST (already done naturally, but ensure clean)
        # self.play(FadeOut(data_particles), run_time=1) # Redundant now, but safer to leave empty or fast
        # Just clear them to be safe
        self.remove(data_particles)
        
        # Move remaining elements (DB icon + Label) to the left
        raw_data_group = VGroup(db_icon, raw_data_label)
        
        self.play(
            raw_data_group.animate.move_to(LEFT * 4.5 + DOWN * 1.5),
            run_time=2
        )
        
        # Scale down slightly to match previous final state
        self.play(
             raw_data_group.animate.scale(0.8),
             run_time=1
        )
        
        self.wait(1)

        # REMOVED early FadeOut of raw_data_group
        # self.play(FadeOut(raw_data_group), run_time=1)
        
        # Process nodes
        node_data = [
            ("Collection", "collection.png", BLUE),
            ("Cleaning", "data-cleaning.png", LIGHT_BLUE),
            ("Analysis", "analysis.png", ManimColor("#82A6B1")),
            ("Prediction", "prediction.png", ORANGE),
            ("Visualization", "visualisation.png", ManimColor("#669bbc")),
            ("Decision", "desicion.png", ManimColor("#bb8588"))
        ]
        
        # Create curved flow path
        process_start = db_icon.get_right() + RIGHT * 0.5
        # Extend end point to the right to increase spacing
        process_end = np.array([frame_width/2 - 0.0, frame_height/2 - 1.5, 0])
        
        def process_curve(t):
            x = process_start[0] + t * (process_end[0] - process_start[0])
            # Reduce amplitude from 1.2 to 0.8 to lower the curve
            y = process_start[1] + t * (process_end[1] - process_start[1]) + 0.8 * np.sin(t * np.pi * 0.8)
            return np.array([x, y, 0])
        
        # Gradient path
        process_path = ParametricFunction(
            process_curve,
            t_range=[0, 1, 0.01],
            stroke_width=5
        )
        process_path.set_color_by_gradient(LIGHT_BLUE, BLUE, ManimColor("#0096c7")) # Beige end
        
        self.play(Create(process_path), run_time=2.5)
        
        # Create and animate nodes
        nodes_group = Group()
        
        for i, (label, icon_name, color) in enumerate(node_data):
            t = (i + 1) / (len(node_data) + 1)
            pos = process_curve(t)
            
            # Node circle with glow
            glow = Circle(
                radius=0.75,
                fill_color=color,
                fill_opacity=0.15,
                stroke_width=0
            )
            glow.move_to(pos)
            
            # Make Decision node uniform (remove special outer ring)
            
            circle = Circle(
                radius=0.6,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=3
            )
            circle.move_to(pos)
            
            # Icon placeholder (use SVG icons)
            # Use provided PNG images
            icon = ImageMobject(icon_name)
            # Scale icon to fit comfortably inside the circle (radius 0.6)
            if "desicion" in icon_name.lower():
                 icon.scale_to_fit_height(0.50) # Smaller for decision to avoid overlap
            else:
                 icon.scale_to_fit_height(0.6)
            
            icon.move_to(pos)
            
            # Label below
            text = Text(
                label,
                font="Montserrat",
                font_size=16,
                color=WHITE, # White labels
                weight=BOLD
            )
            text.next_to(circle, DOWN, buff=0.25)
            
            node = Group(glow, circle, icon, text)
            nodes_group.add(node)
            
            # Animate appearance with Camera Move
            # Camera logic: Zoom in to current node
            
            # Setup camera target
            camera_target = pos
            frame_width_target = 6.0 # Zoomed in
            
            animations = [
                FadeIn(glow),
                GrowFromCenter(circle),
                FadeIn(icon, scale=0.5),
                Write(text),
                self.camera.frame.animate.move_to(camera_target).set(width=frame_width_target)
            ]
            
            # Additional logic for specific nodes
            if i == 0:
                # First node: Fade out Raw Data group (particles already gone)
                animations.append(FadeOut(raw_data_group))
                # particles removed earlier, no need to remove again
            
            if i > 0:
                # Vanish previous node completely
                prev_node = nodes_group[i-1]
                animations.append(FadeOut(prev_node))
                # animations.append(prev_node.animate.set_opacity(0)) # Alternative if FadeOut causes issues
                
            self.play(
                *animations,
                run_time=1.5 # Slower for camera movement
            )
            self.wait(0.5)
        
        # Removed long wait: self.wait(8)
        self.wait(0.5)
        
        # ===== SCENE 4: REMOVED (Highlighter Loop) =====
        # Logic moved to Camera Tour in Scene 3
        
        self.wait(1)
        
        # ===== SCENE 5: HUMAN IN THE LOOP (70-85s) =====
        # "Analytics empowers human decision making"
        
        # Load human icon
        # Icon name: human.svg or intro_video_39.png
        decision_node = nodes_group[5] # Define decision_node for reference
        human_icon = ImageMobject("intro_video_39.png")
        human_icon.scale(0.4)
        human_icon.move_to(decision_node.get_center() + DOWN*2.5 + LEFT*0.5)

        # Move camera to Human Icon - ALIGN WITH FEEDBACK ARROW instead
        # self.play(
        #     self.camera.frame.animate.move_to(human_icon.get_center()).set(width=5.0),
        #     run_time=1.5
        # )
        
        # Feedback arrow
        feedback_start = decision_node.get_bottom() + DOWN*0.2
        feedback_end = human_icon.get_top() + UP*0.1
        
        feedback_curve = CubicBezier(
            feedback_start,
            feedback_start + DOWN*1.2,
            feedback_end + UP*1.2 + RIGHT*0.5,
            feedback_end,
            color=ACCENT_BLUE,
            stroke_width=5
        )
        
        # Arrow tip
        arrow_tip = Triangle(
            color=ACCENT_BLUE,
            fill_opacity=1,
            stroke_width=0
        ).scale(0.15)
        arrow_tip.rotate(-PI/2)
        arrow_tip.move_to(feedback_end + DOWN*0.15)
        
        self.play(
            Create(feedback_curve),
            GrowFromPoint(arrow_tip, feedback_start),
            # Move camera along with the arrow flow
            self.camera.frame.animate.move_to(human_icon.get_center()).set(width=5.0),
            run_time=2.5
        )
        
        self.play(
            FadeIn(human_icon, scale=0.7),
            run_time=1.5
        )
        
        # Human empowerment label
        empower_text = Text(
            "Human-Powered Decisions",
            font="Montserrat",
            font_size=16, # Reduced size from 22
            color=ACCENT_BLUE,
            weight=BOLD
        )
        empower_text.next_to(human_icon, DOWN, buff=0.15) # Reduced buff
        empower_text.shift(LEFT * 0.5) # Reduced shift to keep it closer
        
        self.play(Write(empower_text), run_time=1.5)
        
        # Removed long wait: self.wait(8)
        self.wait(2)
        
        # ===== SCENE 6: BUSINESS IMPACT (85-95s) =====
        # "It transforms data into tangible business results"
        
        # Zoom out to full picture and restore Raw Data
        
        # Need to ensure raw_data_group is in the correct final position (left side)
        # It was moved there in lines 188-196. Since we faded it out, it should still be there but invisible.
        
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width), # Restore full frame
            FadeIn(raw_data_group),
            # Restore all nodes (they were faded out)
            FadeIn(nodes_group),
            run_time=2.5
        )
        
        self.wait(3)
        
        # Final hold
        self.wait(2)


