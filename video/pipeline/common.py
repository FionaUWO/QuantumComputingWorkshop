"""Shared look and timing for the Quantum Computing Workshop videos (Manim CE).

Colours follow the website: dark purple ground, lilac for outcome 0, a white ring for
outcome 1 (the same dots as the site's simulator). Each colour means one thing: lilac is
never used for emphasis, cyan (HILITE) is. Orange is kept for minus signs and
cancellation only. The bottom strip of the frame (below y = -2.95) stays empty for the
burned-in subtitles.
"""
import json
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import load_script, out_dir  # noqa: E402

BG = "#24123F"        # site --purple-dark
PANEL = "#33205A"
INK = "#F4F0FA"
MUTED = "#A89BC4"
LILAC = "#B9A3DC"     # outcome 0, and nothing else
PURPLE = "#7B4FC0"
RING = "#FFFFFF"      # outcome 1
DIM = "#3E2C63"       # an empty dot
ACCENT = "#F28C28"    # minus signs and cancellation only
HILITE = "#7FD4E6"    # emphasis: "look here", key words, frames, the state arrow
GOOD = "#6FCF97"
FONT = "Segoe UI"

config.background_color = BG
config.max_files_cached = 2000
TPL = TexTemplate(preamble=r"\usepackage{amsmath}" + "\n" + r"\usepackage{amssymb}")


def T(s, size=28, color=INK, bold=False, **kw):
    return Text(s, font=FONT, font_size=size, color=color, weight=BOLD if bold else NORMAL, **kw)


def M(*parts, size=40, color=INK):
    return MathTex(*parts, tex_template=TPL, font_size=size, color=color)


def fit(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def pill(text, color=MUTED, size=20, fill=None):
    t = T(text, size=size, color=color)
    box = RoundedRectangle(width=t.width + 0.36, height=t.height + 0.24, corner_radius=0.14,
                           color=color, stroke_width=1.6, fill_color=fill or BG, fill_opacity=1)
    return VGroup(box, t.move_to(box))


def header(text):
    return T(text, size=22, color=MUTED).to_corner(UL, buff=0.3)


def def_card(term, definition, width=11.0):
    """A definition card for the lower third, just above the subtitle strip."""
    t = T(term, size=28, bold=True)
    d = fit(T(definition, size=22, color=INK), width - 0.7)
    body = VGroup(t, d).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    box = RoundedRectangle(width=width, height=body.height + 0.42, corner_radius=0.16, color=PURPLE,
                           stroke_width=2, fill_color=PANEL, fill_opacity=1)
    bar = Rectangle(width=0.1, height=body.height + 0.1, color=HILITE, fill_color=HILITE,
                    fill_opacity=1, stroke_width=0)
    body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.42)
    bar.next_to(body, LEFT, buff=0.14)
    card = VGroup(box, bar, body)
    card.move_to([0, -2.95 + card.height / 2 + 0.12, 0])
    return card


def colvec(a, b, size=44, color=INK):
    """A column vector with two entries (LaTeX strings). vec.top and vec.bottom are the entries."""
    v = Matrix([[a], [b]], left_bracket="(", right_bracket=")", v_buff=0.8 * size / 44,
               bracket_h_buff=0.14, element_to_mobject=lambda s: M(s, size=size, color=color))
    v.get_brackets().set_color(color)
    v.top, v.bottom = v.get_entries()
    return v


def bars(p0, p1, x=0.0, base=-0.6, full=2.0, w=0.6, labels=True, values=None):
    """Two bars for the probabilities of 0 and 1. `full` is the height of probability one.
    g.b0, g.b1 are the bars; g.v0, g.v1 the value labels (if `values` is given)."""
    g = VGroup()
    g.add(Line([x - w * 1.5, base, 0], [x + w * 1.5, base, 0], color=MUTED, stroke_width=2))
    cols = []
    for k, p in enumerate((p0, p1)):
        cx = x + (k - 0.5) * w * 1.35
        h = max(p * full, 0.02)
        b = Rectangle(width=w, height=h, stroke_width=2.2 if k else 0, color=RING if k else LILAC,
                      fill_color=BG if k else LILAC, fill_opacity=1)
        b.move_to([cx, base + h / 2, 0])
        cols.append(b)
        g.add(b)
        if labels:
            g.add(T(str(k), size=20, color=MUTED).move_to([cx, base - 0.25, 0]))
    g.b0, g.b1 = cols
    if values:
        g.v0 = M(values[0], size=30).next_to(cols[0], UP, buff=0.12)
        g.v1 = M(values[1], size=30).next_to(cols[1], UP, buff=0.12)
        g.add(g.v0, g.v1)
    return g


