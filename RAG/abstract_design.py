from manim import *
from manim.utils.color import ManimColor
import numpy as np

class Asset1(VGroup):
    def __init__(
        self,
        ribbon_height: float = 3.5,
        ribbon_width: float = 0.6,
        ribbon_spacing: float = 2.2,
        header_font_size: float = 36,
        content_font_size: float = 20,
        color_left: str = "#FF9500",
        color_center: str = "#0066FF",
        color_right: str = "#00CC66",
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.ribbon_height = ribbon_height
        self.ribbon_width = ribbon_width
        self.ribbon_spacing = ribbon_spacing
        self.header_font_size = header_font_size
        self.content_font_size = content_font_size
        
        self.color_left = ManimColor(color_left)
        self.color_center = ManimColor(color_center)
        self.color_right = ManimColor(color_right)
        
        # Content phrases for each column
        self.phrases_left = [
            "wider applicant pool",
            "lower initial cutoff",
            "diversity focus"
        ]
        self.phrases_center = [
            "4C breakdown",
            "psychometric profile",
            "peer benchmarking"
        ]
        self.phrases_right = [
            "longitudinal tracking",
            "value-add measurement",
            "cohort success"
        ]
        
        self._build_asset()
    
    def _build_ribbon(self, x_pos: float, color: ManimColor) -> VGroup:
        """Build a single ribbon using Bezier curves."""
        ribbon_group = VGroup()
        
        # Define Bezier path (vertical curve with slight wave)
        control_points_left = [
            np.array([x_pos - self.ribbon_width / 2, 0, 0]),
            np.array([x_pos - self.ribbon_width / 2 - 0.15, self.ribbon_height / 2, 0]),
            np.array([x_pos - self.ribbon_width / 2, self.ribbon_height, 0])
        ]
        
        control_points_right = [
            np.array([x_pos + self.ribbon_width / 2, 0, 0]),
            np.array([x_pos + self.ribbon_width / 2 + 0.15, self.ribbon_height / 2, 0]),
            np.array([x_pos + self.ribbon_width / 2, self.ribbon_height, 0])
        ]
        
        # Create left and right boundary curves
        left_curve = CubicBezier(*control_points_left)
        right_curve = CubicBezier(*control_points_right)
        
        # Create filled region between curves
        ribbon_path = VMobject()
        ribbon_path.set_points_as_corners([
            control_points_left[0],
            control_points_left[1],
            control_points_left[2],
            control_points_right[2],
            control_points_right[1],
            control_points_right[0],
            control_points_left[0]
        ])
        ribbon_path.set_fill(color, opacity=1.0)
        ribbon_path.set_stroke(color, width=0)
        
        ribbon_group.add(ribbon_path)
        ribbon_group.move_to(np.array([x_pos, self.ribbon_height / 2, 0]))
        
        return ribbon_group
    
    def _build_column(
        self,
        x_pos: float,
        color: ManimColor,
        header_text: str,
        phrases: list,
        column_name: str
    ) -> VGroup:
        """Build a complete column: ribbon + header + content."""
        column_group = VGroup()
        
        # Build ribbon
        ribbon = self._build_ribbon(x_pos, color)
        column_group.add(ribbon)
        
        # Build header
        header = Text(
            header_text,
            font_size=self.header_font_size,
            font="Girder 117",
            color=ManimColor("#FFFFFF"),
            weight="bold"
        )
        header.move_to(np.array([x_pos, self.ribbon_height + 0.5, 0]))
        column_group.add(header)
        
        # Build content phrases
        content_group = VGroup()
        y_start = self.ribbon_height * 0.6
        y_spacing = 0.5
        
        for i, phrase in enumerate(phrases):
            phrase_text = Text(
                phrase,
                font_size=self.content_font_size,
                font="Inter",
                color=ManimColor("#E0E7FF")
            )
            phrase_text.move_to(np.array([
                x_pos,
                y_start - i * y_spacing,
                0
            ]))
            content_group.add(phrase_text)
        
        column_group.add(content_group)
        
        # Store references for animation access
        setattr(self, f"column_{column_name}", column_group)
        setattr(self, f"ribbon_{column_name}", ribbon)
        setattr(self, f"header_{column_name}", header)
        setattr(self, f"content_{column_name}", content_group)
        
        return column_group
    
    def _build_asset(self):
        """Construct the complete three-column ribbon system."""
        # Build three columns
        col_left = self._build_column(
            -self.ribbon_spacing,
            self.color_left,
            "Selection",
            self.phrases_left,
            "left"
        )
        
        col_center = self._build_column(
            0,
            self.color_center,
            "Insight",
            self.phrases_center,
            "center"
        )
        
        col_right = self._build_column(
            self.ribbon_spacing,
            self.color_right,
            "Outcome",
            self.phrases_right,
            "right"
        )
        
        # Group all columns
        self.ribbons_group = VGroup(col_left, col_center, col_right)
        self.add(self.ribbons_group)
        
        # Build connection lines from top-center to column headers
        self.connectors_group = VGroup()
        
        connector_start = np.array([0, self.ribbon_height + 1.2, 0])
        
        for x_pos in [-self.ribbon_spacing, 0, self.ribbon_spacing]:
            connector_end = np.array([x_pos, self.ribbon_height + 0.5, 0])
            connector_line = Line(
                connector_start,
                connector_end,
                color=ManimColor("#FF9F1C"),
                stroke_width=2
            )
            self.connectors_group.add(connector_line)
        
        self.add(self.connectors_group)
        
        # System identifier (MySATHI mark placeholder)
        self.system_identifier = VGroup()
        identifier_mark = Circle(
            radius=0.3,
            color=ManimColor("#FF9F1C"),
            fill_opacity=0.3
        )
        identifier_mark.move_to(np.array([0, self.ribbon_height + 1.2, 0]))
        self.system_identifier.add(identifier_mark)
        self.add(self.system_identifier)
        
        # Master group for global transforms
        self.master_group = VGroup(
            self.ribbons_group,
            self.connectors_group,
            self.system_identifier
        )

        return self.master_group

    def get_subcomponent(self, position: str, component_type: str):
        """
        Access subcomponents by position and type.
        position: 'left', 'center', 'right'
        component_type: 'ribbon', 'header', 'content', 'column'
        """
        valid_positions = ["left", "center", "right"]
        valid_types = ["ribbon", "header", "content", "column"]
        
        if position not in valid_positions:
            raise ValueError(f"Position must be one of {valid_positions}")
        if component_type not in valid_types:
            raise ValueError(f"Component type must be one of {valid_types}")
            
        attr_name = f"{component_type}_{position}"
        return getattr(self, attr_name, None)
    
    def get_connector_group(self):
        return self.connectors_group

    def set_header_text(self, position: str, new_text: str):
        """Update the header text for a specific column."""
        old_header = self.get_subcomponent(position, "header")
        column = self.get_subcomponent(position, "column")
        
        if old_header and column:
            new_header = Text(
                new_text,
                font_size=self.header_font_size,
                font="Girder 117",
                color=old_header.color,
                weight="bold"
            )
            new_header.move_to(old_header.get_center())
            
            # Swap in the column VGroup
            column.remove(old_header)
            column.add(new_header)
            
            # Update reference
            setattr(self, f"header_{position}", new_header)

    def set_ribbon_color(self, position: str, color: str):
        """Update the color of a ribbon."""
        ribbon = self.get_subcomponent(position, "ribbon")
        if ribbon:
            c = ManimColor(color)
            ribbon.set_fill(c)
            ribbon.set_stroke(c)

    def animate_entry(self):
        """Returns an AnimationGroup for the standard entry of the asset."""
        return AnimationGroup(
            FadeIn(self.ribbons_group, shift=UP),
            Create(self.connectors_group),
            FadeIn(self.system_identifier, scale=0.5),
            lag_ratio=0.2
        )

    def animate_content_reveal(self, position: str):
        """Returns an animation to reveal content for a specific column."""
        content = self.get_subcomponent(position, "content")
        if content:
            return Write(content)
        return Wait(0.1)

    def animate_column_emphasis(self, position: str):
        """Returns an animation to emphasize a specific column."""
        column = self.get_subcomponent(position, "column")
        if column:
            return Indicate(column, scale_factor=1.05)
        return Wait(0.1)