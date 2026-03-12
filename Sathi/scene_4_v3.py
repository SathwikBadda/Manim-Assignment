from manim import *
import numpy as np
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
#  PALETTE
# ─────────────────────────────────────────────────────────────────
BG          = "#F2EFE9"
GRAD_TOP    = "#5B8DB8"       # sky blue  (top of building)
GRAD_BOT    = "#1B2A4A"       # deep navy (base of building)
STONE       = "#D4C9B5"
STONE_DRK   = "#B0A898"
GOLD        = "#C9A84C"
WIN_BASE    = ManimColor("#A8D8EA")
WIN_GLARE   = ManimColor("#E8F6FF")
DOOR_COL    = "#0D1B2A"
FLAG_COL    = "#E05A2B"
TEXT_COL    = "#1B2A4A"
POLE_COL    = "#9AABB8"
FONT        = "Libre Baskerville"

def gradient_rect(width, height, top_col, bot_col, stroke_col=None, sw=1.4):
    n = 40
    strips = VGroup()
    for i in range(n):
        t   = i / (n - 1)
        col = interpolate_color(ManimColor(top_col), ManimColor(bot_col), t)
        s   = Rectangle(
            width=width, height=height / n,
            fill_color=col, fill_opacity=1,
            stroke_width=0,
        )
        strips.add(s)
    strips.arrange(DOWN, buff=0)

    result = VGroup(strips)
    if stroke_col:
        border = Rectangle(
            width=width, height=height,
            fill_opacity=0,
            stroke_color=stroke_col, stroke_width=sw,
        )
        border.move_to(strips.get_center())
        result.add(border)
    return result

