from manim import *
import numpy as np

class SpeechBubble(VGroup):
    def __init__(
        self,
        width: float = 2.0,
        height: float = 1.2,
        corner_radius: float = 0.1,
        pointer_length: float = 0.3,
        pointer_direction: str = "down_left",
        text_padding: float = 0.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.bubble_width = width
        self.bubble_height = height
        self.corner_radius = corner_radius
        self.pointer_length = pointer_length
        self.pointer_direction = pointer_direction
        self.text_padding = text_padding
        
        # Primary Accent color
        self.accent_color = ManimColor("#F4B400")
        
        # Subcomponents
        self.body = None
        self.pointer = None
        self.body_and_pointer_group = VGroup()
        self.text_container = None
        self.connector_point = None
        
        self._build_parts()
        
    def _build_parts(self):
        # Create body (rounded rectangle)
        self.body = RoundedRectangle(
            width=self.bubble_width,
            height=self.bubble_height,
            corner_radius=self.corner_radius,
            fill_color=self.accent_color,
            fill_opacity=1,
            stroke_color=self.accent_color,
            stroke_width=2
        )
        self.body.move_to(ORIGIN)
        
        # Create pointer based on direction
        pointer_base_width = self.bubble_width * 0.25
        
        if self.pointer_direction == "down_left":
            # Triangle pointing down-left from bottom-left of body
            bottom_left = self.body.get_corner(DOWN + LEFT)
            anchor_point = bottom_left + RIGHT * (self.bubble_width * 0.2)
            pointer_points = [
                anchor_point,
                anchor_point + LEFT * (pointer_base_width / 2),
                anchor_point + RIGHT * (pointer_base_width / 2),
                anchor_point + DOWN * self.pointer_length
            ]
            self.connector_point = anchor_point + DOWN * self.pointer_length
            
        elif self.pointer_direction == "down_right":
            # Triangle pointing down-right from bottom-right of body
            bottom_right = self.body.get_corner(DOWN + RIGHT)
            anchor_point = bottom_right + LEFT * (self.bubble_width * 0.2)
            pointer_points = [
                anchor_point,
                anchor_point + LEFT * (pointer_base_width / 2),
                anchor_point + RIGHT * (pointer_base_width / 2),
                anchor_point + DOWN * self.pointer_length
            ]
            self.connector_point = anchor_point + DOWN * self.pointer_length
            
        elif self.pointer_direction == "down":
            # Triangle pointing straight down from bottom center of body
            bottom_center = self.body.get_bottom()
            anchor_point = bottom_center
            pointer_points = [
                anchor_point,
                anchor_point + LEFT * (pointer_base_width / 2),
                anchor_point + RIGHT * (pointer_base_width / 2),
                anchor_point + DOWN * self.pointer_length
            ]
            self.connector_point = anchor_point + DOWN * self.pointer_length
            
        elif self.pointer_direction == "left":
            # Triangle pointing left from left edge of body
            left_center = self.body.get_left()
            anchor_point = left_center
            pointer_height = self.bubble_height * 0.2
            pointer_points = [
                anchor_point,
                anchor_point + UP * pointer_height,
                anchor_point + DOWN * pointer_height,
                anchor_point + LEFT * self.pointer_length
            ]
            self.connector_point = anchor_point + LEFT * self.pointer_length
            
        elif self.pointer_direction == "right":
            # Triangle pointing right from right edge of body
            right_center = self.body.get_right()
            anchor_point = right_center
            pointer_height = self.bubble_height * 0.2
            pointer_points = [
                anchor_point,
                anchor_point + UP * pointer_height,
                anchor_point + DOWN * pointer_height,
                anchor_point + RIGHT * self.pointer_length
            ]
            self.connector_point = anchor_point + RIGHT * self.pointer_length
        else:
            # Default: down_left
            bottom_left = self.body.get_corner(DOWN + LEFT)
            anchor_point = bottom_left + RIGHT * (self.bubble_width * 0.2)
            pointer_points = [
                anchor_point,
                anchor_point + LEFT * (pointer_base_width / 2),
                anchor_point + RIGHT * (pointer_base_width / 2),
                anchor_point + DOWN * self.pointer_length
            ]
            self.connector_point = anchor_point + DOWN * self.pointer_length
        
        self.pointer = Polygon(
            *pointer_points,
            fill_color=self.accent_color,
            fill_opacity=1,
            stroke_color=self.accent_color,
            stroke_width=2
        )
        
        # Group body and pointer
        self.body_and_pointer_group.add(self.body, self.pointer)
        
        # Create text container (invisible rectangle for text layout)
        self.text_container = Rectangle(
            width=self.bubble_width - 2 * self.text_padding,
            height=self.bubble_height - 2 * self.text_padding,
            fill_opacity=0,
            stroke_opacity=0
        )
        self.text_container.move_to(self.body.get_center())
        
        # Add all components to self
        self.add(self.body_and_pointer_group, self.text_container)
        
    def get_body(self) -> VGroup:
        """Return the body group (rounded rectangle)."""
        return self.body_and_pointer_group
    
    def get_pointer(self) -> VMobject:
        """Return the pointer triangle."""
        return self.pointer
    
    def get_text_anchor(self, anchor_name: str = "center") -> np.ndarray:
        """
        Return a position anchor within the text container.
        anchor_name: 'center', 'top_left', 'top_center', 'top_right',
                     'center_left', 'center_right',
                     'bottom_left', 'bottom_center', 'bottom_right'
        """
        anchor_map = {
            "center": self.text_container.get_center,
            "top_left": self.text_container.get_top_left,
            "top_center": self.text_container.get_top,
            "top_right": self.text_container.get_top_right,
            "center_left": self.text_container.get_left,
            "center_right": self.text_container.get_right,
            "bottom_left": self.text_container.get_bottom_left,
            "bottom_center": self.text_container.get_bottom,
            "bottom_right": self.text_container.get_bottom_right,
        }
        
        if anchor_name in anchor_map:
            return anchor_map[anchor_name]()
        else:
            return self.text_container.get_center()
    
    def get_connector_point(self) -> np.ndarray:
        """Return the connector point (pointer apex or body anchor)."""
        return self.connector_point
    
    def set_color(self, color: str):
        """Set the color of body and pointer."""
        c = ManimColor(color)
        self.body.set_fill(c, opacity=1)
        self.body.set_stroke(c, width=2)
        self.pointer.set_fill(c, opacity=1)
        self.pointer.set_stroke(c, width=2)