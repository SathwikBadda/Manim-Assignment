from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *

config.background_color = "#FFFFFF"

class FinalScene(MovingCameraScene):
    def construct(self):
        # --------------------------------------------------
        # Typography & Sizing Constants
        # --------------------------------------------------
        main_font = "Helvetica"
        BASE = config.frame_height / 8
        TITLE_SIZE = 54 * BASE
        LABEL_SIZE = 50 * BASE  # Increased significantly (was 30)
        QUESTION_SIZE = 40 * BASE # Increased significantly (was 24)
        SMALL_SIZE = 35 * BASE  # Increased significantly (was 22)

        # --------------------------------------------------
        # Color Palette
        # --------------------------------------------------
        SOFT_VIOLET = "#8B7CF6"
        SUNNY_ORANGE = "#FFB703"
        SOFT_CHARCOAL = "#444B55"
        FRIENDLY_BLUE = "#3FA9F5"
        GRAPHITE_GRAY = "#444B55"
        CLOUD_WHITE = "#F9FAFC"
        OCEAN_BLUE = "#03045e"
        SKY_BLUE = "#48cae4"

        # --------------------------------------------------
        # Layout Helpers (Virtual Anchors)
        # --------------------------------------------------
        temp_title = Tex(
            "Converting Unlike Fractions to Like Fractions",
            font_size=TITLE_SIZE,
            color=BLACK
        ).to_corner(UL, buff=0.5)
        
        temp_label = Tex(
            "Let's make them friends!",
            font_size=LABEL_SIZE,
            color=SOFT_VIOLET
        ).next_to(temp_title, DOWN, buff=0.3, aligned_edge=LEFT)

        temp_question = Tex(
            r"How can we compare or add fractions like\\3/4 and 5/8 when they have\\different bottom numbers?",
            font_size=QUESTION_SIZE,
            color=BLACK,
            tex_environment="flushleft"
        ).next_to(temp_label, DOWN, buff=0.3, aligned_edge=LEFT)
        temp_question.set(width=config.frame_width * 0.45)

        temp_div = Line(LEFT, RIGHT).next_to(temp_question, DOWN, buff=0.3, aligned_edge=LEFT)
        temp_div.set(width=temp_question.width)

        DIVIDER_Y = temp_div.get_y()

        temp_goal_title = Tex(
            "The Big Goal",
            font_size=LABEL_SIZE,
            color=FRIENDLY_BLUE
        ).next_to(temp_div, DOWN, buff=0.4, aligned_edge=LEFT)

        temp_goal_note = Tex(
            "Make the bottom numbers the same!",
            font_size=SMALL_SIZE,
            color=GRAPHITE_GRAY
        ).next_to(temp_goal_title, DOWN, buff=0.2, aligned_edge=LEFT)

        # --------------------------------------------------
        # Pizza Image Integration
        # --------------------------------------------------
        pizza = ImageMobject("../images/ace_math_1.png")
        pizza.set(width=config.frame_width * 0.35)
        pizza.set(width=config.frame_width * 0.35)
        # Place pizza after (below) the left text, moved up slightly to fit
        pizza.next_to(temp_goal_note, DOWN, buff=0.1, aligned_edge=LEFT)
        pizza.shift(UP * 0.2) # "move little up"
        # Ensure it doesn't go too low, maybe check edges?
        # For now, this places it on the left side, avoiding the right panel.

        # Duplicate Pizza (Top Right)
        pizza2 = ImageMobject("../images/ace_math_1.png")
        pizza2.set(width=config.frame_width * 0.35) # Matched size (was 0.25)
        # Position roughly where the panel header will be (Top Right area)
        # Static position, shifted closer to edge and UP to fit (Feedback 9)
        # Moved very close to UR corner (buff=0.1) and minimal down shift
        pizza2.to_corner(UR, buff=0.1)
        pizza2.shift(DOWN * 0.2 + LEFT * 0.1)

        self.pizza = pizza
        self.pizza2 = pizza2

        # --------------------------------------------------
        ## Section 1
        # --------------------------------------------------
        title = Tex(
            "Converting Unlike Fractions to Like Fractions",
            font_size=TITLE_SIZE,
            color=BLACK
        )
        title.to_corner(UL, buff=0.5)

        self.play(
            Write(title),
            FadeIn(pizza, shift=UP),
            FadeIn(pizza2, shift=UP), # Animate top pizza together
            run_time=4.66
        )

        # --------------------------------------------------
        ## Section 2
        # --------------------------------------------------
        label = Tex(
            "Let's make them friends!",
            font_size=LABEL_SIZE,
            color=SOFT_VIOLET
        )
        label.next_to(title, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(
            FadeIn(label, shift=RIGHT),
            run_time=3.58
        )

        # --------------------------------------------------
        ## Section 3
        # --------------------------------------------------
        keywords_section3 = ["3/4", "5/8", "different bottom numbers"]
        
        question = Tex(
            r"How can we compare or add fractions like\\3/4 and 5/8 when they have\\different bottom numbers?",
            substrings_to_isolate=keywords_section3,
            font_size=QUESTION_SIZE,
            color=BLACK,
            tex_environment="flushleft"
        )
        question.set(width=config.frame_width * 0.45)
        question.next_to(label, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(
            Write(question),
            run_time=2.4
        )

        kw_colors_section3 = {
            "3/4": SUNNY_ORANGE,
            "5/8": SUNNY_ORANGE,
            "different bottom numbers": SUNNY_ORANGE
        }
        
        self.play(
            question.animate.set_color_by_tex_to_color_map(kw_colors_section3),
            run_time=1.22
        )

        # --------------------------------------------------
        ## Section 4
        # --------------------------------------------------
        divider = Line(
            start=LEFT,
            end=RIGHT,
            stroke_width=2,
            color=SOFT_CHARCOAL
        )
        divider.set(width=question.width)
        divider.next_to(question, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(
            Create(divider),
            run_time=2.69
        )

        # --------------------------------------------------
        ## Section 5
        # --------------------------------------------------
        goal_title = Tex(
            "The Big Goal",
            font_size=LABEL_SIZE,
            color=FRIENDLY_BLUE
        )
        goal_title.next_to(divider, DOWN, buff=0.4, aligned_edge=LEFT)

        goal_note = Tex(
            "Make the bottom numbers the same!",
            font_size=SMALL_SIZE,
            color=GRAPHITE_GRAY
        )
        goal_note.next_to(goal_title, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(
            Write(goal_title),
            run_time=1.93
        )

        self.play(
            Write(goal_note),
            run_time=1.93
        )

        # --------------------------------------------------
        ## Section 6
        # --------------------------------------------------
        unlike_label = Tex(
            "Unlike Fractions",
            font_size=35 * BASE, # Increased form 20
            color=SUNNY_ORANGE # Changed from OCEAN_BLUE (Feedback 10)
        )
        
        unlike_examples = Tex(
            r"$\frac{1}{2}, \frac{1}{3}$",
            font_size=40 * BASE, # Increased from 22
            color=SUNNY_ORANGE # Changed from OCEAN_BLUE (Feedback 10)
        )
        unlike_examples.next_to(unlike_label, DOWN, buff=0.2)

        unlike_group = VGroup(unlike_label, unlike_examples).arrange(DOWN, buff=0.2)

        like_label = Tex(
            "Like Fractions",
            font_size=35 * BASE, # Increased from 20
            color=SUNNY_ORANGE # Changed from OCEAN_BLUE (Feedback 10)
        )
        
        like_examples = Tex(
            r"$\frac{1}{4}, \frac{2}{4}$",
            font_size=40 * BASE, # Increased from 22
            color=SUNNY_ORANGE # Changed from OCEAN_BLUE (Feedback 10)
        )
        like_examples.next_to(like_label, DOWN, buff=0.2)

        like_group = VGroup(like_label, like_examples).arrange(DOWN, buff=0.2)

        panel_content = VGroup(unlike_group, like_group).arrange(DOWN, buff=0.6)

        panel_box = SurroundingRectangle(
            panel_content,
            buff=0.3,
            corner_radius=0.1,
            stroke_color=FRIENDLY_BLUE,
            stroke_width=2,
            fill_color=WHITE, # Changed from SKY_BLUE (Feedback 10)
            fill_opacity=1.0 # Increased opacity for White box
        )

        panel = Group(panel_box, panel_content)
        panel.to_edge(RIGHT, buff=0.3)
        # Reverted shift DOWN (Feedback 8) - Box stays at original height matching goal_title
        panel.match_y(goal_title, direction=UP)

        # Refine pizza2 position relative to the panel now that panel exists?
        # User wanted it "up of unlike and like fraction box".
        # We can animate it sliding into perfect position, or just leave it if it's close.
        # Let's slide it to be safe and precise.
        self.play(
            GrowFromCenter(panel_box),
            FadeIn(panel_content),
            # pizza2.animate.next_to(panel_box, UP, buff=0.1), # REMOVED: Static position (Feedback 6)
            run_time=2.0
        )
        self.wait(3.0)

        self.play(
            title.animate.shift(UP * 2).set_opacity(0),
            label.animate.shift(UP * 2).set_opacity(0),
            run_time=1.0
        )
        
        self.play(
            ShrinkToCenter(question),
            Uncreate(divider),
            run_time=1.0
        )
        
        self.play(
            goal_title.animate.scale(1.5).set_opacity(0),
            goal_note.animate.scale(1.5).set_opacity(0),
            run_time=1.0
        )

        self.play(
            Rotate(pizza, angle=2*PI),
            Rotate(pizza2, angle=-2*PI),
            panel.animate.scale(0.01).rotate(PI),
            run_time=1.5
        )
        
        self.play(
            FadeOut(pizza),
            FadeOut(pizza2),
            FadeOut(panel),
            run_time=0.5
        )
