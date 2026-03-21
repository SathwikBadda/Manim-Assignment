from manim import *
from manim.utils.rate_functions import ease_out_back
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from manim_asset_codes.asset_1 import Asset1
import numpy as np

# Font Weight Constants
MEDIUM = "MEDIUM"
REGULAR = "NORMAL"

class FinalScene(ThreeDScene):
    def construct(self):
        self.stop_coins = False
        self.camera.background_color = "#FFFFFF"

        ## Section 1
        circle_g = Circle(radius=0.7, fill_opacity=1, fill_color=WHITE, stroke_width=8, stroke_color=ManimColor("#084993"))
        circle_a1 = Circle(radius=0.7, fill_opacity=1, fill_color=WHITE, stroke_width=8, stroke_color=ManimColor("#084993"))
        circle_a2 = Circle(radius=0.7, fill_opacity=1, fill_color=WHITE, stroke_width=8, stroke_color=ManimColor("#084993"))
        circle_p = Circle(radius=0.7, fill_opacity=1, fill_color=WHITE, stroke_width=8, stroke_color=ManimColor("#084993"))
        
        text_g = Text("G", font_size=72, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to(circle_g.get_center())
        text_a1 = Text("A", font_size=72, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to(circle_a1.get_center())
        text_a2 = Text("A", font_size=72, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to(circle_a2.get_center())
        text_p = Text("P", font_size=72, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to(circle_p.get_center())
        
        circle_g.add(text_g)
        circle_a1.add(text_a1)
        circle_a2.add(text_a2)
        circle_p.add(text_p) 
        
        circle_g.move_to([-2.4, -5, 0])
        circle_a1.move_to([-0.8, -5, 0])
        circle_a2.move_to([0.8, -5, 0])
        circle_p.move_to([2.4, -5, 0])
        
        circle_g.set_z_index(3)
        circle_a1.set_z_index(3)
        circle_a2.set_z_index(3)
        circle_p.set_z_index(3)
        # US Map Visibility
        image_1 = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/US_Map.png").scale(2.4).move_to(ORIGIN).set_z_index(0)
        
        # Flipping Document and Background Set
        primary_doc = Asset1(sheet_width=1.0, sheet_height=1.3, sheet_color=ManimColor("#FFFFE4"), line_color=ManimColor("#ed8c32"), currency_color=ManimColor("#084993")).scale(1.4).move_to(RIGHT*5.8).set_z_index(2)
        
        # Pure Polygon Outlines for background
        doc_outlines = VGroup()
        for i in range(2):
            w, h = 1.0 * 1.4, 1.3 * 1.4 # Scaled dimensions
            f = 0.2 * 1.4 # Scaled fold
            outline = Polygon(
                [-w/2, -h/2, 0], [w/2, -h/2, 0], [w/2, h/2-f, 0], 
                [w/2-f, h/2, 0], [-w/2, h/2, 0],
                stroke_color=ManimColor("#ed8c32"), stroke_width=2, fill_color=ManimColor("#FFFFE4"), fill_opacity=1
            ).move_to(RIGHT*5.8 + LEFT*0.1*(i+1) + UP*0.25*(i+1)).set_z_index(1)
            doc_outlines.add(outline)
        
        supporting_text = Text("The foundation of financial reporting", font_size=64, color=ManimColor("#084993"), font="Avenir", weight=BOLD).scale(0.5).move_to([0, -3.2, 0])
        supporting_bg = RoundedRectangle(width=supporting_text.width + 1.0, height=0.7, corner_radius=0.2, fill_color=ManimColor("#DEEBF7"), fill_opacity=1, stroke_width=0).move_to(supporting_text.get_center())
        #supporting_text.set_opacity(0)
        
        #self.add(image_1)
        
        self.play(FadeIn(circle_g), run_time=0.2)
        self.play(circle_g.animate.move_to([-2.4, 0, 0]), run_time=0.4, rate_func=ease_out_back)
        
        self.play(FadeIn(circle_a1), run_time=0.2)
        self.play(circle_a1.animate.move_to([-0.8, 0, 0]), run_time=0.4, rate_func=linear)
        
        self.play(FadeIn(circle_a2), run_time=0.2)
        self.play(circle_a2.animate.move_to([0.8, 0, 0]), run_time=0.4, rate_func=ease_out_back)
        
        self.play(FadeIn(circle_p), run_time=0.2)
        self.play(circle_p.animate.move_to([2.4, 0, 0]), run_time=0.4, rate_func=linear)
        
        self.play(FadeIn(image_1), run_time=0.8)
        
        # Display ONE doc, Flip it, and show background docs simultaneously
        self.play(FadeIn(primary_doc), run_time=0.4)
        self.play(
            Rotate(primary_doc, angle=2*PI, axis=UP), 
            FadeIn(doc_outlines, lag_ratio=0.1),
            run_time=0.8
        )
        
        self.play(FadeIn(supporting_bg), Write(supporting_text), run_time=0.74)
        self.wait(0.6)
        
        
        ## Section 2
        self.play(FadeOut(image_1), FadeOut(primary_doc), FadeOut(doc_outlines), FadeOut(supporting_text), FadeOut(supporting_bg), run_time=1.19)
        self.remove(image_1, primary_doc, doc_outlines, supporting_text, supporting_bg)
        
        margin_rect = Rectangle(width=1.0, height=8.0, fill_color=ManimColor("#85c2e0"), fill_opacity=0.3, stroke_width=0).move_to([-4.8, 8, 0])
        
        # 1. Move GAAP to left first (Centered on Margin)
        self.play(
            circle_g.animate.move_to([-5.0, 1.8, 0]).scale(0.5),
            circle_a1.animate.move_to([-5.0, 0.6, 0]).scale(0.5),
            circle_a2.animate.move_to([-5.0, -0.6, 0]).scale(0.5),
            circle_p.animate.move_to([-5.0, -1.8, 0]).scale(0.5),
            run_time=1.5
        )
        
        # 2. Then drop the margin (avoid overlap)
        self.play(
            margin_rect.animate.move_to([-5.0, 0, 0]), # Falling from top
            run_time=1.0
        )
        
        scandal_pos = [1.3, 2.8, 0]
        sec_pos = [1.3 - 1.8, 0, 0]
        fasb_pos = [1.3 + 1.8, 0, 0]
        principles_pos = [1.3, -2.8, 0]
        
        def create_flow_box(text_str, image_path, pos, width=3.5, height=1.2, font_size=40, icon_scale=0.7):
            box = RoundedRectangle(width=width, height=height, corner_radius=0.15, 
                                 fill_color=ManimColor("#DEEBF7"), fill_opacity=1, 
                                 stroke_width=1.5, stroke_color=ManimColor("#084993"))
            
            icon = ImageMobject(image_path)
            # Use specific scale for icon
            icon.height = height * icon_scale
            icon.move_to(box.get_left() + RIGHT * (icon.width/2 + 0.3))
            
            text_obj = Text(text_str, font_size=font_size, color=ManimColor("#084993"), font="Avenir", weight=BOLD)
            # Ensure text doesn't overlap icon or box edges
            max_text_w = width - icon.width - 0.4
            if text_obj.width > max_text_w:
                text_obj.scale(max_text_w / text_obj.width)
            
            text_obj.move_to(box.get_right() + LEFT * (text_obj.width/2 + 0.2))
            
            group = Group(box, icon, text_obj).move_to(pos)
            return group, box

        def create_stakeholder_view(text_str, image_path, pos, img_scale=1.2, font_size=28):
            # Box-less for Section 3: Larger icon, smaller text below
            icon = ImageMobject(image_path).scale(img_scale)
            text_obj = Text(text_str, font_size=font_size, color=ManimColor("#084993"), font="Avenir", weight=BOLD)
            text_obj.next_to(icon, DOWN, buff=0.2)
            
            group = Group(icon, text_obj).move_to(pos)
            return group, icon

        # Create Boxes
        scandal_grp, scandal_box = create_flow_box("Financial Scandal", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Scandal.png", scandal_pos, icon_scale=0.7)
        sec_grp, sec_box = create_flow_box("", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/SEC.png", sec_pos, width=1.5, icon_scale=0.7)
        fasb_grp, fasb_box = create_flow_box("", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/FASB_logo.png", fasb_pos, width=1.8, icon_scale=0.35)
        principles_grp, principles_box = create_flow_box("Accounting Principles", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Accounting_Principles.png", principles_pos, width=4.5, icon_scale=0.7)

        # Create Connectors
        def create_connector(start_point, end_point):
            mid_y = (start_point[1] + end_point[1]) / 2
            path = VMobject(color=ManimColor("#084993"), stroke_width=1.5)
            path.set_points_as_corners([
                start_point,
                [start_point[0], mid_y, 0],
                [end_point[0], mid_y, 0],
                end_point
            ])
            return path

        conn_s_sec = create_connector(scandal_box.get_bottom(), sec_box.get_top())
        conn_s_fasb = create_connector(scandal_box.get_bottom(), fasb_box.get_top())
        conn_sec_p = create_connector(sec_box.get_bottom(), principles_box.get_top())
        conn_fasb_p = create_connector(fasb_box.get_bottom(), principles_box.get_top())

        # Animations
        self.play(FadeIn(scandal_grp), run_time=0.8)
        self.play(Create(conn_s_sec), Create(conn_s_fasb), run_time=0.6)
        self.play(FadeIn(sec_grp), FadeIn(fasb_grp), run_time=0.8)
        self.play(Create(conn_sec_p), Create(conn_fasb_p), run_time=0.6)
        self.play(FadeIn(principles_grp), run_time=0.8)
        
        # Section 2 Flowing Balls (Split-Join Cycles)
        def run_split_join_cycle():
            dot1 = Circle(radius=0.08, fill_color=ManimColor("#ed8c32"), fill_opacity=1, stroke_width=0).set_z_index(3)
            
            s_bottom = scandal_box.get_bottom()
            sec_top = sec_box.get_top()
            fasb_top = fasb_box.get_top()
            sec_bot = sec_box.get_bottom()
            fasb_bot = fasb_box.get_bottom()
            p_top = principles_box.get_top()
            
            mid_y_top = (s_bottom[1] + sec_top[1]) / 2
            mid_y_bot = (sec_bot[1] + p_top[1]) / 2
            
            # Paths
            path_scandal_drop = Line(s_bottom, [s_bottom[0], mid_y_top, 0])
            path_sec_branch = VMobject().set_points_as_corners([[s_bottom[0], mid_y_top, 0], [sec_top[0], mid_y_top, 0], sec_top])
            path_fasb_branch = VMobject().set_points_as_corners([[s_bottom[0], mid_y_top, 0], [fasb_top[0], mid_y_top, 0], fasb_top])
            
            path_sec_exit = VMobject().set_points_as_corners([sec_bot, [sec_bot[0], mid_y_bot, 0], [p_top[0], mid_y_bot, 0]])
            path_fasb_exit = VMobject().set_points_as_corners([fasb_bot, [fasb_bot[0], mid_y_bot, 0], [p_top[0], mid_y_bot, 0]])
            path_final_drop = Line([p_top[0], mid_y_bot, 0], p_top)
            
            # Sequence
            self.add(dot1)
            self.play(MoveAlongPath(dot1, path_scandal_drop, rate_func=linear), run_time=0.4)
            
            dot2 = dot1.copy()
            self.add(dot2)
            self.play(
                MoveAlongPath(dot1, path_sec_branch, rate_func=linear),
                MoveAlongPath(dot2, path_fasb_branch, rate_func=linear),
                run_time=0.8
            )
            
            # Wait at boxes briefly
            self.wait(0.2)
            
            self.play(
                MoveAlongPath(dot1, path_sec_exit, rate_func=linear),
                MoveAlongPath(dot2, path_fasb_exit, rate_func=linear),
                run_time=0.8
            )
            
            self.remove(dot2)
            self.play(MoveAlongPath(dot1, path_final_drop, rate_func=linear), run_time=0.4)
            self.play(FadeOut(dot1, run_time=0.2))

        # Cycle 1
        run_split_join_cycle()
        self.wait(0.3)
        # Cycle 2
        run_split_join_cycle()
        self.wait(0.3)
        
        self.wait(3.23)
        # time_parser_adjust: self.wait(2.74)

        ## Section 3
        # Clean up Section 2 (Keep GAAP and Margin)
        self.play(
            FadeOut(scandal_grp), FadeOut(sec_grp), FadeOut(fasb_grp), FadeOut(principles_grp),
            FadeOut(conn_s_sec), FadeOut(conn_s_fasb), FadeOut(conn_sec_p), FadeOut(conn_fasb_p),
            run_time=0.8
        )
        self.remove(scandal_grp, sec_grp, fasb_grp, principles_grp, conn_s_sec, conn_s_fasb, conn_sec_p, conn_fasb_p)
        
        # Title Box at Top Center of Flow Area
        title_box = RoundedRectangle(width=4.5, height=0.7, corner_radius=0.1, 
                                   fill_color=ManimColor("#1a5276"), fill_opacity=1, 
                                   stroke_width=0).move_to([1.3, 3.4, 0])
        title_text = Text("Financial Reporting", font_size=24, color=WHITE, font="Avenir", weight=BOLD).move_to(title_box.get_center())
        title_grp = Group(title_box, title_text)
        
        # Bracket Container
        bracket = VMobject(color=ManimColor("#1a5276"), stroke_width=2)
        bracket.set_points_as_corners([
            [1.3 - 2.5, 2.5, 0],
            [1.3 - 2.5, 2.8, 0],
            [1.3 + 2.5, 2.8, 0],
            [1.3 + 2.5, 2.5, 0]
        ])

        self.play(FadeIn(title_grp), Create(bracket), run_time=0.8)
        
        # Simplified Cluster of Documents (3 icons, reduced size, moved DOWN)
        doc_icons = VGroup(*[
            Asset1(sheet_width=1.0, sheet_height=1.3, sheet_color=ManimColor("#F5F5F5"), line_color=ManimColor("#ed8c32"), currency_color=ManimColor("#084993")).scale(0.8).move_to([1.3 + 0.1*i, 1.7 + 0.08*i, 0]).set_z_index(1)
            for i in range(3)
        ])
        
        # Stakeholder Layout - Increased Gap, Graphs inside the gap for safety
        assembly_center = 1.3
        
        # Rotating Gear Logic
        teeth = 8
        inner_r = 0.4 # Scaled down for the gap
        outer_r = 0.5
        points = []
        for i in range(teeth):
            a1 = i * TAU / teeth
            a2 = (i + 0.25) * TAU / teeth
            a3 = (i + 0.5) * TAU / teeth
            a4 = (i + 0.75) * TAU / teeth
            points.append(np.array([inner_r * np.cos(a1), inner_r * np.sin(a1), 0]))
            points.append(np.array([outer_r * np.cos(a2), outer_r * np.sin(a2), 0]))
            points.append(np.array([outer_r * np.cos(a3), outer_r * np.sin(a3), 0]))
            points.append(np.array([inner_r * np.cos(a4), inner_r * np.sin(a4), 0]))

        gear = VMobject()
        gear.set_points_as_corners(points)
        gear.add_line_to(points[0]) 
        gear.set_stroke(ManimColor("#084993"), width=3)
        gear.move_to([assembly_center, -0.6, 0]) # Center between stakeholder boxes
        
        # Gear background and inner hub
        gear_bg = Circle(radius=inner_r, fill_color=ManimColor("#DEEBF7"), fill_opacity=1, stroke_width=0).move_to(gear)
        gear_hub = Circle(radius=inner_r * 0.5, stroke_color=ManimColor("#084993"), stroke_width=2, fill_opacity=0).move_to(gear)
        gear_grp = Group(gear_bg, gear, gear_hub)
        
        # Continuous Rotation
        gear.add_updater(lambda m, dt: m.rotate(dt * 0.5 * PI))
        
        # Sequential Entrance Sequence
        # 1. Documents appear
        self.play(LaggedStart(*[FadeIn(doc) for doc in doc_icons], lag_ratio=0.1), run_time=0.6)
        
        # 2. Arrows/Lines stretch from stack to stakeholder positions
        # Create stakeholder views first to get precise targets (3x Larger per request)
        internal_grp, internal_icon = create_stakeholder_view("Internal Stakeholders", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Internal_Stakeholder.png", [assembly_center - 2.8, -0.6, 0], img_scale=1.35)
        external_grp, external_icon = create_stakeholder_view("External Stakeholders", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/External.png", [assembly_center + 2.8, -0.6, 0], img_scale=1.35)
        
        # Point EXACTLY to the center of the icons
        arrow_l = Line(start=doc_icons.get_center(), end=internal_icon.get_center(), stroke_width=2, stroke_color=ManimColor("#084993"))
        arrow_r = Line(start=doc_icons.get_center(), end=external_icon.get_center(), stroke_width=2, stroke_color=ManimColor("#084993"))
        self.play(Create(arrow_l), Create(arrow_r), run_time=0.6)
        
        # 3. Stakeholder Images + Text appear
        self.play(FadeIn(internal_grp), FadeIn(external_grp), run_time=0.8)
        
        # 4. Bar/Pie graphs appear (Ensure visibility, moved up slightly)
        image_8_s3 = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/image_8.png").scale(0.4).next_to(internal_grp, DOWN, buff=0.2)
        image_9_s3 = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/image_9.png").scale(0.4).next_to(external_grp, DOWN, buff=0.2)
        self.play(FadeIn(image_9_s3), FadeIn(image_8_s3), run_time=0.6)
        
        # 5. Gear appears and starts rotating
        self.play(FadeIn(gear_grp), run_time=0.6)
        
        # Flowing Circle (Yellow circles keep moving)

        # Flowing Circle
        flow_circle = Circle(radius=0.12, fill_color=ManimColor("#ed8c32"), fill_opacity=1, stroke_width=0).move_to(doc_icons.get_center()).set_z_index(2)
        flow_circle.time = 0
        def update_flow(mob, dt):
            mob.time += dt
            t = (mob.time % 2) / 2
            if t < 0.5: # To Internal
                mob.move_to(interpolate(doc_icons.get_center(), internal_icon.get_center(), t*2))
            else: # To External
                mob.move_to(interpolate(doc_icons.get_center(), external_icon.get_center(), (t-0.5)*2))
        
        flow_circle.add_updater(update_flow)
        self.add(flow_circle)
        
        # Insights Area - Gear Removed, wait for flow
        self.wait(9.92)
        
        self.play(
            FadeOut(internal_grp), FadeOut(external_grp), FadeOut(arrow_l), FadeOut(arrow_r),
            FadeOut(image_9_s3), FadeOut(image_8_s3),
            FadeOut(doc_icons), FadeOut(title_grp), FadeOut(bracket), 
            FadeOut(flow_circle), # Ensure yellow circle fades out
            FadeOut(gear_grp), # Added FadeOut(gear_grp)
            run_time=0.8
        )
        flow_circle.remove_updater(update_flow)
        self.remove(internal_grp, external_grp, arrow_l, arrow_r, doc_icons, flow_circle, title_grp, bracket, image_9_s3, image_8_s3)
        
        # New Visuals        ## Section 4 (Asset Flow)
        # Shift icons further LEFT to avoid Section 5 text overlap
        image_11 = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Investor_1.png").scale(1.2).move_to([-2.5, -0.5, 0])
        building_main = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Company.png").scale(3.2).move_to([0.5, -0.5, 0])
        
        self.play(FadeIn(image_11), FadeIn(building_main), run_time=0.8)
        
        # Gold Coin Animation with Border and $ Sign (Investor -> Company)
        def create_coin():
            coin = Circle(radius=0.15, fill_color=ManimColor("#FFD700"), fill_opacity=1, stroke_width=2, stroke_color=ManimColor("#DAA520"))
        # Reversed Path: Investor (image_11) to Company (building_main)
        coin_path = Line(image_11.get_center(), building_main.get_center())
        # Currency Coins - Sequential discrete flow (matching Section 5 logic)
        def create_coin():
            coin_base = Circle(radius=0.15, fill_color=ManimColor("#FFD700"), fill_opacity=1, stroke_width=2, stroke_color=ManimColor("#DAA520"))
            dollar = Text("$", font_size=14, color=ManimColor("#DAA520"), font="Avenir", weight=BOLD).move_to(coin_base.get_center())
            return Group(coin_base, dollar).set_z_index(4)
            
        coin_animations = []
        num_coins = 12
        coins_group = Group() # Create a Group to hold all coins
        for i in range(num_coins):
            coin = create_coin().move_to(image_11.get_center())
            coin.set_opacity(0)
            self.add(coin)
            coins_group.add(coin) # Add coin to the group
            
            # Succession: Wait -> Move -> FadeOut (Matching Section 5 timing)
            coin_anim = Succession(
                Wait(i * 0.3), # Match Section 5 stagger
                FadeIn(coin, run_time=0.05),
                coin.animate.move_to(building_main.get_center()).set_run_time(1.2), # Match Section 5 duration
                FadeOut(coin, run_time=0.1)
            )
            coin_animations.append(coin_anim)
        
        # Character-level FadeIn for Core Insights (Shifted right to avoid building)
        profitable_text = Text("Profitable", font_size=54, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to([1.3 + 3.4, 1.0, 0])
        stable_text = Text("Stable", font_size=54, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to([1.3 + 3.4, 0.0, 0])
        trustworthy_text = Text("Trustworthy", font_size=54, color=ManimColor("#084993"), font="Avenir", weight=BOLD).move_to([1.3 + 3.4, -1.0, 0])
        
        # Sequential word-by-word and letter-by-letter entrance
        self.play(
            Succession(
                LaggedStart(*[FadeIn(char, shift=UP*0.15, rate_func=ease_out_back) for char in profitable_text], lag_ratio=0.08, **{"run_time": 1.0}),
                LaggedStart(*[FadeIn(char, shift=UP*0.15, rate_func=ease_out_back) for char in stable_text], lag_ratio=0.08, **{"run_time": 1.0}),
                LaggedStart(*[FadeIn(char, shift=UP*0.15, rate_func=ease_out_back) for char in trustworthy_text], lag_ratio=0.08, **{"run_time": 1.0}),
            ),
            LaggedStart(*coin_animations, lag_ratio=0),
            run_time=6.02
        )
        ## Section 5
        self.play(FadeOut(profitable_text), FadeOut(stable_text), FadeOut(trustworthy_text), run_time=0.4)
        
        # Final cleanup: Remove all coin objects from scene before building fades out
        self.remove(coins_group)
            
        self.play(FadeOut(building_main), run_time=0.6)
        self.remove(building_main)
        
        # Shift person image RIGHT after building fades out
        self.play(image_11.animate.move_to([-1.0, -0.5, 0]), run_time=0.8)
        
        image_12a = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Company.png").scale(2.4).move_to([1.3 + 1.5, 1.8, 0])
        image_12b = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Company.png").scale(2.4).move_to([1.3 + 1.5, 0.0, 0])
        image_12c = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Company.png").scale(2.4).move_to([1.3 + 1.5, -1.8, 0])
        self.play(FadeIn(image_12a), FadeIn(image_12b), FadeIn(image_12c), run_time=0.5)
        
        self.play(image_11.animate.shift(LEFT * 0.6), run_time=0.6)
        
        tiles_active = []
        
        tile_animations = []

        tile_configs = [
            {"color": ManimColor("#FF6B6B"), "currency": "$", "building": image_12a},
            {"color": ManimColor("#4ECDC4"), "currency": "€", "building": image_12b},
            {"color": ManimColor("#FFE66D"), "currency": "₹", "building": image_12c}
        ]

        spawn_times = [0.8, 1.1, 1.4]

        for spawn_time, config in zip(spawn_times, tile_configs):

            start_pos = config["building"].get_center()
            end_pos = image_11.get_center()

            for i in range(6):  # number of tiles to emit
                tile = Asset1(
                    sheet_width=0.5,
                    sheet_height=0.4,
                    sheet_color=ManimColor("#F5F5F5"),
                    line_color=config["color"],
                    currency_color=ManimColor("#084993")
                ).scale(0.5).move_to(start_pos).set_z_index(1)

                self.add(tile)

                tile_anim = Succession(
                    Wait(spawn_time + i * 0.25),
                    tile.animate.move_to(end_pos).set_run_time(0.8),
                    FadeOut(tile, run_time=0.1)
                )

                tile_animations.append(tile_anim)

        self.play(
            LaggedStart(*tile_animations, lag_ratio=0), **{"run_time": 0.85}
        )
        
        # Investor Coin-Flip Transition (90 deg edge-on flip to Investor_2.png)
        image_11_new = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Investor_2.png").scale(1.2).move_to(image_11.get_center())
        # First half: pivot to edge
        self.play(
            Rotate(image_11, axis=UP, angle=PI/2, about_point=image_11.get_center()),
            run_time=0.25, rate_func=rate_functions.ease_in_sine
        )
        self.remove(image_11)
        # Second half: pivot out from edge
        image_11_new.rotate(PI/2, axis=UP, about_point=image_11_new.get_center())
        self.add(image_11_new)
        self.play(
            Rotate(image_11_new, angle=-PI/2, axis=UP, about_point=image_11_new.get_center()),
            run_time=0.35, rate_func=rate_functions.ease_out_back
        )
        image_11 = image_11_new # Update reference for cleanup
        # time_parser_adjust: self.wait(1.2)
        
        ## Section 6 (Cleanup Chaos)
        self.play(
            FadeOut(image_11), FadeOut(image_12a), FadeOut(image_12b), FadeOut(image_12c),
            run_time=0.8
        )
        self.wait(5.2)
        
        # Move to Meaning of GAAP (Anchor on Left remains)
        self.wait(1)
        
        
        self.wait(1.06)
             ## Section 7 (Meaning of GAAP - Slide 2 Style)
        # Move circles to horizontal header at top
        header_y = 2.5
        circle_spacing = 3.2
        self.play(
            circle_g.animate.move_to([-1.5 * circle_spacing, header_y, 0]).scale(2.0),
            circle_a1.animate.move_to([-0.5 * circle_spacing, header_y, 0]).scale(2.0),
            circle_a2.animate.move_to([0.5 * circle_spacing, header_y, 0]).scale(2.0),
            circle_p.animate.move_to([1.5 * circle_spacing, header_y, 0]).scale(2.0),
            margin_rect.animate.move_to([-8.0, 0, 0]), # Exit to left early
            run_time=1.2
        )
        
        # Vertical Boxes below circles (Perfect Overlap Design)
        box_h = 4.8
        box_w = 2.8
        
        def create_detail_box(label, image_path, pos, color):
            # Rectangle top edge perfectly centered on GAAP circle center
            box_pos = pos + DOWN * (box_h/2) 
            box = RoundedRectangle(width=box_w, height=box_h, corner_radius=0.1, fill_color=color, fill_opacity=1, stroke_width=2, stroke_color=ManimColor("#084993")).move_to(box_pos)
            # Text centered in the box
            text = Text(label, font_size=36, color=ManimColor("#084993"), font="Avenir", weight=BOLD).scale(0.5).move_to(box_pos + UP * 1.2)
            # Mini Icon below text
            icon = ImageMobject(image_path).scale(2.0).move_to(box_pos + DOWN * 0.8)
            return Group(box, text, icon)

        box_g = create_detail_box("GENERALLY", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Generally.png", [-1.5 * circle_spacing, header_y, 0], ManimColor("#E1F5FE"))
        box_a1 = create_detail_box("ACCEPTED", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Accepted.png", [-0.5 * circle_spacing, header_y, 0], ManimColor("#FFF9C4"))
        box_a2 = create_detail_box("ACCOUNTING", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Accounting.png", [0.5 * circle_spacing, header_y, 0], ManimColor("#FFEBEE"))
        box_p = create_detail_box("PRINCIPLES", "/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Procedure.png", [1.5 * circle_spacing, header_y, 0], ManimColor("#E8F5E9"))

        self.play(FadeIn(box_g), FadeIn(box_a1), FadeIn(box_a2), FadeIn(box_p), run_time=1.0)
        
        # Comprehensive Group for scaling/shifting
        full_gaap_grp = Group(circle_g, circle_a1, circle_a2, circle_p, box_g, box_a1, box_a2, box_p)
        self.wait(9.1)
        
        ## Section 8 (Outcomes)
        self.play(full_gaap_grp.animate.scale(0.8).shift(UP * 0.5), run_time=1.0)
        
        box_center = 0
        box_1 = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.2, fill_color=ManimColor("#DEEBF7"), fill_opacity=1, stroke_width=0).move_to([box_center - 2.8, -3.2, 0])
        box_2 = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.2, fill_color=ManimColor("#DEEBF7"), fill_opacity=1, stroke_width=0).move_to([box_center, -3.2, 0])
        box_3 = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.2, fill_color=ManimColor("#DEEBF7"), fill_opacity=1, stroke_width=0).move_to([box_center + 2.8, -3.2, 0])
        
        #box_1.set_opacity(0)
        #box_2.set_opacity(0)
        #box_3.set_opacity(0)
        #self.add(box_1, box_2, box_3)
        self.play(FadeIn(box_1), FadeIn(box_2), FadeIn(box_3), run_time=0.736)
        
        text_uniformity = Text("Uniformity", font_size=36, color=ManimColor("#084993"), font="Avenir", weight=BOLD).scale(0.5).move_to(box_1.get_center() + DOWN * 0.1)
        text_clarity = Text("Clarity", font_size=36, color=ManimColor("#084993"), font="Avenir", weight=BOLD).scale(0.5).move_to(box_2.get_center() + DOWN * 0.1)
        text_comparability = Text("Comparability", font_size=36, color=ManimColor("#084993"), font="Avenir", weight=BOLD).scale(0.5).move_to(box_3.get_center() + DOWN * 0.1)
        
        # Upscaled Outcome Icons (Scale 0.8)
        icon_u = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Uniformity.png").scale(0.8).next_to(box_1, UP, buff=0.15)
        icon_cl = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Clarity.png").scale(0.8).next_to(box_2, UP, buff=0.15)
        icon_com = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_1/Comparability.png").scale(0.8).next_to(box_3, UP, buff=0.15)

        self.play(
            FadeIn(text_uniformity), FadeIn(text_clarity), FadeIn(text_comparability), 
            FadeIn(icon_u), FadeIn(icon_cl), FadeIn(icon_com),
            run_time=0.736
        )
        
        self.wait(5.71)

if __name__ == "__main__":
    config.processes = 4  # Use 4 CPU cores
    config.max_files_cached = 200  # Helps with memory management
    config.progress_bar = "none"
    config.enable_cuda = True
    config.disable_caching = True
    #config.background_color = "#ffffff"
    config.pixel_height = 360
    config.pixel_width = 640
    config.frame_rate = 15
    #config.pixel_height = 180
    #config.pixel_width = 320
    #config.frame_rate = 10
    from pathlib import Path
    import shutil

    scene_to_render = FinalScene()
    scene_to_render.render()

    file_dir = Path(r"../test_raw_videos")
    file_dir.mkdir(exist_ok=True)
    file_name = "group_1.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")