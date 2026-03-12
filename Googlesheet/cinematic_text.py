
## 0 - 3 Introducing ElevenLabs Conversational Agents

from manim import *
import numpy as np

class CinematicTypography(Scene):
    def construct(self):
        self.camera.background_color = ManimColor("#000000")

        # ── SCENE 1 TEXT ──────────────────────────────────────────
        t1_building = Text("Building", font_size=60, font="sans-serif", weight=BOLD, color=WHITE)
        t1_ai = Text("AI agents", font_size=60, font="sans-serif", weight=BOLD)
        t1_ai.set_color_by_gradient(ManimColor("#F472B6"), ManimColor("#A78BFA")) # Pink to Lavender/Purple
        t1_speak = Text("that can speak", font_size=60, font="sans-serif", weight=BOLD)
        t1_speak.set_color_by_gradient(ManimColor("#60A5FA"), ManimColor("#22D3EE")) # Blue to Cyan

        scene1 = VGroup(t1_building, t1_ai, t1_speak)
        scene1.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        scene1.move_to(ORIGIN)

        # ── SCENE 2 TEXT ──────────────────────────────────────────
        t2_isnow = Text("is now", font_size=60, font="sans-serif", weight=BOLD, color=WHITE)
        
        t2_easier = Text("easier", font_size=60, font="sans-serif", weight=BOLD)
        t2_easier.set_color_by_gradient(ManimColor("#F472B6"), ManimColor("#A78BFA"))
        
        t2_than = Text("than ever.", font_size=60, font="sans-serif", weight=BOLD, color=WHITE)

        scene2 = VGroup(t2_isnow, t2_easier, t2_than)
        scene2.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        scene2.move_to(ORIGIN)

        # ── PHASE 1: Entrance Scene 1 ──────────────────────────────
        entrance_ai = [FadeIn(char, shift=UP*0.15) for char in t1_ai]
        entrance_speak = [FadeIn(char, shift=UP*0.15) for char in t1_speak]
        
        self.play(
            AnimationGroup(
                FadeIn(t1_building, shift=UP*0.15),
                LaggedStart(*entrance_ai, lag_ratio=0.02),
                LaggedStart(*entrance_speak, lag_ratio=0.02),
                lag_ratio=0.05
            ),
            run_time=0.8,
            rate_func=smooth,
        )

        self.wait(0.6)

        # ── PHASE 2: Scene 1 Exit (Custom Request) ────────────────—
        exit_ai = [FadeOut(char, shift=UP*0.2) for char in t1_ai]
        exit_speak = [FadeOut(char, shift=UP*0.2) for char in t1_speak]
        
        self.play(
            FadeOut(t1_building, shift=UP*0.25, run_time=0.2),
            LaggedStart(*exit_ai, lag_ratio=0.015),
            LaggedStart(*exit_speak, lag_ratio=0.015),
            run_time=0.6,
            rate_func=smooth
        )

        # ── PHASE 3: Scene 2 Entrance ──────────────────────────────
        entrance_t2_isnow = [FadeIn(char, shift=UP*0.15) for char in t2_isnow]
        entrance_t2_easier = [FadeIn(char, shift=UP*0.15) for char in t2_easier]
        entrance_t2_than = [FadeIn(char, shift=UP*0.15) for char in t2_than]

        self.play(
            LaggedStart(*entrance_t2_isnow, *entrance_t2_easier, *entrance_t2_than, lag_ratio=0.015),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(0.6)
        
        # ── PHASE 4: Scene 2 Exit (Increase/Zoom Out) ───────────────
        # Scale up massively and fade out to simulate zooming past the camera
        self.play(
            scene2.animate.scale(15).set_opacity(0),
            run_time=0.5,
            rate_func=rush_into
        )
        self.wait(0.1)
