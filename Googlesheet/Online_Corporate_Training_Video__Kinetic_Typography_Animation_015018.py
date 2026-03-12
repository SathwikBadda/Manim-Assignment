"""
================================================================================
RAG / LLM Context Metadata:
- Domain: Python Animation, Data Visualization, 3D Geometry
- Framework: Manim (Community Edition)
- Class Type: ThreeDScene (Allows manipulation of the camera via phi/theta angles)
- Key Concepts: 
    1. Explicit 3D Camera Positioning (phi, theta, and move_camera)
    2. Mathematical Deformation (apply_function to map 2D text onto a 3D arc)
    3. Viewport Alignment (Rotating 3D objects to perfectly face a tilted camera)
    4. Z-Index Occlusion (Using rendering order to hide text behind a solid sphere)
    5. Imperative Execution (No updaters, no procedural loops, explicit definitions)

FIX SUMMARY (v2 — minimal, positions/sizes unchanged):
- Root cause: In ThreeDScene, Manim uses a 3D depth (z-buffer) renderer, 
  which IGNORES z_index entirely for 3D objects like Sphere. z_index only 
  affects 2D mobjects layered in screen space.
- FIX: The Sphere is replaced with a combination of:
    1. A large solid Circle (2D, facing camera) at z_index=10 — this IS 
       respected by the 2D compositor and will always render over text.
    2. The original Sphere kept purely for the 3D visual/shading aesthetics 
       at z_index=10. 
- The critical addition is a flat opaque Circle "mask" rotated to face the 
  camera at phi=70°, placed at the exact same screen position as the sphere.
  Because it is a 2D VMobject, z_index=10 is fully honored, guaranteeing 
  the sphere visually occludes the text (z_index=-1) during the shift.
- ALL original coordinates, sphere size, and camera settings are preserved.
================================================================================
"""

from manim import *
import numpy as np


class LLMKnowledgeToGenerationSequence(ThreeDScene):
    """
    Flattened, linear implementation of a 3D text wrapping and occlusion sequence.
    Sphere occludes moving text via a 2D Circle mask at high z_index.
    """

    def construct(self):
        # ==================================================
        # CHUNK 1: EXPLICIT 3D CAMERA SETUP
        # ==================================================
        self.camera.background_color = WHITE
        self.set_camera_orientation(phi=70 * DEGREES, theta=-90 * DEGREES)

        # ==================================================
        # CHUNK 2: SPHERE + 2D OCCLUSION MASK
        # 
        # ORIGINAL positions and radius are fully preserved.
        # FIX: A flat Circle (VMobject) at the same screen location is added.
        # Because ThreeDScene's depth renderer ignores z_index on 3D objects,
        # this 2D Circle at z_index=10 is what actually enforces occlusion.
        # ==================================================
        globe_center = LEFT * 8 + DOWN * 2.5          # ← UNCHANGED
        full_height_radius = config.frame_height / 1.4  # ← UNCHANGED

        globe = Sphere(
            radius=full_height_radius,
            resolution=(64, 64)
        )
        globe.set_fill("#89c9d6", opacity=1)
        globe.set_stroke(width=0)
        globe.move_to(globe_center)
        globe.set_z_index(10)

        # --- 2D OCCLUSION MASK (THE KEY FIX) ---
        # A Circle with the same color and radius as the sphere, rotated to
        # face the camera (phi=70°). Being a VMobject, its z_index=10 IS
        # honored by Manim's compositor, so it always renders on top of the
        # text (z_index=-1) regardless of 3D depth sorting.
        occlusion_mask = Circle(
            radius=full_height_radius,
            fill_color="#89c9d6",
            fill_opacity=1,
            stroke_width=0
        )
        # Rotate to align with the tilted camera plane
        occlusion_mask.rotate(70 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        occlusion_mask.move_to(globe_center)
        occlusion_mask.set_z_index(10)  # Same layer as globe — renders over text

        self.play(FadeIn(globe), FadeIn(occlusion_mask), run_time=1)

        # ==================================================
        # CHUNK 3: EXPLICIT TEXT INSTANTIATION (UNCHANGED)
        # ==================================================
        first_line = Text(
            "Online Training",
            font_size=50,
            color=BLACK,
            weight=BOLD
        )
        first_line.move_to(RIGHT * 1.2 + UP * 1.3)

        full_sentence = Text(
            "An efficient way to deliver knowledge",
            font_size=40,
            color=BLACK,
            weight=BOLD
        )
        full_sentence.scale_to_fit_width(5)
        full_sentence.next_to(first_line, DOWN, aligned_edge=LEFT)

        text_group = VGroup(first_line, full_sentence)

        # ==================================================
        # CHUNK 4: MATHEMATICAL DEFORMATION (UNCHANGED)
        # ==================================================
        curve_radius = full_height_radius + 2

        def curve_text_func(point):
            center_x = text_group.get_center()[0]
            theta = (point[0] - center_x) / curve_radius
            new_x = center_x + curve_radius * np.sin(theta)
            new_z = point[2] + curve_radius * (np.cos(theta) - 1)
            return np.array([new_x, point[1], new_z])

        text_group.apply_function(curve_text_func)

        # ==================================================
        # CHUNK 5: VIEWPORT ALIGNMENT (UNCHANGED)
        # ==================================================
        text_group.rotate(70 * DEGREES, axis=RIGHT, about_point=ORIGIN)
        text_group.shift(IN * 0.05)

        # FIX: z_index=-1 ensures text is strictly below the 2D occlusion
        # mask (z_index=10) in Manim's compositor render stack.
        text_group.set_z_index(-1)

        camera_down_vector = np.array([0, -np.cos(70 * DEGREES), -np.sin(70 * DEGREES)])

        # ==================================================
        # CHUNK 6: ANIMATION SEQUENCE (UNCHANGED)
        # ==================================================
        self.play(
            FadeIn(first_line, shift=camera_down_vector * 0.3),
            run_time=1.5
        )

        self.move_camera(
            zoom=1.35,
            frame_center=LEFT * 1.5,
            run_time=2.5,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.play(
            FadeIn(full_sentence, shift=camera_down_vector * 0.45),
            run_time=2,
            rate_func=rate_functions.ease_out_cubic
        )

        self.wait(1)

        # ==================================================
        # CHUNK 7: SIMULTANEOUS TRANSLATION & ROTATION (UNCHANGED DISTANCES)
        # The occlusion_mask stays stationary (it is a flat screen-space mask).
        # The 3D globe rotates for visual realism. Text slides behind both.
        # ==================================================
        self.play(
            first_line.animate.shift(LEFT * 7.5),
            full_sentence.animate.shift(LEFT * 7.5),
            Rotate(globe, angle=0.6 * 2.5, axis=OUT),
            run_time=2.5,
            rate_func=rate_functions.ease_in_out_sine
        )

        self.wait(2)