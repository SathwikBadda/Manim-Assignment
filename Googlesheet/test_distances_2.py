from manim import *
import numpy as np

class LLMKnowledgeToGenerationSequence(ThreeDScene):
    def construct(self):
        globe_center = LEFT * 8 + DOWN * 2.5
        full_height_radius = 8 / 1.4

        first_line = Text("Online Training", font_size=50)
        first_line.move_to(RIGHT * 1.2 + UP * 1.3)
        full_sentence = Text("An efficient way to deliver knowledge", font_size=40)
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
        
        # Test character "A" in "An"
        char_A = full_sentence[0]
        
        for dx in np.linspace(4.0, 7.5, 30):
            pos_right = char_A.get_right() + LEFT * dx
            dist = np.linalg.norm(pos_right - globe_center)
            print(f"dx={dx:.2f}, right_x={pos_right[0]:.2f}, dist={dist:.4f}")

if __name__ == "__main__":
    from manim.__main__ import main
    import sys
    sys.argv = ["manim", "test_distances_2.py", "LLMKnowledgeToGenerationSequence", "-ql", "-v", "WARNING"]
    main()
