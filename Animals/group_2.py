from manim import *

import random

import numpy as np

from math import pi, sin, cos

from manim import *
import numpy as np

class FinalScene(MovingCameraScene):
    def construct(self):
        # ==========================================
        # GLOBAL CONFIGURATION
        # ==========================================
        self.camera.background_color = "#F9FAFC"
        
        # --- STATIC HEADER ---
        header_rect = Rectangle(width=config.frame_width, height=1.2, color="#3FA9F5", fill_opacity=1, stroke_width=0)
        header_rect.to_edge(UP, buff=0)
        
        # --- STATIC FOOTER (Notebook Binding) ---
        footer_colors = ["#FFB703", "#3FA9F5", "#FFB703", "#3FA9F5", "#FFB703", "#3FA9F5"]
        footer_group = VGroup()
        num_circles = int(config.frame_width / 0.4) + 2
        
        for i in range(num_circles):
            c = Circle(radius=0.18, color=WHITE, fill_color=footer_colors[i % len(footer_colors)], fill_opacity=1, stroke_width=4)
            hole = Circle(radius=0.06, color=WHITE, fill_color="#F9FAFC", fill_opacity=1, stroke_width=0)
            footer_group.add(VGroup(c, hole))
        
        footer_group.arrange(RIGHT, buff=0.1)
        footer_group.to_edge(DOWN, buff=0.2)
        
        self.add(header_rect, footer_group)

        # ==========================================
        # SECTION 1: DYNAMIC TITLE
        # ==========================================
        # ==========================================
        # SECTION 1: TITLE BLOCKS AND SUBTITLE
        # ==========================================
        ## Section 1
        
        # 1. Bouncing Title (Split into 2 lines)
        line1_text = "Herbivores"
        line2_text = "and Their Tools!"
        
        title_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, RED, ORANGE]
        color_idx = 0
        
        def create_block(char, color):
            block = RoundedRectangle(corner_radius=0.2, width=0.8, height=0.8, color=BLACK, stroke_width=3, fill_color=color, fill_opacity=1)
            letter = Text(char, font="Comic Sans MS", weight=BOLD, color=WHITE, font_size=48).set_stroke(BLACK, 1)
            return VGroup(block, letter)

        # Line 1
        line1_group = VGroup()
        for char in line1_text:
            color = title_colors[color_idx % len(title_colors)]
            line1_group.add(create_block(char, color))
            color_idx += 1
        line1_group.arrange(RIGHT, buff=0.1)
        
        # Line 2
        line2_group = VGroup()
        for char in line2_text:
            if char == " ": # Space
                line2_group.add(VGroup(Rectangle(width=0.8, height=0.8, fill_opacity=0, stroke_width=0))) # Empty space placeholder
                continue
            color = title_colors[color_idx % len(title_colors)]
            line2_group.add(create_block(char, color))
            color_idx += 1
        line2_group.arrange(RIGHT, buff=0.1)
        
        # Combine Lines
        title_group = VGroup(line1_group, line2_group).arrange(DOWN, buff=0.2)
        title_group.move_to(ORIGIN).shift(UP*0.5)

        # Subtitle
        subtitle = Text("Body parts for eating plants", font="Comic Sans MS", weight=BOLD, font_size=28, color="#444B55")
        subtitle.set_stroke(color=BLACK, width=0)
        subtitle.next_to(title_group, DOWN, buff=0.4)
        
        # Animate Title (Lagged Bounce)
        final_positions = []
        for line in title_group:
            for m in line:
                final_positions.append(m.get_center())
                m.shift(UP * 7) # Move up for entrance
            
        all_blocks = [m for line in title_group for m in line]
        
        title_anims = [m.animate(rate_func=rate_functions.ease_out_bounce, run_time=1.5).move_to(final_positions[i]) for i, m in enumerate(all_blocks)]
        
        self.play(
            LaggedStart(*title_anims, lag_ratio=0.05),
            run_time=3.0
        )
        
        # Subtitle appears AFTER Title
        self.play(FadeIn(subtitle, shift=UP), run_time=1.0)
        
        self.wait(1.0)
        
        # Exit Title & Subtitle Together
        self.play(
            FadeOut(title_group, shift=UP),
            FadeOut(subtitle, shift=UP),
            run_time=1.0
        )

        # ==========================================
        # SECTION 2: RULE CARD (Center -> Top)
        # ==========================================
        ## Section 2
        
        # Increase Rule Box Size: 12 x 4.0
        rule_box = RoundedRectangle(corner_radius=0.3, width=12, height=4.0, color="#3FA9F5", stroke_width=0, fill_color="#3FA9F5", fill_opacity=1)
        rule_box.move_to(ORIGIN)
        
        # Increase Badge Size
        badge_star = Star(n=5, outer_radius=0.7, inner_radius=0.4, color="#FFB703", fill_opacity=1, stroke_color="#FFB703", stroke_width=2)
        badge_text = Text("RULE", font="Comic Sans MS", weight=BOLD, font_size=28, color=WHITE).set_stroke(BLACK, 1)
        badge_group = VGroup(badge_star, badge_text).move_to(rule_box.get_corner(UR) + DOWN*0.6 + LEFT*0.6)
        
        # Increase Content Font Size
        rule_content = Text("Herbivores have special body parts that help them eat plants easily!", font="Comic Sans MS", color="#444B55", font_size=42)
        rule_content.move_to(rule_box.get_center())
        rule_content.scale_to_fit_width(rule_box.width - 2.0)
        
        rule_group = VGroup(rule_box, rule_content, badge_group)
        rule_group.set_z_index(5) # Ensure it's above everything
        
        # Appear in Center
        self.play(GrowFromCenter(rule_box, rate_func=rate_functions.ease_out_back), run_time=1.5)
        self.play(
            FadeIn(rule_content), 
            GrowFromCenter(badge_group),
            run_time=1.0
        )
        self.wait(1.0)
        
        # Move to Top Border ("Settle") - Absolute Top
        # Shrink slightly to act as a header/banner
        # Make the box itself INVISIBLE so only text/star remain on the static header
        target_rule_box = RoundedRectangle(corner_radius=0.3, width=13, height=1.5, color="#3FA9F5", stroke_width=0, fill_color="#3FA9F5", fill_opacity=0)
        target_rule_box.to_edge(UP, buff=0) # Absolute top to cover header
        
        target_content = rule_content.copy().scale(0.85).move_to(target_rule_box.get_center()) # Slightly smaller for header
        target_badge = badge_group.copy().scale(0.6).move_to(target_rule_box.get_corner(UR) + DOWN*0.35 + LEFT*0.4) # Moved DOWN and LEFT to avoid border overlap
        
        self.play(
             Transform(rule_box, target_rule_box),
             Transform(rule_content, target_content),
             Transform(badge_group, target_badge),
             run_time=1.5
        )
        
        # ==========================================
        # SECTION 3: SEQUENTIAL CARDS & HIGHLIGHTS
        # ==========================================
        ## Section 3
        
        # Function to create card components (NOT Group) for manual animation
        def get_card_components(image_path, main_text, highlight_text, bg_color):
            # Card Background (Keep size same, content changes)
            card_bg = RoundedRectangle(corner_radius=0.25, width=3.5, height=5.0, color=BLACK, stroke_width=2, fill_color=bg_color, fill_opacity=1)
            
            # Components for animation
            try:
                img = ImageMobject(image_path)
                img.scale_to_fit_height(2.8) 
                # Final position - Moved UP slightly to fit text below
                img_target_pos = card_bg.get_center() + UP * 1.0 
                img.move_to(img_target_pos)
            except:
                img = Circle(color=WHITE) 
                
            # Main Text - DOUBLED Font Size (approx)
            # reduced line spacing slightly to fit
            text_obj = Text(main_text, font="Comic Sans MS", color="#444B55", font_size=32, line_spacing=0.7)
            text_obj.scale_to_fit_width(card_bg.width - 0.2) # Uses almost full width
            text_obj.move_to(card_bg.get_center() + DOWN * 0.7) # Moved UP (was 1.3)
            
            # Highlight Text (Hidden initially) - Reduced from 36 to 28 for better fit
            # Ensure text is CENTER aligned for multi-line support
            highlight_obj = Text(highlight_text, font="Comic Sans MS", color="#FFB703", font_size=28, weight=BOLD, line_spacing=0.8) # 36 -> 28
            # Use scale_to_fit_width but with a check to avoid over-shrinking if already wrapped
            if highlight_obj.width > (card_bg.width - 0.4):
                highlight_obj.scale_to_fit_width(card_bg.width - 0.4)
            
            highlight_obj.next_to(text_obj, DOWN, buff=0.15)
            # Safety check to keep inside card - Enforce bottom margin
            if highlight_obj.get_bottom()[1] < card_bg.get_bottom()[1] + 0.2:
                 highlight_obj.move_to(card_bg.get_bottom() + UP * 0.4)
            
            return card_bg, img, text_obj, highlight_obj

        # 1. COW SEQUENCE
        cow_bg, cow_img, cow_text, cow_hl = get_card_components(
            "../images/aced_science_6.png", 
            "Cows have sharp front teeth for biting\nand strong back teeth for grinding grass.",
            "sharp front\nback teeth", # Split into 2 lines for consistent size
            "#DFDBE6"
        )
        # Position Cow Card (Left)
        cow_group = Group(cow_bg, cow_img, cow_text, cow_hl) # Group for positioning
        cow_group.move_to(LEFT * 4.0 + DOWN * 0.5)
        
        # Cow Animation
        self.play(FadeIn(cow_bg, shift=UP), run_time=0.5)
        start_point = cow_bg.get_corner(UL)
        self.play(GrowFromPoint(cow_img, start_point, rate_func=rate_functions.ease_out_bounce), run_time=1.0)
        self.play(AddTextLetterByLetter(cow_text), run_time=2.0)
        
        # Cow Highlight (Immediately after)
        self.play(cow_hl.animate.scale(1.1).set_color("#FFD700"), run_time=1.0)
        self.play(cow_hl.animate.scale(1/1.1).set_color("#FFB703"), run_time=0.5)
        self.wait(0.5)
        
        # 2. ELEPHANT SEQUENCE
        ele_bg, ele_img, ele_text, ele_hl = get_card_components(
            "../images/aced_science_7.png",
            "Elephants use their long trunks to\npull out leaves and grass.",
            "long trunks",
            "#FBEDDA"
        )
        # Position Elephant Card (Center)
        ele_group = Group(ele_bg, ele_img, ele_text, ele_hl)
        ele_group.move_to(DOWN * 0.5) # Center
        
        # Elephant Animation
        self.play(FadeIn(ele_bg, shift=UP), run_time=0.5)
        start_point = ele_bg.get_corner(UL)
        self.play(GrowFromPoint(ele_img, start_point, rate_func=rate_functions.ease_out_bounce), run_time=1.0)
        self.play(AddTextLetterByLetter(ele_text), run_time=2.0)
        
        # Elephant Highlight (Immediately after)
        self.play(ele_hl.animate.scale(1.1).set_color("#FFD700"), run_time=1.0)
        self.play(ele_hl.animate.scale(1/1.1).set_color("#FFB703"), run_time=0.5)
        self.wait(0.5)
        
        # 3. GIRAFFE SEQUENCE
        gir_bg, gir_img, gir_text, gir_hl = get_card_components(
            "../images/aced_science_8.png",
            "Giraffes use their long necks to\nreach leaves on tall trees.",
            "long necks",
            "#DFDBE6"
        )
        # Position Giraffe Card (Right)
        gir_group = Group(gir_bg, gir_img, gir_text, gir_hl)
        gir_group.move_to(RIGHT * 4.0 + DOWN * 0.5)
        
        # Giraffe Animation
        self.play(FadeIn(gir_bg, shift=UP), run_time=0.5)
        start_point = gir_bg.get_corner(UL)
        self.play(GrowFromPoint(gir_img, start_point, rate_func=rate_functions.ease_out_bounce), run_time=1.0)
        self.play(AddTextLetterByLetter(gir_text), run_time=2.0)
        
        # Giraffe Highlight (Immediately after)
        self.play(gir_hl.animate.scale(1.1).set_color("#FFD700"), run_time=1.0)
        self.play(gir_hl.animate.scale(1/1.1).set_color("#FFB703"), run_time=0.5)
        self.wait(0.5)
        
        # ==========================================
        # SECTION 4: FINAL STATE
        # ==========================================
        ## Section 4
        
        self.wait(1.0)

        # ==========================================
        # SECTION 4: EXIT ANIMATIONS
        # ==========================================
        
        # 1. Simultaneous Card Exit
        self.play(
            cow_group.animate.shift(LEFT * 12),
            ele_group.animate.shift(DOWN * 10),
            gir_group.animate.shift(RIGHT * 12),
            run_time=1.5
        )

        # 4. Header Exit (Text, Star, RuleBox, and Blue Rect)
        # Use the objects that are currently on screen (rule_box, rule_content, badge_group have been Transformed)
        header_exit_group = Group(header_rect, rule_box, rule_content, badge_group)
        self.play(header_exit_group.animate.shift(UP * 5), run_time=1.5)
        
        self.wait(1.0)
