from manim import *
import numpy as np

class LLMKnowledgeToGenerationSequence(ThreeDScene):
    def construct(self):
        globe_center = LEFT * 8 + DOWN * 2.5
        full_height_radius = config.frame_height / 1.4

        globe = Sphere(radius=full_height_radius, resolution=(64, 64))
        globe.set_fill("#89c9d6", opacity=1)
        globe.set_stroke(width=0)
        globe.move_to(globe_center)
        
        first_line = Text("Online Training", font_size=50)
        first_line.move_to(RIGHT * 1.2 + UP * 1.3)
        full_sentence = Text("An efficient way to deliver knowledge", font_size=40)
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
        
        char_n = first_line[1] # 'n' in "Online"
        
        for dx in np.linspace(4.0, 7.5, 30):
            pos_left = char_n.get_left() + LEFT * dx
            pos_center = char_n.get_center() + LEFT * dx
            print(f"dx={dx:.2f}, center_x={pos_center[0]:.2f}, left_x={pos_left[0]:.2f}")

if __name__ == "__main__":
    from manim.__main__ import main
    import sys
    sys.argv = ["manim", "test_clip.py", "LLMKnowledgeToGenerationSequence", "-ql", "-v", "WARNING"]
    main()
