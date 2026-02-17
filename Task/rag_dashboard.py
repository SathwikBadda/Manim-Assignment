from manim import *
import numpy as np


# =========================
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

        # ------------------------------------------------------
        # Create a shadow for depth effect
        # This is a semi-transparent black rectangle shifted slightly
        # down and right to simulate a drop shadow.
        # ------------------------------------------------------
        shadow = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.2,
            fill_color=BLACK,
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(position + RIGHT * 0.05 + DOWN * 0.05)

        # ------------------------------------------------------
        # Main background card
        # This is the actual visible card content carrier, placed
        # at the exact target position.
        # ------------------------------------------------------
        bg = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.2,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        ).move_to(position)

        self.bg = bg
        self.add(shadow, bg)


# =========================
# =========================
# METRIC CARD
# =========================
class MetricCard(Card):
    """
    Displays a key metric with a label.
    Supports prefixes (like currency), suffixes (units), and animating numbers.
    """
    def __init__(
        self, position, width, height,
        prefix, value, suffix,
        color, label,
        font_size=64, decimals=0
    ):
        super().__init__(width, height, position)

        self.target_value = value
        self.suffix = suffix

        self.target_value = value
        self.suffix = suffix

        # ------------------------------------------------------
        # Dynamic Number Object
        # This DecimalNumber will animate from 0 to the target value.
        # It handles formatting like font size, color, and commas.
        # ------------------------------------------------------
        number = DecimalNumber(
            0,
            num_decimal_places=decimals,
            font_size=font_size,
            color=color,
            group_with_commas=True
        )
        self.number = number

        items = [] # Initialize items list for horizontal arrangement
        items.append(number)
        
        # Store layout elements
        self.prefix_elem = None
        self.suffix_elem = None

        # Handle Prefix (Currency symbols etc.)
        if prefix:
            if prefix == "₹" or prefix == "\u20b9":
                 # Use Text for Rupee to avoid LaTeX issues
                 self.prefix_elem = Text(prefix, font="sans-serif", font_size=font_size * 0.6, color=color, weight=BOLD)
            else:
                 self.prefix_elem = Tex(rf"\textbf{{{prefix}}}", font_size=font_size * 0.6, color=color)
            items.insert(0, self.prefix_elem)
        
        # Handle Suffix (Units etc.)
        if suffix:
            self.suffix_elem = Tex(rf"\textbf{{{suffix}}}", font_size=font_size * 0.75, color=color)
            items.append(self.suffix_elem)

        # Arrange items horizontally
        # ------------------------------------------------------
        # Layout Assembly
        # Arrange the prefix, number, and suffix horizontally.
        # The 'aligned_edge=DOWN' ensures they sit on the same baseline.
        # ------------------------------------------------------
        metric = VGroup(*items).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        
        # Correction: Shift '+' suffix up slightly to align with the number center
        if self.suffix == "+" and self.suffix_elem:
            self.suffix_elem.shift(UP * 0.15)
        
        metric.move_to(self.bg.get_center() + UP * 0.2)
        
        self.metric_group = metric

        # ------------------------------------------------------
        # Bottom Label
        # A static text label placed below the main metric numbers.
        # ------------------------------------------------------
        label_text = Tex(rf"\textbf{{{label}}}", font_size=18, color=GRAY)
        label_text.move_to(self.bg.get_center() + DOWN * 0.65)

        self.add(metric, label_text)

    def animate(self):
        """
        Animates the number counting up from 0 to target_value.
        Dynamically adjusts layout to keep content centered.
        """
        tracker = ValueTracker(0)
        
        # ------------------------------------------------------
        # Updater Function
        # This function runs every frame during the animation.
        # 1. Updates the number's value based on the tracker.
        # 2. Re-arranges the group to keep it centered as width changes.
        # ------------------------------------------------------
        def update_layout(m):
            # 1. Update number value
            m.set_value(tracker.get_value())
            
            # 2. Re-arrange the group to maintain center alignment
            self.metric_group.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            
            # Apply suffix position correction again after rearrange
            if self.suffix == "+":
                 self.suffix_elem.shift(UP * 0.15)
                 
            self.metric_group.move_to(self.bg.get_center() + UP * 0.2)
            
        self.number.add_updater(update_layout)
        return tracker.animate.set_value(self.target_value)


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

        # ------------------------------------------------------
        # District Metric Construction
        # A small box within the card to show 'Districts'.
        # ------------------------------------------------------
        dist_bg = RoundedRectangle(
            width=1.5, height=1.1, corner_radius=0.1,
            fill_color="#F8F9FA", fill_opacity=1,
            stroke_color="#E0E0E0"
        ).move_to(position + LEFT * 0.9 + UP * 0.15)

        dist_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6")
        dist_num.target = 739
        dist_num.move_to(dist_bg.get_center() + LEFT * 0.2)

        dist_lbl = Tex(r"\textbf{Districts}", font_size=18, color=GRAY)
        dist_lbl.move_to(dist_bg.get_center() + DOWN * 0.3)

        # ------------------------------------------------------
        # State Metric Construction
        # A second small box within the card to show 'States'.
        # ------------------------------------------------------
        state_bg = dist_bg.copy().move_to(position + RIGHT * 0.9 + UP * 0.15)
        state_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6")
        state_num.target = 28
        state_num.move_to(state_bg.get_center() + LEFT * 0.2)

        state_lbl = Tex(r"\textbf{States}", font_size=18, color=GRAY)
        state_lbl.move_to(state_bg.get_center() + DOWN * 0.3)

        # Bottom Caption
        bottom = Tex(r"\textbf{\textit{Pan India Reach}}", font_size=18, color=GRAY)
        bottom.move_to(self.bg.get_center() + DOWN * 0.65)

        self.nums = [dist_num, state_num]
        self.add(dist_bg, dist_num, dist_lbl, state_bg, state_num, state_lbl, bottom)

    def animate(self):
        """Animate both counters simultaneously."""
        anims = []
        for num in self.nums:
            t = ValueTracker(0)
            num.add_updater(lambda m, tr=t: m.set_value(tr.get_value()))
            anims.append(t.animate.set_value(num.target))
        return AnimationGroup(*anims)


