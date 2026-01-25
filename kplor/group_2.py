from manim import *

import random

import numpy as np

from math import pi, sin, cos

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        # Deterministic color definitions
        FONT_COLOR_1 = ManimColor("#000000")
        FONT_COLOR_2 = ManimColor("#9AA4B2")
        FONT_COLOR_3 = ManimColor("#B96606")
        ACCENT_COLOR_1 = ManimColor("#00ADEE")
        ACCENT_COLOR_2 = ManimColor("#F8CF0A")
        HIGHLIGHT_COLOR = ManimColor("#B96606")

        ## Section 1
        # Title fade-in over 0.8 seconds, remaining for 10.91 seconds
        title_text = Text(
            "The Six Pillars of Competency –\nHexagonal Knowledge Structure",
            font_size=40,
            color=ManimColor("#2C3E50"),
            weight=BOLD
        )
        title_text.to_edge(UP, buff=0.15)
        
        self.play(FadeIn(title_text), run_time=0.8)
        self.wait(10.91)
        
        ## Section 2
        # Central hexagon construction and fade-in
        hex_height = 0.18 * self.camera.frame_height
        hex_width = hex_height * np.sqrt(3)
        
        # Create regular hexagon using RegularPolygon
        central_hex = RegularPolygon(
            n=6,
            radius=hex_height / np.sqrt(3),
            fill_color=ManimColor("#004080"),
            fill_opacity=1,
            stroke_color=ManimColor("#A9CCE3"),
            stroke_width=2
        )
        central_hex.move_to(ORIGIN)
        
        # Create shadow/depth effect with offset duplicate
        shadow_hex = central_hex.copy()
        shadow_hex.set_fill(ManimColor("#003060"), opacity=1)
        shadow_hex.shift(DOWN * 0.05 + RIGHT * 0.05)
        
        # Central text
        central_text = Text(
            "BUSINESS ANALYTICS",
            font_size=int(0.06 * self.camera.frame_height),
            color=ManimColor("#46C5C5"),
            weight=BOLD
        )
        central_text.move_to(central_hex.get_center())
        
        # Icon: interconnected nodes (4-5 circles with connecting lines)
        icon_radius = 0.015 * self.camera.frame_height
        icon_circles = VGroup()
        icon_positions = [
            UP * 0.06 * self.camera.frame_height,
            DOWN * 0.06 * self.camera.frame_height,
            LEFT * 0.06 * self.camera.frame_height,
            RIGHT * 0.06 * self.camera.frame_height
        ]
        
        for pos in icon_positions:
            circle = Circle(
                radius=icon_radius,
                fill_color=ManimColor("#A9CCE3"),
                fill_opacity=0.4,
                stroke_width=0
            )
            circle.move_to(central_hex.get_center() + pos)
            icon_circles.add(circle)
        
        # Connecting lines
        icon_lines = VGroup()
        for i in range(len(icon_positions)):
            for j in range(i + 1, len(icon_positions)):
                line = Line(
                    icon_circles[i].get_center(),
                    icon_circles[j].get_center(),
                    color=ManimColor("#0F79C0"),
                    stroke_width=1.5,
                    stroke_opacity=0.4
                )
                icon_lines.add(line)
        
        # Group central hexagon assembly
        central_assembly = VGroup(shadow_hex, central_hex, icon_circles, icon_lines, central_text)
        
        self.play(FadeIn(central_assembly), run_time=0.6)
        
        # Gentle rotation/bobbing motion for icon circles (slow, continuous)
        def update_icon_rotation(mob, dt):
            mob.rotate(0.3 * dt, about_point=central_hex.get_center())
        
        icon_circles.add_updater(update_icon_rotation)
        
        self.wait(12.11)
        
        ## Section 3
        # Construct six surrounding hexagons
        surrounding_hexagons = VGroup()
        surrounding_texts = VGroup()
        surrounding_icons = VGroup()
        
        hex_labels = [
            "Data Collection &\nCleaning",
            "Statistical\nAnalysis",
            "Predictive\nModeling",
            "Machine Learning\n& AI",
            "Data Visualization\n& Dashboards",
            "SQL & Database\nManagement"
        ]
        
        # Positions at 60-degree angles around center
        angles = [90, 30, -30, -90, -150, 150]  # degrees
        
        surrounding_hex_objects = []
        fade_animations = []
        
        for idx, (angle_deg, label) in enumerate(zip(angles, hex_labels)):
            angle_rad = angle_deg * DEGREES
            
            # Position hexagon adjacent to central hexagon
            distance = hex_height * 1.5
            hex_pos = distance * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            
            # Create surrounding hexagon
            surr_hex = RegularPolygon(
                n=6,
                radius=hex_height / np.sqrt(3),
                fill_color=ManimColor("#6CB4EE"),
                fill_opacity=0.15,
                stroke_color=ManimColor("#A9CCE3"),
                stroke_width=2
            )
            surr_hex.move_to(hex_pos)
            
            # Shadow for surrounding hexagon
            surr_shadow = surr_hex.copy()
            surr_shadow.set_fill(ManimColor("#5BA3DD"), opacity=0.12)
            surr_shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
            
            # Text label
            label_text = Text(
                label,
                font_size=20,
                color=ManimColor("#5D6D7E"),
                weight=BOLD
            )
            label_text.move_to(surr_hex.get_center())
            
            # Group hexagon with text
            hex_group = VGroup(surr_shadow, surr_hex, label_text)
            surrounding_hex_objects.append(hex_group)
            
            # Staggered fade-in animation
            start_time = idx * 0.3
            fade_animations.append((hex_group, start_time))
        
        # Play staggered fade-ins
        for hex_group, start_time in fade_animations:
            self.play(FadeIn(hex_group), run_time=0.4)
            if start_time < 20.83 - (len(fade_animations) - 1) * 0.3 - 0.4:
                wait_time = 0.3 - 0.4
                if wait_time > 0:
                    self.wait(wait_time)
        
        # Add all surrounding hexagons to scene
        for hex_group in surrounding_hex_objects:
            surrounding_hexagons.add(hex_group)
        
        # Wait for remainder of section
        remaining_time = 20.83 - (len(fade_animations) * 0.4 + (len(fade_animations) - 1) * 0.3)
        if remaining_time > 0:
            self.wait(remaining_time)
        
        ## Section 4
        # Pulsing animation for 2 seconds
        all_hexagons = VGroup(central_assembly, surrounding_hexagons)
        
        # Pulse: opacity oscillates between 85% and 100% with 3-second period
        # Over 2 seconds, we'll do partial pulse
        pulse_start_opacity = 1.0
        pulse_min_opacity = 0.85
        
        def pulse_updater(mob, alpha):
            # 2-second animation mapped to pulse cycle
            cycle_progress = (alpha * 2.0) / 3.0  # 2 seconds into 3-second cycle
            opacity = pulse_min_opacity + (pulse_start_opacity - pulse_min_opacity) * (np.cos(cycle_progress * TAU) + 1) / 2
            mob.set_opacity(opacity)
        
        # Gentle compaction: all hexagons move inward
        center_point = ORIGIN
        compaction_vectors = []
        for hex_group in surrounding_hex_objects:
            current_pos = hex_group.get_center()
            direction = (center_point - current_pos) / np.linalg.norm(center_point - current_pos)
            compaction_vectors.append(direction * 0.15)
        
        # Also compact central assembly slightly
        central_compaction = np.array([0, 0, 0])
        
        # Play pulse and compaction simultaneously
        pulse_anim = UpdateFromAlphaFunc(all_hexagons, pulse_updater)
        compaction_anims = [
            hex_group.animate.shift(vec)
            for hex_group, vec in zip(surrounding_hex_objects, compaction_vectors)
        ]
        
        self.play(pulse_anim, *compaction_anims, run_time=2.0)
        
        # Hold stable for remainder
        self.wait(0.2)
        
        # Collapse animation: 1.5 seconds
        collapse_anims = []
        
        # Central hexagon collapses to center
        collapse_anims.append(
            central_assembly.animate.scale(0.01).move_to(ORIGIN).set_opacity(0)
        )
        
        # Surrounding hexagons collapse to center
        for hex_group in surrounding_hex_objects:
            hex_center = hex_group.get_center()
            direction = -hex_center / (np.linalg.norm(hex_center) + 0.001)
            collapse_anims.append(
                hex_group.animate.scale(0.01).move_to(ORIGIN).set_opacity(0)
            )
        
        self.play(*collapse_anims, run_time=1.5)
        
        # Create luminous dot at center
        luminous_dot = Circle(
            radius=0.1,
            fill_color=ManimColor("#76B8CE"),
            fill_opacity=0.8,
            stroke_color=ManimColor("#374149"),
            stroke_width=2
        )
        luminous_dot.move_to(ORIGIN)
        
        # Add glow effect using set_sheen
        luminous_dot.set_sheen(-0.3, UP)
        
        self.play(FadeIn(luminous_dot), run_time=0.5)
        
        # Gentle pulse for luminous dot
        def dot_pulse(mob, alpha):
            scale_factor = 1.0 + 0.1 * np.sin(alpha * TAU)
            mob.set_height(0.2 * scale_factor)
        
        self.play(
            UpdateFromAlphaFunc(luminous_dot, dot_pulse),
            run_time=11.29
        )
