from manim import *
import numpy as np

class Buddy4StudyImpactDashboard(MovingCameraScene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#1E3A8A"
        
        # SECTION 1: Logo Anchor Container
        logo_container = self.create_logo_container()
        
        # SECTION 2: Logo Entry Animation
        self.animate_logo_entry(logo_container)
        
        # SECTION 3: Curved Growth Lines
        curves = self.create_growth_curves()
        self.play(*[Create(curve, run_time=0.5, rate_func=smooth) for curve in curves]) # Faster
        
        # SECTION 4: Icon Terminals
        icons = self.create_icons(curves)
        self.animate_icons(icons, curves)
        
        self.wait(0.1) 
        
        # SECTION 5: Camera Transition
        self.play(
            self.camera.frame.animate.shift(UP * 6.5).set(height=10.5), 
            run_time=0.8, # Faster Transition
            rate_func=smooth
        )
        
        # Fade curves and icons slightly but keep lines visible
        fade_anims = []
        for curve in curves:
            fade_anims.append(curve.animate.set_stroke(opacity=0.6))
        self.play(*fade_anims, run_time=0.3)
        
        # SECTION 6: Dashboard Cards
        cards = self.create_dashboard_cards()
        self.animate_dashboard_cards(cards)
        
        # SECTION 7: Ambient Motion
        self.apply_ambient_motion(cards, logo_container)
        
        self.wait(7) # Increased final wait (added ~2s saved from start)
    
    def create_logo_container(self):
        # White rounded rectangle
        rect = RoundedRectangle(
            width=3.5,
            height=2.2,
            corner_radius=0.25,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        rect.move_to(np.array([0, -2.8, 0]))
        
        # Try to load logo SVG, fallback to text
        logo = SVGMobject("logo.svg")
        logo.scale_to_fit_width(2.8)
        logo.scale_to_fit_height(1.6)
        logo.move_to(rect.get_center())
        
        logo_group = VGroup(rect, logo)
        return logo_group
    
    def animate_logo_entry(self, logo_container):
        logo_container.scale(0.85)

        self.play(
            FadeIn(logo_container),
            logo_container.animate.scale(1 / 0.85),
            run_time=0.3, # Faster
            rate_func=smooth
        )
        
        # Breathing effect
        self.play(
            logo_container.animate.scale(1.02),
            rate_func=there_and_back,
            run_time=0.5 # Faster
        )
    
    def create_growth_curves(self):
        start_point = np.array([0, -1.6, 0])
        
        endpoints = [
            np.array([-4.5, 2.5, 0]),
            np.array([-3.0, 3.0, 0]),
            np.array([-1.5, 3.2, 0]),
            np.array([1.5, 3.2, 0]),
            np.array([3.0, 3.0, 0]),
            np.array([4.5, 2.5, 0])
        ]
        
        curves = []
        for i, endpoint in enumerate(endpoints):
            # Calculate control points for smooth symmetric arcs
            direction = endpoint - start_point
            mid_point = (start_point + endpoint) / 2
            
            # Create upward arcing control points
            control1 = start_point + direction * 0.3 + UP * 1.2
            control2 = endpoint - direction * 0.3 + UP * 1.5
            
            curve = CubicBezier(
                start_point,
                control1,
                control2,
                endpoint,
                stroke_width=1.5,
                color="#E0E0E0",
                stroke_opacity=1.0
            )
            curves.append(curve)
        
        return curves
    
    def create_institution_icon(self):
        """Create institution/building icon"""
        # Base
        # Classical building (Greek Temple) - Refined
        
        # 1. Base (Stepped)
        base_bottom = Rectangle(width=0.55, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        base_top = Rectangle(width=0.50, height=0.03, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        base_bottom.move_to(DOWN * 0.22)
        base_top.next_to(base_bottom, UP, buff=0)
        
        # 2. Columns (4 pillars)
        # Evenly spaced
        col_width = 0.05
        col_height = 0.22
        columns = VGroup(*[
            Rectangle(width=col_width, height=col_height, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            for _ in range(4)
        ])
        columns.arrange(RIGHT, buff=0.08) # 3 gaps of 0.08 + 4 widths of 0.05 = 0.24 + 0.2 = 0.44 width (fits on 0.50 base)
        columns.next_to(base_top, UP, buff=0)
        
        # 3. Capital (Top of columns)
        capital = Rectangle(width=0.50, height=0.04, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        capital.next_to(columns, UP, buff=0)
        
        # 4. Roof (Pediment - Triangle)
        roof = Polygon(
            capital.get_corner(UL) + LEFT * 0.04,
            capital.get_top() + UP * 0.16,
            capital.get_corner(UR) + RIGHT * 0.04,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        
        icon = VGroup(base_bottom, base_top, columns, capital, roof)
        return icon
    
    def create_location_icon(self):
        """Create map pin/location icon"""
        # Main pin shape - Teardrop
        # Use a smooth connection between circle and triangle
        
        # Scale everything down to fit inside the parent circle (radius 0.3)
        # Target height ~0.4 (reduced to ~0.35)
        
        pin_radius = 0.10 # Reduced from 0.12
        pin_circle = Circle(radius=pin_radius, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        pin_circle.move_to(UP * 0.06)
        
        # Triangle for the point
        triangle = Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0)
        # Make the triangle narrower to blend with the circle
        triangle.stretch_to_fit_width(pin_radius * 1.8) 
        triangle.stretch_to_fit_height(pin_radius * 2.0)
        triangle.rotate(PI)
        triangle.move_to(pin_circle.get_center() + DOWN * 0.10)
        
        # Union to merge them
        pin_body = Union(pin_circle, triangle)
        pin_body.set_fill(WHITE, 1)
        pin_body.set_stroke(width=0)
        
        # Use Difference to cut a HOLE
        hole = Circle(radius=0.04, fill_color=BLACK, fill_opacity=1, stroke_width=0) 
        hole.move_to(pin_circle.get_center())
        
        # Create the final icon with hole cut out
        icon = Difference(pin_body, hole)
        icon.set_fill(WHITE, 1)
        icon.set_stroke(width=0)
        
        # Center the icon visually
        icon.move_to(ORIGIN)
        
        # Manually shift down slightly if it feels top heavy
        icon.shift(DOWN * 0.02)
        
        return icon
    
    def create_graduation_cap_icon(self):
        # 1. The Cap Top (Rhombus/Mortarboard) - Wide diamond
        # Reference shows a wide perspective
        top_diamond = Polygon(
            UP * 0.12, RIGHT * 0.35, DOWN * 0.12, LEFT * 0.35,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        top_diamond.shift(UP * 0.1) # Shift up slightly to make room for cap
        
        # 2. The Skull Cap (Cylindrical base)
        # Construct a cylinder shape: Rectangle body + Ellipical bottom
        
        cap_width = 0.28
        cap_height = 0.18
        
        # Main body (Rectangle)
        cap_rect = Rectangle(width=cap_width, height=cap_height, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        
        # Bottom curve (Ellipse)
        cap_bottom = Ellipse(width=cap_width, height=0.08, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        cap_bottom.move_to(cap_rect.get_bottom())
        
        # Merge them
        skull_cap = Union(cap_rect, cap_bottom)
        skull_cap.set_fill(WHITE, 1)
        skull_cap.set_stroke(width=0)
        
        # Position underneath the diamond
        # The top of the skull cap should be hidden by the diamond
        skull_cap.move_to(top_diamond.get_center() + DOWN * 0.12)
        
        # 3. Tassel
        center_point = top_diamond.get_center()
        right_corner = top_diamond.get_vertices()[1]
        
        # Bezier curve for natural hang
        tassel_string = CubicBezier(
            center_point,
            center_point + RIGHT * 0.15,
            right_corner + UP * 0.05 + LEFT * 0.05,
            right_corner + DOWN * 0.02,
            color=WHITE, stroke_width=2
        )
        
        tassel_hang = Line(tassel_string.get_end(), tassel_string.get_end() + DOWN * 0.18, color=WHITE, stroke_width=2)
        tassel_knot = Circle(radius=0.02, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(center_point)
        tassel_end = Circle(radius=0.03, fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(tassel_hang.get_end())
        
        icon = VGroup(skull_cap, top_diamond, tassel_string, tassel_hang, tassel_knot, tassel_end)
        
        # Center the icon
        icon.move_to(ORIGIN)
        return icon
    
    def create_icons(self, curves):
        icons = []
        
        # Icon 1: Rupee symbol
        endpoint = curves[0].get_end()
        circle1 = Circle(radius=0.3, fill_color="#FF6B35", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle1.move_to(endpoint)
        icon_text1 = Text("₹", font_size=32, color=WHITE, weight=BOLD)
        icon_text1.move_to(circle1.get_center())
        icon1 = VGroup(circle1, icon_text1)
        icons.append(icon1)
        
        # Icon 2: Graduation cap
        endpoint = curves[1].get_end()
        circle2 = Circle(radius=0.3, fill_color="#4A90E2", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle2.move_to(endpoint)
        cap_icon = self.create_graduation_cap_icon()
        cap_icon.scale(0.7)
        cap_icon.move_to(circle2.get_center())
        icon2 = VGroup(circle2, cap_icon)
        icons.append(icon2)
        
        # Icon 3: Institution building
        endpoint = curves[2].get_end()
        circle3 = Circle(radius=0.3, fill_color="#50C878", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle3.move_to(endpoint)
        building_icon = self.create_institution_icon()
        building_icon.scale(0.8)
        building_icon.move_to(circle3.get_center())
        icon3 = VGroup(circle3, building_icon)
        icons.append(icon3)
        
        # Icon 4: Map pin
        endpoint = curves[3].get_end()
        circle4 = Circle(radius=0.3, fill_color="#9B59B6", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle4.move_to(endpoint)
        pin_icon = self.create_location_icon()
        pin_icon.scale(0.9)
        pin_icon.move_to(circle4.get_center())
        icon4 = VGroup(circle4, pin_icon)
        icons.append(icon4)
        
        # Icon 5: Female symbol
        endpoint = curves[4].get_end()
        circle5 = Circle(radius=0.3, fill_color="#E91E63", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle5.move_to(endpoint)
        icon_text5 = Text("♀", font_size=36, color=WHITE, weight=BOLD)
        icon_text5.move_to(circle5.get_center())
        icon5 = VGroup(circle5, icon_text5)
        icons.append(icon5)
        
        # Icon 6: Heart symbol
        endpoint = curves[5].get_end()
        circle6 = Circle(radius=0.3, fill_color="#FF9800", fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        circle6.move_to(endpoint)
        icon_text6 = Text("❤", font_size=28, color=WHITE)
        icon_text6.move_to(circle6.get_center())
        icon6 = VGroup(circle6, icon_text6)
        icons.append(icon6)
        
        return icons
    
    def animate_icons(self, icons, curves):
        anims = []
        for icon in icons:
            icon.save_state()
            icon.scale(0.5)
            anims.append(AnimationGroup(
                FadeIn(icon),
                icon.animate.restore()
            ))
            
        self.play(
            LaggedStart(*anims, lag_ratio=0.05, run_time=0.8) # Faster
        )
        
        # Floating updater
        for i, icon in enumerate(icons):
            phase = i * PI / 3
            icon.add_updater(
                lambda m, dt, p=phase: m.shift(
                    UP * 0.002 * np.sin(self.renderer.time * 2 + p)
                )
            )
    

    def create_dashboard_cards(self):
        cards = []

        # 0. Dashboard Container
        dashboard_center = UP * 7.5
        
        dashboard_bg = RoundedRectangle(
            width=14.5, # Increased width
            height=7.8, # Increased height to ensure full containment
            corner_radius=0.5,
            fill_color="#F0F4F8",
            fill_opacity=1,
            stroke_width=2,
            stroke_color="#BDC3C7"
        )
        dashboard_bg.move_to(dashboard_center)
        cards.append(dashboard_bg)
        
        # Row 1 (Top) - Hero Cards
        y_row1 = 2.1
        x_spacing = 4.6 # Increased spacing for wider cards
        
        # CARD 1 - Funding (Hero)
        card1 = self.create_metric_card(
            position=dashboard_center + UP * y_row1 + LEFT * x_spacing,
            width=3.8, height=2.0, 
            prefix="₹", target_val=700, suffix=" Cr", 
            main_size=72, main_color="#FF6B35",
            unit_text="", label_text="Total Funding Enabled",
            is_int=True
        )
        cards.append(card1)
        
        # CARD 2 - Scholars
        card2 = self.create_metric_card(
            position=dashboard_center + UP * y_row1,
            width=4.0, height=2.0, # Increased width to 4.0 to match perceived size
            prefix="", target_val=1.53, suffix=" L",
            main_size=72, main_color="#4A90E2",
            unit_text="", label_text="Scholars Empowered",
            is_int=False
        )
        cards.append(card2)
        
        # CARD 3 - Institutions
        # Ensuring this one is also 4.0 for symmetry if user used it as reference
        card3 = self.create_metric_card(
            position=dashboard_center + UP * y_row1 + RIGHT * x_spacing,
            width=4.0, height=2.0, # Increased to 4.0
            prefix="", target_val=11700, suffix="+",
            main_size=60, main_color="#50C878",
            unit_text="", label_text="Institutions Reached",
            is_int=True
        )
        cards.append(card3)
        
        # Row 2 (Middle) - Donut, Geo, Orphans
        y_row2 = -0.2
        
        # CARD 5 - Women Donut (Left)
        card5 = self.create_donut_card(
            position=dashboard_center + UP * y_row2 + LEFT * x_spacing,
            width=4.0 
        )
        cards.append(card5)
        
        # CARD 4 - Geography (Center)
        card4 = self.create_geography_card(
            position=dashboard_center + UP * y_row2
        )
        cards.append(card4)
        
        # CARD 7 - Orphans (Right)
        card7 = self.create_metric_card(
            position=dashboard_center + UP * y_row2 + RIGHT * x_spacing,
            width=3.8, height=2.0, # Consistent width
            prefix="", target_val=20000, suffix="+",
            main_size=60, main_color="#FF9800",
            unit_text="", label_text="Orphaned Scholars",
            is_int=True
        )
        cards.append(card7)
        
        # Row 3 (Bottom)
        y_row3 = -2.6
        row3_x_spacing = 2.6
        
        # 9/10 Card
        card_row3_1 = self.create_bar_card(
            position=dashboard_center + UP * y_row3 + LEFT * row3_x_spacing,
            width=4.6, height=1.6 
        )
        cards.append(card_row3_1)
        
        # Differently-Abled Card
        card_row3_2 = self.create_metric_card(
            position=dashboard_center + UP * y_row3 + RIGHT * row3_x_spacing,
            width=4.4, height=1.6,
            prefix="", target_val=2500, suffix=" +",
            main_size=56, main_color="#9C27B0",
            unit_text="", label_text="Differently-Abled",
            is_int=True
        )
        cards.append(card_row3_2)
        
        return cards
    
    
    def create_metric_card(self, position, width, height, prefix, target_val, suffix, main_size, main_color, unit_text, label_text, is_int):
        # Shadow
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=0.2,
            fill_color=BLACK, fill_opacity=0.1, stroke_width=0
        )
        shadow.move_to(position + np.array([0.05, -0.05, 0]))
        
        # Card background
        card_bg = RoundedRectangle(
            width=width, height=height, corner_radius=0.2,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        card_bg.move_to(position)
        
        # Main number (DecimalNumber)
        num_decimals = 0 if is_int else 2
        number_mob = DecimalNumber(
            0,
            num_decimal_places=num_decimals,
            include_sign=False,
            font_size=main_size,
            color=main_color,
            group_with_commas=True
        )
        # Store target for animation
        number_mob.target_val = target_val
        
        # Prefix/Suffix - Make them smaller and thinner as requested
        # Also set them to invisible initially (to appear after count)
        num_group_items = []
        
        if prefix:
            # Using Tex for prefix
            if prefix == "₹":
                 # Use Text for Rupee symbol
                 p_text = Text(prefix, font="Montserrat", font_size=main_size * 0.6, weight=BOLD, color=main_color) # Thick/Bold
            else:
                 # Use Tex for others, wrapped in bold
                 p_text = Tex(r"\textbf{" + prefix + "}", font_size=main_size * 0.6, color=main_color, stroke_width=1)
                 
            # p_text.set_opacity(0) # REMOVED: Visible from start
            p_text.is_symbol = True # Tag for animation
            num_group_items.append(p_text)
        
        num_group_items.append(number_mob)
        
        if suffix:
             # Make suffix same relative size for ALL (CR, L, +) to ensure alignment consistency
             # Using Tex for suffix allows better baseline alignment
            suffix_font_scale = 0.75 # Increased from 0.55
            if "+" in suffix:
                suffix_font_scale = 0.85 # Increased from 0.65
            
            # Using Tex for suffix
            # Clean suffix text for Latex (escape + if needed?) - Text usually doesn't need escaping in simple Tex
            # But + is safe.
            s_text = Tex(r"\textbf{" + suffix + "}", font_size=main_size * suffix_font_scale, color=main_color, stroke_width=1)
            # s_text.set_opacity(0) # Visible from start
            s_text.is_symbol = True # Tag for animation
            num_group_items.append(s_text)
            
        # Align them by BASELINE to handle different font sizes gracefully
        # Use a VGroup for the number line
        main_group = VGroup(*num_group_items)
        # Initial arrangement - aligned_edge=DOWN is critical for Tex
        main_group.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        
        # Micro-adjustment not needed as much for Tex usually, but let's see.
        # Tex baselines are usually consistent.
        # But if suffix has + it might still hang.
        if suffix and "+" in suffix:
             # Just a small shift
             main_group[-1].shift(UP * 0.1 * (main_size/60))
        
        # Unit text
        if unit_text:
            unit = Tex(unit_text, font_size=24, color=GRAY)
            metric_group = VGroup(main_group, unit).arrange(DOWN, buff=0.1)
        else:
            metric_group = VGroup(main_group)
        
        # Determine the visual center for the metric (slightly up from center to leave room for label)
        metric_center = card_bg.get_center() + UP * 0.2
        metric_group.move_to(metric_center)
        
        # CONTINUOUS LAYOUT UPDATER
        def update_layout(m):
            if unit_text:
                 mg = m[0]
            else:
                 mg = m[0]
            
            mg.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            
            # Re-apply + shift if needed
            if suffix and "+" in suffix:
                mg[-1].shift(UP * 0.1 * (main_size/60))

            if unit_text:
                m.arrange(DOWN, buff=0.1)
            
            m.move_to(metric_center)
            
        metric_group.add_updater(update_layout)
        
        # Label
        label = Tex(r"\textbf{" + label_text + "}", font_size=18, color=GRAY, stroke_width=0.5) # BOLD Label
        label.move_to(card_bg.get_center() + DOWN * 0.65)
        
        card_group = VGroup(shadow, card_bg, metric_group, label)
        return card_group

    
    def create_geography_card(self, position):
        # Shadow
        shadow = RoundedRectangle(
            width=4.0, height=2.0, corner_radius=0.2, # Resize to 4.0
            fill_color=BLACK, fill_opacity=0.1, stroke_width=0
        )
        shadow.move_to(position + np.array([0.05, -0.05, 0]))
        
        # Main Card Background
        card_bg = RoundedRectangle(
            width=4.0, height=2.0, corner_radius=0.2, # Resize to 4.0
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        card_bg.move_to(position)
        
        # Sub-Tile: Districts
        dist_bg = RoundedRectangle(
            width=1.5, height=1.1, corner_radius=0.1, # Slightly wider sub-tiles
            fill_color="#F8F9FA", fill_opacity=1, stroke_width=1, stroke_color="#E0E0E0"
        )
        dist_bg.move_to(card_bg.get_center() + LEFT * 0.9 + UP * 0.15)
        
        dist_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6", group_with_commas=False)
        dist_num.target_val = 739
        # Shift LEFT slightly for visual balance
        dist_num.move_to(dist_bg.get_center() + LEFT * 0.2)
        
        # Bold Label
        dist_lbl = Tex(r"\textbf{Districts}", font_size=18, color=GRAY, stroke_width=0.5)
        dist_lbl.move_to(dist_bg.get_center() + DOWN * 0.3)
        dist_group = VGroup(dist_bg, dist_num, dist_lbl)
        
        # Sub-Tile: States
        state_bg = RoundedRectangle(
            width=1.5, height=1.1, corner_radius=0.1,
            fill_color="#F8F9FA", fill_opacity=1, stroke_width=1, stroke_color="#E0E0E0"
        )
        state_bg.move_to(card_bg.get_center() + RIGHT * 0.9 + UP * 0.15)
        
        state_num = DecimalNumber(0, num_decimal_places=0, font_size=36, color="#9B59B6")
        state_num.target_val = 28
        # Shift LEFT slightly for visual balance
        state_num.move_to(state_bg.get_center() + LEFT * 0.2)
        
        # Bold Label
        state_lbl = Tex(r"\textbf{States}", font_size=18, color=GRAY, stroke_width=0.5)
        state_lbl.move_to(state_bg.get_center() + DOWN * 0.3)
        state_group = VGroup(state_bg, state_num, state_lbl)
        
        # Bottom label
        bottom_label = Tex(r"\textbf{\textit{Pan India Reach}}", font_size=18, color=GRAY, stroke_width=0.5)
        bottom_label.move_to(card_bg.get_center() + DOWN * 0.65)
        
        card_group = VGroup(shadow, card_bg, dist_group, state_group, bottom_label)
        return card_group
    
    def create_donut_card(self, position, width=3.2):
        shadow = RoundedRectangle(
            width=width, height=2.4, corner_radius=0.2, # Use width
            fill_color=BLACK, fill_opacity=0.1, stroke_width=0
        )
        shadow.move_to(position + np.array([0.05, -0.05, 0]))
        
        card_bg = RoundedRectangle(
            width=width, height=2.4, corner_radius=0.2, # Use width
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        card_bg.move_to(position)
        # Force size for consistency
        card_bg.stretch_to_fit_width(width)
        # Increased height from 1.8 to 2.2 as requested to avoid donut overlap
        card_bg.stretch_to_fit_height(2.2) 
        shadow.stretch_to_fit_width(width)
        shadow.stretch_to_fit_height(2.2)
        
        # Donut chart
        donut_center = card_bg.get_center() + UP * 0.25 # Adjusted for shorter card
        
        # Background circle
        bg_donut = Annulus(
            arc_center=donut_center, # Use arc_center!
            inner_radius=0.35, outer_radius=0.7,
            fill_color=GRAY, fill_opacity=0.2, stroke_width=0
        )
        # No move_to needed
        
        # Active sector (Start at 0%)
        # Note: We will animate the angle of this sector
        active_sector = AnnularSector(
            arc_center=donut_center, # Use arc_center!
            inner_radius=0.35, outer_radius=0.7,
            start_angle=PI / 2, angle=0.001, # Start closed
            fill_color="#E91E63", fill_opacity=1, stroke_width=0
        )
        # Tag for easy finding and store fixed center to prevent drift during animation
        active_sector.is_donut_sector = True
        active_sector.fixed_center = donut_center
        
        # Center text
        percent_num = DecimalNumber(0, num_decimal_places=0, font_size=32, color="#E91E63", include_sign=False)
        percent_num.target_val = 57 # Target percent
        
        # Percent symbol
        percent_sym = Tex(r"\textbf{\%}", font_size=20, color="#E91E63", stroke_width=1)
        # percent_sym.set_opacity(0) # Visible from start
        percent_sym.is_symbol = True
        
        percent_group = VGroup(percent_num, percent_sym)
        # Initial position
        percent_group.arrange(RIGHT, buff=0.05, aligned_edge=UP)
        percent_group.move_to(donut_center)
        
        # Updater to keep percent text centered and arranged
        def update_percent_layout(m):
            m.arrange(RIGHT, buff=0.05, aligned_edge=UP)
            m.move_to(donut_center)
            
        percent_group.add_updater(update_percent_layout)
        
        # Label
        label = Tex(r"\textbf{Young Women Scholars}", font_size=18, color=GRAY, stroke_width=0.5)
        label.move_to(card_bg.get_center() + DOWN * 0.65)
        
        card_group = VGroup(shadow, card_bg, bg_donut, active_sector, percent_group, label)
        return card_group
    
    def create_bar_card(self, position, width=3.2, height=2.0):
        # Default scale calc
        scale_factor = width / 3.2 
        
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=0.2,
            fill_color=BLACK, fill_opacity=0.1, stroke_width=0
        )
        shadow.move_to(position + np.array([0.05, -0.05, 0]))
        
        card_bg = RoundedRectangle(
            width=width, height=height, corner_radius=0.2,
            fill_color=WHITE, fill_opacity=1, stroke_width=0
        )
        card_bg.move_to(position)
        
        # Bar chart background
        # Reduced width/height as requested
        bar_bg = RoundedRectangle(
            width=width * 0.7, height=0.3, # Reduced width factor (0.85->0.7) and height (0.4->0.3)
            corner_radius=0.15, 
            fill_color=GRAY, fill_opacity=0.2, stroke_width=0
        )
        bar_bg.move_to(card_bg.get_center() + DOWN * 0.15) 
        
        # Active bar
        target_bar_width = width * 0.7 * 0.9 # Match background width factor
        
        bar_active = RoundedRectangle(
            width=0.01, # Start small
            height=0.3, # Match bg height
            corner_radius=0.15,
            fill_color="#17A2B8", fill_opacity=1, stroke_width=0
        )
        # Left align it within the bar_bg
        bar_active.move_to(bar_bg.get_left() + RIGHT * 0.005, aligned_edge=LEFT)
        
        # Store metadata for animation
        bar_active.is_bar = True
        bar_active.target_width = target_bar_width
        bar_active.align_point = bar_bg.get_left()
        bar_active.bar_bg_ref = bar_bg # Reference for dynamic positioning
        bar_active.bar_bg_ref = bar_bg # Reference for dynamic positioning
        
        # Overlay text: "9/10"
        # Using Tex for better Fraction-like look or just align
        numerator = DecimalNumber(0, num_decimal_places=0, font_size=54, color="#17A2B8", include_sign=False, stroke_width=2.5)
        numerator.target_val = 9
        
        # Tex separator
        denominator = Tex(r"\textbf{/10}", font_size=48, color="#17A2B8", stroke_width=1) # Reduced slightly to 48
        # Boldness in Tex is usually implied or \textbf{}, but font_size is small so it looks bold enough.
        
        # Increase buff to prevent overlap during count up
        # Increase buff to prevent overlap during count up
        # Manual Alignment Strategy
        ratio_group = VGroup(numerator, denominator).arrange(RIGHT, buff=0.1)
        numerator.shift(DOWN * 0.05) # Initial shift for 9
        
        # Move text UP to clear the bar
        ratio_group.move_to(card_bg.get_center() + UP * 0.35)
        
        # Updater for ratio group to keep centered
        # Updater for ratio group to keep centered and manually aligned
        # Updater for ratio group to keep centered
        # Updater for ratio group to keep centered
        def update_ratio(m):
            m.arrange(RIGHT, buff=0.1) # Center alignment (default)
            # Manual tweak: Shift denominator (m[1]) slightly DOWN relative to '9'
            m[1].shift(DOWN * 0.08) # Increased shift to 0.08
            m.move_to(card_bg.get_center() + UP * 0.35) # Keep fixed position
            
        ratio_group.add_updater(update_ratio)
        
        
        # Label
        label = Tex(r"\textbf{First Generation Learners}", font_size=18, color=GRAY, stroke_width=0.5)
        label.move_to(card_bg.get_center() + DOWN * 0.6)
        
        card_group = VGroup(shadow, card_bg, bar_bg, bar_active, ratio_group, label)
        return card_group
    
    def create_title_card(self, position):
        return VGroup() # Empty as requested
    
    
    
    def animate_dashboard_cards(self, cards):
        # 1. Fade In Cards (Container + Content)
        
        dashboard_bg = cards[0]
        content_cards = cards[1:]
        
        # Display everything at once (with slight lag for visual pleasantness)
        self.play(FadeIn(dashboard_bg), run_time=0.5)
        
        # Animate all cards in simultaneously (very small lag)
        self.play(
            AnimationGroup(
                *[FadeIn(card, shift=UP*0.2) for card in content_cards],
                lag_ratio=0.05
            ),
            run_time=1.0
        )
        
        # 2. Animate Numbers, Donut, and find Symbols to reveal later
        anims = []
        trackers = []
        symbols_to_reveal = []
        
        # Helper to recursively find objects
        def get_all_mobjects(mobject, type_check_func):
            found = []
            if type_check_func(mobject):
                found.append(mobject)
            for sub in mobject.submobjects:
                found.extend(get_all_mobjects(sub, type_check_func))
            return found

        # --- A. Setup Number Animations ---
        for card in content_cards:
            # Find DecimalNumbers with 'target_val'
            d_nums = get_all_mobjects(card, lambda m: isinstance(m, DecimalNumber) and hasattr(m, 'target_val'))
            
            for d_num in d_nums:
                tracker = ValueTracker(0)
                trackers.append(tracker)
                
                # Update function for decimal
                def update_decimal(m, t=tracker):
                    m.set_value(t.get_value())
                
                d_num.add_updater(update_decimal)
                anims.append(tracker.animate.set_value(d_num.target_val))
            
            # Find Symbols (tagged with is_symbol=True)
            syms = get_all_mobjects(card, lambda m: hasattr(m, 'is_symbol') and m.is_symbol)
            symbols_to_reveal.extend(syms)
            
            # Find Donut Sector (tagged with is_donut_sector)
            sectors = get_all_mobjects(card, lambda m: isinstance(m, AnnularSector) and hasattr(m, 'is_donut_sector'))
            for sector in sectors:
                # ValueTracker for angle (0 to 57%)
                # 57% of TAU is approx 3.58 rad
                donut_tracker = ValueTracker(0.001)
                trackers.append(donut_tracker)
                
                # Updater to redraw the sector with new angle
                # We need to capture the current properties of the sector
                start_dist = sector.start_angle
                i_rad = sector.inner_radius
                o_rad = sector.outer_radius
                col = sector.fill_color
                # CRITICAL: Use the stored fixed center or fallback to current center
                center = getattr(sector, 'fixed_center', sector.get_center())
                
                def update_sector(m, t=donut_tracker, c=center):
                    # We modify the angle. 
                    # create a new sector and become it.
                    new_sec = AnnularSector(
                        arc_center=c, # IMPORTANT: Keep center fixed
                        inner_radius=i_rad, outer_radius=o_rad,
                        start_angle=start_dist, angle=t.get_value(),
                        # FORCE PINK COLOR HERE just in case 'col' variable is wrong
                        fill_color="#E91E63", fill_opacity=1, stroke_width=0
                    )
                    # No move_to(c) because arc_center handles it
                    m.become(new_sec)
                
                sector.add_updater(update_sector)
                anims.append(donut_tracker.animate.set_value(0.57 * TAU))
            
            # Find Active Bar (tagged with is_bar)
            bars = get_all_mobjects(card, lambda m: hasattr(m, 'is_bar'))
            for bar in bars:
                bar_tracker = ValueTracker(0.01)
                trackers.append(bar_tracker)
                
                # Default props
                t_w = getattr(bar, 'target_width', 1.0)
                align_p = getattr(bar, 'align_point', bar.get_left())
                h = bar.height
                c_r = bar.corner_radius
                col = bar.fill_color
                
                def update_bar(m, t=bar_tracker):
                    # Create new rounded rect with current width
                    new_bar = RoundedRectangle(
                        width=t.get_value(), height=h, corner_radius=c_r,
                        fill_color=col, fill_opacity=1, stroke_width=0
                    )
                    
                    # FIX: Use dynamic position from bg_ref if available
                    current_align_p = align_p
                    if hasattr(bar, 'bar_bg_ref'):
                         current_align_p = bar.bar_bg_ref.get_left() + RIGHT * 0.005
                    
                    new_bar.move_to(current_align_p, aligned_edge=LEFT)
                    # Restore props so next update finds it
                    new_bar.bar_bg_ref = getattr(bar, 'bar_bg_ref', None)
                    m.become(new_bar)
                
                bar.add_updater(update_bar)
                anims.append(bar_tracker.animate.set_value(t_w))

        # --- B. Play Main Animations ---
        if anims:
            self.play(AnimationGroup(*anims), run_time=1.5, rate_func=smooth)
            
            # Cleanup updaters
            for card in content_cards:
                d_nums = get_all_mobjects(card, lambda m: isinstance(m, DecimalNumber))
                for d_num in d_nums:
                    d_num.clear_updaters()
                
                sectors = get_all_mobjects(card, lambda m: isinstance(m, AnnularSector) and hasattr(m, 'is_donut_sector'))
                for s in sectors:
                    s.clear_updaters()
                    
        # --- C. Reveal Symbols (after numbers reach max) ---
        if symbols_to_reveal:
            self.play(
                *[sym.animate.set_opacity(1) for sym in symbols_to_reveal],
                run_time=0.5
            )
        
        self.wait(0.2)
    
    def apply_ambient_motion(self, cards, logo_container):
        # Apply floating updaters to all cards
        for i, card in enumerate(cards):
            phase = i * PI / 4.5
            card.add_updater(
                lambda m, dt, p=phase: m.shift(
                    UP * 0.0008 * np.sin(self.renderer.time * 1.5 + p)
                )
            )
        
        # Shadow pulsing
        for card in cards:
            if len(card) > 0:
                shadow = card[0]
                original_opacity = shadow.get_fill_opacity()
                
                def pulse_updater(m, dt, orig=original_opacity):
                    new_opacity = orig + 0.04 * np.sin(self.renderer.time * 2)
                    m.set_fill(opacity=max(0, min(0.15, new_opacity)))
                
                shadow.add_updater(pulse_updater)