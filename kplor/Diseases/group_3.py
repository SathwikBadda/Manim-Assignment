from manim import *

import random

import numpy as np

from math import pi, sin, cos

class FinalScene(MovingCameraScene):
    def construct(self):
        # ==============================================================================
        # SETUP & CONFIGURATION
        # ==============================================================================
        self.camera.background_color = ManimColor("#031422")
        
        palette_colors = {
            "primary_shape": ManimColor("#3B447D"),
            "secondary_shape": ManimColor("#3774B4"),
            "primary_text": ManimColor("#61D262"),
            "secondary_text": ManimColor("#E1DBD5"),
        }
        
        BORDER_WIDTH = config.frame_width * 0.015
        FONT = "Baloo Bhai 2"
        TITLE_FONT_SIZE = 48
        YEAR_FONT_SIZE = 32
        HEADLINE_FONT_SIZE = 28
        DESC_FONT_SIZE = 24
        
        # ==============================================================================
        # SECTION 1: BORDERS AND TITLE
        # ==============================================================================
        ## Section 1
        
        left_border = Rectangle(
            width=BORDER_WIDTH,
            height=config.frame_height,
            stroke_width=0,
            fill_color=palette_colors["primary_shape"],
            fill_opacity=1
        ).move_to(LEFT * (config.frame_width / 2 - BORDER_WIDTH / 2))
        
        top_border = Rectangle(
            width=config.frame_width,
            height=BORDER_WIDTH,
            stroke_width=0,
            fill_color=palette_colors["secondary_shape"],
            fill_opacity=1
        ).move_to(UP * (config.frame_height / 2 - BORDER_WIDTH / 2))
        
        bottom_border = Rectangle(
            width=config.frame_width,
            height=BORDER_WIDTH,
            stroke_width=0,
            fill_color=palette_colors["primary_text"],
            fill_opacity=1
        ).move_to(DOWN * (config.frame_height / 2 - BORDER_WIDTH / 2))
        
        right_border = Rectangle(
            width=BORDER_WIDTH,
            height=config.frame_height,
            stroke_width=0,
            fill_color=palette_colors["secondary_text"],
            fill_opacity=1
        ).move_to(RIGHT * (config.frame_width / 2 - BORDER_WIDTH / 2))
        
        borders = VGroup(left_border, top_border, bottom_border, right_border)
        borders.set_z_index(20)
        
        title = Tex(
            "Impact of NCDs: Understanding the Shift",
            font_size=TITLE_FONT_SIZE,
            color=palette_colors["primary_text"]
        )
        title.to_corner(UL, buff=0.5).shift(DOWN * 0.3 + RIGHT * 0.3)
        
        self.play(Create(left_border), run_time=2.43)
        self.play(Create(top_border), run_time=2.43)
        self.play(Create(bottom_border), run_time=2.43)
        self.play(Create(right_border), run_time=1.48)
        self.play(Write(title), run_time=1.05)
        
        # ==============================================================================
        # SECTION 2: PATH DRAWING AND ROCKET MOVEMENT
        # ==============================================================================
        ## Section 2
        
        steps = 4
        START_Y = -config.frame_height * 0.25
        VERTICAL_RISE = config.frame_height * 0.18
        
        usable_width = config.frame_width - (2 * BORDER_WIDTH) - 1.0
        start_x = -config.frame_width / 2 + BORDER_WIDTH + 0.5
        
        arc_radius = VERTICAL_RISE / 2
        curve_width = 2 * arc_radius
        total_curve_effective_width = (steps - 1) * curve_width
        segment_length = (usable_width - total_curve_effective_width) / steps
        
        stroke_width = 8
        dot_radius = config.frame_height * 0.015
        img_radius = config.frame_height * 0.08
        
        current_pos = np.array([start_x, START_Y, 0])
        path_segments = []
        content_groups = []
        
        def get_rocket():
            body = Ellipse(width=0.6, height=0.25, color=GRAY, fill_opacity=1, fill_color=WHITE).set_stroke(BLACK, 2)
            fin_top = Polygon([-0.15, 0.08, 0], [-0.3, 0.2, 0], [-0.08, 0.08, 0], color=BLACK, fill_opacity=1, fill_color=RED)
            fin_bottom = Polygon([-0.15, -0.08, 0], [-0.3, -0.2, 0], [-0.08, -0.08, 0], color=BLACK, fill_opacity=1, fill_color=RED)
            window = Dot(color=BLUE).shift(RIGHT * 0.12).scale(0.6)
            flame = Polygon([-0.3, 0.04, 0], [-0.55, 0, 0], [-0.3, -0.04, 0], color=ORANGE, fill_opacity=1, fill_color=ORANGE)
            rocket = VGroup(flame, fin_top, fin_bottom, body, window)
            rocket.set_z_index(50)
            return rocket
        
        rocket = get_rocket()
        rocket.scale(config.frame_height * 0.12)
        
        colors_sequence = [
            palette_colors["primary_shape"],
            palette_colors["secondary_shape"],
            palette_colors["primary_shape"],
            palette_colors["secondary_shape"]
        ]
        
        for i in range(steps):
            col = colors_sequence[i]
            
            end_pos_line = current_pos + RIGHT * segment_length
            line = Line(current_pos, end_pos_line, color=col, stroke_width=stroke_width)
            line.set_stroke(opacity=1)
            path_segments.append(line)
            
            step_content = {
                "txt_main": None,
                "txt_desc": None,
                "dot": None,
                "line": line
            }
            content_groups.append(step_content)
            
            current_pos = end_pos_line
            
            if i < steps - 1:
                next_col = colors_sequence[i + 1]
                
                arc1 = Arc(
                    radius=arc_radius,
                    start_angle=-PI / 2,
                    angle=PI / 2,
                    arc_center=current_pos + UP * arc_radius,
                    stroke_width=stroke_width
                ).set_color_by_gradient(col, next_col)
                path_segments.append(arc1)
                
                joint_dot = Dot(
                    point=arc1.get_end(),
                    radius=dot_radius,
                    color=interpolate_color(col, next_col, 0.5),
                    stroke_color=WHITE,
                    stroke_width=3
                )
                joint_dot.set_z_index(10)
                content_groups[i]["dot"] = joint_dot
                
                arc2 = Arc(
                    radius=arc_radius,
                    start_angle=PI,
                    angle=-PI / 2,
                    arc_center=arc1.get_end() + RIGHT * arc_radius,
                    stroke_width=stroke_width
                ).set_color_by_gradient(col, next_col)
                path_segments.append(arc2)
                
                current_pos = arc2.get_end()
        
        rocket.move_to(path_segments[0].get_start())
        self.add(rocket)
        
        segment_animations = []
        for seg in path_segments:
            segment_animations.append(
                AnimationGroup(
                    Create(seg, rate_func=linear),
                    MoveAlongPath(rocket, seg, rate_func=linear),
                    run_time=1
                )
            )
        
        self.play(
            LaggedStart(*segment_animations, lag_ratio=0.5),
            run_time=7.39
        )
        
        # ==============================================================================
        # SECTION 3: MILESTONE PLACEHOLDERS AND TEXT BLOCKS
        # ==============================================================================
        ## Section 3
        
        TITLE_BOX_WIDTH = segment_length * 1.2
        
        def create_text_block(year_str, headline_str, desc_str, color, anchor_point):
            t_year = Tex(year_str, font_size=YEAR_FONT_SIZE, color=color)
            
            t_headline = Tex(
                headline_str,
                font_size=HEADLINE_FONT_SIZE,
                color=palette_colors["primary_text"],
                tex_template=TexTemplate()
            ).set_max_width(TITLE_BOX_WIDTH)
            
            t_desc = Tex(
                desc_str,
                font_size=DESC_FONT_SIZE,
                color=palette_colors["secondary_text"],
                tex_template=TexTemplate()
            ).set_max_width(TITLE_BOX_WIDTH)
            
            block_main = VGroup(t_year, t_headline).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            block_main.next_to(anchor_point, DOWN, buff=0.4, aligned_edge=LEFT)

            t_desc.next_to(block_main, DOWN, buff=0.15, aligned_edge=LEFT)
            
            return block_main, t_desc
        
        for i in range(steps):
            col = colors_sequence[i]
            line = content_groups[i]["line"]
            
            # Circles removed as per requirement
            pass
        
        milestone_data = [
            ("Historically", "Infectious Focus", "(e.g., Malaria)"),
            ("Recent Shift", "Lifestyle Changes", "(Processed Food, Less Activity)"),
            ("Result", "NCDs Become Common", "(Diabetes, Heart Disease, Cancer)"),
            ("Current Reality", "Leading Cause of Deaths", "(Shorter Lifespans)")
        ]
        
        for i, (year_label, headline, desc) in enumerate(milestone_data):
            line = content_groups[i]["line"]
            col = colors_sequence[i]
            
            txt_main, txt_desc = create_text_block(year_label, headline, desc, col, line)
            content_groups[i]["txt_main"] = txt_main
            content_groups[i]["txt_desc"] = txt_desc
        
        content_animations = []
        for i, item in enumerate(content_groups):
            step_anims = []
            if item["txt_main"]:
                step_anims.append(Write(item["txt_main"]))
            if item["dot"]:
                step_anims.append(GrowFromCenter(item["dot"]))
            
            content_animations.append(
                AnimationGroup(*step_anims, run_time=1.2)
            )
        
        self.play(
            LaggedStart(*content_animations, lag_ratio=0.6),
            run_time=10.42
        )
        
        # ==============================================================================
        # SECTION 4: IMAGE ASSETS REVEAL
        # ==============================================================================
        ## Section 4
        
        image_assets = [
            "../images/ace_disease_4.png",
            "../images/ace_disease_5.png",
            "../images/ace_disease_6.png",
            "../images/ace_disease_7.png"
        ]
        
        image_anims = []
        for i, img_path in enumerate(image_assets):
            line = content_groups[i]["line"]
            col = colors_sequence[i]
            
            # Position image where circles used to be (above line)
            img = ImageMobject(img_path)
            # Scale image shorter than diameter (0.16) to fit inside (though circles are gone, keeping size consistent)
            img.height = config.frame_height * 0.18
            # Center of line + UP offset
            img.move_to(line.get_center() + UP * 1.0)
            
            img.set_z_index(25)
            
            self.add(img)
            content_groups[i]["img_asset"] = img
            
            image_anims.append(
                AnimationGroup(
                    GrowFromCenter(img),
                    Write(content_groups[i]["txt_desc"])
                )
            )
        
        self.play(
            LaggedStart(*image_anims, lag_ratio=0.4),
            run_time=16.85
        )
        
        # ==============================================================================
        # SECTION 5: EXIT SEQUENCE - CONTENT REMOVAL AND REVERSE TRAVERSAL
        # ==============================================================================
        ## Section 5
        
        all_exit_anims = []
        for item in content_groups:
            if item["txt_main"]:
                all_exit_anims.append(
                    item["txt_main"].animate.shift(DOWN * 0.3).set_opacity(0)
                )
            if item["txt_desc"]:
                all_exit_anims.append(
                    item["txt_desc"].animate.shift(DOWN * 0.3).set_opacity(0)
                )
            if item["dot"]:
                all_exit_anims.append(
                    item["dot"].animate.scale(0.1).set_opacity(0)
                )
            if "img_asset" in item and item["img_asset"]:
                all_exit_anims.append(
                    item["img_asset"].animate.shift(UP * 0.5).set_opacity(0)
                )
        
        self.play(*all_exit_anims, run_time=2.0)
        
        self.play(
            Rotate(rocket, PI),
            run_time=0.8
        )
        
        reversed_segments = path_segments[::-1]
        reverse_animations = []
        
        for seg in reversed_segments:
            reverse_animations.append(
                AnimationGroup(
                    Uncreate(seg, rate_func=linear),
                    MoveAlongPath(rocket, seg, rate_func=lambda t: 1 - t),
                    run_time=1
                )
            )
        
        self.play(
            LaggedStart(*reverse_animations, lag_ratio=0.5),
            run_time=5.39
        )
        
        # ==============================================================================
        # SECTION 6: FINAL CLEAN EXIT
        # ==============================================================================
        ## Section 6
        
        self.play(
            rocket.animate.scale(0.3).set_opacity(0).shift(LEFT * 0.5),
            title.animate.shift(UP * 0.5).set_opacity(0),
            borders.animate.set_opacity(0),
            run_time=8.43
        )
        
        self.wait(0.1)
