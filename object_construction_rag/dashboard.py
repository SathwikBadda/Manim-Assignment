"""
Impact Dashboard Animation Elements

This script uses the Manim library to provide visual components for a dashboard displaying key impact metrics.
It defines modular 'Card' classes for different data types (Metrics, Geography, Donut Charts, Bar Charts).
The classes expose getters, setters, and animation helper methods for manipulation from external scenes.
"""
from manim import *
import numpy as np


# =========================
# BASE CARD
# =========================
class Card(VGroup):
    """
    Base class for all dashboard cards.
    Creates a rounded rectangle background with a shadow.
    """
    def __init__(self, width, height, position):
        super().__init__()

        self.shadow = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.2,
            fill_color=BLACK,
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(position + RIGHT * 0.05 + DOWN * 0.05)

        self.bg = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.2,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(position)

        self.add(self.shadow, self.bg)


# =========================
# METRIC CARD
# =========================
class MetricCard(Card):
    """
    Displays a key metric with a label.
    Supports prefixes (like currency) and suffixes (units).
    Provides methods to get/set values and generate animations.
    """
    def __init__(
        self, position, width, height,
        prefix, value, suffix,
        color, label,
        font_size=64, decimals=0
    ):
        super().__init__(width, height, position)

        self.color = ManimColor(color)
        self.font_size = font_size
        self.decimals = decimals
        self.prefix = prefix
        self.suffix = suffix
        
        self.number = DecimalNumber(
            value,
            num_decimal_places=decimals,
            font_size=font_size,
            color=self.color,
            group_with_commas=True
        )

        items = []
        items.append(self.number)
        
        self.prefix_elem = None
        self.suffix_elem = None

        if prefix:
            if prefix == "₹" or prefix == "\u20b9":
                 self.prefix_elem = Text(prefix, font="sans-serif", font_size=font_size * 0.6, color=self.color, weight=BOLD)
            else:
                 self.prefix_elem = Tex(rf"\textbf{{{prefix}}}", font_size=font_size * 0.6, color=self.color)
            items.insert(0, self.prefix_elem)
        
        if suffix:
            self.suffix_elem = Tex(rf"\textbf{{{suffix}}}", font_size=font_size * 0.75, color=self.color)
            items.append(self.suffix_elem)

        self.metric_group = VGroup(*items).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        
        if self.suffix == "+" and self.suffix_elem:
            self.suffix_elem.shift(UP * 0.15)
        
        self.metric_group.move_to(self.bg.get_center() + UP * 0.2)
        
        self.label_text = Tex(rf"\textbf{{{label}}}", font_size=18, color=GRAY)
        self.label_text.move_to(self.bg.get_center() + DOWN * 0.65)

        self.add(self.metric_group, self.label_text)

    def get_subcomponent(self, component_name: str):
        """Access a specific subcomponent of the card."""
        components = {
            "number": self.number,
            "prefix": self.prefix_elem,
            "suffix": self.suffix_elem,
            "label": self.label_text,
            "metric_group": self.metric_group,
            "bg": self.bg,
            "shadow": self.shadow
        }
        return components.get(component_name, None)

    def set_value(self, new_value):
        """Directly set the number to a new value."""
        self.number.set_value(new_value)
        self._realign_metric_group()
        
    def set_label(self, new_label):
        """Update the label text below the metric."""
        new_label_tex = Tex(rf"\textbf{{{new_label}}}", font_size=18, color=GRAY)
        new_label_tex.move_to(self.label_text.get_center())
        self.remove(self.label_text)
        self.add(new_label_tex)
        self.label_text = new_label_tex
        
    def set_color(self, new_color):
        """Update the main color scheme of the card components."""
        c = ManimColor(new_color)
        self.color = c
        self.number.set_color(c)
        if self.prefix_elem:
            self.prefix_elem.set_color(c)
        if self.suffix_elem:
            self.suffix_elem.set_color(c)

    def _realign_metric_group(self):
        """Helper to re-center the metric group layout."""
        self.metric_group.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        if self.suffix == "+" and self.suffix_elem:
            self.suffix_elem.shift(UP * 0.15)
        self.metric_group.move_to(self.bg.get_center() + UP * 0.2)

    def animate_entry(self, animation_type=FadeIn, **kwargs):
        """Animation helper for card entry (e.g. FadeIn)."""
        return animation_type(self, **kwargs)
        
    def animate_value_change(self, target_value: float, run_time: float = 1.0):
        """Animation helper to transition smoothly to a new metric value."""
        start_value = self.number.get_value()
        def update_func(m, alpha):
            val = interpolate(start_value, target_value, alpha)
            self.set_value(val)
        return UpdateFromAlphaFunc(self, update_func, run_time=run_time)


