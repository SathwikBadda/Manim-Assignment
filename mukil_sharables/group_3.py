from manim.utils.rate_functions import ease_in_out_quad, ease_in_out_cubic, ease_out_back
from manim import *
from asset_manim_codes.asset_3 import Pathway
import numpy as np

class FinalScene(ThreeDScene):
    def construct(self):
        # Color definitions
        PRIMARY_ACCENT = ManimColor("#F97316")
        PRIMARY_TEXT = ManimColor("#C6C7DC")
        SECONDARY_TEXT = ManimColor("#A5B4FC")
        DATA_ACCENT = ManimColor("#22D3EE")
        SECONDARY_SHAPE = ManimColor("#8B5CF6")
        
        self.camera.background_color = ManimColor("#FFFFFF")
        
        ## Section 1
        
        heading = Text(
            "The World Needs a New Architecture",
            font="Georgia",
            font_size=32,
            color=PRIMARY_TEXT
        ).move_to(UP * 3.0)
        
        subheading = Text(
            "for Learning and Employability",
            font="Times New Roman",
            font_size=22,
            color=SECONDARY_TEXT
        ).move_to(UP * 2.2).scale(0.7)
        
        dividing_line = Line(
            start=LEFT * 8.0,
            end=RIGHT * 8.0,
            stroke_color=PRIMARY_ACCENT,
            stroke_width=2
        ).move_to(DOWN * 1.6)
        
        self.play(AddTextLetterByLetter(heading, run_time=1.5, rate_func=linear), opacity=1.0)
        
        self.play(
            heading.animate.scale(1.02),
            run_time=0.15
        )
        self.play(
            heading.animate.scale(1.0),
            run_time=0.15
        )
        
        self.play(
            FadeIn(subheading, run_time=0.9, rate_func=ease_in_out_quad),
            run_time=0.9
        )
        
        self.play(Create(dividing_line, run_time=1.8, rate_func=ease_in_out_cubic))
        
        self.play(
            heading.animate.shift(DOWN * 0.15),
            subheading.animate.shift(DOWN * 0.15),
            dividing_line.animate.shift(DOWN * 0.15),
            run_time=0.35
        )
        self.play(
            heading.animate.shift(UP * 0.15),
            subheading.animate.shift(UP * 0.15),
            dividing_line.animate.shift(UP * 0.15),
            run_time=0.35
        )
        
        self.wait(1.5)
        
        ## Section 2
        
        pathway_line = Line(
            start=LEFT * 8.0,
            end=RIGHT * 8.0,
            stroke_color=SECONDARY_SHAPE,
            stroke_width=1.5
        ).move_to(DOWN * 2.5)
        
        waypoint_labels = []
        waypoint_positions = [-6.0, -3.0, 0.0, 3.0, 6.0]
        waypoint_texts = ["School", "Higher Education", "Workplace", "Policy", "Society"]
        
        for pos, text in zip(waypoint_positions, waypoint_texts):
            label = Text(
                text,
                font="Times New Roman",
                font_size=18,
                color=SECONDARY_TEXT,
                
            ).move_to([pos, -2.5, 0]).scale(0.6)
            waypoint_labels.append(label)
        
        arc_path = VMobject()
        arc_path.set_points_as_corners([
            np.array([-6.0, -2.5, 0]),
            np.array([-3.0, 0.5, 0]),
            np.array([0.0, 0.5, 0]),
            np.array([3.0, 0.5, 0]),
            np.array([6.0, -2.5, 0])
        ])
        arc_path.set_stroke(color=DATA_ACCENT, width=1.5)
        
        arc_text = Text(
            "Dynamic Passport of Potential",
            font="Georgia",
            font_size=16,
            color=PRIMARY_TEXT
        ).move_to([0.0, 0.3, 0])
        
        box = RoundedRectangle(
            width=3.5,
            height=2.0,
            corner_radius=0.1,
            fill_opacity=0,
            stroke_color=PRIMARY_ACCENT,
            stroke_width=2
        ).move_to(ORIGIN)
        
        box_text_1 = Text(
            "mySATHI",
            font="Georgia",
            font_size=32,
            weight=BOLD,
            color=PRIMARY_TEXT
        ).move_to(ORIGIN + UP * 0.4)
        
        box_text_2 = Text(
            "Longitudinal Learning &",
            font="Times New Roman",
            font_size=18,
            color=SECONDARY_TEXT
        ).move_to(ORIGIN + DOWN * 0.15)
        
        box_text_3 = Text(
            "Talent Intelligence Infrastructure",
            font="Times New Roman",
            font_size=18,
            weight=LIGHT,
            color=SECONDARY_TEXT
        ).move_to(ORIGIN + DOWN * 0.55)
        
        self.play(Create(pathway_line, run_time=1.2, rate_func=ease_in_out_quad))
        
        for i, label in enumerate(waypoint_labels):
            self.play(FadeIn(label, run_time=0.24), run_time=0.24)
        
        self.play(Create(arc_path, run_time=1.1, rate_func=ease_in_out_cubic))
        
        self.wait(0.2)
        self.play(AddTextLetterByLetter(arc_text, run_time=0.9, rate_func=linear))
        
        self.play(GrowFromCenter(box, run_time=1.0, rate_func=ease_out_back))
        
        self.play(AddTextLetterByLetter(box_text_1, run_time=0.6, rate_func=ease_in_out_quad))
        
        self.wait(0.3)
        self.play(AddTextLetterByLetter(box_text_2, run_time=0.6, rate_func=ease_in_out_quad))
        
        self.wait(0.3)
        self.play(AddTextLetterByLetter(box_text_3, run_time=0.6, rate_func=ease_in_out_quad))
        
        self.wait(0.2)
        
        # Oscillation for pathway system
        def oscillate_pathway(obj, t):
            if t < 2.0:
                offset = 0.3 * np.sin(np.pi * t / 2.0)
                obj.shift(UP * offset)
        
        for obj in waypoint_labels + [pathway_line, arc_path, arc_text]:
            obj.add_updater(lambda m, t=0: None)
        
        self.play(
            *[
                obj.animate.shift(UP * 0.3)
                for obj in waypoint_labels + [pathway_line, arc_path, arc_text]
            ],
            run_time=2.0,
            rate_func=lambda t: np.sin(np.pi * t / 2.0)
        )
        self.play(
            *[
                obj.animate.shift(DOWN * 0.3)
                for obj in waypoint_labels + [pathway_line, arc_path, arc_text]
            ],
            run_time=2.0,
            rate_func=lambda t: np.sin(np.pi * t / 2.0)
        )
        
        self.wait(1.6)
        
        ## Section 3
        
        node_positions = {
            "TOP": UP * 3.2,
            "RIGHT": RIGHT * 4.2,
            "BOTTOM": DOWN * 3.2,
            "LEFT": LEFT * 4.2
        }
        
        node_circles = {}
        node_order = ["TOP", "RIGHT", "BOTTOM", "LEFT"]
        
        for node_name in node_order:
            circle = Circle(
                radius=0.5,
                stroke_color=PRIMARY_ACCENT,
                stroke_width=2,
                fill_opacity=0,
                
            ).move_to(node_positions[node_name]).scale(0.01)
            node_circles[node_name] = circle
        
        connecting_lines = {}
        for node_name in node_order:
            line = Line(
                start=ORIGIN,
                end=node_positions[node_name],
                stroke_color=DATA_ACCENT,
                stroke_width=1.5,
                
            )
            connecting_lines[node_name] = line
        
        image_19 = ImageMobject("../images/image_19.png").scale(0.8).move_to(node_positions["TOP"]).set_opacity(0)
        image_20 = ImageMobject("../images/image_20.png").scale(0.8).move_to(node_positions["RIGHT"]).set_opacity(0)
        image_21 = ImageMobject("../images/image_21.png").scale(0.8).move_to(node_positions["BOTTOM"]).set_opacity(0)
        image_22 = ImageMobject("../images/image_22.png").scale(0.8).move_to(node_positions["LEFT"]).set_opacity(0)
        
        label_critical = Text("Critical Thinking", font="Times New Roman", font_size=18, color=SECONDARY_TEXT).move_to(node_positions["TOP"] + DOWN * 0.8).scale(0.6)
        label_creativity = Text("Creativity", font="Times New Roman", font_size=18, color=SECONDARY_TEXT).move_to(node_positions["RIGHT"] + RIGHT * 0.8).scale(0.6)
        label_communication = Text("Communication", font="Times New Roman", font_size=18, color=SECONDARY_TEXT).move_to(node_positions["BOTTOM"] + UP * 0.8).scale(0.6)
        label_collaboration = Text("Collaboration", font="Times New Roman", font_size=18, color=SECONDARY_TEXT).move_to(node_positions["LEFT"] + LEFT * 0.8).scale(0.6)
        
        for i, node_name in enumerate(node_order):
            self.play(GrowFromCenter(node_circles[node_name], run_time=0.4, rate_func=ease_out_back))
            self.play(
                node_circles[node_name].animate.scale(1.05),
                run_time=0.05
            )
            self.play(
                node_circles[node_name].animate.scale(1.0),
                run_time=0.05
            )
            if i < len(node_order) - 1:
                self.wait(0.3)
        
        self.play(
            Create(connecting_lines["TOP"], run_time=1.5, rate_func=ease_in_out_cubic),
            Create(connecting_lines["RIGHT"], run_time=1.5, rate_func=ease_in_out_cubic),
            Create(connecting_lines["BOTTOM"], run_time=1.5, rate_func=ease_in_out_cubic),
            Create(connecting_lines["LEFT"], run_time=1.5, rate_func=ease_in_out_cubic),
            lag_ratio=0.0
        )
        
        self.play(FadeIn(image_19, run_time=0.5, rate_func=ease_in_out_quad))
        self.wait(0.15)
        self.play(FadeIn(label_critical, run_time=0.5, rate_func=ease_in_out_quad))
        
        self.wait(0.25)
        self.play(FadeIn(image_20, run_time=0.5, rate_func=ease_in_out_quad))
        self.wait(0.15)
        self.play(FadeIn(label_creativity, run_time=0.5, rate_func=ease_in_out_quad))
        
        self.wait(0.25)
        self.play(FadeIn(image_21, run_time=0.5, rate_func=ease_in_out_quad))
        self.wait(0.15)
        self.play(FadeIn(label_communication, run_time=0.5, rate_func=ease_in_out_quad))
        
        self.wait(0.25)
        self.play(FadeIn(image_22, run_time=0.5, rate_func=ease_in_out_quad))
        self.wait(0.15)
        self.play(FadeIn(label_collaboration, run_time=0.5, rate_func=ease_in_out_quad))
        
        self.wait(0.3)
        
        self.wait(2.31)
        
       ## Section 4
        
        pathway_1 = Pathway(
            title="SATHI NAO",
            subheading="Grades 8–10",
            descriptor="Early Aptitude & Scholarship Readiness"
        ).move_to(DOWN * 1.5)
        
        pathway_2 = Pathway(
            title="SATHI PATHWAYS",
            subheading="Grades 11–12",
            descriptor="Career Alignment & Skill Mapping"
        ).move_to(DOWN * 3.0)
        
        pathway_3 = Pathway(
            title="SATHI OUTCOMES",
            subheading="Higher Education & Employment",
            descriptor="Longitudinal Success Tracking"
        ).move_to(DOWN * 4.5)
        
        pathway_3.hide_arrow()
        
        self.play(pathway_1.animate_boundary_grow())
        self.play(pathway_1.animate_text_reveal())
        self.play(pathway_1.animate_arrow_reveal())
        
        self.wait(0.2)
        self.play(pathway_2.animate_boundary_grow())
        self.play(pathway_2.animate_text_reveal())
        self.play(pathway_2.animate_arrow_reveal())
        
        self.wait(0.2)
        self.play(pathway_3.animate_boundary_grow())
        self.play(pathway_3.animate_text_reveal())
        
        shield_positions = [
            UP * 4.5,
            UP * 3.2 + RIGHT * 3.5,
            RIGHT * 5.0,
            DOWN * 3.2 + RIGHT * 3.5,
            DOWN * 4.5,
            DOWN * 3.2 + LEFT * 3.5,
            LEFT * 5.0,
            UP * 3.2 + LEFT * 3.5
        ]
        
        shield_labels = [
            "Trust", "Reliability", "Security", "Transparency",
            "Integrity", "Privacy", "Accountability", "Excellence"
        ]
        
        shield_icons = []
        shield_label_objs = []
        
        for i, (pos, label_text) in enumerate(zip(shield_positions, shield_labels)):
            shield = ImageMobject("../images/image_23.png").scale(0.6).move_to(pos).set_opacity(0)
            label = Text(label_text, font="Times New Roman", font_size=14, color=SECONDARY_TEXT).move_to(pos + DOWN * 0.7).scale(0.4)
            shield_icons.append(shield)
            shield_label_objs.append(label)
        
        for i, (shield, label) in enumerate(zip(shield_icons, shield_label_objs)):
            self.play(FadeIn(shield, run_time=0.4, rate_func=ease_in_out_quad))
            self.play(FadeIn(label, run_time=0.4, rate_func=ease_in_out_quad))
            if i < len(shield_icons) - 1:
                self.wait(0.225)
        
        rotation_speeds = [0.2, 0.25, 0.18, 0.22, 0.24, 0.19, 0.23, 0.21]
        
        for shield, speed in zip(shield_icons, rotation_speeds):
            shield.add_updater(lambda m, s=speed, dt=0.016: m.rotate(s * dt))
        
        self.wait(2.68)
        
        ## Section 5
        
        for obj in [heading, subheading, dividing_line, pathway_line, box, box_text_1, box_text_2, box_text_3, arc_path, arc_text] + waypoint_labels + [image_19, image_20, image_21, image_22, label_critical, label_creativity, label_communication, label_collaboration] + list(node_circles.values()) + list(connecting_lines.values()) + [pathway_1, pathway_2, pathway_3] + shield_icons + shield_label_objs:
            obj.set_opacity(0.5)
        
        curved_flow = VMobject()
        curved_flow.set_points_as_corners([
            np.array([-8.0, -3.0, 0]),
            np.array([-5.0, -2.0, 0]),
            np.array([-2.0, -1.0, 0]),
            np.array([1.0, 0.5, 0]),
            np.array([4.0, 1.5, 0]),
            np.array([5.0, 2.0, 0])
        ])
        curved_flow.set_stroke(color=DATA_ACCENT, width=2.5)
        
        student_icons = []
        student_x_positions = [-6.0, -4.5, -3.0, -1.5, 0.0, 1.5, 3.0, 4.5]
        
        for x_pos in student_x_positions:
            y_pos = -3.0 + 0.3 * np.sin((x_pos + 6.0) / 6.0 * np.pi)
            student = ImageMobject("../images/image_24.png").scale(0.5).move_to([x_pos, y_pos, 0]).set_opacity(0)
            student_icons.append(student)
        
        rising_line = Line(
            start=DOWN * 4.5 + LEFT * 6.0,
            end=UP * 2.0 + RIGHT * 5.0,
            stroke_color=SECONDARY_SHAPE,
            stroke_width=2
        )
        
        rising_label = Text(
            "Better Fit, Lower Dropouts, Personalized Pathways, Employability Outcomes",
            font="Times New Roman",
            font_size=14,
            color=SECONDARY_TEXT
        ).move_to([0.0, -0.5, 0]).scale(0.5)
        
        conclusion_text = Text(
            "mySATHI measures what truly prepares learners for the future.",
            font="Georgia",
            font_size=24,
            weight=BOLD,
            color=PRIMARY_TEXT
        ).move_to(DOWN * 5.5)
        
        self.play(Create(curved_flow, run_time=1.4, rate_func=ease_in_out_cubic))
        
        self.wait(0.3)
        for i, student in enumerate(student_icons):
            self.play(FadeIn(student, run_time=0.3, rate_func=ease_in_out_quad))
            self.wait(0.15)
        
        self.play(Create(rising_line, run_time=1.3, rate_func=ease_in_out_cubic))
        
        self.wait(0.2)
        self.play(FadeIn(rising_label, run_time=0.8, rate_func=ease_in_out_quad))
        
        self.wait(0.8)
        self.play(FadeIn(conclusion_text, run_time=1.0, rate_func=ease_in_out_quad))
        
        self.wait(1.2)
        
        def student_flow_updater(student, dt):
            current_pos = student.get_center()
            if current_pos[0] > 6.0:
                student.move_to([-8.0, -3.0, 0])
            else:
                student.shift(RIGHT * 2.0 * dt)
        
        for student in student_icons:
            student.add_updater(student_flow_updater)
        
        self.wait(2.03)