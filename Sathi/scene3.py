from manim import *
import numpy as np
import random
import os

IMG_BASE = "/Users/sathwikbadda/Assigment/Manim-Assignment/images"

def scatter_images(folder_name, img_h=0.7):
    """Place images on left/right using a refined grid to prevent overlap.
    Includes robust alpha filtering to remove black backgrounds and set opacity."""
    folder = os.path.join(IMG_BASE, folder_name)
    files  = sorted([f for f in os.listdir(folder) if f.endswith(".png") and not f.startswith(".")])[:20]
    
    mobs = []
    num_total = len(files)
    num_left  = num_total // 2
    num_right = num_total - num_left

    # Column x-coordinates (refined for separation)
    cols_left  = [-6.1, -4.4]
    cols_right = [4.4, 6.1]

    target_alpha = int(0.75 * 255)

    for idx, f in enumerate(files):
        img = ImageMobject(os.path.join(folder, f))
        
        # --- Robust Transparency Fix: Alpha Management ---
        pa = img.pixel_array.copy()
        if pa.shape[2] == 3: # RGB -> RGBA
            alphas = np.ones((pa.shape[0], pa.shape[1], 1), dtype=pa.dtype) * 255
            pa = np.concatenate([pa, alphas], axis=2)
        
        # Set all non-background pixels to target_alpha
        # Set background pixels (nearly black) to 0
        is_black = np.all(pa[:, :, :3] < 15, axis=2)
        
        # Set alpha for icons
        pa[~is_black, 3] = target_alpha
        # Set alpha for background
        pa[is_black, 3] = 0
        
        img.pixel_array = pa
        # --------------------------------------------------

        img.scale_to_fit_height(img_h)
        # IMPORTANT: Do NOT call img.set_opacity() as it overrides pixel_array alpha
        
        if idx < num_left:
            # Column 0 or 1 on Left
            col_idx = idx % 2
            row_idx = idx // 2
            rows = (num_left + 1) // 2
            y_space = np.linspace(-3.4, 3.4, rows) # Refined for safety
            x = cols_left[col_idx] + random.uniform(-0.05, 0.05)
            y = float(y_space[row_idx]) + random.uniform(-0.1, 0.1)
        else:
            # Column 0 or 1 on Right
            ridx = idx - num_left
            col_idx = ridx % 2
            row_idx = ridx // 2
            rows = (num_right + 1) // 2
            y_space = np.linspace(-3.4, 3.4, rows) # Refined for safety
            x = cols_right[col_idx] + random.uniform(-0.05, 0.05)
            y = float(y_space[row_idx]) + random.uniform(-0.1, 0.1)
        
        img.move_to(np.array([x, y, 0.]))
        img.set_z_index(30)
        mobs.append(img)
    
    return Group(*mobs)

def fly_in_images(scene, grid):
    """Creative entry: images fly in from the sides, scaling up from 0.1."""
    anims = []
    # Pre-calculate target positions and setup initial off-screen states
    for img in grid:
        target_pos = img.get_center().copy()
        cx = target_pos[0]
        if cx < 0:
            start_pos = target_pos + np.array([-8.0, 0., 0.])
        else:
            start_pos = target_pos + np.array([8.0, 0., 0.])
        
        # We need to animate FROM start_pos TO target_pos
        # But Manim ImageMobjects scale/move differently in animations
        # We'll set them to start state and animate to target
        img.move_to(start_pos)
        img.scale(0.1)
        anims.append(img.animate.move_to(target_pos).scale(10.0))
        
    scene.play(LaggedStart(*anims, lag_ratio=0.15), run_time=0.6)

def fly_out_images(scene, grid):
    """Creative exit: left images fly off-screen left, right images fly right,
    each with a shrink+shift combo, staggered for a dynamic effect."""
    anims = []
    for img in grid:
        cx = img.get_center()[0]
        if cx < 0:
            target = img.get_center() + np.array([-8.0, 0., 0.])
        else:
            target = img.get_center() + np.array([8.0, 0., 0.])
        anims.append(img.animate.move_to(target).scale(0.1))
    scene.play(LaggedStart(*anims, lag_ratio=0.15), run_time=0.4)

def start_floating(grid):
    """Add a slow, constrained floating motion to each image in the grid.
    Oscillation is relative to the original position to prevent frame exit."""
    for i, img in enumerate(grid):
        orig_pos = img.get_center().copy()
        state = {
            "ox": random.uniform(0, TAU),
            "oy": random.uniform(0, TAU),
            "sx": random.uniform(0.5, 0.9),
            "sy": random.uniform(0.5, 0.9)
        }
        def update_float(mob, dt, s=state, op=orig_pos):
            s["ox"] += s["sx"] * dt
            s["oy"] += s["sy"] * dt
            # Move relative to original position using sine waves
            mob.move_to(op + np.array([
                0.12 * np.sin(s["ox"]), # Tightened x swing
                0.15 * np.cos(s["oy"]), # Tightened y swing
                0
            ]))
        img.add_updater(update_float)

def stop_floating(grid):
    """Remove updaters from all images in the grid."""
    for img in grid:
        img.clear_updaters()



