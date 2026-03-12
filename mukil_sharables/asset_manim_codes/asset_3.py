from manim import *
from manim.utils.rate_functions import linear, ease_out_cubic, ease_in_out_quad
import numpy as np

class Pathway(VGroup):
    """
    A reusable pathway module asset with exposed semantic components.
    
    Attributes:
        module_group (VGroup): Master container for the entire module.
        boundary (RoundedRectangle): Outer rectangle defining module envelope.
        title_text (VGroup): Primary title text element.
        subheading_text (VGroup): Secondary subheading text element.
        descriptor_text (VGroup): Tertiary descriptor text element.
        text_group (VGroup): Grouped collection of all text elements.
        flow_arrow (VGroup): Downward-pointing arrow for flow indication.
    """
    
    def __init__(
        self,
        width=4.0,
        height=1.2,
        title="SATHI NAO",
        subheading="Grades 8–10",
        descriptor="Early Aptitude & Scholarship Readiness",
        include_arrow=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.width = width
        self.height = height
        self.title = title
        self.subheading = subheading
        self.descriptor = descriptor
        self.include_arrow = include_arrow
        
        # Color definitions
        self.PRIMARY_ACCENT = ManimColor("#F97316")
        self.PRIMARY_TEXT = ManimColor("#C6C7DC")
        self.SECONDARY_TEXT = ManimColor("#A5B4FC")
        
        # Component placeholders
        self.boundary = None
        self.title_text = None
        self.subheading_text = None
        self.descriptor_text = None
        self.text_group = None
        self.flow_arrow = None
        self.module_group = None
        
        self._build_structure()
    
    def _build_structure(self):
        """Construct the pathway module with hierarchical structure."""
        
        # ===== BOUNDARY RECTANGLE =====
        self.boundary = RoundedRectangle(
            width=self.width,
            height=self.height,
            corner_radius=0.1,
            fill_opacity=0,
            stroke_color=self.PRIMARY_ACCENT,
            stroke_width=2
        )
        
        # ===== TEXT LAYER =====
        # Title text
        self.title_text = VGroup(
            Text(
                self.title,
                font="Georgia",
                font_size=36,
                weight=BOLD,
                color=self.PRIMARY_TEXT
            )
        )
        
        # Subheading text
        self.subheading_text = VGroup(
            Text(
                self.subheading,
                font="Times New Roman",
                font_size=24,
                weight=NORMAL,
                color=self.SECONDARY_TEXT
            )
        )
        
        # Descriptor text
        self.descriptor_text = VGroup(
            Text(
                self.descriptor,
                font="Times New Roman",
                font_size=18,
                weight=LIGHT,
                color=self.SECONDARY_TEXT
            )
        )
        
        # Assemble text group with proper spacing
        self.text_group = VGroup(
            self.title_text,
            self.subheading_text,
            self.descriptor_text
        )
        
        # Position text elements vertically within the boundary
        self.title_text.align_to(self.boundary.get_top(), UP).shift(DOWN * 0.15)
        self.subheading_text.next_to(self.title_text, DOWN, buff=0.1)
        self.descriptor_text.next_to(self.subheading_text, DOWN, buff=0.15)
        
        # Center text horizontally within boundary
        self.text_group.move_to(self.boundary.get_center())
        self.text_group.align_to(self.boundary, UP).shift(DOWN * 0.15)
        
        # ===== FLOW ARROW =====
        arrow_start = self.boundary.get_bottom() + DOWN * 0.1
        arrow_end = arrow_start + DOWN * 0.3
        
        arrow_line = Line(
            start=arrow_start,
            end=arrow_end,
            stroke_color=self.PRIMARY_ACCENT,
            stroke_width=1.5
        )
        
        # Arrowhead polygon
        arrowhead = Polygon(
            arrow_end,
            arrow_end + UP * 0.08 + LEFT * 0.05,
            arrow_end + UP * 0.08 + RIGHT * 0.05,
            fill_color=self.PRIMARY_ACCENT,
            fill_opacity=1,
            stroke_width=0
        )
        
        self.flow_arrow = VGroup(arrow_line, arrowhead) if self.include_arrow else VGroup()
        
        # ===== MASTER MODULE GROUP =====
        self.module_group = VGroup(
            self.boundary,
            self.text_group,
            self.flow_arrow
        )
        
        self.add(self.module_group)
    
    def get_boundary(self):
        """Return the outer rectangle for relative positioning."""
        return self.boundary
    
    def get_text_layer(self):
        """Return the grouped text elements for animation."""
        return self.text_group
    
    def get_arrow(self):
        """Return the flow arrow for conditional visibility control."""
        return self.flow_arrow
    
    def set_title(self, new_title):
        """Update the title text."""
        self.title_text[0].become(
            Text(
                new_title,
                font="Georgia",
                font_size=36,
                weight=BOLD,
                color=self.PRIMARY_TEXT
            )
        )
        self.title_text[0].align_to(self.boundary.get_top(), UP).shift(DOWN * 0.15)
    
    def set_subheading(self, new_subheading):
        """Update the subheading text."""
        self.subheading_text[0].become(
            Text(
                new_subheading,
                font="Times New Roman",
                font_size=24,
                weight=NORMAL,
                color=self.SECONDARY_TEXT
            )
        )
        self.subheading_text[0].next_to(self.title_text, DOWN, buff=0.1)
    
    def set_descriptor(self, new_descriptor):
        """Update the descriptor text."""
        self.descriptor_text[0].become(
            Text(
                new_descriptor,
                font="Times New Roman",
                font_size=18,
                weight=LIGHT,
                color=self.SECONDARY_TEXT
            )
        )
        self.descriptor_text[0].next_to(self.subheading_text, DOWN, buff=0.15)
    
    def hide_arrow(self):
        """Hide the flow arrow."""
        self.flow_arrow.set_opacity(0)
    
    def show_arrow(self):
        """Show the flow arrow."""
        self.flow_arrow.set_opacity(1)
    
    def animate_text_reveal(self):
        """Return animation for sequential text reveal."""
        return AnimationGroup(
            AddTextLetterByLetter(self.title_text[0], run_time=0.35, rate_func=linear),
            AddTextLetterByLetter(self.subheading_text[0], run_time=0.25, rate_func=linear),
            AddTextLetterByLetter(self.descriptor_text[0], run_time=0.35, rate_func=linear),
            lag_ratio=0.1
        )
    
    def animate_boundary_grow(self):
        """Return animation for boundary expansion."""
        return GrowFromCenter(self.boundary, run_time=0.6, rate_func=ease_out_cubic)

    def animate_arrow_reveal(self):
        """Return animation for arrow appearance."""
        return Create(self.flow_arrow, run_time=0.3, rate_func=ease_in_out_quad)