# =========================
# DONUT CARD
# =========================
class DonutCard(Card):
    """
    Displays a donut chart with percentage.
    """
    def __init__(self, position, width, percent):
        super().__init__(width, 2.2, position)

        center = self.bg.get_center() + UP * 0.25

        # Background Ring
        base = Annulus(
            arc_center=center,
            inner_radius=0.55, 
            outer_radius=0.95, 
            fill_color=GRAY,
            fill_opacity=0.2,
            stroke_width=0
        )

        # Active Sector (initially 0 degrees)
        self.sector = AnnularSector(
            arc_center=center,
            inner_radius=0.55,
            outer_radius=0.95, 
            start_angle=PI/2,
            angle=0.001,
            fill_color="#E91E63",
            stroke_width=0
        )

        # Percentage Text
        self.num = DecimalNumber(0, num_decimal_places=0, font_size=32, color="#E91E63")
        sym = Tex(r"\%", font_size=20, color="#E91E63")
        self.grp = VGroup(self.num, sym).arrange(RIGHT, buff=0.05, aligned_edge=UP)
        self.grp.move_to(center)

        label = Tex(r"\textbf{Young Women Scholars}", font_size=18, color=GRAY)
        label.move_to(self.bg.get_center() + DOWN * 0.85) 

        self.percent = percent
        self.center = center

        self.add(base, self.sector, self.grp, label)

    def animate(self):
        """
        Animates the sector filling up to 'percent' and the number counting up.
        """
        a = ValueTracker(0.001)
        v = ValueTracker(0)

        # ------------------------------------------------------
        # Sector Updater
        # Redraws the sector (arc) with an increasing angle.
        # This creates the "filling up" circular progress effect.
        # ------------------------------------------------------
        self.sector.add_updater(
            lambda m: m.become(
                AnnularSector(
                    arc_center=self.center,
                    inner_radius=0.55,
                    outer_radius=0.95,
                    start_angle=PI/2,
                    angle=a.get_value(),
                    fill_color="#E91E63"
                )
            )
        )
        
        # ------------------------------------------------------
        # Number Updater
        # Updates the center percentage text and ensures it stays centered.
        # ------------------------------------------------------
        def update_num(m):
            m.set_value(v.get_value())
            self.grp.arrange(RIGHT, buff=0.05, aligned_edge=UP)
            self.grp.move_to(self.center)
            
        self.num.add_updater(update_num)

        return AnimationGroup(
            a.animate.set_value(self.percent / 100 * TAU),
            v.animate.set_value(self.percent)
        )


