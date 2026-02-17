from manim import *
import random
import numpy as np
from math import pi, sin, cos
import textwrap

config.background_color = ManimColor("#F9FAFC")

class FinalScene(MovingCameraScene):
    def construct(self):
        ## Section 1
        title = Text(
            "How Animals Eat!",
            weight=BOLD,
            color=ManimColor("#444B55")
        ).scale(1.3).move_to(UP * 3.5)
        
        # 1) The Title animation is very basic make the title appear letter by letter like "How Animals Eat!"
        self.play(Write(title), run_time=2.0)
        
        central_axis = Rectangle(
            height=4.5,
            width=0.3,
            fill_color=ManimColor("#3FA9F5"),
            fill_opacity=1,
            stroke_width=0
        ).move_to(DOWN * 0.2)
        
        self.play(GrowFromEdge(central_axis, DOWN), run_time=5.44)
        
        ## Section 2
        bar_width = 4.0
        bar_height = 0.6
        gap = 1.2
        
        colors = [
            ManimColor("#4CAF50"),
            ManimColor("#E74C3C"),
            ManimColor("#8B7CF6"),
            ManimColor("#8B6F47"),
            ManimColor("#95A5A6")
        ]
        
        categories = ["Herbivores", "Carnivores", "Omnivores", "Parasites", "Scavengers"]
        
        axis_top = central_axis.get_top()
        positions = [
            axis_top + DOWN * (gap * i) for i in range(5)
        ]
        
        bars = []
        bar_starts = []
        
        for i, (pos, color) in enumerate(zip(positions, colors)):
            final_bar = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            ).move_to(pos)
            
            start_bar = final_bar.copy().stretch_to_fit_width(0.01)
            bar_starts.append(start_bar)
            bars.append(final_bar)
            self.add(start_bar)
        
        bar_animations = [Transform(bar_starts[i], bars[i]) for i in range(5)]
        self.play(LaggedStart(*bar_animations, lag_ratio=0.15), run_time=6.36)
        
        for i in range(5):
            bars[i] = bar_starts[i]
        
        ## Section 3
        icon_paths = [
            "../images/aced_science_1.png",
            "../images/aced_science_2.png",
            "../images/aced_science_3.png",
            "../images/aced_science_4.png",
            "../images/aced_science_5.png"
        ]
        
        icons = []
        labels = []
        icon_label_anims = []
        
        for i, (bar, category, icon_path, color) in enumerate(zip(bars, categories, icon_paths, colors)):
            icon = ImageMobject(icon_path).scale(0.25).move_to(bar.get_left() + RIGHT * 0.5)
            icons.append(icon)
            
            label = Text(
                category,
                color=ManimColor("#444B55"),
                weight=BOLD
            ).scale(0.5).next_to(icon, RIGHT, buff=0.2)
            labels.append(label)
            
            # 3) The icons and text inside Herbivors;carnivores etc appears very basic create a bouncing effect 
            # that icons and text bounces and places inside that rectangle block itself
            icon_anim = GrowFromCenter(icon, rate_func=rate_functions.ease_out_elastic, run_time=1.5)
            label_anim = GrowFromCenter(label, rate_func=rate_functions.ease_out_elastic, run_time=1.5)
            icon_label_anims.append(AnimationGroup(icon_anim, label_anim))
            
        self.play(LaggedStart(*icon_label_anims, lag_ratio=0.3), run_time=4.0)
        
        ## Section 4
        definitions = [
            "Eat only plants",
            "Eat other animals",
            "Eat plants and animals",
            "Live on or inside other animals for food",
            "Eat dead animals"
        ]
        
        examples = [
            "Like cows and rabbits",
            "Like tigers and eagles",
            "Like bears and humans",
            "Like ticks and fleas",
            "Like vultures and hyenas"
        ]
        
        branches_data = []
        branch_animations = []
        
        # 2) decrease the length of straight lines that are joined between blocks of herbivors and eat only plants type of blocks
        # it is pushing the corner blocks to the edges
        line_seg_lengths = [0.5, 0.2, 0.5] # Reduced from 0.8, 0.4, 1.0

        for i, (bar, color, category) in enumerate(zip(bars, colors, categories)):
            left_start = bar.get_left()
            right_start = bar.get_right()
            
            left_p1 = left_start
            left_p2 = left_p1 + LEFT * line_seg_lengths[0]
            left_p3 = left_p2 + LEFT * line_seg_lengths[1]
            left_p4 = left_p3 + LEFT * line_seg_lengths[2]
            
            right_p1 = right_start
            right_p2 = right_p1 + RIGHT * line_seg_lengths[0]
            right_p3 = right_p2 + RIGHT * line_seg_lengths[1]
            right_p4 = right_p3 + RIGHT * line_seg_lengths[2]
            
            left_l1 = Line(left_p1, left_p2, color=color, stroke_width=4)
            left_l2 = Line(left_p2, left_p3, color=color, stroke_width=4)
            left_l3 = Line(left_p3, left_p4, color=color, stroke_width=4)
            left_branch = VGroup(left_l1, left_l2, left_l3)
            
            right_l1 = Line(right_p1, right_p2, color=color, stroke_width=4)
            right_l2 = Line(right_p2, right_p3, color=color, stroke_width=4)
            right_l3 = Line(right_p3, right_p4, color=color, stroke_width=4)
            right_branch = VGroup(right_l1, right_l2, right_l3)
            
            branches_data.append({
                "left_branch": left_branch,
                "right_branch": right_branch,
                "left_end": left_p4,
                "right_end": right_p4,
                "color": color
            })
            
            branch_animations.append(AnimationGroup(Create(left_branch), Create(right_branch), lag_ratio=1))

        self.play(LaggedStart(*branch_animations, lag_ratio=1), run_time=4.36)
        
        self.wait(2.0)
        
        ## Section 5
        definition_boxes = []
        example_boxes = []
        box_animations = []
        
        # 4) some text is being overlapped from the block create a logic that dynamically adjust the text like if overlapping is there 
        # it will show text in next line instead of overlapping with blocks
        def create_wrapped_text(text_content, width=24):
            wrapped_text = textwrap.fill(text_content, width=width)
            return Text(
                wrapped_text,
                color=ManimColor("#444B55"),
                weight=BOLD,
                line_spacing=0.8
            ).scale(0.35)

        for i, (branch_data, definition, example, color) in enumerate(zip(branches_data, definitions, examples, colors)):
            left_end = branch_data["left_end"]
            right_end = branch_data["right_end"]
            
            left_def_box = Rectangle(
                width=3.0,
                height=1.2,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            ).move_to(left_end + LEFT * 1.5)
            
            left_def_text = create_wrapped_text(definition).move_to(left_def_box.get_center())
            
            right_def_box = Rectangle(
                width=3.0,
                height=1.2,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            ).move_to(right_end + RIGHT * 1.5)
            
            right_def_text = create_wrapped_text(example).move_to(right_def_box.get_center())
            

            box_animations.append(AnimationGroup(
                GrowFromCenter(left_def_box, run_time=0.767),
                FadeIn(left_def_text, run_time=0.567),
                GrowFromCenter(right_def_box, run_time=0.767),
                FadeIn(right_def_text, run_time=0.567),
                lag_ratio=1
            ))

            definition_boxes.append((left_def_box, left_def_text, right_def_box, right_def_text))
            
        self.play(LaggedStart(*box_animations, lag_ratio=1), run_time=5.2)

        self.wait(1.45)
        
        ## Section 6
        ## Section 6
        self.wait(2.0)
        
        # Gather mobjects for exit animation
        lines_group = VGroup()
        for branch_data in branches_data:
            lines_group.add(branch_data["left_branch"])
            lines_group.add(branch_data["right_branch"])
            
        left_blocks_group = VGroup()
        right_blocks_group = VGroup()
        
        for box_tuple in definition_boxes:
            left_def_box, left_def_text, right_def_box, right_def_text = box_tuple
            left_blocks_group.add(left_def_box, left_def_text)
            right_blocks_group.add(right_def_box, right_def_text)
            
        center_blocks = []
        for i in range(5):
            center_blocks.append(Group(bars[i], icons[i], labels[i]))
            
        # Animation Sequence (Total ~4s)
        # 1. Lines and Central Axis Fade Out (1.0s)
        self.play(
            FadeOut(lines_group),
            FadeOut(central_axis),
            run_time=1.0
        )
        
        # 2. Exits (3.0s)
        self.play(
            title.animate.shift(UP * 8), # Title moves up
            left_blocks_group.animate.shift(LEFT * 15), # Left blocks move left
            right_blocks_group.animate.shift(RIGHT * 15), # Right blocks move right
            LaggedStart(*[FadeOut(cb, shift=DOWN * 0.5) for cb in center_blocks], lag_ratio=0.3), # Center blocks fade one by one
            run_time=3.0
        )
