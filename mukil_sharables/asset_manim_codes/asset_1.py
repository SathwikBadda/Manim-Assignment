from manim import *
import numpy as np

class asset_1(VGroup):
    def __init__(
        self,
        num_steps: int = 4,
        step_height: float = 1.8,
        platform_width: float = 1.5,
        platform_thickness: float = 0.08,
        riser_thickness: float = 0.06,
        primary_text_color: str = "#0B2A5B",
        primary_accent_color: str = "#F4B400",
        baseline_length: float = 0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.num_steps = num_steps
        self.step_height = step_height
        self.platform_width = platform_width
        self.platform_thickness = platform_thickness
        self.riser_thickness = riser_thickness
        self.primary_text_color = ManimColor(primary_text_color)
        self.primary_accent_color = ManimColor(primary_accent_color)
        self.baseline_length = baseline_length
        
        # Exposed structural groups
        self.baseline = None
        self.platforms = VGroup()
        self.risers = VGroup()
        self.steps_group = VGroup()
        self.staircase_group = VGroup()
        
        # Storage for individual platform references
        self.platform_list = []
        self.riser_list = []
        
        self._build_staircase()
    
    def _build_staircase(self):
        """Construct the complete staircase structure."""
        
        # Build baseline
        self.baseline = Line(
            start=ORIGIN,
            end=RIGHT * self.baseline_length,
            color=self.primary_text_color,
            stroke_width=2
        )
        
        # Build steps sequentially
        current_x = 0
        current_y = 0
        
        for step_index in range(self.num_steps):
            # Platform rectangle
            platform = Rectangle(
                width=self.platform_width,
                height=self.platform_thickness,
                fill_color=self.primary_text_color,
                fill_opacity=1,
                stroke_width=0
            )
            platform.move_to(np.array([current_x + self.platform_width / 2, current_y, 0]))
            
            # Store platform with semantic name
            platform_name = f"step_{step_index + 1}_platform"
            setattr(self, platform_name, platform)
            self.platform_list.append(platform)
            self.platforms.add(platform)
            
            # Riser line (vertical connector to next platform)
            if step_index < self.num_steps - 1:
                riser_start = np.array([current_x + self.platform_width, current_y, 0])
                riser_end = np.array([current_x + self.platform_width, current_y + self.step_height, 0])
                
                riser = Line(
                    start=riser_start,
                    end=riser_end,
                    color=self.primary_accent_color,
                    stroke_width=2
                )
                
                riser_name = f"riser_{step_index + 1}_to_{step_index + 2}"
                setattr(self, riser_name, riser)
                self.riser_list.append(riser)
                self.risers.add(riser)
            
            # Update position for next step
            current_x += self.platform_width
            current_y += self.step_height
        
        # Assemble steps group
        self.steps_group.add(self.platforms, self.risers)
        
        # Assemble master staircase group
        self.staircase_group.add(self.baseline, self.steps_group)
        
        # Add to self
        self.add(self.staircase_group)
    
    def get_platform_at_step(self, step_index: int):
        """
        Retrieve the platform at a specific step (0-indexed).
        Returns the platform VGroup or None if out of bounds.
        """
        if 0 <= step_index < len(self.platform_list):
            return self.platform_list[step_index]
        return None
    
    def get_riser_between_steps(self, step_from: int, step_to: int):
        """
        Retrieve the riser connecting two steps (0-indexed).
        Returns the riser Line or None if out of bounds.
        """
        if step_from < step_to and step_to < self.num_steps:
            riser_index = step_from
            if 0 <= riser_index < len(self.riser_list):
                return self.riser_list[riser_index]
        return None
    
    def get_platform_center(self, step_index: int):
        """
        Get the center position of a platform at a specific step.
        Useful for positioning characters on platforms.
        """
        platform = self.get_platform_at_step(step_index)
        if platform:
            return platform.get_center()
        return None
    
    def highlight_platform(self, step_index: int, highlight_color: str):
        """
        Returns an animation to highlight a platform.
        """
        platform = self.get_platform_at_step(step_index)
        if platform:
            return platform.animate.set_color(ManimColor(highlight_color))
        return Wait(0.1)
    
    def highlight_riser(self, step_from: int, step_to: int, highlight_color: str):
        """
        Returns an animation to highlight a riser.
        """
        riser = self.get_riser_between_steps(step_from, step_to)
        if riser:
            return riser.animate.set_color(ManimColor(highlight_color))
        return Wait(0.1)