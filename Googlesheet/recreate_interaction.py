from manim import *
import numpy as np

def ease_out_quint(t: float) -> float:
    return 1 - (1 - t) ** 5

def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3

def build_pointer() -> VGroup:
    verts = [
        [0.00,  0.00, 0],  # Tip
        [0.00, -1.05, 0],  # Left straight edge
        [0.26, -0.78, 0],  # inner indent
        [0.48, -1.15, 0],  # right leg tip
        [0.64, -1.05, 0],  # right leg outer
        [0.42, -0.68, 0],  # right indent
        [0.72, -0.68, 0],  # rightmost point
    ]
    body = Polygon(*verts, fill_color="#18181A", fill_opacity=1, stroke_color="#FFFFFF", stroke_width=3.5)
    body.scale(0.5)
    shadow = Polygon(*verts, fill_color="#000000", fill_opacity=0.25, stroke_width=0)
    shadow.scale(0.5)
    shadow.shift(DOWN * 0.05 + RIGHT * 0.05)
    return VGroup(shadow, body)

def build_card(label_title, p_width=7.5, p_height=2.8, content_text="", is_dropdown=False) -> VGroup:
    card_outline_glow = RoundedRectangle(
        corner_radius=0.3, width=p_width + 0.08, height=p_height + 0.08, fill_opacity=0, stroke_width=3.0
    )
    card_bg = RoundedRectangle(
        corner_radius=0.3, width=p_width, height=p_height, fill_color="#F8F9FA", fill_opacity=1,
        stroke_color="#E2E8F0", stroke_width=1.5
    )
    lbl = Text(label_title, font="Helvetica", font_size=20, color="#111827", weight=BOLD)
    lbl.move_to(card_bg.get_top() + DOWN * 0.5).align_to(card_bg.get_left() + RIGHT * 0.4, LEFT)
    
    input_box = RoundedRectangle(
        corner_radius=0.2, width=p_width - 0.7, height=p_height - 1.4, fill_color="#FFFFFF",
        fill_opacity=1, stroke_color="#E2E8F0", stroke_width=1.0
    )
    input_box.next_to(lbl, DOWN, buff=0.3).align_to(lbl, LEFT)
    
    group_elements = [card_outline_glow, card_bg, lbl, input_box]
    vgroup = VGroup(*group_elements)
    
    if content_text:
        if isinstance(content_text, str):
            content_text = [content_text]
        content_lbl = Paragraph(*content_text, font="Helvetica", font_size=16, color="#374151", line_spacing=0.8, alignment="left")
        content_lbl.move_to(input_box.get_top() + DOWN * 0.35).align_to(input_box.get_left() + RIGHT * 0.25, LEFT)
        for letter in content_lbl.family_members_with_points():
            letter.set_opacity(0)
        vgroup.add(content_lbl)
        vgroup.content_lbl = content_lbl
        vgroup.is_typed = False
        
    if is_dropdown:
        chevron = VGroup(
            Line([-0.1, 0.05, 0], [0, -0.05, 0]), Line([0, -0.05, 0], [0.1, 0.05, 0])
        )
        chevron.set_stroke(color="#6B7280", width=2)
        chevron.move_to(input_box.get_right() + LEFT * 0.4)
        chevron_up = VGroup(
            Line([-0.1, -0.05, 0], [0, 0.05, 0]), Line([0, 0.05, 0], [0.1, -0.05, 0])
        )
        chevron_up.set_stroke(color="#6B7280", width=2)
        chevron_up.next_to(chevron, UP, buff=0.1)
        vgroup.add(chevron, chevron_up)
    
    vgroup.glow = card_outline_glow
    vgroup.bg = card_bg
    vgroup.input_box = input_box
    return vgroup

def build_dropdown_menu(options, width, parent_box):
    h = len(options) * 0.5 + 0.3
    bg = RoundedRectangle(
        corner_radius=0.15, width=width, height=h, fill_color="#FFFFFF", fill_opacity=1,
        stroke_color="#E2E8F0", stroke_width=1.0
    )
    bg.next_to(parent_box, DOWN, buff=0.1)
    
    texts = VGroup()
    for i, opt in enumerate(options):
        lbl = Text(opt, font="Helvetica", font_size=16, color="#4B5563")
        lbl.move_to(bg.get_top() + DOWN * (0.4 + i * 0.5)).align_to(bg.get_left() + RIGHT * 0.3, LEFT)
        texts.add(lbl)
                
    menu = VGroup(bg, texts)
    menu.set_z_index(30)
    menu.set_opacity(0)
    return menu, texts

