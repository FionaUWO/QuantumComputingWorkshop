"""Section 8.2 — Stabilizer codes.   Draft.
Build from the video folder with the Manim environment:
    python pipeline/build.py 8.2 render --low        (ONLY=<letters> renders chosen scenes)
Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.
Colours as in 8.1: a purple tile is the letter X, a green tile the letter Z, a dark tile the
identity. Orange is a minus sign, the answer -1, and a 1 in a syndrome. White is the answer +1
and a 0 in a syndrome. Cyan marks what to look at. Each check has a lamp: a hollow white ring
for +1, a filled orange disc for -1.
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from common import *  # noqa: E402,F401
DROP = 0.4            # the camera looks this much higher, which centres the picture (as in 1.2)
TS = 0.66             # side of a letter tile
X_TILE, Z_TILE = PAULI_X, PAULI_Z      # common.py
CHECKS = ["ZZI", "IZZ"]                # the bit flip code


def tile(ch, s=TS):
    """One letter of a Pauli string (as in 8.1). tile.ch is the letter."""
    col = {"X": X_TILE, "Z": Z_TILE, "Y": X_TILE, "I": DIM}[ch]
    box = RoundedRectangle(width=s, height=s, corner_radius=0.12 * s, stroke_width=0, fill_color=col, fill_opacity=1)
    g = VGroup(box)
    if ch == "I":
        g.add(Dot(box.get_center(), radius=0.05 * s / TS, color=MUTED))
    else:
        g.add(T(ch, size=34 * s / TS, color=BG if ch == "Z" else INK, bold=True).move_to(box))
    g.ch = ch
    return g


def pstring(letters, s=TS, buff=None):
    return VGroup(*[tile(c, s) for c in letters]).arrange(RIGHT, buff=0.12 * s if buff is None else buff)


def minus(size=54):
    return M("-", size=size, color=ACCENT)


def answer(plus, size=34):
    return M("+1", size=size, color=INK) if plus else M("-", "1", size=size, color=ACCENT)


def lamp(kind, r=0.2):
    """kind: '+' a hollow white ring, '-' a filled orange disc, '?' a muted ring with a question mark."""
    if kind == "-":
        return Circle(radius=r, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
    if kind == "?":
        return VGroup(Circle(radius=r, color=MUTED, stroke_width=3), T("?", size=22, color=MUTED))
    return Circle(radius=r, color=INK, stroke_width=4)


def anticommutes(a, b):
    return sum(x != y and "I" not in (x, y) for x, y in zip(a, b)) % 2 == 1


def syndrome(err):
    return "".join("1" if anticommutes(c, err) else "0" for c in CHECKS)


def weight(s):
    return sum(c != "I" for c in s)


class Main(NarratedScene):
    EP = "8.2"
    SCENES = [("i", "opening"), ("a", "hook"), ("b", "syndromes"), ("c", "adding"), ("d", "regions"),
              ("e", "distance"), ("f", "closing")]
    GC = np.array([1.5, 0.35, 0.0])      # centre of the 2 x 2 picture of three qubits
    CW, CH = 3.6, 1.7
    LX, LY = -4.9, 0.1                   # centre of the list of checks
    EY = 2.3                             # height of the error string

    def construct(self):
        only = os.environ.get("ONLY", "")
        self.busy = {}
        self.head = header("8.2  Stabilizer codes")
        self.wm = watermark()
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter != "i" and self.head not in self.mobjects:     # nothing over the opening card
                self.camera.frame_center = np.array([0.0, DROP, 0.0])
                self.head.shift(UP * DROP)
                self.wm.shift(UP * DROP)
                self.play(FadeIn(self.head), FadeIn(self.wm), run_time=0.4)
            getattr(self, name)()
        self.save_marks()
        (out_dir(self.EP) / "busy.json").write_text(json.dumps(self.busy, indent=1), encoding="utf-8")

    @contextmanager
    def voice(self, *ids, gap=None):
        """As in 8.1: holds scale to the recorded length, and busy time is noted per line."""
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

    def stage(self):
        return [m for m in self.mobjects if m is not self.head and m is not self.wm]

    def clear_stage(self, run_time=0.6):
        self.card_mob = None
        left = self.stage()
        if left:
            self.play(*[FadeOut(m) for m in left], run_time=run_time)

    # ------------------------------------------------------------ shared pieces
    def grid(self):
        """The eight basis states in four cells, columns by Z1 Z2, rows by Z2 Z3 (as in 8.1)."""
        txt = {(0, 0): r"|000\rangle,\ |111\rangle", (1, 0): r"|100\rangle,\ |011\rangle",
               (0, 1): r"|001\rangle,\ |110\rangle", (1, 1): r"|010\rangle,\ |101\rangle"}
        cells = {}
        for (c, r), s in txt.items():
            box = Rectangle(width=self.CW, height=self.CH, color=MUTED, stroke_width=2)
            box.move_to(self.GC + [(c - 0.5) * self.CW, (0.5 - r) * self.CH, 0])
            cells[(c, r)] = VGroup(box, M(s, size=30).move_to(box))
        for k in ((1, 0), (0, 1), (1, 1)):
            cells[k][0].set_stroke(opacity=0.22)
            cells[k][1].set_opacity(0.22)
        return cells

    def glow(self, cell):
        return Rectangle(width=self.CW, height=self.CH, stroke_color=HILITE, stroke_width=5, fill_color=HILITE,
                         fill_opacity=0.18).move_to(cell[0])

    def cell_of(self, syn):
        """Which cell a syndrome points to: the first bit picks the column, the second the row."""
        return (int(syn[0]), int(syn[1]))

    def checks_panel(self):
        """The list of checks, a lamp right of each row. Returns a group with .rows and .lamps."""
        rows = VGroup(*[pstring(s) for s in CHECKS]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lamps = VGroup(*[lamp("+").next_to(r, RIGHT, buff=0.4) for r in rows])
        box = SurroundingRectangle(VGroup(rows, lamps), color=MUTED, buff=0.24, corner_radius=0.14, stroke_width=1.6)
        g = VGroup(box, rows, lamps).move_to([self.LX, self.LY, 0])
        g.box, g.rows, g.lamps = box, rows, lamps
        g.title = T("checks", size=22, color=MUTED).next_to(box, UP, buff=0.18)
        return g

    def set_lamps(self, panel, kinds, run_time=0.4):
        anims = []
        for k, (old, kind) in enumerate(zip(panel.lamps, kinds)):
            new = lamp(kind).move_to(old)
            anims.append(Transform(old, new))
        self.play(*anims, run_time=run_time)

    def error_string(self, letters):
        e = pstring(letters).move_to([self.LX, self.EY, 0])
        e.label = T("error", size=22, color=MUTED).next_to(e, LEFT, buff=0.3)
        return e

    def swap_error(self, err, letters, run_time=0.5):
        new = pstring(letters).move_to(err)
        self.play(Transform(err, new), run_time=run_time)
        for t, c in zip(err, letters):       # Transform keeps the old letter tags
            t.ch = c
        return err

    def flip_route(self, key):
        hc = self.GC + [-self.CW / 2, self.CH / 2, 0]      # centre of the code cell
        routes = {
            (1, 0): (hc + [0.5, self.CH / 2 + 0.12, 0], hc + [self.CW - 0.5, self.CH / 2 + 0.12, 0], -0.9, UP * 0.55),
            (0, 1): (hc + [-self.CW / 2 - 0.12, 0.2, 0], hc + [-self.CW / 2 - 0.12, -self.CH - 0.2, 0], 0.9, LEFT * 0.62),
            (1, 1): (self.GC + [-0.42, 0.3, 0], self.GC + [0.42, -0.3, 0], 0.0, [0.42, 0.3, 0]),
        }
        return routes[key]

    def flip_arrow(self, key, name):
        start, end, bend, off = self.flip_route(key)
        arr = CurvedArrow(start, end, angle=bend, color=X_TILE, stroke_width=5, tip_length=0.22)
        lab = M(name, size=30, color=INK).move_to((start + end) / 2 + np.array(off))
        return VGroup(arr, lab)

    def wall_picture(self, letters="ZII"):
        """The checks see a shadow of the error, not the error: string, a pale wall, two lamps."""
        err = pstring(letters).move_to([-4.2, 0.6, 0])
        wall = Rectangle(width=0.35, height=3.4, stroke_width=0, fill_color=MUTED, fill_opacity=0.3).move_to([-1.2, 0.6, 0])
        rays = VGroup(*[DashedLine(err.get_right() + [0.15, dy, 0], wall.get_left() + [0, dy * 1.6, 0],
                                   color=MUTED, stroke_width=2, dash_length=0.12) for dy in (-0.25, 0, 0.25)])
        shadow = VGroup(*[lamp("+" if c == "0" else "-", r=0.14) for c in syndrome(letters)]).arrange(DOWN, buff=0.25)
        shadow.move_to(wall)
        lamps = VGroup(*[lamp("+" if c == "0" else "-") for c in syndrome(letters)]).arrange(DOWN, buff=0.4)
        lamps.move_to([1.6, 0.6, 0])
        names = VGroup(*[pstring(s, s=0.42).next_to(l, RIGHT, buff=0.35) for s, l in zip(CHECKS, lamps)])
        lab_e = T("the error", size=22, color=MUTED).next_to(err, UP, buff=0.3)
        lab_c = T("what the checks see", size=22, color=MUTED).next_to(VGroup(lamps, names), UP, buff=0.3)
        return VGroup(err, rays, wall, shadow, lamps, names, lab_e, lab_c)

    # ------------------------------------------------------------ I. opening
    def opening(self):
        centre = [0, 1.35, 0]
        lab = T("QAICON Lab", size=54, bold=True).move_to([0, -0.85, 0])
        full = T("Quantum and AI for Computing, Optimization, and Networking", size=26, color=HILITE)
        full.next_to(lab, DOWN, buff=0.3)
        where = T("Western University", size=24, color=MUTED).next_to(full, DOWN, buff=0.25)
        with self.voice("i1"):
            mark = logo_reveal(self, centre)
            self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.6)
            self.hold(0.3)
            self.play(FadeIn(full, shift=UP * 0.15), run_time=0.7)
            self.hold(1.2)
            self.play(FadeIn(where), run_time=0.5)
        series = T("Quantum Computing Workshop", size=28, color=MUTED).move_to([0, 1.2, 0])
        title = T("Stabilizer codes", size=50, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 8  ·  Section 8.2", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    # ------------------------------------------------------------ A. one error is caught, one is not
    def hook(self):
        self.clear_stage()
        panel = self.checks_panel()
        cells = self.grid()
        home = cells[(0, 0)]
        glow = self.glow(home)
        err = self.error_string("XII")
        # a1: the picture where 8.1 ended; X on qubit one moves the code out and the first lamp goes orange
        with self.voice("a1"):
            self.play(FadeIn(panel), FadeIn(panel.title), FadeIn(VGroup(*cells.values())), FadeIn(glow), run_time=0.8)
            self.hold(1.6)
            self.play(FadeIn(err, shift=RIGHT * 0.6), FadeIn(err.label), run_time=0.6)
            fl = self.flip_arrow((1, 0), "X_1")
            tgt = cells[(1, 0)]
            self.play(Create(fl[0]), FadeIn(fl[1]), tgt[0].animate.set_stroke(opacity=1),
                      tgt[1].animate.set_opacity(1), run_time=0.8)
            self.hold(1.4)
            self.set_lamps(panel, "-+")
            self.play(Indicate(panel.lamps[0], color=ACCENT, scale_factor=1.4), run_time=0.6)
        # a2: same qubit, a Z instead of an X
        with self.voice("a2"):
            self.play(FadeOut(fl), tgt[0].animate.set_stroke(opacity=0.22), tgt[1].animate.set_opacity(0.22),
                      run_time=0.6)
            self.set_lamps(panel, "??")
            self.hold(1.0)
            self.swap_error(err, "ZII")
        # a3: both checks answer +1; the state stays in the code cell
        with self.voice("a3"):
            self.hold(0.6)
            self.set_lamps(panel, "++")
            self.play(Indicate(panel.lamps, color=INK, scale_factor=1.25), run_time=0.7)
        # a4: (thinking pause) the code cell flashes, nothing new appears
        with self.voice("a4"):
            self.play(glow.animate(rate_func=there_and_back).set_fill(opacity=0.4), run_time=0.9)
        # a5: inside the code cell, the plus has become a minus
        state = M(r"|000\rangle", "+", r"|111\rangle", size=48).move_to(self.GC + [0, 0.2, 0])
        a_lab = T("the encoded state", size=22, color=MUTED).next_to(state, UP, buff=0.45)
        with self.voice("a5"):
            self.hold(1.4)
            others = VGroup(*[cells[k] for k in ((1, 0), (0, 1), (1, 1))], home[1])
            self.play(FadeOut(others), FadeOut(glow), home[0].animate.set_stroke(color=HILITE, opacity=1)
                      .stretch_to_fit_width(2 * self.CW).stretch_to_fit_height(2 * self.CH).move_to(self.GC),
                      run_time=0.8)
            self.play(FadeIn(state), FadeIn(a_lab), run_time=0.6)
            self.hold(1.6)
            tok = minus(48).move_to(state[2].get_top() + UP * 0.35)
            self.play(err[0].animate(rate_func=there_and_back).scale(1.25), FadeIn(tok, shift=DOWN * 0.2), run_time=0.7)
            new_sign = M("-", size=48, color=ACCENT).move_to(state[1])
            self.play(ReplacementTransform(tok, new_sign), FadeOut(state[1]), run_time=0.6)
            self.hold(1.4)
            self.play(Indicate(panel.lamps, color=INK, scale_factor=1.25), run_time=0.7)
        # a6: the checks only see a shadow of the error; the whole picture shrinks to the corner
        wall = self.wall_picture("ZII")
        with self.voice("a6"):
            self.clear_stage(0.6)
            self.play(FadeIn(wall[0]), FadeIn(wall[6]), run_time=0.5)
            self.play(FadeIn(wall[2]), Create(wall[1]), run_time=0.8)
            self.play(FadeIn(wall[3]), FadeIn(wall[4]), FadeIn(wall[5]), FadeIn(wall[7]), run_time=0.7)
            self.hold(3.2)
            self.play(wall.animate.scale(0.32).to_corner(UL, buff=0.35).shift(DOWN * 0.55 + UP * DROP), run_time=0.9)
        self.corner_wall = wall

    # ------------------------------------------------------------ B. the syndrome
    def product_row(self, e_letters, y=1.2):
        """g E |psi> written with tiles: a check, an error, a state."""
        g = pstring("ZZI")
        e = pstring(e_letters)
        ket = M(r"|\psi\rangle", size=48)
        row = VGroup(g, e, ket).arrange(RIGHT, buff=0.45).move_to([-0.6, y, 0])
        g_lab = T("check", size=20, color=MUTED).next_to(g, DOWN, buff=0.2)
        e_lab = T("error", size=20, color=MUTED).next_to(e, DOWN, buff=0.2)
        return row, g_lab, e_lab

    def slide_past(self, row, labels, spark):
        """The check slides from the left of the error to its right; an anticommuting pair throws a minus."""
        g, e, ket = row
        g_to, e_to = e.get_center() + (g.get_width() - e.get_width()) / 2 * RIGHT, g.get_center()
        e_to = g.get_left() + e.get_width() / 2 * RIGHT
        g_to = e_to + (e.get_width() / 2 + 0.45 + g.get_width() / 2) * RIGHT
        self.play(g.animate(path_arc=-PI / 2).move_to(g_to), e.animate(path_arc=-PI / 2).move_to(e_to),
                  labels[0].animate.move_to(g_to + DOWN * (g.get_height() / 2 + 0.3)),
                  labels[1].animate.move_to(e_to + DOWN * (e.get_height() / 2 + 0.3)), run_time=0.9)
        tok = None
        if spark:
            tok = minus(54).next_to(VGroup(g, e), UP, buff=0.25)
            self.play(FadeIn(tok, scale=1.6), run_time=0.4)
            self.play(tok.animate.next_to(e, LEFT, buff=0.15), run_time=0.5)
        return tok

    def syndromes(self):
        # the corner picture from A stays as a reminder
        keep = getattr(self, "corner_wall", None)
        for m in self.stage():
            if m is not keep:
                self.remove(m)
        row, g_lab, e_lab = self.product_row("IIX")
        e_part, g_part, ket = row[1], row[0], row[2]
        eq1 = VGroup(M("=", size=48), M(r"|\psi\rangle", size=48)).arrange(RIGHT, buff=0.3)
        # b1: a code state answers the check with +1
        with self.voice("b1"):
            self.hold(0.8)
            self.play(FadeIn(g_part), FadeIn(g_lab), FadeIn(ket), run_time=0.6)
            eq1.next_to(ket, RIGHT, buff=0.3)
            self.hold(1.2)
            self.play(FadeIn(eq1), run_time=0.5)
            ans = answer(True, 40).next_to(eq1, RIGHT, buff=0.7)
            self.play(FadeIn(ans), run_time=0.4)
            self.hold(1.2)
        # b2: an error that commutes; the check slides past it with no spark
        with self.voice("b2"):
            self.play(FadeOut(eq1), FadeOut(ans), run_time=0.4)
            self.play(FadeIn(e_part, shift=DOWN * 0.3), FadeIn(e_lab), run_time=0.6)
            self.hold(1.6)
            self.slide_past(row, (g_lab, e_lab), spark=False)
            ans = answer(True, 40).next_to(row, RIGHT, buff=0.7)
            self.play(FadeIn(ans), run_time=0.4)
            self.hold(1.0)
        # b3: an error that anticommutes; sliding past throws off a minus sign, the answer is -1
        row2, g2_lab, e2_lab = self.product_row("XII", y=-1.0)
        with self.voice("b3"):
            self.play(FadeIn(row2), FadeIn(g2_lab), FadeIn(e2_lab), run_time=0.6)
            self.hold(1.4)
            tok = self.slide_past(row2, (g2_lab, e2_lab), spark=True)
            ans2 = answer(False, 40).next_to(row2, RIGHT, buff=0.7).align_to(ans, LEFT)
            self.play(FadeIn(ans2), run_time=0.4)
        # b4: (the other speaker answers) nothing new
        with self.voice("b4"):
            pass
        # b5: the same answer whatever code state was hit; then the state is covered
        with self.voice("b5"):
            self.hold(0.8)
            for name in (r"|\phi\rangle", r"|\chi\rangle", r"|\psi\rangle"):
                new = M(name, size=48).move_to(row2[2])
                self.play(Transform(row2[2], new), Indicate(ans2, color=ACCENT, scale_factor=1.2), run_time=0.7)
                self.hold(0.5)
            self.hold(2.0)
            shield = SurroundingRectangle(row2[2], color=HILITE, buff=0.15, corner_radius=0.1, fill_color=HILITE,
                                          fill_opacity=0.35)
            self.play(FadeIn(shield), run_time=0.6)
            self.hold(1.4)
        # b6: back to the bit flip code; orange lamp -> 1, white -> 0, the string is the syndrome
        panel = self.checks_panel()
        err = self.error_string("XII")
        with self.voice("b6"):
            self.play(*[FadeOut(m) for m in self.stage() if m is not keep], run_time=0.5)
            self.play(FadeIn(panel), FadeIn(panel.title), FadeIn(err), FadeIn(err.label), run_time=0.6)
            self.set_lamps(panel, "-+")
            self.hold(1.2)
            bits = VGroup(*[M(b, size=36, color=ACCENT if b == "1" else INK).next_to(l, RIGHT, buff=0.55)
                            for b, l in zip(syndrome("XII"), panel.lamps)])
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bits], lag_ratio=0.4), run_time=0.8)
            self.hold(1.2)
            word = M(syndrome("XII")[0], syndrome("XII")[1], size=52).move_to([self.LX, -1.6, 0])
            word[0].set_color(ACCENT)
            name = T("syndrome", size=28, color=HILITE).next_to(word, RIGHT, buff=0.4)
            self.play(TransformFromCopy(bits, word), run_time=0.7)
            self.play(FadeIn(name), run_time=0.4)
        # b7: the three single flips give three different syndromes, one per dimmed cell
        cells = self.grid()
        glow = self.glow(cells[(0, 0)])
        tags = []
        with self.voice("b7"):
            self.play(FadeOut(bits), FadeOut(word), FadeOut(name), FadeIn(VGroup(*cells.values())), FadeIn(glow),
                      run_time=0.6)
            if keep is not None:
                self.play(FadeOut(keep), run_time=0.3)
            for k, (q, nm) in enumerate((("XII", "X_1"), ("IXI", "X_2"), ("IIX", "X_3"))):
                syn = syndrome(q)
                key = self.cell_of(syn)
                self.swap_error(err, q, run_time=0.4)
                self.set_lamps(panel, "".join("-" if b == "1" else "+" for b in syn), run_time=0.3)
                fl = self.flip_arrow(key, nm)
                tag = M(syn, size=30, color=ACCENT).move_to(cells[key][0].get_corner(DR) + [-0.35, 0.25, 0])
                self.play(Create(fl[0]), FadeIn(fl[1]), cells[key][0].animate.set_stroke(opacity=1),
                          cells[key][1].animate.set_opacity(1), FadeIn(tag), run_time=0.7)
                tags.append(VGroup(fl, tag))
                self.hold(0.5)
        self.b_state = (panel, err, cells, glow, tags)

    # ------------------------------------------------------------ C. syndromes add; two flips pass for one
    def adding(self):
        if not hasattr(self, "b_state"):          # rendering this scene on its own
            panel, err = self.checks_panel(), self.error_string("IIX")
            cells = self.grid()
            glow = self.glow(cells[(0, 0)])
            self.add(panel, panel.title, err, err.label, *cells.values(), glow)
            tags = []
        else:
            panel, err, cells, glow, tags = self.b_state
        # c1: both qubits one and two flip; the lamps become question marks (thinking pause)
        with self.voice("c1"):
            self.play(*[FadeOut(t) for t in tags], run_time=0.4)
            for k in ((1, 0), (0, 1), (1, 1)):
                cells[k][0].set_stroke(opacity=0.22)
                cells[k][1].set_opacity(0.22)
            self.hold(1.0)
            self.swap_error(err, "XXI")
            self.set_lamps(panel, "??")
        with self.voice("c2"):
            pass
        # c3: each check counts the minus signs; two cancel, one stays. 10 + 11 = 01
        with self.voice("c3"):
            self.hold(0.6)
            for r, row in enumerate(panel.rows):
                toks = []
                for j, (a, b) in enumerate(zip(row, err)):
                    if a.ch != "I" and b.ch != "I" and a.ch != b.ch:
                        toks.append(minus(40).next_to(a, DOWN, buff=0.02).shift(UP * 0.05))
                self.play(Indicate(row, color=HILITE, scale_factor=1.08), *[FadeIn(t, shift=DOWN * 0.15) for t in toks],
                          run_time=0.6)
                if len(toks) == 2:
                    mid = (toks[0].get_center() + toks[1].get_center()) / 2
                    self.play(*[t.animate.move_to(mid).set_opacity(0) for t in toks], run_time=0.5)
                else:
                    self.play(*[FadeOut(t) for t in toks], run_time=0.3)
                self.set_lamps(panel, "+?" if r == 0 else "+-", run_time=0.3)
            sumline = M(r"10", "+", r"11", "=", r"01", size=40).move_to([self.LX, -1.6, 0])
            for k in (0, 2, 4):
                sumline[k].set_color(INK)
            self.hold(0.8)
            self.play(Write(sumline), run_time=0.9)
            self.hold(1.2)
        # c4: 01 is also the syndrome of a lone flip on qubit three; a decoder adds X3 (thinking pause)
        with self.voice("c4"):
            self.hold(0.8)
            fl = self.flip_arrow((0, 1), "X_3")
            tgt = cells[(0, 1)]
            self.play(Indicate(sumline[4], color=ACCENT, scale_factor=1.3), Create(fl[0]), FadeIn(fl[1]),
                      tgt[0].animate.set_stroke(opacity=1), tgt[1].animate.set_opacity(1), run_time=0.9)
            self.hold(1.4)
            dec = T("decoder", size=22, color=HILITE).next_to(err, UP, buff=0.25)
            self.play(FadeIn(dec), run_time=0.4)
            self.swap_error(err, "XXX", run_time=0.6)
            self.set_lamps(panel, "++")
            self.hold(0.6)
        # c5: the code state is back in the code cell, but its two amplitudes have changed places
        home = cells[(0, 0)]
        a_bar = Rectangle(width=0.5, height=1.3, stroke_width=0, fill_color=HILITE, fill_opacity=1)
        b_bar = Rectangle(width=0.5, height=0.55, stroke_width=0, fill_color=HILITE, fill_opacity=1)
        bars = VGroup(a_bar, b_bar).arrange(RIGHT, buff=0.9, aligned_edge=DOWN).move_to(self.GC + [0, 0.15, 0])
        bl = VGroup(M(r"|000\rangle", size=28).next_to(a_bar, DOWN, buff=0.15),
                    M(r"|111\rangle", size=28).next_to(b_bar, DOWN, buff=0.15)).align_to(bars, DOWN).shift(DOWN * 0.45)
        with self.voice("c5"):
            self.play(FadeOut(fl), FadeOut(dec), FadeOut(sumline), *[FadeOut(cells[k]) for k in ((1, 0), (0, 1), (1, 1))],
                      FadeOut(home[1]), FadeOut(glow),
                      home[0].animate.set_stroke(color=HILITE, opacity=1).stretch_to_fit_width(2 * self.CW)
                      .stretch_to_fit_height(2 * self.CH).move_to(self.GC), run_time=0.7)
            self.play(FadeIn(bars), FadeIn(bl), run_time=0.5)
            self.play(a_bar.animate.stretch_to_fit_height(0.55, about_edge=DOWN),
                      b_bar.animate.stretch_to_fit_height(1.3, about_edge=DOWN), run_time=0.9)
        # c6: XXX passes both checks, and it is not one of them
        tick = T("passes both checks", size=22, color=INK).next_to(err, DOWN, buff=1.9)
        cross = T("is not a check", size=22, color=ACCENT).next_to(tick, DOWN, buff=0.2)
        with self.voice("c6"):
            self.hold(2.6)
            self.play(Indicate(panel.lamps, color=INK, scale_factor=1.25), FadeIn(tick), run_time=0.7)
            self.hold(1.6)
            self.play(FadeIn(cross), run_time=0.5)
            self.hold(2.0)

    # ------------------------------------------------------------ D. three kinds of error
    def regions(self):
        self.clear_stage()
        outer = RoundedRectangle(width=12.4, height=5.6, corner_radius=0.3, color=MUTED, stroke_width=2).move_to([0, 0.3, 0])
        mid = RoundedRectangle(width=8.6, height=3.6, corner_radius=0.25, color=MUTED, stroke_width=2).move_to([0, -0.05, 0])
        inner = RoundedRectangle(width=3.6, height=1.5, corner_radius=0.2, color=MUTED, stroke_width=2).move_to([0, -0.75, 0])
        l_out = VGroup(T("detected", size=26, bold=True), T("anticommutes with at least one check", size=18, color=MUTED))
        l_out.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(outer.get_corner(UL) + [2.3, -0.5, 0])
        l_mid = VGroup(T("logical error", size=26, bold=True), T("commutes with every check, not a check", size=18, color=MUTED))
        l_mid.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(mid.get_corner(UL) + [2.35, -0.45, 0])
        l_in = VGroup(T("no effect", size=24, bold=True), T("a check, or a product of checks", size=16, color=MUTED))
        l_in.arrange(DOWN, buff=0.06).move_to(inner.get_top() + DOWN * 0.38)

        def put(letters, where, s=0.42):
            g = pstring(letters, s=s)
            syn = syndrome(letters)
            ls = VGroup(*[lamp("+" if b == "0" else "-", r=0.11) for b in syn]).arrange(RIGHT, buff=0.1)
            ls.next_to(g, DOWN, buff=0.1)
            return VGroup(g, ls).move_to(where)
        with self.voice("d1"):
            self.play(Create(outer), run_time=0.6)
            self.play(Create(mid), run_time=0.5)
            self.play(Create(inner), run_time=0.5)
        with self.voice("d2"):
            self.play(inner.animate.set_stroke(HILITE, width=4), run_time=0.4)
            self.hold(1.6)
            zz = put("ZZI", inner.get_center() + DOWN * 0.28)
            self.play(FadeIn(zz, shift=DOWN * 0.3), run_time=0.6)
            self.hold(1.8)
            self.play(FadeIn(l_in), run_time=0.5)
        with self.voice("d3"):
            self.play(inner.animate.set_stroke(MUTED, width=2), outer.animate.set_stroke(HILITE, width=4), run_time=0.4)
            self.hold(1.4)
            singles = VGroup(put("XII", [-5.25, 0.55, 0]), put("IXI", [-5.25, -1.05, 0]), put("IIX", [5.25, 0.55, 0]))
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in singles], lag_ratio=0.3), run_time=0.9)
            self.play(FadeIn(l_out), run_time=0.5)
        with self.voice("d4"):
            self.play(outer.animate.set_stroke(MUTED, width=2), mid.animate.set_stroke(HILITE, width=4), run_time=0.4)
            self.hold(2.8)
            logic = VGroup(put("ZII", [-2.9, -0.75, 0]), put("XXX", [2.9, -0.75, 0]))
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in logic], lag_ratio=0.4), run_time=0.8)
        with self.voice("d5"):
            self.play(mid.animate(rate_func=there_and_back).set_stroke(width=8), run_time=0.8)
        with self.voice("d6"):
            self.hold(1.8)
            self.play(FadeIn(l_mid[0]), run_time=0.5)
            self.hold(1.0)
            self.play(FadeIn(l_mid[1]), run_time=0.4)
            self.hold(1.2)
            # above XXX (below it sits the box edge), nudged right to clear the inner box's corner
            ops = T("logical operators", size=20, color=HILITE).next_to(logic[1], UP, buff=0.25).shift(RIGHT * 0.2)
            self.play(FadeIn(ops), run_time=0.4)
        # d7: the same string is a failure by accident and a gate on purpose
        with self.voice("d7"):
            # the regions clear away; only XXX stays, then splits into two clean panels
            src = logic[1][0]
            rest = [m for m in self.stage() if m is not logic[1]] + [logic[1][1]]   # everything but the XXX tiles
            self.play(*[FadeOut(m) for m in rest], src.animate.scale(1.4).move_to([0, 1.7, 0]), run_time=0.8)
            left = src.copy()
            right = src.copy()
            div = DashedLine([0, 0.9, 0], [0, -2.0, 0], color=MUTED, stroke_width=1.5)
            self.play(left.animate.move_to([-3.6, -0.3, 0]), right.animate.move_to([1.9, -0.3, 0]),
                      FadeIn(div), run_time=0.8)
            fail = T("by accident: a failure", size=24, color=ACCENT).next_to(left, DOWN, buff=0.4)
            line = Line([0, 0, 0], [2.4, 0, 0], color=MUTED, stroke_width=2).next_to(right, RIGHT, buff=0.0)
            box = Square(side_length=0.62, color=INK, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(line)
            xl = M("X_L", size=26).move_to(box)
            gate = T("on purpose: a gate", size=24, color=HILITE).next_to(VGroup(right, line), DOWN, buff=0.4)
            self.play(FadeIn(fail), run_time=0.4)
            self.hold(1.4)
            self.play(Create(line), FadeIn(box), FadeIn(xl), FadeIn(gate), run_time=0.6)
            self.hold(1.0)
        self.d_state = (logic,)

    # ------------------------------------------------------------ E. weight and distance
    def distance(self):
        self.clear_stage()
        rows = VGroup(pstring("ZII"), pstring("XXX")).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-4.6, 1.0, 0])
        wts = VGroup(*[M(str(weight(s)), size=40, color=HILITE).next_to(r, RIGHT, buff=0.5)
                       for s, r in zip(("ZII", "XXX"), rows)])
        cap = T("logical errors", size=22, color=MUTED).next_to(rows, UP, buff=0.3)
        with self.voice("e1"):
            self.play(FadeIn(cap), FadeIn(rows), run_time=0.6)
            self.hold(2.6)
            for r, w in zip(rows, wts):
                self.play(*[Indicate(t, color=HILITE, scale_factor=1.15) for t in r if t.ch != "I"], run_time=0.6)
                self.play(FadeIn(w), run_time=0.3)
            name = T("weight", size=26, color=HILITE).next_to(wts, UP, buff=0.35)
            self.play(FadeIn(name), run_time=0.4)
        # e2: a ruler; d marks the lightest logical error; below d, caught or harmless
        ruler = NumberLine(x_range=[0, 4, 1], length=7.0, include_numbers=True, color=MUTED,
                           font_size=30).move_to([1.8, -1.5, 0])
        with self.voice("e2"):
            self.play(FadeOut(name), Create(ruler), run_time=0.8)
            self.hold(1.4)
            pin = M("d", size=40, color=HILITE).next_to(ruler.n2p(2.6), UP, buff=0.5)
            low = Line(ruler.n2p(0), ruler.n2p(2.6), color=HILITE, stroke_width=10, stroke_opacity=0.5)
            low_lab = T("caught, or harmless", size=20, color=MUTED).next_to(low, DOWN, buff=0.75)
            self.play(FadeIn(pin), run_time=0.4)
            self.hold(1.0)
            self.play(Create(low), FadeIn(low_lab), run_time=0.7)
        # e3: what is d for the bit flip code? (thinking pause) ZII is dimmed so the answer does not show
        q = M("?", size=40, color=HILITE).move_to(pin)
        with self.voice("e3"):
            self.play(FadeOut(low), FadeOut(low_lab), Transform(pin, q), rows[0].animate.set_opacity(0.25),
                      wts[0].animate.set_opacity(0.25), run_time=0.6)
        # e4: the guess: XXX at 3
        with self.voice("e4"):
            mark3 = rows[1].copy().scale(0.6).next_to(ruler.n2p(3), UP, buff=0.25)
            self.play(TransformFromCopy(rows[1], mark3), run_time=0.7)
        # e5: ZII lights again and lands at 1; d = 1
        with self.voice("e5"):
            self.hold(2.4)
            self.play(rows[0].animate.set_opacity(1), wts[0].animate.set_opacity(1), run_time=0.5)
            mark1 = rows[0].copy().scale(0.6).next_to(ruler.n2p(1), UP, buff=0.25)
            self.play(TransformFromCopy(rows[0], mark1), run_time=0.7)
            self.hold(1.2)
            d1 = M("d = 1", size=40, color=HILITE).next_to(mark1, UP, buff=0.3)
            self.play(Transform(pin, d1), run_time=0.6)
        # e6: [[3, 1, 1]]: one bit flip yes, any single-qubit error no
        tag = VGroup(M(r"[[3,1,1]]", size=36),
                     T("one bit flip  ✓", size=22, color=INK),
                     T("any single-qubit error  ✗", size=22, color=ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tag.move_to([4.6, 1.6, 0])
        with self.voice("e6"):
            self.hold(1.0)
            self.play(FadeIn(tag[0]), run_time=0.5)
            self.hold(1.2)
            self.play(FadeIn(tag[1]), run_time=0.4)
            self.hold(0.6)
            self.play(FadeIn(tag[2]), run_time=0.4)
        # e7: XXI times IIX is XXX, a logical error
        a, b = pstring("XXI", s=0.5), pstring("IIX", s=0.5)
        prod = VGroup(a, M(r"\times", size=34), b, M("=", size=34), pstring("XXX", s=0.5)).arrange(RIGHT, buff=0.25)
        prod.move_to([1.8, -2.75, 0])   # below the ruler, clear of d = 1 and the tiles
        with self.voice("e7"):
            self.hold(3.4)
            self.play(FadeIn(prod[:3]), run_time=0.6)
            self.hold(1.0)
            self.play(FadeIn(prod[3:]), run_time=0.6)
            self.play(Indicate(prod[4], color=HILITE, scale_factor=1.15), Indicate(rows[1], color=HILITE, scale_factor=1.1),
                      run_time=0.8)
        # e8: two errors of weight at most t laid end to end are still shorter than d; only then t is written
        with self.voice("e8"):
            self.play(FadeOut(prod), FadeOut(mark1), FadeOut(mark3), FadeOut(tag), Transform(pin, M("d", size=40, color=HILITE)
                      .next_to(ruler.n2p(3), UP, buff=1.05)), run_time=0.6)
            seg1 = Line(ruler.n2p(0), ruler.n2p(1), color=ACCENT, stroke_width=10).shift(UP * 0.35)
            seg2 = Line(ruler.n2p(1), ruler.n2p(2), color=ACCENT, stroke_width=10).shift(UP * 0.35)
            self.hold(1.2)
            self.play(Create(seg1), run_time=0.6)
            self.play(Create(seg2), run_time=0.6)
            self.hold(1.4)
            gap = Brace(Line(ruler.n2p(2), ruler.n2p(3)), UP, color=MUTED).shift(UP * 0.35)
            self.play(FadeIn(gap), run_time=0.4)
            self.hold(1.4)
            t = M(r"t = \left\lfloor \tfrac{d-1}{2} \right\rfloor", size=40).move_to([4.6, 1.6, 0])
            self.play(Write(t), run_time=0.8)

    # ------------------------------------------------------------ F. close, towards 8.3
    def closing(self):
        self.clear_stage()
        wall = self.wall_picture("ZII")
        with self.voice("f1"):
            self.play(FadeIn(wall), run_time=0.8)
            self.hold(3.0)
            self.play(Indicate(wall[0], color=HILITE, scale_factor=1.1), run_time=0.8)
        with self.voice("f2"):
            pass
        nxt = VGroup(T("Next", size=26, color=MUTED), T("8.3  Three codes", size=50, bold=True))
        nxt.arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        with self.voice("f3"):
            self.hold(1.6)
            self.play(*[FadeOut(m) for m in self.stage()], run_time=0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