# =========================
# GEOGRAPHY CARD
# =========================
class GeographyCard(Card):
    """
    Specialized card for geographic reach (Districts & States).
    Contains two sub-metrics side by side.
    """
    def __init__(self, position):
        super().__init__(4.0, 2.0, position)

        # --- District Metric ---
        self.dist_bg = RoundedRectangle(
            width=1.5, height=1.1, corner_radius=0.1,
            fill_color="#F8F9FA", fill_opacity=1, stroke_color="#E0E0E0"
        ).move_to(position + LEFT * 0.9 + UP * 0.15)

        self.dist_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6")
        self.dist_num.move_to(self.dist_bg.get_center() + LEFT * 0.2)

        self.dist_lbl = Tex(r"\textbf{Districts}", font_size=18, color=GRAY)
        self.dist_lbl.move_to(self.dist_bg.get_center() + DOWN * 0.3)

        # --- State Metric ---
        self.state_bg = self.dist_bg.copy().move_to(position + RIGHT * 0.9 + UP * 0.15)
        self.state_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6")
        self.state_num.move_to(self.state_bg.get_center() + LEFT * 0.2)

        self.state_lbl = Tex(r"\textbf{States}", font_size=18, color=GRAY)
        self.state_lbl.move_to(self.state_bg.get_center() + DOWN * 0.3)

        # Bottom Caption
        self.bottom = Tex(r"\textbf{\textit{Pan India Reach}}", font_size=18, color=GRAY)
        self.bottom.move_to(self.bg.get_center() + DOWN * 0.65)

        self.add(self.dist_bg, self.dist_num, self.dist_lbl, self.state_bg, self.state_num, self.state_lbl, self.bottom)

    def get_subcomponent(self, component_name: str):
        components = {
            "dist_bg": self.dist_bg,
            "dist_num": self.dist_num,
            "dist_lbl": self.dist_lbl,
            "state_bg": self.state_bg,
            "state_num": self.state_num,
            "state_lbl": self.state_lbl,
            "bottom": self.bottom,
            "bg": self.bg,
            "shadow": self.shadow
        }
        return components.get(component_name, None)

    def set_dist_value(self, value):
        self.dist_num.set_value(value)

    def set_state_value(self, value):
        self.state_num.set_value(value)

    def set_bottom_label(self, new_text):
        new_bottom = Tex(rf"\textbf{{\textit{{{new_text}}}}}", font_size=18, color=GRAY)
        new_bottom.move_to(self.bottom.get_center())
        self.remove(self.bottom)
        self.add(new_bottom)
        self.bottom = new_bottom

    def animate_entry(self, animation_type=FadeIn, **kwargs):
        return animation_type(self, **kwargs)

    def animate_values_change(self, target_dist, target_state, run_time=1.0):
        start_dist = self.dist_num.get_value()
        start_state = self.state_num.get_value()
        
        def update_func(m, alpha):
            self.set_dist_value(interpolate(start_dist, target_dist, alpha))
            self.set_state_value(interpolate(start_state, target_state, alpha))
            
        return UpdateFromAlphaFunc(self, update_func, run_time=run_time)


# =========================
# DONUT CARD
# =========================
class DonutCard(Card):
    """
    Displays a donut chart with percentage.
    """
    def __init__(self, position, width, percent):
        super().__init__(width, 2.2, position)

        self.center_pos = self.bg.get_center() + UP * 0.25

        self.base = Annulus(
            arc_center=self.center_pos,
            inner_radius=0.55, outer_radius=0.95, 
            fill_color=GRAY, fill_opacity=0.2, stroke_width=0
        )

        self.sector = AnnularSector(
            arc_center=self.center_pos,
            inner_radius=0.55, outer_radius=0.95, 
            start_angle=PI/2, angle=0.001,
            fill_color="#E91E63", stroke_width=0
        )

        self.num = DecimalNumber(0, num_decimal_places=0, font_size=32, color="#E91E63")
        self.sym = Tex(r"\%", font_size=20, color="#E91E63")
        self.grp = VGroup(self.num, self.sym).arrange(RIGHT, buff=0.05, aligned_edge=UP)
        self.grp.move_to(self.center_pos)

        self.label_text = Tex(r"\textbf{Young Women Scholars}", font_size=18, color=GRAY)
        self.label_text.move_to(self.bg.get_center() + DOWN * 0.85) 

        self.add(self.base, self.sector, self.grp, self.label_text)
        
        # Apply initial settings
        self.set_percent(percent)

    def get_subcomponent(self, component_name: str):
        components = {
            "base": self.base,
            "sector": self.sector,
            "number": self.num,
            "symbol": self.sym,
            "group": self.grp,
            "label": self.label_text,
            "bg": self.bg,
            "shadow": self.shadow
        }
        return components.get(component_name, None)
        
    def _realign_grp(self):
        self.grp.arrange(RIGHT, buff=0.05, aligned_edge=UP)
        self.grp.move_to(self.center_pos)

    def set_percent(self, percent):
        self.num.set_value(percent)
        self._realign_grp()
        
        angle = max(0.001, (percent / 100) * TAU)
        new_sector = AnnularSector(
            arc_center=self.center_pos,
            inner_radius=0.55, outer_radius=0.95,
            start_angle=PI/2, angle=angle,
            fill_color=self.sector.get_color(), stroke_width=0
        )
        self.sector.become(new_sector)

    def set_label(self, new_label):
        new_label_tex = Tex(rf"\textbf{{{new_label}}}", font_size=18, color=GRAY)
        new_label_tex.move_to(self.label_text.get_center())
        self.remove(self.label_text)
        self.add(new_label_tex)
        self.label_text = new_label_tex

    def animate_entry(self, animation_type=FadeIn, **kwargs):
        return animation_type(self, **kwargs)

    def animate_percent_change(self, target_percent, run_time=1.0):
        start_percent = self.num.get_value()
        def update_func(m, alpha):
            val = interpolate(start_percent, target_percent, alpha)
            self.set_percent(val)
        return UpdateFromAlphaFunc(self, update_func, run_time=run_time)


