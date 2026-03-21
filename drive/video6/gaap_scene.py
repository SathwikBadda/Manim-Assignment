"""
GAAP Animation Scene — Complete Recreation
Based on scene_recreation_instructions.json

Render command:
    manim -pql --resolution 640,360 --frame_rate 15 gaap_scene.py GAAPScene

Note:
- ImageMobject placeholders are replaced with SVG/VMobject stand-ins.
- Asset1 (financial document) is implemented inline as a VMobject.
- Font "Avenir" falls back to system sans-serif if not installed.
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
PRIMARY_BLUE       = "#084993"
ORANGE_ACCENT      = "#ed8c32"
LIGHT_BLUE_FILL    = "#DEEBF7"
SKY_BLUE_STRIP     = "#85c2e0"
PALE_YELLOW        = "#FFFFE4"
DARK_NAVY          = "#1a5276"
LIGHT_YELLOW_COL   = "#FFF9C4"
LIGHT_RED_COL      = "#FFEBEE"
LIGHT_GREEN_COL    = "#E8F5E9"
LIGHT_BLUE_COL     = "#E1F5FE"
COIN_GOLD          = "#FFD700"
COIN_BORDER        = "#DAA520"

FONT = "Avenir"   # falls back gracefully


# ─────────────────────────────────────────────────────────────────────────────
# HELPER MOBJECTS
# ─────────────────────────────────────────────────────────────────────────────

def make_circle_letter(letter: str, radius: float = 0.7) -> VGroup:
    """Filled white circle with blue stroke + centred letter."""
    circ = Circle(
        radius=radius,
        fill_color=WHITE,
        fill_opacity=1,
        stroke_color=PRIMARY_BLUE,
        stroke_width=8,
    )
    lbl = Text(letter, font_size=72, color=PRIMARY_BLUE, weight=BOLD)
    lbl.move_to(circ.get_center())
    grp = VGroup(circ, lbl)
    grp.set_z_index(3)
    return grp


def make_asset1(
    sheet_w=1.0, sheet_h=1.3,
    sheet_color=PALE_YELLOW,
    line_color=ORANGE_ACCENT,
    currency_color=PRIMARY_BLUE,
) -> VGroup:
    """Stylised financial-document icon (replaces asset_1.py)."""
    # Document body
    body = Rectangle(width=sheet_w, height=sheet_h,
                     fill_color=sheet_color, fill_opacity=1,
                     stroke_color=line_color, stroke_width=2)
    # Fold triangle in top-right corner
    fold_size = 0.2 * sheet_w
    tr = body.get_corner(UR)
    fold = Polygon(
        tr + LEFT * fold_size,
        tr + DOWN * fold_size,
        tr,
        fill_color=line_color, fill_opacity=0.6, stroke_width=0,
    )
    # Lines on document
    lines = VGroup(*[
        Line(
            body.get_left() + RIGHT * 0.15 + UP * (0.4 - 0.18 * i),
            body.get_right() + LEFT * 0.15 + UP * (0.4 - 0.18 * i),
            stroke_color=line_color, stroke_width=1.2,
        )
        for i in range(3)
    ])
    # Currency symbol
    sym = Text("$", font_size=28, color=currency_color, weight=BOLD)
    sym.move_to(body.get_center() + DOWN * 0.25)
    return VGroup(body, fold, lines, sym)


def make_doc_outline(w=1.4, h=1.82, fold=0.28) -> VMobject:
    """5-corner document polygon outline."""
    poly = Polygon(
        [-w/2, -h/2, 0],
        [ w/2 - fold, -h/2, 0],
        [ w/2, -h/2 + fold, 0],
        [ w/2,  h/2, 0],
        [-w/2,  h/2, 0],
        fill_color=PALE_YELLOW, fill_opacity=1,
        stroke_color=ORANGE_ACCENT, stroke_width=2,
    )
    return poly


def make_gear(outer_r=0.5, inner_r=0.4, teeth=8) -> VMobject:
    """Gear VMobject with `teeth` rectangular teeth."""
    pts = []
    for i in range(teeth):
        for r, da in [(inner_r, 0), (outer_r, 0.5), (outer_r, 1.0), (inner_r, 1.5)]:
            angle = (i * 4 + [0, 0.5, 1.0, 1.5].index([0, 0.5, 1.0, 1.5][[0,0.5,1.0,1.5].index(da)])) / (4 * teeth) * TAU
            angle = (i + [0, 0.5, 1.0, 1.5].index(da) / 4) / teeth * TAU
            pts.append([r * np.cos(angle), r * np.sin(angle), 0])
    gear = VMobject(stroke_color=PRIMARY_BLUE, stroke_width=3, fill_opacity=0)
    gear.set_points_as_corners([*pts, pts[0]])
    return gear


def make_rounded_box(w, h, r=0.15, fill=LIGHT_BLUE_FILL, stroke=PRIMARY_BLUE, sw=1.5) -> RoundedRectangle:
    return RoundedRectangle(
        width=w, height=h, corner_radius=r,
        fill_color=fill, fill_opacity=1,
        stroke_color=stroke, stroke_width=sw,
    )


def make_us_map_placeholder() -> VMobject:
    """Simple silhouette approximation of the contiguous USA."""
    # Rough bounding polygon that suggests a USA outline
    pts = [
        [-3.0,  0.5], [-2.5,  1.2], [-1.8,  1.4], [-0.5,  1.5],
        [ 0.5,  1.4], [ 1.5,  1.5], [ 2.5,  1.3], [ 3.0,  0.6],
        [ 3.2, -0.2], [ 2.8, -1.0], [ 2.0, -1.4], [ 1.0, -1.5],
        [ 0.0, -1.3], [-0.8, -1.5], [-1.8, -1.2], [-2.6, -0.6],
        [-3.0, -0.1],
    ]
    shape = Polygon(*[[x, y, 0] for x, y in pts],
                    fill_color=SKY_BLUE_STRIP, fill_opacity=1,
                    stroke_width=0)
    return shape


def make_building_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    """Simple building silhouette."""
    base = Rectangle(width=1.0*scale, height=1.2*scale,
                     fill_color=color, fill_opacity=1, stroke_width=0)
    roof = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    roof.scale(0.55 * scale).next_to(base, UP, buff=0)
    windows = VGroup(*[
        Square(side_length=0.18*scale, fill_color=WHITE, fill_opacity=1, stroke_width=0)
              .move_to(base.get_center() + RIGHT * dx + UP * dy)
        for dx in [-0.2*scale, 0.2*scale]
        for dy in [0.2*scale, -0.1*scale]
    ])
    return VGroup(base, roof, windows)


def make_investor_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    """Simple stick-person investor icon."""
    head = Circle(radius=0.25*scale, fill_color=color, fill_opacity=1, stroke_width=0)
    body = Line(ORIGIN, DOWN*0.6*scale, stroke_color=color, stroke_width=4)
    l_arm = Line(ORIGIN, DL*0.4*scale, stroke_color=color, stroke_width=3)
    r_arm = Line(ORIGIN, DR*0.4*scale, stroke_color=color, stroke_width=3)
    l_leg = Line(ORIGIN, DL*0.5*scale, stroke_color=color, stroke_width=3)
    r_leg = Line(ORIGIN, DR*0.5*scale, stroke_color=color, stroke_width=3)
    body_grp = VGroup(body, l_arm, r_arm)
    body_grp.shift(head.get_bottom())
    leg_grp = VGroup(l_leg, r_leg)
    leg_grp.shift(body.get_end())
    return VGroup(head, body_grp, leg_grp)


def make_shield_icon(color=PRIMARY_BLUE, scale=1.0) -> VMobject:
    pts = [[-0.4,0.6],[0.4,0.6],[0.5,0.1],[0.0,-0.5],[-0.5,0.1]]
    s = Polygon(*[[x*scale,y*scale,0] for x,y in pts],
                fill_color=color, fill_opacity=1, stroke_width=0)
    return s


def make_thumbsup_icon(color=ORANGE_ACCENT, scale=1.0) -> VGroup:
    thumb = RoundedRectangle(width=0.3*scale, height=0.7*scale, corner_radius=0.1,
                             fill_color=color, fill_opacity=1, stroke_width=0)
    hand  = Rectangle(width=0.6*scale, height=0.4*scale,
                      fill_color=color, fill_opacity=1, stroke_width=0)
    hand.next_to(thumb, DOWN, buff=0)
    return VGroup(thumb, hand)


def make_calculator_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    body = RoundedRectangle(width=0.7*scale, height=0.9*scale, corner_radius=0.1,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    screen = Rectangle(width=0.5*scale, height=0.2*scale,
                       fill_color=WHITE, fill_opacity=1, stroke_width=0)
    screen.move_to(body.get_top() + DOWN*0.15*scale)
    return VGroup(body, screen)


def make_chess_knight_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    base = Rectangle(width=0.6*scale, height=0.15*scale,
                     fill_color=color, fill_opacity=1, stroke_width=0)
    body = RoundedRectangle(width=0.4*scale, height=0.65*scale, corner_radius=0.12,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    body.next_to(base, UP, buff=0).shift(LEFT*0.05*scale)
    head = Ellipse(width=0.35*scale, height=0.3*scale,
                   fill_color=color, fill_opacity=1, stroke_width=0)
    head.next_to(body, UR, buff=-0.15*scale)
    return VGroup(base, body, head)


def make_warn_icon(scale=1.0) -> VGroup:
    tri = Triangle(fill_color=ORANGE_ACCENT, fill_opacity=1, stroke_width=0).scale(0.4*scale)
    ex  = Text("!", font_size=int(22*scale), color=WHITE, weight=BOLD).move_to(tri)
    return VGroup(tri, ex)


def make_gov_building_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    base   = Rectangle(width=0.9*scale, height=0.6*scale,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    pillars = VGroup(*[
        Rectangle(width=0.08*scale, height=0.45*scale,
                  fill_color=WHITE, fill_opacity=0.4, stroke_width=0)
        .move_to(base.get_left() + RIGHT*(0.15+i*0.22)*scale + UP*0.07*scale)
        for i in range(4)
    ])
    roof   = Rectangle(width=1.0*scale, height=0.12*scale,
                       fill_color=color, fill_opacity=1, stroke_width=0)
    roof.next_to(base, UP, buff=0)
    return VGroup(base, pillars, roof)


def make_book_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    left_page  = Rectangle(width=0.4*scale, height=0.55*scale,
                           fill_color=LIGHT_BLUE_FILL, fill_opacity=1,
                           stroke_color=color, stroke_width=1.5)
    right_page = Rectangle(width=0.4*scale, height=0.55*scale,
                           fill_color=WHITE, fill_opacity=1,
                           stroke_color=color, stroke_width=1.5)
    right_page.next_to(left_page, RIGHT, buff=0.02*scale)
    spine = Line(left_page.get_right(), right_page.get_left(),
                 stroke_color=color, stroke_width=2)
    return VGroup(left_page, right_page, spine)


def make_fasb_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    doc  = Rectangle(width=0.55*scale, height=0.4*scale,
                     fill_color=LIGHT_BLUE_FILL, fill_opacity=1,
                     stroke_color=color, stroke_width=1.5)
    lbl  = Text("FASB", font_size=int(12*scale), color=color, weight=BOLD)
    lbl.move_to(doc)
    return VGroup(doc, lbl)


def make_people_icon(color=PRIMARY_BLUE, scale=1.0) -> VGroup:
    heads = VGroup(*[
        Circle(radius=0.12*scale, fill_color=color, fill_opacity=1, stroke_width=0)
        .shift(RIGHT * i * 0.28 * scale)
        for i in range(3)
    ])
    return heads


def make_barchart_icon(scale=1.0) -> VGroup:
    bars = VGroup(*[
        Rectangle(width=0.12*scale, height=h*scale,
                  fill_color=PRIMARY_BLUE, fill_opacity=1, stroke_width=0)
        .align_to(Line(ORIGIN, DOWN*0.5*scale), DOWN)
        .shift(RIGHT*i*0.17*scale)
        for i, h in enumerate([0.25, 0.45, 0.35])
    ])
    return bars


def make_piechart_icon(scale=1.0) -> VGroup:
    circ = Circle(radius=0.25*scale, fill_color=PRIMARY_BLUE,
                  fill_opacity=1, stroke_width=0)
    wedge = Sector(outer_radius=0.25*scale, angle=PI/3, start_angle=0,
                   fill_color=ORANGE_ACCENT, fill_opacity=1, stroke_width=0)
    wedge.shift(circ.get_center())
    return VGroup(circ, wedge)


def make_ruler_icon(scale=1.0) -> VGroup:
    ruler = Rectangle(width=0.8*scale, height=0.2*scale,
                      fill_color=LIGHT_YELLOW_COL, fill_opacity=1,
                      stroke_color=PRIMARY_BLUE, stroke_width=1.5)
    ticks = VGroup(*[
        Line(ruler.get_bottom() + RIGHT*(i*0.13-0.3)*scale,
             ruler.get_bottom() + RIGHT*(i*0.13-0.3)*scale + UP*0.07*scale,
             stroke_color=PRIMARY_BLUE, stroke_width=1)
        for i in range(6)
    ])
    return VGroup(ruler, ticks)


def make_magnify_icon(scale=1.0) -> VGroup:
    lens   = Circle(radius=0.2*scale, stroke_color=PRIMARY_BLUE,
                    stroke_width=2, fill_opacity=0)
    handle = Line(lens.get_corner(DR), lens.get_corner(DR)+DR*0.2*scale,
                  stroke_color=PRIMARY_BLUE, stroke_width=3)
    return VGroup(lens, handle)


def make_comparison_barchart_icon(scale=1.0) -> VGroup:
    left_bars  = VGroup(*[
        Rectangle(width=0.1*scale, height=h*scale,
                  fill_color=PRIMARY_BLUE, fill_opacity=1, stroke_width=0)
        .shift(RIGHT*i*0.14*scale)
        for i, h in enumerate([0.3, 0.5])
    ])
    right_bars = left_bars.copy().set_fill(ORANGE_ACCENT).shift(RIGHT*0.35*scale)
    return VGroup(left_bars, right_bars)


def l_shaped_connector(p_start, p_end, color=PRIMARY_BLUE, sw=1.5) -> VMobject:
    """Right-angle connector: straight down → horizontal → straight down."""
    mid_y = (p_start[1] + p_end[1]) / 2
    path = VMobject(stroke_color=color, stroke_width=sw)
    path.set_points_as_corners([
        p_start,
        [p_start[0], mid_y, 0],
        [p_end[0],   mid_y, 0],
        p_end,
    ])
    return path


def make_coin() -> VGroup:
    c = Circle(radius=0.15, fill_color=COIN_GOLD, fill_opacity=1,
               stroke_color=COIN_BORDER, stroke_width=2)
    lbl = Text("$", font_size=14, color=COIN_BORDER, weight=BOLD)
    lbl.move_to(c)
    return VGroup(c, lbl)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SCENE
# ─────────────────────────────────────────────────────────────────────────────

class GAAPScene(ThreeDScene):

    def construct(self):
        self.camera.background_color = WHITE

        # Build the four persistent GAAP circles
        letters = ["G", "A", "A", "P"]
        x_positions = [-2.4, -0.8, 0.8, 2.4]
        circles = [make_circle_letter(l) for l in letters]
        for circ, x in zip(circles, x_positions):
            circ.move_to([x, -5, 0])

        self.section_1(circles, x_positions)
        self.section_2(circles)
        self.section_3(circles)
        self.section_4(circles)
        self.section_5(circles)
        self.section_7(circles)
        self.section_8(circles)

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 1 — GAAP circles rise + US map + document + tagline
    # ─────────────────────────────────────────────────────────────────────
    def section_1(self, circles, x_positions):
        rate_fns = [there_and_back, linear, there_and_back, linear]

        # Circles rise one-by-one
        for i, (circ, x) in enumerate(zip(circles, x_positions)):
            self.play(FadeIn(circ, run_time=0.2))
            self.play(circ.animate.move_to([x, 0, 0]),
                      run_time=0.4,
                      rate_func=rate_functions.ease_out_back if i % 2 == 0 else linear)

        # US Map fades in (placeholder polygon)
        us_map = make_us_map_placeholder()
        us_map.scale(1.0).move_to(ORIGIN).set_z_index(0)
        self.play(FadeIn(us_map, run_time=0.8))

        # Financial document + outlines
        doc_main = make_asset1()
        doc_main.scale(1.4).move_to([5.8, 0, 0]).set_z_index(2)

        fold_size = 0.28
        outline1 = make_doc_outline(); outline1.move_to([5.7, 0.25, 0]).set_z_index(1)
        outline2 = make_doc_outline(); outline2.move_to([5.6, 0.50, 0]).set_z_index(1)
        outlines = VGroup(outline1, outline2)

        self.play(
            FadeIn(doc_main, run_time=0.4),
        )
        self.play(
            Rotate(doc_main, angle=TAU, axis=UP, run_time=0.8),
            LaggedStart(FadeIn(outline1), FadeIn(outline2),
                        lag_ratio=0.1, run_time=0.8),
        )

        # Supporting text + background pill
        sup_text = Text("The foundation of financial reporting",
                        font_size=64, color=PRIMARY_BLUE, weight=BOLD)
        sup_text.scale(0.5).move_to([0, -3.2, 0])

        sup_bg = RoundedRectangle(
            width=sup_text.width + 1.0, height=0.7, corner_radius=0.2,
            fill_color=LIGHT_BLUE_FILL, fill_opacity=1, stroke_width=0,
        )
        sup_bg.move_to(sup_text.get_center())

        self.play(
            FadeIn(sup_bg, run_time=0.74),
            Write(sup_text, run_time=0.74),
        )
        self.wait(0.6)

        # Clean-up (keep circles)
        self.play(
            FadeOut(VGroup(us_map, doc_main, outlines, sup_text, sup_bg)),
            run_time=1.19,
        )

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 2 — Circles to left column + flowchart
    # ─────────────────────────────────────────────────────────────────────
    def section_2(self, circles):
        circle_G, circle_A1, circle_A2, circle_P = circles
        new_positions = [
            [-5.0, 1.8, 0],
            [-5.0, 0.6, 0],
            [-5.0,-0.6, 0],
            [-5.0,-1.8, 0],
        ]

        # Scale down & reposition all circles simultaneously
        self.play(*[
            AnimationGroup(
                circ.animate.scale(0.5).move_to(pos)
            )
            for circ, pos in zip(circles, new_positions)
        ], run_time=1.5)

        # Margin strip falls from top
        margin_rect = Rectangle(
            width=1.0, height=8.0,
            fill_color=SKY_BLUE_STRIP, fill_opacity=0.3, stroke_width=0,
        )
        margin_rect.move_to([-4.8, 8, 0])
        self.add(margin_rect)
        self.play(margin_rect.animate.move_to([-5.0, 0, 0]), run_time=1.0)

        # ── Flowchart boxes ──────────────────────────────────────────────
        scandal_box = make_rounded_box(3.5, 1.2)
        scandal_icon = make_warn_icon(scale=0.8)
        scandal_icon.move_to(scandal_box.get_left() + RIGHT * 0.55)
        scandal_lbl = Text("Financial Scandal", font_size=40,
                           color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
        scandal_lbl.move_to(scandal_box.get_right() + LEFT * 0.8)
        scandal_grp = VGroup(scandal_box, scandal_icon, scandal_lbl)
        scandal_grp.move_to([1.3, 2.8, 0])
        self.play(FadeIn(scandal_grp, run_time=0.8))

        # Connectors scandal → sec & fasb
        sec_pos  = np.array([-0.5, 0.0, 0])
        fasb_pos = np.array([ 3.1, 0.0, 0])
        scandal_bottom = np.array([1.3, 2.8 - 0.6, 0])

        conn_s_sec = l_shaped_connector(
            scandal_bottom, sec_pos + np.array([0, 0.6, 0]))
        conn_s_fasb = l_shaped_connector(
            scandal_bottom, fasb_pos + np.array([0, 0.6, 0]))
        self.play(
            Create(conn_s_sec,  run_time=0.6),
            Create(conn_s_fasb, run_time=0.6),
        )

        sec_box = make_rounded_box(1.5, 1.2)
        sec_icon = make_gov_building_icon(scale=0.7)
        sec_icon.move_to(sec_box.get_center())
        sec_grp = VGroup(sec_box, sec_icon)
        sec_grp.move_to(sec_pos)

        fasb_box = make_rounded_box(1.8, 1.2)
        fasb_icon = make_fasb_icon(scale=0.6)
        fasb_icon.move_to(fasb_box.get_center())
        fasb_grp = VGroup(fasb_box, fasb_icon)
        fasb_grp.move_to(fasb_pos)

        self.play(
            FadeIn(sec_grp,  run_time=0.8),
            FadeIn(fasb_grp, run_time=0.8),
        )

        # Connectors sec & fasb → principles
        principles_pos = np.array([1.3, -2.8, 0])
        conn_sec_p  = l_shaped_connector(
            sec_pos  + np.array([0, -0.6, 0]),
            principles_pos + np.array([0, 0.6, 0]))
        conn_fasb_p = l_shaped_connector(
            fasb_pos + np.array([0, -0.6, 0]),
            principles_pos + np.array([0, 0.6, 0]))
        self.play(
            Create(conn_sec_p,  run_time=0.6),
            Create(conn_fasb_p, run_time=0.6),
        )

        principles_box = make_rounded_box(4.5, 1.2)
        principles_icon = make_book_icon(scale=0.7)
        principles_icon.move_to(principles_box.get_left() + RIGHT * 0.55)
        principles_lbl = Text("Accounting Principles", font_size=40,
                              color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
        principles_lbl.move_to(principles_box.get_right() + LEFT * 1.1)
        principles_grp = VGroup(principles_box, principles_icon, principles_lbl)
        principles_grp.move_to(principles_pos)
        self.play(FadeIn(principles_grp, run_time=0.8))

        # ── Flowing ball ─────────────────────────────────────────────────
        for _ in range(2):
            dot = Dot(color=ORANGE_ACCENT, radius=0.08).set_z_index(3)
            dot.move_to(scandal_bottom)
            self.add(dot)

            mid_y = (scandal_bottom[1] + sec_pos[1]) / 2
            mid_pt = np.array([scandal_bottom[0], mid_y, 0])

            self.play(dot.animate.move_to(mid_pt), run_time=0.4)

            dot2 = dot.copy()
            self.add(dot2)

            self.play(
                dot.animate.move_to(sec_pos  + UP * 0.6),
                run_time=0.8,
            )
            # Play dot2 to fasb separately (Manim limitation with same-obj anims)
            self.play(dot2.animate.move_to(fasb_pos + UP * 0.6), run_time=0.8)

            self.wait(0.2)

            merge_y = (sec_pos[1] + principles_pos[1]) / 2
            self.play(
                dot.animate.move_to([sec_pos[0],  merge_y, 0]), run_time=0.4,
            )
            self.play(
                dot2.animate.move_to([fasb_pos[0], merge_y, 0]), run_time=0.4,
            )
            self.remove(dot2)
            self.play(
                dot.animate.move_to([principles_pos[0], merge_y, 0]), run_time=0.4,
            )
            self.play(dot.animate.move_to(principles_pos + UP*0.6), run_time=0.4)
            self.play(FadeOut(dot, run_time=0.2))
            self.wait(0.3)

        # Clean-up flowchart, keep circles + margin
        self.play(
            FadeOut(VGroup(
                scandal_grp, sec_grp, fasb_grp, principles_grp,
                conn_s_sec, conn_s_fasb, conn_sec_p, conn_fasb_p,
            )),
            run_time=0.8,
        )

        # Store margin_rect for later sections
        self._margin_rect = margin_rect

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 3 — Financial Reporting Flow
    # ─────────────────────────────────────────────────────────────────────
    def section_3(self, circles):
        margin_rect = self._margin_rect

        # Title box
        title_box = RoundedRectangle(
            width=4.5, height=0.7, corner_radius=0.1,
            fill_color=DARK_NAVY, fill_opacity=1, stroke_width=0,
        )
        title_box.move_to([1.3, 3.4, 0])
        title_lbl = Text("Financial Reporting", font_size=24,
                         color=WHITE, weight=BOLD)
        title_lbl.move_to(title_box)
        title_grp = VGroup(title_box, title_lbl)

        # Bracket
        bracket = VMobject(stroke_color=DARK_NAVY, stroke_width=2)
        bracket.set_points_as_corners([
            [-1.2, 2.5, 0], [-1.2, 2.8, 0],
            [ 3.8, 2.8, 0], [ 3.8, 2.5, 0],
        ])

        self.play(
            FadeIn(title_grp, run_time=0.8),
            Create(bracket,   run_time=0.8),
        )

        # Doc icons stack
        doc1 = make_asset1(sheet_color="#F5F5F5").scale(0.8).move_to([1.3, 1.7, 0])
        doc2 = make_asset1(sheet_color="#F5F5F5").scale(0.8).move_to([1.4, 1.78, 0])
        doc3 = make_asset1(sheet_color="#F5F5F5").scale(0.8).move_to([1.5, 1.86, 0])
        doc_icons = VGroup(doc1, doc2, doc3).set_z_index(1)
        self.play(LaggedStart(
            FadeIn(doc1), FadeIn(doc2), FadeIn(doc3),
            lag_ratio=0.1, run_time=0.6,
        ))

        doc_center = doc_icons.get_center()
        int_pos = np.array([-1.5, -0.6, 0])
        ext_pos = np.array([ 4.1, -0.6, 0])

        # Arrows
        arrow_left  = Line(doc_center, int_pos, stroke_color=PRIMARY_BLUE, stroke_width=2)
        arrow_right = Line(doc_center, ext_pos, stroke_color=PRIMARY_BLUE, stroke_width=2)
        self.play(
            Create(arrow_left,  run_time=0.6),
            Create(arrow_right, run_time=0.6),
        )

        # Stakeholder groups
        int_icon = make_people_icon(scale=1.35)
        int_lbl  = Text("Internal Stakeholders", font_size=28,
                        color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
        int_lbl.next_to(int_icon, DOWN, buff=0.2)
        int_grp  = VGroup(int_icon, int_lbl).move_to(int_pos)

        ext_icon = make_investor_icon(scale=0.7)
        ext_lbl  = Text("External Stakeholders", font_size=28,
                        color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
        ext_lbl.next_to(ext_icon, DOWN, buff=0.2)
        ext_grp  = VGroup(ext_icon, ext_lbl).move_to(ext_pos)

        self.play(
            FadeIn(int_grp, run_time=0.8),
            FadeIn(ext_grp, run_time=0.8),
        )

        # Gear (continuous rotation via updater)
        gear_bg  = Circle(radius=0.4, fill_color=LIGHT_BLUE_FILL,
                          fill_opacity=1, stroke_width=0)
        gear_hub = Circle(radius=0.2, stroke_color=PRIMARY_BLUE,
                          stroke_width=2, fill_opacity=0)
        gear_shape = make_gear()
        gear_grp = VGroup(gear_bg, gear_shape, gear_hub)
        gear_grp.move_to([1.3, -0.6, 0])
        self.play(FadeIn(gear_grp, run_time=0.6))
        gear_shape.add_updater(lambda m, dt: m.rotate(dt * 0.5 * PI))

        # Chart icons
        bar_icon = make_barchart_icon(scale=0.4)
        bar_icon.scale(1.0).next_to(int_grp, DOWN, buff=0.2)
        pie_icon = make_piechart_icon(scale=0.4)
        pie_icon.next_to(ext_grp, DOWN, buff=0.2)
        self.play(FadeIn(bar_icon, run_time=0.6), FadeIn(pie_icon, run_time=0.6))

        # Flow circle updater
        flow_circle = Dot(color=ORANGE_ACCENT, radius=0.12).set_z_index(2)
        flow_circle.move_to(doc_center)
        self.add(flow_circle)
        elapsed = [0.0]

        def flow_updater(m, dt):
            elapsed[0] += dt
            t = (elapsed[0] % 2.0) / 2.0
            if t < 0.5:
                m.move_to(interpolate(doc_center, int_pos, t * 2))
            else:
                m.move_to(interpolate(doc_center, ext_pos, (t - 0.5) * 2))

        flow_circle.add_updater(flow_updater)
        self.wait(9.92)

        # Clean-up
        gear_shape.clear_updaters()
        flow_circle.clear_updaters()
        self.play(
            FadeOut(VGroup(
                int_grp, ext_grp, arrow_left, arrow_right,
                bar_icon, pie_icon, doc_icons,
                title_grp, bracket, flow_circle, gear_grp,
            )),
            run_time=0.8,
        )

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 4 — Investor & Company — Coin Flow
    # ─────────────────────────────────────────────────────────────────────
    def section_4(self, circles):
        investor1 = make_investor_icon(scale=1.2)
        investor1.move_to([-2.5, -0.5, 0])

        building_main = make_building_icon(scale=1.2)
        building_main.scale(3.2 / 3.6).move_to([0.5, -0.5, 0])

        self.play(
            FadeIn(investor1,    run_time=0.8),
            FadeIn(building_main, run_time=0.8),
        )

        # Insight texts (letter-by-letter)
        texts_info = [
            ("Profitable",   [4.7,  1.0, 0]),
            ("Stable",       [4.7,  0.0, 0]),
            ("Trustworthy",  [4.7, -1.0, 0]),
        ]
        text_mobs = []
        for content, pos in texts_info:
            t = Text(content, font_size=54, color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
            t.move_to(pos)
            text_mobs.append(t)

        # Coin flow (12 coins)
        inv_center  = investor1.get_center()
        bldg_center = building_main.get_center()

        coin_anims = []
        for i in range(12):
            coin = make_coin()
            coin.move_to(inv_center).set_z_index(4)
            coin_anims.append(Succession(
                Wait(i * 0.3),
                FadeIn(coin, run_time=0.05),
                coin.animate(run_time=1.2).move_to(bldg_center),
                FadeOut(coin, run_time=0.1),
            ))

        text_anims = [
            LaggedStart(*[
                FadeIn(char, shift=UP * 0.15)
                for char in AddTextLetterByLetter(t)
            ], lag_ratio=0.08, run_time=1.0)
            if False else FadeIn(t, shift=UP * 0.15, run_time=1.0)
            for t in text_mobs
        ]

        # Play coins and insight texts simultaneously
        self.play(
            LaggedStart(*coin_anims, lag_ratio=0),
            Succession(*[FadeIn(t, shift=UP * 0.15, run_time=1.0)
                         for t in text_mobs]),
        )

        self.play(FadeOut(VGroup(*text_mobs), run_time=0.4))
        self.play(FadeOut(building_main, run_time=0.6))

        # Reposition investor for Section 5
        self.play(investor1.animate.move_to([-1.0, -0.5, 0]), run_time=0.8)
        self._investor1 = investor1

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 5 — Three Companies → Investor
    # ─────────────────────────────────────────────────────────────────────
    def section_5(self, circles):
        investor1 = self._investor1
        self.play(investor1.animate.shift(LEFT * 0.6), run_time=0.6)
        # investor at x = -1.6

        b1 = make_building_icon(scale=0.9).move_to([ 2.8,  1.8, 0])
        b2 = make_building_icon(scale=0.9).move_to([ 2.8,  0.0, 0])
        b3 = make_building_icon(scale=0.9).move_to([ 2.8, -1.8, 0])
        buildings = VGroup(b1, b2, b3)

        self.play(FadeIn(buildings, run_time=0.5))

        inv_center = investor1.get_center()
        colors_per_stream = ["#FF6B6B", "#4ECDC4", "#FFE66D"]
        offsets = [0.8, 1.1, 1.4]
        sources = [b.get_center() for b in [b1, b2, b3]]

        tile_anims = []
        for src, col, offset in zip(sources, colors_per_stream, offsets):
            for j in range(6):
                tile = make_asset1(sheet_w=0.5, sheet_h=0.4,
                                   sheet_color="#F5F5F5").scale(0.5).set_z_index(1)
                tile.move_to(src)
                tile_anims.append(Succession(
                    Wait(offset + j * 0.25),
                    tile.animate(run_time=0.8).move_to(inv_center),
                    FadeOut(tile, run_time=0.1),
                ))

        self.play(LaggedStart(*tile_anims, lag_ratio=0))

        # Coin flip: investor1 → investor2 (darker tint)
        self.play(Rotate(investor1, angle=PI/2, axis=UP, run_time=0.25,
                         rate_func=rate_functions.ease_in_sine))
        investor2 = make_investor_icon(color=DARK_NAVY, scale=1.2)
        investor2.move_to(investor1.get_center())
        investor2.rotate(PI/2, axis=UP)
        self.remove(investor1)
        self.add(investor2)
        self.play(Rotate(investor2, angle=-PI/2, axis=UP, run_time=0.35,
                         rate_func=rate_functions.ease_out_back))

        # Clean-up
        self.play(FadeOut(VGroup(investor2, b1, b2, b3), run_time=0.8))
        self.wait(5.2)

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 7 — GAAP Full Expansion — Letter Columns
    # ─────────────────────────────────────────────────────────────────────
    def section_7(self, circles):
        margin_rect = self._margin_rect
        circle_G, circle_A1, circle_A2, circle_P = circles

        header_positions = [
            [-4.8, 2.5, 0],
            [-1.6, 2.5, 0],
            [ 1.6, 2.5, 0],
            [ 4.8, 2.5, 0],
        ]

        # Scale circles up (they are currently 0.5x; scale(2) restores full size)
        self.play(
            *[circ.animate.scale(2.0).move_to(pos)
              for circ, pos in zip(circles, header_positions)],
            margin_rect.animate.move_to([-8.0, 0, 0]),
            run_time=1.2,
        )

        # Column boxes
        box_configs = [
            ("GENERALLY",  LIGHT_BLUE_COL,   -4.8, make_shield_icon),
            ("ACCEPTED",   LIGHT_YELLOW_COL, -1.6, make_thumbsup_icon),
            ("ACCOUNTING", LIGHT_RED_COL,     1.6, make_calculator_icon),
            ("PRINCIPLES", LIGHT_GREEN_COL,   4.8, make_chess_knight_icon),
        ]

        box_h = 4.8
        box_y_center = 0.1   # = header_y(2.5) - box_h/2
        detail_boxes = VGroup()

        for label, fill_col, cx, icon_fn in box_configs:
            box = RoundedRectangle(
                width=2.8, height=box_h, corner_radius=0.1,
                fill_color=fill_col, fill_opacity=1,
                stroke_color=PRIMARY_BLUE, stroke_width=2,
            )
            box.move_to([cx, box_y_center, 0])

            lbl = Text(label, font_size=36, color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
            lbl.move_to([cx, box_y_center + 1.2, 0])

            icon = icon_fn(scale=2.0)
            icon.move_to([cx, box_y_center - 0.8, 0])

            detail_boxes.add(VGroup(box, lbl, icon))

        self.play(FadeIn(detail_boxes, run_time=1.0))
        self.wait(9.1)

        # Scale + shift up to make room for Section 8 outcome boxes
        full_gaap_grp = VGroup(*circles, detail_boxes)
        self.play(full_gaap_grp.animate.scale(0.8).shift(UP * 0.5), run_time=1.0)

        self._full_gaap_grp = full_gaap_grp

    # ─────────────────────────────────────────────────────────────────────
    # SECTION 8 — Outcomes: Uniformity, Clarity, Comparability
    # ─────────────────────────────────────────────────────────────────────
    def section_8(self, circles):
        full_gaap_grp = self._full_gaap_grp

        # Three outcome boxes
        outcome_labels = ["Uniformity", "Clarity", "Comparability"]
        outcome_x      = [-2.8, 0.0, 2.8]
        outcome_icons_fn = [make_ruler_icon, make_magnify_icon, make_comparison_barchart_icon]

        boxes  = VGroup()
        texts  = VGroup()
        icons  = VGroup()

        for label, cx, icon_fn in zip(outcome_labels, outcome_x, outcome_icons_fn):
            box = RoundedRectangle(
                width=2.5, height=0.7, corner_radius=0.2,
                fill_color=LIGHT_BLUE_FILL, fill_opacity=1, stroke_width=0,
            )
            box.move_to([cx, -3.2, 0])
            boxes.add(box)

            txt = Text(label, font_size=36, color=PRIMARY_BLUE, weight=BOLD).scale(0.5)
            txt.move_to([cx, -3.3, 0])
            texts.add(txt)

            icon = icon_fn(scale=0.8)
            icon.next_to(box, UP, buff=0.15)
            icons.add(icon)

        self.play(
            FadeIn(boxes, run_time=0.736),
            FadeIn(texts, run_time=0.736),
            FadeIn(icons, run_time=0.736),
        )
        self.wait(5.71)