def mark(ok, size=0.16):
    """A tick or a cross, drawn rather than typed so it never depends on a font."""
    if ok:
        m = VMobject(color=GOOD, stroke_width=4)
        m.set_points_as_corners([[-size, 0, 0], [-size * 0.3, -size * 0.7, 0], [size, size * 0.8, 0]])
        return m
    return VGroup(Line([-size, -size, 0], [size, size, 0]), Line([-size, size, 0], [size, -size, 0])
                  ).set_color(MUTED).set_stroke(width=4)


def status(text, ok):
    """A small note under the puzzle badge: a label with a tick or a cross."""
    row = VGroup(T(text, size=20, color=INK), mark(ok)).arrange(RIGHT, buff=0.18)
    box = RoundedRectangle(width=row.width + 0.4, height=row.height + 0.26, corner_radius=0.14,
                           color=GOOD if ok else MUTED, stroke_width=1.6, fill_color=BG, fill_opacity=1)
    return VGroup(box, row.move_to(box))


class Grid2:
    """A 2 x 2 matrix drawn cell by cell, so its columns can be filled in one at a time."""

    def __init__(self, center, dx=1.3, dy=0.95, size=40, widest="0"):
        # `widest` is the widest entry the matrix will hold, so the brackets leave room for it
        self.dx, self.dy, self.size = dx, dy, size
        proto = Matrix([[widest, widest], [widest, widest]], left_bracket="(", right_bracket=")", h_buff=dx, v_buff=dy,
                       element_to_mobject=lambda s: M(s, size=size)).move_to(center)
        self.c = proto.get_center()
        self.frame = proto.get_brackets().set_color(INK)
        self.slots = [e.get_center() for e in proto.get_entries()]      # row by row
        self.cells = {}

    def pos(self, row, col):
        return self.slots[2 * row + col]

    def entry(self, row, col, tex, color=INK):
        m = M(tex, size=self.size, color=color).move_to(self.pos(row, col))
        self.cells[(row, col)] = m
        return m

    def column(self, col, a, b):
        return VGroup(self.entry(0, col, a), self.entry(1, col, b))

    def band(self, col):
        """A soft highlight behind one column."""
        return RoundedRectangle(width=self.dx * 0.78, height=self.dy * 2 + 0.1, corner_radius=0.12,
                                stroke_width=0, fill_color=PURPLE, fill_opacity=0.45
                                ).move_to([self.pos(0, col)[0], self.c[1], 0])

    def everything(self):
        return VGroup(self.frame, *self.cells.values())