class BuildingScene(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        # ═══════════════════════════════════════════════════════
        #  WINDOW HELPER
        # ═══════════════════════════════════════════════════════
        def win(size=0.26):
            return Rectangle(
                width=size, height=size * 1.3,
                fill_color=WIN_BASE, fill_opacity=1,
                stroke_color=ManimColor("#1A2A40"), stroke_width=0.8,
            )

        def win_grid(cols, rows, pad_h=0.20, pad_v=0.24):
            g = VGroup(*[win() for _ in range(cols * rows)])
            g.arrange_in_grid(rows=rows, cols=cols,
                              h_buff=pad_h, v_buff=pad_v)
            return g

        # ═══════════════════════════════════════════════════════
        #  BUILDING PARTS
        # ═══════════════════════════════════════════════════════

        # wing dimensions
        iwing_w, iwing_h = 1.6, 2.2  
        owing_w, owing_h = 1.3, 1.4  

        def make_wing(w, h, cols, rows):
            wing = gradient_rect(w, h, GRAD_TOP, GRAD_BOT,
                                 stroke_col=ManimColor("#0D1F35"), sw=1.2)
            wins = win_grid(cols, rows, pad_h=0.18, pad_v=0.22)
            
            ledge = Rectangle(width=w + 0.12, height=0.13,
                              fill_color=STONE, fill_opacity=1,
                              stroke_color=STONE_DRK, stroke_width=0.8)
            wins.move_to(wing.get_center())
            ledge.next_to(wing, UP, buff=0)
            
            return VGroup(wing, wins, ledge), wing, wins, ledge

        left_iwing_g, left_iwing, liw_wins, li_ledge = make_wing(iwing_w, iwing_h, 2, 3)
        right_iwing_g, right_iwing, riw_wins, ri_ledge = make_wing(iwing_w, iwing_h, 2, 3)
        
        left_owing_g, left_owing, low_wins, lo_ledge = make_wing(owing_w, owing_h, 2, 2)
        right_owing_g, right_owing, row_wins, ro_ledge = make_wing(owing_w, owing_h, 2, 2)

        def make_sub_building():
            c_w, c_h = 2.0, 2.2
            center = gradient_rect(c_w, c_h, GRAD_TOP, GRAD_BOT, stroke_col=ManimColor("#0D1F35"), sw=1.2)
            center.set_z_index(4)
            c_wins = win_grid(2, 2, pad_h=0.18, pad_v=0.22)
            c_wins.move_to(center.get_center() + UP * 0.3)
            
            d_w, d_h = 0.8, 0.9
            d_bg = Rectangle(width=d_w, height=d_h, fill_color=ManimColor("#FFE8A1"), fill_opacity=1, stroke_width=0)
            d_bg.set_z_index(1)
            d_left = Rectangle(width=d_w / 2 - 0.02, height=d_h - 0.04, fill_color=WIN_BASE, fill_opacity=0.9, stroke_color=ManimColor("#1A2A40"), stroke_width=1)
            d_right = Rectangle(width=d_w / 2 - 0.02, height=d_h - 0.04, fill_color=WIN_BASE, fill_opacity=0.9, stroke_color=ManimColor("#1A2A40"), stroke_width=1)
            d_left.set_z_index(3)
            d_right.set_z_index(3)
            d_left.move_to(d_bg.get_center() + LEFT * (d_w / 4))
            d_right.move_to(d_bg.get_center() + RIGHT * (d_w / 4))
            d_frame = Rectangle(width=d_w + 0.1, height=d_h + 0.05, fill_opacity=0, stroke_color=GOLD, stroke_width=2)
            d_frame.align_to(d_bg, DOWN)
            
            door = VGroup(d_bg, d_left, d_right, d_frame)
            door.align_to(center, DOWN)
            door.set_x(center.get_x())
            
            cornice = Rectangle(width=c_w + 0.1, height=0.12, fill_color=STONE, fill_opacity=1, stroke_color=STONE_DRK, stroke_width=0.8)
            cornice.next_to(center, UP, buff=0)
            
            roof = Polygon(
                cornice.get_corner(UL), cornice.get_corner(UR),
                cornice.get_center() + UP * 0.6,
                fill_color=ManimColor(GRAD_TOP), fill_opacity=1, stroke_color=GOLD, stroke_width=1.2
            )
            
            w_w, w_h = 1.0, 1.4
            l_wing_g, _, lw_wins, _ = make_wing(w_w, w_h, 1, 2)
            r_wing_g, _, rw_wins, _ = make_wing(w_w, w_h, 1, 2)
            
            l_wing_g.next_to(center, LEFT, buff=0, aligned_edge=DOWN)
            r_wing_g.next_to(center, RIGHT, buff=0, aligned_edge=DOWN)
            
            bg_group = VGroup(l_wing_g, r_wing_g, center, c_wins, door, cornice, roof)
            return bg_group, [c_wins, lw_wins, rw_wins], door, d_left, d_right

        block_b_g, block_b_wins, block_b_door, bb_d_left, bb_d_right = make_sub_building()

        # ═══════════════════════════════════════════════════════
        #  CENTRAL BLOCK - Classy
        # ═══════════════════════════════════════════════════════
        ctr_w, ctr_h = 2.8, 3.0

        centre = gradient_rect(ctr_w, ctr_h, GRAD_TOP, GRAD_BOT,
                               stroke_col=ManimColor("#0D1F35"), sw=1.5)
        centre.set_z_index(4)

        ctr_wins = win_grid(3, 3, pad_h=0.18, pad_v=0.22)
        ctr_wins.move_to(centre.get_center() + UP * 0.45)

        # Sliding door
        door_width, door_height = 0.9, 1.0
        door_bg = Rectangle(width=door_width, height=door_height,
                            fill_color=ManimColor("#FFE8A1"), fill_opacity=1, stroke_width=0)
        door_bg.set_z_index(1)
        door_left = Rectangle(width=door_width / 2 - 0.02, height=door_height - 0.04,
                              fill_color=WIN_BASE, fill_opacity=0.9,
                              stroke_color=ManimColor("#1A2A40"), stroke_width=1)
        door_left.set_z_index(3)
        door_right = Rectangle(width=door_width / 2 - 0.02, height=door_height - 0.04,
                               fill_color=WIN_BASE, fill_opacity=0.9,
                               stroke_color=ManimColor("#1A2A40"), stroke_width=1)
        door_right.set_z_index(3)
        
        door_left.move_to(door_bg.get_center() + LEFT * (door_width / 4))
        door_right.move_to(door_bg.get_center() + RIGHT * (door_width / 4))
        
        door_frame = Rectangle(width=door_width + 0.1, height=door_height + 0.05,
                               fill_opacity=0, stroke_color=GOLD, stroke_width=2)
        door_frame.align_to(door_bg, DOWN)
        
        door = VGroup(door_bg, door_left, door_right, door_frame)
        door.align_to(centre, DOWN)
        door.set_x(centre.get_x())

        # pilasters — subtle, same blue family
        col_l = Line(centre.get_corner(DL) + RIGHT * 0.22,
                     centre.get_corner(UL) + RIGHT * 0.22,
                     color=ManimColor("#A8C4D8"), stroke_width=1.5)
        col_r = Line(centre.get_corner(DR) + LEFT * 0.22,
                     centre.get_corner(UR) + LEFT * 0.22,
                     color=ManimColor("#A8C4D8"), stroke_width=1.5)

        # cornice
        cornice = Rectangle(width=ctr_w + 0.12, height=0.14,
                            fill_color=STONE, fill_opacity=1,
                            stroke_color=STONE_DRK, stroke_width=0.8)
        cornice.next_to(centre, UP, buff=0)

        # Dome explicitly shaped
        dome = Arc(radius=(ctr_w + 0.12) / 2, start_angle=0, angle=PI,
                   fill_color=ManimColor(GRAD_TOP), fill_opacity=1,
                   stroke_color=GOLD, stroke_width=1.8)
        dome.next_to(cornice, UP, buff=0)
        
        # Lantern on dome
        lantern = Rectangle(width=0.35, height=0.45, fill_color=STONE, fill_opacity=1,
                            stroke_color=GOLD, stroke_width=1.2)
        lantern.next_to(dome, UP, buff=-0.1)
        lantern.set_z_index(-1)

        # (flag_g added after pole/flag creation below)
        centre_g = VGroup(centre, ctr_wins, door, col_l, col_r,
                          cornice, dome, lantern)

        # ═══════════════════════════════════════════════════════
        #  FLAG
        # ═══════════════════════════════════════════════════════
        pole_bot = lantern.get_top()
        pole = Line(pole_bot, pole_bot + UP * 0.9,
                    color=POLE_COL, stroke_width=2.5)
        flag = Rectangle(width=0.55, height=0.35,
                         fill_color=FLAG_COL, fill_opacity=1, stroke_width=0)
        flag.next_to(pole.get_end(), RIGHT, buff=0.02)
        flag_g = VGroup(pole, flag)
        # Add flag to centre_g so it moves as one unit
        centre_g.add(flag_g)

        # ═══════════════════════════════════════════════════════
        #  ASSEMBLE BUILDING & STEPS
        # ═══════════════════════════════════════════════════════
        centre_g.move_to([0, -0.6, 0])  # Anchor the center
        left_iwing_g.next_to(centre_g, LEFT, buff=0, aligned_edge=DOWN)
        right_iwing_g.next_to(centre_g, RIGHT, buff=0, aligned_edge=DOWN)
        
        left_owing_g.next_to(left_iwing_g, LEFT, buff=0, aligned_edge=DOWN)
        right_owing_g.next_to(right_iwing_g, RIGHT, buff=0, aligned_edge=DOWN)
        
        block_b_g.next_to(right_owing_g, RIGHT, buff=0, aligned_edge=DOWN)

        # Build steps that PERFECTLY frame this asymmetrical building
        left_bound = left_owing_g.get_left()[0]
        right_bound = block_b_g.get_right()[0]
        b_width = right_bound - left_bound
        
        step3_w = b_width + 1.2 # 0.6 padding on each side
        step3_cx = (left_bound + right_bound) / 2
        
        step3 = Rectangle(width=step3_w, height=0.20, fill_color=STONE, fill_opacity=1, stroke_color=STONE_DRK, stroke_width=1)
        step3.next_to(centre_g, DOWN, buff=0)
        step3.set_x(step3_cx)
        
        step2 = Rectangle(width=step3_w + 1.5, height=0.20, fill_color=STONE, fill_opacity=1, stroke_color=STONE_DRK, stroke_width=1)
        step2.next_to(step3, DOWN, buff=0).set_x(step3_cx)
        
        step1 = Rectangle(width=step3_w + 3.0, height=0.20, fill_color=STONE, fill_opacity=1, stroke_color=STONE_DRK, stroke_width=1)
        step1.next_to(step2, DOWN, buff=0).set_x(step3_cx)
        
        ground = Rectangle(width=step3_w + 5.0, height=0.20, fill_color=STONE_DRK, fill_opacity=1, stroke_width=0)
        ground.next_to(step1, DOWN, buff=0).set_x(step3_cx)
        
        steps = VGroup(ground, step1, step2, step3)

        # ═══════════════════════════════════════════════════════
        #  WINDOWS flat list
        # ═══════════════════════════════════════════════════════
        all_win_list = list(liw_wins) + list(riw_wins) + list(low_wins) + list(row_wins) + list(ctr_wins) + [door_left, door_right]
        for w_group in block_b_wins:
            all_win_list.extend(list(w_group))
        all_win_list.extend([bb_d_left, bb_d_right])

        # ═══════════════════════════════════════════════════════
        #  SHIFT OFF-SCREEN FOR OLD APPEAR ANIMATION
        # ═══════════════════════════════════════════════════════
        everything = VGroup(steps, block_b_g, left_owing_g, right_owing_g, left_iwing_g, right_iwing_g,
                            centre_g)
        everything.move_to(ORIGIN)
        everything.shift(DOWN * 1.05)
        everything.scale(1.0)
        
        # Shift specifically for the drop down animation
        for part in [steps, block_b_g, left_owing_g, right_owing_g, left_iwing_g, right_iwing_g, centre_g]:
            part.shift(DOWN * 7)
            
        everything.set_z_index(4)

        # ═══════════════════════════════════════════════════════
        #  BALLS A, B, C, D (continuous wavy stream)
        # ═══════════════════════════════════════════════════════
        grades = ["A", "B", "C", "D"]
        init_col = ManimColor("#3AA3F9")
        final_col = ManimColor("#2C3E78")
        
        # 36 balls flying in
        balls = VGroup()
        for i in range(36):
            b = Circle(radius=0.35, fill_color=init_col, fill_opacity=1, stroke_width=3, stroke_color=WHITE)
            t = Text(grades[i % 4], font_size=28, color=WHITE, font=FONT, weight=BOLD)
            t.move_to(b.get_center())
            bt = VGroup(b, t)
            balls.add(bt)
            
        balls_start_x = -22.0
        for b in balls:
            b.move_to([balls_start_x, 5.0, 0])
            b.set_z_index(5)

        # ═══════════════════════════════════════════════════════
        #  ANIMATIONS
        # ═══════════════════════════════════════════════════════

        # window glare updater
        t_ref = [0.0]
        def glare_updater(mob, dt):
            t_ref[0] += dt
            t = t_ref[0]
            for i, w in enumerate(all_win_list):
                phase = (t * 1.6 + i * 0.6) % (2 * PI)
                alpha = 0.5 + 0.5 * np.sin(phase)
                w.set_fill(interpolate_color(WIN_BASE, WIN_GLARE, alpha), opacity=1)

        dummy = VMobject()
        dummy.add_updater(glare_updater)
        self.add(dummy)

        # 1. Start camera tight, showing the foundation
        # We start with width=24, centered slightly right
        self.camera.frame.set_width(24)
        self.camera.frame.move_to([2.0, 0, 0])

        # 2. Old Building Animation: drop down from above/shift up
        y_shift = UP * 7
        everything.shift(DOWN * 0.5) # ensure base starts slightly lower
        
        self.play(steps.animate.shift(y_shift), rate_func=rate_functions.ease_out_back, run_time=0.40)
        self.play(
            block_b_g.animate.shift(y_shift),
            left_owing_g.animate.shift(y_shift), right_owing_g.animate.shift(y_shift),
            rate_func=rate_functions.ease_out_back, run_time=0.40
        )
        self.play(
            left_iwing_g.animate.shift(y_shift), right_iwing_g.animate.shift(y_shift),
            rate_func=rate_functions.ease_out_back, run_time=0.50
        )
        self.play(centre_g.animate.shift(y_shift), rate_func=rate_functions.ease_out_back, run_time=0.55)
        # flag is now inside centre_g, no separate animation needed
        
        # 3. Wait 1 second, then zoom out
        self.wait(1.0)
        
        target_width = config.frame_width * 2.5 
        
        self.play(
            self.camera.frame.animate.set_width(target_width).move_to([2.0, 2.0, 0]),
            rate_func=rate_functions.smooth, run_time=2.0
        )
        
        # 4. Open center door only
        door_movement = (door_width / 2 - 0.05) * 0.85 # accommodate scale
        self.play(
            door_left.animate.shift(LEFT * door_movement),
            door_right.animate.shift(RIGHT * door_movement),
            run_time=0.8, rate_func=rate_functions.ease_in_out_sine
        )
        
        self.add(balls)
        
        # 5. Wavy approach from left
        wave_time = ValueTracker(0)
        
        # calculate door bottom center explicitly
        door_cx = door_bg.get_center()[0]
        door_cy = door_bg.get_bottom()[1] + 0.3
        
        def make_ball_updater(idx, ball_group):
            circle = ball_group[0]
            def upd(mob):
                t = wave_time.get_value()
                lag_t = t - idx * 0.45 
                
                if lag_t < 0:
                    mob.set_opacity(0)
                elif lag_t < 4.0:
                    alpha = lag_t / 4.0
                    
                    curr_x = np.interp(alpha, [0, 1.0], [balls_start_x, door_cx])
                    
                    mob.set_opacity(1)
                    if alpha < 0.9:
                        mob.set_z_index(5) # in front of building facade
                    else:
                        mob.set_z_index(2) # behind sliding doors, in front of yellow bg
                    
                    curr_scale = np.interp(alpha, [0, 0.8, 1.0], [0.7, 0.7, 0.1])
                    mob.scale_to_fit_height(curr_scale)
                    
                    base_y = np.interp(alpha, [0, 0.6, 1.0], [5.0, door_cy + 1.2, door_cy]) 
                    amp = np.interp(alpha, [0, 0.8, 1.0], [1.0, 0.5, 0.0])
                    wave_y = amp * (0.5 * np.sin(0.9 * curr_x) + 0.3 * np.cos(0.4 * curr_x))
                    
                    mob.move_to([curr_x, base_y + wave_y, 0])
                    
                    if alpha < 0.8:
                        circle.set_fill(init_col)
                    else:
                        c_alpha = (alpha - 0.8) / 0.2
                        circle.set_fill(interpolate_color(init_col, final_col, c_alpha))
                        if c_alpha > 0.5:
                            mob.set_opacity(1 - (c_alpha - 0.5) / 0.5)
                else:
                    mob.set_opacity(0)
            return upd
            
        for i, b in enumerate(balls):
            b.add_updater(make_ball_updater(i, b))
            
        self.play(wave_time.animate.set_value(21.0), run_time=12.0, rate_func=linear)
        
        for b in balls:
            b.clear_updaters()

        # 6A. Create 4 panels (staggered) to the right of the building
        panel_data = [
            ("Critical\nThinking",  15.0, 1.5),
            ("Collaboration",        22.0, 0.5),
            ("Creativity",           29.0, 2.0),
            ("Communication",        36.0, 0.8),
        ]
        panel_width, panel_height = 3.8, 2.2
        panel_color   = ManimColor("#1B2A4A")
        panel_accent  = ManimColor("#C9A84C")  # gold
        
        panels = VGroup()
        panel_centers = []

        for label, px, py in panel_data:
            bg = RoundedRectangle(
                corner_radius=0.25,
                width=panel_width, height=panel_height,
                fill_color=panel_color, fill_opacity=1,
                stroke_color=panel_accent, stroke_width=2.5
            )
            bg.move_to([px, py, 0])
            
            # Gold top accent bar
            accent_bar = Rectangle(width=panel_width, height=0.2,
                                   fill_color=panel_accent, fill_opacity=1, stroke_width=0)
            accent_bar.align_to(bg, UP)
            accent_bar.set_x(bg.get_x())
            
            txt = Text(label, font_size=28, color=WHITE, font=FONT, weight=BOLD,
                       line_spacing=1.2)
            txt.move_to(bg.get_center())
            
            panel_g = VGroup(bg, accent_bar, txt)
            panel_g.set_z_index(3)
            panels.add(panel_g)
            panel_centers.append([px, py, 0])

        # Fade in panels before camera pans
        self.play(FadeIn(panels, shift=UP * 0.5), run_time=1.2)

        # 6B. Pan Camera Right slowly as balls come out – building exits left
        # Open Block B door first
        bb_door_movement = (0.8 / 2 - 0.05) * 0.85
        self.play(
            bb_d_left.animate.shift(LEFT * bb_door_movement),
            bb_d_right.animate.shift(RIGHT * bb_door_movement),
            run_time=0.8, rate_func=rate_functions.ease_in_out_sine
        )

        # 7. Outgoing balls from Block B; they weave AROUND panels
        out_balls = VGroup()
        for i in range(36):
            b = Circle(radius=0.35, fill_color=final_col, fill_opacity=1, stroke_width=3, stroke_color=WHITE)
            t = Text(grades[i % 4], font_size=28, color=WHITE, font=FONT, weight=BOLD)
            t.move_to(b.get_center())
            bt = VGroup(b, t)
            out_balls.add(bt)
            
        bb_door_cx = block_b_door.get_center()[0]
        bb_door_cy = block_b_door.get_bottom()[1] + 0.3
        
        for b in out_balls:
            b.move_to([bb_door_cx, bb_door_cy, 0])
            b.set_z_index(2)
            b.set_opacity(0)
            
        self.add(out_balls)
        
        out_wave_time = ValueTracker(0)

        # ── SNAKE PATH COMPUTATION ────────────────────────────────────
        # For each panel, balls either pass ABOVE or BELOW in strict alternation.
        # We pre-build two piecewise-linear paths (A and B) that zigzag
        # through every panel staying strictly outside panel boundaries.
        pw2 = panel_width  / 2.0   # 1.9  – half-width
        ph2 = panel_height / 2.0   # 1.1  – half-height
        ball_r  = 0.35
        clr     = 0.6              # clear gap from panel edge to ball centre

        # y-positions balls must reach above / below each panel
        above_ys = [cy + ph2 + ball_r + clr for (_, _, cy) in panel_data]
        below_ys = [cy - ph2 - ball_r - clr for (_, _, cy) in panel_data]
        panel_xs  = [px for (_, px, _) in panel_data]

        # x-margin: ball must reach its panel-y BEFORE entering the panel x-range
        x_entry = pw2 + 1.2   # approach start:  panel_cx - x_entry
        x_exit  = pw2 + 1.2   # departure end:   panel_cx + x_exit

        bx     = bb_door_cx
        by_d   = bb_door_cy
        out_end_x = panel_xs[-1] + 6.0   # finish a bit after last panel

        def build_path(start_above):
            """Build waypoints. start_above=True → panel-0 is above."""
            pts_x = [bx]
            pts_y = [by_d]
            for i, px in enumerate(panel_xs):
                use_above = (start_above and i % 2 == 0) or (not start_above and i % 2 == 1)
                py = above_ys[i] if use_above else below_ys[i]
                pts_x.append(px - x_entry)
                pts_y.append(py)
                pts_x.append(px + x_exit)
                pts_y.append(py)
            # tail – fly away
            pts_x.append(out_end_x)
            pts_y.append(above_ys[-1] if (start_above and len(panel_xs) % 2 == 1) else below_ys[-1])
            return pts_x, pts_y

        xs_A, ys_A = build_path(start_above=True)   # even-idx balls
        xs_B, ys_B = build_path(start_above=False)  # odd-idx  balls

        def make_out_updater(idx, ball_group):
            # capture path choice at definition time
            xs_p = xs_A if idx % 2 == 0 else xs_B
            ys_p = ys_A if idx % 2 == 0 else ys_B

            def upd(mob):
                t = out_wave_time.get_value()
                lag_t = t - idx * 0.45

                if lag_t < 0:
                    mob.set_opacity(0)
                elif lag_t < 4.0:
                    alpha = lag_t / 4.0

                    curr_x = np.interp(alpha, [0, 1.0], [bx, out_end_x])

                    curr_scale = np.interp(alpha, [0, 0.4, 1.0], [0.1, 0.7, 0.7])
                    mob.scale_to_fit_height(curr_scale)
                    mob.set_z_index(6)

                    # Strict piecewise-linear – no extra wave that could cause collision
                    base_y = float(np.interp(curr_x, xs_p, ys_p))
                    mob.move_to([curr_x, base_y, 0])

                    if alpha < 0.12:
                        mob.set_opacity(alpha / 0.12)
                    elif alpha > 0.88:
                        mob.set_opacity(1 - (alpha - 0.88) / 0.12)
                    else:
                        mob.set_opacity(1)
                else:
                    mob.set_opacity(0)
            return upd

        for i, b in enumerate(out_balls):
            b.add_updater(make_out_updater(i, b))

        # 8. During the outgoing balls, pan camera right so building exits left frame
        self.play(
            out_wave_time.animate.set_value(21.0),
            self.camera.frame.animate.move_to([28.0, 2.5, 0]),
            run_time=13.0, rate_func=linear
        )
        
        for b in out_balls:
            b.clear_updaters()
        
        self.wait(1.5)
        dummy.clear_updaters()

if __name__ == "__main__":
    config.processes = 4
    config.max_files_cached = 200
    config.progress_bar = "none"
    config.enable_cuda = True

