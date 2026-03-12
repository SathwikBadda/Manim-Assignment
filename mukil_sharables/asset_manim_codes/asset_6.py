from manim import *
import numpy as np

class SWOTMatrix(VGroup):
    def __init__(
        self,
        width=6,
        height=6,
        stroke_color=WHITE,
        stroke_width=2,
        label_font="Georgia",
        label_font_size=28,
        label_color=WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)

        # --------------------------------------------------
        # Outer Boundary
        # --------------------------------------------------
        outer_rect = Rectangle(
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )

        # --------------------------------------------------
        # Divider Lines
        # --------------------------------------------------
        vertical_divider = Line(
            outer_rect.get_top(),
            outer_rect.get_bottom(),
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )

        horizontal_divider = Line(
            outer_rect.get_left(),
            outer_rect.get_right(),
            stroke_color=stroke_color,
            stroke_width=stroke_width
        )

        # --------------------------------------------------
        # Quadrant Labels
        # --------------------------------------------------
        strengths = Text(
            "Strengths",
            font=label_font,
            font_size=label_font_size,
            color=label_color
        )

        weaknesses = Text(
            "Weaknesses",
            font=label_font,
            font_size=label_font_size,
            color=label_color
        )

        opportunities = Text(
            "Opportunities",
            font=label_font,
            font_size=label_font_size,
            color=label_color
        )

        threats = Text(
            "Threats",
            font=label_font,
            font_size=label_font_size,
            color=label_color
        )

        # Position labels inside quadrants
        strengths.move_to(
            np.array([-width/4, height/4, 0])
        )

        weaknesses.move_to(
            np.array([width/4, height/4, 0])
        )

        opportunities.move_to(
            np.array([-width/4, -height/4, 0])
        )

        threats.move_to(
            np.array([width/4, -height/4, 0])
        )

        # --------------------------------------------------
        # Add Everything To VGroup
        # --------------------------------------------------
        self.add(
            outer_rect,
            vertical_divider,
            horizontal_divider,
            strengths,
            weaknesses,
            opportunities,
            threats
        )

        # Store references if needed externally
        self.outer_rect = outer_rect
        self.vertical_divider = vertical_divider
        self.horizontal_divider = horizontal_divider
        self.strengths_label = strengths
        self.weaknesses_label = weaknesses
        self.opportunities_label = opportunities
        self.threats_label = threats