# ---------------------------------------------------------------- 100 measured copies
def dot_grid(rows=5, cols=20, step=0.25, r=0.092):
    """An empty grid of dots, one per measured copy."""
    g = VGroup()
    for k in range(rows * cols):
        d = Circle(radius=r, stroke_width=0, fill_color=DIM, fill_opacity=1)
        d.move_to([(k % cols - (cols - 1) / 2) * step, ((rows - 1) / 2 - k // cols) * step, 0])
        g.add(d)
    return g


def dot_look(dot, outcome):
    """Restyle one dot in place: None = empty, 0 = lilac disc, 1 = white ring."""
    if outcome is None:
        dot.set_fill(DIM, opacity=1).set_stroke(width=0)
    elif outcome == 0:
        dot.set_fill(LILAC, opacity=1).set_stroke(width=0)
    else:
        dot.set_fill(BG, opacity=1).set_stroke(RING, width=2.2)
    return dot


def fill_dots(grid, outcomes, run_time=1.2):
    """Animation: the dots take their outcomes one after another, in order."""
    return LaggedStart(*[UpdateFromFunc(d, lambda m, o=o: dot_look(m, o), run_time=0.05)
                         for d, o in zip(grid, outcomes)], lag_ratio=1.0, run_time=run_time)


def clear_dots(grid):
    for d in grid:
        dot_look(d, None)


# ---------------------------------------------------------------- Bloch sphere (flat drawing)
YAW, PITCH = -0.55, 0.32      # the same view as the simulator on the website


def bloch_project(p, R=1.0):
    """Project a point of the unit sphere to the picture plane; third entry is depth (>= 0 is in front)."""
    x1 = p[0] * np.cos(YAW) - p[1] * np.sin(YAW)
    y1 = p[0] * np.sin(YAW) + p[1] * np.cos(YAW)
    return np.array([R * y1, R * (p[2] * np.cos(PITCH) - x1 * np.sin(PITCH)),
                     x1 * np.cos(PITCH) + p[2] * np.sin(PITCH)])


def rotate_about(v, axis, angle):
    """Rodrigues' formula: v turned by `angle` about the unit vector `axis`."""
    v, k = np.array(v, float), np.array(axis, float)
    return v * np.cos(angle) + np.cross(k, v) * np.sin(angle) + k * np.dot(k, v) * (1 - np.cos(angle))


class Bloch(VGroup):
    """A Bloch sphere drawn in the plane. `state` is the Bloch vector; `arrow()` gives a mobject
    that follows `self.t`, a ValueTracker running from 0 to 1 along the current move."""

    def __init__(self, R=1.5, center=ORIGIN):
        super().__init__()
        self.R, self.c = R, np.array(center, float)
        self.state = np.array([0.0, 0.0, 1.0])
        self.add(Circle(radius=R, color=INK, stroke_width=2.5).move_to(self.c))
        for f in (lambda a: [np.cos(a), np.sin(a), 0], lambda a: [np.cos(a), 0, np.sin(a)],
                  lambda a: [0, np.cos(a), np.sin(a)]):
            self.add(*self._circle(f))
        for v, lab in (([0, 0, 1], r"|0\rangle"), ([0, 0, -1], r"|1\rangle"),
                       ([1, 0, 0], r"|{+}\rangle"), ([-1, 0, 0], r"|{-}\rangle")):
            q = bloch_project(v, R)
            front = q[2] >= 0
            self.add(Line(self.c, self.c + [q[0], q[1], 0], color=INK, stroke_width=1.2,
                          stroke_opacity=0.45 if front else 0.2))
            q2 = bloch_project(np.array(v) * 1.24, R)
            self.add(M(lab, size=26, color=INK if front else MUTED).move_to(self.c + [q2[0], q2[1], 0]))

    def _circle(self, f):
        """One great circle: the front half solid, the back half dashed."""
        pts = [bloch_project(f(a), self.R) for a in np.linspace(0, TAU, 121)]
        out = []
        for front in (True, False):
            run = []
            for p in pts + [None]:
                if p is not None and (p[2] >= 0) == front:
                    run.append(self.c + [p[0], p[1], 0])
                    continue
                if len(run) > 1:
                    seg = VMobject(color=INK, stroke_width=1.3, stroke_opacity=0.5 if front else 0.22)
                    seg.set_points_as_corners(run)
                    out.append(seg if front else DashedVMobject(seg, num_dashes=max(4, len(run) // 3)))
                run = []
        return out

    def point(self, v):
        q = bloch_project(v, self.R)
        return self.c + [q[0], q[1], 0]

    def arrow(self, v=None):
        v = self.state if v is None else v
        tip = self.point(v)
        line = Line(self.c, tip, color=HILITE, stroke_width=5)
        return VGroup(line, Dot(tip, radius=0.09, color=HILITE))

    def path(self, axis, angle, t0=0.0, t1=1.0, n=40):
        """The curve the arrow tip traces while the state turns by `angle` about `axis`."""
        pts = [self.point(rotate_about(self.state, axis, angle * t)) for t in np.linspace(t0, t1, n)]
        m = VMobject(color=HILITE, stroke_width=3)
        m.set_points_as_corners(pts)
        return m


H_AXIS = np.array([1.0, 0.0, 1.0]) / np.sqrt(2)     # H is a half turn about this axis


# ---------------------------------------------------------------- narrated scene
class NarratedScene(MovingCameraScene):
    """A scene whose pacing follows the narration audio.

    `with self.voice("a1"):` marks where that line starts, and the block is padded so the
    picture never runs ahead of the voice. After the line the scene waits for the pause the
    script asks for (PAUSE_AFTER / DEFAULT_PAUSE). The start times are written to
    out/<lecture>/<section>/marks.json and are the timing marks for the voice-over.
    """
    EP = "1.1"

    def setup(self):
        super().setup()
        self.script = load_script(self.EP)
        self.subs = {i: sub for i, sub, _ in self.script.SEGS}
        p = out_dir(self.EP) / "durations.json"
        self.durs = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        self.marks = []
        self.head = None

    @property
    def now(self):
        return self.renderer.time

    def pause_after(self, seg_id):
        s = self.script
        return getattr(s, "PAUSE_AFTER", {}).get(seg_id, getattr(s, "DEFAULT_PAUSE", 0.35))

    @contextmanager
    def voice(self, *ids, gap=None):
        t0 = t = self.now
        for i in ids:
            d = self.durs.get(i, len(self.subs[i].split()) / 150 * 60)
            self.marks.append({"id": i, "start": round(t, 3), "dur": d})
            t += d + 0.25
        total = t - t0 - 0.25
        yield total
        left = t0 + total + (self.pause_after(ids[-1]) if gap is None else gap) - self.now
        if left > 0.04:
            self.wait(left)

    def hold(self, seconds):
        if seconds > 0.04:
            self.wait(seconds)

    def set_header(self, text):
        new = header(text)
        if self.head is None:
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeOut(self.head), FadeIn(new), run_time=0.4)
        self.head = new

    def card(self, term, definition):
        new = def_card(term, definition)
        old = getattr(self, "card_mob", None)
        if old is None:
            self.play(FadeIn(new, shift=UP * 0.2), run_time=0.5)
        else:
            self.play(FadeOut(old), FadeIn(new, shift=UP * 0.2), run_time=0.5)
        self.card_mob = new

    def uncard(self):
        if getattr(self, "card_mob", None) is not None:
            self.play(FadeOut(self.card_mob), run_time=0.3)
            self.card_mob = None

    # ---- shared closing blocks
    def recap(self, bullets, ids, title="Recap"):
        head = T(title, size=38, bold=True).move_to([0, 2.7, 0])
        rows = VGroup()
        for k, b in enumerate(bullets):
            num = T(str(k + 1), size=28, color=BG, bold=True)
            dot = Circle(radius=0.3, color=HILITE, fill_color=HILITE, fill_opacity=1, stroke_width=0)
            txt = Paragraph(*b, font=FONT, font_size=26, color=INK, line_spacing=0.8)
            rows.add(VGroup(VGroup(dot, num.move_to(dot)), txt).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0, 0.1, 0])
        with self.voice(ids[0]):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        for row, i in zip(rows, ids[1:]):
            with self.voice(i):
                self.play(FadeIn(row, shift=RIGHT * 0.3))
        self.play(FadeOut(VGroup(head, rows)))

    def questions(self, qas, intro_id, pause=5.0):
        """qas: (question id, answer id, question mobject, answer mobject). The viewer gets
        `pause` seconds, shown as a shrinking bar, before each answer."""
        head = T("Check yourself", size=38, bold=True).move_to([0, 2.7, 0])
        with self.voice(intro_id):
            self.play(FadeIn(head, shift=DOWN * 0.2))
        for k, (qid, aid, q, ans) in enumerate(qas):
            q.move_to([0, 0.9, 0])
            qn = pill(f"Question {k + 1} of {len(qas)}", color=HILITE, size=22).next_to(q, UP, buff=0.4)
            with self.voice(qid, gap=0.3):
                self.play(FadeIn(qn), FadeIn(q, shift=UP * 0.2))
            bar_bg = Rectangle(width=6, height=0.16, color=DIM, fill_color=DIM, fill_opacity=1,
                               stroke_width=0).move_to([0, -0.35, 0])
            bar = Rectangle(width=6, height=0.16, color=HILITE, fill_color=HILITE, fill_opacity=1,
                            stroke_width=0).move_to(bar_bg)
            hint = T("Pause and think", size=22, color=MUTED).next_to(bar_bg, DOWN, buff=0.2)
            self.add(bar_bg, bar, hint)
            self.play(bar.animate.stretch_to_fit_width(0.02).align_to(bar_bg, LEFT),
                      run_time=pause, rate_func=linear)
            self.remove(bar_bg, bar, hint)
            ans.set_color(GOOD).move_to([0, -0.8, 0])
            with self.voice(aid, gap=0.8):
                self.play(FadeIn(ans, shift=UP * 0.2))
            self.play(FadeOut(VGroup(qn, q, ans)))
        self.play(FadeOut(head))

    def save_marks(self):
        d = out_dir(self.EP)
        d.mkdir(parents=True, exist_ok=True)
        (d / "marks.json").write_text(
            json.dumps({"total": round(self.now, 3), "marks": self.marks}, indent=1), encoding="utf-8")
