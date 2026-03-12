from manim import *
import numpy as np

class LLMKnowledgeToGenerationSequence(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(phi=70 * DEGREES, theta=-90 * DEGREES)
        
        globe_center = LEFT * 8 + DOWN * 2.5
        full_height_radius = config.frame_height / 1.4

        globe = Sphere(radius=full_height_radius, resolution=(64, 64))
        globe.set_fill("#89c9d6", opacity=1)
        globe.set_stroke(width=0)
        globe.move_to(globe_center)
        # We explicitly set extremely separated z_indices
        globe.set_z_index(100)

        self.play(FadeIn(globe), run_time=1)
        
        first_line = Text("Online Training", font_size=50, color=BLACK, weight=BOLD)
        first_line.move_to(RIGHT * 1.2 + UP * 1.3)
        full_sentence = Text("An efficient way to deliver knowledge", font_size=40, color=BLACK, weight=BOLD)
        full_sentence.scale_to_fit_width(5)
        full_sentence.next_to(first_line, DOWN, aligned_edge=LEFT)
        text_group = VGroup(first_line, full_sentence)
        
        curve_radius = full_height_radius + 2 
        def curve_text_func(point):
            center_x = text_group.get_center()[0]
            theta = (point[0] - center_x) / curve_radius
            new_x = center_x + curve_radius * np.sin(theta)
            new_z = point[2] + curve_radius * (np.cos(theta) - 1) 
            return np.array([new_x, point[1], new_z])

        text_group.apply_function(curve_text_func)
        text_group.rotate(70 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        text_group.shift(IN * 0.05) 
        text_group.set_z_index(-100) 
        
        camera_down_vector = np.array([0, -np.cos(70 * DEGREES), -np.sin(70 * DEGREES)])
        
        self.play(FadeIn(first_line, shift=camera_down_vector * 0.3), run_time=1.5)
        self.move_camera(zoom=1.35, frame_center=LEFT * 1.5, run_time=2.5, rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(full_sentence, shift=camera_down_vector * 0.45), run_time=2, rate_func=rate_functions.ease_out_cubic)
        
        self.wait(1)

        # Print out the calculated z index before playing
        print("Globe Z index:", globe.z_index)
        print("Text Z index:", first_line.z_index)
        
        self.play(
            first_line.animate.shift(LEFT * 7.5),
            full_sentence.animate.shift(LEFT * 7.5),
            Rotate(globe, angle=0.6 * 2.5, axis=OUT),
            run_time=2.5,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.wait(2)
        print("Test Complete")
