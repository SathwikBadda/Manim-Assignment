from manim import *
import numpy as np

class SeedToTreeGrowth(Scene):
    def construct(self):
        # Set background color - soft sky blue
        self.camera.background_color = "#E8F5F7"
        
        # Create ground line
        ground = Line(
            start=LEFT * 7,
            end=RIGHT * 7,
            stroke_color="#8B7355",
            stroke_width=8
        ).shift(DOWN * 2.5)
        
        # Create shadow (stays on ground throughout)
        shadow = self.create_shadow()
        shadow.shift(DOWN * 2.4)
        
        # Add ground
        self.add(ground)
        
        # Create all stages
        seed = self.create_seed()
        seed.shift(DOWN * 2.2)
        
        sprout = self.create_sprout()
        sprout.shift(DOWN * 2.2)
        
        plant = self.create_plant()
        plant.shift(DOWN * 2.2)
        
        tree = self.create_tree()
        tree.shift(DOWN * 2.2)
        
        # ==================== STAGE 1: SEED ====================
        
        # Phase 1: Seed appears (drops from above)
        seed.shift(UP * 3)
        
        self.play(
            seed.animate.shift(DOWN * 3),
            FadeIn(shadow, scale=0.5),
            run_time=1.0,
            rate_func=smooth
        )
        
        # Seed settles (small bounce)
        self.play(
            seed.animate.shift(UP * 0.1),
            run_time=0.2
        )
        self.play(
            seed.animate.shift(DOWN * 0.1),
            run_time=0.2
        )
        
        self.wait(0.8)
        
        # Seed wiggles (germination starting)
        for _ in range(2):
            self.play(
                seed.animate.rotate(5 * DEGREES),
                run_time=0.2
            )
            self.play(
                seed.animate.rotate(-10 * DEGREES),
                run_time=0.2
            )
            self.play(
                seed.animate.rotate(5 * DEGREES),
                run_time=0.2
            )
        
        self.wait(0.5)
        
        # ==================== STAGE 2: SPROUT ====================
        
        # Phase 2: Transform to sprout
        sprout_shadow = self.create_shadow(width=0.8, height=0.25)
        sprout_shadow.shift(DOWN * 2.4)
        
        self.play(
            Transform(seed, sprout),
            Transform(shadow, sprout_shadow),
            run_time=2.0,
            rate_func=smooth
        )
        
        self.wait(0.8)
        
        # Sprout grows a bit more (stretches upward)
        self.play(
            seed.animate.scale([1, 1.2, 1]),
            run_time=1.0,
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # ==================== STAGE 3: SMALL PLANT ====================
        
        # Phase 3: Transform to plant
        plant_shadow = self.create_shadow(width=1.5, height=0.3)
        plant_shadow.shift(DOWN * 2.4)
        
        self.play(
            Transform(seed, plant),
            Transform(shadow, plant_shadow),
            run_time=2.5,
            rate_func=smooth
        )
        
        self.wait(0.8)
        
        # Plant grows (stretches taller)
        self.play(
            seed.animate.scale([1, 1.15, 1]),
            run_time=1.2,
            rate_func=smooth
        )
        
        self.wait(0.5)
        
        # ==================== STAGE 4: TREE ====================
        
        # Phase 4: Transform to tree
        tree_shadow = self.create_shadow(width=3.5, height=0.45)
        tree_shadow.shift(DOWN * 2.4)
        
        self.play(
            Transform(seed, tree),
            Transform(shadow, tree_shadow),
            run_time=3.0,
            rate_func=smooth
        )
        
        self.wait(1.0)
        
        # Phase 5: Tree sways gently
        for _ in range(2):
            self.play(
                seed.animate.rotate(3 * DEGREES, about_point=seed.get_bottom() + DOWN * 0.1),
                run_time=1.0,
                rate_func=smooth
            )
            self.play(
                seed.animate.rotate(-6 * DEGREES, about_point=seed.get_bottom() + DOWN * 0.1),
                run_time=1.5,
                rate_func=smooth
            )
            self.play(
                seed.animate.rotate(3 * DEGREES, about_point=seed.get_bottom() + DOWN * 0.1),
                run_time=1.0,
                rate_func=smooth
            )
        
        self.wait(2)
    
    def create_shadow(self, width=0.6, height=0.2):
        """
        Creates a soft ground shadow using an ellipse.
        
        Args:
            width: Shadow width
            height: Shadow height (flattened)
        
        Returns:
            Ellipse object representing shadow
        """
        shadow = Ellipse(
            width=width,
            height=height,
            fill_color=BLACK,
            fill_opacity=0.15,
            stroke_width=0
        )
        return shadow
    
    def create_seed(self):
        """
        Creates a seed using an ellipse.
        
        Returns:
            VGroup containing seed shape
        """
        # Colors
        SEED_BROWN = "#8B6F47"
        SEED_DARK = "#6B5537"
        
        # Main seed body - small oval
        seed_body = Ellipse(
            width=0.4,
            height=0.5,
            fill_color=SEED_BROWN,
            fill_opacity=1,
            stroke_color=SEED_DARK,
            stroke_width=3
        )
        
        # Seed texture line
        seed_line = Arc(
            radius=0.25,
            start_angle=-PI/3,
            angle=2*PI/3,
            stroke_color=SEED_DARK,
            stroke_width=2
        )
        
        # Small highlight
        highlight = Ellipse(
            width=0.12,
            height=0.15,
            fill_color=WHITE,
            fill_opacity=0.3,
            stroke_width=0
        ).shift(LEFT * 0.08 + UP * 0.1)
        
        seed_group = VGroup(seed_body, seed_line, highlight)
        return seed_group
    
    def create_sprout(self):
        """
        Creates a sprout with curved stem and two small leaves.
        
        Returns:
            VGroup containing sprout parts
        """
        # Colors
        STEM_GREEN = "#7BC043"
        LEAF_GREEN = "#5FA52F"
        SEED_BROWN = "#8B6F47"
        OUTLINE = "#4A7C2F"
        
        # Seed remains at bottom
        seed_remnant = Ellipse(
            width=0.35,
            height=0.4,
            fill_color=SEED_BROWN,
            fill_opacity=0.8,
            stroke_color="#6B5537",
            stroke_width=2
        ).shift(DOWN * 0.1)
        
        # Stem - curved line growing upward
        stem = Arc(
            radius=1.5,
            start_angle=-PI/2,
            angle=PI/6,
            stroke_color=STEM_GREEN,
            stroke_width=6
        ).shift(DOWN * 0.1 + RIGHT * 1.5)
        
        # Left leaf - small ellipse
        left_leaf = Ellipse(
            width=0.3,
            height=0.5,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(40 * DEGREES).shift(LEFT * 0.25 + UP * 0.6)
        
        # Right leaf - small ellipse
        right_leaf = Ellipse(
            width=0.3,
            height=0.5,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-40 * DEGREES).shift(RIGHT * 0.2 + UP * 0.8)
        
        # Leaf veins
        left_vein = Line(
            start=LEFT * 0.25 + UP * 0.5,
            end=LEFT * 0.25 + UP * 0.7,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        
        right_vein = Line(
            start=RIGHT * 0.2 + UP * 0.7,
            end=RIGHT * 0.2 + UP * 0.9,
            stroke_color=OUTLINE,
            stroke_width=1.5
        )
        
        sprout_group = VGroup(
            seed_remnant,
            stem,
            left_leaf,
            right_leaf,
            left_vein,
            right_vein
        )
        
        return sprout_group
    
    def create_plant(self):
        """
        Creates a small plant with thicker stem and larger leaves.
        
        Returns:
            VGroup containing plant parts
        """
        # Colors
        STEM_GREEN = "#6DAE3C"
        LEAF_GREEN = "#5FA52F"
        LEAF_LIGHT = "#7BC043"
        OUTLINE = "#4A7C2F"
        
        # Thicker stem - straight line
        stem = RoundedRectangle(
            width=0.25,
            height=2.0,
            corner_radius=0.12,
            fill_color=STEM_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        )
        
        # Left leaves (2 pairs)
        left_leaf1 = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(50 * DEGREES).shift(LEFT * 0.55 + UP * 0.3)
        
        left_leaf2 = Ellipse(
            width=0.45,
            height=0.7,
            fill_color=LEAF_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(60 * DEGREES).shift(LEFT * 0.6 + UP * 0.8)
        
        # Right leaves (2 pairs)
        right_leaf1 = Ellipse(
            width=0.5,
            height=0.8,
            fill_color=LEAF_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-50 * DEGREES).shift(RIGHT * 0.55 + UP * 0.5)
        
        right_leaf2 = Ellipse(
            width=0.45,
            height=0.7,
            fill_color=LEAF_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).rotate(-60 * DEGREES).shift(RIGHT * 0.6 + UP * 1.0)
        
        # Leaf veins
        veins = VGroup()
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
            veins.add(vein)
        
        plant_group = VGroup(
            stem,
            left_leaf1,
            left_leaf2,
            right_leaf1,
            right_leaf2,
            veins
        )
        
        return plant_group
    
    def create_tree(self):
        """
        Creates a tree with trunk and leafy canopy.
        
        Returns:
            VGroup containing tree parts
        """
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
        
        trunk = Polygon(
            *trunk_points,
            fill_color=TRUNK_BROWN,
            fill_opacity=1,
            stroke_color=TRUNK_DARK,
            stroke_width=4
        ).round_corners(radius=0.15)
        
        # Trunk texture - vertical lines
        trunk_lines = VGroup()
        for x_offset in [-0.15, 0, 0.15]:
            line = Line(
                start=x_offset * RIGHT + UP * 0.2,
                end=x_offset * RIGHT + UP * 2.3,
                stroke_color=TRUNK_DARK,
                stroke_width=2,
                stroke_opacity=0.5
            )
            trunk_lines.add(line)
        
        # Canopy - multiple overlapping circles
        # Center large circle
        canopy_center = Circle(
            radius=1.2,
            fill_color=CANOPY_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(UP * 3.2)
        
        # Left circles
        canopy_left1 = Circle(
            radius=0.9,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(LEFT * 0.9 + UP * 2.8)
        
        canopy_left2 = Circle(
            radius=0.7,
            fill_color=CANOPY_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 1.3 + UP * 3.5)
        
        # Right circles
        canopy_right1 = Circle(
            radius=0.9,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=3
        ).shift(RIGHT * 0.9 + UP * 2.8)
        
        canopy_right2 = Circle(
            radius=0.7,
            fill_color=CANOPY_DARK,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 1.3 + UP * 3.5)
        
        # Top circles
        canopy_top1 = Circle(
            radius=0.75,
            fill_color=CANOPY_GREEN,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(UP * 4.0)
        
        canopy_top2 = Circle(
            radius=0.6,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(LEFT * 0.5 + UP * 3.8)
        
        canopy_top3 = Circle(
            radius=0.6,
            fill_color=CANOPY_LIGHT,
            fill_opacity=1,
            stroke_color=OUTLINE,
            stroke_width=2
        ).shift(RIGHT * 0.5 + UP * 3.8)
        
        # Group all parts - order matters for layering
        tree_group = VGroup(
            trunk,
            trunk_lines,
            canopy_left1,
            canopy_right1,
            canopy_left2,
            canopy_right2,
            canopy_center,
            canopy_top2,
            canopy_top3,
            canopy_top1
        )
        
        return tree_group