def build_cap(R, cap_color=BLACK, tassel_color="#F59E0B"):
    diam  = R * 2.0
    cap_h = diam * 0.30
    cap_rect   = Rectangle(width=diam, height=cap_h,
                           fill_color=cap_color, fill_opacity=1, stroke_width=0)
    cap_bottom = Ellipse(width=diam, height=diam*0.18,
                         fill_color=cap_color, fill_opacity=1, stroke_width=0)
    cap_bottom.move_to(cap_rect.get_bottom())
    skull_cap = Union(cap_rect, cap_bottom)
    skull_cap.set_fill(cap_color, 1).set_stroke(width=0)

    top_diamond = Polygon(
        UP*(diam*0.18), RIGHT*(diam*0.68),
        DOWN*(diam*0.18), LEFT*(diam*0.68),
        fill_color=cap_color, fill_opacity=1, stroke_width=0)
    top_diamond.move_to(skull_cap.get_top() + UP*diam*0.03)

    ctr  = top_diamond.get_center()
    rcor = top_diamond.get_right()
    hang = rcor + DOWN*diam*0.36

    knot  = Circle(radius=diam*0.038, fill_color=tassel_color, fill_opacity=1, stroke_width=0).move_to(ctr)
    tstr  = CubicBezier(ctr, ctr+RIGHT*diam*0.26+UP*diam*0.04,
                        rcor+LEFT*diam*0.10+UP*diam*0.12, rcor+DOWN*diam*0.03,
                        color=tassel_color, stroke_width=diam*3.6)
    hline = Line(rcor+DOWN*diam*0.03, hang, color=tassel_color, stroke_width=diam*3.6)
    tip   = Circle(radius=diam*0.052, fill_color=tassel_color, fill_opacity=1, stroke_width=0).move_to(hang)
    return VGroup(skull_cap, top_diamond, knot, tstr, hline, tip)


class GraduationCapScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE

        LINE_COL      = ManimColor("#90CAF9") # BLUE
        LINE_COL_DARK = ManimColor("#64B5F6") # Slightly darker for shading
        CIRCLE_BLUE   = ManimColor("#2563EB")
        EDGE_COL      = ManimColor("#5B9BD5") # LIGHT_BLUE
        STEP_COL      = ManimColor("#1D428A") # dark blue steps (from intro.py style)
        STEP_BG       = ManimColor("#E8F0FE")

        fw = self.camera.frame.get_width()
        fh = self.camera.frame.get_height()

        # ── 1. Speed lines ─────────────────────────────────────────────────
        random.seed(7)
        line_specs = []
        for _ in range(10):
            x0  = random.uniform(fw/2+2., fw+6.)
            y   = random.uniform(-fh/2+0.4, fh/2-0.4)
            w   = random.uniform(1., 3.)
            spd = random.uniform(12., 18.)
            opa = random.uniform(0.30, 0.80)
            sw  = random.uniform(1.5, 4.)
            line_specs.append((x0, y, w, spd, opa, sw))

        line_mobs, lines_grp = [], VGroup()
        for x0, y, w, spd, opa, sw in line_specs:
            ln = Line(LEFT*w/2, RIGHT*w/2,
                      stroke_color=LINE_COL, stroke_width=sw, stroke_opacity=opa)
            ln.move_to([x0, y, 0]); line_mobs.append(ln); lines_grp.add(ln)
        self.add(lines_grp)

        t_ln = [0.]
        def line_upd(mob, dt):
            t_ln[0] += dt
            for i, ln in enumerate(line_mobs):
                x0, y, w, spd, *_ = line_specs[i]
                nx = x0 - spd*t_ln[0]
                if nx < -fw/2-w-1: nx = -fw-20
                ln.move_to([nx, y, 0])
        lines_grp.add_updater(line_upd)

        # ── 2. Circle + Cap ─────────────────────────────────────────────────
        R = 0.60
        circle = Circle(radius=R, fill_color=CIRCLE_BLUE, fill_opacity=1,
                        stroke_color=ManimColor("#1E40AF"), stroke_width=4)
        circle.move_to(ORIGIN)
        cap = build_cap(R, cap_color=BLACK, tassel_color="#F59E0B")
        skull = cap[0]
        cap.shift(UP*(circle.get_top()[1]-skull.get_bottom()[1]) - UP*R*0.5)
        grad_group = VGroup(circle, cap)
        grad_group.set_z_index(100) # Ensure head is always in front
        self.add(grad_group)

        hang_line, tip_dot = cap[4], cap[5]
        wt=[0.]; wa=[0.]; won=[False]; wrs=[None]; wre=[None]
        def tassel_wave(mob, dt):
            if not won[0] or wrs[0] is None: return
            wt[0]+=dt; wa[0]=max(0., wa[0]-dt*0.13)
            osc = wa[0]*np.sin(wt[0]*9.5)
            tip = wre[0]+np.array([osc,0,0])
            hang_line.put_start_and_end_on(wrs[0], tip); tip_dot.move_to(tip)
        hang_line.add_updater(tassel_wave)

        grad_group.move_to([-fw/2-grad_group.width-1., 0, 0])
        self.play(grad_group.animate.move_to(ORIGIN),
                  run_time=0.5, rate_func=rate_functions.ease_out_back)  # Narration: "The world your graduates will enter demands three kinds of readiness:"
        wrs[0]=hang_line.get_start().copy(); wre[0]=hang_line.get_end().copy()
        wa[0]=0.25; won[0]=True
        self.play(circle.animate.stretch(0.92,0).stretch(1.08,1), run_time=0.08)
        self.play(circle.animate.stretch(1/0.92,0).stretch(1/1.08,1), run_time=0.08)
        self.wait(0.3)  # Narration: "for further higher education"
        lines_grp.clear_updaters()
        self.wait(0.3)  # Narration: "for 21st-century jobs driven by AI and complexity"

        # ── 3. Triangle geometry ─────────────────────────────────────────────
        group_top_y = cap[1].get_top()[1]
        group_bot_y = circle.get_bottom()[1]
        group_h     = group_top_y - group_bot_y
        group_mid_y = (group_top_y + group_bot_y) / 2.

        margin_v = group_h * 1.2
        margin_h = group_h * 2.0

        tri_apex = np.array([0., group_mid_y + group_h/2 + margin_v, 0.])
        base_y   = group_mid_y - group_h/2 - margin_v
        base_l   = np.array([-margin_h, base_y, 0.])
        base_r   = np.array([ margin_h, base_y, 0.])

        # ── 4. Construct 3D Shaded Pyramid + Shadow ──────────────────────────
        center_pt = np.array([0., group_mid_y, 0.])
        
        # Region faces for 3D effect
        face_top_l = Polygon(tri_apex, center_pt, base_l, fill_color=LINE_COL, fill_opacity=0.9, stroke_width=0)
        face_top_r = Polygon(tri_apex, center_pt, base_r, fill_color=LINE_COL_DARK, fill_opacity=0.9, stroke_width=0)
        face_bot   = Polygon(base_l, center_pt, base_r, fill_color=LINE_COL, fill_opacity=0.95, stroke_width=0)
        
        # Outline
        outline = Polygon(tri_apex, base_l, base_r, stroke_color=EDGE_COL, stroke_width=3, fill_opacity=0)
        
        # Shadow
        pyramid_shadow = Polygon(tri_apex, base_l, base_r, fill_color=BLACK, fill_opacity=0.15, stroke_width=0)
        pyramid_shadow.shift(DOWN * 0.15 + RIGHT * 0.15).set_z_index(4)
        
        # Initial Pyramid Group for entry
        pyramid_group = VGroup(pyramid_shadow, face_top_l, face_top_r, face_bot, outline)
        pyramid_group.set_z_index(5)
        
        # ── 5. Slide 3D Pyramid from DOWN frame with rotation ─────────────────
        # Note: grad_group is already at ORIGIN with z_index 20
        pyramid_group.save_state()
        pyramid_group.move_to(DOWN * 12).rotate(PI/4)
        pyramid_group.set_opacity(0)
        
        self.play(pyramid_group.animate.restore(),
                  run_time=0.5, rate_func=rate_functions.ease_out_cubic)
        tiny_tri = pyramid_group 
        
        won[0]=False; hang_line.clear_updaters()
        grad_group.set_z_index(20)
        self.wait(0.3)  # Narration: "and for entrepreneurship in markets that do not yet exist."

        # ── 5. Three lines from each triangle corner to a center point ──────
        # Lines radiate from the 3 corners toward the group center
        center_pt = np.array([0., group_mid_y, 0.])
        line_c1 = Line(tri_apex, center_pt, stroke_color=EDGE_COL, stroke_width=2.5)
        line_c2 = Line(base_l,   center_pt, stroke_color=EDGE_COL, stroke_width=2.5)
        line_c3 = Line(base_r,   center_pt, stroke_color=EDGE_COL, stroke_width=2.5)
        corner_lines = VGroup(line_c1, line_c2, line_c3)
        corner_lines.set_z_index(15)

        self.play(LaggedStart(
            Create(line_c1), Create(line_c2), Create(line_c3),
            lag_ratio=0.2), run_time=0.3)
        self.wait(0.1)

        # ── 5.5 Glow behind the blue circle ─────────────────────────────────
        # Restore Glow Halo
        glow = VGroup(*[
            Circle(radius=0.6 + i * 0.35, stroke_width=0, fill_color=LINE_COL, fill_opacity=0.15 - i * 0.015)
            for i in range(10)
        ]).move_to(circle.get_center())
        glow.set_z_index(4) # Behind pyramid and head
        
        self.play(FadeIn(glow, scale=0.5), run_time=0.5)
        
        # Add "Wavy" effect to the pyramid's internal glow
        glow.t = 0
        def internal_glow_updater(mob, dt):
            mob.t += dt
            for i, ring in enumerate(mob):
                # Breathing effect
                ring.set_opacity((0.15 - i * 0.015) * (1.2 + 0.8 * np.cos(mob.t * 3 + i * 0.5)))
        glow.add_updater(internal_glow_updater)

        # Add glow and lines to the pyramid group so it spins later
        pyramid_group.add(glow, corner_lines)

        # ── 6. Rounded rectangle "Higher Education" above triangle apex ─────
        top_box = VGroup()
        top_rect = RoundedRectangle(
            corner_radius=0.22, height=0.58, width=3.2, # Narrowed width
            fill_color=STEP_COL, fill_opacity=1,
            stroke_color=ManimColor("#1A3A6E"), stroke_width=2
        )
        top_label = Text("Higher Education", font_size=22, color=WHITE, weight=BOLD)
        top_label.move_to(top_rect.get_center())
        top_box.add(top_rect, top_label)
        top_box.move_to(tri_apex + UP * 0.42)
        top_box.set_z_index(25)

        self.play(FadeIn(top_box, shift=DOWN*0.1), run_time=0.3)

        # ── Education images on the left, beside the triangle ─────────────
        edu_grid = scatter_images("education")
        fly_in_images(self, edu_grid)
        start_floating(edu_grid)
        self.wait(0.3)  # Narration: "mySATHI measures..."

        # ── 7. Rotate + throw ───────────────────────────────────────────────
        target_box_pos = top_box.get_center().copy()  # where AI box will land

        # Build the AI box (starts off-screen above)
        ai_rect = RoundedRectangle(
            corner_radius=0.22, height=0.58, width=3.2, # Narrowed width
            fill_color=ManimColor("#0D47A1"), fill_opacity=1,
            stroke_color=ManimColor("#1A237E"), stroke_width=2
        )
        ai_label = Text("AI Job readiness",
                        font_size=19, color=WHITE, weight=BOLD)
        ai_label.move_to(ai_rect.get_center())
        ai_box = VGroup(ai_rect, ai_label)
        ai_box.move_to(target_box_pos + UP * (fh / 2 + ai_box.height + 0.5))
        ai_box.set_z_index(25)
        self.add(ai_box)

        # PHASE A: triangle + box rotate together by RELEASE_ANGLE degrees
        RELEASE_DEG = 135
        release_rad  = RELEASE_DEG * DEGREES

        # Group everything that spins
        # Restore top_box to rotation group as per user request for consistency
        spin_group = VGroup(tiny_tri, top_box)
        stop_floating(edu_grid)
        fly_out_images(self, edu_grid)
        self.play(
            Rotate(spin_group, angle=release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.linear),
            run_time=0.3
        )

        # ── Exit path: slide down-right perfectly along its tilted angle ────
        release_pos = top_box.get_center().copy()   # capture position after Phase A
        
        # At 135 degrees, the box is tilted -45 degrees from the downward-right diagonal.
        # The user wants it to slide exactly along this angle down and to the right.
        slide_dir = np.array([np.cos(release_rad - PI), np.sin(release_rad - PI), 0])
        
        distance = 8.0
        exit_pt = release_pos + slide_dir * distance
        
        ctrl1 = release_pos + slide_dir * (distance * 0.33)
        ctrl2 = release_pos + slide_dir * (distance * 0.66)
        throw_path = CubicBezier(release_pos, ctrl1, ctrl2, exit_pt)

        # Detach box from spin group so it flies on its own arc
        spin_group.remove(top_box)
        triangle_only = spin_group  # remaining angle = TAU - release_rad

        # PHASE B: triangle finishes the remaining rotation,
        #          box follows the throw arc NO fade — drops naturally,
        #          AI box drops into place from above
        self.play(
            Rotate(triangle_only, angle=TAU - release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.ease_out_sine),  
            MoveAlongPath(top_box, throw_path,
                          rate_func=rate_functions.linear),  
            ai_box.animate.move_to(target_box_pos),
            run_time=0.4,
        )
        # Note: grad_group is NOT in triangle_only, so it stays upright.
        self.wait(0.5)

        # ── throw #2 (for AI box) ───────────────────────────────────────────
        # Show AI images on the right while the AI box is displayed
        ai_grid = scatter_images("ai")
        fly_in_images(self, ai_grid)
        start_floating(ai_grid)
        self.wait(0.3)  # Narration: "against the demands..."
        
        ent_rect = RoundedRectangle(
            corner_radius=0.22, height=0.58, width=3.2, # Narrowed width
            fill_color=STEP_COL, fill_opacity=1,
            stroke_color=ManimColor("#1A3A6E"), stroke_width=2
        )
        ent_label = Text("Entrepreneurship", font_size=20, color=WHITE, weight=BOLD)
        ent_label.move_to(ent_rect.get_center())
        ent_box = VGroup(ent_rect, ent_label)
        ent_box.move_to(target_box_pos + UP * (fh / 2 + ent_box.height + 0.5))
        ent_box.set_z_index(25)
        self.add(ent_box)

        spin_group_2 = VGroup(tiny_tri, ai_box)

        stop_floating(ai_grid)
        fly_out_images(self, ai_grid)
        self.play(
            Rotate(spin_group_2, angle=release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.ease_in_expo),
            run_time=0.3
        )

        release_pos_2 = ai_box.get_center().copy()
        slide_dir_2 = np.array([np.cos(release_rad - PI), np.sin(release_rad - PI), 0])
        
        exit_pt_2 = release_pos_2 + slide_dir_2 * distance
        ctrl1_2 = release_pos_2 + slide_dir_2 * (distance * 0.33)
        ctrl2_2 = release_pos_2 + slide_dir_2 * (distance * 0.66)
        throw_path_2 = CubicBezier(release_pos_2, ctrl1_2, ctrl2_2, exit_pt_2)

        spin_group_2.remove(ai_box)
        triangle_only_2 = spin_group_2

        self.play(
            Rotate(triangle_only_2, angle=TAU - release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.ease_out_sine),
            MoveAlongPath(ai_box, throw_path_2,
                          rate_func=rate_functions.linear),
            ent_box.animate.move_to(target_box_pos),
            run_time=0.4,
        )
        self.wait(0.5)

        # ── throw #3 (for Entrepreneurship box) ─────────────────────────────
        # Show entrepreneurship images on the left while ent box displayed
        ent_grid = scatter_images("entreprenuriship")
        fly_in_images(self, ent_grid)
        start_floating(ent_grid)
        self.wait(0.3)  # Narration: "Modular, fair..."

        spin_group_3 = VGroup(tiny_tri, ent_box)

        stop_floating(ent_grid)
        fly_out_images(self, ent_grid)
        self.play(
            Rotate(spin_group_3, angle=release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.ease_in_expo),
            run_time=0.3
        )

        release_pos_3 = ent_box.get_center().copy()
        slide_dir_3 = np.array([np.cos(release_rad - PI), np.sin(release_rad - PI), 0])
        
        exit_pt_3 = release_pos_3 + slide_dir_3 * distance
        ctrl1_3 = release_pos_3 + slide_dir_3 * (distance * 0.33)
        ctrl2_3 = release_pos_3 + slide_dir_3 * (distance * 0.66)
        throw_path_3 = CubicBezier(release_pos_3, ctrl1_3, ctrl2_3, exit_pt_3)

        spin_group_3.remove(ent_box)
        triangle_only_3 = spin_group_3

        self.play(
            Rotate(triangle_only_3, angle=TAU - release_rad, about_point=ORIGIN,
                   rate_func=rate_functions.ease_out_sine),
            MoveAlongPath(ent_box, throw_path_3,
                          rate_func=rate_functions.linear),
            run_time=0.6,
        )
        self.wait(0.1)  # Narration: "...intelligence that faculty/counsellors can use..."
        
        triangle_exit_group = VGroup(tiny_tri)
        self.play(
            Rotate(triangle_exit_group, angle=release_rad, about_point=ORIGIN, rate_func=rate_functions.ease_in_expo),
            run_time=0.3
        )
        self.play(
            triangle_exit_group.animate.shift(DOWN * 12),
            run_time=0.3,
            rate_func=rate_functions.linear
        )
        self.wait(0.1)

        # ── 9. Final Transformation to Logo ─────────────────────────────────
        # Load the logo image
        logo = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/mysathi.png")
        # Scale to match the circle size roughly
        logo.scale_to_fit_height(circle.height)
        logo.move_to(circle.get_center())
        
        # We need a 3D rotation flip on the Y-axis. 
        # First, we spin the grad_group by 90 degrees around Y so it becomes flat (invisible).
        self.play(
            Rotate(grad_group, angle=PI/2, axis=UP, about_point=circle.get_center()),
            run_time=0.3,
            rate_func=rate_functions.ease_in_sine
        )
        self.remove(grad_group)
        logo.rotate(PI/2, axis=UP, about_point=logo.get_center())
        self.add(logo)
        self.play(
            Rotate(logo, angle=-PI/2, axis=UP, about_point=logo.get_center()),
            run_time=0.3,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.2)

        self.wait(0.1)

        # ── 10. Four C's Donut Graphs ───────────────────────────────────────
        # Create 4 donut charts around the logo: 
        # Communication, Collaboration, Critical Thinking, Creativity
        
        donut_radius = 2.8  # Distance from center logo
        donut_radius = 2.8  # Distance from center logo
        labels = [
            "Communication",
            "Collaboration",
            "Critical Thinking",
            "Creativity"
        ]
        
        # Positions: Top-Right, Bottom-Right, Bottom-Left, Top-Left
        angles = [PI/4, -PI/4, -3*PI/4, 3*PI/4]
        
        all_donuts = VGroup()
        for i in range(4):
            # The exact center for the donut ring
            donut_center = circle.get_center() + np.array([np.cos(angles[i]), np.sin(angles[i]), 0]) * donut_radius
            
            # Donut doubled again to fix overlapping text (outer radius from 0.9 to 1.3)
            bg_donut = Annulus(
                arc_center=donut_center,
                inner_radius=1.0, outer_radius=1.3,
                fill_color=ManimColor("#E0E5EA"), fill_opacity=1, stroke_width=0
            )
            
            # The label directly in the center of the ring
            label_text = labels[i]
            if " " in label_text:
                lbl = Text(label_text.replace(" ", "\n"), font_size=20, color=ManimColor("#1A3A6E"), weight=BOLD)
            else:
                lbl = Text(label_text, font_size=20, color=ManimColor("#1A3A6E"), weight=BOLD)
                
            lbl.move_to(donut_center)
            
            donut_group = VGroup(bg_donut, lbl)
            all_donuts.add(donut_group)

        # Animate them popping in one by one around the logo
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in all_donuts], lag_ratio=0.2),
            run_time=0.8
        )
        self.wait(0.1)

        # ── 11. Logo back to Head and Color Cycle ───────────────────────────
        
        
        # Fade out the text labels inside the donuts while rotating logo flat
        texts_to_fade = [donut[1] for donut in all_donuts]
        
        self.play(
            Rotate(logo, angle=PI/2, axis=UP, about_point=logo.get_center()),
            *[FadeOut(t) for t in texts_to_fade],
            run_time=0.3,
            rate_func=rate_functions.ease_in_sine
        )
        self.remove(logo)
        head_circle = Circle(radius=0.60, fill_color=CIRCLE_BLUE, fill_opacity=1, stroke_color=ManimColor("#1E40AF"), stroke_width=4)
        head_circle.move_to(circle.get_center())
        head_circle.rotate(PI/2, axis=UP, about_point=head_circle.get_center())
        self.add(head_circle)
        self.play(
            Rotate(head_circle, angle=-PI/2, axis=UP, about_point=head_circle.get_center()),
            run_time=0.3,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.1)
        
        # Setup dynamic fill sectors and percentage trackers for the donuts
        trackers = [ValueTracker(0) for _ in range(4)]
        d_centers = [all_donuts[i][0].get_center() for i in range(4)]
        
        # Colored sectors that fill the donuts
        sectors = VGroup(*[
            always_redraw(lambda i=i, t=trackers[i]: AnnularSector(
                arc_center=all_donuts[i][0].get_center(),
                inner_radius=1.0, outer_radius=1.3,
                start_angle=PI/2, angle=-TAU * (t.get_value() / 100),
                fill_color=head_circle.get_fill_color(), fill_opacity=1, stroke_width=0
            ))
            for i in range(4)
        ])

        # Predefined fixed percentages per color round
        # Each entry: (color, [pct_donut0, pct_donut1, pct_donut2, pct_donut3])
        color_sequences = [
            (ManimColor("#E91E63"), [42, 87, 23, 65]),   # Pink/Red
            (ManimColor("#F59E0B"), [91, 34, 78, 12]),   # Amber/Yellow
            (ManimColor("#10B981"), [56, 18, 93, 44]),   # Green
            (ManimColor("#8B5CF6"), [31, 72, 49, 88]),   # Purple
            (CIRCLE_BLUE,           [85, 27, 61, 39]),   # Original Blue
        ]

        # Create one label per donut (will be updated each round)
        pct_labels = []
        for i in range(4):
            num = DecimalNumber(0, num_decimal_places=0, font_size=36, color=CIRCLE_BLUE, include_sign=False)
            sym = Tex(r"\%", font_size=28, color=CIRCLE_BLUE)
            grp = VGroup(num, sym).arrange(RIGHT, buff=0.06, aligned_edge=UP)
            grp.move_to(d_centers[i])
            pct_labels.append(grp)

        self.add(sectors, *pct_labels)

        for color, percentages in color_sequences:
            anims = [head_circle.animate.set_color(color).set_fill(color, opacity=1)]
            for idx, tracker in enumerate(trackers):
                anims.append(tracker.animate.set_value(percentages[idx]))
            self.play(*anims, run_time=0.2)
            for idx, grp in enumerate(pct_labels):
                grp[0].set_value(percentages[idx])
                grp[0].set_color(color); grp[1].set_color(color)
                grp.arrange(RIGHT, buff=0.06, aligned_edge=UP)
                grp.move_to(d_centers[idx])
        self.wait(0.2)

        # ── 12. Donut Wheel Exit ────────────────────────────────────────────
        # Group each donut's components for the "wheel" exit
        donut_wheels = VGroup()
        for i in range(4):
            # Include background annulus, its current sector, and percentage label
            wheel = VGroup(all_donuts[i][0], sectors[i], pct_labels[i])
            donut_wheels.add(wheel)

        top_indices = [0, 3] # Top-Right, Top-Left
        bot_indices = [1, 2] # Bottom-Right, Bottom-Left

        wheel_exit_anims = []
        for i in top_indices:
            donut_wheels[i].save_state()
            wheel_exit_anims.append(
                UpdateFromAlphaFunc(
                    donut_wheels[i],
                    lambda m, a: m.restore().shift(RIGHT * 15 * a).rotate(-TAU * 2 * a)
                )
            )
        for i in bot_indices:
            donut_wheels[i].save_state()
            wheel_exit_anims.append(
                UpdateFromAlphaFunc(
                    donut_wheels[i],
                    lambda m, a: m.restore().shift(LEFT * 15 * a).rotate(TAU * 2 * a)
                )
            )

        self.play(*wheel_exit_anims, run_time=0.6, rate_func=rate_functions.ease_in_sine)
        self.remove(donut_wheels, all_donuts, sectors, *pct_labels)
        self.wait(0.5)

        # ── 13. Flip Head back to Graduation Cap ────────────────────────────
        self.play(
            Rotate(head_circle, angle=PI/2, axis=UP, about_point=head_circle.get_center()),
            run_time=0.2,
            rate_func=rate_functions.ease_in_sine
        )
        self.remove(head_circle)
        self.add(grad_group)
        self.play(
            Rotate(grad_group, angle=-PI/2, axis=UP, about_point=grad_group[0].get_center()),
            run_time=0.3,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.3)

        # ── 14. Pyramid Re-entry ───────────────────────────────────────────
        # User wants it to come from down frame while rotating
        # At this point, triangle_exit_group is at DOWN*12 and tilted by release_rad
        triangle_exit_group.set_z_index(5)
        
        # We define the upright target at ORIGIN
        target_tri_upright = triangle_exit_group.copy().shift(UP * 12).rotate(-release_rad, about_point=ORIGIN)
        
        self.play(
            UpdateFromAlphaFunc(
                triangle_exit_group,
                lambda m, a: m.become(target_tri_upright).shift(DOWN * 12 * (1 - a)).rotate(release_rad * (1 - a))
            ),
            run_time=0.8,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(0.5)

        # ── 15. Text Boxes Re-entry ────────────────────────────────────────
        # Positions: Apex (tri_apex), Bottom-Right (base_r), Bottom-Left (base_l)
        
        # Fix the 135-degree tilts from earlier spinning phases
        top_box.rotate(-release_rad)
        ai_box.rotate(-release_rad)
        ent_box.rotate(-release_rad)
        
        # Initially place them off-screen at screen corners
        top_box.move_to(UL * 10)
        ai_box.move_to(UR * 10)
        ent_box.move_to(DOWN * 10)
        
        self.play(
            top_box.animate.move_to(tri_apex + UP * 0.42),
            ai_box.animate.move_to(base_r + RIGHT * (ai_box.width / 2 + 0.1)),
            ent_box.animate.move_to(base_l + LEFT * (ent_box.width / 2 + 0.1)),
            run_time=0.8,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.2)

        # ── 16. Vertical Columns for Grades & Ranks ───────────────────────────
        
        grades_list = ["S", "A+", "A", "B+", "B", "C", "D"]
        ranks_list = ["1st", "2nd", "3rd", "4th"]
        
        # Helper for superscripts
        def get_rank_text(rank_str, color):
            main_digit = rank_str[:-2]
            suffix = rank_str[-2:]
            
            main_mob = Text(main_digit, font_size=40, color=color, weight=BOLD)
            suffix_mob = Text(suffix, font_size=20, color=color, weight=BOLD)
            suffix_mob.next_to(main_mob.get_top(), RIGHT, buff=0.1).shift(DOWN * 0.1)
            return VGroup(main_mob, suffix_mob)

        bubbles = VGroup()
        
        # Grades on left
        for i, g in enumerate(grades_list):
            # Gradient: dark gray to light gray
            alpha = i / (len(grades_list) - 1)
            color = interpolate_color(ManimColor("#212121"), ManimColor("#BDBDBD"), alpha)
            item = Text(g, font_size=40, color=color, weight=BOLD)
            item.move_to(LEFT * 5 + UP * (2.5 - i * 0.8))
            bubbles.add(item)
            
        # Ranks on right
        for i, r in enumerate(ranks_list):
            alpha = i / (len(ranks_list) - 1)
            color = interpolate_color(ManimColor("#212121"), ManimColor("#9E9E9E"), alpha)
            item = get_rank_text(r, color)
            item.move_to(RIGHT * 5 + UP * (1.5 - i * 1.0))
            bubbles.add(item)

        bubbles.set_z_index(2)

        top_start = top_box.get_center().copy()
        ai_start = ai_box.get_center().copy()
        ent_start = ent_box.get_center().copy()
        
        def orbit_updater(mob, start_pos, alpha, angle=PI):
            current_angle = alpha * angle
            new_pos = np.array([
                start_pos[0] * np.cos(current_angle) - start_pos[1] * np.sin(current_angle),
                start_pos[0] * np.sin(current_angle) + start_pos[1] * np.cos(current_angle),
                0
            ])
            mob.move_to(new_pos)

        # Spin the pyramid group 180 degrees (PI) around the Z-axis
        self.play(
            Rotate(triangle_exit_group, angle=PI, about_point=ORIGIN),
            UpdateFromAlphaFunc(top_box, lambda m, a: orbit_updater(m, top_start, a)),
            UpdateFromAlphaFunc(ai_box, lambda m, a: orbit_updater(m, ai_start, a)),
            UpdateFromAlphaFunc(ent_box, lambda m, a: orbit_updater(m, ent_start, a)),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        # Note: grad_group stays constant
        self.wait(0.5)

        # 1. Immediate Text Boxes Exit
        self.play(
            top_box.animate.shift(DOWN * 12),
            ai_box.animate.shift(UP * 12),
            ent_box.animate.shift(UP * 12),
            run_time=0.8,
            rate_func=rate_functions.ease_in_expo
        )
        self.remove(top_box, ai_box, ent_box)

        # 2. Change the main triangle body AND lines to gray AFTER boxes exit
        # Indices: 0:shadow, 1:face_t_l, 2:face_t_r, 3:face_bot, 4:outline, 5:glow, 6:corner_lines
        self.play(
            tiny_tri[1].animate.set_fill(ManimColor("#D3D3D3"), opacity=0.85), 
            tiny_tri[2].animate.set_fill(ManimColor("#D3D3D3"), opacity=0.85),
            tiny_tri[3].animate.set_fill(ManimColor("#D3D3D3"), opacity=0.85),
            tiny_tri[4].animate.set_stroke(ManimColor("#757575"), width=3), # Gray outline
            tiny_tri[5].animate.set_color(ManimColor("#D3D3D3")), # gray pyramid glow
            tiny_tri[6].animate.set_stroke(ManimColor("#757575")), # Gray corner lines
            FadeIn(bubbles, run_time=0.5),
            run_time=0.6
        )
        self.wait(0.5)
        
        # ── 17. Final Exit and Logo Reveal ─────────────────────────────────
        # Animate bubbles floating outwards and disappearing
        bubble_exit_anims = []
        for b in bubbles:
            b.clear_updaters()
            direction = b.get_center() / np.linalg.norm(b.get_center())
            bubble_exit_anims.append(b.animate.shift(direction * 5).set_opacity(0))
        
        self.play(
            triangle_exit_group.animate.shift(DOWN * 12),
            *bubble_exit_anims,
            run_time=1.0,
            rate_func=rate_functions.ease_in_expo
        )
        self.remove(triangle_exit_group, bubbles)
        
        # Now we only have the grad_group in the center. Let's flip it back to the original mysathi logo.
        logo = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/mysathi.png")
        logo.scale_to_fit_height(circle.height)
        logo.move_to(circle.get_center())
        
        # Flip grad_group 90 degrees so it is invisible edge-on
        self.play(
            Rotate(grad_group, angle=PI/2, axis=UP, about_point=ORIGIN),
            run_time=0.5,
            rate_func=rate_functions.ease_in_sine
        )
        self.remove(grad_group)
        
        # Add logo, start it flat, then flip to face front
        logo.rotate(PI/2, axis=UP, about_point=ORIGIN)
        self.add(logo)
        self.play(
            Rotate(logo, angle=-PI/2, axis=UP, about_point=ORIGIN),
            run_time=0.5,
            rate_func=rate_functions.ease_out_back
        )
        
        self.wait(0.2)

        # ── 18. Orbital Phase ──────────────────────────────────────────────
        # Create 3 concentric orbits
        orbit_colors = [ManimColor("#839EC5"), ManimColor("#6284B6"), ManimColor("#4A6B9C")]
        orbits = VGroup(
            Circle(radius=2.0, stroke_color=orbit_colors[0], stroke_width=2),
            Circle(radius=3.0, stroke_color=orbit_colors[1], stroke_width=2),
            Circle(radius=4.0, stroke_color=orbit_colors[2], stroke_width=2)
        ).move_to(ORIGIN)
        
        # Create the 3 orbital spheres (Input nodes later)
        # Using a solid dark blue from the reference
        NODE_BLUE = ManimColor("#355486")
        
        def make_node(text_str, img_path=None, radius=0.6, font_size=18):
            bg = Circle(radius=radius, fill_color=NODE_BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            # Use Paragraph for reliable multi-line centering and kwargs for consistent styling
            lbl = Paragraph(text_str, font_size=font_size, color=WHITE, weight=BOLD, alignment="center")
            lbl.move_to(bg.get_center())
            node = Group(bg, lbl)
            if img_path:
                img = ImageMobject(img_path)
                img.scale_to_fit_height(radius * 1.0).move_to(bg.get_center())
                node.add(img)
            return node

        ai_img_dir = "/Users/sathwikbadda/Assigment/Manim-Assignment/images/ai"
        node_mod = make_node("MODULAR", os.path.join(ai_img_dir, "ai1.png"), radius=0.6, font_size=16)
        node_fair = make_node("FAIR", os.path.join(ai_img_dir, "ai3.png"), radius=0.6, font_size=16) 
        node_non = make_node("NON\nELIMINATORY", os.path.join(ai_img_dir, "ai5.png"), radius=0.6, font_size=12) 
        
        # Hide text initially, show image
        node_mod[1].set_opacity(0)
        node_fair[1].set_opacity(0)
        node_non[1].set_opacity(0)
        
        # Position them on their respective orbits initially
        node_mod.move_to(RIGHT * 2.0)
        node_fair.move_to(DOWN * 3.0)
        node_non.move_to(LEFT * 4.0)
        
        orbiter_group = Group(node_mod, node_fair, node_non)
        
        self.play(
            LaggedStart(
                *[GrowFromCenter(orbit) for orbit in orbits],
                lag_ratio=0.2, run_time=1.5
            ),
            FadeIn(orbiter_group, shift=UP*0.5, run_time=1.0)
        )
        
        # Revolve around the Mysathi logo (origin)
        self.play(
            Rotate(node_mod, angle=TAU, about_point=ORIGIN, rate_func=rate_functions.linear),
            Rotate(node_fair, angle=TAU, about_point=ORIGIN, rate_func=rate_functions.linear),
            Rotate(node_non, angle=TAU, about_point=ORIGIN, rate_func=rate_functions.linear),
            run_time=1.5
        )
        self.wait(0.2)

        # ── 19. Neural Network Transition ──────────────────────────────────
        # Uncreate the orbits, move logo to top, align nodes on the left
        pos_input_top = np.array([-4.5, 2.0, 0])
        pos_input_mid = np.array([-4.5, 0, 0])
        pos_input_bot = np.array([-4.5, -2.0, 0])
        
        self.play(
            Uncreate(orbits, run_time=0.5),
            logo.animate.move_to(UP * 3.2).scale(0.8),
            node_mod.animate.move_to(pos_input_top).scale(1.4), # Increased scale slightly
            node_fair.animate.move_to(pos_input_mid).scale(1.4),
            node_non.animate.move_to(pos_input_bot).scale(1.4),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_sine
        )
        # Reveal the text and fade out images
        self.play(
            node_mod[1].animate.set_opacity(1),
            node_fair[1].animate.set_opacity(1),
            node_non[1].animate.set_opacity(1),
            node_mod[2].animate.set_opacity(0),
            node_fair[2].animate.set_opacity(0),
            node_non[2].animate.set_opacity(0),
            run_time=0.5
        )
        self.wait(0.5)

        # ── 20. Neural Network Assembly ────────────────────────────────────
        # Hidden Layer (4 nodes) - Center
        HIDDEN_COLOR = ManimColor("#F57C00") # Orange
        hidden_nodes = VGroup(*[
            Circle(radius=0.45, fill_color=HIDDEN_COLOR, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            for _ in range(4)
        ])
        hidden_nodes.arrange(DOWN, buff=0.6).move_to(ORIGIN)
        
        # Output Layer (2 nodes) - Right
        OUT_COLOR = NODE_BLUE # Match Input layer color
        
        # Load images for Output layer
        edu1_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/education/edu1.png")
        edu2_img = ImageMobject("/Users/sathwikbadda/Assigment/Manim-Assignment/images/education/edu2.png")
        
        # Make the output nodes slightly larger to fit the images well
        out_radius = 0.65
        out_bg1 = Circle(radius=out_radius, fill_color=OUT_COLOR, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        out_bg2 = Circle(radius=out_radius, fill_color=OUT_COLOR, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        
        edu1_img.scale_to_fit_height(out_radius * 1.0).move_to(out_bg1.get_center())
        edu2_img.scale_to_fit_height(out_radius * 1.0).move_to(out_bg2.get_center())
        
        out_node1 = Group(out_bg1, edu1_img)
        out_node2 = Group(out_bg2, edu2_img)
        
        out_nodes = Group(out_node1, out_node2)
        out_nodes.arrange(DOWN, buff=1.2).move_to(RIGHT * 4.0) # slightly to the left to fit labels
        
        # Add side labels
        lbl_faculty = Text("Faculty", font_size=28, color=NODE_BLUE, weight=BOLD).next_to(out_node1, RIGHT, buff=0.3)
        lbl_counsellor = Text("Counsellor", font_size=28, color=NODE_BLUE, weight=BOLD).next_to(out_node2, RIGHT, buff=0.3)
        
        out_labels = VGroup(lbl_faculty, lbl_counsellor)
        
        input_nodes = [node_mod, node_fair, node_non]
        
        # Create connection lines
        lines_in_hid = VGroup()
        lines_hid_out = VGroup()
        
        # Sequence 1: Sequential Intersecting Flow Input -> Hidden (Strict One by One)
        seq1_anims = []
        for i, h_node in enumerate(hidden_nodes):
            for i_node in input_nodes:
                l = Line(i_node.get_center(), h_node.get_center(), color=ManimColor("#B0BEC5"), stroke_width=2.0)
                l.set_z_index(-1)
                lines_in_hid.add(l)
                seq1_anims.append(Create(l, run_time=0.1))
            seq1_anims.append(GrowFromCenter(h_node, run_time=0.15))
            
        self.play(Succession(*seq1_anims))
        
        # Sequence 2: Sequential Intersecting Flow Hidden -> Output (Strict One by One)
        seq2_anims = []
        for i, o_node in enumerate(out_nodes):
            for h_node in hidden_nodes:
                l = Line(h_node.get_center(), o_node.get_center(), color=ManimColor("#B0BEC5"), stroke_width=2.0)
                l.set_z_index(-1)
                lines_hid_out.add(l)
                seq2_anims.append(Create(l, run_time=0.08))
                
            seq2_anims.append(
                AnimationGroup(
                    SpinInFromNothing(o_node, run_time=0.3),
                    FadeIn(out_labels[i], shift=LEFT*0.3, run_time=0.3)
                )
            )
            
        self.play(Succession(*seq2_anims))
        
        # Sequence 3: Golden Data Flow Dots (Reverted to simple MoveAlongPath + FadeOut)
        self.add(lines_in_hid, lines_hid_out)
        
        dot_flow_anims = []
        for line in lines_in_hid:
            dot = Dot(color=ManimColor("#FFCA28"), radius=0.06).set_z_index(5)
            flow = Succession(
                MoveAlongPath(dot, line, rate_func=rate_functions.linear, run_time=0.6),
                FadeOut(dot, run_time=0.2)
            )
            dot_flow_anims.append(flow)
            
        self.play(LaggedStart(*dot_flow_anims, lag_ratio=0.03, run_time=0.8))
        
        dot_flow_anims_out = []
        for line in lines_hid_out:
            dot = Dot(color=ManimColor("#FFCA28"), radius=0.06).set_z_index(5)
            flow = Succession(
                MoveAlongPath(dot, line, rate_func=rate_functions.linear, run_time=0.6),
                FadeOut(dot, run_time=0.2)
            )
            dot_flow_anims_out.append(flow)
            
        self.play(LaggedStart(*dot_flow_anims_out, lag_ratio=0.03, run_time=0.8))
        
        # Optional: Final Pulse the network to show "activation"
        all_lines = VGroup(*lines_in_hid, *lines_hid_out)
        self.play(
            all_lines.animate.set_color(ManimColor("#FFCA28")).set_stroke_width(3),
            run_time=0.5,
            rate_func=rate_functions.there_and_back
        )
        
        self.wait(0.2)
        
        # ── 21. Final Scene Collapse ───────────────────────────────────────
        # Group everything making up the network properly (using Group instead of VGroup 
        # because out_nodes contains ImageMobjects)
        neural_network_group = Group(
            lines_in_hid, lines_hid_out,
            node_mod, node_fair, node_non,
            hidden_nodes, out_nodes, out_labels
        )
        # Drop the network visually behind the logo
        neural_network_group.set_z_index(-10)
        logo.set_z_index(20)
        
        # Collapse into the center of the logo and disappear
        self.play(
            neural_network_group.animate.move_to(logo.get_center()).scale(1e-5), # Scale almost to zero
            run_time=0.8,
            rate_func=rate_functions.ease_in_back
        )
        self.remove(neural_network_group)
        self.wait(0.5)
        
        self.wait(0.5)
