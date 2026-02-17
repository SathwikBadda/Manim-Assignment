from manim import *
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30
config.background_color = "#FFFFFF"

class YearScroll(Scene):
    def create_gradient_fade_text(self, text, font_size, color, fade_direction="top"):
        base = Text(text, font_size=font_size, weight=BOLD).set_color(color)
        
        mask_height = base.height / 2
        
        if fade_direction == "top":
            fade_rect = Rectangle(
                width=base.width + 0.5,
                height=mask_height,
                fill_opacity=0.85,
                fill_color="#FFFFFF",
                stroke_width=0
            )
            fade_rect.move_to(base.get_top(), aligned_edge=UP)
        else:
            fade_rect = Rectangle(
                width=base.width + 0.5,
                height=mask_height,
                fill_opacity=0.85,
                fill_color="#FFFFFF",
                stroke_width=0
            )
            fade_rect.move_to(base.get_bottom(), aligned_edge=DOWN)
        
        faded_text = VGroup(base, fade_rect)
        return faded_text
    
    def construct(self):
        ACTIVE_COLOR = BLACK
        INACTIVE_COLOR = GREY_B
        CENTER_Y = 0
        OFFSET_Y = 1.1
        
        year_2026 = Text("2026", font_size=72, weight=BOLD).set_color(ACTIVE_COLOR)
        year_2026.move_to([0, CENTER_Y, 0])
        
        year_2025 = self.create_gradient_fade_text(
            "2025", font_size=60, color=INACTIVE_COLOR, fade_direction="top"
        )
        year_2027 = self.create_gradient_fade_text(
            "2027", font_size=60, color=INACTIVE_COLOR, fade_direction="bottom"
        )
        
        year_2025.move_to([0, CENTER_Y + OFFSET_Y, 0])
        year_2027.move_to([0, CENTER_Y - OFFSET_Y, 0])
        
        self.add(year_2025, year_2026, year_2027)
        self.wait(0.4)
        
        self.play(
            year_2025.animate.move_to([0, CENTER_Y, 0]).scale(1.1),
            year_2026.animate.move_to([0, CENTER_Y - OFFSET_Y, 0]).scale(0.9),
            year_2027.animate.move_to([0, CENTER_Y - 2 * OFFSET_Y, 0]).scale(0.85),
            run_time=1.2,
            rate_func=smooth,
        )
        self.wait(0.3)
        
        self.play(
            year_2025.animate.move_to([0, CENTER_Y + OFFSET_Y, 0]).scale(0.9),
            year_2026.animate.move_to([0, CENTER_Y, 0]).scale(1.1),
            year_2027.animate.move_to([0, CENTER_Y - OFFSET_Y, 0]).scale(0.9),
            run_time=1.0,
            rate_func=smooth,
        )
        self.wait(0.6)