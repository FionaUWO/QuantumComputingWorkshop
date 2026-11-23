"""Section 8.1 — The Pauli group and stabilizers.   Draft.
Build from the video folder with the Manim environment:
    python pipeline/build.py 8.1 render --low        (ONLY=<letters> renders chosen scenes)
Narration ids (a1, a2, ...) match script.py and storyboard.md. The film is a dialogue; who
speaks does not change the picture, only the colour of the subtitle.
Colours in this section (storyboard.md has the table): a purple tile is the letter X, a green
tile the letter Z, a dark tile the identity. Orange stays what it was in lecture 1: a minus
sign, here also the answer -1. Cyan marks what to look at and the part of the space that is kept.
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from common import *  # noqa: E402,F401
DROP = 0.4            # the camera looks this much higher, which centres the picture (as in 1.2)
TS = 0.66             # side of a letter tile
X_TILE, Z_TILE = PURPLE, GOOD

def tile(ch, s=TS):
    """One letter of a Pauli string. tile.ch is the letter."""
    col = {"X": X_TILE, "Z": Z_TILE, "Y": X_TILE, "I": DIM}[ch]
    box = RoundedRectangle(width=s, height=s, corner_radius=0.12 * s, stroke_width=0, fill_color=col, fill_opacity=1)
    g = VGroup(box)
    if ch == "Y":                                   # Y is X and Z together: half of each colour
        g.add(Polygon(box.get_corner(UR) + s * 0.1 * DL, box.get_corner(DR) + s * 0.1 * UL,
                      box.get_corner(DL) + s * 0.1 * UR, stroke_width=0, fill_color=Z_TILE, fill_opacity=1))
    if ch == "I":
        g.add(Dot(box.get_center(), radius=0.05 * s / TS, color=MUTED))
    else:
        g.add(T(ch, size=34 * s / TS, color=BG if ch == "Z" else INK, bold=True).move_to(box))
    g.ch = ch
    return g

def pstring(letters, s=TS, buff=None):
    """A Pauli string: a row of tiles."""
    return VGroup(*[tile(c, s) for c in letters]).arrange(RIGHT, buff=0.12 * s if buff is None else buff)

def minus(size=54):
    return M("-", size=size, color=ACCENT)

def answer(plus, size=34):
    """The answer of a question: +1 in white, -1 in orange."""
    return M("+1", size=size, color=INK) if plus else M("-", "1", size=size, color=ACCENT)

class Main(NarratedScene):
    EP = "8.1"
    SCENES = [("i", "opening"), ("a", "hook"), ("b", "alphabet"), ("c", "commute"), ("d", "bell"),
              ("e", "halving"), ("f", "cost"), ("g", "closing")]
    def construct(self):
        only = os.environ.get("ONLY", "")
        self.busy = {}
        self.head = header("8.1  The Pauli group and stabilizers")
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
        """As in NarratedScene, and two things more. The holds inside a line were written for the
        speed the silent draft assumes (150 words a minute); once the line has been recorded they
        are scaled to its real length, so the picture keeps its place inside the sentence. And the
        time the picture is busy during each line is noted, to catch a line whose animation
        outlasts its voice (written to out/.../busy.json)."""
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
        """Everything on screen except the header and the watermark."""
        return [m for m in self.mobjects if m is not self.head and m is not self.wm]
    def clear_stage(self, run_time=0.6):
        self.card_mob = None
        left = self.stage()
        if left:
            self.play(*[FadeOut(m) for m in left], run_time=run_time)
    # ------------------------------------------------------------ I. opening
    def opening(self):
        """Who is speaking, then what this section is about: the same card as sections 1.1 and 1.2."""
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
        title = T("The Pauli group and stabilizers", size=50, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 8  ·  Section 8.1", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = mark.copy().set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)
    # ------------------------------------------------------------ A. two descriptions of one code
    LX, RX_ = -3.4, 3.3           # centres of the two descriptions
    TOP = 2.35                    # top of both columns
    def amp_rows(self, n, lit, pitch=None):
        """The amplitude table of n qubits as 2^n thin rows; `lit` are the rows that are not zero."""
        pitch = pitch or max(0.42 * 0.72 ** (n - 3), 0.012)
        rows = VGroup()
        for k in range(2 ** n):
            on = k in lit
            r = Rectangle(width=2.2, height=pitch * 0.62, stroke_width=0, fill_color=HILITE if on else MUTED,
                          fill_opacity=1 if on else 0.28)
            r.move_to([self.LX + 0.45, self.TOP - (k + 0.5) * pitch, 0])
            rows.add(r)
        return rows
    def check_list(self, n):
        """The checks of the repetition code on n qubits: Z on each neighbouring pair."""
        s = min(TS, 3.9 / n)
        rows = VGroup(*[pstring(["Z" if j in (i, i + 1) else "I" for j in range(n)], s) for i in range(n - 1)])
        rows.arrange(DOWN, buff=0.16 * s / TS)
        return rows.move_to([self.RX_, 0, 0]).align_to([0, self.TOP, 0], UP)
    def hook(self):
        title = T("bit flip code", size=40, bold=True).move_to([0, 0.6, 0])
        cap_l = T("its states", size=24, color=MUTED).move_to([self.LX, 2.95, 0])
        cap_r = T("its questions", size=24, color=MUTED).move_to([self.RX_, 2.95, 0])
        with self.voice("a1"):
            self.play(FadeIn(title, shift=UP * 0.2), run_time=0.6)
            self.hold(1.2)
            self.play(title.animate.scale(0.6).move_to([0, 2.95, 0]), run_time=0.7)
            self.play(FadeIn(cap_l), FadeIn(cap_r), run_time=0.5)
        # a2: the eight basis states; the code uses the first and the last
        rows = self.amp_rows(3, lit=(0, 7))
        names = VGroup(*[M(rf"|{k:03b}\rangle", size=28, color=HILITE if k in (0, 7) else MUTED)
                         .next_to(rows[k], LEFT, buff=0.25) for k in range(8)])
        for r in rows:
            r.save_state()
            r.set_fill(MUTED, opacity=0.28)
        with self.voice("a2"):
            self.play(LaggedStart(*[FadeIn(VGroup(nm, r), shift=RIGHT * 0.15) for nm, r in zip(names, rows)],
                                  lag_ratio=0.12, run_time=1.6))
            self.hold(2.6)
            self.play(Restore(rows[0]), Restore(rows[7]), run_time=0.6)
        # a3: the two checks
        checks = self.check_list(3)
        with self.voice("a3"):
            self.hold(1.4)
            self.play(FadeIn(checks[0], shift=LEFT * 0.2), run_time=0.6)
            self.hold(1.6)
            self.play(FadeIn(checks[1], shift=LEFT * 0.2), run_time=0.6)
            self.hold(1.0)
            self.play(Indicate(checks[0], color=HILITE, scale_factor=1.12), run_time=0.8)
            self.play(Indicate(checks[1], color=HILITE, scale_factor=1.12), run_time=0.8)
        # a4: more qubits. The table doubles each time, the list grows by one line
        count = M("n = 3", size=40).move_to([0, 1.6, 0])
        with self.voice("a4"):
            self.play(FadeIn(count), FadeOut(names), run_time=0.5)
            for n in range(4, 9):
                new_rows = self.amp_rows(n, lit=(0, 2 ** n - 1))
                new_checks = self.check_list(n)
                new_count = M(f"n = {n}", size=40).move_to(count)
                self.remove(*rows.get_family(), *checks.get_family(), count)
                self.add(new_rows, new_checks, new_count)
                rows, checks, count = new_rows, new_checks, new_count
                self.wait(0.55)
        # a5: what if only the rows that are not zero were kept?
        with self.voice("a5"):
            self.play(*[r.animate.set_fill(opacity=0.08) for r in rows[1:-1]], run_time=0.8)
        # a6: in a larger code the rows that are not zero double as well
        frame = SurroundingRectangle(checks, color=HILITE, buff=0.18, corner_radius=0.12)
        nz = M(r"\text{not zero: }", "2", size=32, color=HILITE).move_to([self.LX + 0.45, 2.95 - 0.02, 0])
        with self.voice("a6"):
            self.play(FadeOut(cap_l), FadeIn(nz), run_time=0.5)
            self.hold(2.0)
            rng = np.random.default_rng(8)
            for m in (4, 8, 16, 32, 64):
                on = set(rng.choice(256, size=m, replace=False).tolist()) | {0, 1, 2, 3, 5, 8, 11, 14}
                new_rows = self.amp_rows(8, lit=on)
                for k, r in enumerate(new_rows):
                    if k not in on:
                        r.set_fill(opacity=0.08)
                new_nz = M(r"\text{not zero: }", str(m), size=32, color=HILITE).move_to(nz)
                self.remove(*rows.get_family(), nz)
                self.add(new_rows, new_nz)
                rows, nz = new_rows, new_nz
                self.wait(0.5)
            self.play(Create(frame), run_time=0.7)
        with self.voice("a7"):
            self.hold(3.0)
            self.clear_stage(0.8)
    # ------------------------------------------------------------ B. the alphabet; a string is a question
    def alphabet(self):
        self.clear_stage()
        letters = pstring("IXYZ", s=1.0, buff=0.35).move_to([0, 1.7, 0])
        with self.voice("b1"):
            self.hold(1.8)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in letters], lag_ratio=0.35, run_time=1.8))
        # b2: one letter for each qubit
        ys = [0.75, -0.15, -1.05]
        wires = VGroup(*[Line([-3.2, y, 0], [3.2, y, 0], color=MUTED, stroke_width=2) for y in ys])
        nums = VGroup(*[T(str(k + 1), size=24, color=MUTED).move_to([-3.6, y, 0]) for k, y in enumerate(ys)])
        on_wire = VGroup(*[tile(c).move_to([0, y, 0]) for c, y in zip("XIZ", ys)])
        src = {"X": letters[1], "I": letters[0], "Z": letters[3]}
        row = pstring("XIZ").move_to([-0.6, -0.15, 0])
        name = M("X_1 Z_3", size=44).next_to(row, RIGHT, buff=0.6)
        with self.voice("b2"):
            self.play(letters.animate.scale(0.6).move_to([0, 2.5, 0]), FadeIn(wires), FadeIn(nums), run_time=0.8)
            self.hold(2.6)
            for t in on_wire:
                self.play(TransformFromCopy(src[t.ch], t), run_time=0.7)
                self.hold(0.9)
            self.play(FadeOut(wires), FadeOut(nums),
                      *[ReplacementTransform(a, b) for a, b in zip(on_wire, row)], run_time=0.9)
            self.play(FadeIn(name, shift=LEFT * 0.2), run_time=0.5)
        # b3: a sign in front; the name of the whole collection
        slot = RoundedRectangle(width=0.95, height=TS, corner_radius=0.08, color=MUTED, stroke_width=2)
        slot.next_to(row, LEFT, buff=0.16)
        sign = M("+1", size=30).move_to(slot)
        with self.voice("b3"):
            self.play(FadeIn(slot), FadeIn(sign), run_time=0.5)
            for tex, col in (("-1", ACCENT), ("+i", INK), ("-i", ACCENT), ("+1", INK)):
                new = M(tex, size=30, color=col).move_to(slot)
                self.play(ReplacementTransform(sign, new), run_time=0.35)
                sign = new
                self.hold(0.25)
            self.card("Pauli group", "all strings of I, X, Y and Z, with a sign in front")
        ask = M("?", size=110, color=HILITE).next_to(row, UP, buff=0.35)
        with self.voice("b4"):
            self.play(FadeIn(ask, scale=0.6), run_time=0.5)
        # b5: a question with two answers
        q = pstring("ZZI").move_to([-0.6, -0.15, 0])
        out_p = VGroup(T("answer", size=20, color=MUTED), answer(True, 44)).arrange(RIGHT, buff=0.25).move_to([4.6, 0.55, 0])
        out_m = VGroup(T("answer", size=20, color=MUTED), answer(False, 44)).arrange(RIGHT, buff=0.25).move_to([4.6, -0.85, 0])
        with self.voice("b5"):
            self.uncard()
            self.play(FadeOut(VGroup(slot, sign, name, letters)), FadeOut(ask),
                      *[ReplacementTransform(a, b) for a, b in zip(row, q)], run_time=0.9)
            self.hold(1.0)
            self.play(FadeIn(out_p, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(out_m, shift=LEFT * 0.2), run_time=0.5)
        def feed(bits):
            """A basis state above the string, one bit over each tile."""
            ds = VGroup(*[M(b, size=48, color=HILITE).next_to(t, UP, buff=0.45) for b, t in zip(bits, q)])
            ket = VGroup(M("|", size=48, color=HILITE).next_to(ds[0], LEFT, buff=0.16),
                         M(r"\rangle", size=48, color=HILITE).next_to(ds[-1], RIGHT, buff=0.16))
            return ds, ket
        def signs(bits):
            """A minus sign under every Z that sits on a one."""
            return [minus().next_to(t, DOWN, buff=0.4) for b, t in zip(bits, q) if b == "1" and t.ch == "Z"]
        # b6: 110, two minus signs, they cancel
        ds, ket = feed("110")
        with self.voice("b6"):
            self.play(FadeIn(ds), FadeIn(ket), run_time=0.6)
            self.hold(3.4)
            ms = signs("110")
            for d, m in zip(ds[:2], ms):
                self.play(Indicate(d, color=ACCENT, scale_factor=1.3), FadeIn(m, shift=DOWN * 0.3), run_time=0.7)
            self.hold(0.6)
            mid = (ms[0].get_center() + ms[1].get_center()) / 2
            self.play(ms[0].animate.move_to(mid), ms[1].animate.move_to(mid), run_time=0.5)
            self.play(FadeOut(VGroup(*ms), scale=0.2), run_time=0.3)
            self.play(Indicate(out_p[1], color=HILITE, scale_factor=1.5), run_time=0.8)
        # b7: 100, one minus sign, nothing cancels it
        ds2, _ = feed("100")
        with self.voice("b7"):
            self.play(ReplacementTransform(ds, ds2), run_time=0.6)
            self.hold(1.6)
            m = signs("100")[0]
            self.play(Indicate(ds2[0], color=ACCENT, scale_factor=1.3), FadeIn(m, shift=DOWN * 0.3), run_time=0.7)
            self.hold(1.4)
            self.play(Indicate(out_m[1], color=ACCENT, scale_factor=1.5), run_time=0.8)
    # ------------------------------------------------------------ C. two questions: commute or anticommute
    def scan(self, top, bot, y_tokens, run=0.45):
        """A frame runs over two stacked strings slot by slot. A slot where the letters differ and
        neither is the identity flashes and drops a minus sign. Returns the frame and the signs."""
        frame = RoundedRectangle(width=TS + 0.2, height=top.get_top()[1] - bot.get_bottom()[1] + 0.24,
                                 corner_radius=0.1, color=HILITE, stroke_width=3)
        x0 = top[0].get_center()[0]
        mid_y = (top.get_top()[1] + bot.get_bottom()[1]) / 2
        frame.move_to([x0 - TS - 0.3, mid_y, 0])
        return frame, mid_y
    def run_scan(self, frame, mid_y, top, bot, y_tokens, run=0.45):
        tokens = []
        for a, b in zip(top, bot):
            self.play(frame.animate.move_to([a.get_center()[0], mid_y, 0]), run_time=run)
            if a.ch != b.ch and "I" not in (a.ch, b.ch):
                tok = minus().move_to([a.get_center()[0], y_tokens, 0])
                self.play(frame.animate(rate_func=there_and_back).set_stroke(ACCENT, width=6),
                          FadeIn(tok, shift=DOWN * 0.3), run_time=0.6)
                tokens.append(tok)
            else:
                self.hold(0.25)
        return tokens
    def commute(self):
        self.clear_stage()
        x, z = tile("X", 0.9).move_to([0, 1.5, 0]), tile("Z", 0.9).move_to([0, 0.3, 0])
        with self.voice("c1"):
            self.hold(2.0)
            self.play(FadeIn(x, shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(z, shift=UP * 0.2), run_time=0.5)
        # c2: swap the two, and a minus sign appears
        m = minus(72).move_to([-1.3, 0.9, 0])
        rule = M("X", "Z", "=", "-", "Z", "X", size=52).move_to([0, -1.1, 0])
        rule[0].set_color(X_TILE), rule[5].set_color(X_TILE), rule[1].set_color(Z_TILE), rule[4].set_color(Z_TILE)
        rule[3].set_color(ACCENT)
        with self.voice("c2"):
            self.hold(2.4)
            self.play(x.animate(path_arc=PI).move_to(z.get_center()), z.animate(path_arc=PI).move_to(x.get_center()),
                      run_time=1.0)
            self.play(FadeIn(m, scale=2.0), run_time=0.4)
            self.hold(0.6)
            self.play(FadeIn(rule[:3]), TransformFromCopy(m, rule[3]), FadeIn(rule[4:]), run_time=0.8)
            self.hold(1.8)
            self.card("anticommute", "swapping the order of the two costs a minus sign")
        # c3: longer strings, slot by slot
        top, bot = pstring("XZZXI").move_to([0, 1.5, 0]), pstring("IXZZX").move_to([0, 0.55, 0])
        with self.voice("c3"):
            self.uncard()
            self.play(FadeOut(VGroup(x, z, m, rule)), run_time=0.5)
            self.play(FadeIn(top), FadeIn(bot), run_time=0.6)
            frame, mid_y = self.scan(top, bot, -0.45)
            self.play(FadeIn(frame), run_time=0.3)
            tokens = self.run_scan(frame, mid_y, top, bot, -0.45, run=0.6)
        # c4: X X against Z Z, and a pause to think
        top2, bot2 = pstring("XX").move_to([0, 1.5, 0]), pstring("ZZ").move_to([0, 0.55, 0])
        frame2, mid_y = self.scan(top2, bot2, -0.45)
        with self.voice("c4"):
            self.play(FadeOut(VGroup(*tokens)), FadeOut(top), FadeOut(bot), FadeOut(frame), run_time=0.5)
            self.hold(1.4)
            self.play(FadeIn(top2), run_time=0.5)
            self.hold(1.2)
            self.play(FadeIn(bot2), run_time=0.5)
            self.play(FadeIn(frame2), run_time=0.3)
        with self.voice("c5"):
            self.play(Indicate(frame2, color=HILITE, scale_factor=1.08), run_time=0.8)
        # c6: two slots, two minus signs, they cancel
        verdict = T("commute", size=40, bold=True).move_to([0, -0.45, 0])
        with self.voice("c6"):
            self.hold(2.6)
            toks = self.run_scan(frame2, mid_y, top2, bot2, -0.45, run=0.6)
            self.hold(1.6)
            self.play(toks[0].animate.move_to([0, -0.45, 0]), toks[1].animate.move_to([0, -0.45, 0]), run_time=0.5)
            self.play(FadeOut(VGroup(*toks), scale=0.2), FadeIn(verdict, scale=0.7), run_time=0.5)
        # c7: the rule
        even = VGroup(T("even number of clashes", size=26), T("commute", size=26, bold=True)
                      ).arrange(RIGHT, buff=0.5).move_to([0, -1.5, 0])
        odd = VGroup(T("odd number of clashes", size=26), T("anticommute", size=26, color=ACCENT, bold=True)
                     ).arrange(RIGHT, buff=0.5).move_to([0, -2.15, 0])
        none = T("no state answers +1 to both", size=22, color=MUTED).next_to(odd, RIGHT, buff=0.5)
        VGroup(odd, none).move_to([0, -2.15, 0])
        with self.voice("c7"):
            self.play(FadeOut(frame2), run_time=0.3)
            self.hold(1.2)
            self.play(FadeIn(even, shift=UP * 0.15), run_time=0.5)
            self.hold(2.4)
            self.play(FadeIn(odd, shift=UP * 0.15), run_time=0.5)
            self.hold(1.6)
            self.play(FadeIn(none, shift=LEFT * 0.15), run_time=0.5)
    # ------------------------------------------------------------ D. the space a list fixes
    def list_box(self, strings, x=-4.9, y=0.9, title="list"):
        rows = VGroup(*[pstring(s) for s in strings]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        box = SurroundingRectangle(rows, color=MUTED, buff=0.22, corner_radius=0.14, stroke_width=1.6)
        g = VGroup(box, rows).move_to([x, y, 0])
        g.rows, g.box = rows, box
        g.title = T(title, size=22, color=MUTED).next_to(box, UP, buff=0.18)
        return g
    def bell(self):
        self.clear_stage()
        lst = self.list_box(["XX", "ZZ"])
        xs = [-1.0, 0.6, 2.2, 3.8]
        base, full = -0.5, 1.9
        kets = VGroup(*[M(rf"|{k:02b}\rangle", size=34).move_to([x, base - 0.4, 0]) for k, x in enumerate(xs)])
        line = Line([xs[0] - 0.8, base, 0], [xs[-1] + 0.8, base, 0], color=MUTED, stroke_width=2)
        hs = [ValueTracker(v) for v in (0.85, 0.5, 0.65, 0.4)]
        def bar(k):
            return always_redraw(lambda: Rectangle(
                width=0.7, height=max(hs[k].get_value() * full, 0.02), stroke_width=0, fill_color=HILITE,
                fill_opacity=1).move_to([xs[k], base + max(hs[k].get_value() * full, 0.02) / 2, 0]))
        bars_ = [bar(k) for k in range(4)]
        with self.voice("d1"):
            self.play(FadeIn(lst), FadeIn(lst.title), run_time=0.7)
        # d2: Z Z keeps 00 and 11
        pick_z = SurroundingRectangle(lst.rows[1], color=HILITE, buff=0.08, corner_radius=0.1)
        knife = Line([xs[0] - 1.0, base + full + 0.5, 0], [xs[0] - 1.0, base - 0.75, 0], color=HILITE, stroke_width=4)
        with self.voice("d2"):
            self.play(FadeIn(line), FadeIn(kets), *[FadeIn(b) for b in bars_], run_time=0.8)
            self.hold(2.0)
            self.play(Create(pick_z), run_time=0.4)
            self.play(FadeIn(knife), run_time=0.2)
            self.play(knife.animate.shift(RIGHT * (xs[-1] - xs[0] + 2.0)), hs[1].animate.set_value(0),
                      hs[2].animate.set_value(0), kets[1].animate.set_opacity(0.25),
                      kets[2].animate.set_opacity(0.25), run_time=1.4)
            self.play(FadeOut(knife), run_time=0.2)
        # d3: X X swaps the two that are left, so they must be equal
        pick_x = SurroundingRectangle(lst.rows[0], color=HILITE, buff=0.08, corner_radius=0.1)
        swap = CurvedDoubleArrow([xs[0], base + full + 0.25, 0], [xs[3], base + full + 0.25, 0], angle=-0.5,
                                 color=X_TILE, stroke_width=4, tip_length=0.2)
        with self.voice("d3"):
            self.play(ReplacementTransform(pick_z, pick_x), run_time=0.4)
            self.play(Create(swap), run_time=0.6)
            for _ in range(2):
                a, b = hs[0].get_value(), hs[3].get_value()
                self.play(hs[0].animate.set_value(b), hs[3].animate.set_value(a), run_time=0.8)
            self.hold(0.5)
            self.play(hs[0].animate.set_value(0.62), hs[3].animate.set_value(0.62), run_time=0.8)
        with self.voice("d4"):
            self.play(FadeOut(swap), FadeOut(pick_x), run_time=0.4)
        # d5: one state from two strings
        state = M(r"\tfrac{1}{\sqrt2}\big(|00\rangle + |11\rangle\big)", size=40, color=HILITE).move_to([1.4, -1.75, 0])
        frame = SurroundingRectangle(lst.box, color=HILITE, buff=0.1, corner_radius=0.16)
        with self.voice("d5"):
            self.hold(1.6)
            self.play(FadeIn(state, shift=UP * 0.2), run_time=0.6)
            self.hold(3.0)
            self.play(Create(frame), run_time=0.6)
        # d6: the names, after the thing itself
        vs = M("V_S", size=44, color=HILITE).move_to([1.4, 2.55, 0])
        sname = T("stabilizer S", size=24, color=HILITE).move_to(lst.title)
        with self.voice("d6"):
            self.hold(2.6)
            self.play(FadeIn(vs, shift=DOWN * 0.2), run_time=0.6)
            self.hold(3.0)
            self.play(FadeOut(frame), ReplacementTransform(lst.title, sname), run_time=0.6)
        gens = T("generators", size=22, color=MUTED).next_to(lst.box, DOWN, buff=0.2)
        with self.voice("d7"):
            self.hold(1.4)
            self.play(FadeIn(gens, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(lst.rows, color=HILITE, scale_factor=1.08), run_time=0.9)
    # ------------------------------------------------------------ E. every check halves the space
    GC = np.array([0.5, 0.75, 0.0])      # centre of the 2 x 2 picture of three qubits
    CW, CH = 3.0, 1.35
    def grid(self):
        """The eight basis states of three qubits in four cells, sorted by the two checks of the bit
        flip code: columns by Z1 Z2, rows by Z2 Z3. Returns {(col, row): VGroup(box, text)}."""
        txt = {(0, 0): r"|000\rangle,\ |111\rangle", (1, 0): r"|100\rangle,\ |011\rangle",
               (0, 1): r"|001\rangle,\ |110\rangle", (1, 1): r"|010\rangle,\ |101\rangle"}
        cells = {}
        for (c, r), s in txt.items():
            box = Rectangle(width=self.CW, height=self.CH, color=MUTED, stroke_width=2)
            box.move_to(self.GC + [(c - 0.5) * self.CW, (0.5 - r) * self.CH, 0])
            cells[(c, r)] = VGroup(box, M(s, size=30).move_to(box))
        return cells
    def dim(self, cell, to=0.22):
        return [cell[0].animate.set_stroke(opacity=to), cell[1].animate.set_opacity(to)]
    def number(self, tex, color=INK):
        return M(tex, size=72, color=color).move_to([5.45, 0.55, 0])
    def halving(self):
        self.clear_stage()
        lst = self.list_box(["ZZI", "IZZ"], x=-5.0, y=0.9, title="checks")
        cells = self.grid()
        allc = VGroup(*cells.values())
        dlabel = T("dimension", size=22, color=MUTED).move_to([5.45, 1.5, 0])
        num = self.number("8")
        with self.voice("e1"):
            self.play(FadeIn(lst), FadeIn(lst.title), run_time=0.6)
            self.hold(1.4)
            self.play(LaggedStart(*[FadeIn(c) for c in cells.values()], lag_ratio=0.2, run_time=1.2))
            self.play(FadeIn(dlabel), FadeIn(num), run_time=0.5)
        # e2: the first check keeps the left column
        left, right = self.GC[0] - self.CW / 2, self.GC[0] + self.CW / 2
        top, bottom = self.GC[1] + self.CH, self.GC[1] - self.CH
        pick = SurroundingRectangle(lst.rows[0], color=HILITE, buff=0.08, corner_radius=0.1)
        cut1 = Line([self.GC[0], top + 0.3, 0], [self.GC[0], bottom - 0.3, 0], color=HILITE, stroke_width=5)
        cp = answer(True).move_to([left, top + 0.4, 0])
        cm = answer(False).move_to([right, top + 0.4, 0])
        with self.voice("e2"):
            self.play(Create(pick), run_time=0.4)
            self.hold(2.4)
            self.play(Create(cut1), run_time=0.7)
            self.play(FadeIn(cp), FadeIn(cm), run_time=0.4)
            self.hold(1.2)
            new = self.number("4")
            self.play(*self.dim(cells[(1, 0)]), *self.dim(cells[(1, 1)]), ReplacementTransform(num, new), run_time=0.8)
            num = new
        # e3: the second check cuts across
        pick2 = SurroundingRectangle(lst.rows[1], color=HILITE, buff=0.08, corner_radius=0.1)
        x_l, x_r = self.GC[0] - self.CW, self.GC[0] + self.CW
        cut2 = Line([x_l - 0.3, self.GC[1], 0], [x_r + 0.3, self.GC[1], 0], color=HILITE, stroke_width=5)
        rp = answer(True).move_to([x_l - 0.55, self.GC[1] + self.CH / 2, 0])
        rm = answer(False).move_to([x_l - 0.55, self.GC[1] - self.CH / 2, 0])
        with self.voice("e3"):
            self.play(ReplacementTransform(pick, pick2), run_time=0.4)
            self.hold(1.8)
            self.play(Create(cut2), run_time=0.7)
            self.play(FadeIn(rp), FadeIn(rm), run_time=0.4)
            self.play(*self.dim(cells[(0, 1)]), run_time=0.8)
        # e4, e5: how many are left? (nothing new during the pause)
        ask = self.number("?", HILITE)
        with self.voice("e4"):
            self.play(FadeOut(pick2), ReplacementTransform(num, ask), run_time=0.5)
            self.play(Indicate(cells[(0, 0)][0], color=HILITE, scale_factor=1.03), run_time=0.9)
        num = ask
        with self.voice("e5"):
            for tex in ("8", "4", "2"):
                new = self.number(tex)
                self.play(ReplacementTransform(num, new), run_time=0.3)
                num = new
                self.hold(0.35)
        # e6: the code space
        glow = Rectangle(width=self.CW, height=self.CH, stroke_color=HILITE, stroke_width=5, fill_color=HILITE,
                         fill_opacity=0.18).move_to(cells[(0, 0)][0])
        tag = T("code space", size=20, color=HILITE).move_to(cells[(0, 0)][0].get_bottom() + UP * 0.24)
        two = M("2", "= 2^1", size=44).move_to([5.45, 0.55, 0])
        with self.voice("e6"):
            self.play(FadeIn(glow), cells[(0, 0)][1].animate.shift(UP * 0.14), run_time=0.6)
            self.hold(1.6)
            self.play(ReplacementTransform(num, two), run_time=0.5)
            self.hold(1.8)
            self.play(FadeIn(tag), run_time=0.4)
        num = two
        # e7: any number of qubits. A long bar halved again and again, and only then the formula
        bx, bw, by = -5.9, 8.4, -2.05
        bar = Rectangle(width=bw, height=0.34, stroke_width=0, fill_color=MUTED, fill_opacity=0.35)
        bar.move_to([bx + bw / 2, by, 0])
        lab = M("2^n", size=32).next_to(bar, UP, buff=0.12).align_to(bar, RIGHT)
        formula = M(r"\dim V_S = 2^k", size=42, color=HILITE).move_to([4.6, by + 0.05, 0])
        halves = []
        with self.voice("e7"):
            self.hold(2.6)
            self.play(FadeIn(bar), FadeIn(lab), run_time=0.6)
            self.hold(1.6)
            w = bw
            for k, tex in enumerate(("2^{n-1}", "2^{n-2}", r"\cdots", "2^k")):
                w = w / 2
                h = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=HILITE,
                              fill_opacity=0.3 + 0.2 * k).move_to([bx + w / 2, by, 0])
                hl = M(tex, size=30, color=HILITE).next_to(h, DOWN, buff=0.12).align_to(h, RIGHT)
                self.play(FadeIn(h), FadeIn(hl), run_time=0.5)
                halves += [h, hl]
                self.hold(0.7)
            self.hold(1.4)
            self.play(FadeIn(formula, shift=LEFT * 0.2), run_time=0.6)
        # e8: a third check, proposed
        third = pstring("ZIZ").next_to(lst.rows, DOWN, buff=0.16, aligned_edge=LEFT)
        third.set_opacity(0.45)
        box3 = SurroundingRectangle(VGroup(lst.rows, third), color=MUTED, buff=0.22, corner_radius=0.14,
                                    stroke_width=1.6)
        with self.voice("e8"):
            self.play(FadeOut(VGroup(bar, lab, formula, *halves)), run_time=0.5)
            self.play(FadeIn(third), ReplacementTransform(lst.box, box3), run_time=0.6)
        lst.box = box3
        # e9: it is the product of the other two, so it cuts nothing
        marks = [SurroundingRectangle(cells[k][0], color=ACCENT, buff=-0.08, stroke_width=4) for k in ((1, 0), (0, 1))]
        with self.voice("e9"):
            self.hold(2.6)
            third.set_opacity(1)
            self.play(TransformFromCopy(lst.rows[0], third), TransformFromCopy(lst.rows[1], third.copy()), run_time=1.0)
            self.hold(1.6)
            # Z1 Z3 answers -1 on the two cells that are already dark: nothing new goes
            self.play(*[Create(m) for m in marks], run_time=0.6)
            self.hold(0.5)
            self.play(*[FadeOut(m) for m in marks], Indicate(num[0], color=HILITE, scale_factor=1.5), run_time=0.9)
        strike = Line(third.get_left() + LEFT * 0.1, third.get_right() + RIGHT * 0.1, color=ACCENT, stroke_width=5)
        with self.voice("e10"):
            self.play(Create(strike), run_time=0.5)
            self.card("independent", "no check in the list is a product of the others")
        self.hold(0.3)
        self.uncard()
    # ------------------------------------------------------------ F. what each description costs
    def cost(self):
        self.clear_stage()
        n = M("n = 50", size=44).move_to([0, 2.8, 0])
        # the list: a block of small tiles stands for fifty strings of fifty letters
        rng = np.random.default_rng(3)
        block = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_opacity=1,
                                fill_color=[DIM, DIM, Z_TILE, X_TILE][rng.integers(4)]) for _ in range(100)])
        block.arrange_in_grid(10, 10, buff=0.04).move_to([3.3, 0.9, 0])
        cap_r = T("the list", size=24, color=MUTED).next_to(block, UP, buff=0.25)
        bits = M(r"\approx 5\,000\ \text{bits}", size=40, color=HILITE).next_to(block, DOWN, buff=0.4)
        # the amplitudes: a column that runs out of the frame
        col = Rectangle(width=2.2, height=9, stroke_width=0, fill_color=MUTED, fill_opacity=0.3)
        col.move_to([-3.3, 2.1 - 4.5, 0])
        stripes = VGroup(*[Line([-4.4, 2.1 - 0.16 * k, 0], [-2.2, 2.1 - 0.16 * k, 0], color=BG, stroke_width=2)
                           for k in range(1, 40)])
        cap_l = T("the amplitudes", size=24, color=MUTED).move_to([-3.3, 2.45, 0])
        big = M(r"2^{50} \approx 10^{15}", size=44, color=HILITE).move_to([-0.2, 0.2, 0])
        big.shift(LEFT * 0.2)
        with self.voice("f1"):
            self.play(FadeIn(n), run_time=0.5)
            self.hold(1.0)
            self.play(FadeIn(cap_r), LaggedStart(*[FadeIn(s) for s in block], lag_ratio=0.01, run_time=1.2))
            self.hold(1.6)
            self.play(FadeIn(bits, shift=UP * 0.2), run_time=0.5)
            self.hold(1.4)
            self.play(FadeIn(cap_l), GrowFromEdge(col, UP), FadeIn(stripes), run_time=1.2)
            self.hold(1.4)
            self.play(FadeIn(big, shift=UP * 0.2), run_time=0.5)
        ask = M("?", size=110, color=HILITE).move_to([0.2, -1.7, 0])
        with self.voice("f2"):
            self.play(FadeIn(ask, scale=0.6), run_time=0.5)
        # f3: not every state. The ones that can are an island in the space of all states
        sea = RoundedRectangle(width=10.5, height=4.6, corner_radius=0.4, color=MUTED, stroke_width=2)
        sea.move_to([0, 0.3, 0])
        sea_l = T("all states", size=24, color=MUTED).move_to(sea.get_corner(UL) + [1.1, -0.4, 0])
        isle = Ellipse(width=5.2, height=2.5, color=HILITE, stroke_width=3, fill_color=HILITE, fill_opacity=0.14)
        isle.move_to([1.1, -0.1, 0])
        isle_l = T("stabilizer states", size=24, color=HILITE, bold=True).move_to(isle.get_center() + UP * 0.72)
        codes = VGroup(*[T(s, size=22) for s in ("bit flip", "Shor", "Steane", "surface")])
        codes.arrange_in_grid(2, 2, buff=(0.7, 0.25)).move_to(isle.get_center() + DOWN * 0.25)
        with self.voice("f3"):
            self.play(*[FadeOut(m) for m in self.stage()], run_time=0.6)
            self.play(Create(sea), FadeIn(sea_l), run_time=0.8)
            self.hold(2.6)
            self.play(FadeIn(isle, scale=0.8), FadeIn(isle_l), run_time=0.7)
            self.hold(3.0)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in codes], lag_ratio=0.4, run_time=1.6))
    # ------------------------------------------------------------ G. close, towards 8.2
    def closing(self):
        self.clear_stage()
        lst = self.list_box(["ZZI", "IZZ"], x=-5.0, y=0.9, title="checks")
        cells = self.grid()
        for k in ((1, 0), (0, 1), (1, 1)):
            cells[k][0].set_stroke(opacity=0.22)
            cells[k][1].set_opacity(0.22)
        home = cells[(0, 0)]
        glow = Rectangle(width=self.CW, height=self.CH, stroke_color=HILITE, stroke_width=5, fill_color=HILITE,
                         fill_opacity=0.18).move_to(home[0])
        with self.voice("g1"):
            self.play(FadeIn(lst), FadeIn(lst.title), FadeIn(VGroup(*cells.values())), FadeIn(glow), run_time=0.8)
        with self.voice("g2"):
            for k in ((1, 0), (1, 1), (0, 1)):
                self.play(cells[k][0].animate(rate_func=there_and_back).set_stroke(HILITE, opacity=1), run_time=0.55)
        # g3: each dark cell is where one bit flip sends the code
        flips = [((1, 0), "X_1", (False, True)), ((1, 1), "X_2", (False, False)), ((0, 1), "X_3", (True, False))]
        pairs = []
        with self.voice("g3"):
            self.hold(3.4)
            hc = home[0].get_center()
            routes = {      # (start, end, bend, where the label sits relative to the arrow's middle)
                (1, 0): (hc + [0.5, self.CH / 2 + 0.12, 0], hc + [self.CW - 0.5, self.CH / 2 + 0.12, 0], -0.9, UP * 0.55),
                (0, 1): (hc + [-self.CW / 2 - 0.12, 0.2, 0], hc + [-self.CW / 2 - 0.12, -self.CH - 0.2, 0], 0.9, LEFT * 0.62),
                (1, 1): (self.GC + [-0.42, 0.3, 0], self.GC + [0.42, -0.3, 0], 0.0, [0.42, 0.3, 0]),
            }
            for k, name, (a, b) in flips:
                tgt = cells[k]
                start, end, bend, off = routes[k]
                arr = CurvedArrow(start, end, angle=bend, color=X_TILE, stroke_width=5, tip_length=0.22)
                lab = M(name, size=30, color=INK).move_to((start + end) / 2 + np.array(off))
                pair = VGroup(answer(a, 26), answer(b, 26)).arrange(RIGHT, buff=0.3)
                pair.move_to(tgt[0].get_bottom() + UP * 0.24)
                self.play(Create(arr), FadeIn(lab), tgt[0].animate.set_stroke(opacity=1),
                          tgt[1].animate.set_opacity(1).shift(UP * 0.14), run_time=0.8)
                self.play(FadeIn(pair), run_time=0.4)
                pairs.append(pair)
                self.hold(0.9)
        nxt = VGroup(T("Next", size=26, color=MUTED), T("8.2  Stabilizer codes", size=50, bold=True))
        nxt.arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        with self.voice("g4"):
            minus_ones = [p[i] for p, (_, _, ans) in zip(pairs, flips) for i in (0, 1) if not ans[i]]
            self.hold(3.0)
            self.play(*[Indicate(m, color=ACCENT, scale_factor=1.6) for m in minus_ones], run_time=1.0)
            self.hold(1.2)
            self.play(*[FadeOut(m) for m in self.stage()], run_time=0.6)
            self.play(FadeIn(nxt, shift=UP * 0.2), run_time=0.7)
