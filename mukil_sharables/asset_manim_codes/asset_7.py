from manim import *
import numpy as np


class DecisionSignPost(VGroup):
    def __init__(
        self,
        labels=None,
        pole_height=5,
        pole_width=0.15,
        board_width=3.5,
        board_height=0.6,
        board_spacing=0.8,
        board_colors=None,
        font="Georgia",
        font_size=24,
        text_color=WHITE,
        stroke_color=WHITE,
        stroke_width=2,
        depth_offset=0.05,  # gives subtle 2.5D stacking feel
        **kwargs
    ):
        super().__init__(**kwargs)

        if labels is None:
            labels = [
                "Engineering",
                "Medical",
                "Design",
                "Commerce",
                "Study Abroad",
                "Startup"
            ]

        if board_colors is None:
            board_colors = [BLUE_E, GREEN_E, TEAL_E, ORANGE, PURPLE, MAROON]

        # --------------------------------------------------
        # Vertical Pole
        # --------------------------------------------------
        pole = Rectangle(
            width=pole_width,
            height=pole_height,
            fill_color=stroke_color,
            fill_opacity=1,
            stroke_width=0
        )

        pole.move_to(ORIGIN)

        # --------------------------------------------------
        # Create Sign Boards
        # --------------------------------------------------
        boards = VGroup()
        texts = VGroup()

        start_y = pole_height / 2 - 0.8

        for i, (label, color) in enumerate(zip(labels, board_colors)):
            direction = "right" if i % 2 == 0 else "left"

            y_pos = start_y - i * board_spacing

            # Main rectangular board
            board = Rectangle(
                width=board_width,
                height=board_height,
                fill_color=color,
                fill_opacity=1,
                stroke_color=stroke_color,
                stroke_width=stroke_width
            )

            # Arrow tip
            arrow_tip = Polygon(
                [0, 0, 0],
                [0.4, board_height / 2, 0],
                [0.4, -board_height / 2, 0],
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            )

            arrow_tip.next_to(board, RIGHT, buff=0)

            # Combine rectangle + arrow
            full_board = VGroup(board, arrow_tip)

            if direction == "left":
                full_board.flip(LEFT)

            # Position relative to pole
            if direction=="left":
                full_board.next_to(pole, LEFT, buff=0)
            else:
                full_board.next_to(pole, RIGHT, buff=0)


            full_board.shift(UP * (y_pos - pole_height / 2))

            # Add subtle Z offset for 2.5D stacking
            full_board.shift(OUT * i * depth_offset)

            # Text
            text = Text(
                label,
                font=font,
                font_size=font_size,
                color=text_color
            )
            text.move_to(board.get_center())
            text.shift(OUT * i * depth_offset)

            boards.add(full_board)
            texts.add(text)

        # --------------------------------------------------
        # Add To Group
        # --------------------------------------------------
        self.add(pole, boards, texts)

        # Store references for later animation
        self.pole = pole
        self.boards = boards
        self.texts = texts