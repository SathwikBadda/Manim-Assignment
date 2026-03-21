from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from group_8 import FullDisclosureScene
except ImportError:
    pass

class TimingScene(FullDisclosureScene):
    def construct(self):
        self.section_times = [self.renderer.time]
        super().construct()
        self.section_times.append(self.renderer.time)
        print("--- Section Times ---")
        for i in range(1, len(self.section_times)):
            print(f"Section {i} actual physical time: {self.section_times[i] - self.section_times[i-1]}")

    def wait(self, duration=1.0, *args, **kwargs):
        super().wait(duration, *args, **kwargs)
        # We can't perfectly intercept sections, but let's just use the parser's logic.