# =========================
# BAR CARD
# =========================
class BarCard(Card):
    """
    Displays a horizontal bar chart with a ratio (e.g., 9/10).
    """
    def __init__(self, position, width):
        super().__init__(width, 1.6, position)

        self.bg_bar = RoundedRectangle(
            width=width * 0.7, height=0.3, corner_radius=0.15,
            fill_color=GRAY, fill_opacity=0.2, stroke_width=0
        ).move_to(self.bg.get_center() + DOWN * 0.15)

        self.bar = RoundedRectangle(
            width=0.01, height=0.3, corner_radius=0.15,
            fill_color="#17A2B8", fill_opacity=1, stroke_width=0
        ).move_to(self.bg_bar.get_left(), aligned_edge=LEFT)

        self.num = DecimalNumber(0, num_decimal_places=0, font_size=54, color="#17A2B8")
        self.txt = Tex(r"/10", font_size=48, color="#17A2B8")
        self.grp = VGroup(self.num, self.txt).arrange(RIGHT, buff=0.1)
        self.grp.move_to(self.bg.get_center() + UP * 0.35)

        self.label_text = Tex(r"\textbf{First Generation Learners}", font_size=18, color=GRAY)
        self.label_text.move_to(self.bg.get_center() + DOWN * 0.6)

        self.add(self.bg_bar, self.bar, self.grp, self.label_text)
        
        self.target_denom = 10
        self.target_num = 0

    def get_subcomponent(self, component_name: str):
        components = {
            "bg_bar": self.bg_bar,
            "bar": self.bar,
            "number": self.num,
            "denominator_text": self.txt,
            "group": self.grp,
            "label": self.label_text,
            "bg": self.bg,
            "shadow": self.shadow
        }
        return components.get(component_name, None)

    def set_ratio(self, numerator, denominator=10):
        self.target_num = numerator
        self.target_denom = denominator
        self.num.set_value(numerator)
        
        new_txt = Tex(rf"/{denominator}", font_size=48, color=self.txt.get_color())
        
        self.grp.remove(self.txt)
        self.txt = new_txt
        self.grp.add(self.txt)
        self.grp.arrange(RIGHT, buff=0.1)
        self.grp.move_to(self.bg.get_center() + UP * 0.35)
        
        ratio = numerator / max(1, denominator)
        w = max(0.01, self.bg_bar.width * ratio)
        new_bar = RoundedRectangle(
            width=w, height=0.3, corner_radius=0.15,
            fill_color=self.bar.get_color(), fill_opacity=1, stroke_width=0
        ).move_to(self.bg_bar.get_left(), aligned_edge=LEFT)
        self.bar.become(new_bar)

    def set_label(self, new_label):
        new_label_tex = Tex(rf"\textbf{{{new_label}}}", font_size=18, color=GRAY)
        new_label_tex.move_to(self.label_text.get_center())
        self.remove(self.label_text)
        self.add(new_label_tex)
        self.label_text = new_label_tex

    def animate_entry(self, animation_type=FadeIn, **kwargs):
        return animation_type(self, **kwargs)

    def animate_ratio_change(self, target_numerator, target_denominator=10, run_time=1.0):
        start_num = self.num.get_value()
        def update_func(m, alpha):
            val_num = interpolate(start_num, target_numerator, alpha)
            self.set_ratio(val_num, target_denominator)
        return UpdateFromAlphaFunc(self, update_func, run_time=run_time)
