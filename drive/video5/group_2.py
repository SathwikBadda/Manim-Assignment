from manim import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from manim_asset_codes.asset_2 import Asset2
import numpy as np

class FinalScene(ThreeDScene):
    def construct(self):

        self.camera.background_color = "#FFFFFF"
        
        ## Section 1: Asset Setup (Using Images)
        factory_left = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/EV_1.png").scale(1.6)
        factory_right = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/EV2.png").scale(1.6)
        car_left = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/Car_1.png").scale(1.275)
        car_right = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/Car_2.png").scale(1.275)
        
        # Positions (Adjusted for new larger cars/smaller factories)
        factory_left.move_to(LEFT * 3.5 + UP * 1.8)
        factory_right.move_to(RIGHT * 3.5 + UP * 1.8)
        car_left.move_to(LEFT * 3.2 + UP * 0.2)
        car_right.move_to(RIGHT * 3.2 + UP * 0.2)
        
        # Stacking order
        factory_left.set_z_index(2)
        factory_right.set_z_index(2)
        car_left.set_z_index(3)
        car_right.set_z_index(3)
        
        # Entrance Animation (FadeIn automatically adds them)
        self.play(
            FadeIn(factory_left, scale=0.8),
            FadeIn(factory_right, scale=0.8),
            FadeIn(car_left, scale=0.8),
            FadeIn(car_right, scale=0.8),
            run_time=0.8
        )
        self.wait(0.75)
        
        # Pulse effect for both factories
        self.play(
            factory_left.animate.scale(1.1),
            factory_right.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.3
        )
        
        self.wait(0.4)
        
        # Final position adjustment if needed
        self.play(
            factory_left.animate.shift(UP * 0.2),
            factory_right.animate.shift(UP * 0.2),
            run_time=0.6
        )
        
        self.wait(0.2)
        
        ## Section 2: Revenue Cycle Left
        customer_left = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/Customer_1.png").scale(1.1)
        customer_left.move_to(LEFT * 4.0 + DOWN * 2.8)
        
        self.play(FadeIn(customer_left, scale=0.8), run_time=0.67)
        
        # Curved Dashed Path for Left (Curves EXTREME OUTWARD to the left)
        arc_l = ArcBetweenPoints(
            start=customer_left.get_top() + UP * 0.2,
            end=factory_left.get_bottom(),
            angle=-TAU/2.5
        )
        arrow_path = DashedVMobject(arc_l, num_dashes=15).set_color(ManimColor("#084993"))
        
        self.play(Create(arrow_path), run_time=0.87)
        
        self.wait(0.2)
        
        order_text = Text("Order", font="Montserrat", weight=BOLD, font_size=24, color=ManimColor("#084993"))
        order_text.add_background_rectangle(opacity=1, color=WHITE, buff=0.1)
        order_text.move_to(customer_left.get_top() + UP * 0.2)
        
        self.play(FadeIn(order_text), run_time=0.4)
        
        # Move Along the Curve
        order_path_anim = MoveAlongPath(
            order_text,
            arc_l,
            run_time=0.8
        )
        
        self.play(order_path_anim)
        self.play(FadeOut(order_text), run_time=0.2)
        
        self.wait(0.73)
        
        # Gold Revenue Text (Small -> Large Growth)
        revenue_text_left = Text("+ REVENUE", font="Montserrat", weight=BOLD, font_size=36, color="#FFD700")
        revenue_text_left.set_z_index(1) 
        revenue_text_left.move_to(factory_left.get_center()).scale(0.1)
        
        self.play(
            revenue_text_left.animate.shift(UP * 2.0).scale(15.0).set_opacity(0),
            run_time=1.2
        )
        
        self.play(FadeOut(arrow_path), run_time=0.1)
        
        
        ## Section 3: Revenue Cycle Right
        customer_right = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/Scene_2/Customer_2.png").scale(1.1)
        customer_right.move_to(RIGHT * 4.0 + DOWN * 2.8)
        
        self.play(FadeIn(customer_right, scale=0.8), run_time=0.47)
        
        # Curved Dashed Path for Right (Curves OUTWARD to the right)
        arc_r = ArcBetweenPoints(
            start=customer_right.get_top() + UP * 0.2,
            end=factory_right.get_bottom(),
            angle=TAU/4
        )
        arrow_path_right = DashedVMobject(arc_r, num_dashes=15).set_color(ManimColor("#084993"))
        
        self.play(Create(arrow_path_right), run_time=0.67)
        
        self.wait(0.2)
        
        # Yellow Coin (Primitive for better color control)
        coin_core = Circle(radius=0.2, fill_color=YELLOW, fill_opacity=1, stroke_width=2, stroke_color=ManimColor("#b58900"))
        coin_sym = Text("$", color=BLACK, font_size=20, weight=BOLD).move_to(coin_core.get_center())
        coin = VGroup(coin_core, coin_sym)
        coin.move_to(customer_right.get_top() + UP * 0.2)
        
        self.play(FadeIn(coin), run_time=0.4)
        
        # Move Along the Curve
        coin_path_anim = MoveAlongPath(coin, arc_r)
        
        self.play(coin_path_anim, run_time=0.8)
        self.play(FadeOut(coin), run_time=0.2)

        
        # Gold Revenue Text (Small -> Large Growth)
        revenue_text_right = Text("+ REVENUE", font="Montserrat", weight=BOLD, font_size=36, color="#FFD700")
        revenue_text_right.set_z_index(1)
        revenue_text_right.move_to(factory_right.get_center()).scale(0.1)
        
        self.play(
            revenue_text_right.animate.shift(UP * 2.0).scale(15.0).set_opacity(0),
            run_time=0.5
        )
        
        self.play(FadeOut(arrow_path_right), run_time=0.1)
        
        ## Section 4: Car Movement
        self.wait(2.15)
        self.wait(2.16)

        # ✅ FIX: time tracker
        elapsed_time = ValueTracker(0)
        elapsed_time.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(elapsed_time)

        def drift_left(mob, dt):
            t = elapsed_time.get_value()
            offset = 0.08 * np.sin(2 * np.pi * (t / 5.17))
            mob.shift(RIGHT * offset * dt / 5.17)

        def drift_right(mob, dt):
            t = elapsed_time.get_value()
            offset = 0.08 * np.sin(2 * np.pi * (t / 5.17))
            mob.shift(RIGHT * offset * dt / 5.17)

        car_left.add_updater(drift_left)
        car_right.add_updater(drift_right)

        # Car setup for final movement
        car_left.remove_updater(drift_left) if hasattr(car_left, 'updaters') else None
        car_right.remove_updater(drift_right) if hasattr(car_right, 'updaters') else None
        
        car_left_move = car_left.animate.move_to(customer_left.get_center()).set_opacity(0.0)
        car_right_move = car_right.animate.move_to(customer_right.get_center()).set_opacity(0.0)

        # 1. Cars Move to Customers
        self.play(car_left_move, car_right_move, run_time=3.0)

        # Final Simultaneous Revenue Texts
        revenue_final_left = Text("+ REVENUE", font="Montserrat", weight=BOLD, font_size=36, color="#FFD700")
        revenue_final_left.set_z_index(1)
        revenue_final_left.move_to(factory_left.get_center()).scale(0.1)
        
        revenue_final_right = Text("+ REVENUE", font="Montserrat", weight=BOLD, font_size=36, color="#FFD700")
        revenue_final_right.set_z_index(1)
        revenue_final_right.move_to(factory_right.get_center()).scale(0.1)
        
        # 2. Sequential Bonus: Dual Revenue growth triggered AFTER car move
        self.play(
            revenue_final_left.animate.shift(UP * 2.5).scale(15.0).set_opacity(0),
            revenue_final_right.animate.shift(UP * 2.5).scale(15.0).set_opacity(0),
            run_time=2.5
        )
        
        self.wait(0.53)

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
    file_name = "group_2.mp4"
    file_path = file_dir / file_name
    

    try:
        media_dir = Path("media/videos")
        latest_video = sorted(media_dir.glob("**/*.mp4"),
                                key=lambda f: f.stat().st_mtime, reverse=True)[0]
        shutil.move(str(latest_video), str(file_path))
        print(f"Video moved to {file_path}")
    except IndexError:
        print("No video file was generated by Manim.")