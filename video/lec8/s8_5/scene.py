"""Section 8.5 — The surface code.   Draft.
Build from the video folder with the Manim environment:
    python pipeline/build.py 8.5 render --low        (ONLY=<letters> renders chosen scenes)
Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.

The torus is drawn flat (the user's choice after the 3D draft, 2026-11-24): arrows on the square's
edges mark the gluing, and a flat doughnut icon shows the two kinds of loop. The scene is still a
ThreeDScene (the 3D helpers bend() and torus() are kept, unused, in case they are wanted later). Everything else is drawn flat with the camera looking
straight down, which renders the same as the earlier sections; the heading and the watermark are
fixed in the frame so they stay put while the camera turns.

Colours as in 8.1 to 8.4: purple is X (vertex checks, X errors), green is Z (face checks, Z
errors), orange a check that fires (a 1 in the syndrome) and the minus signs, cyan what to look at.
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from common import *  # noqa: E402,F401
from common import NarratedScene as _NS  # noqa: E402

X_COL, Z_COL = PAULI_X, PAULI_Z
FLAT = dict(phi=0, theta=-90 * DEGREES, zoom=1.0)
TILT = dict(phi=62 * DEGREES, theta=-62 * DEGREES, zoom=1.45)


def tile(ch, s=0.3):
    col = {"X": X_COL, "Z": Z_COL, "I": DIM}[ch]
    box = RoundedRectangle(width=s, height=s, corner_radius=0.12 * s, stroke_width=0, fill_color=col, fill_opacity=1)
    g = VGroup(box)
    if ch != "I":
        g.add(T(ch, size=max(int(68 * s), 12), color=BG if ch == "Z" else INK, bold=True).move_to(box))
    return g


def pstring(letters, s=0.3):
    return VGroup(*[tile(c, s) for c in letters]).arrange(RIGHT, buff=0.14 * s)


def minus(size=40):
    return M("-", size=size, color=ACCENT)


# ------------------------------------------------------------------ the lattice
class Lat:
    """An L x L patch of the square lattice, qubits on edges. Vertices are (c, r), c to the right,
    r downwards; edges are ('h', r, c) from (c, r) to (c+1, r) and ('v', r, c) from (c, r) to
    (c, r+1). Index L on either axis is the dashed boundary glued to index 0."""

    def __init__(self, L=6, s=0.7, centre=(-0.9, 0.15)):
        self.L, self.s = L, s
        self.x0 = centre[0] - L * s / 2
        self.y0 = centre[1] + L * s / 2

    def v(self, c, r):
        return np.array([self.x0 + c * self.s, self.y0 - r * self.s, 0.0])

    def ends(self, e):
        k, r, c = e
        return (self.v(c, r), self.v(c + 1, r)) if k == "h" else (self.v(c, r), self.v(c, r + 1))

    def mid(self, e):
        a, b = self.ends(e)
        return (a + b) / 2

    def face(self, c, r):
        return self.v(c, r) + np.array([self.s / 2, -self.s / 2, 0])

    def lines(self, color=MUTED, width=2):
        g = VGroup()
        for k in range(self.L + 1):
            for a, b in ((self.v(0, k), self.v(self.L, k)), (self.v(k, 0), self.v(k, self.L))):
                ln = Line(a, b, color=color, stroke_width=width)
                if k == self.L:
                    ln = DashedLine(a, b, color=color, stroke_width=width, dash_length=0.09)
                g.add(ln)
        return g

    def all_edges(self):
        return [("h", r, c) for r in range(self.L) for c in range(self.L)] + \
               [("v", r, c) for r in range(self.L) for c in range(self.L)]

    def dots(self, r=0.045):
        return VGroup(*[Dot(self.mid(e), radius=r, color=MUTED) for e in self.all_edges()])

    def edge(self, e, color, width=7):
        a, b = self.ends(e)
        return Line(a, b, color=color, stroke_width=width)

    def path_edges(self, pts):
        out = []
        for (c1, r1), (c2, r2) in zip(pts, pts[1:]):
            if r1 == r2:
                out.append(("h", r1, min(c1, c2)))
            else:
                out.append(("v", min(r1, r2), c1))
        return out

    def vertex_edges(self, c, r):
        return [("h", r, c), ("h", r, c - 1), ("v", r, c), ("v", r - 1, c)]

    def face_edges(self, c, r):
        return [("h", r, c), ("h", r + 1, c), ("v", r, c), ("v", r, c + 1)]

    def glue_marks(self):
        """Arrow heads on the boundary: one on top and bottom, two on left and right."""
        g = VGroup()
        for r in (0, self.L):
            p = (self.v(0, r) + self.v(self.L, r)) / 2
            g.add(Triangle(color=MUTED, fill_opacity=1, stroke_width=0).scale(0.09).rotate(-PI / 2).move_to(p))
        for c in (0, self.L):
            p = (self.v(c, 0) + self.v(c, self.L)) / 2
            for d in (-0.1, 0.1):
                g.add(Triangle(color=MUTED, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI).move_to(p + [0, d, 0]))
        return g


# ------------------------------------------------------------------ the torus (3D)
SW, SH = 8.4, 3.4          # the sheet that is rolled: wider than tall, so the torus has a hole


def _sinc(x):
    return 1.0 if abs(x) < 1e-6 else np.sin(x) / x


def bend(X, Y, t, s):
    """Roll the sheet about the x axis (t: 0 flat -> 1 tube), then bend the tube (s: 0 -> 1 torus).
    Each stage subtracts the centroid of its arc, so the shape stays centred at the origin."""
    R1 = SH / (2 * PI)
    if t < 1e-3:
        y, z, zc = Y, 0.0, 0.0
    else:
        r = SH / (2 * PI * t)
        th = Y / r
        y, z = r * np.sin(th), r * (1 - np.cos(th))
        zc = r * (1 - _sinc(PI * t))
    if s < 1e-3:
        return np.array([X, y, z - zc])
    R2 = SW / (2 * PI * s)
    d = z - R1
    phi = X / R2
    p = np.array([(R2 - d) * np.sin(phi), y, R1 + R2 - (R2 - d) * np.cos(phi)])
    return p - np.array([0, 0, R1 + R2 - R2 * _sinc(PI * s)])


class Narrated3D(ThreeDScene):
    """NarratedScene's pacing (voice blocks, pauses, marks) on a ThreeDScene."""
    EP = "1.1"
    voice = _NS.__dict__["voice"]
    pause_after = _NS.pause_after
    save_marks = _NS.save_marks
    now = _NS.now

    def setup(self):
        ThreeDScene.setup(self)
        self.script = load_script(self.EP)
        self.subs = {i: sub for i, sub, _ in self.script.SEGS}
        p = out_dir(self.EP) / "durations.json"
        self.durs = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        self.marks = []
        self.head = None

    def hold(self, seconds):
        if seconds > 0.04:
            self.wait(seconds)


