"""Section 1.2 — States.   Draft.

Build from the video folder with the Manim environment:
    python pipeline/build.py 1.2 preview --scene a

Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))

from common import *  # noqa: E402,F401

LEFT_X, RIGHT_X = -3.2, 3.2
VEC_Y, BAR_BASE = 1.9, -2.0
ROOT = r"\tfrac{1}{\sqrt2}"
C0 = np.array([0.6, 0.75, 0.0])     # origin of the plane of states
U = 2.1                              # length of a state arrow on screen
BX, BBASE = 5.3, -0.9                # the probability bars beside the plane
RX = 4.9                             # centre of the column of formulas on the right
DIAL_Y, DIAL_R = 1.0, 1.15           # the discs for complex amplitudes
DROP = 0.4                           # how far the picture sits below where it was drawn (centres it)


class Main(NarratedScene):
    EP = "1.2"

    SCENES = [("i", "opening"), ("a", "hook"), ("b", "arrow"), ("c", "minus_sign"), ("d", "overlap"), ("e", "other_axes"),
              ("f", "complex_entries"), ("g", "closing")]

    def construct(self):
        only = os.environ.get("ONLY", "")
        self.head = header("1.2  States")
        self.wm = watermark()
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter != "i" and self.head not in self.mobjects:     # nothing over the opening card
                # Subtitles are no longer part of the picture, so the strip kept free for them at the
                # bottom is gone: the camera looks `DROP` higher, which moves the whole picture
                # down to the middle of the frame. Header and watermark stay on top.
                self.camera.frame_center = np.array([0.0, DROP, 0.0])
                self.head.shift(UP * DROP)
                self.wm.shift(UP * DROP)
                self.play(FadeIn(self.head), FadeIn(self.wm), run_time=0.4)
            getattr(self, name)()
        self.save_marks()

    def opening(self):
        """Who is speaking, then what this section is about: the same card as section 1.1."""
        centre = [0, 1.35, 0]
        lab = T("QAICON Lab", size=54, bold=True).move_to([0, -0.85, 0])
        full = T("Quantum and AI for Computing, Optimization, and Networking", size=26, color=HILITE)
        full.next_to(lab, DOWN, buff=0.3)
        where = T("Western University", size=24, color=MUTED).next_to(full, DOWN, buff=0.25)
        with self.voice("i1"):
            mark = logo_reveal(self, centre)          # blurred "AI", the Q as a lens, the logo
            self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.6)
            self.hold(0.3)
            self.play(FadeIn(full, shift=UP * 0.15), run_time=0.7)
            self.hold(1.2)
            self.play(FadeIn(where), run_time=0.5)

        series = T("Quantum Computing Workshop", size=28, color=MUTED).move_to([0, 1.2, 0])
        title = T("States", size=58, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 1  ·  Section 1.2", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    def hook(self):
        """Two columns of amplitudes with the same bars: are they the same state?"""
        plus = colvec(ROOT, ROOT, size=54).move_to([LEFT_X, VEC_Y, 0])
        minus = colvec(ROOT, "-" + ROOT, size=54).move_to([RIGHT_X, VEC_Y, 0])
        sign = minus.bottom[0][0]            # the minus sign: orange for the whole lecture
        sign.set_color(ACCENT)

        with self.voice("a1"):
            self.play(Write(plus), run_time=0.9)
            self.play(Write(minus), run_time=0.9)

        # a2: each entry is squared into the height of its bar
        charts = [bars(0.5, 0.5, x=x, base=BAR_BASE, full=2.2, values=(r"\tfrac12", r"\tfrac12"))
                  for x in (LEFT_X, RIGHT_X)]
        with self.voice("a2"):
            for vec, ch in zip((plus, minus), charts):
                frame_parts = VGroup(*[m for m in ch if m not in (ch.b0, ch.b1, ch.v0, ch.v1)])
                self.play(FadeIn(frame_parts), run_time=0.3)
                self.play(TransformFromCopy(vec.top, ch.v0), GrowFromEdge(ch.b0, DOWN),
                          TransformFromCopy(vec.bottom, ch.v1), GrowFromEdge(ch.b1, DOWN), run_time=0.9)

        # a3, a4: the two charts are the same
        same = M("=", size=96, color=HILITE).move_to([0, BAR_BASE + 1.1, 0])
        with self.voice("a3"):
            self.play(FadeIn(same, scale=0.6), run_time=0.5)
        with self.voice("a4"):
            # a pulse in size only: the bars keep their outcome colours
            self.play(VGroup(charts[0].b0, charts[0].b1, charts[1].b0, charts[1].b1)
                      .animate(rate_func=there_and_back).stretch(1.05, 1, about_edge=DOWN), run_time=1.0)

        # a5: the question, then a thinking pause during which nothing new appears
        ask = M("?", size=110, color=HILITE).move_to(same)
        with self.voice("a5"):
            self.play(Transform(same, ask), run_time=0.5)

        # a6: no. The only thing that differs is the sign
        differ = M(r"\neq", size=96, color=HILITE).move_to(same)   # orange stays with the minus sign
        with self.voice("a6"):
            self.play(Transform(same, differ), run_time=0.4)
            self.play(Indicate(sign, color=ACCENT, scale_factor=2.2), run_time=0.9)

        # a7: the bars go; the two columns stay and move aside to make room for a picture
        with self.voice("a7"):
            self.play(FadeOut(charts[0]), FadeOut(charts[1]), FadeOut(same), run_time=0.7)
            self.play(plus.animate.scale(0.7).move_to([-5.6, 1.7, 0]),
                      minus.animate.scale(0.7).move_to([-5.6, -0.6, 0]), run_time=1.0)
        self.keep = VGroup(plus, minus)
        self.sign = sign

    # ------------------------------------------------------------ the plane of states
    def pt(self, a, b):
        """The point of the picture with amplitude `a` along outcome 0 and `b` along outcome 1."""
        return C0 + U * np.array([a, b, 0.0])

    def arrow_to(self, a, b, color=HILITE, width=7, opacity=1.0):
        arr = Arrow(C0, self.pt(a, b), buff=0, color=color, stroke_width=width,
                    max_tip_length_to_length_ratio=0.13, max_stroke_width_to_length_ratio=30)
        return arr.set_opacity(opacity)

    def need_keep(self):
        """The two columns scene A leaves at the left edge (rebuilt when a draft skips scene A)."""
        if hasattr(self, "keep"):
            return
        plus = colvec(ROOT, ROOT, size=54).scale(0.7).move_to([-5.6, 1.7, 0])
        minus = colvec(ROOT, "-" + ROOT, size=54).scale(0.7).move_to([-5.6, -0.6, 0])
        self.sign = minus.bottom[0][0].set_color(ACCENT)
        self.keep = VGroup(plus, minus)
        self.add(self.keep)

    def make_axes(self):
        ax0 = Line(self.pt(-1.25, 0), self.pt(1.25, 0), color=LILAC, stroke_width=3)
        ax1 = Line(self.pt(0, -1.2), self.pt(0, 1.25), color=RING, stroke_width=3)
        l0 = T("0", size=24, color=LILAC).next_to(ax0.get_end(), RIGHT, buff=0.12)
        l1 = T("1", size=24, color=RING).next_to(ax1.get_end(), UP, buff=0.1)
        return VGroup(ax0, ax1, l0, l1)

    def need_plane(self):
        """Axes, unit circle, the turning state arrow and the two basis arrows, as scene B leaves them."""
        self.need_keep()
        if hasattr(self, "axes"):
            return
        self.axes = self.make_axes()
        self.circle = Circle(radius=U, color=MUTED, stroke_width=2).move_to(C0)
        self.th = ValueTracker(55 * DEGREES)
        self.live = self.live_arrow()
        self.e0 = self.arrow_to(1, 0, color=LILAC, width=5, opacity=0.45)
        self.e1 = self.arrow_to(0, 1, color=RING, width=5, opacity=0.45)
        self.k0 = M(r"|0\rangle", size=34, color=LILAC).next_to(self.pt(1, 0), DR, buff=0.1)
        self.k1 = M(r"|1\rangle", size=34, color=RING).next_to(self.pt(0, 1), UR, buff=0.1)
        self.chart_static, self.chart_live = self.linked_bars()
        self.add(self.axes, self.circle, self.e0, self.e1, self.k0, self.k1, self.live,
                 self.chart_static, self.chart_live)

    def live_arrow(self):
        return always_redraw(lambda: self.arrow_to(np.cos(self.th.get_value()), np.sin(self.th.get_value())))

    def linked_bars(self):
        """Probability bars that follow the state arrow: (the fixed parts, the two moving bars)."""
        g = bars(0.5, 0.5, x=BX, base=BBASE, full=2.2)
        fixed = VGroup(g[0], g[2], g[4])

        def two():
            t = self.th.get_value()
            h = bars(np.cos(t) ** 2, np.sin(t) ** 2, x=BX, base=BBASE, full=2.2, labels=False)
            return VGroup(h.b0, h.b1)
        return fixed, always_redraw(two)

    def turn(self, degrees, run_time=0.8):
        self.play(self.th.animate.set_value(degrees * DEGREES), run_time=run_time)

    def tip(self):
        t = self.th.get_value()
        return self.pt(np.cos(t), np.sin(t))


    def present(self, *mobs):
        """Those of `mobs` (groups are opened up) that are on screen now, so a fade never flashes
        something that had already gone."""
        out = []
        for m in mobs:
            if m is None:
                continue
            if m in self.mobjects:
                out.append(m)
            elif isinstance(m, VGroup):
                out += self.present(*m.submobjects)
        return out

    # ------------------------------------------------------------ B. a state is an arrow
    def arrow(self):
        self.need_keep()
        plus, minus = self.keep
        r = 1 / np.sqrt(2)
        self.axes = self.make_axes()
        ax0, ax1, l0, l1 = self.axes
        with self.voice("b1"):
            self.play(Create(ax0), FadeIn(l0), run_time=0.8)
            self.play(Create(ax1), FadeIn(l1), run_time=0.8)

        tx = M(ROOT, size=30, color=LILAC).next_to(self.pt(r, 0), DOWN, buff=0.15)
        ty = M(ROOT, size=30, color=RING).next_to(self.pt(0, r), LEFT, buff=0.15)
        drop = VGroup(DashedLine(self.pt(r, 0), self.pt(r, r), color=MUTED, stroke_width=2),
                      DashedLine(self.pt(0, r), self.pt(r, r), color=MUTED, stroke_width=2))
        state = self.arrow_to(r, r)
        with self.voice("b2"):
            self.play(Indicate(plus, color=HILITE, scale_factor=1.1), run_time=0.6)
            self.play(TransformFromCopy(plus.top, tx), TransformFromCopy(plus.bottom, ty), run_time=0.9)
            self.play(Create(drop), run_time=0.4)
            self.play(GrowArrow(state), run_time=0.7)

        # b3: the squares of the two entries, as areas
        sq0 = Square(side_length=U * r, color=LILAC, stroke_width=2, fill_color=LILAC, fill_opacity=0.35)
        sq0.move_to(self.pt(r / 2, -r / 2))
        sq1 = Square(side_length=U * r, color=RING, stroke_width=2, fill_color=RING, fill_opacity=0.12)
        sq1.move_to(self.pt(-r / 2, r / 2))
        h0 = M(r"\tfrac12", size=36).move_to(sq0)
        h1 = M(r"\tfrac12", size=36).move_to(sq1)
        total = M(r"\tfrac12", "+", r"\tfrac12", "=", "1", size=48).move_to([RX, 2.3, 0])
        with self.voice("b3"):
            self.play(FadeIn(sq0), FadeIn(sq1), ReplacementTransform(tx, h0), ReplacementTransform(ty, h1),
                      run_time=0.9)
            self.play(TransformFromCopy(h0, total[0]), TransformFromCopy(h1, total[2]), FadeIn(total[1]),
                      run_time=0.7)
            self.play(Write(total[3:]), run_time=0.5)

        # b4: so the arrow has length one, and its tip can only be on this circle
        self.circle = Circle(radius=U, color=MUTED, stroke_width=2).move_to(C0)
        one = M("1", size=40, color=HILITE).move_to(self.pt(r / 2 - 0.13, r / 2 + 0.13))
        with self.voice("b4"):
            self.play(FadeOut(sq0), FadeOut(sq1), FadeOut(h0), FadeOut(h1), FadeOut(drop), run_time=0.5)
            self.play(TransformFromCopy(total[4], one), run_time=0.6)
            self.play(Create(self.circle), run_time=1.0)

        # b5: every state is such an arrow; the bars follow it
        self.th = ValueTracker(PI / 4)
        self.live = self.live_arrow()
        self.chart_static, self.chart_live = self.linked_bars()
        with self.voice("b5"):
            self.play(FadeOut(one), FadeOut(total), FadeIn(self.chart_static), FadeIn(self.chart_live), run_time=0.5)
            self.remove(state)
            self.add(self.live)
            self.turn(112, 1.0)
            self.turn(18, 1.1)
            self.turn(60, 0.9)

        # b6: the name, after the thing
        psi = always_redraw(lambda: M(r"|\psi\rangle", size=38, color=HILITE)
                            .move_to(C0 + 1.17 * (self.tip() - C0)))
        with self.voice("b6"):
            self.play(FadeIn(psi), self.keep.animate.set_opacity(0.3), run_time=0.4)
            self.card("ket", "a column of amplitudes, drawn as an arrow and written with this bracket",
                      width=9.6, x=0.6)

        # b7: the two arrows along the axes
        self.e0 = self.arrow_to(1, 0, color=LILAC, width=5, opacity=0.45)
        self.e1 = self.arrow_to(0, 1, color=RING, width=5, opacity=0.45)
        self.k0 = M(r"|0\rangle", size=34, color=LILAC).next_to(self.pt(1, 0), DR, buff=0.1)
        self.k1 = M(r"|1\rangle", size=34, color=RING).next_to(self.pt(0, 1), UR, buff=0.1)
        with self.voice("b7"):
            self.uncard()
            self.play(FadeOut(psi), run_time=0.2)
            self.turn(0, 0.8)
            self.play(FadeIn(self.k0), FadeIn(self.e0), run_time=0.4)
            self.turn(90, 0.8)
            self.play(FadeIn(self.k1), FadeIn(self.e1), run_time=0.4)

        # b8: any other arrow is some of one plus some of the other
        a, b = np.cos(55 * DEGREES), np.sin(55 * DEGREES)
        seg0 = Line(C0, self.pt(a, 0), color=LILAC, stroke_width=8)
        seg1 = Line(self.pt(a, 0), self.pt(a, b), color=RING, stroke_width=8)
        mix = M(r"|\psi\rangle", "=", r"\alpha", r"|0\rangle", "+", r"\beta", r"|1\rangle", size=44)
        mix[0].set_color(HILITE)
        mix[3].set_color(LILAC)
        fit(mix, 3.3).move_to([5.2, 2.45, 0])
        with self.voice("b8"):
            self.turn(55, 0.8)
            self.play(Create(seg0), run_time=0.5)
            self.play(Create(seg1), run_time=0.5)
            self.play(Write(mix), run_time=0.9)
        with self.voice("b9"):
            self.card("superposition", "a state with some of ket zero and some of ket one", width=7.4, x=0.6)

        # b10: the popular reading, drawn as two ghost arrows; then a thinking pause
        ghosts = VGroup(self.arrow_to(1, 0, opacity=0.55), self.arrow_to(0, 1, opacity=0.55))
        with self.voice("b10"):
            self.uncard()
            self.play(FadeIn(ghosts), run_time=0.6)
        # b11: there is one arrow
        with self.voice("b11"):
            self.play(FadeOut(ghosts), FadeOut(seg0), FadeOut(seg1), self.keep.animate.set_opacity(1),
                      run_time=0.6)
            self.play(Flash(self.tip(), color=HILITE, flash_radius=0.45), run_time=0.8)
        self.mix = mix

    # ------------------------------------------------------------ C. the minus sign is a direction
    def minus_sign(self):
        self.need_plane()
        plus, minus = self.keep
        r = 1 / np.sqrt(2)
        with self.voice("c1"):
            if hasattr(self, "mix"):
                self.play(FadeOut(self.mix), run_time=0.3)
            self.play(Indicate(plus, color=HILITE, scale_factor=1.12), run_time=0.7)
            self.turn(45, 0.8)
        self.a_plus = self.arrow_to(r, r)
        self.lab_plus = M(r"|+\rangle", size=38, color=HILITE).next_to(self.pt(r, r), UR, buff=0.08)
        with self.voice("c2"):
            self.add(self.a_plus)
            self.remove(self.live)
            self.play(FadeIn(self.lab_plus), run_time=0.4)
        # c3: where does the one with the minus sign point? Nothing new until the pause is over
        with self.voice("c3"):
            self.play(Indicate(minus, color=HILITE, scale_factor=1.12), run_time=0.7)
            self.play(Indicate(self.sign, color=ACCENT, scale_factor=2.2), run_time=0.8)
        self.a_minus = self.arrow_to(r, -r)
        down = Line(self.pt(r, 0), self.pt(r, -r), color=ACCENT, stroke_width=5)
        along = Line(C0, self.pt(r, 0), color=LILAC, stroke_width=8)
        with self.voice("c4"):
            self.play(Create(along), run_time=0.5)
            self.play(Create(down), run_time=0.5)
            self.play(GrowArrow(self.a_minus), run_time=0.7)
        self.lab_minus = M("|", "-", r"\rangle", size=38, color=HILITE).next_to(self.pt(r, -r), DR, buff=0.08)
        self.lab_minus[1].set_color(ACCENT)
        with self.voice("c5"):
            self.play(FadeIn(self.lab_minus), FadeOut(along), FadeOut(down), run_time=0.5)
        # c6: the bars are the same for both
        box = SurroundingRectangle(VGroup(self.chart_static, self.chart_live), color=HILITE, buff=0.2,
                                   stroke_width=2.5, corner_radius=0.1)
        with self.voice("c6"):
            self.play(Create(box), run_time=0.5)
            for arr in (self.a_plus, self.a_minus, self.a_plus, self.a_minus):
                self.play(Indicate(arr, color=HILITE, scale_factor=1.08), run_time=0.45)
            self.play(FadeOut(box), run_time=0.3)
        # c7: and yet the arrows are at a right angle
        self.corner = RightAngle(Line(C0, self.pt(r, r)), Line(C0, self.pt(r, -r)), length=0.38,
                                 color=INK, stroke_width=3)
        with self.voice("c7"):
            self.play(Create(self.corner), run_time=0.6)
        with self.voice("c8"):
            self.play(self.corner.animate.set_color(HILITE).set_stroke(width=6), run_time=0.5)
        # c9: where random bits live, and where ket minus is
        seg = Line(self.pt(1, 0), self.pt(0, 1), color=INK, stroke_width=7)
        seg_l = T("random bits", size=22, color=INK).move_to(self.pt(1.5, 0.52))
        ptr = Line(seg_l.get_left() + LEFT * 0.08, self.pt(0.8, 0.2), color=MUTED, stroke_width=2)
        with self.voice("c9"):
            self.play(Create(seg), FadeIn(seg_l), Create(ptr), run_time=0.9)
            self.hold(1.2)
            self.play(Flash(self.pt(r, -r), color=ACCENT, flash_radius=0.45), run_time=0.8)
        self.c_extra = VGroup(seg, seg_l, ptr)

    # ------------------------------------------------------------ D. overlap
    def overlap(self):
        self.need_plane()
        r = 1 / np.sqrt(2)
        if not hasattr(self, "a_plus"):          # a draft that starts here
            self.remove(self.live)
            self.a_plus, self.a_minus = self.arrow_to(r, r), self.arrow_to(r, -r)
            self.lab_plus = M(r"|+\rangle", size=38, color=HILITE).next_to(self.pt(r, r), UR, buff=0.08)
            self.lab_minus = M("|", "-", r"\rangle", size=38, color=HILITE).next_to(self.pt(r, -r), DR, buff=0.08)
            self.lab_minus[1].set_color(ACCENT)
            self.corner = RightAngle(Line(C0, self.pt(r, r)), Line(C0, self.pt(r, -r)), length=0.38,
                                     color=HILITE, stroke_width=6)
            self.c_extra = VGroup()
            self.add(self.a_plus, self.a_minus, self.lab_plus, self.lab_minus, self.corner)
        ask = M("?", size=64, color=HILITE).move_to(self.pt(0.42, 0))
        with self.voice("d1"):
            self.play(*[FadeOut(m) for m in self.present(self.c_extra, self.chart_static, self.chart_live)],
                      run_time=0.5)
            self.play(ReplacementTransform(self.corner, ask), run_time=0.5)

        # d2: the shadow of a turning arrow on the direction of ket plus
        def shadow():
            t = self.th.get_value()
            c = np.cos(t - PI / 4)
            foot = self.pt(c * r, c * r)
            parts = VGroup()
            if abs(c) > 0.02:
                parts.add(Line(C0, foot, color=INK, stroke_width=11))
            if np.linalg.norm(self.tip() - foot) > 0.08:
                parts.add(DashedLine(self.tip(), foot, color=MUTED, stroke_width=2.5))
            return parts
        self.th.set_value(-45 * DEGREES)
        self.live = self.live_arrow()
        shade = always_redraw(shadow)
        guide = Line(self.pt(-0.95 * r, -0.95 * r), self.pt(1.25 * r, 1.25 * r), color=MUTED, stroke_width=1.5)
        with self.voice("d2"):
            self.play(FadeOut(ask), FadeOut(self.lab_minus), self.a_plus.animate.set_opacity(0.4),
                      FadeIn(guide), run_time=0.5)
            self.add(self.live, shade)
            self.remove(self.a_minus)
            self.turn(45, 1.0)
            self.turn(100, 0.9)
            self.turn(15, 0.9)

        rule = M(r"\begin{pmatrix}a\\b\end{pmatrix}", r"\cdot", r"\begin{pmatrix}c\\d\end{pmatrix}", "=",
                 "ac", "+", "bd", size=44)
        fit(rule, 3.2).move_to([5.3, 2.45, 0])
        with self.voice("d3"):
            self.play(Write(rule[:3]), run_time=0.9)
            self.play(Write(rule[3:]), run_time=0.9)
        calc = M(r"\tfrac{1}{\sqrt2}\cdot\tfrac{1}{\sqrt2}", "+", r"\tfrac{1}{\sqrt2}\cdot\big(", "-",
                 r"\tfrac{1}{\sqrt2}\big)", size=40)
        fit(calc, 3.2).move_to([5.3, 1.3, 0])       # clear of the axis label at the edge of the circle
        calc[3].set_color(ACCENT)
        with self.voice("d4"):
            self.play(Write(calc), run_time=1.2)
        res = M("=", r"\tfrac12", "-", r"\tfrac12", "=", "0", size=46).move_to([5.2, 0.1, 0])
        res[2].set_color(ACCENT)
        with self.voice("d5"):
            self.play(Write(res[:4]), run_time=0.7)
            self.play(Write(res[4:]), run_time=0.4)
            self.turn(-45, 1.0)
        self.corner = RightAngle(Line(C0, self.pt(r, r)), Line(C0, self.pt(r, -r)), length=0.38,
                                 color=HILITE, stroke_width=6)
        with self.voice("d6"):
            self.play(Create(self.corner), FadeIn(self.lab_minus), self.a_plus.animate.set_opacity(1),
                      run_time=0.6)
            self.card("orthogonal", "two states with zero overlap: arrows at a right angle")
        braket = M(r"\langle +|", r"-\rangle", "=", "0", size=58).move_to([5.2, -1.2, 0])
        with self.voice("d7"):
            self.uncard()
            self.play(Write(braket), run_time=0.8)
            self.play(Indicate(braket[0], color=HILITE), run_time=0.7)
            self.play(Indicate(braket[1], color=HILITE), run_time=0.7)
        selfo = M(r"\langle\psi|\psi\rangle", "=", "1", size=58).move_to([5.2, 1.5, 0])
        with self.voice("d8"):
            self.play(FadeOut(rule), FadeOut(calc), FadeOut(res), run_time=0.4)
            self.play(Write(selfo), run_time=0.8)
            self.play(Flash(self.tip(), color=HILITE, flash_radius=0.45), run_time=0.7)
        self.d_extra = VGroup(braket, selfo, guide, shade, self.corner)

    # ------------------------------------------------------------ E. another pair of axes
    def other_axes(self):
        self.need_plane()
        r = 1 / np.sqrt(2)
        gone = self.present(getattr(self, "d_extra", None), getattr(self, "lab_plus", None),
                            getattr(self, "lab_minus", None), getattr(self, "a_plus", None),
                            getattr(self, "a_minus", None), self.live, self.k0, self.k1,
                            self.axes[2], self.axes[3], self.chart_static, self.chart_live)
        # everything below is fixed geometry, so the whole picture can be turned as one piece
        old_axes = VGroup(self.axes[0], self.axes[1])
        new_p = Line(self.pt(-1.2 * r, -1.2 * r), self.pt(1.25 * r, 1.25 * r), color=HILITE, stroke_width=3)
        new_m = Line(self.pt(-1.2 * r, 1.2 * r), self.pt(1.25 * r, -1.25 * r), color=HILITE, stroke_width=3)
        ap, am = self.arrow_to(r, r), self.arrow_to(r, -r)
        psi_deg = 20
        psi = self.arrow_to(np.cos(psi_deg * DEGREES), np.sin(psi_deg * DEGREES), color=INK)
        with self.voice("e1"):
            self.play(*[FadeOut(m) for m in gone], FadeIn(ap), FadeIn(am), run_time=0.6)
            self.play(Create(new_p), Create(new_m), old_axes.animate.set_opacity(0.3),
                      self.e0.animate.set_opacity(0.3), self.e1.animate.set_opacity(0.3), run_time=0.9)
            self.play(GrowArrow(psi), run_time=0.6)
        picture = VGroup(old_axes, self.circle, self.e0, self.e1, new_p, new_m, ap, am, psi)
        lp = M(r"|+\rangle", size=36, color=HILITE).next_to(self.pt(0, 1.25 * 1.0), UP, buff=0.1)
        lm = M("|", "-", r"\rangle", size=36, color=HILITE).next_to(self.pt(1.25, 0), RIGHT, buff=0.1)
        lm[1].set_color(ACCENT)
        with self.voice("e2"):
            self.play(Rotate(picture, PI / 4, about_point=C0), run_time=1.6)
            self.play(FadeIn(lp), FadeIn(lm), ap.animate.set_opacity(0.35), am.animate.set_opacity(0.35),
                      run_time=0.5)
        # e3: the same arrow, read off against the new axes
        t = (psi_deg + 45) * DEGREES
        px = Line(C0, self.pt(np.cos(t), 0), color=HILITE, stroke_width=8)
        py = Line(self.pt(np.cos(t), 0), self.pt(np.cos(t), np.sin(t)), color=HILITE, stroke_width=8)
        cx = M(r"\langle -|\psi\rangle", size=32).next_to(px, DOWN, buff=0.12)
        cy = M(r"\langle +|\psi\rangle", size=32).next_to(py, RIGHT, buff=0.12)
        with self.voice("e3"):
            self.play(Indicate(psi, color=INK, scale_factor=1.06), run_time=0.7)
            self.play(Create(px), FadeIn(cx), run_time=0.7)
            self.play(Create(py), FadeIn(cy), run_time=0.7)
        # e4: a question for the viewer, two empty boxes, and a thinking pause
        k0n = M(r"|0\rangle", size=36, color=LILAC).next_to(self.pt(r, r), UR, buff=0.1)
        rows = VGroup(M(r"\langle -|0\rangle", "=", size=46), M(r"\langle +|0\rangle", "=", size=46))
        rows.arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([RX - 0.3, 2.1, 0])
        boxes = VGroup(*[RoundedRectangle(width=1.1, height=1.0, corner_radius=0.1, color=HILITE, stroke_width=2.5)
                         .next_to(row, RIGHT, buff=0.25) for row in rows])
        with self.voice("e4"):
            self.play(FadeOut(px), FadeOut(py), FadeOut(cx), FadeOut(cy), run_time=0.4)
            self.play(Rotate(psi, (45 - psi_deg - 45) * DEGREES, about_point=C0), run_time=0.8)
            self.play(psi.animate.set_color(LILAC), FadeIn(k0n), run_time=0.4)
            self.play(Write(rows), Create(boxes), run_time=0.9)
        fills = VGroup(*[M(ROOT, size=40).move_to(b) for b in boxes])
        with self.voice("e5"):
            self.play(Write(fills[0]), run_time=0.6)
            self.play(Write(fills[1]), run_time=0.6)
        # e6: the squares still add to one, in these axes and in the old ones
        sq0 = Square(side_length=U * r, color=HILITE, stroke_width=2, fill_color=HILITE, fill_opacity=0.25)
        sq0.move_to(self.pt(r / 2, -r / 2))
        sq1 = sq0.copy().move_to(self.pt(-r / 2, r / 2))
        total = M(r"\tfrac12", "+", r"\tfrac12", "=", "1", size=46).move_to([RX, -0.9, 0])
        back = M("1", "+", "0", "=", "1", size=46).move_to([RX, -0.9, 0])
        with self.voice("e6"):
            self.play(FadeIn(sq0), FadeIn(sq1), run_time=0.6)
            self.play(Write(total), run_time=0.8)
            self.hold(0.6)
            self.play(FadeOut(sq0), FadeOut(sq1), FadeOut(lp), FadeOut(lm), FadeOut(k0n), run_time=0.4)
            self.play(Rotate(picture, -PI / 4, about_point=C0), run_time=1.3)
            self.play(ReplacementTransform(total, back), run_time=0.7)
        self.e_all = VGroup(picture, rows, boxes, fills, back)

    # ------------------------------------------------------------ F. complex amplitudes
    def dial(self, x, length, angle):
        """A small disc with a pointer: one complex amplitude. Returns (disc, pointer, length, angle)."""
        centre = np.array([x, DIAL_Y, 0.0])
        ring = Circle(radius=DIAL_R, color=MUTED, stroke_width=2).move_to(centre)
        cross = VGroup(Line(centre + LEFT * DIAL_R, centre + RIGHT * DIAL_R, color=DIM, stroke_width=2),
                       Line(centre + DOWN * DIAL_R, centre + UP * DIAL_R, color=DIM, stroke_width=2))
        ln, an = ValueTracker(length), ValueTracker(angle)

        def pointer():
            v = DIAL_R * ln.get_value() * np.array([np.cos(an.get_value()), np.sin(an.get_value()), 0.0])
            return Arrow(centre, centre + v, buff=0, color=HILITE, stroke_width=7,
                         max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=30)
        return VGroup(cross, ring), always_redraw(pointer), ln, an, centre

    def complex_entries(self):
        self.need_keep()
        everything = [m for m in self.mobjects if m is not self.head and m is not self.wm]
        col = colvec(r"\alpha", r"\beta", size=64).move_to([-4.3, DIAL_Y, 0])
        with self.voice("f1"):
            self.play(*[FadeOut(m) for m in everything], run_time=0.7)
            self.play(Write(col), run_time=0.9)
        d1, p1, len1, ang1, c1 = self.dial(-0.9, 0.8, 60 * DEGREES)
        d2, p2, len2, ang2, c2 = self.dial(2.2, 0.6, 140 * DEGREES)
        n1 = M(r"\alpha", size=40).next_to(d1, UP, buff=0.15)
        n2 = M(r"\beta", size=40).next_to(d2, UP, buff=0.15)
        with self.voice("f2"):
            self.play(FadeIn(d1), FadeIn(d2), TransformFromCopy(col.top, n1), TransformFromCopy(col.bottom, n2),
                      run_time=0.9)
            self.play(FadeIn(p1), FadeIn(p2), run_time=0.5)
        # f3: a size and a turn
        arc = Arc(radius=0.45, start_angle=0, angle=60 * DEGREES, arc_center=c1, color=INK, stroke_width=3)
        turn_l = T("turn", size=20).next_to(arc, RIGHT, buff=0.08).shift(UP * 0.12)
        size_l = T("size", size=20).move_to(c1 + DIAL_R * 0.55 * np.array([np.cos(105 * DEGREES),
                                                                           np.sin(105 * DEGREES), 0]) + UP * 0.25)
        with self.voice("f3"):
            self.play(FadeIn(size_l), run_time=0.5)
            self.play(Create(arc), FadeIn(turn_l), run_time=0.6)
        ex = M(r"|\psi\rangle", "=", r"\tfrac{1}{\sqrt3}", r"|0\rangle", "+", r"\tfrac{1+i}{\sqrt3}", r"|1\rangle",
               size=46).move_to([0.6, 3.15, 0])
        ex[0].set_color(HILITE)
        with self.voice("f4"):
            self.play(FadeOut(arc), FadeOut(turn_l), FadeOut(size_l), run_time=0.3)
            self.play(Write(ex), run_time=1.2)
        cap1 = M(r"\tfrac{1}{\sqrt3}", size=36).next_to(d1, DOWN, buff=0.2)
        cap2 = M(r"\sqrt{\tfrac23}", r",\ \ 45^\circ", size=36).next_to(d2, DOWN, buff=0.2)
        with self.voice("f5"):
            self.play(len1.animate.set_value(1 / np.sqrt(3)), ang1.animate.set_value(0), run_time=0.9)
            self.play(FadeIn(cap1), run_time=0.3)
            self.play(len2.animate.set_value(np.sqrt(2 / 3)), ang2.animate.set_value(45 * DEGREES), run_time=0.9)
            self.play(FadeIn(cap2), run_time=0.3)
        chart = bars(1 / 3, 2 / 3, x=5.4, base=DIAL_Y - DIAL_R, full=2.4, values=(r"\tfrac13", r"\tfrac23"))
        with self.voice("f6"):
            self.play(FadeIn(VGroup(chart[0], chart[2], chart[4])), run_time=0.3)
            self.play(GrowFromEdge(chart.b0, DOWN), FadeIn(chart.v0), run_time=0.6)
            self.play(GrowFromEdge(chart.b1, DOWN), FadeIn(chart.v1), run_time=0.6)
        # f7: a minus sign is a pointer turned halfway round
        neg = M("-", size=90, color=ACCENT).next_to(d2, RIGHT, buff=0.25).shift(UP * 0.6)
        with self.voice("f7"):
            self.play(FadeOut(cap2[1]), run_time=0.2)
            self.play(ang2.animate.set_value(180 * DEGREES), run_time=1.1)
            self.play(FadeIn(neg, scale=0.6), run_time=0.4)
        # f8: the bra turns each pointer the other way
        v = DIAL_R * np.sqrt(2 / 3) * np.array([np.cos(-45 * DEGREES), np.sin(-45 * DEGREES), 0.0])
        mirror = Arrow(c2, c2 + v, buff=0, color=INK, stroke_width=5, max_tip_length_to_length_ratio=0.2,
                       max_stroke_width_to_length_ratio=30).set_opacity(0.7)
        bra_l = T("in the bra", size=20).next_to(c2 + v, DR, buff=0.05)
        norm = M(r"\langle\psi|\psi\rangle", "=", r"|\alpha|^2", "+", r"|\beta|^2", "=", "1", size=46)
        norm.move_to([0.6, -2.0, 0])
        with self.voice("f8"):
            self.play(FadeOut(neg), ang2.animate.set_value(45 * DEGREES), run_time=0.8)
            self.play(GrowArrow(mirror), FadeIn(bra_l), run_time=0.7)
            self.play(Write(norm), run_time=1.2)

    # ------------------------------------------------------------ G. close
    def closing(self):
        r = 1 / np.sqrt(2)
        everything = [m for m in self.mobjects if m is not self.head and m is not self.wm]
        axes = self.make_axes()
        circle = Circle(radius=U, color=MUTED, stroke_width=2).move_to(C0)
        ap, am = self.arrow_to(r, r), self.arrow_to(r, -r)
        lp = M(r"|+\rangle", size=38, color=HILITE).next_to(self.pt(r, r), UR, buff=0.08)
        lm = M("|", "-", r"\rangle", size=38, color=HILITE).next_to(self.pt(r, -r), DR, buff=0.08)
        lm[1].set_color(ACCENT)
        chart = bars(0.5, 0.5, x=BX, base=BBASE, full=2.2, values=(r"\tfrac12", r"\tfrac12"))
        arrows = VGroup(ap, am, lp, lm)
        with self.voice("g1"):
            if everything:
                self.play(*[FadeOut(m) for m in everything], run_time=0.6)
            self.play(FadeIn(axes), FadeIn(circle), run_time=0.5)
            self.play(GrowArrow(ap), GrowArrow(am), FadeIn(lp), FadeIn(lm), run_time=0.8)
            self.play(FadeIn(chart), run_time=0.5)
        with self.voice("g2"):
            self.play(arrows.animate.set_opacity(0.3), run_time=0.6)
            self.play(VGroup(chart.b0, chart.b1).animate(rate_func=there_and_back)
                      .stretch(1.05, 1, about_edge=DOWN), run_time=0.9)
        ask = M("?", size=150, color=HILITE).move_to(self.pt(0.45, 0))
        with self.voice("g3"):
            self.play(arrows.animate.set_opacity(1), run_time=0.5)
            self.play(FadeIn(ask, scale=0.6), run_time=0.6)
        nxt = VGroup(T("Next", size=26, color=MUTED), T("1.3  Measurement", size=50, bold=True))
        nxt.arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        with self.voice("g4"):
            self.play(*[FadeOut(m) for m in (axes, circle, arrows, chart, ask)], run_time=0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
