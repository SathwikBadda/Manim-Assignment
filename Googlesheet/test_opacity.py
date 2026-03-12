from manim import *

class TestOpacity(Scene):
    def construct(self):
        text = Text("Hello World")
        self.add(text)
        self.play(text.animate.shift(LEFT*2).set_opacity(0))

if __name__ == "__main__":
    from manim.__main__ import main
    import sys
    sys.argv = ["manim", "test_opacity.py", "TestOpacity", "-ql", "-v", "WARNING"]
    main()
