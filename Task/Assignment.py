from manim import *
import numpy as np

class PhilosophicalSeeker(Scene):
    def construct(self):
        # ========================================
        # CONFIGURATION
        # ========================================
        self.camera.background_color = "#0a0a0a"
        
        # ========================================
        # 1. BACKGROUND - SINGLE INTERSECTION (+)
        # ========================================
        
        # User requested "only one intersection like (+)" and "no boxes"
        # So we create two infinite lines crossing at the origin
        
        h_line = Line(LEFT * 50, RIGHT * 50, stroke_width=2, color=BLUE_E)
        v_line = Line(UP * 50, DOWN * 50, stroke_width=2, color=BLUE_E)
        
        background_cross = VGroup(h_line, v_line)
        background_cross.set_z_index(-1) # FORCE BACK LAYER
        
        # Time tracker for continuous updates
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(time_tracker)
        
        # Updater 1: Continuous left-to-right drift
        # This will move the vertical line right, effectively moving the intersection
        drift_speed = 0.2
        def drift_updater(mob, dt):
            mob.shift(RIGHT * drift_speed * dt)
        
        background_cross.add_updater(drift_updater)
        
        # Updater 2: Fluctuating Opacity (Extreme range as requested)
        # 0.1 to 0.9 opacity
        def opacity_updater(mob):
            t = time_tracker.get_value()
            # sin goes from -1 to 1. 
            # We want  0.1 to 0.9
            # Range is 0.8. Midpoint is 0.5.
            # 0.5 + 0.4 * sin(t) -> goes from 0.1 to 0.9
            new_opacity = 0.5 + 0.4 * np.sin(0.5 * t)
            mob.set_stroke(opacity=new_opacity)
            
        background_cross.add_updater(opacity_updater)
        
        self.add(background_cross)
        
        # ========================================
        # 2. CENTRAL FIGURE - THINKING SEEKER
        # ========================================
        
        # 1. HEAD & FACE
        head_group = VGroup()
        face = Circle(radius=0.3, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=3)
        
        # Eyes (small dots)
        left_eye = Dot(point=face.get_center() + np.array([-0.1, 0.05, 0]), radius=0.03, color=WHITE)
        right_eye = Dot(point=face.get_center() + np.array([0.1, 0.05, 0]), radius=0.03, color=WHITE)
        
        # Nose (small vertical line)
        nose = Line(face.get_center() + np.array([0, 0, 0]), face.get_center() + np.array([0, -0.05, 0]), color=WHITE, stroke_width=2)
        
        # Mouth (small arc)
        mouth = Arc(radius=0.1, start_angle=-150*DEGREES, angle=120*DEGREES, color=WHITE, stroke_width=2)
        mouth.move_to(face.get_center() + DOWN * 0.15)
        
        # Ears (small arcs)
        left_ear = Arc(radius=0.08, start_angle=90*DEGREES, angle=180*DEGREES, color=WHITE, stroke_width=2).next_to(face, LEFT, buff=-0.05)
        right_ear = Arc(radius=0.08, start_angle=-90*DEGREES, angle=180*DEGREES, color=WHITE, stroke_width=2).next_to(face, RIGHT, buff=-0.05)
        
        head_group.add(face, left_eye, right_eye, nose, mouth, left_ear, right_ear)
        head_group.shift(UP * 0.5) 
        
        # 2. BODY & POSE
        body_top = head_group.get_bottom() + UP * 0.05
        body_bottom = body_top + DOWN * 1.2
        body_line = Line(body_top, body_bottom, color=WHITE, stroke_width=3)
        
        # Legs
        left_leg = Line(body_bottom, body_bottom + DOWN * 0.8 + LEFT * 0.4, color=WHITE, stroke_width=3)
        right_leg = Line(body_bottom, body_bottom + DOWN * 0.8 + RIGHT * 0.4, color=WHITE, stroke_width=3)
        
        # Arms - Correct Thinking Pose
        # Right Arm: Hand on chin
        shoulder_right = body_top + DOWN * 0.2
        # Elbow out to the right
        elbow_right = shoulder_right + RIGHT * 0.6 + DOWN * 0.1
        # Hand touches chin area
        hand_right_pos = head_group.get_bottom() + RIGHT * 0.15 + DOWN * 0.1
        
        arm_right_upper = Line(shoulder_right, elbow_right, color=WHITE, stroke_width=3)
        arm_right_lower = Line(elbow_right, hand_right_pos, color=WHITE, stroke_width=3)
        
        # Left Arm: Crossing body to support right elbow
        shoulder_left = body_top + DOWN * 0.2
        # Elbow slightly out to left
        elbow_left = shoulder_left + LEFT * 0.2 + DOWN * 0.4
        # Hand meets right elbow
        hand_left_pos = elbow_right + DOWN * 0.05 + LEFT * 0.1
        
        arm_left_upper = Line(shoulder_left, elbow_left, color=WHITE, stroke_width=3)
        arm_left_lower = Line(elbow_left, hand_left_pos, color=WHITE, stroke_width=3)
        
        seeker_figure = VGroup(
            head_group, body_line, left_leg, right_leg, 
            arm_right_upper, arm_right_lower, 
            arm_left_upper, arm_left_lower
        )
        seeker_figure.move_to(DOWN * 1.5)
        seeker_figure.scale(0.8) 
        
        # ========================================
        # 3. THOUGHT BUBBLE & TEXT
        # ========================================
        
        # Create Thinking Bubble (Cloud shape)
        bubble_center = UP * 1.5
        
        c1 = Circle(radius=0.9).move_to(bubble_center)
        c2 = Circle(radius=0.7).move_to(bubble_center + LEFT * 1.1 + DOWN * 0.2)
        c3 = Circle(radius=0.7).move_to(bubble_center + RIGHT * 1.1 + DOWN * 0.2)
        c4 = Circle(radius=0.6).move_to(bubble_center + UP * 0.9)
        c5 = Circle(radius=0.6).move_to(bubble_center + LEFT * 0.7 + UP * 0.7)
        c6 = Circle(radius=0.6).move_to(bubble_center + RIGHT * 0.7 + UP * 0.7)
        
        cloud_body = VGroup(c1, c2, c3, c4, c5, c6)
        cloud_outline = Union(c1, c2, c3, c4, c5, c6)
        cloud_outline.set_stroke(WHITE, width=3)
        cloud_outline.set_fill(BLACK, opacity=1)
        
        # Trailing dots
        d1 = Circle(radius=0.08, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=2).move_to(seeker_figure.get_top() + UP * 0.2 + RIGHT * 0.3)
        d2 = Circle(radius=0.12, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=2).move_to(seeker_figure.get_top() + UP * 0.5 + RIGHT * 0.4)
        d3 = Circle(radius=0.18, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=2).move_to(seeker_figure.get_top() + UP * 0.9 + RIGHT * 0.3)
        
        thought_bubbles = VGroup(cloud_outline, d1, d2, d3)
        
        # Text "Welcome to Kplor" inside the bubble
        # Reduced font size to avoid collision
        text_content = Text("Welcome to Kplor", font_size=24, color=WHITE)
        text_content.move_to(cloud_outline.get_center())
        
        full_bubble = VGroup(thought_bubbles, text_content)
        full_group = VGroup(seeker_figure, full_bubble)
        full_group.set_z_index(10) # FORCE FRONT LAYER
        
        # Animation: 
        self.play(FadeIn(seeker_figure), run_time=1)
        self.play(Write(thought_bubbles), run_time=1)
        self.play(Write(text_content), run_time=1)
        
        # ========================================
        # 4. QUESTION MARKS - UNCERTAINTY MOTIF
        # ========================================
        
        question_marks = VGroup()
        offsets = [
            [-5, 3, 0], [5, 3, 0],
            [-5, -3, 0], [5, -3, 0],
            [-6, 0, 0], [6, 0, 0]
        ]
        
        for i, offset in enumerate(offsets):
            q = Tex("?", font_size=40, color=WHITE)
            q.move_to(np.array(offset))
            q.set_opacity(0.8) # Increased opacity as requested
            q.set_z_index(5) # Middle layer
            
            # Simple rotation
            q.add_updater(lambda m, dt: m.rotate(0.5 * dt, axis=UP))
            question_marks.add(q)
            
        self.play(FadeIn(question_marks), run_time=1)
        
        # Hold
        self.wait(8)