class UIInteraction(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"
        
        sys_prompt_text = (
            "You are a sophisticated yet practical weekend planning assistant.",
            "You suggest activities, restaurants, and entertainment based on",
            "their interests, budget, and schedule. Your suggestions always include..."
        )
        first_msg_text = ("Hey, welcome to QuickCrate. How can I help you today?",)
        
        # ── UI Construction ────────────────────────────────────────────────────
        card1 = build_card("System Prompt", 8.8, 3.2, sys_prompt_text)
        card1.move_to(RIGHT * 2 + UP * 2.5)
        
        card2 = build_card("First Message", 8.8, 2.8, first_msg_text)
        card2.next_to(card1, DOWN, buff=0.45)
        
        card_llm = build_card("LLM", 4.0, 2.5, "Claude 3.5 Sonnet", is_dropdown=True)
        card_llm.next_to(card2, DOWN, buff=0.45).align_to(card2, LEFT)
        
        card_voice = build_card("Voice", 4.0, 2.5, "Default Voice", is_dropdown=True)
        card_voice.next_to(card_llm, RIGHT, buff=0.8)
        
        build_test_text = Paragraph(
            "Build,", "test,", "and", "deploy.",
            font="Helvetica", font_size=60, color="#000000", weight=BOLD, line_spacing=0.8, alignment="left"
        )
        build_test_text.move_to(LEFT * 4.5 + DOWN * 0.2)
        
        ui_layer = VGroup(card1, card2, card_llm, card_voice, build_test_text)
        # Entrance animation later instead of self.add(ui_layer)
        
        gradient_colors = ["#4D70FF", "#35E9E8", "#C43DD4"]
        
        # Dropdowns mapping
        llm_menu, llm_opts = build_dropdown_menu(["claude 3 sonnet", "claude 4 sonnet", "claude 4.5 sonnet"], 4.0, card_llm.input_box)
        voice_menu, voice_opts = build_dropdown_menu(["Raju - Hindi", "Sarah - English", "Jason - Deep", "Guru - Rich"], 4.0, card_voice.input_box)
        self.add(llm_menu, voice_menu)
        
        # Pointer setup
        pointer = build_pointer()
        START_POS = card1.get_center() + DOWN * 0.4 + RIGHT * 0.5
        pointer.move_to(START_POS)
        pointer.set_z_index(50)
        
        self.camera.frame.move_to(UP * 1.5)
        
        # Entrance animation
        # Build text swoops in from the left line by line
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 2) for line in build_test_text],
                lag_ratio=0.2
            ),
            run_time=1.0, rate_func=ease_out_cubic
        )
        
        # Cards swoop in staggeringly from the right
        self.play(
            LaggedStart(
                *[FadeIn(card, shift=LEFT * 2) for card in [card1, card2, card_llm, card_voice]],
                lag_ratio=0.15
            ),
            run_time=1.2, rate_func=ease_out_cubic
        )
        self.play(FadeIn(pointer, shift=DOWN * 0.5), run_time=0.4)
        
        def click_card(card, pntr, show_text=True):
            self.play(pntr.animate.scale(0.85), card.animate.scale(0.98), run_time=0.12, rate_func=ease_out_quint)
            card.glow.set_color(color=[*gradient_colors])
            self.play(
                pntr.animate.scale(1/0.85), card.animate.scale(1.04 / 0.98),
                card.glow.animate.set_opacity(1), card.bg.animate.set_stroke(color="#FFFFFF", width=0.1),
                run_time=0.25, rate_func=ease_out_cubic
            )
            # Fast text typing after clicking
            if show_text and hasattr(card, "content_lbl") and hasattr(card, "is_typed") and not card.is_typed:
                letters = card.content_lbl.family_members_with_points()
                if letters:
                    self.play(
                        LaggedStart(
                            *[letter.animate.set_opacity(1) for letter in letters],
                            lag_ratio=0.03
                        ),
                        run_time=min(1.5, len(letters) * 0.03)
                    )
                card.is_typed = True
                
        def select_dropdown_option(menu, opts, opt_index, target_card, target_str):
            # Fade in menu
            self.play(menu.animate.set_opacity(1), run_time=0.2)
            # Move pointer to option
            opt_pos = opts[opt_index].get_left() + RIGHT * 0.5 + DOWN * 0.1
            self.play(pointer.animate.move_to(opt_pos), run_time=0.35, rate_func=smooth)
            # Click option
            self.play(pointer.animate.scale(0.85), run_time=0.1)
            self.play(pointer.animate.scale(1/0.85), run_time=0.15)
            # Fade out menu
            self.play(menu.animate.set_opacity(0), run_time=0.25)
            # Update target card text letter by letter
            if hasattr(target_card, "content_lbl"):
                new_lbl = Paragraph(target_str, font="Helvetica", font_size=16, color="#374151", line_spacing=0.8, alignment="left")
                new_lbl.move_to(target_card.input_box.get_top() + DOWN * 0.35).align_to(target_card.input_box.get_left() + RIGHT * 0.25, LEFT)
                for letter in new_lbl.family_members_with_points():
                    letter.set_opacity(0)
                
                target_card.remove(target_card.content_lbl)
                self.remove(target_card.content_lbl)
                target_card.add(new_lbl)
                target_card.content_lbl = new_lbl
                target_card.is_typed = False
                
                letters = target_card.content_lbl.family_members_with_points()
                if letters:
                    self.play(
                        LaggedStart(
                            *[letter.animate.set_opacity(1) for letter in letters],
                            lag_ratio=0.03
                        ),
                        run_time=min(1.0, len(letters) * 0.03)
                    )
                target_card.is_typed = True

        self.wait(0.2)
        click_card(card1, pointer)
        self.wait(0.2)
        
        # Faster transition to Card 2, preserving glow
        self.play(
            pointer.animate.move_to(card2.get_center() + DOWN * 0.0 + RIGHT * 1.5),
            self.camera.frame.animate.shift(DOWN * 1.5),
            card1.animate.scale(1/1.04),
            run_time=0.45, rate_func=smooth
        )
        click_card(card2, pointer)
        self.wait(0.2)
        
        # Scroll camera down to reveal LLM and Voice cards and dropdown menus natively before moving pointer mapping
        self.play(
            self.camera.frame.animate.shift(DOWN * 2.7),
            card2.animate.scale(1/1.04),
            run_time=0.6, rate_func=smooth
        )
        
        # Faster transition to LLM (card 3), preserving glow
        self.play(
            pointer.animate.move_to(card_llm.get_center() + DOWN * 0.1 + RIGHT * 0.5),
            run_time=0.45, rate_func=smooth
        )
        click_card(card_llm, pointer, show_text=False)
        select_dropdown_option(llm_menu, llm_opts, 1, card_llm, "claude 4 sonnet")
        self.wait(0.2)
        
        # Transition to Voice (card 4), preserving glow
        self.play(
            pointer.animate.move_to(card_voice.get_center() + DOWN * 0.1 + RIGHT * 0.5),
            card_llm.animate.scale(1/1.04),
            run_time=0.45, rate_func=smooth
        )
        click_card(card_voice, pointer, show_text=False)
        select_dropdown_option(voice_menu, voice_opts, 2, card_voice, "Jason - Deep")
        self.wait(0.4)

        # Move pointer away at the end
        self.play(
            pointer.animate.shift(DOWN * 2 + RIGHT * 2),
            card_voice.animate.scale(1/1.04),
            run_time=0.6, rate_func=rate_functions.ease_in_cubic
        )
        self.wait(0.5)
        
        # Exit animation
        self.play(FadeOut(pointer, shift=DOWN * 0.5), run_time=0.3)
        self.play(
            LaggedStart(
                *[FadeOut(card, shift=RIGHT * 2) for card in [card_voice, card_llm, card2, card1]],
                lag_ratio=0.15
            ),
            run_time=1.2, rate_func=rate_functions.ease_in_cubic
        )
        self.play(
            LaggedStart(
                *[FadeOut(line, shift=LEFT * 2) for line in reversed(build_test_text)],
                lag_ratio=0.2
            ),
            run_time=0.8, rate_func=rate_functions.ease_in_cubic
        )
        self.wait(0.5)

if __name__ == "__main__":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_rate = 60
    scene = UIInteraction()
    scene.render()
