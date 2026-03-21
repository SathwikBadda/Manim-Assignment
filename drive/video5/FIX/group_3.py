from manim import *

import random

import numpy as np

from math import pi, sin, cos

import textwrap
import os

class FinalScene(MovingCameraScene):
    def get_image_or_fallback(self, filename, scale_val=1.0, fallback_text="IMG", color=WHITE):
        if os.path.exists(filename):
            img = ImageMobject(filename)
            target_size = 0.8 * scale_val
            img.scale_to_fit_height(target_size)
            img.scale_to_fit_width(target_size)
            return img
        body = Circle(radius=0.4, color=color, fill_opacity=0.3, stroke_width=2)
        label = Text(fallback_text, font_size=24, color=WHITE)
        fallback = VGroup(body, label)
        fallback.scale(scale_val * 2)
        return fallback

    def construct(self):
        self.camera.background_color = "#2B2E4A"
        primary_font = "Comic Sans MS"
        secondary_font = "Baloo Bhai 2"

        ## Section 1
        
        title = Text("How Much Can It Hold?", font_size=48, color="#FFFFFF", font=primary_font)
        
        title_start = title.get_center() + UP * 1.5
        title.move_to(title_start)
        
        self.play(FadeIn(title), run_time=1.0)
        self.wait(2)
        self.play(title.animate.move_to(UP * 3.0), run_time=5.05)
        
        ## Section 2
        beaker = self.get_image_or_fallback("../images/capacity_11.png", scale_val=1.2, fallback_text="BEAKER")
        beaker_start = LEFT * 6 + DOWN * 4
        beaker_end = LEFT * 5 + DOWN * 1.5
        beaker.move_to(beaker_start)
        
        beaker_settled = beaker.copy().move_to(beaker_end)
        beaker_settled.scale_to_fit_height(self.camera.frame_height*0.45)
        max_beaker_width = self.camera.frame_width*0.4

        if beaker_settled.width > max_beaker_width:
            beaker_settled.scale(max_beaker_width / beaker_settled.width)

        self.play(Transform(beaker,beaker_settled), run_time=6.55)
        self.wait(1.8)
        
        ## Section 3
        ARC_RADIUS = 7
        ARC_CENTER = self.camera.frame.get_corner(DL)
        ARC_COLOR = "#9B5DE5"
        
        num_items = 4
        total_angle = num_items * 20 * DEGREES
        
        main_arc = Arc(
            radius=ARC_RADIUS,
            start_angle=5 * DEGREES,
            angle=total_angle,
            color=ARC_COLOR,
            stroke_width=5,
            arc_center=ARC_CENTER
        )
        
        self.play(Create(main_arc), run_time=3.0)
        
        ## Section 4
        top_y = main_arc.point_from_proportion(0.95)[1]
        bottom_y = main_arc.point_from_proportion(0.05)[1]
        desired_ys = np.linspace(top_y, bottom_y, num_items)
        
        target_props = []
        for y in desired_ys:
            props = np.linspace(0, 1, 200)
            arc_points = [main_arc.point_from_proportion(p) for p in props]
            closest = min(range(len(props)), key=lambda i: abs(arc_points[i][1] - y))
            target_props.append(props[closest])
        
        current_prop = 0.0
        start_point = main_arc.point_from_proportion(current_prop)
        
        traveler_dot = Dot(color=ARC_COLOR, radius=0.1)
        traveler_glow = Dot(color=ARC_COLOR, radius=0.18, fill_opacity=0.35)
        traveler_group = Group(traveler_glow, traveler_dot).move_to(start_point)
        
        self.play(FadeIn(traveler_group, scale=0.5), run_time=0.8)
        
        box_data = [
            {"title": "Teaspoon", "desc": "Holds 5 ml.", "icon": "../images/capacity_12.png"},
            {"title": "Glass", "desc": "Holds 250 ml.", "icon": "../images/capacity_13.png"},
            {"title": "Big Water Bottle", "desc": "Holds 1 Litre (l).", "icon": "../images/capacity_14.png"},
            {"title": "Remember:", "desc": "1 Litre = 1000 ml.", "icon": "../images/Litre.png"},
        ]
        
        anchors = []
        connectors = []
        full_groups = []
        icons = []
        
        self.play(FadeOut(title, shift=UP * 1.5), run_time=0.5)

        for index in range(num_items):
            data = box_data[index]
            target_prop = target_props[index]

            angle_start = main_arc.start_angle + (current_prop * main_arc.angle)
            angle_end = main_arc.start_angle + (target_prop * main_arc.angle)
            path = Arc(
                radius=ARC_RADIUS,
                start_angle=angle_start,
                angle=angle_end - angle_start,
                arc_center=ARC_CENTER
            )

            anchor_pos = main_arc.point_from_proportion(target_prop)
            anchor = traveler_dot.copy().move_to(anchor_pos)

            current_prop = target_prop

            line_end = anchor_pos + RIGHT * 1.8
            conn = Line(anchor_pos, line_end, color=ARC_COLOR, stroke_width=2.5)

            icon = ImageMobject(data["icon"])
            # Increase size for last box image only, but keep rectangle size same
            if index == 3:
                icon.scale_to_fit_height(2.0)
                icon.scale_to_fit_width(2.0)
            else:
                icon.scale_to_fit_height(0.8)
                icon.scale_to_fit_width(0.8)
            icon.set_z_index(2)

            heading = Text(
                data["title"],
                font_size=22,
                color="#FFFFFF",
                weight=BOLD,
                font=primary_font
            )

            desc = Text(
                data["desc"],
                font_size=32,
                color="#E0E7FF",
                font=secondary_font
            ).scale(0.5)

            text_col = VGroup(heading, desc).arrange(
                DOWN, aligned_edge=LEFT, buff=0.15
            )

            # Keep rectangle size same for all boxes
            content_height = max(0.8, text_col.height) + 0.5

            box = RoundedRectangle(
                width=5.0,
                height=content_height,
                corner_radius=0.2,
                stroke_color="#FF9F1C",
                fill_color="#FF9F1C",
                fill_opacity=0.8,
                stroke_width=2
            ).set_z_index(-1)

            box.move_to(line_end + RIGHT * 2.5)
            icon.next_to(box.get_left(), RIGHT, buff=0.3).match_y(box)
            text_col.next_to(icon, RIGHT, buff=0.3).match_y(box)

            full_group = Group(box, icon, text_col)
            full_groups.append(full_group)

            # Per-item animation pipeline
            self.play(MoveAlongPath(traveler_group, path),run_time = 0.5)
            self.play(FadeIn(anchor),run_time = 0.5)
            self.play(Create(conn),run_time = 0.5)
            self.play(GrowFromPoint(full_group, point=line_end),run_time = 0.5)
            #FadeIn(icon,shift=UP*0.5),
            self.play(Rotate(icon, angle=TAU, axis=OUT),run_time = 0.5)

            icons.append(icon)
            anchors.append(anchor)
            connectors.append(conn)
            #item_animations.append(item_anim)

        

        
        self.wait(1.84)
        
        ## Section 5
        section5_animations = []
        for idx in range(num_items - 1, -1, -1):
            icon = icons[idx]
            full_group = full_groups[idx]
            conn = connectors[idx]
            anchor = anchors[idx]
            
            section5_animations.append(Rotate(icon, angle=-TAU, axis=OUT, run_time=0.4))
            #section5_animations.append(FadeOut(icon, shift=DOWN*0.5))
            section5_animations.append(ShrinkToCenter(full_group, run_time=0.5))
            section5_animations.append(Uncreate(conn, run_time=0.3))
            section5_animations.append(FadeOut(anchor, run_time=0))
            
            if idx > 0:
                prev_prop = target_props[idx - 1]
                curr_prop = target_props[idx]
                ang_s = main_arc.start_angle + (curr_prop * main_arc.angle)
                ang_e = main_arc.start_angle + (prev_prop * main_arc.angle)
                ret_path = Arc(radius=ARC_RADIUS, start_angle=ang_s, angle=ang_e - ang_s, arc_center=ARC_CENTER)
                section5_animations.append(MoveAlongPath(traveler_group, ret_path, run_time=0.9))
            else:
                curr_prop = target_props[0]
                ang_s = main_arc.start_angle + (curr_prop * main_arc.angle)
                ang_e = main_arc.start_angle + (0.0 * main_arc.angle)
                ret_path = Arc(radius=ARC_RADIUS, start_angle=ang_s, angle=ang_e - ang_s, arc_center=ARC_CENTER)
                section5_animations.append(MoveAlongPath(traveler_group, ret_path, run_time=0.9))
        
        self.wait(7.35)
        
        self.play(Succession(*section5_animations),run_time = 3.0)
        
        self.play(FadeOut(traveler_group, scale=0.5), run_time=1.5)
        
        ## Section 6
        self.play(Uncreate(main_arc), run_time=2.0)
        
        beaker_start_pos = LEFT * 6 + DOWN * 6
        self.play(beaker.animate.move_to(beaker_start_pos), run_time=1.5)