"""Section 8.4 — CSS codes.   Draft.
Build from the video folder with the Manim environment:
    python pipeline/build.py 8.4 render --low        (ONLY=<letters> renders chosen scenes)
Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.
Colours as in 8.1 to 8.3: a purple tile is X (and every row of H_X), a green tile is Z (and
every row of H_Z), a tile split purple and green is Y, a dark tile the identity. In a table of
bits, 1 is white and 0 is dark. Orange is a minus sign, "odd", a 1 in a syndrome or a non-zero
entry of a product. Cyan marks what to look at.
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from common import *  # noqa: E402,F401

DROP = 0.4
X_TILE, Z_TILE = PAULI_X, PAULI_Z
HAM = ["0001111", "0110011", "1010101"]           # the Hamming table: columns are 1..7 in binary
BITFLIP = ["110", "011"]                          # the bit flip code's table


def tile(ch, s=0.5):
    """One letter of a Pauli string (as in 8.3). Y is split purple / green."""
    if ch == "Y":
        a = Polygon([-s / 2, s / 2, 0], [s / 2, s / 2, 0], [-s / 2, -s / 2, 0], stroke_width=0,
                    fill_color=X_TILE, fill_opacity=1)
        b = Polygon([s / 2, s / 2, 0], [s / 2, -s / 2, 0], [-s / 2, -s / 2, 0], stroke_width=0,
                    fill_color=Z_TILE, fill_opacity=1)
        g = VGroup(VGroup(a, b), T("Y", size=int(68 * s), color=INK, bold=True))
        g.ch = "Y"
        return g
    col = {"X": X_TILE, "Z": Z_TILE, "I": DIM}[ch]
    box = RoundedRectangle(width=s, height=s, corner_radius=0.12 * s, stroke_width=0, fill_color=col,
                           fill_opacity=1)
    g = VGroup(box)
    if ch == "I":
        g.add(Dot(box.get_center(), radius=0.075 * s, color=MUTED))
    else:
        g.add(T(ch, size=int(68 * s), color=BG if ch == "Z" else INK, bold=True).move_to(box))
    g.ch = ch
    return g


def pstring(letters, s=0.5, step=None):
    step = s * 1.14 if step is None else step
    g = VGroup(*[tile(c, s).move_to([k * step, 0, 0]) for k, c in enumerate(letters)])
    return g.move_to(ORIGIN)


def as_paulis(bits, letter):
    return "".join(letter if b == "1" else "I" for b in bits)


def lamp(kind, r=0.15):
    if kind == "-":
        return Circle(radius=r, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
    if kind == "?":
        return VGroup(Circle(radius=r, color=MUTED, stroke_width=3), T("?", size=int(110 * r), color=MUTED))
    return Circle(radius=r, color=INK, stroke_width=3)


def bitmat(rows, step=0.42, size=26):
    """A table of bits: 1 white, 0 dark. m[i][j] is row i, column j."""
    m = VGroup()
    for i, r in enumerate(rows):
        m.add(VGroup(*[T(b, size=size, color=INK if b == "1" else DIM, bold=True).move_to([j * step, -i * step, 0])
                       for j, b in enumerate(r)]))
    return m.move_to(ORIGIN)


def qdot(label, r=0.2, color=MUTED):
    c = Circle(radius=r, color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(c, T(str(label), size=int(80 * r), color=INK).move_to(c))


def overlap(a, b):
    return sum(x == "1" and y == "1" for x, y in zip(a, b))


class Main(NarratedScene):
    EP = "8.4"
    SCENES = [("i", "opening"), ("a", "hook"), ("b", "classical"), ("c", "condition"), ("d", "decoders"),
              ("e", "steane"), ("f", "closing")]
    BADGE = np.array([5.05, 2.85, 0])

    def construct(self):
        only = os.environ.get("ONLY", "")
        self.busy = {}
        self.head = header("8.4  CSS codes")
        self.wm = watermark()
        self.badge = None
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter != "i" and self.head not in self.mobjects:
                self.camera.frame_center = np.array([0.0, DROP, 0.0])
                self.head.shift(UP * DROP)
                self.wm.shift(UP * DROP)
                self.play(FadeIn(self.head), FadeIn(self.wm), run_time=0.4)
            if letter not in "ia" and self.badge is None:        # a scene rendered on its own
                self.badge = self.make_badge().scale(0.72).move_to(self.BADGE)
                if letter in "def":
                    self.fill_slot(animate=False)
                self.add(self.badge)
            getattr(self, name)()
        self.save_marks()
        (out_dir(self.EP) / "busy.json").write_text(json.dumps(self.busy, indent=1), encoding="utf-8")

    @contextmanager
    def voice(self, *ids, gap=None):
        words = sum(len(self.subs[i].split()) for i in ids)
        real = sum(self.durs[i] for i in ids) if all(i in self.durs for i in ids) else None
        self.pace = real / (words / 150 * 60) if real else 1.0
        with super().voice(*ids, gap=gap) as total:
            t0 = self.now
            yield total
            self.busy[ids[-1]] = {"busy": round(self.now - t0, 2), "voice": round(total, 2),
                                  "at_219_wpm": round(words / 219 * 60, 2)}
        self.pace = 1.0

    def hold(self, seconds):
        super().hold(seconds * getattr(self, "pace", 1.0))

    def keep(self):
        return [self.head, self.wm, self.badge]

    def stage(self):
        return [m for m in self.mobjects if m not in self.keep()]

    def clear_stage(self, run_time=0.6):
        left = self.stage()
        if left:
            self.play(*[FadeOut(m) for m in left], run_time=run_time)

    def gone(self, *mobs):
        """Take loose pieces off the stage at once (pieces animated one by one sit there separately)."""
        fam = set()
        for m in mobs:
            fam |= set(m.get_family())
        self.remove(*[m for m in self.mobjects if m in fam])

    # ------------------------------------------------------------ shared pieces
    def make_badge(self):
        """Two slots: a good classical code (ticked from the start), and the missing half."""
        s1 = VGroup(T("a good classical code", size=22), mark(True)).arrange(RIGHT, buff=0.18)
        q = T("?", size=30, color=HILITE, bold=True)
        s2 = VGroup(q)
        box1 = RoundedRectangle(width=4.0, height=0.62, corner_radius=0.12, color=MUTED, stroke_width=1.6)
        box2 = DashedVMobject(RoundedRectangle(width=4.0, height=0.62, corner_radius=0.12, color=HILITE,
                                               stroke_width=1.6), num_dashes=30)
        g = VGroup(VGroup(box1, s1.move_to(box1)), VGroup(box2, s2.move_to(box2))).arrange(DOWN, buff=0.14)
        g.slot2 = g[1]
        return g

    def fill_slot(self, animate=True):
        content = VGroup(M(r"H_X H_Z^{\mathsf T} = 0", size=30), mark(True)).arrange(RIGHT, buff=0.18)
        content.move_to(self.badge.slot2[0]).scale_to_fit_height(self.badge.slot2[0].height * 0.62)
        solid = RoundedRectangle(width=self.badge.slot2[0].width, height=self.badge.slot2[0].height,
                                 corner_radius=0.09, color=MUTED, stroke_width=1.6).move_to(self.badge.slot2[0])
        new = VGroup(solid, content)
        if animate:
            self.play(Transform(self.badge.slot2, new), run_time=0.7)
        else:
            self.badge.slot2.become(new)

    def venn(self, centre, R=0.75):
        k = R / 85.0
        circ = {1: (180, 130), 2: (135, 205), 3: (225, 205)}
        qub = {4: (180, 85), 6: (128, 155), 5: (232, 155), 7: (180, 180), 2: (90, 240), 3: (180, 237), 1: (270, 240)}
        to = lambda p: np.array(centre) + np.array([(p[0] - 180) * k, -(p[1] - 180) * k, 0])
        circles = {i: Circle(radius=R, color=MUTED, stroke_width=2, fill_color=MUTED, fill_opacity=0.05).move_to(to(p))
                   for i, p in circ.items()}
        dots = {j: qdot(j, r=0.13).move_to(to(p)) for j, p in qub.items()}
        g = VGroup(*circles.values(), *dots.values())
        g.circles, g.dots = circles, dots
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
        title = T("CSS codes", size=50, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 8  ·  Section 8.4", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark_.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark_, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    # ------------------------------------------------------------ A. does the recipe always work?
    def hook(self):
        self.clear_stage()
        S = 0.34
        xs = [pstring(as_paulis(r, "X"), s=S) for r in HAM]
        zs = [pstring(as_paulis(r, "Z"), s=S) for r in HAM]
        checks = VGroup(*xs, *zs).arrange(DOWN, buff=0.1).move_to([-3.3, 0.3, 0])
        checks[3:].shift(DOWN * 0.15)
        tbl = bitmat(HAM).move_to([2.6, 0.3, 0])
        tlab = M("H", size=36, color=MUTED).next_to(tbl, LEFT, buff=0.35)
        ax = Arrow(VGroup(*checks[:3]).get_right(), tbl.get_left() + LEFT * 0.55 + UP * 0.2, buff=0.25,
                   color=X_TILE, stroke_width=3)
        az = Arrow(VGroup(*checks[3:]).get_right(), tbl.get_left() + LEFT * 0.55 + DOWN * 0.2, buff=0.25,
                   color=Z_TILE, stroke_width=3)
        cards = VGroup(pill("Shor  [[9,1,3]]", color=MUTED, size=20), pill("Steane  [[7,1,3]]", color=MUTED, size=20))
        cards.arrange(RIGHT, buff=0.2).to_corner(DL, buff=0.35).shift(UP * (DROP + 0.25))
        # a1: Steane's six checks: two halves, one table
        with self.voice("a1"):
            self.play(FadeIn(cards, shift=UP * 0.2), run_time=0.6)
            self.hold(1.6)
            self.play(TransformFromCopy(cards[1], checks), run_time=1.0)
            self.hold(2.0)
            self.play(Indicate(VGroup(*checks[:3]), color=X_TILE, scale_factor=1.05), run_time=0.6)
            self.play(Indicate(VGroup(*checks[3:]), color=Z_TILE, scale_factor=1.05), run_time=0.6)
            self.hold(0.8)
            self.play(FadeIn(tbl), FadeIn(tlab), GrowArrow(ax), GrowArrow(az), run_time=0.9)
        # a2: the Hamming code, older than quantum computing
        msg = self.message("0110011", y=-1.35, x0=0.0)
        cap = T("Hamming code  ·  1950", size=24, color=MUTED)
        with self.voice("a2"):
            self.play(FadeOut(VGroup(checks, ax, az, cards)), run_time=0.6)
            self.play(VGroup(tbl, tlab).animate.move_to([0, 1.1, 0]), run_time=0.7)
            cap.next_to(VGroup(tbl, tlab), UP, buff=0.35)
            self.play(FadeIn(cap), run_time=0.5)
            self.hold(1.4)
            self.play(FadeIn(msg), run_time=0.6)
            fx = tile("X", 0.32).next_to(msg.cells[4], UP, buff=0.15)
            self.play(FadeIn(fx, shift=DOWN * 0.2), run_time=0.4)
            self.flip_bit(msg, 4)
            self.hold(1.0)
            self.flip_bit(msg, 4)
            self.play(FadeOut(fx), run_time=0.3)
        # a3: the recipe: X copy and Z copy of one table; does it always work?
        xv = VGroup(*[pstring(as_paulis(r, "X"), s=0.34) for r in HAM]).arrange(DOWN, buff=0.1).move_to([-3.4, 1.0, 0])
        zv = VGroup(*[pstring(as_paulis(r, "Z"), s=0.34) for r in HAM]).arrange(DOWN, buff=0.1).move_to([-3.4, -1.1, 0])
        goal = VGroup(T("quantum code", size=30), T("?", size=40, color=HILITE, bold=True)).arrange(RIGHT, buff=0.2)
        goal.move_to([3.0, 0.0, 0])
        a_x = Arrow(xv.get_right(), goal.get_left(), buff=0.3, color=MUTED, stroke_width=3)
        a_z = Arrow(zv.get_right(), goal.get_left(), buff=0.3, color=MUTED, stroke_width=3)
        with self.voice("a3"):
            self.play(FadeOut(VGroup(msg, cap)), run_time=0.4)
            self.hold(1.0)
            self.play(TransformFromCopy(tbl, xv), run_time=0.9)
            self.play(TransformFromCopy(tbl, zv), FadeOut(VGroup(tbl, tlab)), run_time=0.9)
            self.hold(1.0)
            self.play(GrowArrow(a_x), GrowArrow(a_z), FadeIn(goal[0]), run_time=0.7)
            self.play(FadeIn(goal[1], scale=1.5), run_time=0.4)
        # a4: her reasons
        lz = T("catches bit flips", size=20, color=MUTED).next_to(zv, DOWN, buff=0.2)
        lx = T("catches phase flips", size=20, color=MUTED).next_to(xv, UP, buff=0.2)
        with self.voice("a4"):
            self.hold(0.6)
            self.play(FadeIn(lz), run_time=0.5)
            self.hold(0.8)
            self.play(FadeIn(lx), run_time=0.5)
        # a5: half of the answer: the badge goes up and stays
        b = self.make_badge().move_to([3.0, -1.6, 0])
        with self.voice("a5"):
            self.play(FadeIn(b[0]), run_time=0.5)
            self.hold(1.8)
            self.play(Create(b[1][0]), FadeIn(b[1][1]), run_time=0.7)
            self.hold(1.6)
            self.play(b.animate.scale(0.72).move_to(self.BADGE), run_time=0.8)
        self.badge = b
        self.clear_stage()

    # helpers for messages of bits
    def message(self, bits, y, x0=0.0, step=0.42, s=0.38):
        cells = VGroup(*[Square(s, color=MUTED, stroke_width=2) for _ in bits])
        for j, c in enumerate(cells):
            c.move_to([x0 + (j - (len(bits) - 1) / 2) * step, y, 0])
        digits = VGroup(*[T(b, size=24, color=INK, bold=True).move_to(c) for b, c in zip(bits, cells)])
        g = VGroup(cells, digits)
        g.cells, g.digits, g.bits = cells, digits, list(bits)
        return g

    def flip_bit(self, msg, j, run_time=0.4):
        msg.bits[j] = "1" if msg.bits[j] == "0" else "0"
        new = T(msg.bits[j], size=24, color=INK, bold=True).move_to(msg.cells[j])
        self.play(Transform(msg.digits[j], new), Indicate(msg.cells[j], color=HILITE), run_time=run_time)

    # ------------------------------------------------------------ B. what the table does classically
    def classical(self):
        self.clear_stage()
        step = 0.6
        tbl = bitmat(HAM, step=step, size=30).move_to([-0.6, 1.75, 0])
        tlab = M("H", size=36, color=MUTED).next_to(tbl, LEFT, buff=0.4)
        colx = [tbl[0][j].get_center()[0] for j in range(7)]
        msg = self.message("0110011", y=-0.05, x0=float(np.mean(colx)), step=step, s=0.46)
        mlab = T("message", size=20, color=MUTED).next_to(msg, LEFT, buff=0.35)
        res = [None, None, None]

        def check_row(r, run_time=0.5):
            ones = [j for j in range(7) if HAM[r][j] == "1"]
            fr = VGroup(*[SurroundingRectangle(msg.cells[j], color=HILITE, buff=0.04) for j in ones])
            n = sum(int(msg.bits[j]) for j in ones)
            lab = T(f"{n}  {'even' if n % 2 == 0 else 'odd'}", size=24,
                    color=INK if n % 2 == 0 else ACCENT).next_to(tbl[r], RIGHT, buff=0.55)
            self.play(*[tbl[r][j].animate.set_color(HILITE) for j in ones], Create(fr), run_time=run_time)
            if res[r] is None:
                self.play(FadeIn(lab), run_time=0.3)
                res[r] = lab
            else:
                self.play(Transform(res[r], lab), run_time=0.3)
            self.play(*[tbl[r][j].animate.set_color(INK) for j in ones], FadeOut(fr), run_time=0.3)
        # b1: one row asks one parity question
        with self.voice("b1"):
            self.play(FadeIn(tbl), FadeIn(tlab), run_time=0.6)
            self.play(FadeIn(msg), FadeIn(mlab), run_time=0.6)
            self.hold(1.8)
            check_row(0, run_time=0.8)
        # b2: all three rows say even: the message passes; the code is the kernel
        ok = VGroup(T("passes", size=22, color=INK), mark(True)).arrange(RIGHT, buff=0.15).next_to(msg, RIGHT, buff=0.45)
        words = ["1110000", "1001100", "0000000"]
        others = VGroup(*[self.message(w, y=0, step=0.3, s=0.26) for w in words]).arrange(RIGHT, buff=0.5)
        for o in others:
            o.add(mark(True, size=0.12).next_to(o, RIGHT, buff=0.12))
        box = SurroundingRectangle(others, color=MUTED, buff=0.25, corner_radius=0.15, stroke_width=1.6)
        code = VGroup(others, box).move_to([-0.6, -1.45, 0])
        ker = M(r"\text{the code} = \ker H \pmod 2", size=30).next_to(box, DOWN, buff=0.2)
        with self.voice("b2"):
            check_row(1)
            check_row(2)
            self.play(FadeIn(ok), run_time=0.4)
            self.hold(1.0)
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.2) for o in others], lag_ratio=0.3), Create(box), run_time=1.2)
            self.hold(1.4)
            self.play(FadeIn(ker), run_time=0.6)
        # b3: flip bit 5: rows 1 and 3 say odd, and that is column 5
        fx = tile("X", 0.36).next_to(msg.cells[4], UP, buff=0.12)
        with self.voice("b3"):
            self.play(FadeOut(VGroup(code, ker, ok)), run_time=0.5)
            self.play(FadeIn(fx, shift=DOWN * 0.2), run_time=0.4)
            self.flip_bit(msg, 4)
            for r in range(3):
                check_row(r, run_time=0.4)
            lamps = VGroup(*[lamp("-" if HAM[r][4] == "1" else "+", r=0.14).next_to(res[r], RIGHT, buff=0.35)
                             for r in range(3)])
            self.play(FadeIn(lamps), run_time=0.4)
            self.hold(0.6)
            col5 = SurroundingRectangle(VGroup(*[tbl[r][4] for r in range(3)]), color=HILITE, buff=0.08)
            self.play(Create(col5), Indicate(lamps, color=ACCENT, scale_factor=1.3), run_time=0.8)
        # b4: Steane's address trick
        v = self.venn([4.9, -1.5, 0], R=0.62)
        with self.voice("b4"):
            self.play(FadeIn(v), run_time=0.5)
            self.play(v.circles[1].animate.set_stroke(ACCENT, width=3.5), v.circles[3].animate.set_stroke(ACCENT, width=3.5),
                      v.dots[5][0].animate.set_stroke(HILITE, width=4), run_time=0.5)
        # b5: nothing quantum here
        cl = pill("classical", color=MUTED, size=22).move_to([-5.4, 2.45, 0])
        with self.voice("b5"):
            self.play(FadeOut(v), run_time=0.5)
            self.hold(2.4)
            self.play(FadeIn(cl, shift=DOWN * 0.15), run_time=0.5)
            self.hold(2.5)
        self.clear_stage()

    # ------------------------------------------------------------ C. two tables, one condition
    def condition(self):
        self.clear_stage()
        HX = ["110011", "011110"]
        HZ = ["111100", "001111"]
        tx = bitmat(HX, step=0.45).move_to([-3.4, 1.0, 0])
        tz = bitmat(HZ, step=0.45).move_to([2.6, 1.0, 0])
        lx = M("H_X", size=36, color=X_TILE).next_to(tx, LEFT, buff=0.35)
        lz = M("H_Z", size=36, color=Z_TILE).next_to(tz, LEFT, buff=0.35)
        sx = VGroup(*[pstring(as_paulis(r, "X"), s=0.38, step=0.45) for r in HX])
        sz = VGroup(*[pstring(as_paulis(r, "Z"), s=0.38, step=0.45) for r in HZ])
        for s_, row in zip(sx, tx):
            s_.move_to(row)
        for s_, row in zip(sz, tz):
            s_.move_to(row)
        # c1: two tables, rows become X checks and Z checks
        with self.voice("c1"):
            self.hold(1.0)
            self.play(FadeIn(tx), FadeIn(lx), run_time=0.6)
            self.play(FadeIn(tz), FadeIn(lz), run_time=0.6)
            self.hold(2.0)
            self.play(*[ReplacementTransform(r, s_) for r, s_ in zip(tx, sx)], run_time=0.9)
            self.play(*[ReplacementTransform(r, s_) for r, s_ in zip(tz, sz)], run_time=0.9)
        # c2: same letters always commute; only X against Z is in question
        def link(a, b, ok=None, bend=0.0):
            ln = Line(a, b, color=MUTED, stroke_width=2)
            if ok is None:
                lab = T("?", size=26, color=HILITE, bold=True)
            else:
                lab = mark(True)
            return VGroup(ln, lab.move_to(ln.get_center() + bend * RIGHT))
        with self.voice("c2"):
            self.play(sx[0].animate.move_to([-3.0, 0.9, 0]), sx[1].animate.move_to([-3.0, -1.2, 0]),
                      sz[0].animate.move_to([2.4, 0.9, 0]), sz[1].animate.move_to([2.4, -1.2, 0]),
                      lx.animate.move_to([-5.3, -0.15, 0]), lz.animate.move_to([4.7, -0.15, 0]), run_time=0.8)
            xx = link(sx[0].get_bottom() + DOWN * 0.08, sx[1].get_top() + UP * 0.08, ok=True, bend=-0.3)
            zz = link(sz[0].get_bottom() + DOWN * 0.08, sz[1].get_top() + UP * 0.08, ok=True, bend=0.3)
            self.play(Create(xx), run_time=0.5)
            self.play(Create(zz), run_time=0.5)
            self.hold(2.0)
            cross = VGroup(*[link(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1) for a in sx for b in sz])
            for c, (k, l) in zip(cross, [(0, 0), (0, 1), (1, 0), (1, 1)]):
                c[1].move_to(c[0].point_from_proportion(0.3 + 0.4 * ((k + l) % 2)))
            self.play(LaggedStart(*[Create(c) for c in cross], lag_ratio=0.15), run_time=1.0)
        # c3: one X row against one Z row (the lecture's figure): two clashes cancel
        with self.voice("c3"):
            self.clear_stage(run_time=0.5)
            self.overlap_pair("1010101", "0110011", y=0.5, show_nums=True)
        # c4: the recipe on the bit flip code (thinking pause)
        bf = bitmat(BITFLIP, step=0.5).move_to([0, 2.0, 0])
        bxs = VGroup(*[pstring(as_paulis(r, "X"), s=0.42, step=0.5) for r in BITFLIP]).arrange(DOWN, buff=0.12).move_to([-3.3, 1.9, 0])
        bzs = VGroup(*[pstring(as_paulis(r, "Z"), s=0.42, step=0.5) for r in BITFLIP]).arrange(DOWN, buff=0.12).move_to([3.3, 1.9, 0])
        with self.voice("c4"):
            self.clear_stage(run_time=0.5)
            self.play(FadeIn(bf), run_time=0.5)
            self.hold(1.8)
            self.play(TransformFromCopy(bf, bxs), TransformFromCopy(bf, bzs), run_time=0.9)
            self.hold(0.6)
            top = bxs[0].copy()
            bot = bzs[1].copy()
            self.play(top.animate.move_to([0, 0.3, 0]), bot.animate.move_to([0, -0.3, 0]), run_time=0.8)
            q = T("?", size=36, color=HILITE, bold=True).next_to(VGroup(top, bot), RIGHT, buff=0.4)
            self.play(FadeIn(q), run_time=0.3)
        # c5: she counts: qubit two only
        fr = SurroundingRectangle(VGroup(top[1], bot[1]), color=HILITE, buff=0.06)
        with self.voice("c5"):
            self.play(Create(fr), run_time=0.5)
            self.play(Transform(q, M("1", size=40, color=HILITE).move_to(q)), run_time=0.4)
        # c6: one minus sign, nothing to cancel it: they anticommute
        with self.voice("c6"):
            mi = M("-", size=96, color=ACCENT).next_to(fr, UP, buff=0.05)
            self.play(FadeIn(mi, scale=1.6), run_time=0.5)
            verdict = VGroup(T("odd", size=26, color=ACCENT), mark(False)).arrange(RIGHT, buff=0.2).next_to(q, RIGHT, buff=0.4)
            self.play(FadeIn(verdict), run_time=0.4)
            self.hold(2.0)
            self.play(Indicate(self.badge.slot2, color=HILITE, scale_factor=1.08), run_time=0.8)
        # c7: all overlaps in one product; the condition
        with self.voice("c7"):
            self.play(FadeOut(VGroup(top, bot, fr, q, mi, verdict, bf)), run_time=0.5)
            self.hold(1.2)
            grid = self.overlap_grid(bxs, bzs)
            self.hold(1.0)
            cond = M(r"H_X\,H_Z^{\mathsf T} = 0 \pmod 2", size=44).move_to([0, -2.1, 0])
            self.play(TransformFromCopy(grid, cond), run_time=1.0)
            self.fill_slot()
        # c8: the logical qubits left: n minus the independent checks of each kind
        with self.voice("c8"):
            self.play(FadeOut(VGroup(grid, bxs, bzs)), cond.animate.scale(0.75).move_to([-3.4, 2.2, 0]), run_time=0.7)
            self.halving()
        self.clear_stage()

    def overlap_pair(self, xbits, zbits, y=0.4, show_nums=False):
        """An X row over a Z row; the shared columns throw minus signs, which cancel in pairs."""
        step = 0.62
        xs = pstring(as_paulis(xbits, "X"), s=0.52, step=step).move_to([0, y + 0.35, 0])
        zs = pstring(as_paulis(zbits, "Z"), s=0.52, step=step).move_to([0, y - 0.35, 0])
        nums = VGroup(*[T(str(j + 1), size=20, color=MUTED).next_to(xs[j], UP, buff=0.18) for j in range(len(xbits))])
        lx = T("X-type check", size=20, color=MUTED).next_to(xs, LEFT, buff=0.4)
        lz = T("Z-type check", size=20, color=MUTED).next_to(zs, LEFT, buff=0.4)
        self.play(FadeIn(xs), FadeIn(zs), FadeIn(lx), FadeIn(lz), FadeIn(nums), run_time=0.7)
        self.hold(1.0)
        both = [j for j in range(len(xbits)) if xbits[j] == "1" and zbits[j] == "1"]
        frs = VGroup(*[SurroundingRectangle(VGroup(xs[j], zs[j]), color=HILITE, buff=0.06) for j in both])
        self.play(Create(frs), run_time=0.6)
        sparks = VGroup(*[M("-", size=54, color=ACCENT).next_to(f, DOWN, buff=0.12) for f in frs])
        self.play(FadeIn(sparks, scale=1.6), run_time=0.5)
        mid = (sparks[0].get_center() + sparks[-1].get_center()) / 2
        self.play(*[s.animate.move_to(mid) for s in sparks], run_time=0.7)
        self.play(FadeOut(sparks, scale=0.3), Flash(mid, color=ACCENT), run_time=0.5)
        v = VGroup(T(f"{len(both)}  even", size=26), mark(True)).arrange(RIGHT, buff=0.2).next_to(VGroup(xs, zs), RIGHT, buff=0.5)
        self.play(FadeIn(v), run_time=0.4)
        return VGroup(xs, zs, nums, lx, lz, frs, v)

    def overlap_grid(self, bxs, bzs):
        """Rows of H_X down the side, rows of H_Z across the top, overlap mod 2 in each cell."""
        cw, ch = 1.25, 0.85
        x0, y0 = 0.4, 0.15                       # centre of the top-left cell
        self.play(bxs[0].animate.scale(0.8).move_to([x0 - 1.45, y0, 0]),
                  bxs[1].animate.scale(0.8).move_to([x0 - 1.45, y0 - ch, 0]),
                  bzs[0].animate.scale(0.8).move_to([x0, y0 + 0.85, 0]),
                  bzs[1].animate.scale(0.8).move_to([x0 + cw, y0 + 0.85, 0]), run_time=0.8)
        cells = VGroup()
        pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i, j in pairs:
            box = Rectangle(width=cw, height=ch, color=MUTED, stroke_width=1.6).move_to([x0 + j * cw, y0 - i * ch, 0])
            t = M(str(overlap(BITFLIP[i], BITFLIP[j])), size=34, color=INK).move_to(box)
            cells.add(VGroup(box, t))
        self.play(LaggedStart(*[Create(c[0]) for c in cells], lag_ratio=0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c[1]) for c in cells], lag_ratio=0.3), run_time=1.0)
        self.hold(0.6)
        anims = []
        for c, (i, j) in zip(cells, pairs):
            v = overlap(BITFLIP[i], BITFLIP[j]) % 2
            anims.append(Transform(c[1], M(str(v), size=34, color=ACCENT if v else INK).move_to(c[0])))
        self.play(*anims, run_time=0.6)
        bad = VGroup(*[c[0] for c, (i, j) in zip(cells, pairs) if overlap(BITFLIP[i], BITFLIP[j]) % 2])
        self.play(bad.animate.set_stroke(ACCENT, width=3), run_time=0.4)
        return cells

    def halving(self):
        """2^n, halved once per independent check: three X checks, then two Z checks, leaves 2^k."""
        start = M("2^n", size=44).move_to([-4.3, 0.2, 0])
        self.play(FadeIn(start), run_time=0.5)
        self.hold(0.8)
        cuts = VGroup()
        for k, ch in enumerate("XXXZZ"):
            g = VGroup(M(r"\div 2", size=30, color=MUTED), tile(ch, 0.36)).arrange(DOWN, buff=0.12)
            g.move_to([-3.0 + k * 1.05, 0.2, 0])
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=0.4)
            cuts.add(g)
        end = M("2^k", size=44, color=HILITE).move_to([2.6, 0.2, 0])
        self.play(FadeIn(end), run_time=0.4)
        rx = Brace(VGroup(*cuts[:3]), DOWN, color=X_TILE)
        rz = Brace(VGroup(*cuts[3:]), DOWN, color=Z_TILE)
        lrx = M(r"\operatorname{rank} H_X", size=28, color=X_TILE).next_to(rx, DOWN, buff=0.1)
        lrz = M(r"\operatorname{rank} H_Z", size=28, color=Z_TILE).next_to(rz, DOWN, buff=0.1)
        self.play(GrowFromCenter(rx), FadeIn(lrx), GrowFromCenter(rz), FadeIn(lrz), run_time=0.7)
        k = M(r"k = n - \operatorname{rank} H_X - \operatorname{rank} H_Z", size=40).move_to([-0.6, -2.05, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.6)

    # ------------------------------------------------------------ D. two kinds of error, two decoders
    def decoders(self):
        self.clear_stage()
        dots = VGroup(*[qdot(j + 1, r=0.2) for j in range(7)]).arrange(RIGHT, buff=0.42).move_to([-1.6, 0.25, 0])
        xl = VGroup(*[lamp("+", r=0.14) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        zl = VGroup(*[lamp("+", r=0.14) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        xg = VGroup(T("X checks", size=20, color=X_TILE), xl).arrange(RIGHT, buff=0.3).move_to([-1.6, 1.65, 0])
        zg = VGroup(T("Z checks", size=20, color=Z_TILE), zl).arrange(RIGHT, buff=0.3).move_to([-1.6, -1.15, 0])

        def dbox(label, y):
            t = VGroup(T("classical decoder", size=20), M(label, size=28)).arrange(DOWN, buff=0.08)
            b = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.15, color=MUTED, stroke_width=1.8)
            return VGroup(b, t.move_to(b)).move_to([4.5, y, 0])
        dx = dbox(r"\text{for } H_X", 1.65)
        dz = dbox(r"\text{for } H_Z", -1.15)

        def set_l(lamps, bits):
            self.play(*[Transform(l, lamp("-" if b == "1" else "+", r=0.14).move_to(l)) for l, b in zip(lamps, bits)],
                      run_time=0.4)

        def col(j):
            return "".join(HAM[r][j] for r in range(3))
        # d1: a bit flip trips only the Z checks
        with self.voice("d1"):
            self.play(FadeIn(dots), FadeIn(xg), FadeIn(zg), run_time=0.7)
            self.play(FadeIn(dx), FadeIn(dz), run_time=0.5)
            self.hold(1.8)
            e = tile("X", 0.34).next_to(dots[4], UP, buff=0.5)
            self.play(FadeIn(e, shift=DOWN * 0.3), run_time=0.4)
            self.play(e.animate.next_to(dots[4], UR, buff=0.0).scale(0.8), run_time=0.4)
            set_l(zl, col(4))
            arr = Arrow(zg.get_right(), dz.get_left(), buff=0.2, color=ACCENT, stroke_width=3)
            ez = M("H_Z\\, e", size=30).next_to(arr, DOWN, buff=0.1)
            self.play(GrowArrow(arr), FadeIn(ez), run_time=0.6)
            self.play(Indicate(dz, color=Z_TILE, scale_factor=1.05), FadeOut(e), run_time=0.7)
        # d2: a phase flip trips only the X checks
        with self.voice("d2"):
            self.play(FadeOut(arr), FadeOut(ez), run_time=0.3)
            set_l(zl, "000")
            e = tile("Z", 0.34).next_to(dots[2], UP, buff=0.5)
            self.play(FadeIn(e, shift=DOWN * 0.3), run_time=0.4)
            self.play(e.animate.next_to(dots[2], UR, buff=0.0).scale(0.8), run_time=0.4)
            set_l(xl, col(2))
            arr = Arrow(xg.get_right(), dx.get_left(), buff=0.2, color=ACCENT, stroke_width=3)
            ex = M("H_X\\, e'", size=30).next_to(arr, UP, buff=0.1)
            self.play(GrowArrow(arr), FadeIn(ex), run_time=0.6)
            self.play(Indicate(dx, color=X_TILE, scale_factor=1.05), FadeOut(e), run_time=0.7)
        # d3: a Y hovers (thinking pause)
        y = tile("Y", 0.4).next_to(dots[5], UP, buff=0.6)
        with self.voice("d3"):
            self.play(FadeOut(arr), FadeOut(ex), run_time=0.3)
            set_l(xl, "000")
            self.play(FadeIn(y, shift=DOWN * 0.3), run_time=0.5)
        # d4: both halves light; Y splits, each part goes to its own decoder
        with self.voice("d4"):
            self.play(y.animate.next_to(dots[5], UR, buff=0.0).scale(0.85), run_time=0.4)
            set_l(xl, col(5))
            set_l(zl, col(5))
            self.hold(0.8)
            xpart = tile("X", 0.3).move_to(y)
            zpart = tile("Z", 0.3).move_to(y)
            self.remove(y)
            self.add(xpart, zpart)
            self.play(xpart.animate.move_to(dz.get_center() + LEFT * 1.1), zpart.animate.move_to(dx.get_center() + LEFT * 1.1),
                      run_time=1.0)
            self.play(Indicate(dz, color=Z_TILE, scale_factor=1.05), Indicate(dx, color=X_TILE, scale_factor=1.05), run_time=0.7)
            self.play(FadeOut(xpart), FadeOut(zpart), run_time=0.4)
            set_l(xl, "000")
            set_l(zl, "000")
        # d5: two classical problems, no talking needed
        wall = Rectangle(width=3.2, height=0.14, stroke_width=0, fill_color=MUTED, fill_opacity=0.35).move_to([4.5, 0.25, 0])
        wl = T("no talking needed", size=20, color=MUTED).next_to(wall, DOWN, buff=0.12)
        with self.voice("d5"):
            self.hold(0.8)
            self.play(FadeIn(wall), FadeIn(wl), run_time=0.6)
            self.hold(1.5)
            self.play(Indicate(dx, color=INK, scale_factor=1.04), Indicate(dz, color=INK, scale_factor=1.04), run_time=0.8)
        self.clear_stage()

    # ------------------------------------------------------------ E. back to Steane
    def steane(self):
        self.clear_stage()
        H = bitmat(HAM, step=0.36, size=24).move_to([-3.9, 0.4, 0])
        HT = bitmat(["".join(HAM[r][j] for r in range(3)) for j in range(7)], step=0.36, size=24).move_to([-0.6, 0.4, 0])
        times = M(r"\times", size=40).move_to([(H.get_right()[0] + HT.get_left()[0]) / 2, 0.4, 0])
        eq = M("=", size=44).next_to(HT, RIGHT, buff=0.45)
        lh = M("H", size=30, color=MUTED).next_to(H, UP, buff=0.25)
        lht = M(r"H^{\mathsf T}", size=30, color=MUTED).next_to(HT, UP, buff=0.15)
        grid = VGroup()
        for i in range(3):
            for j in range(3):
                grid.add(Square(0.62, color=MUTED, stroke_width=1.6).move_to(eq.get_right() + [0.75 + j * 0.62, (1 - i) * 0.62, 0]))
        with self.voice("e1"):
            self.hold(1.4)
            self.play(FadeIn(H), FadeIn(lh), run_time=0.6)
            self.play(FadeIn(times), FadeIn(HT), FadeIn(lht), run_time=0.7)
            self.play(FadeIn(eq), LaggedStart(*[Create(g) for g in grid], lag_ratio=0.05), run_time=0.8)
        vals = VGroup()
        with self.voice("e2"):
            order = [(0, 0), (1, 1), (2, 2), (0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
            for k, (i, j) in enumerate(order):
                n = overlap(HAM[i], HAM[j])
                rt = 0.5 if k < 3 else 0.32
                self.play(H[i].animate.set_color(HILITE), *[HT[c][j].animate.set_color(HILITE) for c in range(7)],
                          run_time=rt * 0.5)
                t = M(str(n), size=30).move_to(grid[3 * i + j])
                self.play(FadeIn(t), run_time=rt * 0.5)
                self.play(H[i].animate.set_color(INK), *[HT[c][j].animate.set_color(INK) for c in range(7)], run_time=0.12)
                for r in range(3):
                    for c in range(7):
                        H[r][c].set_color(INK if HAM[r][c] == "1" else DIM)
                for c in range(7):
                    for r in range(3):
                        HT[c][r].set_color(INK if HAM[r][c] == "1" else DIM)
                vals.add(t)
            self.hold(0.4)
            self.play(*[Transform(t, M("0", size=30).move_to(t)) for t in vals], run_time=0.6)
            okm = mark(True, size=0.22).next_to(grid, RIGHT, buff=0.3)
            self.play(FadeIn(okm), run_time=0.3)
        steane = VGroup(H, HT, times, eq, lh, lht, grid, vals, okm)
        # e3: the bit flip table fails, the Hamming table passes
        bm = Matrix([[0, 1], [1, 0]], element_to_mobject=lambda v: M(str(v), size=34, color=ACCENT if v else INK),
                    v_buff=0.6, h_buff=0.6)
        bm.get_brackets().set_color(INK)
        bf = VGroup(T("bit flip", size=22, color=MUTED), bm, mark(False)).arrange(RIGHT, buff=0.3)
        st = VGroup(T("Hamming", size=22, color=MUTED),
                    Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]], element_to_mobject=lambda v: M(str(v), size=30),
                           v_buff=0.5, h_buff=0.5), mark(True)).arrange(RIGHT, buff=0.3)
        row = VGroup(bf, st).arrange(RIGHT, buff=1.4).move_to([0, -1.9, 0])
        with self.voice("e3"):
            self.play(steane.animate.scale(0.7).shift(UP * 0.75), run_time=0.6)
            self.play(FadeIn(bf, shift=UP * 0.2), FadeIn(st, shift=UP * 0.2), run_time=0.6)
        # e4: the code contains its dual
        big = RoundedRectangle(width=6.0, height=3.4, corner_radius=0.3, color=MUTED, stroke_width=2).move_to([0, 0.2, 0])
        small = RoundedRectangle(width=3.4, height=1.4, corner_radius=0.2, color=HILITE, stroke_width=2.5).move_to([0.9, -0.35, 0])
        lb = T("Hamming code", size=24).next_to(big.get_corner(UL), DR, buff=0.25)
        ls = VGroup(T("its dual", size=22, color=HILITE), T("(spanned by the rows of H)", size=16, color=MUTED)).arrange(DOWN, buff=0.06).move_to(small)
        cap = T("contains its dual", size=30, bold=True).next_to(big, DOWN, buff=0.3)
        with self.voice("e4"):
            self.play(FadeOut(VGroup(steane, row)), run_time=0.5)
            self.play(Create(big), FadeIn(lb), run_time=0.7)
            self.hold(1.2)
            self.play(Create(small), FadeIn(ls), run_time=0.7)
            self.hold(0.8)
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        self.clear_stage()

    # ------------------------------------------------------------ F. closing
    def closing(self):
        self.clear_stage()
        dots = VGroup(*[qdot(j + 1, r=0.2) for j in range(7)]).arrange(RIGHT, buff=0.42).move_to([-0.8, -0.3, 0])
        xs = [d.get_center()[0] for d in dots]
        top = VGroup(*[pstring(as_paulis(r, "X"), s=0.3, step=xs[1] - xs[0]) for r in HAM]).arrange(DOWN, buff=0.06)
        bot = VGroup(*[pstring(as_paulis(r, "Z"), s=0.3, step=xs[1] - xs[0]) for r in HAM]).arrange(DOWN, buff=0.06)
        top.move_to([float(np.mean(xs)), 0.95, 0])
        bot.move_to([float(np.mean(xs)), -1.55, 0])
        ev = VGroup(T("even overlaps", size=22), mark(True)).arrange(RIGHT, buff=0.15).next_to(dots, RIGHT, buff=0.6)
        name = T("CSS codes", size=40, bold=True).move_to([-0.8, 2.35, 0])
        who = T("Calderbank  ·  Shor  ·  Steane", size=20, color=MUTED).next_to(name, DOWN, buff=0.12)
        with self.voice("f1"):
            self.play(FadeIn(dots), run_time=0.5)
            self.play(FadeIn(top, shift=DOWN * 0.3), run_time=0.7)
            self.play(FadeIn(bot, shift=UP * 0.3), run_time=0.7)
            self.hold(1.6)
            self.play(FadeIn(ev), run_time=0.5)
            self.hold(3.2)
            self.play(FadeIn(name, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(who), run_time=0.4)
        # f2: a check reaches right across the code
        anc = Dot([dots[3].get_center()[0], 1.3, 0], radius=0.11, color=X_TILE)
        wires = VGroup(*[Line(anc.get_center(), dots[j].get_top(), color=X_TILE, stroke_width=2.5) for j in (0, 2, 4, 6)])
        with self.voice("f2"):
            self.play(FadeOut(VGroup(top, bot, ev)), run_time=0.5)
            self.play(FadeIn(anc), LaggedStart(*[Create(w) for w in wires], lag_ratio=0.2), run_time=0.9)
        # f3: next: the surface code
        nxt = VGroup(T("Next", size=26, color=MUTED), T("8.5  The surface code", size=48, bold=True)).arrange(DOWN, buff=0.3)
        nxt.move_to([0, 0.9, 0])
        pts = [[x, y, 0] for x in np.arange(-1.2, 1.21, 0.6) for y in np.arange(-2.1, -0.89, 0.6)]
        gd = VGroup(*[Dot(p, radius=0.06, color=MUTED) for p in pts])
        c = np.array([0.0, -1.5, 0])
        chk = Dot(c, radius=0.1, color=Z_TILE)
        near = VGroup(*[Line(c, c + d, color=Z_TILE, stroke_width=2.5) for d in (UP * 0.6, DOWN * 0.6, LEFT * 0.6, RIGHT * 0.6)])
        with self.voice("f3"):
            self.hold(1.6)
            self.play(*[FadeOut(m) for m in self.stage() + [self.badge]], run_time=0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(gd), run_time=0.4)
            self.play(FadeIn(chk), LaggedStart(*[Create(l) for l in near], lag_ratio=0.15), run_time=0.7)
