from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *

class FinalScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"

        ## Section 1
        top_band = Rectangle(
            height=1.2,
            width=0.2,
            fill_color="#3FA9F5",
            fill_opacity=1,
            stroke_width=0
        ).to_corner(UL, buff=0)

        self.add(top_band)

        self.play(
            top_band.animate.stretch_to_fit_width(
                config.frame_width, about_edge=LEFT
            ),
            run_time=2.0
        )

        title = Text(
            "Meat Eaters Have Special Ways to Eat!",
            font="Bubblegum Sans",
            font_size=40,
            color="#FFFFFF"
        )
        title.set_z_index(3)
        title.move_to(top_band.get_top() + UP * 3.0)

        self.play(
            FadeIn(title),
            title.animate.move_to(top_band.get_center()),
            run_time=2.34,
            rate_func=rate_functions.ease_out_bounce
        )

        self.wait(1.5)

        ## Section 2
        category_band = RoundedRectangle(
            height=1.0, # Reduced height
            width=0.2,
            corner_radius=0.15,
            fill_color="#8B7CF6",
            fill_opacity=1,
            stroke_width=0
        ).next_to(top_band, DOWN, buff=0.2) # Reduced buff

        self.add(category_band)

        self.play(
            category_band.animate.stretch_to_fit_width(
                config.frame_width - 0.5
            ),
            run_time=2.5
        )

        category_title = Text(
            "Carnivores and Scavengers",
            font="Bubblegum Sans",
            font_size=28,
            color="#FFFFFF"
        )
        category_title.set_z_index(3)
        category_title.move_to(category_band.get_top() + DOWN * 0.25)

        self.play(
            FadeIn(category_title),
            run_time=1.0
        )

        category_desc = Text(
            "Animals that eat other animals or dead animals have amazing body parts",
            font="Bubblegum Sans", 
            font_size=18, # Reduced from 24
            color="#FFFFFF"
        )
        category_desc.set_z_index(3)
        category_desc.move_to(category_band.get_center() + DOWN * 0.15) # Centered in band

        self.play(
            AddTextLetterByLetter(category_desc),
            run_time=3.78
        )

        ## Section 3
        # 2x2 GRID positions assuming centerish (0, -1.5)
        # Cells need to be wider to accommodate text
        # Frame width ~14. Grid needs to fit in width 12ish.
        # Height ~5 available? Header ends at ~2.5 UP? (Top band 1.2, cat band 1.0 + buffs)
        # Let's say effective top is 1.5 UP. Bottom is 4.0 DOWN. Total height 5.5.
        
        # TL, TR, BL, BR
        grid_positions = [
            np.array([-3.2, -0.2, 0]),
            np.array([3.2, -0.2, 0]),
            np.array([-3.2, -3.0, 0]),
            np.array([3.2, -3.0, 0])
        ]

        grid_cells = []
        for pos in grid_positions:
            # Invisible anchors
            cell = RoundedRectangle(
                height=2.6,
                width=6.0,
                corner_radius=0.2,
                fill_color="#F9FAFC",
                fill_opacity=0, # Invisible
                stroke_color="#E0E0E0",
                stroke_width=0  # Invisible
            )
            cell.move_to(pos)
            grid_cells.append(cell)
            self.add(cell)

        cell_animations = []
        for cell in grid_cells:
            cell_animations.append(FadeIn(cell))

        self.play(
            LaggedStart(*cell_animations, lag_ratio=0.15),
            run_time=6.32 # Restored to original duration
        )

        # Helper to find VGroup indices for a substring in Text
        def get_indices(full_text_obj, substring):
            full_str = full_text_obj.original_text
            start_char_idx = full_str.find(substring)
            if start_char_idx == -1:
                return None, None
            end_char_idx = start_char_idx + len(substring)
            
            # Map string indices to VGroup indices (skipping spaces)
            vg_start = 0
            vg_end = 0
            
            # Count non-space chars before start
            for i in range(start_char_idx):
                if full_str[i] != " " and full_str[i] != "\n":
                     vg_start += 1
            
            # Count non-space chars in the substring
            count = 0
            for i in range(start_char_idx, end_char_idx):
                if full_str[i] != " " and full_str[i] != "\n":
                    count += 1
            
            vg_end = vg_start + count
            return vg_start, vg_end

        ## Section 4 - TIGER (TL)
        tiger_cell = grid_cells[0]
        tiger_img = ImageMobject("../images/aced_science_9.png").scale_to_fit_height(1.8) 
        # Move image to the LEFT side of the cell
        tiger_img.move_to(tiger_cell.get_left() + RIGHT * 0.8) # Moved LEFT (1.5 -> 0.8)

        self.play(GrowFromCenter(tiger_img), run_time=0.5)
        self.play(tiger_img.animate.scale(1.1), run_time=0.15)
        self.play(tiger_img.animate.scale(0.95), run_time=0.15)

        tiger_text = Text(
            "Tigers have sharp claws to hold\nprey and pointed teeth to tear meat",
            font="Bubblegum Sans", # Changed to match title
            font_size=18, 
            color="#000000",
            line_spacing=1.0
        )
        # Position Text to the RIGHT of the image
        tiger_text.next_to(tiger_img, RIGHT, buff=0.3) # Closer buff (0.5 -> 0.3)
        # tiger_text.scale_to_fit_width(3.0) # Ensure it fits if too wide?
        
        self.play(AddTextLetterByLetter(tiger_text), run_time=3.5) 
        
        self.wait(0.5) 

        # Inline Highlight: "sharp claws" 
        s1, e1 = get_indices(tiger_text, "sharp claws")
        if s1 is not None:
             self.play(
                 tiger_text[s1:e1].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.5
             )
             self.play(tiger_text[s1:e1].animate.scale(1/1.15), run_time=0.5)

        # Inline Highlight: "pointed teeth" 
        s2, e2 = get_indices(tiger_text, "pointed teeth")
        if s2 is not None:
             self.play(
                 tiger_text[s2:e2].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.3
             )
             self.play(tiger_text[s2:e2].animate.scale(1/1.15), run_time=0.2)


        ## Section 5 - HAWK (TR)
        hawk_cell = grid_cells[1]
        hawk_img = ImageMobject("../images/aced_science_10.png").scale_to_fit_height(1.8)
        hawk_img.move_to(hawk_cell.get_left() + RIGHT * 0.4) # Moved LEFT (1.5 -> 0.4) for right side

        self.play(GrowFromCenter(hawk_img), run_time=0.2)
        self.play(hawk_img.animate.scale(1.1), run_time=0.15)
        self.play(hawk_img.animate.scale(0.95), run_time=0.15)

        hawk_text = Text(
            "Hawks have hooked beaks to tear\nmeat and strong talons to catch prey",
            font="Bubblegum Sans", # Changed to match title
            font_size=18, 
            color="#000000",
             line_spacing=1.0
        )
        hawk_text.next_to(hawk_img, RIGHT, buff=0.3)

        self.play(AddTextLetterByLetter(hawk_text), run_time=2.0)
        
        self.wait(0.3) 

        # Inline Highlight: "hooked beaks" 
        s1, e1 = get_indices(hawk_text, "hooked beaks")
        if s1 is not None:
             self.play(
                 hawk_text[s1:e1].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.3
             )
             self.play(hawk_text[s1:e1].animate.scale(1/1.15), run_time=0.25)

        # Inline Highlight: "strong talons" 
        s2, e2 = get_indices(hawk_text, "strong talons")
        if s2 is not None:
             self.play(
                 hawk_text[s2:e2].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.3
             )
             self.play(hawk_text[s2:e2].animate.scale(1/1.15), run_time=0.25)
        
        self.wait(0.2) 


        # HYENA (BL)
        hyena_cell = grid_cells[2]
        hyena_img = ImageMobject("../images/aced_science_11.png").scale_to_fit_height(1.8)
        hyena_img.move_to(hyena_cell.get_left() + RIGHT * 0.8) # Moved LEFT (1.5 -> 0.8)

        self.play(GrowFromCenter(hyena_img), run_time=0.3)
        self.play(hyena_img.animate.scale(1.1), run_time=0.15)
        self.play(hyena_img.animate.scale(0.95), run_time=0.15)

        hyena_text = Text(
            "Hyenas have strong, broad\nteeth to crunch rotting meat",
            font="Bubblegum Sans", # Changed to match title
            font_size=18, 
            color="#000000",
            line_spacing=1.0
        )
        hyena_text.next_to(hyena_img, RIGHT, buff=0.3)

        self.play(AddTextLetterByLetter(hyena_text), run_time=2.0)
        
        self.wait(0.2) 

        # Inline Highlight: "strong, broad teeth" 
        s1, e1 = get_indices(hyena_text, "strong, broad")
        s2, e2 = get_indices(hyena_text, "teeth") 
        
        if s1 is not None and s2 is not None:
             self.play(
                 hyena_text[s1:e1].animate.set_color("#FFB703").scale(1.15),
                 hyena_text[s2:e2].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.3
             )
             self.play(
                  hyena_text[s1:e1].animate.scale(1/1.15), 
                  hyena_text[s2:e2].animate.scale(1/1.15),
                  run_time=0.25
             )
             
        self.wait(0.2) 


        # VULTURE (BR)
        vulture_cell = grid_cells[3]
        vulture_img = ImageMobject("../images/aced_science_12.png").scale_to_fit_height(1.8)
        vulture_img.move_to(vulture_cell.get_left() + RIGHT * 0.4) # Moved LEFT (1.5 -> 0.4)

        self.play(GrowFromCenter(vulture_img), run_time=0.3)
        self.play(vulture_img.animate.scale(1.1), run_time=0.15)
        self.play(vulture_img.animate.scale(0.95), run_time=0.15)

        vulture_text = Text(
            "Vultures have excellent eyesight and\na strong sense of smell to find dead animals",
            font="Bubblegum Sans", # Changed to match title
            font_size=18, 
            color="#000000",
            line_spacing=1.0
        )
        vulture_text.next_to(vulture_img, RIGHT, buff=0.3)
        vulture_text.scale_to_fit_width(4.5) # Adjusted width constraint

        self.play(AddTextLetterByLetter(vulture_text), run_time=2.0)
        
        self.wait(0.2) 

        # Inline Highlight: "excellent eyesight" 
        s1, e1 = get_indices(vulture_text, "excellent eyesight")
        if s1 is not None:
             self.play(
                 vulture_text[s1:e1].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.3
             )
             self.play(vulture_text[s1:e1].animate.scale(1/1.15), run_time=0.25)
        
        # Inline Highlight: "strong sense of smell"
        s2, e2 = get_indices(vulture_text, "strong sense of smell")
        if s2 is not None:
             self.play(
                 vulture_text[s2:e2].animate.set_color("#FFB703").scale(1.15),
                 run_time=0.1
             )
             self.play(vulture_text[s2:e2].animate.scale(1/1.15), run_time=0.1)


        ## Section 6
        self.wait(6.96) # Restored long final wait