# =========================
# BAR CARD
# =========================
class BarCard(Card):
    """
    Displays a horizontal bar chart with a ratio (e.g., 9/10).
    """
    def __init__(self, position, width):
        super().__init__(width, 1.6, position)

        # Bar background
        bg_bar = RoundedRectangle(
            width=width * 0.7,
            height=0.3,
            corner_radius=0.15,
            fill_color=GRAY,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(self.bg.get_center() + DOWN * 0.15)

        # Active Bar
        self.bar = RoundedRectangle(
            width=0.01,
            height=0.3,
            corner_radius=0.15,
            fill_color="#17A2B8",
            fill_opacity=1,
            stroke_width=0
        ).move_to(bg_bar.get_left(), aligned_edge=LEFT)

        self.bg_bar = bg_bar

        # Ratio Text
        self.num = DecimalNumber(0, num_decimal_places=0, font_size=54, color="#17A2B8")
        txt = Tex(r"/10", font_size=48, color="#17A2B8")
        grp = VGroup(self.num, txt).arrange(RIGHT, buff=0.1)
        grp.move_to(self.bg.get_center() + UP * 0.35)

        label = Tex(r"\textbf{First Generation Learners}", font_size=18, color=GRAY)
        label.move_to(self.bg.get_center() + DOWN * 0.6)

        self.add(bg_bar, self.bar, grp, label)

    def animate(self):
        """
        Animates the bar growing and the numerator counting up.
        """
        # ------------------------------------------------------
        # ------------------------------------------------------
        t = ValueTracker(0)
        self.num.add_updater(lambda m: m.set_value(9 * t.get_value()))

        # ------------------------------------------------------
        # Bar Geometry Updater
        # Increases the width of the colored bar based on the tracker value.
        # Uses 'aligned_edge=LEFT' to make it grow from left to right.
        # ------------------------------------------------------
        self.bar.add_updater(
            lambda m: m.become(
                RoundedRectangle(
                    width=max(0.01, self.bg_bar.width * 0.9 * t.get_value()),
                    height=0.3,
                    corner_radius=0.15,
                    fill_color="#17A2B8",
                    fill_opacity=1
                ).move_to(self.bg_bar.get_left(), aligned_edge=LEFT)
            )
        )
        return t.animate.set_value(1)


# =========================
# DASHBOARD SCENE
# =========================
class Buddy4StudyImpactDashboard(Scene):
    """
    Main scene that composes the dashboard.
    1. Sets background.
    2. Creates dashboard container.
    3. Places all metric cards.
    4. Animates entry and values.
    """
    def construct(self):
        self.camera.background_color = "#1E3A8A"

        dashboard = RoundedRectangle(
            width=14.5, height=7.8, corner_radius=0.5,
            fill_color="#F0F4F8", fill_opacity=1,
            stroke_color="#BDC3C7"
        )

        cards = [
            MetricCard(LEFT*4.6 + UP*2.1, 3.8, 2.0, "₹", 700, "Cr", "#FF6B35", "Total Funding Enabled"),
            MetricCard(UP*2.1, 4.0, 2.0, "", 1.53, "L", "#4A90E2", "Scholars Empowered", decimals=2),
            MetricCard(RIGHT*4.6 + UP*2.1, 4.0, 2.0, "", 11700, "+", "#50C878", "Institutions Reached"),
            DonutCard(LEFT*4.6 + DOWN*0.2, 4.0, 57), # Moved Down slightly
            GeographyCard(ORIGIN + DOWN*0.2), # Moved Down to align with Donut
            MetricCard(RIGHT*4.6 + DOWN*0.2, 3.8, 2.0, "", 20000, "+", "#FF9800", "Orphaned Scholars"), # Aligned
            BarCard(LEFT*2.6 + DOWN*2.6, 4.6),
            MetricCard(RIGHT*2.6 + DOWN*2.6, 4.4, 1.6, "", 2500, "+", "#9C27B0", "Differently-Abled"),
        ]

        # ------------------------------------------------------
        # 1. Background Ssetup
        # ------------------------------------------------------
        self.play(FadeIn(dashboard))

        # ------------------------------------------------------
        # 2. Entrance Animation
        # Fade in all cards with a slight upward shift.
        # ------------------------------------------------------
        self.play(*[FadeIn(c, shift=UP*0.2) for c in cards], run_time=1)

        # ------------------------------------------------------
        # 3. Data Animation
        # Triggers .animate() on every card to count up numbers/fill charts.
        # ------------------------------------------------------
        self.play(
            AnimationGroup(*[c.animate() for c in cards]),
            run_time=1.5,
            rate_func=smooth
        )

        self.wait(7)