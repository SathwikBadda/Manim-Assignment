## 26 -31 Introducing ElevenLabs Conversational Agents

from manim import *
import numpy as np


class PipelineToCircle(Scene):
    def construct(self):
        self.camera.background_color = ManimColor("#F8F8F8")

        import os
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, "images")
        
        img_names = [
            "google_calendar.png",
            "google_drive.png",
            "youtube.png",
            "google_meet.png",
            "google_sheets.png",
            "google_docs.png",
            "gmail.png",
            "google_slides.png",
        ]
        
        card_data = [
            ("Transcription", img_names[0]),
            ("Turn taking", img_names[1]),
            ("LLM", img_names[2]),
            ("Knowledge\nbase", img_names[3]),
            ("Text-to-\nSpeech", img_names[4]),
            ("Testing", img_names[5]),
            ("Phone", img_names[6]),
            ("Website", img_names[7]),
        ]

        # ── Icon card builder ──────────────────────────────────────
        def make_card(label, img_filename, width=1.22, height=1.22):
            bg = RoundedRectangle(
                corner_radius=0.18, width=width, height=height,
                fill_color=ManimColor("#EBEBEB"),
                fill_opacity=1, stroke_width=0,
            )
            
            img_path = os.path.join(images_dir, img_filename)
            icon = ImageMobject(img_path)
            icon.height = 0.55 # Scale icon nicely into the box
            icon.move_to(bg.get_center() + DOWN * 0.1)

            lines = label.split("\n")
            if len(lines) == 2:
                lbl = VGroup(
                    Text(lines[0], font_size=13, color=ManimColor("#333333"), weight=BOLD),
                    Text(lines[1], font_size=13, color=ManimColor("#333333"), weight=BOLD),
                ).arrange(DOWN, buff=0.03)
            else:
                lbl = Text(label, font_size=13, color=ManimColor("#333333"), weight=BOLD)
            lbl.move_to(bg.get_top() + DOWN * 0.22)
            
            return Group(bg, lbl, icon)

        cards = Group(*[make_card(lbl, img) for lbl, img in card_data])

        # ── PHASE 1: Linear horizontal layout ─────────────────────
        pipeline_positions = []
        total = len(cards)
        spacing = 1.65 # Slightly wider to prevent line cramping
        start_x = -(total - 1) * spacing / 2
        for i in range(total):
            pipeline_positions.append(np.array([start_x + i * spacing, -0.15, 0]))

        # Dashed connectors between cards (With Vector Math anti-clipping)
        connectors = VGroup()
        card_radius = 1.22 / 2 + 0.05 # Add tiny buffer 0.05 to ensure visual gap
        
        for i in range(total - 1):
            p1 = pipeline_positions[i]
            p2 = pipeline_positions[i + 1]
            
            # Linear direction vector
            direction = (p2 - p1)
            dist = np.linalg.norm(direction)
            unit_dir = direction / dist
            
            # Offset start and end points by card_radius
            start_p = p1 + unit_dir * card_radius
            end_p = p2 - unit_dir * card_radius
            
            # Give a slight arch for visual flair
            mid_up = (start_p + end_p) / 2 + UP * 0.65
            path = CubicBezier(start_p, mid_up, mid_up, end_p,
                               stroke_width=1.8, stroke_color=ManimColor("#AAAAAA"))
            dashed = DashedVMobject(path, num_dashes=12, dashed_ratio=0.5)
            connectors.add(dashed)

        for card, pos in zip(cards, pipeline_positions):
            card.move_to(pos)
            # Cannot use set_opacity directly on Group with images nicely; apply to elements
            for el in card: el.set_opacity(0)
            
        self.add(cards) # Add only cards first to keep connectors hidden

        # Scale down to fit screen
        pipeline_group = Group(cards, connectors)
        pipeline_group.scale(0.82)

        # Fade in cards
        fade_anims = []
        for card in cards:
            fade_anims.append(Restore(card.copy().set_opacity(1), rate_func=smooth)) # Hack generic fade for Groups
        
        # Manually force opacity 1 onto the real cards for final state rendering
        # Because we need complex fading for ImageMobjects
        def fade_in_group(group):
            anims = []
            for sub in group:
                if type(sub) is ImageMobject:
                    sub.set_opacity(0.0) # Prepare
                    anims.append(sub.animate.set_opacity(1.0))
                else:
                    anims.append(sub.animate.set_opacity(1.0))
            return AnimationGroup(*anims)
        
        self.play(
            LaggedStart(
                *[fade_in_group(card) for card in cards],
                lag_ratio=0.13
            ),
            run_time=1.6, rate_func=smooth,
        )
        
        # Draw connectors sequentially one by one (True Wave)
        self.play(
            LaggedStart(
                *[Create(line, run_time=0.4) for line in connectors],
                lag_ratio=0.8
            ),
            rate_func=linear
        )
        self.wait(0.6)

        # ── PHASE 2: Transition to Circular layout ──────────────────────────────
        n = len(cards)
        circle_radius = 2.85
        circle_center = np.array([0.0, -0.1, 0])
        circle_positions = [
            circle_center + np.array([
                circle_radius * np.cos(PI / 2 + 2 * PI * i / n),
                circle_radius * np.sin(PI / 2 + 2 * PI * i / n),
                0
            ])
            for i in range(n)
        ]

        self.play(
            FadeOut(connectors),
            *[cards[i].animate.move_to(circle_positions[i])
              for i in range(n)],
            run_time=1.5, rate_func=smooth,
        )

        # Draw circular connectors (With Vector Math anti-clipping)
        circle_connectors = VGroup()
        for i in range(n):
            p1 = circle_positions[i]
            p2 = circle_positions[(i + 1) % n]
            
            # Calculate direction vector between cards
            direction = (p2 - p1)
            dist = np.linalg.norm(direction)
            unit_dir = direction / dist
            
            # Offset the line start/end points identically off the cards edge
            # So they only touch, never overlap the background.
            start_p = p1 + unit_dir * card_radius
            end_p = p2 - unit_dir * card_radius
            
            line = DashedLine(
                start_p, end_p,
                dash_length=0.1, dashed_ratio=0.5,
                stroke_width=1.5, stroke_color=ManimColor("#AAAAAA")
            )
            circle_connectors.add(line)
            
        # Draw circular connectors sequentially one by one (True Wave)
        self.play(
            LaggedStart(
                *[Create(line, run_time=0.4) for line in circle_connectors],
                lag_ratio=0.8
            ),
            rate_func=linear
        )

        self.wait(1.5)
