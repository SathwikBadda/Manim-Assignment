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
        # Title animation
        title_text = Text(
            "Real-World Applications – Branching Specialization Tree",
            font_size=36,
            color=ManimColor("#33415C"),
            weight=BOLD,
            font="sans-serif"
        )
        title_text.move_to(ORIGIN).shift(self.camera.frame.height * 0.45 * UP)
        
        self.play(FadeIn(title_text), run_time=0.8)
        self.wait(11.3)
        
        ## Section 2
        # Central target icon with concentric circles
        circle_1 = Circle(
            radius=0.03 * self.camera.frame.height,
            stroke_width=1.5,
            color=ManimColor("#607D8B"),
            fill_opacity=0
        )
        circle_2 = Circle(
            radius=0.06 * self.camera.frame.height,
            stroke_width=1.5,
            color=ManimColor("#607D8B"),
            fill_opacity=0
        )
        circle_3 = Circle(
            radius=0.09 * self.camera.frame.height,
            stroke_width=1.5,
            color=ManimColor("#607D8B"),
            fill_opacity=0
        )
        dot_center = Dot(
            radius=0.02 * self.camera.frame.height,
            color=ManimColor("#607D8B"),
            fill_opacity=1
        )
        
        central_icon = VGroup(circle_1, circle_2, circle_3, dot_center)
        central_icon.move_to(ORIGIN)
        
        self.play(FadeIn(central_icon), run_time=0.6)
        self.wait(12.72)
        
        ## Section 3
        # Three concentric rings
        ring_1 = Circle(
            radius=0.2 * self.camera.frame.height,
            stroke_width=2,
            color=ManimColor("#BDC3C7"),
            stroke_opacity=0.3,
            fill_opacity=0
        )
        ring_1.move_to(ORIGIN)
        
        self.play(FadeIn(ring_1), run_time=0.6)
        self.wait(0.5)
        
        ring_2 = Circle(
            radius=0.3 * self.camera.frame.height,
            stroke_width=2,
            color=ManimColor("#BDC3C7"),
            stroke_opacity=0.3,
            fill_opacity=0
        )
        ring_2.move_to(ORIGIN)
        
        self.play(FadeIn(ring_2), run_time=0.6)
        self.wait(0.5)
        
        ring_3 = Circle(
            radius=0.4 * self.camera.frame.height,
            stroke_width=2,
            color=ManimColor("#BDC3C7"),
            stroke_opacity=0.3,
            fill_opacity=0
        )
        ring_3.move_to(ORIGIN)
        
        self.play(FadeIn(ring_3), run_time=0.6)
        self.wait(10.86)
        
        rings_group = VGroup(ring_1, ring_2, ring_3)
        
        ## Section 4
        # Labels for innermost ring (3 labels)
        inner_labels = []
        inner_label_texts = ["Foundational Concepts", "Data Literacy", "Analytical Thinking"]
        inner_angles = [0, 2*np.pi/3, 4*np.pi/3]
        inner_radius = 0.2 * self.camera.frame.height + 0.3
        
        inner_label_animations = []
        for idx, (text, angle) in enumerate(zip(inner_label_texts, inner_angles)):
            pos_x = inner_radius * np.cos(angle)
            pos_y = inner_radius * np.sin(angle)
            
            shadow_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#BDC3C7"),
                fill_opacity=0.05,
                stroke_width=0
            )
            shadow_rect.move_to(np.array([pos_x, pos_y, 0]) + DOWN * 0.01 + RIGHT * 0.01)
            
            main_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#F8F8F8"),
                fill_opacity=0.05,
                stroke_color=ManimColor("#BDC3C7"),
                stroke_width=2,
                stroke_opacity=0.3
            )
            main_rect.move_to(np.array([pos_x, pos_y, 0]))
            
            label_text = Text(
                text,
                font_size=22,
                color=ManimColor("#424242")
            )
            label_text.move_to(main_rect.get_center())
            
            label_group = VGroup(shadow_rect, main_rect, label_text)
            inner_labels.append(label_group)
            
            inner_label_animations.append(FadeIn(label_group))
        
        self.play(
            LaggedStart(*inner_label_animations, lag_ratio=0.4),
            run_time=1.2
        )
        
        # Labels for middle ring (4 labels)
        middle_labels = []
        middle_label_texts = ["SQL Mastery", "Statistical Methods", "Python Programming", "Visualization Design"]
        middle_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
        middle_radius = 0.3 * self.camera.frame.height + 0.3
        
        middle_label_animations = []
        for idx, (text, angle) in enumerate(zip(middle_label_texts, middle_angles)):
            pos_x = middle_radius * np.cos(angle)
            pos_y = middle_radius * np.sin(angle)
            
            shadow_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#BDC3C7"),
                fill_opacity=0.05,
                stroke_width=0
            )
            shadow_rect.move_to(np.array([pos_x, pos_y, 0]) + DOWN * 0.01 + RIGHT * 0.01)
            
            main_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#F8F8F8"),
                fill_opacity=0.05,
                stroke_color=ManimColor("#BDC3C7"),
                stroke_width=2,
                stroke_opacity=0.3
            )
            main_rect.move_to(np.array([pos_x, pos_y, 0]))
            
            label_text = Text(
                text,
                font_size=22,
                color=ManimColor("#424242")
            )
            label_text.move_to(main_rect.get_center())
            
            label_group = VGroup(shadow_rect, main_rect, label_text)
            middle_labels.append(label_group)
            
            middle_label_animations.append(FadeIn(label_group))
        
        self.play(
            LaggedStart(*middle_label_animations, lag_ratio=0.4),
            run_time=1.6
        )
        
        # Labels for outer ring (5 labels)
        outer_labels = []
        outer_label_texts = ["Capstone Project", "Real-World Case Studies", "Professional Tools", "Stakeholder Communication", "Career Readiness"]
        outer_angles = [0, 2*np.pi/5, 4*np.pi/5, 6*np.pi/5, 8*np.pi/5]
        outer_radius = 0.4 * self.camera.frame.height + 0.3
        
        outer_label_animations = []
        for idx, (text, angle) in enumerate(zip(outer_label_texts, outer_angles)):
            pos_x = outer_radius * np.cos(angle)
            pos_y = outer_radius * np.sin(angle)
            
            shadow_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#BDC3C7"),
                fill_opacity=0.05,
                stroke_width=0
            )
            shadow_rect.move_to(np.array([pos_x, pos_y, 0]) + DOWN * 0.01 + RIGHT * 0.01)
            
            main_rect = RoundedRectangle(
                width=0.14 * self.camera.frame.width,
                height=0.055 * self.camera.frame.height,
                corner_radius=0.01,
                fill_color=ManimColor("#F8F8F8"),
                fill_opacity=0.05,
                stroke_color=ManimColor("#BDC3C7"),
                stroke_width=2,
                stroke_opacity=0.3
            )
            main_rect.move_to(np.array([pos_x, pos_y, 0]))
            
            label_text = Text(
                text,
                font_size=22,
                color=ManimColor("#424242")
            )
            label_text.move_to(main_rect.get_center())
            
            label_group = VGroup(shadow_rect, main_rect, label_text)
            outer_labels.append(label_group)
            
            outer_label_animations.append(FadeIn(label_group))
        
        self.play(
            LaggedStart(*outer_label_animations, lag_ratio=0.4),
            run_time=2.0
        )
        
        all_labels = VGroup(*inner_labels, *middle_labels, *outer_labels)
        
        self.wait(2.0)
        
        # Contraction and fade animation
        contraction_animations = []
        
        # Rings contract and fade
        contraction_animations.append(
            ring_1.animate.scale(0.01).set_opacity(0)
        )
        contraction_animations.append(
            ring_2.animate.scale(0.01).set_opacity(0)
        )
        contraction_animations.append(
            ring_3.animate.scale(0.01).set_opacity(0)
        )
        
        # Labels move to origin and fade
        for label in inner_labels:
            contraction_animations.append(
                label.animate.move_to(ORIGIN).scale(0.1).set_opacity(0)
            )
        
        for label in middle_labels:
            contraction_animations.append(
                label.animate.move_to(ORIGIN).scale(0.1).set_opacity(0)
            )
        
        for label in outer_labels:
            contraction_animations.append(
                label.animate.move_to(ORIGIN).scale(0.1).set_opacity(0)
            )
        
        # Central icon grows and brightens
        contraction_animations.append(
            central_icon.animate.scale(1.5).set_opacity(1)
        )
        
        self.play(
            *contraction_animations,
            run_time=1.2
        )
        
        self.wait(17.65)