class Main(Narrated3D):
    EP = "8.5"
    SCENES = [("i", "opening"), ("a", "hook"), ("b", "lattice"), ("c", "chains"), ("d", "loops"),
              ("e", "decoding"), ("f", "closing")]

    def construct(self):
        only = os.environ.get("ONLY", "")
        self.busy = {}
        self.set_camera_orientation(**FLAT)
        self.head = header("8.5  The surface code")
        self.wm = watermark()
        self.lat = Lat()
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter != "i" and self.head not in self.mobjects:
                self.add_fixed_in_frame_mobjects(self.head, self.wm)
                self.remove(self.head, self.wm)
                self.play(FadeIn(self.head), FadeIn(self.wm), run_time=0.4)
            getattr(self, name)()
        self.save_marks()
        (out_dir(self.EP) / "busy.json").write_text(json.dumps(self.busy, indent=1), encoding="utf-8")

    @contextmanager
    def voice(self, *ids, gap=None):
        words = sum(len(self.subs[i].split()) for i in ids)
        real = sum(self.durs[i] for i in ids) if all(i in self.durs for i in ids) else None
        self.pace = real / (words / 150 * 60) if real else 1.0
        with Narrated3D.voice(self, *ids, gap=gap) as total:
            t0 = self.now
            yield total
            self.busy[ids[-1]] = {"busy": round(self.now - t0, 2), "voice": round(total, 2),
                                  "at_219_wpm": round(words / 219 * 60, 2)}
        self.pace = 1.0

    def hold(self, seconds):
        super().hold(seconds * getattr(self, "pace", 1.0))

    def keep(self):
        return [self.head, self.wm]

    def stage(self):
        return [m for m in self.mobjects if m not in self.keep()]

    def clear_stage(self, run_time=0.6):
        left = self.stage()
        if left:
            self.play(*[FadeOut(m) for m in left], run_time=run_time)

    def fixed(self, *mobs):
        """Text that must stay upright while the camera turns."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)
        return mobs[0] if len(mobs) == 1 else VGroup(*mobs)

    # ------------------------------------------------------------ shared pieces
    def grid(self, lat=None, glue=True):
        lat = lat or self.lat
        g = VGroup(lat.lines(), lat.dots())
        if glue:
            g.add(lat.glue_marks())
        return g

    def vertex_check(self, c, r, lat=None):
        lat = lat or self.lat
        edges = [lat.edge(e, X_COL, 6) for e in lat.vertex_edges(c, r)]
        tiles = [tile("X", 0.24).move_to(lat.mid(e)) for e in lat.vertex_edges(c, r)]
        return VGroup(VGroup(*edges), VGroup(*tiles))

    def face_check(self, c, r, lat=None):
        lat = lat or self.lat
        edges = [lat.edge(e, Z_COL, 6) for e in lat.face_edges(c, r)]
        tiles = [tile("Z", 0.24).move_to(lat.mid(e)) for e in lat.face_edges(c, r)]
        return VGroup(VGroup(*edges), VGroup(*tiles))

    def fire(self, p, r=0.11):
        return Dot(p, radius=r, color=ACCENT)

    def ring(self, p, r=0.11, q=False):
        c = Circle(radius=r, color=INK, stroke_width=2.5).move_to(p)
        if q:
            return VGroup(c, T("?", size=16, color=MUTED).move_to(p))
        return c

    def chain(self, pts, color=Z_COL, lat=None):
        lat = lat or self.lat
        return VGroup(*[lat.edge(e, color) for e in lat.path_edges(pts)])

    def torus(self, t, s, L=6, extra_rows=(), extra_color=Z_COL):
        """The lattice drawn on the rolled sheet; extra_rows are rows drawn thick (a loop)."""
        g = VGroup()
        for k in range(L):
            Y = SH / 2 - k * SH / L
            pts = [bend(-SW / 2 + SW * j / 72, Y, t, s) for j in range(73)]
            g.add(VMobject(stroke_color=MUTED, stroke_width=2).set_points_smoothly(pts))
        for k in range(L):
            X = -SW / 2 + k * SW / L
            pts = [bend(X, SH / 2 - SH * j / 40, t, s) for j in range(41)]
            g.add(VMobject(stroke_color=MUTED, stroke_width=2).set_points_smoothly(pts))
        for k in extra_rows:
            Y = SH / 2 - k * SH / L
            pts = [bend(-SW / 2 + SW * j / 72, Y, t, s) for j in range(73)]
            g.add(VMobject(stroke_color=extra_color, stroke_width=7).set_points_smoothly(pts))
        return g

    def donut(self, centre, w=2.4, h=1.4):
        """A flat drawing of a torus: outline, the hole, and the two kinds of loop on it.
        .around is the loop around the hole (the grid's rows), .through the loop round the tube
        (the grid's columns)."""
        c = np.array((list(centre) + [0.0, 0.0])[:3], dtype=float)
        outer = Ellipse(width=w, height=h, color=MUTED, stroke_width=2.5).move_to(c)
        hole_top = ArcBetweenPoints(c + [-0.3 * w, 0.02 * h, 0], c + [0.3 * w, 0.02 * h, 0], angle=-PI / 2.4,
                                    color=MUTED, stroke_width=2.5)
        hole_bot = ArcBetweenPoints(c + [-0.24 * w, 0.06 * h, 0], c + [0.24 * w, 0.06 * h, 0], angle=PI / 2.6,
                                    color=MUTED, stroke_width=2.5)
        around = Ellipse(width=0.74 * w, height=0.56 * h, color=MUTED, stroke_width=2).move_to(c + [0, 0.02 * h, 0])
        around.set_stroke(opacity=0.0)
        through = Ellipse(width=0.12 * w, height=0.3 * h, color=MUTED, stroke_width=2).move_to(c + [-0.37 * w, -0.05 * h, 0])
        through.set_stroke(opacity=0.0)
        g = VGroup(outer, hole_top, hole_bot, around, through)
        g.around, g.through = around, through
        return g

    # ------------------------------------------------------------ I. opening
    def opening(self):
        centre = [0, 1.35, 0]
        lab = T("QAICON Lab", size=54, bold=True).move_to([0, -0.85, 0])
        full = T("Quantum and AI for Computing, Optimization, and Networking", size=26, color=HILITE)
        full.next_to(lab, DOWN, buff=0.3)
        where = T("Western University", size=24, color=MUTED).next_to(full, DOWN, buff=0.25)
        with self.voice("i1"):
            mark_ = logo_reveal(self, centre)
            self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.6)
            self.hold(0.3)
            self.play(FadeIn(full, shift=UP * 0.15), run_time=0.7)
            self.hold(1.2)
            self.play(FadeIn(where), run_time=0.5)
        series = T("Quantum Computing Workshop", size=28, color=MUTED).move_to([0, 1.2, 0])
        title = T("The surface code", size=50, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 8  ·  Section 8.5", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark_.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark_, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    # ------------------------------------------------------------ A. do the checks have to grow?
    def hook(self):
        self.clear_stage()
        cards = VGroup(*[pill(t, color=MUTED, size=22) for t in ("Shor  [[9,1,3]]", "Steane  [[7,1,3]]", "five-qubit  [[5,1,3]]")])
        cards.arrange(RIGHT, buff=0.35).move_to([0, 2.1, 0])
        threes = VGroup(*[T("d = 3", size=22, color=HILITE).next_to(c, DOWN, buff=0.15) for c in cards])
        row = VGroup(*[Dot(radius=0.07, color=MUTED) for _ in range(24)]).arrange(RIGHT, buff=0.32).move_to([0, -0.6, 0])
        with self.voice("a1"):
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.25), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(t) for t in threes], lag_ratio=0.3), run_time=0.9)
            self.hold(2.4)
            self.play(FadeIn(row), run_time=0.6)
            errs = VGroup(*[tile(ch, 0.26).next_to(row[k], UP, buff=0.12) for k, ch in
                            ((2, "X"), (6, "Z"), (9, "X"), (13, "Z"), (17, "X"), (21, "Z"))])
            self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.4) for e in errs], lag_ratio=0.2), run_time=1.4)
        # a2: does each check have to reach further? (thinking pause)
        anc = Dot([0, 1.4, 0], radius=0.12, color=HILITE)
        def fan(n, width):
            ds = VGroup(*[Dot(radius=0.06, color=MUTED) for _ in range(n)]).arrange(RIGHT, buff=width / max(n - 1, 1) - 0.12)
            ds.move_to([0, -0.9, 0])
            return VGroup(ds, VGroup(*[Line(anc.get_center(), d.get_center(), color=MUTED, stroke_width=1.5) for d in ds]))
        f4, f8, f16 = fan(4, 1.6), fan(8, 4.0), fan(16, 9.0)
        q = T("?", size=48, color=HILITE, bold=True).move_to([5.6, 0.3, 0])
        with self.voice("a2"):
            self.play(FadeOut(VGroup(cards, threes, row, errs)), run_time=0.5)
            self.play(FadeIn(anc), FadeIn(f4), run_time=0.6)
            self.hold(1.4)
            self.play(ReplacementTransform(f4, f8), run_time=0.8)
            self.play(ReplacementTransform(f8, f16), run_time=0.8)
            self.play(FadeIn(q, scale=1.5), run_time=0.4)
        # a3: (she answers; nothing new)
        with self.voice("a3"):
            self.play(Indicate(q, color=HILITE, scale_factor=1.3), run_time=0.8)
        # a4: no: the fan folds back to four neighbours, and the cross tiles a grid
        shor = pstring("XXXXXXIII", 0.3).move_to([-3.9, 2.4, 0])
        sl = T("Shor: six qubits", size=20, color=MUTED).next_to(shor, DOWN, buff=0.15)
        lat = self.lat
        cross = self.vertex_check(3, 3)
        with self.voice("a4"):
            self.play(FadeIn(shor), FadeIn(sl), run_time=0.5)
            self.hold(1.8)
            self.play(FadeOut(VGroup(shor, sl, q)), run_time=0.4)
            self.play(ReplacementTransform(VGroup(f16, anc), cross), run_time=1.2)
            self.hold(1.0)
            g = self.grid(glue=False)
            self.play(Create(g[0]), FadeIn(g[1]), run_time=1.4)
            self.hold(0.6)
        self.clear_stage()

    # ------------------------------------------------------------ B. the lattice and its checks
    def lattice(self):
        self.clear_stage()
        lat = self.lat
        g = self.grid()
        # b1: grid, qubits on edges, glued boundary
        with self.voice("b1"):
            self.hold(0.8)
            self.play(Create(g[0]), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in g[1]], lag_ratio=0.01), run_time=1.2)
            self.hold(1.0)
            self.play(FadeIn(g[2]), run_time=0.6)
        # b2: the glued square is a doughnut (flat icon); a column goes round the tube, a row round the hole
        icon = self.donut([4.6, 1.3])
        name = T("the toric code", size=30, bold=True).next_to(icon, DOWN, buff=0.35)
        with self.voice("b2"):
            self.play(Create(icon[:3]), run_time=0.9)
            self.hold(0.6)
            col = lat.edge(("v", 0, 2), HILITE, 5)
            colv = VGroup(*[lat.edge(("v", r, 2), HILITE, 5) for r in range(6)])
            self.play(*[Indicate(m, color=HILITE, scale_factor=1.8) for m in g[2][:2]], Create(colv), run_time=0.8)
            self.play(icon.through.animate.set_stroke(HILITE, opacity=1, width=4), run_time=0.6)
            rowv = VGroup(*[lat.edge(("h", 3, c), HILITE, 5) for c in range(6)])
            self.play(*[Indicate(m, color=HILITE, scale_factor=1.8) for m in g[2][2:]], Create(rowv), run_time=0.8)
            self.play(icon.around.animate.set_stroke(HILITE, opacity=1, width=4), run_time=0.6)
            self.play(FadeIn(name, shift=UP * 0.15), run_time=0.5)
            self.hold(1.0)
            self.play(FadeOut(VGroup(colv, rowv)), icon.through.animate.set_stroke(opacity=0),
                      icon.around.animate.set_stroke(opacity=0), run_time=0.5)
            br = Brace(VGroup(Dot(lat.v(0, 6)), Dot(lat.v(6, 6))), DOWN, color=MUTED, buff=0.15)
            bl = M("L", size=32, color=MUTED).next_to(br, DOWN, buff=0.08)
            n = M("n = 2L^2", size=38).move_to([4.6, -1.0, 0])
            self.play(GrowFromCenter(br), FadeIn(bl), FadeIn(n), run_time=0.6)
        self.icon = icon
        # b3: the two kinds of check
        A = self.vertex_check(2, 2)
        B = self.face_check(4, 1)
        la = M("A_v", size=38, color=X_COL).next_to(np.array([lat.x0, lat.v(2, 2)[1], 0]), LEFT, buff=0.3)
        lb = M("B_f", size=34, color=Z_COL).next_to(lat.v(4, 1) + np.array([lat.s / 2, 0, 0]), UP, buff=0.32)
        with self.voice("b3"):
            self.play(FadeOut(VGroup(br, bl, icon, name)), n.animate.move_to([4.7, 2.3, 0]).scale(0.8), run_time=0.4)
            self.hold(0.6)
            self.play(Create(A[0]), FadeIn(A[1]), run_time=0.8)
            self.play(FadeIn(la), run_time=0.3)
            self.hold(1.2)
            self.play(Create(B[0]), FadeIn(B[1]), run_time=0.8)
            self.play(FadeIn(lb), run_time=0.3)
        # b4: (she asks)
        with self.voice("b4"):
            self.play(Indicate(A, color=X_COL, scale_factor=1.08), Indicate(B, color=Z_COL, scale_factor=1.08), run_time=0.8)
        # b5: a vertex and a face share two edges or none; two clashes cancel
        with self.voice("b5"):
            B2 = self.face_check(2, 2)
            self.play(ReplacementTransform(B.copy(), B2), run_time=0.8)
            shared = [("h", 2, 2), ("v", 2, 2)]
            frs = VGroup(*[Circle(radius=0.2, color=HILITE, stroke_width=3).move_to(lat.mid(e)) for e in shared])
            self.play(Create(frs), run_time=0.5)
            sp = VGroup(*[minus().next_to(f, UR, buff=0.0) for f in frs])
            self.play(FadeIn(sp, scale=1.6), run_time=0.4)
            midp = (sp[0].get_center() + sp[1].get_center()) / 2
            self.play(*[m.animate.move_to(midp) for m in sp], run_time=0.6)
            self.play(FadeOut(sp, scale=0.3), Flash(midp, color=ACCENT), run_time=0.5)
            ev = VGroup(T("2  even", size=24), mark(True)).arrange(RIGHT, buff=0.15).move_to([4.7, 1.2, 0])
            self.play(FadeIn(ev), run_time=0.4)
            self.play(FadeOut(VGroup(B2, frs)), run_time=0.4)
            far = VGroup(T("0", size=24), mark(True)).arrange(RIGHT, buff=0.15).next_to(ev, DOWN, buff=0.25, aligned_edge=LEFT)
            self.play(Indicate(B, color=Z_COL), FadeIn(far), run_time=0.7)
        # b6: hardware: an ancilla in the middle, four CNOTs (the circuit)
        anc = Dot(lat.face(4, 1), radius=0.1, color=HILITE)
        wires = VGroup(*[Line(lat.face(4, 1), lat.mid(e), color=HILITE, stroke_width=2.5) for e in lat.face_edges(4, 1)])
        circ = Circuit(["1", "2", "3", "4"], 1, [("cnot", k, 4) for k in range(4)], gap=0.36, step=0.42, lead=0.5, size=0.26)
        circ.move_to([4.6, -1.0, 0])
        with self.voice("b6"):
            self.play(FadeOut(VGroup(ev, far, A, la)), lb.animate.next_to(B, UP, buff=0.12), run_time=0.5)
            self.play(FadeIn(anc, scale=1.6), run_time=0.4)
            self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.2), run_time=0.8)
            self.hold(1.0)
            self.play(Create(circ.wires), FadeIn(circ.labels), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c) for c in circ.cols], lag_ratio=0.25), FadeIn(circ.meters), run_time=1.2)
        self.circ_shape = circ.copy()
        # b7: all vertex checks multiply to I, all face checks too: two relations, k = 2
        with self.voice("b7"):
            self.play(FadeOut(VGroup(anc, wires, circ, B, lb)), run_time=0.5)
            allx = VGroup(*[lat.edge(e, X_COL, 5) for e in lat.all_edges()])
            px = M(r"\prod_v A_v = I", size=34, color=X_COL).move_to([4.6, 1.2, 0])
            self.play(Create(allx), run_time=0.9)
            self.play(allx.animate.set_stroke(width=10, opacity=0.9), run_time=0.4)
            self.play(FadeOut(allx), FadeIn(px), run_time=0.6)
            allz = VGroup(*[lat.edge(e, Z_COL, 5) for e in lat.all_edges()])
            pz = M(r"\prod_f B_f = I", size=34, color=Z_COL).next_to(px, DOWN, buff=0.3)
            self.play(Create(allz), run_time=0.9)
            self.play(FadeOut(allz), FadeIn(pz), run_time=0.6)
            k = M(r"2L^2 - (2L^2 - 2) = 2", size=32).next_to(pz, DOWN, buff=0.45)
            self.play(FadeIn(k), run_time=0.6)
            kk = M("k = 2", size=40, color=HILITE).next_to(k, DOWN, buff=0.3)
            self.play(FadeIn(kk, shift=UP * 0.15), run_time=0.5)
        self.clear_stage()

    # ------------------------------------------------------------ C. errors are chains
    def chains(self):
        self.clear_stage()
        lat = self.lat
        g = self.grid()
        pts = [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)]
        ch = self.chain(pts)
        with self.voice("c1"):
            self.play(FadeIn(g), run_time=0.6)
            self.hold(1.4)
            self.play(LaggedStart(*[Create(e) for e in ch], lag_ratio=0.5), run_time=1.6)
        rings = VGroup(*[self.ring(lat.v(*p), q=True) for p in pts])
        with self.voice("c2"):
            self.hold(1.6)
            self.play(LaggedStart(*[FadeIn(r) for r in rings], lag_ratio=0.15), run_time=0.8)
        with self.voice("c3"):
            pass
        with self.voice("c4"):
            self.hold(2.0)
            mids = pts[1:-1]
            for p in mids:
                q = lat.v(*p)
                a, b = minus(34).move_to(q + [-0.18, 0.2, 0]), minus(34).move_to(q + [0.18, 0.2, 0])
                self.play(FadeIn(a, scale=1.5), FadeIn(b, scale=1.5), run_time=0.25)
                self.play(a.animate.move_to(q + [0, 0.2, 0]), b.animate.move_to(q + [0, 0.2, 0]), run_time=0.3)
                self.play(FadeOut(VGroup(a, b), scale=0.3), Transform(rings[pts.index(p)], self.ring(q)), run_time=0.3)
            self.hold(0.4)
            for p in (pts[0], pts[-1]):
                q = lat.v(*p)
                a = minus(34).move_to(q + [0, 0.22, 0])
                self.play(FadeIn(a, scale=1.5), run_time=0.25)
                self.play(Transform(rings[pts.index(p)], self.fire(q)), FadeOut(a), run_time=0.35)
        # c5: the syndrome shows only where the chain stops
        alts = VGroup(*[DashedLine(lat.v(*a), lat.v(*b), color=HILITE, stroke_width=3, dash_length=0.1) for a, b in
                        [((1, 1), (3, 1)), ((3, 1), (3, 3)), ((1, 1), (1, 3)), ((1, 3), (3, 3))]])
        with self.voice("c5"):
            self.play(ch.animate.set_stroke(opacity=0.2), FadeOut(VGroup(rings[1], rings[2], rings[3])), run_time=0.8)
            self.hold(1.4)
            self.play(Create(alts), run_time=1.0)
        # c6: X errors on the dual lattice light two face checks
        dual = VGroup(*[DashedLine(lat.face(0, k) + [-lat.s / 2, 0, 0], lat.face(5, k) + [lat.s / 2, 0, 0], color=MUTED,
                                   stroke_width=1.2, dash_length=0.06) for k in range(6)] +
                      [DashedLine(lat.face(k, 0) + [0, lat.s / 2, 0], lat.face(k, 5) + [0, -lat.s / 2, 0], color=MUTED,
                                  stroke_width=1.2, dash_length=0.06) for k in range(6)])
        xe = VGroup(*[lat.edge(("v", 4, c), X_COL) for c in (1, 2, 3)])
        with self.voice("c6"):
            self.play(FadeOut(VGroup(ch, alts, rings[0], rings[4])), run_time=0.5)
            self.play(Create(dual), run_time=1.0)
            self.hold(1.4)
            path = Line(lat.face(0, 4), lat.face(3, 4), color=X_COL, stroke_width=2.5)
            self.play(Create(xe), Create(path), run_time=1.0)
            self.play(FadeIn(self.fire(lat.face(0, 4))), FadeIn(self.fire(lat.face(3, 4))), run_time=0.5)
        self.clear_stage()

    # ------------------------------------------------------------ D. loops
    def loops(self):
        self.clear_stage()
        lat = self.lat
        g = self.grid()
        loop_pts = [(4, 1), (5, 1), (5, 2), (5, 3), (4, 3), (4, 2)]
        open_ch = self.chain(loop_pts)
        close = lat.edge(("v", 1, 4), Z_COL)
        e1, e2 = self.fire(lat.v(4, 1)), self.fire(lat.v(4, 2))
        # d1: a chain closes into a loop; its ends go dark
        with self.voice("d1"):
            self.play(FadeIn(g), run_time=0.5)
            self.play(LaggedStart(*[Create(e) for e in open_ch], lag_ratio=0.3), run_time=1.2)
            self.play(FadeIn(e1), FadeIn(e2), run_time=0.4)
            self.hold(1.0)
            self.play(Create(close), run_time=0.6)
            self.play(FadeOut(e1), FadeOut(e2), run_time=0.5)
        loop = VGroup(open_ch, close)
        # d2: a loop round a patch is the product of the face checks inside: no effect
        fill = Polygon(lat.v(4, 1), lat.v(5, 1), lat.v(5, 3), lat.v(4, 3), stroke_width=0, fill_color=HILITE, fill_opacity=0.18)
        f1, f2 = self.face_check(4, 1), self.face_check(4, 2)
        note = VGroup(T("product of 2 face checks", size=22), T("no effect  (the innermost region of 8.2)", size=18, color=MUTED))
        note.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.7, 1.5, 0])
        with self.voice("d2"):
            self.play(FadeIn(fill), run_time=0.5)
            self.hold(1.0)
            ghost = VGroup(f1[0].copy(), f2[0].copy())
            self.play(FadeIn(ghost), run_time=0.6)
            shared = lat.edge(("h", 2, 4), HILITE, 7)
            self.play(Create(shared), run_time=0.4)
            self.play(FadeOut(shared), FadeOut(ghost), run_time=0.6)
            self.play(FadeIn(note), run_time=0.5)
        for m in [m for m in self.mobjects if m not in self.keep() and m not in (g, loop, fill, note)]:
            self.remove(m)
        # d3: a line all the way across one row (thinking pause)
        row = VGroup(*[lat.edge(("h", 4, c), Z_COL) for c in range(6)])
        with self.voice("d3"):
            self.play(FadeOut(VGroup(loop, fill, note)), run_time=0.4)
            self.play(LaggedStart(*[Create(e) for e in row], lag_ratio=0.4), run_time=1.6)
            self.play(row.animate.set_stroke(HILITE, width=9), run_time=0.3)
            self.play(row.animate.set_stroke(Z_COL, width=7), run_time=0.3)
        # d4: the row runs into the glued edge and comes back: a closed loop round the hole; a logical operator
        icon = self.donut([4.6, 1.3])
        lab = T("logical operator", size=30, bold=True).next_to(icon, DOWN, buff=0.4)
        with self.voice("d4"):
            spark = Dot(lat.v(0, 4), radius=0.1, color=HILITE)
            self.play(FadeIn(spark), run_time=0.2)
            self.play(spark.animate.move_to(lat.v(6, 4)), run_time=1.0, rate_func=linear)
            edges = VGroup(DashedLine(lat.v(6, 0), lat.v(6, 6), color=HILITE, stroke_width=3, dash_length=0.09),
                           Line(lat.v(0, 0), lat.v(0, 6), color=HILITE, stroke_width=3))
            self.play(FadeIn(edges), run_time=0.3)
            spark.move_to(lat.v(0, 4))
            self.play(FadeOut(edges), Flash(lat.v(0, 4), color=HILITE), run_time=0.4)
            self.play(FadeOut(spark), run_time=0.2)
            self.play(Create(icon[:3]), run_time=0.7)
            glow = icon.around.copy().set_stroke(HILITE, opacity=0.35, width=12)
            self.play(icon.around.animate.set_stroke(Z_COL, opacity=1, width=5), FadeIn(glow), run_time=0.7)
            self.hold(1.6)
            tryf = self.face_check(2, 3)
            self.play(FadeIn(tryf[0]), run_time=0.4)
            self.play(FadeOut(tryf[0]), FadeIn(mark(False).move_to(lat.face(2, 3)).scale(1.3)), run_time=0.6)
            self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
            self.hold(1.0)
        stray = [m for m in self.mobjects if m not in self.keep() and m not in (g, row)]
        if stray:
            self.play(*[FadeOut(m) for m in stray], run_time=0.3)
        # d5: count the row: d = L; the grid grows, the checks keep their size
        nums = VGroup(*[T(str(c + 1), size=18, color=HILITE).next_to(lat.mid(("h", 4, c)), DOWN, buff=0.12) for c in range(6)])
        dL = M("d = L", size=40, color=HILITE).move_to([4.7, 1.2, 0])
        big = Lat(L=8, s=lat.s, centre=(-0.9, 0.15))
        with self.voice("d5"):
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.15), run_time=0.9)
            self.play(FadeIn(dL), run_time=0.4)
            self.hold(1.6)
            g2 = self.grid(big)
            row2 = VGroup(*[big.edge(("h", 6, c), Z_COL) for c in range(8)])
            vc, fc = self.vertex_check(2, 2, big), self.face_check(5, 1, big)
            self.play(FadeOut(nums), ReplacementTransform(g, g2), ReplacementTransform(row, row2), run_time=1.4)
            self.play(FadeIn(vc), FadeIn(fc), run_time=0.6)
            self.hold(0.6)
        # d6: [[2L^2, 2, L]]
        code = M(r"[[\,2L^2,\ 2,\ L\,]]", size=44).next_to(dL, DOWN, buff=0.5)
        with self.voice("d6"):
            self.play(FadeIn(code, shift=UP * 0.15), run_time=0.6)
        # d7: shrinkable loop (harmless) against a loop around (logical)
        with self.voice("d7"):
            self.play(FadeOut(VGroup(g2, row2, vc, fc)), VGroup(dL, code).animate.scale(0.8).move_to([4.8, 2.3, 0]), run_time=0.6)
            sq1 = Square(2.4, color=MUTED, stroke_width=2).move_to([-3.4, -0.2, 0])
            sq2 = Square(2.4, color=MUTED, stroke_width=2).move_to([0.6, -0.2, 0])
            c1 = Circle(radius=0.7, color=Z_COL, stroke_width=6).move_to(sq1)
            l2 = Line(sq2.get_left(), sq2.get_right(), color=Z_COL, stroke_width=6)
            t1 = T("harmless", size=24).next_to(sq1, DOWN, buff=0.25)
            t2 = T("logical", size=24).next_to(sq2, DOWN, buff=0.25)
            self.play(Create(sq1), Create(sq2), FadeIn(sq2.copy().set_stroke(opacity=0)), run_time=0.5)
            self.play(Create(c1), Create(l2), run_time=0.7)
            self.hold(2.0)
            self.play(c1.animate.scale(0.02), run_time=1.2)
            self.play(FadeOut(c1), FadeIn(t1), run_time=0.4)
            self.play(l2.animate.shift(UP * 0.6), run_time=0.6)
            self.play(l2.animate.shift(DOWN * 1.2), run_time=0.8)
            self.play(l2.animate.shift(UP * 0.6), FadeIn(t2), run_time=0.6)
        self.clear_stage()

    # ------------------------------------------------------------ E. decoding, and the flat patch
    def decoding(self):
        self.clear_stage()
        lat = self.lat
        g = self.grid()
        errs = [[(0, 1), (1, 1), (2, 1)], [(4, 3), (5, 3), (5, 4)], [(1, 4), (1, 5)]]
        E = VGroup(*[self.chain(p) for p in errs])
        ends = [(p[0], p[-1]) for p in errs]
        dots = VGroup(*[self.fire(lat.v(*q)) for pair in ends for q in pair])
        fixes = [[(0, 1), (1, 1), (2, 1)], [(4, 3), (4, 4), (5, 4)], [(1, 4), (1, 5)]]
        with self.voice("e1"):
            self.play(FadeIn(g), run_time=0.5)
            self.play(FadeIn(E), run_time=0.6)
            self.play(FadeIn(dots), run_time=0.4)
            self.hold(0.6)
            self.play(E.animate.set_stroke(opacity=0), run_time=0.6)
            self.hold(0.8)
            paths = VGroup(*[VMobject(stroke_color=HILITE, stroke_width=4).set_points_as_corners([lat.v(*q) for q in f]) for f in fixes])
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.35), run_time=1.4)
            corr = VGroup(*[self.chain(f) for f in fixes])
            self.play(ReplacementTransform(paths, corr), FadeOut(dots), run_time=0.8)
        # e2: guess + error form a loop that shrinks away
        with self.voice("e2"):
            self.play(E.animate.set_stroke(opacity=1), run_time=0.6)
            fill = Square(lat.s, stroke_width=0, fill_color=HILITE, fill_opacity=0.3).move_to(lat.face(4, 3))
            self.play(FadeIn(fill), Indicate(VGroup(E[1], corr[1]), color=HILITE, scale_factor=1.05), run_time=0.8)
            self.hold(1.4)
            loopg = VGroup(E[1], corr[1], fill)
            self.play(loopg.animate.scale(0.05), run_time=1.0)
            self.play(FadeOut(loopg), FadeOut(VGroup(E[0], E[2], corr[0], corr[2])),
                      FadeIn(mark(True).scale(1.6).move_to([4.6, 1.0, 0])), run_time=0.6)
        # e3: failure needs about L/2 errors in a row, so that error + correction wraps around
        with self.voice("e3"):
            self.play(*[FadeOut(m) for m in self.stage() if m is not g], run_time=0.4)
            bad = VGroup(*[lat.edge(("h", 2, c), Z_COL) for c in range(3)])
            fix = VGroup(*[lat.edge(("h", 2, c), HILITE) for c in range(3, 6)])
            self.play(LaggedStart(*[Create(e) for e in bad], lag_ratio=0.4), run_time=1.0)
            d1, d2 = self.fire(lat.v(0, 2)), self.fire(lat.v(3, 2))
            self.play(FadeIn(d1), FadeIn(d2), run_time=0.3)
            self.hold(1.0)
            self.play(LaggedStart(*[Create(e) for e in fix], lag_ratio=0.4), run_time=1.0)
            self.play(FadeOut(d1), FadeOut(d2), VGroup(bad, fix).animate.set_stroke(HILITE, width=10), run_time=0.6)
            lab = VGroup(M(r"\approx L/2", size=38), mark(False)).arrange(RIGHT, buff=0.25).move_to([4.6, 1.0, 0])
            self.play(FadeIn(lab), run_time=0.5)
        # e4: matching, polynomial time
        with self.voice("e4"):
            self.play(*[FadeOut(m) for m in self.stage()], run_time=0.5)
            P = [np.array(p) for p in ([-3, 1.2, 0], [-1.4, 1.8, 0], [-2.2, -0.6, 0], [0.2, 0.2, 0], [1.6, 1.4, 0], [1.2, -1.2, 0])]
            pts = VGroup(*[Dot(p, radius=0.12, color=ACCENT) for p in P])
            allp = VGroup(*[Line(P[i], P[j], color=DIM, stroke_width=1.5) for i in range(6) for j in range(i + 1, 6)])
            match = VGroup(*[Line(P[i], P[j], color=HILITE, stroke_width=5) for i, j in ((0, 1), (2, 3), (4, 5))])
            self.play(FadeIn(pts), Create(allp), run_time=0.8)
            self.hold(0.8)
            self.play(Create(match), run_time=0.8)
            t = VGroup(T("minimum-weight matching", size=26), T("polynomial time", size=22, color=MUTED)).arrange(DOWN, buff=0.12)
            t.move_to([4.3, 0.3, 0])
            self.play(FadeIn(t), run_time=0.5)
        # e5: cut the doughnut open (flat icon) into a flat patch with two kinds of boundary
        with self.voice("e5"):
            self.play(*[FadeOut(m) for m in self.stage()], run_time=0.5)
            icon = self.donut([-0.6, 0.2], w=3.2, h=1.9)
            self.play(Create(icon[:3]), run_time=0.8)
            self.hold(0.8)
            cuts = VGroup(icon.around.copy().set_stroke(HILITE, opacity=1, width=3),
                          icon.through.copy().set_stroke(HILITE, opacity=1, width=3))
            self.play(Create(cuts[1]), run_time=0.5)
            self.play(Create(cuts[0]), run_time=0.6)
            self.hold(0.4)
            pl = Lat(L=5, s=0.62, centre=(-0.6, 0.0))
            pg = VGroup(*[Line(pl.v(0, k), pl.v(4, k), color=MUTED, stroke_width=2) for k in range(5)] +
                        [Line(pl.v(k, 0), pl.v(k, 4), color=MUTED, stroke_width=2) for k in range(5)])
            lr = VGroup(Line(pl.v(0, 0), pl.v(0, 4), color=X_COL, stroke_width=6), Line(pl.v(4, 0), pl.v(4, 4), color=X_COL, stroke_width=6))
            tb = VGroup(Line(pl.v(0, 0), pl.v(4, 0), color=Z_COL, stroke_width=6), Line(pl.v(0, 4), pl.v(4, 4), color=Z_COL, stroke_width=6))
            self.play(ReplacementTransform(VGroup(icon[:3], cuts), pg), run_time=1.0)
            self.play(Create(lr), Create(tb), run_time=0.7)
            br = Brace(VGroup(Dot(pl.v(0, 4)), Dot(pl.v(4, 4))), DOWN, color=MUTED, buff=0.15)
            bd = M("d", size=30, color=MUTED).next_to(br, DOWN, buff=0.08)
            info = VGroup(T("1 logical qubit", size=26), M(r"\approx d^2 \text{ data qubits}", size=32)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            info.move_to([4.2, 0.4, 0])
            self.play(GrowFromCenter(br), FadeIn(bd), FadeIn(info), run_time=0.6)
        self.clear_stage()

    # ------------------------------------------------------------ F. closing
    def closing(self):
        self.clear_stage()
        panels = VGroup()
        for k in range(3):
            lt = Lat(L=4, s=0.42, centre=(-4.2 + 3.6 * k, 0.4))
            gl = lt.lines(width=1.5)
            if k == 0:
                extra = VGroup(self.chain([(1, 1), (1, 2), (2, 2)], lat=lt), self.fire(lt.v(1, 1), 0.08), self.fire(lt.v(2, 2), 0.08))
                lab = T("only the ends", size=20)
            elif k == 1:
                extra = VGroup(self.chain([(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)], lat=lt), mark(True).set_opacity(0))
                lab = VGroup(T("loop: harmless", size=20), mark(True)).arrange(RIGHT, buff=0.12)
            else:
                extra = VGroup(VGroup(*[lt.edge(("h", 2, c), Z_COL) for c in range(4)]), mark(False).set_opacity(0))
                lab = VGroup(T("around: logical", size=20), mark(False)).arrange(RIGHT, buff=0.12)
            lab.next_to(gl, DOWN, buff=0.25)
            panels.add(VGroup(gl, extra, lab))
        with self.voice("f1"):
            for p in panels:
                self.play(FadeIn(p), run_time=0.6)
                self.hold(0.8)
            self.play(panels[2][:2].animate.scale(1.35), run_time=1.0)
        circ = self.circ_shape.copy().move_to([0, -0.2, 0]).scale(1.3) if hasattr(self, "circ_shape") else \
            Circuit(["1", "2", "3", "4"], 1, [("cnot", k, 4) for k in range(4)], gap=0.36, step=0.42, lead=0.5, size=0.26).scale(1.3)
        with self.voice("f2"):
            self.play(FadeOut(panels), run_time=0.4)
            self.play(FadeIn(circ), run_time=0.5)
            self.play(circ.cols[2].animate.set_color(ACCENT), run_time=0.4)
            self.play(Indicate(circ.cols[2], color=ACCENT, scale_factor=1.3), run_time=0.6)
        nxt = VGroup(T("Next", size=26, color=MUTED), T("8.6  Thresholds", size=48, bold=True)).arrange(DOWN, buff=0.3)
        nxt.move_to([0, 1.0, 0])
        ln = Line([-3, -1.0, 0], [3, -1.0, 0], color=MUTED, stroke_width=2)
        tick = Line([0, -1.2, 0], [0, -0.8, 0], color=HILITE, stroke_width=4)
        h1 = T("helps", size=24, color=INK).move_to([-1.6, -1.45, 0])
        h2 = T("hurts", size=24, color=MUTED).move_to([1.6, -1.45, 0])
        with self.voice("f3"):
            self.hold(1.6)
            self.play(FadeOut(circ), run_time=0.5)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
            self.play(Create(ln), FadeIn(tick), FadeIn(h1), FadeIn(h2), run_time=0.7)
