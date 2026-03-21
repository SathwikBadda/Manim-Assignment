from manim import *
import sys
import os

# Adjust path to import custom assets
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from manim_asset_codes.asset_1 import Asset1
from manim_asset_codes.asset_2 import Asset2

class Gavel(VGroup):
    def __init__(self, color=ManimColor("#2C3E50"), **kwargs):
        super().__init__(**kwargs)
        handle = RoundedRectangle(width=0.4, height=0.1, corner_radius=0.03, fill_color=color, fill_opacity=1, stroke_width=0)
        head = RoundedRectangle(width=0.2, height=0.3, corner_radius=0.03, fill_color=color, fill_opacity=1, stroke_width=0)
        head.next_to(handle, RIGHT, buff=0)
        head.shift(UP*0.1)
        self.add(handle, head)
        self.rotate(PI/4)

class ChainLink(VGroup):
    def __init__(self, color=ManimColor("#2C3E50"), **kwargs):
        super().__init__(**kwargs)
        link1 = RoundedRectangle(width=0.3, height=0.15, corner_radius=0.05, stroke_width=3, stroke_color=color)
        link2 = RoundedRectangle(width=0.3, height=0.15, corner_radius=0.05, stroke_width=3, stroke_color=color)
        link2.shift(RIGHT*0.2)
        self.add(link1, link2)

class AlertTriangle(VGroup):
    def __init__(self, color=ManimColor("#E67E22"), **kwargs):
        super().__init__(**kwargs)
        tri = Triangle(color=color, fill_opacity=1).scale(0.2)
        exc = Text("!", color=WHITE, font_size=16, weight=BOLD).move_to(tri.get_center() + DOWN*0.02)
        self.add(tri, exc)

class FullDisclosureScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"
        self.navy = ManimColor("#084993")
        self.orange = ManimColor("#ed8c32")
        self.amber = ManimColor("#FFBF00")
        self.teal = ManimColor("#008080")

        self.show_full_disclosure()
        if hasattr(self, 'section_times'): self.section_times.append(self.renderer.time)
        self.show_information_flow()
        if hasattr(self, 'section_times'): self.section_times.append(self.renderer.time)
        self.show_disclosure_scenarios()
        if hasattr(self, 'section_times'): self.section_times.append(self.renderer.time)
        self.show_gaap_overview()

    def create_title(self, text):
        title = Text(text, color=self.navy, font="Montserrat", weight=BOLD, font_size=36)
        title.to_edge(UP, buff=0.5)
        # Use simple navy line as per image reference usually
        underline = Line(LEFT, RIGHT, color=self.orange, stroke_width=2)
        underline.width = title.width
        underline.next_to(title, DOWN, buff=0.1)
        return VGroup(title, underline)

    def create_info_box(self, text, icon=None):
        label = Text(text, color=WHITE, font="Montserrat", weight=BOLD, font_size=40).scale(0.5)
        box = RoundedRectangle(width=label.width + 1.0, height=0.6, corner_radius=0.1, fill_color=self.orange, fill_opacity=1, stroke_width=0)
        group = VGroup(box, label)
        if icon:
            icon.scale(0.5).next_to(label, LEFT, buff=0.2)
            group.add(icon)
        group.to_edge(DOWN, buff=0.5)
        return group

    ## Section 1
    def show_full_disclosure(self):
        # 1. Title
        self.title_grp = self.create_title("Principle of Full Disclosure")
        self.title, self.title_line = self.title_grp[0], self.title_grp[1]
        self.play(Write(self.title), run_time=0.74)
        self.play(Create(self.title_line), run_time=0.6)

        # 2. Document Stack (Reference group_1.py style)
        doc_stack = VGroup()
        for i in range(3):
            doc = Asset1(sheet_width=2.5, sheet_height=3.0, sheet_color=ManimColor("#FFFFE4"), line_color=self.orange).scale(0.8)
            doc.move_to(ORIGIN + UP * 0.2 + LEFT * 0.1 * i + UP * 0.1 * i)
            doc_stack.add(doc)
        
        doc_stack.move_to(ORIGIN + UP * 0.5)
        self.play(FadeIn(doc_stack, lag_ratio=0.1), run_time=0.6)

        # 3. Add text below
        reports_label = Text("Financial Reports", color=self.navy, font="Montserrat", weight=BOLD, font_size=32)
        reports_label.next_to(doc_stack, DOWN, buff=0.5)
        self.play(FadeIn(reports_label), run_time=0.6)

        # 4. Bottom Box
        info_box = self.create_info_box("Nothing material is hidden — full picture always disclosed.")
        self.play(FadeIn(info_box), run_time=0.6)
        
        self.wait(1.5)
        self.play(FadeOut(doc_stack, reports_label, info_box), run_time=0.5)

    ## Section 2
    def show_information_flow(self):
        # Segment 2
        building = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Company.png").scale(1.8).to_edge(LEFT, buff=1.0)
        
        investor_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Investor_1.png").scale(0.5).move_to(RIGHT*4.0 + UP*1.8)
        investor_label = Text("Investor", font_size=24, color=self.navy, font="Montserrat", weight=BOLD).next_to(investor_img, DOWN, buff=0.2)
        
        regulator_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Regulator.png").scale(1.0).move_to(RIGHT*4.0 + DOWN*1.2)
        regulator_label = Text("Regulator", font_size=24, color=self.navy, font="Montserrat", weight=BOLD).next_to(regulator_img, DOWN, buff=0.2)
        
        self.play(FadeIn(building), FadeIn(investor_img), FadeIn(investor_label), FadeIn(regulator_img), FadeIn(regulator_label), run_time=0.8)

        # Paths
        path_up = CurvedArrow(building.get_right(), investor_img.get_left() + LEFT*0.3, angle=-TAU/8, color=self.navy)
        path_down = CurvedArrow(building.get_right(), regulator_img.get_left() + LEFT*0.3, angle=TAU/8, color=self.navy)
        
        self.play(Create(path_up), Create(path_down), run_time=0.82)

        # Loop documents - Phase 28: Stack of 3
        doc_stack = Group()
        for i in range(3):
            doc = Asset1(sheet_width=0.6, sheet_height=0.75, sheet_color=ManimColor("#FFFFE4")).scale(1.2)
            doc.move_to(building.get_right() + RIGHT * 0.1 + LEFT * 0.05 * i + UP * 0.05 * i)
            doc_stack.add(doc)
            
        self.play(FadeIn(doc_stack), run_time=0.5)

        # Animate 2 travel, 1 stays
        self.play(
            MoveAlongPath(doc_stack[2], path_up),
            MoveAlongPath(doc_stack[1], path_down),
            run_time=3.0,
            rate_func=linear
        )

        # No Checkmarks needed per refined request
        info_box = self.create_info_box("All relevant information flows to investors and regulators.")
        self.play(FadeIn(info_box), run_time=0.6)
        
        self.wait(1.0)
        # Fade documents after labels; ensure EVERYTHING goes
        self.play(FadeOut(building, investor_img, investor_label, regulator_img, regulator_label, path_up, path_down, info_box, doc_stack), run_time=0.5)

    ## Section 3
    def show_disclosure_scenarios(self):
        # Segment 3: Layout & Flow Refinement (Phase 28)
        # Center: Building (Smaller)
        main_building = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Company.png").scale(1.8).move_to(ORIGIN)
        
        # Left Side: Boxes + Icons
        # Scenario 1 (Lawsuit)
        lawsuit_box = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.1, fill_color=self.navy, fill_opacity=1, stroke_width=0)
        lawsuit_text = Text("Major Lawsuit\nPending", color=WHITE, font_size=16, weight=BOLD, font="Montserrat").move_to(lawsuit_box.get_center())
        lawsuit_box_grp = VGroup(lawsuit_box, lawsuit_text).move_to(LEFT * 5.2 + UP * 1.5)
        
        lawsuit_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Law_Suit.png").scale(0.8).next_to(lawsuit_box_grp, RIGHT, buff=0.3)
        
        # Scenario 2 (Debt)
        debt_box = RoundedRectangle(width=2.5, height=0.8, corner_radius=0.1, fill_color=self.navy, fill_opacity=1, stroke_width=0)
        debt_text = Text("Debt\nGovernance", color=WHITE, font_size=16, weight=BOLD, font="Montserrat").move_to(debt_box.get_center())
        debt_box_grp = VGroup(debt_box, debt_text).move_to(LEFT * 5.2 + DOWN * 1.0)
        
        debt_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_8/Debt_Governance.png").scale(0.7).next_to(debt_box_grp, RIGHT, buff=0.3)
        
        # Align Lawsuit center vertically with Debt Governance center
        lawsuit_img.set_x(debt_img.get_x())
        
        # Right Side: Financial Statements stack
        statements_stack = VGroup()
        for i in range(4):
            doc = Asset1(sheet_width=0.8, sheet_height=1.0, sheet_color=ManimColor("#FFFFE4")).scale(1.0)
            doc.move_to(RIGHT * 4.5 + LEFT * 0.08 * i + UP * 0.1 * i)
            statements_stack.add(doc)
            
        statements_label = Text("Financial\nStatements", color=self.navy, font="Montserrat", weight=BOLD, font_size=18).next_to(statements_stack, DOWN, buff=0.3)
        right_grp = VGroup(statements_stack, statements_label)

        # Entrance
        self.play(FadeIn(main_building, scale=0.8), run_time=1.0)
        self.play(FadeIn(lawsuit_box_grp), FadeIn(lawsuit_img), FadeIn(debt_box_grp), FadeIn(debt_img), run_time=1.0)
        self.play(FadeIn(right_grp, shift=LEFT*0.5), run_time=0.5)

        # Connections (Building Sides to Icons) - Refined Straight Lines hitting centers for overlap
        conn_start = main_building.get_left() + RIGHT * 1.0
        conn1 = Line(
            start=conn_start, 
            end=lawsuit_img.get_center(), 
            color=self.navy, stroke_width=2
        ).set_z_index(-1)
        conn2 = Line(
            start=conn_start, 
            end=debt_img.get_center(), 
            color=self.navy, stroke_width=2
        ).set_z_index(-1)
        
        self.play(Create(conn1), Create(conn2), run_time=1.0)

        # Bottom Info Box
        info_box = self.create_info_box("Material obligations must always appear in financial statement notes.")
        info_box.width = config.frame_width - 1.0
        self.play(FadeIn(info_box), run_time=0.6)
        
        self.wait(0.5)

        # Outro: fade out connections and text boxes only
        self.play(
            FadeOut(lawsuit_box_grp), FadeOut(debt_box_grp),
            FadeOut(conn1), FadeOut(conn2),
            run_time=0.53
        )

        # Continuous trajectory flow logic (Phase 34/35/36/37)
        # Offset to clear building while avoiding title/footer
        top_traj = main_building.get_top() + UP * 0.8 + LEFT * 0.2
        bottom_traj = main_building.get_bottom() + DOWN * 0.8 + LEFT * 0.2
        
        # Define paths with shallower angles to stay within safe area
        arc_path_lawsuit = ArcBetweenPoints(top_traj, statements_stack.get_center(), angle=-TAU/6)
        arc_path_debt = ArcBetweenPoints(bottom_traj, statements_stack.get_center(), angle=TAU/6)

        # Move to trajectories & SCALE DOWN
        self.play(
            lawsuit_img.animate(rate_func=linear).move_to(top_traj).scale(0.8),
            debt_img.animate(rate_func=linear).move_to(bottom_traj).scale(0.8),
            run_time=0.8
        )

        # Immediate curved travel - Stay BEHIND the stack
        statements_stack.set_z_index(30)
        lawsuit_img.set_z_index(10)
        debt_img.set_z_index(10)
        
        self.play(
            MoveAlongPath(lawsuit_img, arc_path_lawsuit),
            MoveAlongPath(debt_img, arc_path_debt),
            run_time=1.5,
            rate_func=linear
        )
        
        # Settle BEHIND stack - only fade out when the rest of the scene fades
        self.play(
            FadeOut(main_building), 
            FadeOut(right_grp), 
            FadeOut(info_box), 
            FadeOut(self.title),
            FadeOut(self.title_line),
            FadeOut(lawsuit_img),
            FadeOut(debt_img),
            run_time=1.0
        )
        self.wait(0.5)

    ## Section 4
    def show_gaap_overview(self):
        # Segment 4: Exact GAAP Overview (Replicated from scene_3.py)
        # 1. Background and Title setup
        self.camera.background_color = WHITE
        CLIENT_BLUE = "#084993"
        CLIENT_ORANGE = "#ed8c32"
        FONT_MAIN = "Montserrat"

        intro_title = Text("Key Principles of U.S. GAAP", font=FONT_MAIN, weight=BOLD, font_size=42, color=CLIENT_BLUE)
        intro_title.to_edge(UP, buff=0.35)
        intro_underline = Line(intro_title.get_left(), intro_title.get_right(), color=CLIENT_ORANGE, stroke_width=5).next_to(intro_title, DOWN, buff=0.12)
        
        # 2. Map placeholder - drawn with lines
        us_map = RoundedRectangle(width=8, height=4.5, corner_radius=1, color=ManimColor("#D3D3D3"), fill_color=ManimColor("#F8FAFC"), fill_opacity=1)
        us_map.scale(1.2).shift(DOWN * 0.5) 
        
        self.play(FadeIn(intro_title, shift=UP*0.2), Create(intro_underline), run_time=1.0)
        self.play(Create(us_map), run_time=0.8) # Drawn with lines effect

        # 3. GAAP Circles fly-in
        radius = config.frame_width * 0.045
        gaap = Group()
        for char in "GAAP":
            c = Circle(radius=radius, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
            t = Text(char, font=FONT_MAIN, weight=BOLD, font_size=54, color=CLIENT_BLUE).move_to(c)
            gaap.add(Group(c, t))
        
        gaap.arrange(RIGHT, buff=0.4).move_to(us_map.get_center())
        gaap_targets = [g.get_center() for g in gaap]
        for g in gaap: g.shift(DOWN * 7) # Start off-screen

        # Staggered fly-in
        self.play(
            LaggedStart(*[g.animate.move_to(tgt) for g, tgt in zip(gaap, gaap_targets)], lag_ratio=0.2),
            run_time=1.0
        )
        self.wait(0.2)

        # 4. Resize both down to final position
        self.play(
            us_map.animate.scale(0.28).shift(UP * 0.1), 
            gaap.animate.scale(0.28).move_to(us_map.get_center() + UP * 0.1), 
            run_time=0.8
        )
        hex_center = us_map.get_center()

        # 4. Hexagon circles -> rotating -> transforming into pills
        hex_radius = 2.8
        circles = Group()
        # Adjusted angles to match standard hex/image references usually
        for i in range(6):
            angle = i * TAU / 6
            pos = hex_center + np.array([hex_radius * np.cos(angle), hex_radius * np.sin(angle), 0])
            
            # Phase 32: Layout Fix - Move Sincerity (index 2) and Consistency (index 1) down
            if i in [1, 2]:
                pos += DOWN * 0.5
            
            c = Circle(radius=0.42, stroke_width=5, color=CLIENT_BLUE, fill_opacity=0)
            c.move_to(pos)
            circles.add(c)

        self.play(LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.1), run_time=0.6)
        self.play(Rotate(circles, angle=-TAU, about_point=hex_center), run_time=1.0, rate_func=linear)

        # Principle data
        principles = ["Regularity", "Consistency", "Sincerity", "Prudence", "Going Concern", "Full Disclosure"]
        
        principle_images = [
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Principle of Regularity.png",
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Consistency.png",
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Sincerity.png",
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Prudence.png",
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Concern.png",
            "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_3/Disclosure.png"
        ]
        
        pills = Group()
        texts = Group()
        icons = Group()

        for i, name in enumerate(principles):
            pill = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.4, stroke_width=4, color=CLIENT_BLUE, fill_opacity=0).move_to(circles[i])
            txt = Text(name, font=FONT_MAIN, weight=MEDIUM, font_size=40, color=CLIENT_BLUE).scale(0.5).move_to(pill)
            
            icon = ImageMobject(principle_images[i])
            icon.height = 0.9
            icon.next_to(pill, UP, buff=0.18)
            
            pills.add(pill)
            texts.add(txt)
            icons.add(icon)

        self.play(
            *[ReplacementTransform(circles[i], pills[i]) for i in range(6)],
            *[FadeIn(texts[i]) for i in range(6)],
            run_time=0.8
        )
        self.play(LaggedStart(*[FadeIn(icons[i], scale=0.5) for i in range(6)], lag_ratio=0.15), run_time=0.6)

        # Final Wait and Exit to match exactly 10.82 seconds
        # 1.0 + 0.8 + 1.0 + 0.2 + 0.8 + 0.6 + 1.0 + 0.8 + 0.6 = 6.8 seconds so far
        # Remaining: 10.82 - 6.8 = 4.02 seconds
        # Let's use 2.82 for wait and 1.2 for the FadeOut
        self.wait(2.82)
        center_group = Group(us_map, gaap)
        self.play(FadeOut(Group(center_group, pills, texts, icons, intro_title, intro_underline)), run_time=1.2)
