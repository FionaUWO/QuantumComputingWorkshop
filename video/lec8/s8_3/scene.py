"""Section 8.3 — Three codes.   Draft.
Build from the video folder with the Manim environment:
    python pipeline/build.py 8.3 render --low        (ONLY=<letters> renders chosen scenes)
Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.
Colours as in 8.1 and 8.2: a purple tile is the letter X, a green tile the letter Z, a tile split
purple and green is Y, a dark tile the identity. Orange is a minus sign, the answer -1, a 1 in a
syndrome and an ancilla that reads 1. White is +1 and 0. Cyan marks what to look at.
Circuits use common.Circuit (white lines and CNOTs; only real X and Z gates are coloured).
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from common import *  # noqa: E402,F401

DROP = 0.4            # the camera looks this much higher, which centres the picture (as in 8.2)
X_TILE, Z_TILE = PAULI_X, PAULI_Z

SHOR = ["ZZIIIIIII", "IZZIIIIII", "IIIZZIIII", "IIIIZZIII", "IIIIIIZZI", "IIIIIIIZZ",
        "XXXXXXIII", "IIIXXXXXX"]
HAM = ["0001111", "0110011", "1010101"]                  # columns are 1..7 in binary
STEANE = ["".join("X" if b == "1" else "I" for b in r) for r in HAM] + \
         ["".join("Z" if b == "1" else "I" for b in r) for r in HAM]
FIVE = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]


def tile(ch, s=0.5):
    """One letter of a Pauli string (as in 8.1, 8.2). Y is split purple / green."""
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


def pstring(letters, s=0.5, buff=None, block=0):
    """A Pauli string; block > 0 leaves a wider gap after every `block` letters (Shor's blocks)."""
    g = VGroup(*[tile(c, s) for c in letters])
    b = 0.14 * s if buff is None else buff
    x = 0.0
    for k, t in enumerate(g):
        t.move_to([x, 0, 0])
        x += s + b + (0.5 * s if block and (k + 1) % block == 0 else 0)
    return g.move_to(ORIGIN)


def lamp(kind, r=0.15):
    """'+' a hollow white ring, '-' a filled orange disc, '?' a muted ring with a question mark."""
    if kind == "-":
        return Circle(radius=r, stroke_width=0, fill_color=ACCENT, fill_opacity=1)
    if kind == "?":
        return VGroup(Circle(radius=r, color=MUTED, stroke_width=3), T("?", size=int(110 * r), color=MUTED))
    return Circle(radius=r, color=INK, stroke_width=3)


def anticommutes(a, b):
    return sum(x != y and "I" not in (x, y) for x, y in zip(a, b)) % 2 == 1


def qdot(label, r=0.2, color=MUTED):
    c = Circle(radius=r, color=color, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(c, T(str(label), size=int(80 * r), color=INK).move_to(c))


def code_card(name, nkd):
    t = VGroup(T(name, size=20, color=INK), M(nkd, size=26, color=MUTED)).arrange(RIGHT, buff=0.18)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.26, corner_radius=0.12,
                           color=MUTED, stroke_width=1.6, fill_color=BG, fill_opacity=1)
    return VGroup(box, t.move_to(box))


class Main(NarratedScene):
    EP = "8.3"
    SCENES = [("i", "opening"), ("a", "hook"), ("b", "shor"), ("c", "steane"), ("d", "five"),
              ("e", "closing")]
    CARD_Y = -2.55                   # the row of small code cards, bottom left
    BOARD = np.array([5.15, 2.95, 0])

    def construct(self):
        only = os.environ.get("ONLY", "")
        self.busy = {}
        self.head = header("8.3  Three codes")
        self.wm = watermark()
        self.cards = []
        self.board = None
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter != "i" and self.head not in self.mobjects:     # nothing over the opening card
                self.camera.frame_center = np.array([0.0, DROP, 0.0])
                self.head.shift(UP * DROP)
                self.wm.shift(UP * DROP)
                self.play(FadeIn(self.head), FadeIn(self.wm), run_time=0.4)
            if letter not in "ia" and self.board is None:          # a scene rendered on its own
                self.board = self.scoreboard()
                self.add(self.board)
            need = {"c": 1, "d": 2, "e": 3}.get(letter, 0)
            for nm, nkd in [("Shor", "[[9,1,3]]"), ("Steane", "[[7,1,3]]"), ("five-qubit", "[[5,1,3]]")][len(self.cards):need]:
                self.add_card(nm, nkd, animate=False)
            getattr(self, name)()
        self.save_marks()
        (out_dir(self.EP) / "busy.json").write_text(json.dumps(self.busy, indent=1), encoding="utf-8")

    @contextmanager
    def voice(self, *ids, gap=None):
        """As in 8.2: holds scale to the recorded length, and busy time is noted per line."""
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
        return [self.head, self.wm, self.board] + self.cards

    def stage(self):
        return [m for m in self.mobjects if m not in self.keep()]

    def clear_stage(self, run_time=0.6):
        left = self.stage()
        if left:
            self.play(*[FadeOut(m) for m in left], run_time=run_time)

    # ------------------------------------------------------------ shared pieces
    def scoreboard(self, value="?"):
        lab = T("fewest qubits", size=20, color=MUTED)
        val = T(value, size=34, color=HILITE, bold=True)
        row = VGroup(lab, T("=", size=24, color=MUTED), val).arrange(RIGHT, buff=0.15)
        box = RoundedRectangle(width=row.width + 0.45, height=0.7, corner_radius=0.14, color=MUTED,
                               stroke_width=1.6, fill_color=BG, fill_opacity=1)
        g = VGroup(box, row.move_to(box)).move_to(self.BOARD)
        g.val = val
        return g

    def add_card(self, name, nkd, src=None, animate=True):
        card = code_card(name, nkd)
        x = -6.75 + card.width / 2 + sum(c.width + 0.2 for c in self.cards)
        card.move_to([x, self.CARD_Y, 0])
        if animate:
            if src is not None:
                self.play(ReplacementTransform(src, card), run_time=0.8)
            else:
                self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.5)
        else:
            self.add(card)
        self.cards.append(card)
        return card

    def pulse(self, path, run_time=0.9):
        """An orange spark running along a path (an error reaching an ancilla)."""
        d = Dot(path.get_start(), radius=0.08, color=ACCENT)
        trail = path.copy().set_stroke(ACCENT, width=4, opacity=0.8)
        self.play(MoveAlongPath(d, path), Create(trail), run_time=run_time, rate_func=linear)
        return VGroup(d, trail)

    def trail(self, pts):
        p = VMobject()
        p.set_points_as_corners([np.array(q, dtype=float) for q in pts])
        return p

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
        title = T("Three codes", size=50, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 8  ·  Section 8.3", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    # ------------------------------------------------------------ A. how few qubits could do it?
    def hook(self):
        self.clear_stage()
        # a1: the ruler from 8.2, with d at 3
        axis = NumberLine(x_range=[0, 5, 1], length=8, color=MUTED, include_numbers=False, stroke_width=2)
        axis.move_to([0, 0.4, 0])
        nums = VGroup(*[T(str(k), size=22, color=MUTED).next_to(axis.n2p(k), DOWN, buff=0.2) for k in range(6)])
        wlab = T("weight", size=22, color=MUTED).next_to(axis, RIGHT, buff=0.3)
        dmark = VGroup(Line(axis.n2p(3) + DOWN * 0.25, axis.n2p(3) + UP * 0.6, color=HILITE, stroke_width=5),
                       M("d = 3", size=36, color=HILITE).next_to(axis.n2p(3) + UP * 0.6, UP, buff=0.12))
        low = Line(axis.n2p(0), axis.n2p(2.85), color=INK, stroke_width=7).shift(UP * 0.02)
        low_lab = T("caught, or harmless", size=22, color=INK).next_to(low, UP, buff=0.28)
        with self.voice("a1"):
            self.play(Create(axis), FadeIn(nums), FadeIn(wlab), run_time=0.8)
            self.hold(2.5)
            self.play(Create(dmark[0]), FadeIn(dmark[1]), run_time=0.6)
            self.hold(1.5)
            self.play(Create(low), FadeIn(low_lab), run_time=0.8)
        ruler = VGroup(axis, nums, wlab, dmark, low, low_lab)
        # a2: one logical qubit spread over nine
        dots = VGroup(*[qdot(k + 1) for k in range(9)]).arrange(RIGHT, buff=0.38).move_to([0, -1.1, 0])
        top = Dot([0, 1.5, 0], radius=0.16, color=HILITE)
        top_lab = T("1 logical qubit", size=22, color=HILITE).next_to(top, UP, buff=0.18)
        lines = VGroup(*[Line(top.get_center(), d.get_top(), color=MUTED, stroke_width=1.5) for d in dots])
        bot_lab = T("9 physical qubits", size=22, color=MUTED).next_to(dots, DOWN, buff=0.3)
        with self.voice("a2"):
            self.play(FadeOut(ruler), run_time=0.6)
            self.play(FadeIn(top), FadeIn(top_lab), run_time=0.5)
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.08), run_time=1.4)
            self.play(FadeIn(bot_lab), run_time=0.5)
        # a3: the question goes up on the board, and stays for the whole film
        self.board = self.scoreboard()
        with self.voice("a3"):
            self.hold(2.2)
            self.play(FadeIn(self.board, shift=LEFT * 0.3), run_time=0.6)
            self.play(Indicate(self.board.val, color=HILITE, scale_factor=1.4), run_time=0.7)
        # a4: her count, three kinds times three qubits
        with self.voice("a4"):
            self.hold(0.8)
            groups = [VGroup(*dots[3 * g:3 * g + 3]) for g in range(3)]
            self.play(*[grp.animate.shift(RIGHT * (g - 1) * 0.5) for g, grp in enumerate(groups)],
                      *[l.animate.put_start_and_end_on(top.get_center(), d.get_top() + RIGHT * (k // 3 - 1) * 0.5)
                        for k, (l, d) in enumerate(zip(lines, dots))], run_time=0.7)
            kinds = VGroup(*[tile(c, 0.42).next_to(grp, UP, buff=0.3) for c, grp in zip("XYZ", groups)])
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.2) for k in kinds], lag_ratio=0.3), run_time=0.8)
            sum_lab = M(r"3 \times 3 = 9", size=36).next_to(bot_lab, DOWN, buff=0.25)
            self.play(FadeIn(sum_lab), run_time=0.5)
        self.her_nine = sum_lab
        # a5: smaller than nine
        less = T("< 9", size=20, color=MUTED).next_to(self.board, DOWN, buff=0.12)
        with self.voice("a5"):
            self.hold(3.5)
            self.play(FadeIn(less, shift=UP * 0.1), run_time=0.5)
        self.remove(less)          # a part of the board now, not a loose piece clear_stage would take
        self.board.add(less)
        self.clear_stage()

    # ------------------------------------------------------------ B. Shor's code as eight checks
    def shor(self):
        self.clear_stage()
        S = 0.3
        LX = -3.6
        rows = VGroup(*[pstring("I" * 9, s=S, block=3) for _ in SHOR]).arrange(DOWN, buff=0.1)
        rows.move_to([LX, -0.5, 0])
        xs = [t.get_center()[0] for t in rows[0]]
        dots = VGroup(*[qdot(k + 1, r=0.15).move_to([x, rows.get_top()[1] + 0.45, 0]) for k, x in enumerate(xs)])
        lamps = VGroup(*[lamp("+", r=0.11).next_to(r, RIGHT, buff=0.3) for r in rows])
        blocks = [VGroup(*dots[3 * g:3 * g + 3]) for g in range(3)]
        # b1: nine qubits in three blocks, eight blank rows
        with self.voice("b1"):
            self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.06), run_time=0.9)
            self.hold(1.5)
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows], lag_ratio=0.12), run_time=1.4)
            self.play(FadeIn(lamps), run_time=0.4)
        # b2: six Z pairs, two in each block
        with self.voice("b2"):
            for k in range(6):
                new = pstring(SHOR[k], s=S, block=3).move_to(rows[k])
                g = blocks[k // 2]
                self.play(Transform(rows[k], new), *[d[0].animate.set_stroke(HILITE) for d in g], run_time=0.45)
                if k % 2 == 1:
                    self.play(*[d[0].animate.set_stroke(MUTED) for d in g], run_time=0.25)
                for t, c in zip(rows[k], SHOR[k]):
                    t.ch = c
        # b3: two X checks across neighbouring blocks; a Z on qubit 2 lights the first one
        br1 = Brace(VGroup(*blocks[0], *blocks[1]), UP, color=X_TILE, buff=0.08).shift(UP * 0.5)
        br2 = Brace(VGroup(*blocks[1], *blocks[2]), UP, color=X_TILE, buff=0.08).shift(UP * 0.85)
        err = tile("Z", 0.26).next_to(dots[1], UP, buff=0.5)
        with self.voice("b3"):
            for k in (6, 7):
                new = pstring(SHOR[k], s=S, block=3).move_to(rows[k])
                self.play(Transform(rows[k], new), GrowFromCenter(br1 if k == 6 else br2), run_time=0.6)
            self.hold(2.0)
            self.play(FadeIn(err, shift=DOWN * 0.3), run_time=0.4)
            self.play(err.animate.move_to(dots[1].get_center() + UP * 0.34).scale(0.9), run_time=0.4)
            self.play(Transform(lamps[6], lamp("-", r=0.11).move_to(lamps[6])), run_time=0.4)
            self.play(Indicate(lamps[6], color=ACCENT, scale_factor=1.5), run_time=0.5)
        # b4: circuit 1, the Z1 Z2 check: two CNOTs onto an ancilla
        c1 = Circuit(["1", "2", "3"], 1, [("cnot", 0, 3), ("cnot", 1, 3)], gap=0.48, step=0.75, lead=0.7)
        c1.move_to([3.0, -0.1, 0])
        frame1 = SurroundingRectangle(rows[0], color=HILITE, buff=0.06, stroke_width=3)
        tag1 = pstring("ZZI", s=0.32).next_to(c1, UP, buff=0.3)
        with self.voice("b4"):
            self.play(Create(frame1), run_time=0.4)
            self.play(TransformFromCopy(VGroup(*rows[0][:3]), tag1), run_time=0.8)
            self.play(Create(c1.wires), FadeIn(c1.labels), run_time=0.8)
            self.hold(2.2)
            for col in c1.cols:
                self.play(FadeIn(col, scale=0.8), run_time=0.45)
            self.play(FadeIn(c1.meters), run_time=0.4)
            self.hold(0.8)
            # an X on qubit 1 reaches the ancilla through the first CNOT: reads 1
            e1 = tile("X", 0.3).move_to(c1.point(0, "start") + RIGHT * 0.32)
            self.play(FadeIn(e1, scale=1.4), run_time=0.35)
            p = self.pulse(self.trail([e1.get_center(), c1.point(0, 0), c1.point(3, 0),
                                       c1.point(3, "meter") + LEFT * 0.3]))
            r1 = c1.readout(3, 1)
            self.play(FadeIn(r1), FadeOut(p), run_time=0.4)
            self.hold(0.6)
            # X on qubits 1 and 2: two flips arrive and cancel: reads 0
            e2 = tile("X", 0.3).move_to(c1.point(1, "start") + RIGHT * 0.32)
            self.play(FadeIn(e2, scale=1.4), FadeOut(r1), run_time=0.35)
            pa = self.pulse(self.trail([e1.get_center(), c1.point(0, 0), c1.point(3, 0)]), run_time=0.6)
            pb = self.pulse(self.trail([e2.get_center(), c1.point(1, 1), c1.point(3, 1)]), run_time=0.6)
            self.play(FadeOut(pa), FadeOut(pb), Flash(c1.point(3, 1), color=ACCENT), run_time=0.5)
            r0 = c1.readout(3, 0)
            self.play(FadeIn(r0), run_time=0.4)
        circ1 = VGroup(c1, tag1, e1, e2, r0)
        # b5: circuit 2, the X1..X6 check: H, six controlled X, H
        c2 = Circuit([str(k) for k in range(1, 7)], 1,
                     [("h", 6), ("ctrl", 6, {k: "X" for k in range(6)}), ("h", 6)],
                     gap=0.4, step=0.8, lead=0.75, size=0.3)
        c2.move_to([2.6, -0.35, 0])
        frame2 = SurroundingRectangle(rows[6], color=HILITE, buff=0.06, stroke_width=3)
        with self.voice("b5"):
            self.play(circ1.animate.scale(0.45).move_to([5.6, 1.75, 0]), ReplacementTransform(frame1, frame2),
                      run_time=0.7)
            self.play(Create(c2.wires), FadeIn(c2.labels), run_time=0.7)
            self.play(FadeIn(c2.cols[0], scale=0.8), run_time=0.35)
            self.hold(0.6)
            self.play(FadeIn(c2.cols[2], scale=0.8), run_time=0.35)
            self.hold(1.2)
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in c2.cols[1]], lag_ratio=0.12), run_time=1.0)
            self.play(FadeIn(c2.meters), run_time=0.4)
            self.hold(0.8)
            ez = tile("Z", 0.28).move_to(c2.point(1, "start") + RIGHT * 0.3)
            self.play(TransformFromCopy(err, ez), run_time=0.6)
            p = self.pulse(self.trail([ez.get_center(), c2.point(1, 1), c2.point(6, 1),
                                       c2.point(6, "meter") + LEFT * 0.3]))
            rd = c2.readout(6, 1)
            self.play(FadeIn(rd), FadeOut(p), run_time=0.4)
            self.play(Indicate(rd, color=ACCENT, scale_factor=1.5), Indicate(lamps[6], color=ACCENT, scale_factor=1.6),
                      run_time=0.8)
        # b6: back to the list; rows 1 and 7 flash
        with self.voice("b6"):
            self.play(FadeOut(VGroup(c2, ez, rd, circ1, frame2)), run_time=0.6)
            fa = SurroundingRectangle(rows[0], color=HILITE, buff=0.06)
            fb = SurroundingRectangle(rows[6], color=HILITE, buff=0.06)
            self.play(Create(fa), Create(fb), run_time=0.5)
            self.play(FadeOut(fa), FadeOut(fb), run_time=0.4)
        # b7: overlaps are two or zero, both even
        with self.voice("b7"):
            ra = rows[0].copy()
            rb = rows[6].copy()
            self.play(ra.animate.move_to([3.0, 0.8, 0]), rb.animate.move_to([3.0, 0.35, 0]), run_time=0.7)
            box = SurroundingRectangle(VGroup(ra[0], ra[1], rb[0], rb[1]), color=HILITE, buff=0.06)
            n2 = M("2", size=36, color=HILITE).next_to(rb, RIGHT, buff=0.4)
            self.play(Create(box), FadeIn(n2), run_time=0.6)
            ok1 = VGroup(T("even", size=20, color=INK), mark(True)).arrange(RIGHT, buff=0.12).next_to(n2, RIGHT, buff=0.25)
            self.play(FadeIn(ok1), run_time=0.4)
            self.hold(1.2)
            rc = rows[4].copy()
            rd2 = rows[6].copy()
            self.play(rc.animate.move_to([3.0, -0.65, 0]), rd2.animate.move_to([3.0, -1.1, 0]), run_time=0.7)
            n0 = M("0", size=36, color=HILITE).next_to(rd2, RIGHT, buff=0.4)
            ok2 = ok1.copy().next_to(n0, RIGHT, buff=0.25)
            self.play(Indicate(VGroup(*rc[6:8]), color=HILITE), Indicate(VGroup(*rd2[:6]), color=HILITE), run_time=0.8)
            self.play(FadeIn(n0), FadeIn(ok2), run_time=0.5)
        overlap = VGroup(ra, rb, box, n2, ok1, rc, rd2, n0, ok2)
        # b8: eight halvings leave two dimensions
        bar = Rectangle(width=0.7, height=4.0, stroke_width=0, fill_color=HILITE, fill_opacity=0.55)
        bar.move_to([2.6, 0.0, 0]).align_to([0, -2.0, 0], DOWN)
        count = M("2^9", size=40).next_to(bar, RIGHT, buff=0.35).align_to(bar, UP)
        with self.voice("b8"):
            self.play(FadeOut(overlap), FadeOut(err), FadeOut(VGroup(br1, br2)),
                      Transform(lamps[6], lamp("+", r=0.11).move_to(lamps[6])), run_time=0.5)
            self.play(FadeIn(bar), FadeIn(count), run_time=0.5)
            fr = SurroundingRectangle(rows[0], color=HILITE, buff=0.05)
            self.add(fr)
            for k in range(8):
                self.play(fr.animate.move_to(rows[k]),
                          bar.animate.stretch_to_fit_height(4.0 / 2 ** (k + 1), about_edge=DOWN),
                          Transform(count, M(f"2^{{{8 - k}}}" if k < 7 else "2", size=40).next_to(bar, RIGHT, buff=0.35)
                                    .align_to([0, -2.0 + max(4.0 / 2 ** (k + 1), 0.4), 0], UP)), run_time=0.42)
            one = T("1 logical qubit", size=24, color=HILITE).next_to(count, RIGHT, buff=0.3)
            self.play(FadeIn(one), FadeOut(fr), run_time=0.4)
            self.hold(0.6)
            self.play(FadeOut(VGroup(bar, count, one, lamps, dots)), run_time=0.5)
            self.add_card("Shor", "[[9,1,3]]", src=rows)
        # b9: logical X made of Z letters
        zl = pstring("Z" * 9, s=0.48, block=3).move_to([0, 0.2, 0])
        q = M("=", "X_L", "?", size=48).next_to(zl, RIGHT, buff=0.35)
        q[2].set_color(HILITE)
        with self.voice("b9"):
            self.hold(0.8)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in zl], lag_ratio=0.06), run_time=0.9)
            self.play(FadeIn(q), run_time=0.5)
        # b10: thinking pause: only the question mark pulses
        with self.voice("b10"):
            self.play(Indicate(q[2], color=HILITE, scale_factor=1.5), run_time=0.9)
        # b11: each block's plus turns into a minus, |0_L> becomes |1_L>
        parts = []
        for g in range(3):
            parts += [r"(|000\rangle", "+", r"|111\rangle)"]
        state = M(*parts, size=34).move_to([0.6, 1.7, 0])
        name = M(r"|0_L\rangle =", size=38).next_to(state, LEFT, buff=0.25)
        with self.voice("b11"):
            self.play(FadeIn(name), FadeIn(state), run_time=0.7)
            self.hold(0.6)
            for g in range(3):
                blk = VGroup(*zl[3 * g:3 * g + 3])
                self.play(Indicate(blk, color=HILITE, scale_factor=1.1), run_time=0.45)
                mi = M("-", size=34, color=ACCENT).move_to(state[3 * g + 1])
                self.play(Transform(state[3 * g + 1], mi), run_time=0.4)
            self.play(Transform(name, M(r"|1_L\rangle =", size=38).move_to(name)), FadeOut(q[2]), run_time=0.6)
            self.hold(1.4)
            xl = pstring("X" * 9, s=0.48, block=3).move_to([0, -1.1, 0])
            zlab = M("=", "Z_L", size=48).next_to(xl, RIGHT, buff=0.35)
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in xl], lag_ratio=0.05), run_time=0.8)
            self.play(FadeIn(zlab), run_time=0.4)
        self.clear_stage()

    # ------------------------------------------------------------ C. Steane: the syndrome is the address
    def venn_pos(self, centre, R):
        k = R / 85.0
        circ = {1: (180, 130), 2: (135, 205), 3: (225, 205)}
        qub = {4: (180, 85), 6: (128, 155), 5: (232, 155), 7: (180, 180), 2: (90, 240), 3: (180, 237), 1: (270, 240)}
        to = lambda p: np.array(centre) + np.array([(p[0] - 180) * k, -(p[1] - 180) * k, 0])
        return {i: to(p) for i, p in circ.items()}, {i: to(p) for i, p in qub.items()}

    def steane(self):
        self.clear_stage()
        # c1: the numbers one to seven, written in binary as columns
        nums = VGroup(*[T(str(j), size=30, bold=True) for j in range(1, 8)])
        for j, n in enumerate(nums):
            n.move_to([-2.4 + 0.8 * j, 2.2, 0])
        bits = VGroup()
        for r in range(3):
            bits.add(VGroup(*[T(HAM[r][j], size=28, color=INK if HAM[r][j] == "1" else DIM, bold=True)
                              .move_to([-2.4 + 0.8 * j, 1.45 - 0.5 * r, 0]) for j in range(7)]))
        hl = M("H =", size=36, color=MUTED).next_to(bits, LEFT, buff=0.5)
        with self.voice("c1"):
            self.hold(2.0)
            self.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.15) for n in nums], lag_ratio=0.1), run_time=0.9)
            self.hold(1.5)
            for j in range(7):
                self.play(*[TransformFromCopy(nums[j], bits[r][j]) for r in range(3)], run_time=0.35)
            self.play(FadeIn(hl), run_time=0.4)
        table = VGroup(nums, bits, hl)
        # c2: each row becomes a circle around its four qubits
        cpos, qpos = self.venn_pos([-3.4, -0.55, 0], 1.25)
        qd = {j: qdot(j, r=0.19).move_to(qpos[j]) for j in range(1, 8)}
        circles = {i: Circle(radius=1.25, color=MUTED, stroke_width=2.5, fill_color=MUTED, fill_opacity=0.06)
                   .move_to(cpos[i]) for i in (1, 2, 3)}
        clabs = {1: T("1", size=22, color=MUTED).next_to(circles[1], UP, buff=0.08),
                 2: T("2", size=22, color=MUTED).next_to(circles[2], LEFT, buff=0.08).shift(DOWN * 0.6),
                 3: T("3", size=22, color=MUTED).next_to(circles[3], RIGHT, buff=0.08).shift(DOWN * 0.6)}
        with self.voice("c2"):
            self.play(table.animate.scale(0.62).move_to([1.3, 2.35, 0]), run_time=0.8)   # clear of the board
            self.play(LaggedStart(*[TransformFromCopy(nums[j - 1], qd[j]) for j in range(1, 8)], lag_ratio=0.08),
                      run_time=1.0)
            for r in range(3):
                ones = VGroup(*[bits[r][j] for j in range(7) if HAM[r][j] == "1"])
                self.play(ones.animate.set_color(HILITE), *[qd[j + 1][0].animate.set_stroke(HILITE)
                                                            for j in range(7) if HAM[r][j] == "1"], run_time=0.4)
                self.add(circles[r + 1])
                self.bring_to_front(*qd.values())
                self.play(Create(circles[r + 1]), FadeIn(clabs[r + 1]), run_time=0.6)
                self.play(ones.animate.set_color(INK), *[qd[j][0].animate.set_stroke(MUTED) for j in range(1, 8)],
                          run_time=0.3)
        venn = VGroup(*circles.values(), *clabs.values(), *qd.values())
        # c3: two checks per circle: six checks on seven qubits
        S = 0.3
        chk = VGroup(*[pstring(s, s=S) for s in STEANE]).arrange(DOWN, buff=0.1)
        chk.move_to([2.4, -0.25, 0])
        chk[3:].shift(DOWN * 0.15)
        tags = VGroup(*[T(str(k % 3 + 1), size=18, color=MUTED).next_to(r, LEFT, buff=0.25) for k, r in enumerate(chk)])
        count = M("7 - 6 = 1", size=34).next_to(chk, DOWN, buff=0.35)
        with self.voice("c3"):
            for k in range(3):
                self.play(Indicate(circles[k + 1], color=HILITE, scale_factor=1.03),
                          FadeIn(chk[k], shift=RIGHT * 0.2), FadeIn(chk[k + 3], shift=RIGHT * 0.2),
                          FadeIn(tags[k]), FadeIn(tags[k + 3]), run_time=0.7)
            self.hold(1.6)
            self.play(FadeIn(count), run_time=0.5)
        # c4: every overlap is even
        def share(a, b, qs, n, y):
            hi = [qd[j][0].animate.set_stroke(HILITE, width=4) for j in qs]
            ca = [circles[c].animate.set_stroke(HILITE) for c in (a, b)]
            lab = VGroup(M(n, size=30, color=HILITE), mark(True)).arrange(RIGHT, buff=0.15).move_to([5.9, y, 0])
            self.play(*hi, *ca, run_time=0.4)
            self.play(FadeIn(lab), run_time=0.3)
            self.hold(0.7)
            self.play(*[qd[j][0].animate.set_stroke(MUTED, width=2.5) for j in qs],
                      *[circles[c].animate.set_stroke(MUTED) for c in (a, b)], run_time=0.3)
            return lab
        with self.voice("c4"):
            self.play(FadeOut(count), run_time=0.3)
            l1 = share(1, 2, (6, 7), "2", 0.55)
            l2 = share(1, 3, (5, 7), "2", 0.1)
            fr = VGroup(SurroundingRectangle(chk[0], color=HILITE, buff=0.04), SurroundingRectangle(chk[3], color=HILITE, buff=0.04))
            l3 = VGroup(M("4", size=30, color=HILITE), mark(True)).arrange(RIGHT, buff=0.15).move_to([5.9, -0.35, 0])
            self.play(Create(fr), run_time=0.4)
            self.play(FadeIn(l3), run_time=0.3)
            self.hold(0.6)
            self.play(FadeOut(fr), run_time=0.3)
        evens = VGroup(l1, l2, l3)
        # c5: an X on qubit five; three lamps wait (thinking pause)
        zl = VGroup(*[lamp("?", r=0.13).next_to(chk[3 + r], RIGHT, buff=0.25) for r in range(3)])
        ex = tile("X", 0.3).move_to(qd[5].get_center() + UP * 0.95)
        with self.voice("c5"):
            self.play(FadeOut(evens), run_time=0.3)
            self.play(FadeIn(ex, shift=DOWN * 0.3), run_time=0.4)
            self.play(ex.animate.move_to(qd[5].get_center() + UR * 0.24).scale(0.8), run_time=0.4)
            self.hold(2.0)
            self.play(FadeIn(zl), run_time=0.4)
        # c6: (she answers; nothing new)
        with self.voice("c6"):
            self.play(qd[5][0].animate(rate_func=there_and_back).set_stroke(HILITE, width=5), run_time=0.8)
        # c7: circles one and three light up: 1 0 1 = 5
        with self.voice("c7"):
            self.play(circles[1].animate.set_stroke(ACCENT, width=4), circles[3].animate.set_stroke(ACCENT, width=4),
                      run_time=0.5)
            self.play(Transform(zl[0], lamp("-", r=0.13).move_to(zl[0])), Transform(zl[1], lamp("+", r=0.13).move_to(zl[1])),
                      Transform(zl[2], lamp("-", r=0.13).move_to(zl[2])), run_time=0.5)
            self.hold(1.0)
            syn = VGroup(T("1", size=30, color=ACCENT, bold=True), T("0", size=30, bold=True),
                         T("1", size=30, color=ACCENT, bold=True)).arrange(RIGHT, buff=0.12)
            syn.next_to(zl, RIGHT, buff=0.35)
            self.play(FadeIn(syn), run_time=0.4)
            self.hold(0.8)
            five = M("= 5", size=38, color=HILITE).next_to(syn, RIGHT, buff=0.2)
            self.play(FadeIn(five), Indicate(qd[5], color=HILITE, scale_factor=1.4), run_time=0.7)
        # c8: circuit 3: three ancillas, twelve CNOTs; the X on qubit 5 reaches ancillas 1 and 3
        cols = []
        groups = []
        for r in range(3):
            g = []
            for j in range(7):
                if HAM[r][j] == "1":
                    g.append(len(cols))
                    cols.append(("cnot", j, 7 + r))
            groups.append(g)
        c3 = Circuit([str(j) for j in range(1, 8)], 3, cols, gap=0.36, step=0.36, lead=0.55, size=0.26)
        c3.move_to([2.3, 0.0, 0])
        with self.voice("c8"):
            self.play(FadeOut(VGroup(chk, tags, zl, syn, five)), table.animate.scale(0.8).move_to([-3.4, 2.55, 0]),
                      run_time=0.6)
            self.play(Create(c3.wires), FadeIn(c3.labels), run_time=0.7)
            for r, g in enumerate(groups):
                self.play(circles[r + 1].animate.set_stroke(HILITE, width=4),
                          LaggedStart(*[FadeIn(c3.cols[k], scale=0.8) for k in g], lag_ratio=0.2), run_time=0.7)
                self.play(circles[r + 1].animate.set_stroke(ACCENT if r != 1 else MUTED, width=4 if r != 1 else 2.5),
                          run_time=0.2)
            self.play(FadeIn(c3.meters), run_time=0.3)
            e5 = tile("X", 0.26).move_to(c3.point(4, "start") + RIGHT * 0.27)
            self.play(TransformFromCopy(ex, e5), run_time=0.5)
            hits = [k for k, c in enumerate(cols) if c[1] == 4]
            ps = [self.pulse(self.trail([e5.get_center(), c3.point(4, k), c3.point(c[2], k),
                                         c3.point(c[2], "meter") + LEFT * 0.3]), run_time=0.8)
                  for k, c in ((k, cols[k]) for k in hits)]
            reads = VGroup(*[c3.readout(7 + r, b, size=24) for r, b in enumerate((1, 0, 1))])
            self.play(FadeIn(reads), *[FadeOut(p) for p in ps], run_time=0.5)
        # c9: column five of the table is the same 1 0 1
        col5 = SurroundingRectangle(VGroup(*[bits[r][4] for r in range(3)]), color=HILITE, buff=0.06)
        with self.voice("c9"):
            self.play(Create(col5), Indicate(reads, color=HILITE, scale_factor=1.2), run_time=0.7)
        # c10: any qubit: the syndrome is its address
        with self.voice("c10"):
            self.hold(1.6)
            for j in (3, 6, 7):
                b = [int(HAM[r][j - 1]) for r in range(3)]
                new_e = tile("X", 0.26).move_to(c3.point(j - 1, "start") + RIGHT * 0.27)
                new_col = SurroundingRectangle(VGroup(*[bits[r][j - 1] for r in range(3)]), color=HILITE, buff=0.06)
                new_reads = VGroup(*[c3.readout(7 + r, v, size=24) for r, v in enumerate(b)])
                self.play(Transform(e5, new_e), Transform(col5, new_col), Transform(reads, new_reads),
                          Indicate(qd[j], color=HILITE, scale_factor=1.4), run_time=0.7)
                self.hold(0.5)
            zn = VGroup(tile("Z", 0.3), T("on qubit 5:  X checks read", size=20, color=MUTED),
                        T("1", size=24, color=ACCENT, bold=True), T("0", size=24, bold=True),
                        T("1", size=24, color=ACCENT, bold=True)).arrange(RIGHT, buff=0.12)
            zn.next_to(c3, DOWN, buff=0.3)
            self.play(FadeIn(zn, shift=UP * 0.15), run_time=0.6)
            self.hold(1.0)
            stray = [m for m in self.stage() if not isinstance(m, VMobject)]
            self.remove(*stray)
            whole = VGroup(*self.stage())
            self.add_card("Steane", "[[7,1,3]]", src=whole)

    # ------------------------------------------------------------ D. the five-qubit code, and why five
    def five(self):
        self.clear_stage()
        S = 0.5
        rows = VGroup(*[pstring(s, s=S) for s in FIVE]).arrange(DOWN, buff=0.14).move_to([-3.3, 0.6, 0])
        # d1: one string, shifted along each time
        with self.voice("d1"):
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in rows[0]], lag_ratio=0.1), run_time=0.8)
            self.hold(1.6)
            for k in range(1, 4):
                src = rows[k - 1].copy()
                anims = [src[i].animate.move_to(rows[k][(i + 1) % 5]) for i in range(4)]
                anims.append(src[4].animate(path_arc=-PI / 2).move_to(rows[k][0]))
                self.play(*anims, run_time=0.7)
                self.remove(src, *src)       # the tiles were animated one by one, so each is on stage
                self.add(rows[k])
        fam = set(rows.get_family())
        self.remove(*[m for m in self.mobjects if m in fam])   # one group from here on, so it becomes its card in one piece
        self.add(rows)
        # d2: circuit 4: the mixed check, its gates lined up with the letters
        c4 = Circuit([str(j) for j in range(1, 6)], 1,
                     [("h", 5), ("ctrl", 5, {0: "X", 1: "Z", 2: "Z", 3: "X"}), ("h", 5)],
                     gap=0.5, step=0.95, lead=0.8, size=0.36)
        c4.move_to([2.6, 0.45, 0])
        fr = SurroundingRectangle(rows[0], color=HILITE, buff=0.06)
        with self.voice("d2"):
            self.play(Create(fr), run_time=0.4)
            self.play(Create(c4.wires), FadeIn(c4.labels), run_time=0.7)
            self.play(FadeIn(c4.cols[0]), FadeIn(c4.cols[2]), run_time=0.5)
            self.hold(0.8)
            gates = [m for m in c4.cols[1] if isinstance(m, VGroup)]
            self.play(FadeIn(VGroup(*[m for m in c4.cols[1] if not isinstance(m, VGroup)])), run_time=0.3)
            self.play(LaggedStart(*[TransformFromCopy(rows[0][i], g) for i, g in enumerate(gates)], lag_ratio=0.25),
                      run_time=1.4)
            self.play(FadeIn(c4.meters), run_time=0.3)
            self.play(Indicate(rows[0][4], color=HILITE), Indicate(c4.wires[4], color=HILITE), run_time=0.7)
        # d3: the five-qubit card; the board moves to the middle
        with self.voice("d3"):
            self.play(FadeOut(VGroup(c4, fr)), run_time=0.5)
            self.add_card("five-qubit", "[[5,1,3]]", src=rows)
            self.hold(1.2)
            self.play(self.board.animate.move_to([0, 2.85, 0]).scale(1.1), run_time=0.7)
        # d4: on n qubits: 3n errors, plus "no error"
        def case_col(n_rows):
            lines = VGroup()
            none = VGroup(Square(0.34, stroke_width=0, fill_color=INK, fill_opacity=1),
                          T("no error", size=18, color=MUTED)).arrange(RIGHT, buff=0.2)
            lines.add(none)
            for lab in n_rows:
                row = VGroup(T(lab, size=18, color=MUTED), *[tile(c, 0.34) for c in "XYZ"]).arrange(RIGHT, buff=0.1)
                lines.add(row)
            return lines.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        cases = case_col(["qubit 1", "qubit 2", "      ⋮", "qubit n"]).move_to([-4.3, 0.2, 0])
        cases[3].submobjects = cases[3].submobjects[:1]
        clab = M("3n + 1", size=40, color=INK).next_to(cases, DOWN, buff=0.35)
        with self.voice("d4"):
            self.hold(0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in cases[1:]], lag_ratio=0.25), run_time=1.3)
            self.hold(2.4)
            self.play(FadeIn(cases[0], shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(clab), run_time=0.5)
        # d5: n - 1 checks give 2^(n-1) syndromes; one case per slot
        slots = VGroup(*[RoundedRectangle(width=0.42, height=0.42, corner_radius=0.06, color=MUTED, stroke_width=2)
                         for _ in range(8)]).arrange_in_grid(2, 4, buff=0.14).move_to([3.4, 0.45, 0])
        slab = M("2^{n-1}", size=40).next_to(slots, DOWN, buff=0.4)
        slab_t = T("syndromes", size=20, color=MUTED).next_to(slots, UP, buff=0.25)
        clab_t = T("cases", size=20, color=MUTED).next_to(cases, UP, buff=0.25)
        ineq = M(r"3n + 1", r"\le", r"2^{n-1}", size=48).move_to([0, -1.55, 0])
        with self.voice("d5"):
            self.play(FadeIn(clab_t), run_time=0.3)
            self.hold(1.4)
            self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.08), FadeIn(slab_t), run_time=0.9)
            self.play(FadeIn(slab), run_time=0.5)
            self.hold(1.2)
            movers = [cases[0][0].copy(), cases[1][1].copy(), cases[1][2].copy(), cases[1][3].copy()]
            self.play(LaggedStart(*[m.animate.move_to(slots[k]).scale(0.85) for k, m in enumerate(movers)],
                                  lag_ratio=0.25), run_time=1.2)
            self.hold(1.0)
            self.play(TransformFromCopy(clab, ineq[0]), FadeIn(ineq[1]), TransformFromCopy(slab, ineq[2]), run_time=0.9)
        general = VGroup(cases, clab, slots, slab, *movers)
        # d6 / d7: n = 3, 4, 5, concretely
        def fill(n):
            m = 3 * n + 1
            s = 2 ** (n - 1)
            kinds = ["I"] + [c for _ in range(n) for c in "XYZ"]
            pieces = VGroup()
            for c in kinds:
                pieces.add(Square(0.3, stroke_width=0, fill_color=INK, fill_opacity=1) if c == "I" else tile(c, 0.3))
            pieces.arrange_in_grid(cols=4, buff=0.1).move_to([-4.0, 0.3, 0])
            cols = 4 if s <= 8 else 4
            box = VGroup(*[RoundedRectangle(width=0.36, height=0.36, corner_radius=0.05, color=MUTED, stroke_width=2)
                           for _ in range(s)]).arrange_in_grid(cols=cols, buff=0.1).move_to([3.4, 0.3, 0])
            nlab = M(f"n = {n}", size=40, color=HILITE).move_to([0, 1.7, 0])
            counts = VGroup(M(str(m), size=36).next_to(pieces, DOWN, buff=0.3),
                            M(str(s), size=36).next_to(box, DOWN, buff=0.3))
            return pieces, box, nlab, counts, min(m, s)
        state = {}

        def show(n, first=False):
            pieces, box, nlab, counts, k = fill(n)
            if first:
                self.play(FadeOut(general), FadeOut(clab_t), FadeOut(slab_t), run_time=0.5)
                self.play(FadeIn(nlab), FadeIn(pieces), FadeIn(box), FadeIn(counts), run_time=0.7)
            else:
                old = state["g"]
                self.play(FadeOut(old), run_time=0.4)
                self.play(FadeIn(nlab), FadeIn(pieces), FadeIn(box), FadeIn(counts), run_time=0.6)
            self.play(LaggedStart(*[pieces[i].animate.move_to(box[i]) for i in range(k)], lag_ratio=0.05),
                      run_time=1.0)
            if len(pieces) > k:
                self.play(VGroup(*pieces[k:]).animate.set_opacity(0.25), run_time=0.4)
            state["g"] = VGroup(pieces, box, nlab, counts)
        with self.voice("d6"):
            show(3, first=True)
        with self.voice("d7"):
            self.hold(0.3)
            show(4)
            self.hold(0.8)
            show(5)
            new = self.scoreboard("5").scale(1.1).move_to(self.board)
            self.play(Transform(self.board[1][2], new[1][2]), run_time=0.6)
            self.play(Indicate(self.board[1][2], color=HILITE, scale_factor=1.5), run_time=0.7)
        # d8: her nine comes back beside the five
        nine = M(r"3 \times 3 = 9", size=30, color=MUTED).next_to(self.board, RIGHT, buff=0.4)
        with self.voice("d8"):
            self.play(FadeIn(nine, shift=LEFT * 0.4), run_time=0.6)
        # d9: Shor's code gives Z1 and Z2 the same lamps
        rows78 = VGroup(*[pstring(SHOR[k], s=0.26, block=3) for k in (6, 7)]).arrange(DOWN, buff=0.1)

        def shor_panel(q, x):
            e = pstring("I" * q + "Z" + "I" * (8 - q), s=0.26, block=3)
            r = rows78.copy()
            ls = VGroup(*[lamp("-" if anticommutes(SHOR[k], "I" * q + "Z" + "I" * (8 - q)) else "+", r=0.1)
                          .next_to(rr, RIGHT, buff=0.2) for k, rr in zip((6, 7), r)])
            lab = M(f"Z_{q + 1}", size=34, color=Z_TILE)
            g = VGroup(e, VGroup(r, ls)).arrange(DOWN, buff=0.3)
            lab.next_to(g, UP, buff=0.2)
            return VGroup(lab, g).move_to([x, 0.1, 0])
        p1 = shor_panel(0, -3.2)
        p2 = shor_panel(1, 2.0)
        eq = M("=", size=48).move_to([-0.6, -0.3, 0])
        with self.voice("d9"):
            self.play(FadeOut(VGroup(state["g"], ineq)), run_time=0.5)
            self.play(Indicate(self.cards[0], color=HILITE, scale_factor=1.15), run_time=0.7)
            self.hold(2.5)
            self.play(TransformFromCopy(self.cards[0], p1), run_time=0.8)
            self.play(TransformFromCopy(self.cards[0], p2), run_time=0.8)
            self.hold(0.6)
            self.play(Indicate(p1[1][1][1], color=HILITE), Indicate(p2[1][1][1], color=HILITE), FadeIn(eq), run_time=0.8)
        # d10: Z1 Z2 is a check, so mixing them up does nothing; and five holds for any code
        prod = pstring(SHOR[0], s=0.32, block=3).move_to([0, -1.9, 0])
        plab = VGroup(T("a check: does nothing", size=20, color=MUTED), mark(True)).arrange(RIGHT, buff=0.15)
        plab.next_to(prod, RIGHT, buff=0.35)
        anyc = T("for any code", size=18, color=MUTED).next_to(self.board, DOWN, buff=0.12)
        with self.voice("d10"):
            self.play(TransformFromCopy(VGroup(p1[1][0], p2[1][0]), prod), run_time=0.9)
            self.play(FadeIn(plab), run_time=0.5)
            self.hold(2.2)
            self.play(FadeIn(anyc, shift=UP * 0.1), run_time=0.5)
        self.remove(anyc)
        self.board.add(anyc)
        self.clear_stage()

    # ------------------------------------------------------------ E. closing
    def closing(self):
        self.clear_stage()
        lists = {"Shor": SHOR, "Steane": STEANE, "five-qubit": FIVE}
        xs = [-4.2, 0.0, 4.2]
        with self.voice("e1"):
            anims = []
            for c, x in zip(self.cards, xs):
                anims.append(c.animate.scale(1.25).move_to([x, 1.6, 0]))
            self.play(*anims, run_time=0.9)
            full = VGroup(*[Square(0.2, stroke_width=0, fill_color=INK, fill_opacity=1) for _ in range(16)])
            full.arrange_in_grid(4, 4, buff=0.06).next_to(self.cards[-1], DOWN, buff=0.35)
            self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in full], lag_ratio=0.04), run_time=0.9)
        with self.voice("e2"):
            self.play(FadeOut(full), run_time=0.3)
            shown = []
            for c, name in zip(self.cards, ["Shor", "Steane", "five-qubit"]):
                g = VGroup(*[pstring(s, s=0.16, buff=0.03) for s in lists[name]]).arrange(DOWN, buff=0.05)
                g.next_to(c, DOWN, buff=0.3)
                shown.append(g)
            self.play(*[LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.1) for g in shown], run_time=1.0)
        nxt = VGroup(T("Next", size=26, color=MUTED), T("8.4  CSS codes", size=50, bold=True))
        nxt.arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        with self.voice("e3"):
            self.hold(2.0)
            self.play(*[FadeOut(m) for m in self.stage() + self.cards + [self.board]], run_time=0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
