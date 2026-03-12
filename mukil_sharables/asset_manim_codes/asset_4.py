from manim import *
import numpy as np


class AcademicIntelligenceDashboard(VGroup):
    """
    Academic Intelligence Dashboard asset.
    
    Hierarchical container exposing:
    - self.base_background: rounded rectangle with shadow
    - self.header_group: top divider line
    - self.metrics_group: primary metrics zone (MetricCard, GeographyCard, DonutCard, BarCard)
    - self.details_group: secondary details zone
    - self.card_container: logical grouping of all card subcomponents
    
    Enables external animation of individual cards, zones, and metrics.
    """
    
    def __init__(
        self,
        width=8.0,
        height=5.0,
        bg_color="#0F172A",
        accent_color="#F97316",
        text_color="#A5B4FC",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.width = width
        self.height = height
        self.bg_color = ManimColor(bg_color)
        self.accent_color = ManimColor(accent_color)
        self.text_color = ManimColor(text_color)
        
        # Build structural layers
        self._build_base_background()
        self._build_header()
        self._build_metrics_zone()
        self._build_details_zone()
        self._assemble_dashboard()
    
    def _build_base_background(self):
        """
        Create rounded rectangle background with semi-transparent drop shadow.
        """
        # Shadow layer (offset down and right)
        self.shadow = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.15,
            fill_color=BLACK,
            fill_opacity=0.15,
            stroke_width=0
        ).shift(RIGHT * 0.1 + DOWN * 0.1)
        
        # Main background
        self.background = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.15,
            fill_color=self.bg_color,
            fill_opacity=1,
            stroke_color=self.accent_color,
            stroke_width=2
        )
        
        self.base_background = VGroup(self.shadow, self.background)
    
    def _build_header(self):
        """
        Create header divider line at top of content area.
        """
        line_width = self.width * 0.9
        header_line = Line(
            LEFT * (line_width / 2),
            RIGHT * (line_width / 2),
            color=self.accent_color,
            stroke_width=2
        )
        header_line.move_to(self.background.get_top() + DOWN * 0.4)
        
        self.header_group = VGroup(header_line)
        self.header_group.move_to(self.background.get_center())
    
    def _build_metrics_zone(self):
        """
        Create primary metrics zone with MetricCard, GeographyCard, DonutCard, BarCard.
        Arranged in grid-like structure using relative positioning.
        """
        # Zone positioned relative to background center
        zone_center = self.background.get_center() + UP * 0.8
        
        # MetricCard 1: Students Reached
        metric_1 = self._create_metric_card(
            prefix="",
            value=15000,
            suffix="+",
            label="Students Reached",
            color=self.text_color
        )
        metric_1.move_to(zone_center + LEFT * 2.5 + UP * 0.5)
        
        # MetricCard 2: Schools Empaneled
        metric_2 = self._create_metric_card(
            prefix="",
            value=250,
            suffix="",
            label="Schools Empaneled",
            color=self.text_color
        )
        metric_2.move_to(metric_1.get_center() + RIGHT * 2.0)
        
        # GeographyCard: Pan India Reach
        geo_card = self._create_geography_card()
        geo_card.move_to(metric_2.get_center() + RIGHT * 2.0)
        
        # DonutCard: Young Women Scholars
        donut_card = self._create_donut_card(percent=68)
        donut_card.move_to(zone_center + LEFT * 2.5 + DOWN * 1.5)
        
        # BarCard: First Generation Learners
        bar_card = self._create_bar_card()
        bar_card.move_to(donut_card.get_center() + RIGHT * 2.0)
        
        # Group all cards
        self.card_container = VGroup(metric_1, metric_2, geo_card, donut_card, bar_card)
        self.metrics_group = VGroup(self.card_container)
        self.metrics_group.move_to(self.background.get_center())
    
    def _build_details_zone(self):
        """
        Create secondary details zone with text elements and connector indicators.
        """
        details_center = self.background.get_center() + DOWN * 1.8
        
        # Detail label 1
        detail_1 = Text(
            "Real-time Progress Tracking",
            font="Times New Roman",
            font_size=16,
            color=self.text_color
        )
        detail_1.move_to(details_center + LEFT * 1.5)
        
        # Connector dot 1
        dot_1 = Circle(radius=0.08, fill_color=self.accent_color, fill_opacity=1, stroke_width=0)
        dot_1.move_to(detail_1.get_left() + LEFT * 0.3)
        
        # Detail label 2
        detail_2 = Text(
            "Competency Insights",
            font="Times New Roman",
            font_size=16,
            color=self.text_color
        )
        detail_2.move_to(details_center + RIGHT * 1.5)
        
        # Connector dot 2
        dot_2 = Circle(radius=0.08, fill_color=self.accent_color, fill_opacity=1, stroke_width=0)
        dot_2.move_to(detail_2.get_left() + LEFT * 0.3)
        
        self.details_group = VGroup(detail_1, dot_1, detail_2, dot_2)
        self.details_group.move_to(self.background.get_center())
    
    def _assemble_dashboard(self):
        """
        Assemble all structural layers into final dashboard.
        """
        self.add(
            self.base_background,
            self.header_group,
            self.metrics_group,
            self.details_group
        )
    
    def _create_metric_card(self, prefix, value, suffix, label, color):
        """
        Helper: Create a metric card subcomponent.
        """
        card_bg = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.1,
            fill_color=ManimColor("#1E293B"),
            fill_opacity=0.8,
            stroke_color=color,
            stroke_width=1
        )
        
        # Number
        num_text = Text(
            str(int(value)),
            font="Times New Roman",
            font_size=24,
            color=color
        )
        num_text.move_to(card_bg.get_center() + UP * 0.15)
        
        # Suffix
        suffix_text = Text(
            suffix,
            font="Times New Roman",
            font_size=12,
            color=color
        ) if suffix else VMobject()
        suffix_text.next_to(num_text, RIGHT, buff=0.05)
        
        # Label
        label_text = Text(
            label,
            font="Times New Roman",
            font_size=10,
            color=color
        )
        label_text.move_to(card_bg.get_center() + DOWN * 0.35)
        
        card = VGroup(card_bg, num_text, suffix_text, label_text)
        return card
    
    def _create_geography_card(self):
        """
        Helper: Create geography card (Districts & States).
        """
        card_bg = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.1,
            fill_color=ManimColor("#1E293B"),
            fill_opacity=0.8,
            stroke_color=self.text_color,
            stroke_width=1
        )
        
        # Districts
        dist_text = Text(
            "28\nDistricts",
            font="Times New Roman",
            font_size=12,
            color=self.text_color,
            line_spacing=0.8
        )
        dist_text.move_to(card_bg.get_center() + LEFT * 0.3)
        
        # States
        state_text = Text(
            "8\nStates",
            font="Times New Roman",
            font_size=12,
            color=self.text_color,
            line_spacing=0.8
        )
        state_text.move_to(card_bg.get_center() + RIGHT * 0.3)
        
        card = VGroup(card_bg, dist_text, state_text)
        return card
    
    def _create_donut_card(self, percent):
        """
        Helper: Create donut chart card.
        """
        card_bg = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.1,
            fill_color=ManimColor("#1E293B"),
            fill_opacity=0.8,
            stroke_color=self.text_color,
            stroke_width=1
        )
        
        # Donut base
        donut_base = Annulus(
            arc_center=card_bg.get_center() + UP * 0.1,
            inner_radius=0.25,
            outer_radius=0.4,
            fill_color=ManimColor("#374151"),
            fill_opacity=0.5,
            stroke_width=0
        )
        
        # Donut sector (filled portion)
        angle = (percent / 100.0) * TAU
        donut_sector = AnnularSector(
            arc_center=card_bg.get_center() + UP * 0.1,
            inner_radius=0.25,
            outer_radius=0.4,
            start_angle=PI / 2,
            angle=angle,
            fill_color=self.accent_color,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Percent text
        percent_text = Text(
            f"{int(percent)}%",
            font="Times New Roman",
            font_size=16,
            color=self.accent_color
        )
        percent_text.move_to(card_bg.get_center() + UP * 0.1)
        
        # Label
        label_text = Text(
            "Young Women",
            font="Times New Roman",
            font_size=9,
            color=self.text_color
        )
        label_text.move_to(card_bg.get_center() + DOWN * 0.35)
        
        card = VGroup(card_bg, donut_base, donut_sector, percent_text, label_text)
        return card
    
    def _create_bar_card(self):
        """
        Helper: Create horizontal bar chart card.
        """
        card_bg = RoundedRectangle(
            width=1.6,
            height=1.2,
            corner_radius=0.1,
            fill_color=ManimColor("#1E293B"),
            fill_opacity=0.8,
            stroke_color=self.text_color,
            stroke_width=1
        )
        
        # Bar background
        bar_bg = RoundedRectangle(
            width=1.0,
            height=0.15,
            corner_radius=0.08,
            fill_color=ManimColor("#374151"),
            fill_opacity=0.5,
            stroke_width=0
        )
        bar_bg.move_to(card_bg.get_center() + UP * 0.15)
        
        # Bar fill (9/10)
        bar_fill = RoundedRectangle(
            width=0.9,
            height=0.15,
            corner_radius=0.08,
            fill_color=self.accent_color,
            fill_opacity=1,
            stroke_width=0
        )
        bar_fill.move_to(bar_bg.get_left(), aligned_edge=LEFT)
        
        # Ratio text
        ratio_text = Text(
            "9/10",
            font="Times New Roman",
            font_size=18,
            color=self.accent_color
        )
        ratio_text.move_to(card_bg.get_center() + DOWN * 0.05)
        
        # Label
        label_text = Text(
            "First Gen Learners",
            font="Times New Roman",
            font_size=9,
            color=self.text_color
        )
        label_text.move_to(card_bg.get_center() + DOWN * 0.45)
        
        card = VGroup(card_bg, bar_bg, bar_fill, ratio_text, label_text)
        return card
    
    # Public getter methods for external animation access
    
    def get_metric_card(self, index):
        """
        Retrieve a specific metric card by index.
        index: 0-4 (cards in card_container)
        """
        if 0 <= index < len(self.card_container):
            return self.card_container[index]
        return None
    
    def get_subcomponent(self, name):
        """
        Retrieve a major structural layer by name.
        name: 'base_background', 'header_group', 'metrics_group', 'details_group', 'card_container'
        """
        if hasattr(self, name):
            return getattr(self, name)
        return None
    
    def get_zone(self, zone_name):
        """
        Retrieve a zone by name.
        zone_name: 'metrics' or 'details'
        """
        if zone_name == "metrics":
            return self.metrics_group
        elif zone_name == "details":
            return self.details_group
        return None