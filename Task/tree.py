from manim import *
import numpy as np

class Seed(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seed_body = None
        self.seed_line = None
        self.highlight = None
        self._build_parts()

    def _build_parts(self):
        # Colors
        SEED_BROWN = "#8B6F47"
        SEED_DARK = "#6B5537"
        
        # Main seed body - small oval
        self.seed_body = Ellipse(
            width=0.4,
            height=0.5,
            fill_color=SEED_BROWN,
            fill_opacity=1,
            stroke_color=SEED_DARK,
            stroke_width=3
        )
        
        # Seed texture line
        self.seed_line = Arc(
            radius=0.25,
            start_angle=-PI/3,
            angle=2*PI/3,
            stroke_color=SEED_DARK,
            stroke_width=2
        )
        
        # Small highlight
        self.highlight = Ellipse(
            width=0.12,
            height=0.15,
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_width=0
        ).shift(LEFT * 0.08 + UP * 0.1)
        
        self.add(self.seed_body, self.seed_line, self.highlight)

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Seed")

    def set_color(self, part_name: str, color: str):
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     opacity = 0.3 if part_name == "highlight" else 1
                     component.set_fill(c, opacity=opacity)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)

class Sprout(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seed_remnant = None
        self.stem = None
        self.left_leaf = None
        self.right_leaf = None
        self.left_vein = None
        self.right_vein = None
        self._build_parts()

    def _build_parts(self):
        # Colors
        STEM_GREEN = "#7BC043"
        LEAF_GREEN = "#5FA52F"
        SEED_BROWN = "#8B6F47"
        OUTLINE = "#4A7C2F"
        
        # Seed remains at bottom
        self.seed_remnant = Ellipse(
            width=0.35,
            height=0.4,
            fill_color=SEED_BROWN,
            fill_opacity=0.8,
            stroke_color="#6B5537",
            stroke_width=2
        ).shift(DOWN * 0.1)
        
        # Stem - curved line growing upward
        self.stem = Arc(
            radius=1.5,
            start_angle=-PI/2,
            angle=PI/6,
            stroke_color=STEM_GREEN,
            stroke_width=6
        ).shift(DOWN * 0.1 + RIGHT * 1.5)
        
        # Left leaf - small ellipse
        self.left_leaf = Ellipse(
            width=0.3,
            height=0.5,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(40 * DEGREES).shift(LEFT * 0.25 + UP * 0.6)
        
        # Right leaf - small ellipse
        self.right_leaf = Ellipse(
            width=0.3,
            height=0.5,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-40 * DEGREES).shift(RIGHT * 0.2 + UP * 0.8)
        
        # Leaf veins
        self.left_vein = Line(
            start=LEFT * 0.25 + UP * 0.5,
            end=LEFT * 0.25 + UP * 0.7,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        
        self.right_vein = Line(
            start=RIGHT * 0.2 + UP * 0.7,
            end=RIGHT * 0.2 + UP * 0.9,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        
        self.add(
            self.seed_remnant,
            self.stem,
            self.left_leaf,
            self.right_leaf,
            self.left_vein,
            self.right_vein
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Sprout")

    def set_color(self, part_name: str, color: str):
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1 if part_name != 'seed_remnant' else 0.8)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)

class Plant(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stem = None
        self.left_leaf1 = None
        self.left_leaf2 = None
        self.right_leaf1 = None
        self.right_leaf2 = None
        self.veins = None
        self._build_parts()

    def _build_parts(self):
        # Colors
        STEM_GREEN = "#6DAE3C"
        LEAF_GREEN = "#5FA52F"
        LEAF_LIGHT = "#7BC043"
        OUTLINE = "#4A7C2F"
        
        # Thicker stem - straight line
        self.stem = RoundedRectangle(
            width=0.25,
            height=2.0,
            corner_radius=0.12,
            fill_color=STEM_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        )
        
        # Left leaves (2 pairs)
        self.left_leaf1 = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(50 * DEGREES).shift(LEFT * 0.55 + UP * 0.3)
        
        self.left_leaf2 = Ellipse(
            width=0.45,
            height=0.7,
            fill_color=LEAF_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(60 * DEGREES).shift(LEFT * 0.6 + UP * 0.8)
        
        # Right leaves (2 pairs)
        self.right_leaf1 = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-50 * DEGREES).shift(RIGHT * 0.55 + UP * 0.5)
        
        self.right_leaf2 = Ellipse(
            width=0.45,
            height=0.7,
            fill_color=LEAF_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-60 * DEGREES).shift(RIGHT * 0.6 + UP * 1.0)
        
        # Leaf veins
        self.veins = VGroup()
        vein_positions = [
            (LEFT * 0.55 + UP * 0.3, LEFT * 0.6 + UP * 0.4),
            (LEFT * 0.6 + UP * 0.8, LEFT * 0.65 + UP * 0.9),
            (RIGHT * 0.55 + UP * 0.5, RIGHT * 0.6 + UP * 0.6),
            (RIGHT * 0.6 + UP * 1.0, RIGHT * 0.65 + UP * 1.1)
        ]
        
        for start, end in vein_positions:
            vein = Line(
                start=start,
                end=end,
                stroke_color=OUTLINE,
                stroke_width=1.5
            )
            self.veins.add(vein)
        
        self.add(
            self.stem,
            self.left_leaf1,
            self.left_leaf2,
            self.right_leaf1,
            self.right_leaf2,
            self.veins
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Plant")

    def set_color(self, part_name: str, color: str):
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)

class Tree(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trunk = None
        self.trunk_lines = None
        self.canopy_center = None
        self.canopy_left1 = None
        self.canopy_left2 = None
        self.canopy_right1 = None
        self.canopy_right2 = None
        self.canopy_top1 = None
        self.canopy_top2 = None
        self.canopy_top3 = None
        self._build_parts()

    def _build_parts(self):
        # Colors
        TRUNK_BROWN = "#8B6F47"
        TRUNK_DARK = "#6B5537"
        CANOPY_GREEN = "#5FA52F"
        CANOPY_LIGHT = "#7BC043"
        CANOPY_DARK = "#4A7C2F"
        OUTLINE = "#3D6225"
        
        # Trunk - tapered rounded rectangle
        trunk_points = [
            LEFT * 0.4 + DOWN * 0.1,
            LEFT * 0.25 + UP * 2.5,
            RIGHT * 0.25 + UP * 2.5,
            RIGHT * 0.4 + DOWN * 0.1,
        ]
        
        self.trunk = Polygon(
            *trunk_points,
            fill_color=TRUNK_BROWN,
            fill_opacity=1,
            stroke_color=TRUNK_DARK,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Trunk texture - vertical lines
        self.trunk_lines = VGroup()
        for x_offset in [-0.15, 0, 0.15]:
            line = Line(
                start=x_offset * RIGHT + UP * 0.2,
                end=x_offset * RIGHT + UP * 2.3,
                stroke_color=TRUNK_DARK,
                stroke_width=2,
                stroke_opacity=0.5
            )
            self.trunk_lines.add(line)
        
        # Canopy - multiple overlapping circles
        # Center large circle
        self.canopy_center = Circle(
            radius=1.2,
            fill_color=CANOPY_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(UP * 3.2)
        
        # Left circles
        self.canopy_left1 = Circle(
            radius=0.9,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(LEFT * 0.9 + UP * 2.8)
        
        self.canopy_left2 = Circle(
            radius=0.7,
            fill_color=CANOPY_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 1.3 + UP * 3.5)
        
        # Right circles
        self.canopy_right1 = Circle(
            radius=0.9,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(RIGHT * 0.9 + UP * 2.8)
        
        self.canopy_right2 = Circle(
            radius=0.7,
            fill_color=CANOPY_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 1.3 + UP * 3.5)
        
        # Top circles
        self.canopy_top1 = Circle(
            radius=0.75,
            fill_color=CANOPY_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(UP * 4.0)
        
        self.canopy_top2 = Circle(
            radius=0.6,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.5 + UP * 3.8)
        
        self.canopy_top3 = Circle(
            radius=0.6,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.5 + UP * 3.8)
        
        # Group all parts - order matters for layering
        self.add(
            self.trunk,
            self.trunk_lines,
            self.canopy_left1,
            self.canopy_right1,
            self.canopy_left2,
            self.canopy_right2,
            self.canopy_center,
            self.canopy_top2,
            self.canopy_top3,
            self.canopy_top1
        )

    def get_subcomponent(self, part_name: str):
        if hasattr(self, part_name):
            return getattr(self, part_name)
        raise ValueError(f"Part name {part_name} not found in Tree")

    def set_color(self, part_name: str, color: str):
        component = self.get_subcomponent(part_name)
        if component:
            c = ManimColor(color)
            if isinstance(component, VMobject):
                component.set_color(c)
                if component.get_fill_opacity() > 0:
                     component.set_fill(c, opacity=1)

    def animate_manipulation(self, part_name: str, animation_type: str = "Indicate", **kwargs):
        component = self.get_subcomponent(part_name)
        if not component:
             return Wait(0.1)
             
        if animation_type == "Indicate":
            return Indicate(component, **kwargs)
        elif animation_type == "Wiggle":
            return Wiggle(component, **kwargs)
        elif animation_type == "Flash":
            return Flash(component, **kwargs)
        else:
            return Wait(0.1)
