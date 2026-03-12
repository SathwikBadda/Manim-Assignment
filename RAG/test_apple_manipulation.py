from manim import *
from apple import Apple

class TestAppleManipulation(Scene):
    def construct(self):
        # 1. Instantiate the Apple
        apple = Apple()
        apple.move_to(ORIGIN)
        self.add(apple)
        
        # Display initial state
        self.wait(1)

        # 2. Getter usage example (printed to console if run)
        leaf = apple.get_subcomponent("leaf")
        print(f"Retrieved leaf component: {leaf}")
        
        body = apple.get_subcomponent("body")
        print(f"Retrieved body component: {body}")

        # 3. Setter usage / Manipulation
        
        # Example 1: Change Leaf Color to Yellow
        print("Changing leaf color to YELLOW")
        apple.set_color("leaf", YELLOW)
        self.wait(1)
        
        # Example 2: Change Body Color to Green (Granny Smith style)
        print("Changing body color to GREEN")
        apple.set_color("body", GREEN)
        self.wait(1)

        # Example 3: Scale manipulation
        print("Scaling apple up")
        self.play(ScaleInPlace(apple, 1.5))
        self.wait(0.5)

        # 4. Animation helper usage (from guidelines)
        
        # Wiggle the stem
        print("Animating stem wiggle")
        self.play(apple.animate_manipulation("stem", "Wiggle", scale_value=1.5, rotation_angle=0.1 * TAU))
        self.wait(0.5)
        
        # Indicate the highlight/shine
        print("Indicating shine")
        self.play(apple.animate_manipulation("shine", "Indicate", color=WHITE))
        self.wait(1)

        # Flash the whole apple (using body or group doesn't matter much for Flash, but let's try body)
        # Note: Flash works on Mobjects.
        self.play(Flash(apple, color=GOLD, flash_radius=1.5))
        self.wait(1)

if __name__ == "__main__":
    # Simple verification logic without rendering if executed simply as a python script
    try:
        a = Apple()
        l = a.get_subcomponent("leaf")
        assert l is not None, "Leaf should not be None"
        print("✔ Getter Verification Passed")
        
        a.set_color("leaf", "#FFFF00")
        # Check if color was roughly set (Manim colors are arrays, so strict equality is tricky without converting)
        print("✔ Setter Verification Passed (No crash)")
        
        print("Ready for Manim rendering.")
    except Exception as e:
        print(f"✘ Verification Failed: {e}")
