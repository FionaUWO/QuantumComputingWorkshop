"""Section 1.1 — From bits to amplitudes.   Draft of scene A only.

Build from the video folder with the Manim environment:
    python pipeline/build.py 1.1 preview --scene a

Narration ids (a1, a2, ...) match script.py and storyboard.md.
The H gate is drawn as what it is on the sphere: a half turn about the axis midway
between x and z, which carries |0> to |+> and, applied again, back to |0>.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))

from common import *  # noqa: E402,F401

FULL_W = 14.222
ZOOM_W = 11.6                 # frame width while only one half is in view
LEFT_X, RIGHT_X = -3.5, 3.5
TOP_Y, GRID_Y, TALLY_Y = 2.95, -1.2, -2.1


class Main(NarratedScene):
    EP = "1.1"

    SCENES = [("i", "opening"), ("a", "puzzle"), ("b", "random_bit"), ("c", "operations"), ("d", "no_coin"),
              ("e", "two_changes"), ("f", "side_by_side"), ("r", "closing")]

    def construct(self):
        # ONLY=cd renders just scenes c and d (for quick drafts); unset renders everything.
        only = os.environ.get("ONLY", "")
        for letter, name in self.SCENES:
            if only and letter not in only:
                continue
            if letter not in "ia" and not hasattr(self, "badge"):
                self.furniture()
            getattr(self, name)()
        self.save_marks()

    def make_badge(self):
        t = T("H  H  →  ?", size=22, bold=True)
        box = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.34, corner_radius=0.16,
                               color=HILITE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
        return VGroup(box, t.move_to(box)).to_corner(UR, buff=0.3)

    def furniture(self):
        """The header and the puzzle badge, for drafts that skip scene A."""
        self.badge = self.make_badge()
        self.head = header("1.1  From bits to amplitudes")
        self.add(self.badge, self.head)

    # ------------------------------------------------------------ small helpers
    def tally(self, outcomes, x):
        """The counts under a dot grid: a lilac disc with its count, a white ring with its count."""
        n1 = int(sum(outcomes))
        d0 = dot_look(Circle(radius=0.1), 0)
        d1 = dot_look(Circle(radius=0.1), 1)
        row = VGroup(d0, T(str(100 - n1), size=24, bold=True), d1, T(str(n1), size=24, bold=True))
        row.arrange(RIGHT, buff=0.18)
        row[2].shift(RIGHT * 0.35)
        row[3].shift(RIGHT * 0.35)
        return row.move_to([x, TALLY_Y, 0])

    def flip(self, coin, face, spins=2):
        """Toss the coin: it rises, turns edge-on `spins` times, and lands showing `face`."""
        thin = 0.06
        for k in range(spins):
            last = k == spins - 1
            self.play(coin.animate.shift(UP * 0.3).stretch(thin, 0), run_time=0.14, rate_func=rush_into)
            if last:
                new = T(face, size=60, bold=True).move_to(coin[0]).stretch(thin, 0)
                coin[1].become(new)
            self.play(coin.animate.shift(DOWN * 0.3).stretch(1 / thin, 0), run_time=0.14, rate_func=rush_from)

    def measure(self, grid, outcomes, x, old_tally=None, run_time=1.1):
        """Empty the grid, then fill it with 100 outcomes and show the counts."""
        clear_dots(grid)
        new = self.tally(outcomes, x)
        anims = [fill_dots(grid, outcomes, run_time=run_time)]
        if old_tally is not None:
            self.remove(old_tally)
        self.play(*anims)
        self.play(FadeIn(new), run_time=0.25)
        return new

    def swing(self, bloch, arrow_box, angle=PI, run_time=1.0):
        """Turn the state about the H axis, drawing the path of the arrow tip."""
        t = ValueTracker(0.0)
        start = bloch.state.copy()
        moving = always_redraw(lambda: bloch.arrow(rotate_about(start, H_AXIS, angle * t.get_value())))
        trail = always_redraw(lambda: bloch.path(H_AXIS, angle, 0.0, max(t.get_value(), 1e-3)))
        self.remove(arrow_box[0])
        self.add(trail, moving)
        self.play(t.animate.set_value(1.0), run_time=run_time, rate_func=smooth)
        self.remove(moving, trail)
        fixed_trail = bloch.path(H_AXIS, angle)
        bloch.state = rotate_about(start, H_AXIS, angle)
        arrow_box[0] = bloch.arrow()
        self.add(fixed_trail, arrow_box[0])
        return fixed_trail

    # ------------------------------------------------------------ I. opening
    def opening(self):
        """Who is speaking, then what today is about. No header and no badge yet."""
        logo_file = Path(__file__).resolve().parents[3] / "public" / "assets" / "img" / "logo-800.png"
        # the logo is drawn for a light page, so it sits on a white disc
        disc = Circle(radius=1.5, stroke_width=0, fill_color=RING, fill_opacity=1)
        logo = ImageMobject(str(logo_file)).set(height=2.25).move_to(disc)
        mark = Group(disc, logo).move_to([0, 1.35, 0])
        lab = T("QAICON Lab", size=54, bold=True).move_to([0, -0.85, 0])
        full = T("Quantum and AI for Computing, Optimization, and Networking", size=26, color=HILITE)
        full.next_to(lab, DOWN, buff=0.3)
        where = T("Western University", size=24, color=MUTED).next_to(full, DOWN, buff=0.25)
        with self.voice("i1"):
            self.play(FadeIn(mark, scale=0.85), run_time=0.8)
            self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.6)
            self.hold(1.2)
            self.play(FadeIn(full, shift=UP * 0.15), run_time=0.7)
            self.hold(2.6)
            self.play(FadeIn(where), run_time=0.5)

        series = T("Quantum Computing Workshop", size=28, color=MUTED).move_to([0, 1.2, 0])
        title = T("From bits to amplitudes", size=58, bold=True).move_to([0, 0.2, 0])
        number = T("Lecture 1  ·  Section 1.1", size=26, color=HILITE).next_to(title, DOWN, buff=0.4)
        corner = Group(disc.copy(), logo.copy()).set(height=0.9).to_corner(DL, buff=0.4).shift(UP * 0.5)
        with self.voice("i2"):
            self.play(FadeOut(VGroup(lab, full, where)), ReplacementTransform(mark, corner), run_time=0.8)
            self.play(FadeIn(series), FadeIn(title, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(number), run_time=0.5)
        self.play(FadeOut(VGroup(series, title, number)), FadeOut(corner), run_time=0.6)

    # ------------------------------------------------------------ A. the puzzle
    def puzzle(self):
        rng = np.random.default_rng(11)
        frame = self.camera.frame
        frame.set(width=ZOOM_W).move_to([LEFT_X + 0.3, -0.03, 0])

        # ---- left half: a coin and 100 flips
        coin_l = T("a fair coin", size=26, color=MUTED).move_to([LEFT_X, TOP_Y, 0])
        disc = Circle(radius=0.9, color=INK, stroke_width=3, fill_color=PANEL, fill_opacity=1)
        coin = VGroup(disc, T("?", size=60, bold=True)).move_to([LEFT_X, 1.25, 0])
        grid_l = dot_grid().move_to([LEFT_X, GRID_Y, 0])
        runs = [rng.integers(0, 2, 100) for _ in range(3)]
        faces = ["1", "0", "1"]      # what the coin shows after each toss

        # one dot per flip: the first flip fills the first dot, the second the next, and only
        # "a hundred times" fills the grid, so the picture never runs ahead of the words
        hundred = runs[2].copy()
        hundred[0], hundred[1] = int(faces[0]), int(faces[1])

        def one_dot(k):
            dot_look(grid_l[k], int(hundred[k]))
            self.play(Indicate(grid_l[k], color=RING if hundred[k] else LILAC, scale_factor=2.0), run_time=0.4)

        with self.voice("a1"):
            self.play(FadeIn(coin_l), FadeIn(coin, scale=0.9), FadeIn(grid_l), run_time=0.5)
            self.flip(coin, faces[0])
            one_dot(0)
        with self.voice("a2"):
            self.flip(coin, faces[1])
            one_dot(1)
            self.hold(0.7)
            self.flip(coin, faces[2], spins=3)
            self.play(fill_dots(grid_l, hundred, run_time=1.3))
            tally_l = self.tally(hundred, LEFT_X)
            self.play(FadeIn(tally_l), run_time=0.25)
        left = VGroup(coin_l, coin, grid_l, tally_l)

        # ---- right half: a qubit on the Bloch sphere
        qubit_l = T("a qubit", size=26, color=MUTED).move_to([RIGHT_X, TOP_Y, 0])
        bloch = Bloch(R=1.1, center=[RIGHT_X, 1.0, 0])
        arrow_box = [bloch.arrow()]
        grid_r = dot_grid().move_to([RIGHT_X, GRID_Y, 0])
        with self.voice("a3"):
            # the coin leaves the picture while the camera moves across to the qubit
            self.play(frame.animate.move_to([RIGHT_X - 0.3, -0.03, 0]), FadeOut(left), run_time=1.0)
            self.play(FadeIn(qubit_l), FadeIn(bloch), FadeIn(arrow_box[0]), FadeIn(grid_r), run_time=0.7)

        # the circuit so far, drawn where the label was:  |0> --[H]--[H]--
        ket = M(r"|0\rangle", size=30).move_to([RIGHT_X - 1.25, TOP_Y, 0])
        wire = Line([RIGHT_X - 0.9, TOP_Y, 0], [RIGHT_X + 1.5, TOP_Y, 0], color=INK, stroke_width=2)

        def gate(x):
            box = Square(side_length=0.5, color=INK, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            return VGroup(box, T("H", size=24, bold=True)).move_to([x, TOP_Y, 0])

        h1, h2 = gate(RIGHT_X - 0.2), gate(RIGHT_X + 0.75)
        once = (rng.random(100) < 0.5).astype(int)
        with self.voice("a4"):
            self.play(FadeOut(qubit_l), FadeIn(ket), Create(wire), run_time=0.5)
            self.play(FadeIn(h1, scale=1.3), run_time=0.35)
            trail1 = self.swing(bloch, arrow_box)
            tally_r = self.measure(grid_r, once, RIGHT_X, run_time=1.1)
        with self.voice("a5"):
            self.play(FadeIn(h2, scale=1.3), run_time=0.35)
            self.remove(trail1)
            trail2 = self.swing(bloch, arrow_box)
            tally_r = self.measure(grid_r, np.zeros(100, dtype=int), RIGHT_X, tally_r, run_time=1.0)
            self.play(Indicate(grid_r, color=LILAC, scale_factor=1.06), run_time=0.6)
        right = VGroup(ket, wire, h1, h2, bloch, arrow_box[0], trail2, grid_r, tally_r)

        # ---- both halves, and the question
        # Under each grid: the counts at its left edge, the verdict at its right edge.
        # Both halves use the same layout, so nothing crowds into the middle of the frame.
        still = pill("still random", color=MUTED, size=22)
        certain = pill("certain again", color=HILITE, size=22)
        for label, grid in ((still, grid_l), (certain, grid_r)):
            label.move_to([0, TALLY_Y - 0.14, 0]).align_to(grid, RIGHT)
        qmark = T("?", size=110, color=HILITE, bold=True).move_to([0, 0.9, 0])
        with self.voice("a6"):
            self.play(frame.animate.set(width=FULL_W).move_to(ORIGIN), FadeIn(left), run_time=1.0)
            self.play(tally_l.animate.align_to(grid_l, LEFT).shift(DOWN * 0.14),
                      tally_r.animate.align_to(grid_r, LEFT).shift(DOWN * 0.14),
                      run_time=0.4)
            self.play(FadeIn(still), FadeIn(certain), run_time=0.4)
            self.play(FadeIn(qmark, scale=2.2), run_time=0.6)
            self.play(Wiggle(qmark, scale_value=1.15), run_time=0.9)

        # ---- the question becomes the badge that stays in the corner
        self.badge = self.make_badge()
        step1 = T("1.  Ordinary probability cannot do it", size=32)
        step2 = T("2.  What quantum theory changes", size=32)
        plan = VGroup(step1, step2).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([0, 0.3, 0])
        with self.voice("a7"):
            self.play(FadeOut(VGroup(left, right, still, certain)), ReplacementTransform(qmark, self.badge),
                      run_time=0.9)
            self.set_header("1.1  From bits to amplitudes")
            self.play(FadeIn(step1, shift=RIGHT * 0.3), run_time=0.6)
            self.hold(1.6)
            self.play(FadeIn(step2, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeOut(plan), run_time=0.5)

    # ------------------------------------------------------------ B. a random bit
    def random_bit(self):
        box = VGroup(Square(side_length=1.3, color=INK, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                     T("?", size=56, bold=True)).move_to([-4.7, 1.0, 0])
        box_l = T("a bit we are unsure about", size=22, color=MUTED).next_to(box, UP, buff=0.3)
        with self.voice("b1"):
            self.play(FadeIn(box), FadeIn(box_l), run_time=0.5)
            for ch in "010?":
                box[1].become(T(ch, size=56, bold=True).move_to(box[0]))
                self.wait(0.3)

        chart = bars(0.6, 0.4, x=-0.9, base=-0.4, full=2.8, w=0.75, values=(r"p_0", r"p_1"))
        rest = VGroup(*[m for m in chart if m not in (chart.b0, chart.b1, chart.v0, chart.v1)])
        with self.voice("b2"):
            self.play(FadeIn(rest), run_time=0.4)
            self.hold(1.0)
            self.play(GrowFromEdge(chart.b0, DOWN), FadeIn(chart.v0), run_time=0.8)
            self.hold(0.9)
            self.play(GrowFromEdge(chart.b1, DOWN), FadeIn(chart.v1), run_time=0.8)

        vec = colvec("p_0", "p_1", size=52).move_to([3.7, 1.5, 0])
        name = M("p =", size=52).next_to(vec, LEFT, buff=0.25)
        with self.voice("b3"):
            self.play(FadeIn(vec.get_brackets()), FadeIn(name),
                      TransformFromCopy(chart.v0, vec.top), TransformFromCopy(chart.v1, vec.bottom), run_time=1.0)
            self.card("Probability vector", "A column of two probabilities: one that the bit is 0, one that it is 1.")
        conds = VGroup(M(r"p_0,\ p_1 \ge 0", size=36), M(r"p_0 + p_1 = 1", size=36))
        conds.arrange(DOWN, buff=0.25).next_to(VGroup(name, vec), DOWN, buff=0.45)
        with self.voice("b4"):
            self.play(Write(conds[0]), run_time=0.8)
            self.hold(0.5)
            self.play(Write(conds[1]), run_time=0.8)

        new_chart = bars(0.7, 0.3, x=-0.9, base=-0.4, full=2.8, w=0.75, values=("0.7", "0.3"))
        new_vec = colvec("0.7", "0.3", size=52).move_to(vec)
        with self.voice("b5"):
            self.uncard()
            self.hold(1.2)
            self.play(Transform(chart.b0, new_chart.b0), Transform(chart.b1, new_chart.b1),
                      Transform(chart.v0, new_chart.v0), Transform(chart.v1, new_chart.v1), run_time=1.0)
            self.play(Transform(vec, new_vec), run_time=0.8)
        # ---- the same bars and the same column go on to become e0, e1 and their mixture
        def state(p0, top, bottom, lhs, size=52):
            c = bars(p0, 1 - p0, x=-0.9, base=-0.4, full=2.8, w=0.75, values=(top, bottom))
            v = colvec(top, bottom, size=52).move_to(vec)
            return c, v, M(lhs, size=size).next_to(v, LEFT, buff=0.25)

        def caption(text, color):
            return T(text, size=26, color=color).next_to(vec, DOWN, buff=0.45)

        def morph(target, cap_new, run_time=0.9):
            c, v, n = target
            self.play(Transform(chart.b0, c.b0), Transform(chart.b1, c.b1), Transform(chart.v0, c.v0),
                      Transform(chart.v1, c.v1), Transform(vec, v), Transform(name, n), Transform(cap, cap_new),
                      run_time=run_time)

        cap = caption("certainly 0", LILAC).set_opacity(0)
        self.add(cap)
        with self.voice("b6"):
            self.play(FadeOut(VGroup(box, box_l, conds)), run_time=0.4)
            self.hold(0.9)
            morph(state(1, "1", "0", "e_0 ="), caption("certainly 0", LILAC))
            self.hold(0.9)
            morph(state(0, "0", "1", "e_1 ="), caption("certainly 1", RING))
        with self.voice("b7"):
            self.hold(2.4)
            morph(state(0.5, r"\tfrac12", r"\tfrac12", r"\tfrac12\,e_0 + \tfrac12\,e_1 =", size=44),
                  caption("a fair coin: half of each", MUTED), run_time=1.1)
        self.play(FadeOut(VGroup(chart, vec, name, cap)), run_time=0.5)

    # ------------------------------------------------------------ C. operations: read a matrix by columns
    def labels_for(self, g, right_x):
        """"input 0 / input 1" above the columns, "output 0 / output 1" to the right of the rows."""
        top = g.frame.get_top()[1] + 0.32
        cols = VGroup(*[T(f"input {k}", size=20, color=HILITE).move_to([g.pos(0, k)[0], top, 0]) for k in (0, 1)])
        rows = VGroup(*[T(f"output {k}", size=20, color=MUTED).move_to([right_x, g.pos(k, 0)[1], 0])
                        for k in (0, 1)])
        return cols, rows

    def operations(self):
        g = Grid2([-0.3, 0.9, 0], dx=1.5, dy=1.0, size=44)
        ph = [M(r"\cdot", size=44, color=MUTED).move_to(g.pos(r, c)) for r in (0, 1) for c in (0, 1)]
        name = M("M =", size=46).next_to(g.frame, LEFT, buff=0.3)
        cols, rows = self.labels_for(g, g.frame.get_right()[0] + 0.95)
        band = g.band(0)
        # an operation is seen doing something before it is written down as a matrix
        demo = bars(0.7, 0.3, x=0.0, base=-0.9, full=2.8, w=0.75, values=("0.7", "0.3"))
        swapped = bars(0.3, 0.7, x=0.0, base=-0.9, full=2.8, w=0.75, values=("0.3", "0.7"))
        not_tag = pill("NOT", color=HILITE, size=26).move_to([0, 2.5, 0])
        with self.voice("c1"):
            self.play(FadeIn(demo), run_time=0.5)
            self.hold(1.4)
            self.play(FadeIn(not_tag, shift=DOWN * 0.2), run_time=0.4)
            self.play(Transform(demo.b0, swapped.b0), Transform(demo.b1, swapped.b1),
                      Transform(demo.v0, swapped.v0), Transform(demo.v1, swapped.v1), run_time=1.0)
        with self.voice("c2"):
            self.play(FadeOut(not_tag), demo.animate.scale(0.55).move_to([-5.3, 0.6, 0]), run_time=0.7)
            self.play(FadeIn(g.frame), FadeIn(name), *[FadeIn(p) for p in ph], run_time=0.7)
            self.hold(1.2)
            self.play(FadeIn(band), run_time=0.4)
            self.hold(0.6)
            self.play(band.animate.move_to(g.band(1)), run_time=0.8)
        with self.voice("c3"):
            self.play(band.animate.move_to(g.band(0)), FadeIn(cols[0]), FadeIn(rows), run_time=0.7)
            self.hold(3.2)
            self.play(band.animate.move_to(g.band(1)), FadeIn(cols[1]), run_time=0.7)

        # ---- NOT, one column at a time
        not_name = M(r"\mathrm{NOT} =", size=46).next_to(g.frame, LEFT, buff=0.3)
        side = [5.3, 0.9, 0]
        why0, why1 = M(r"0 \;\to\; 1", size=46).move_to(side), M(r"1 \;\to\; 0", size=46).move_to(side)
        with self.voice("c4"):
            self.play(Transform(name, not_name), band.animate.move_to(g.band(0)), run_time=0.6)
            self.hold(0.7)
            self.play(FadeIn(why0, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeOut(ph[0]), FadeOut(ph[2]), Write(g.column(0, "0", "1")), run_time=0.9)
        with self.voice("c5"):
            self.play(band.animate.move_to(g.band(1)), FadeOut(why0), FadeIn(why1, shift=LEFT * 0.2), run_time=0.6)
            self.play(FadeOut(ph[1]), FadeOut(ph[3]), Write(g.column(1, "1", "0")), run_time=0.9)
        not_all = VGroup(name, g.everything())
        self.play(FadeOut(VGroup(band, why1, cols, rows, demo)), not_all.animate.scale(0.6).move_to([-5.15, 0.9, 0]),
                  run_time=0.7)

        # ---- the noisy channel
        n = Grid2([0.6, 0.9, 0], dx=2.2, dy=1.0, size=40, widest=r"1-\varepsilon")
        nph = [M(r"\cdot", size=44, color=MUTED).move_to(n.pos(r, c)) for r in (0, 1) for c in (0, 1)]
        n_name = M(r"N_\varepsilon =", size=46).next_to(n.frame, LEFT, buff=0.3)
        ncols, nrows = self.labels_for(n, n.frame.get_right()[0] + 0.95)
        note = VGroup(M(r"\varepsilon", size=40), T("= the probability of a flip", size=24, color=MUTED))
        note.arrange(RIGHT, buff=0.2).move_to([0.6, -0.85, 0])
        noisy = VGroup(*[dot_look(Circle(radius=0.14), 0) for _ in range(12)]).arrange(RIGHT, buff=0.14)
        noisy.move_to([0.6, -1.65, 0])
        with self.voice("c6"):
            self.play(FadeIn(n.frame), FadeIn(n_name), *[FadeIn(p) for p in nph], run_time=0.6)
            self.hold(1.2)
            self.play(FadeIn(note), run_time=0.5)
            # a dozen bits go through as 0; now and then one comes out flipped
            self.play(FadeIn(noisy), run_time=0.4)
            dot_look(noisy[8], 1)
            self.play(Indicate(noisy[8], color=RING, scale_factor=1.8), run_time=0.4)
        nband = n.band(0)
        b0 = VGroup(M(r"0 \to 0:\quad 1-\varepsilon", size=34), M(r"0 \to 1:\quad \varepsilon", size=34))
        b0.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([5.65, 0.9, 0])
        b1 = VGroup(M(r"1 \to 0:\quad \varepsilon", size=34), M(r"1 \to 1:\quad 1-\varepsilon", size=34))
        b1.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([5.65, 0.9, 0])
        with self.voice("c7"):
            self.play(FadeIn(nband), FadeIn(ncols), run_time=0.5)
            self.play(FadeIn(b0[0]), run_time=0.5)
            self.play(FadeOut(nph[0]), Write(n.entry(0, 0, r"1-\varepsilon")), run_time=0.8)
            self.hold(1.0)
            self.play(FadeIn(b0[1]), run_time=0.5)
            self.play(FadeOut(nph[2]), Write(n.entry(1, 0, r"\varepsilon")), run_time=0.8)
        with self.voice("c8"):
            self.play(nband.animate.move_to(n.band(1)), FadeOut(b0), FadeIn(b1), run_time=0.5)
            self.play(FadeOut(nph[1]), FadeOut(nph[3]),
                      Write(n.column(1, r"\varepsilon", r"1-\varepsilon")), run_time=0.9)

        def col_box(cells, a, b):
            return SurroundingRectangle(VGroup(cells[a], cells[b]), buff=0.1, corner_radius=0.1,
                                        color=HILITE, stroke_width=2.5)

        boxes = VGroup(col_box(g.cells, (0, 0), (1, 0)), col_box(g.cells, (0, 1), (1, 1)),
                       col_box(n.cells, (0, 0), (1, 0)), col_box(n.cells, (0, 1), (1, 1)))
        with self.voice("c9"):
            self.play(FadeOut(VGroup(nband, b1, ncols, note, noisy)), run_time=0.4)
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3), run_time=1.6)
            self.card("Stochastic matrix",
                      "A matrix in which every column is a probability vector.")
        n_all = VGroup(n_name, n.everything())
        self.uncard()
        self.play(FadeOut(VGroup(not_all, n_all, boxes)), run_time=0.5)

        # ---- throw the bit away and flip a coin
        f = Grid2([-3.7, 0.9, 0], dx=1.4, dy=1.05, size=40, widest=r"\tfrac12")
        f_name = M("F =", size=46).next_to(f.frame, LEFT, buff=0.3)
        gone = VGroup(Square(side_length=1.2, color=INK, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                      T("0", size=52, bold=True)).move_to([3.3, 1.0, 0])
        fresh = VGroup(Circle(radius=0.9, color=INK, stroke_width=3, fill_color=PANEL, fill_opacity=1),
                       T("?", size=60, bold=True)).move_to([3.3, 1.0, 0])
        with self.voice("c10"):
            self.play(FadeIn(f.frame), FadeIn(f_name), FadeIn(gone), run_time=0.6)
            self.hold(0.9)
            self.play(FadeOut(gone, shift=DOWN * 1.4), run_time=0.6)       # the bit is thrown away
            self.play(FadeIn(fresh, scale=0.9), run_time=0.3)
            self.flip(fresh, "1")                                          # and a coin is flipped instead
            self.play(Write(f.column(0, r"\tfrac12", r"\tfrac12")), Write(f.column(1, r"\tfrac12", r"\tfrac12")),
                      run_time=1.0)
        xs = [0.9, 3.3, 5.7]
        charts = [bars(p, 1 - p, x=x, base=-0.3, full=2.2, w=0.45) for p, x in zip((0.7, 0.5, 0.5), xs)]
        caps = [M(t, size=28).move_to([x, -1.05, 0]) for t, x in
                zip((r"(0.7,\ 0.3)", r"(0.5,\ 0.5)", r"(0.5,\ 0.5)"), xs)]
        arrows = []
        for a, b in zip(xs, xs[1:]):
            arr = Arrow([a + 0.75, 0.6, 0], [b - 0.75, 0.6, 0], buff=0, color=HILITE, stroke_width=4,
                        max_tip_length_to_length_ratio=0.25)
            arrows.append(VGroup(arr, M("F", size=32).next_to(arr, UP, buff=0.1)))
        with self.voice("c11"):
            self.play(FadeOut(fresh), FadeIn(charts[0]), FadeIn(caps[0]), run_time=0.5)
            self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), run_time=0.4)
            self.play(TransformFromCopy(charts[0], charts[1]), FadeIn(caps[1]), run_time=0.7)
            self.hold(0.6)
            self.play(GrowArrow(arrows[1][0]), FadeIn(arrows[1][1]), run_time=0.4)
            self.play(TransformFromCopy(charts[1], charts[2]), FadeIn(caps[2]), run_time=0.7)
        self.play(FadeOut(VGroup(f.everything(), f_name, *charts, *caps, *arrows)), run_time=0.5)

    # ------------------------------------------------------------ D. why no coin can do what H does
    def no_coin(self):
        ask = M(r"M \;\stackrel{?}{=}\; H", size=72).move_to([0, 0.8, 0])
        with self.voice("d1"):
            self.play(Indicate(self.badge, color=HILITE, scale_factor=1.25), run_time=0.9)
            self.play(FadeIn(ask, shift=UP * 0.2), run_time=0.6)
        self.play(FadeOut(ask), run_time=0.4)

        def bit(k, pos):
            c = dot_look(Circle(radius=0.34), k).move_to(pos)
            return VGroup(c, T(str(k), size=26, color=BG if k == 0 else INK, bold=True).move_to(c))

        def m_box(pos):
            sq = Square(side_length=0.62, color=INK, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            return VGroup(sq, M("M", size=30)).move_to(pos)

        def edge(a, b, label=None, up=True):
            ln = Line(a.get_right(), b.get_left(), color=MUTED, stroke_width=2.5, buff=0.08)
            if label is None:
                return VGroup(ln)
            lab = M(label, size=28).move_to(ln.get_center() + (UP if up else DOWN) * 0.3)
            return VGroup(ln, lab)

        root_t = T("certainly 0", size=22)
        root = VGroup(RoundedRectangle(width=root_t.width + 0.4, height=0.62, corner_radius=0.14, color=HILITE,
                                       stroke_width=2, fill_color=PANEL, fill_opacity=1), root_t)
        root.move_to([-5.75, 0.6, 0])
        root_t.move_to(root[0])
        m1 = m_box([-3.85, 0.6, 0])
        mid0, mid1 = bit(0, [-2.2, 1.7, 0]), bit(1, [-2.2, -0.5, 0])
        e_root = edge(root, m1)
        e_m0, e_m1 = edge(m1, mid0, r"\tfrac12"), edge(m1, mid1, r"\tfrac12", up=False)
        with self.voice("d2"):
            self.play(FadeIn(root), run_time=0.5)
            self.hold(0.8)
            self.play(Create(e_root), FadeIn(m1), run_time=0.6)
            self.play(Create(e_m0[0]), Create(e_m1[0]), FadeIn(e_m0[1]), FadeIn(e_m1[1]), run_time=0.7)
            self.play(FadeIn(mid0), FadeIn(mid1), run_time=0.4)

        m2a, m2b = m_box([-0.6, 1.7, 0]), m_box([-0.6, -0.5, 0])
        e_a, e_b = edge(mid0, m2a), edge(mid1, m2b)
        with self.voice("d3"):
            self.play(Create(e_a), Create(e_b), FadeIn(m2a), FadeIn(m2b), run_time=0.8)
            self.hold(0.9)
            self.play(Indicate(mid0, color=LILAC, scale_factor=1.3), run_time=0.8)
            self.play(Indicate(mid1, color=RING, scale_factor=1.3), run_time=0.8)

        tint_a = Rectangle(width=7.9, height=2.0, stroke_width=0, fill_color=PURPLE, fill_opacity=0.2
                           ).move_to([0.85, 1.75, 0])
        tint_b = Rectangle(width=7.9, height=1.5, stroke_width=0, fill_color=PURPLE, fill_opacity=0.2
                           ).move_to([0.85, -0.5, 0])
        for t in (tint_a, tint_b):
            t.set_z_index(-1)
        with self.voice("d4"):
            self.play(FadeIn(tint_a), FadeIn(tint_b), run_time=0.7)

        leaf0, leaf1 = bit(0, [1.2, 2.3, 0]), bit(1, [1.2, 1.1, 0])
        e_l0, e_l1 = edge(m2a, leaf0, r"\tfrac12"), edge(m2a, leaf1, r"\tfrac12", up=False)
        block = VGroup(Rectangle(width=1.0, height=0.9, color=RING, stroke_width=2.2, fill_color=BG, fill_opacity=1),
                       M(r"\tfrac14", size=36, color=INK)).move_to([3.95, 1.1, 0])
        calc = M(r"\tfrac12 \times \tfrac12 =", size=30).next_to(block, LEFT, buff=0.2)
        with self.voice("d5"):
            self.play(tint_b.animate.set_opacity(0.05), run_time=0.4)
            self.hold(1.2)
            self.play(Create(e_l0[0]), Create(e_l1[0]), FadeIn(e_l0[1]), FadeIn(e_l1[1]),
                      FadeIn(leaf0), FadeIn(leaf1), run_time=0.9)
            self.hold(1.6)
            self.play(FadeIn(calc), FadeIn(block, scale=0.6), run_time=0.7)
            self.play(Indicate(block, color=RING, scale_factor=1.15), run_time=0.7)

        cloud = VGroup(Ellipse(width=2.5, height=1.05, color=MUTED, stroke_width=2, fill_color=MUTED,
                               fill_opacity=0.28), M(r"\text{?}\ \ge 0", size=32)).move_to([1.9, -0.5, 0])
        e_c = edge(m2b, cloud)
        with self.voice("d6"):
            self.play(tint_a.animate.set_opacity(0.05), tint_b.animate.set_opacity(0.2), run_time=0.4)
            self.hold(1.9)
            self.play(Create(e_c), FadeIn(cloud), run_time=0.7)
            self.play(cloud[0].animate.stretch(1.35, 1), run_time=0.9, rate_func=there_and_back)
            self.play(cloud[0].animate.stretch(0.55, 1), run_time=0.9, rate_func=there_and_back)

        # the bar "probability of outcome 1": the quarter sits at the bottom and nothing removes it
        bx, base, full = 5.9, -1.9, 3.6
        outline = Rectangle(width=1.0, height=full, color=MUTED, stroke_width=1.5).move_to([bx, base + full / 2, 0])
        bar_t = T("probability of 1", size=20, color=MUTED).next_to(outline, UP, buff=0.15)
        ticks = VGroup(T("1", size=18, color=MUTED).next_to(outline.get_corner(UL), LEFT, buff=0.12),
                       T("0", size=18, color=MUTED).next_to(outline.get_corner(DL), LEFT, buff=0.12))
        stack = Rectangle(width=1.0, height=0.9, color=MUTED, stroke_width=1.5, fill_color=MUTED,
                          fill_opacity=0.3).move_to([bx, base + 0.9 + 0.45, 0])
        least = M(r"\ge \tfrac14", size=40).move_to([bx - 1.25, base + 0.45, 0])
        with self.voice("d7"):
            self.play(FadeIn(outline), FadeIn(bar_t), FadeIn(ticks), run_time=0.5)
            self.play(block.animate.move_to([bx, base + 0.45, 0]), FadeOut(calc), run_time=0.8)
            self.play(TransformFromCopy(cloud[0], stack), run_time=0.6)
            self.play(stack.animate.stretch(2.2, 1, about_edge=DOWN), run_time=0.7, rate_func=there_and_back)
            self.play(FadeIn(least), run_time=0.4)

        tree = VGroup(root, m1, mid0, mid1, e_root, e_m0, e_m1, m2a, m2b, e_a, e_b, tint_a, tint_b,
                      leaf0, leaf1, e_l0, e_l1, block, cloud, e_c, outline, bar_t, ticks, stack, least)
        small = T("Certainty does not come back.", size=28, color=MUTED).move_to([0, 1.9, 0])
        big1 = T("Probabilities add.", size=48, bold=True).move_to([0, 0.75, 0])
        big2 = T("They never cancel.", size=48, bold=True, color=HILITE).move_to([0, -0.2, 0])
        self.note = status("a coin", False).next_to(self.badge, DOWN, buff=0.15).align_to(self.badge, RIGHT)
        with self.voice("d8"):
            self.play(FadeOut(tree), FadeIn(small), run_time=0.6)
            self.hold(1.0)
            self.play(FadeIn(big1, shift=UP * 0.2), run_time=0.5)
            self.hold(0.6)
            self.play(FadeIn(big2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(self.note), run_time=0.4)
        self.play(FadeOut(VGroup(small, big1, big2)), run_time=0.5)

    # ------------------------------------------------------------ E. two changes
    def two_changes(self):
        if not hasattr(self, "note"):          # drafts that skip scene D
            self.note = status("a coin", False).next_to(self.badge, DOWN, buff=0.15).align_to(self.badge, RIGHT)
            self.add(self.note)
        sq = r"\square"
        g = Grid2([-1.9, 1.7, 0], dx=1.2, dy=0.9, size=40, widest=sq)
        for r in (0, 1):
            for c in (0, 1):
                g.entry(r, c, sq, color=MUTED)
        vec = colvec(sq, sq, size=40, color=MUTED).move_to([1.5, 1.7, 0])
        vec.get_brackets().set_color(INK)
        skeleton = VGroup(g.everything(), vec)
        with self.voice("e1"):
            # the screen is never empty while the voice speaks: the outline is there from the start
            self.play(FadeIn(skeleton), run_time=0.8)
            self.hold(3.6)
            self.play(Indicate(skeleton, color=INK, scale_factor=1.06), run_time=1.0)

        # ---- examples first, rules after: a coin, then a column no coin could have
        xs = [-4.6, -0.3, 4.0]            # the third column stays clear of the note under the badge
        vy, sy, by, bfull = 1.25, -0.42, -2.45, 1.3
        root2 = r"\tfrac{1}{\sqrt2}"
        titles = [T("a fair coin", size=24, color=MUTED).move_to([xs[0], 2.4, 0]),
                  T("amplitudes", size=24, color=HILITE, bold=True).move_to([xs[1], 2.4, 0]),
                  T("a qubit", size=24, color=MUTED).move_to([xs[2], 2.4, 0])]
        named = T("amplitudes", size=24, color=HILITE, bold=True).move_to(titles[2])
        v1 = colvec(r"\tfrac12", r"\tfrac12", size=36).move_to([xs[0], vy, 0])
        v2 = colvec(root2, root2, size=36).move_to([xs[1], vy, 0])
        v3 = colvec(root2, "-" + root2, size=36).move_to([xs[2], vy, 0])
        v3.bottom[0][0].set_color(ACCENT)     # the minus sign
        with self.voice("e2"):
            # the empty column of the skeleton becomes the coin's vector
            self.play(FadeOut(g.everything()), ReplacementTransform(vec, v1), FadeIn(titles[0]),
                      run_time=0.9)
        with self.voice("e3"):
            self.play(FadeIn(titles[2]), FadeIn(v3.get_brackets()), FadeIn(v3.top), run_time=0.6)
            self.hold(1.6)
            self.play(FadeIn(v3.bottom, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(v3.bottom[0][0], color=ACCENT, scale_factor=2.2), run_time=0.9)
        with self.voice("e4"):
            self.hold(1.3)
            self.play(Indicate(v1, color=INK, scale_factor=1.08), run_time=0.9)      # no minus sign over here
            self.hold(4.0)
            # the name comes after the thing it names
            self.play(Transform(titles[2], named), run_time=0.5)
        with self.voice("e4b"):
            self.card("Amplitude", "An entry of a qubit's vector. It may be negative, or complex.")

        # ---- squaring, drawn as area. A number a becomes a square of side |a|; the two areas
        # then re-form as two slabs that fill one unit square: the squares total one.
        U = 0.9                               # the length that stands for 1

        def tile(k, w, h, pos):
            """A piece of area for outcome k, in that outcome's look, labelled with its area."""
            r = Rectangle(width=w, height=h, stroke_width=2.2 if k else 0, color=RING if k else LILAC,
                          fill_color=BG if k else LILAC, fill_opacity=1)
            return VGroup(r, M(r"\tfrac12", size=26, color=INK if k else BG)).move_to(pos)

        def area(x):
            side = U / np.sqrt(2)
            sqs = [tile(k, side, side, [x + (k - 0.5) * 1.1, sy, 0]) for k in (0, 1)]
            slabs = [tile(k, U, U / 2, [x, sy + (k - 0.5) * U / 2, 0]) for k in (0, 1)]
            one = M("= 1", size=34).next_to(VGroup(*slabs), RIGHT, buff=0.22)
            return sqs, slabs, one

        sq3, slab3, one3 = area(xs[2])
        sq2, slab2, one2 = area(xs[1])
        with self.voice("e5"):
            self.uncard()
            self.hold(1.3)
            self.play(TransformFromCopy(v3.top, sq3[0]), run_time=0.8)
            self.play(TransformFromCopy(v3.bottom, sq3[1]), run_time=0.8)     # the minus sign does not survive
            self.hold(1.2)
            self.play(Transform(sq3[0], slab3[0]), Transform(sq3[1], slab3[1]), run_time=0.9)
            self.play(FadeIn(one3, shift=RIGHT * 0.1), run_time=0.4)
        with self.voice("e6"):
            self.hold(1.4)
            self.play(Indicate(VGroup(sq3[0], sq3[1], one3), color=HILITE, scale_factor=1.12), run_time=1.0)
        with self.voice("e7"):
            self.play(TransformFromCopy(v3, v2), FadeIn(titles[1]), run_time=0.9)
            self.hold(3.4)
            self.play(TransformFromCopy(v2.top, sq2[0]), TransformFromCopy(v2.bottom, sq2[1]), run_time=0.8)
            self.play(Transform(sq2[0], slab2[0]), Transform(sq2[1], slab2[1]), run_time=0.8)
            self.play(FadeIn(one2, shift=RIGHT * 0.1), run_time=0.4)

        # ---- the same areas become the probabilities: each slab turns into its bar
        rule = pill("probability of an outcome  =  square of its amplitude", color=HILITE, size=22)
        rule.move_to([1.85, -1.36, 0])
        charts = [bars(0.5, 0.5, x=x, base=by, full=bfull, w=0.5) for x in xs]

        def to_bars(sqs, chart):
            rest = VGroup(*[m for m in chart if m not in (chart.b0, chart.b1)])
            return [ReplacementTransform(sqs[0][0], chart.b0), ReplacementTransform(sqs[1][0], chart.b1),
                    FadeOut(sqs[0][1]), FadeOut(sqs[1][1]), FadeIn(rest)]

        with self.voice("e8"):
            self.hold(2.6)
            self.play(FadeIn(rule), FadeOut(one2), FadeOut(one3), run_time=0.5)
            self.play(*to_bars(sq2, charts[1]), *to_bars(sq3, charts[2]), run_time=1.3)
        level = DashedLine([-5.7, by + bfull / 2, 0], [5.1, by + bfull / 2, 0], color=MUTED, stroke_width=2,
                           dash_length=0.12)
        with self.voice("e9"):
            self.hold(3.3)
            self.play(FadeIn(charts[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Create(level), run_time=0.9)
        tag = pill("what one H gives", color=HILITE, size=20).next_to(titles[1], UP, buff=0.14)
        with self.voice("e10"):
            self.play(FadeIn(tag), Indicate(self.badge, color=HILITE, scale_factor=1.2), run_time=0.9)
            self.play(Indicate(v2, color=HILITE, scale_factor=1.08), run_time=0.9)
        ring2 = SurroundingRectangle(v2.bottom, buff=0.1, corner_radius=0.1, color=HILITE, stroke_width=2.5)
        ring3 = SurroundingRectangle(v3.bottom, buff=0.1, corner_radius=0.1, color=ACCENT, stroke_width=2.5)
        with self.voice("e11"):
            self.play(FadeOut(tag), run_time=0.3)
            self.hold(1.1)
            self.play(Create(ring2), Create(ring3), run_time=0.8)
        blind = pill("a measurement cannot tell them apart", color=MUTED, size=22).move_to(rule)
        after = [T("after a second H", size=21, color=HILITE).move_to(t) for t in titles[1:]]
        w2 = colvec("1", "0", size=40).move_to(v2)
        w3 = colvec("0", "1", size=40).move_to(v3)
        new2 = bars(1, 0, x=xs[1], base=by, full=bfull, w=0.5)
        new3 = bars(0, 1, x=xs[2], base=by, full=bfull, w=0.5)
        with self.voice("e12"):
            self.play(Transform(rule, blind), run_time=0.6)
            self.hold(2.4)
            # the label goes before the bars change: after a second H they can be told apart
            self.play(FadeOut(VGroup(ring2, ring3, level, rule)),
                      Transform(titles[1], after[0]), Transform(titles[2], after[1]), run_time=0.7)
            self.hold(0.6)
            self.play(Transform(v2, w2), Transform(charts[1].b0, new2.b0), Transform(charts[1].b1, new2.b1),
                      run_time=1.0)
            self.hold(1.0)
            self.play(Transform(v3, w3), Transform(charts[2].b0, new3.b0), Transform(charts[2].b1, new3.b1),
                      run_time=1.0)

        def chip(tex, colour, x):
            box = RoundedRectangle(width=1.25, height=0.95, corner_radius=0.12, stroke_width=0,
                                   fill_color=colour, fill_opacity=1)
            return VGroup(box, M(tex, size=40, color=BG)).move_to([x, 1.1, 0])

        plus, minus = chip(r"+\tfrac12", MUTED, xs[0] - 1.5), chip(r"-\tfrac12", ACCENT, xs[0] + 1.5)
        zero = M("0", size=80).move_to([xs[0], 1.1, 0])
        cancel_t = T("amplitudes can cancel", size=24, color=HILITE).move_to([xs[0], 2.3, 0])
        done = status("amplitudes", True).move_to(self.note).align_to(self.badge, RIGHT)
        with self.voice("e13"):
            self.play(FadeOut(VGroup(titles[0], v1, charts[0])), run_time=0.5)
            self.play(FadeIn(cancel_t), FadeIn(plus), FadeIn(minus), run_time=0.6)
            self.hold(0.8)
            self.play(plus.animate.move_to([xs[0], 1.1, 0]), minus.animate.move_to([xs[0], 1.1, 0]),
                      run_time=0.8, rate_func=rush_into)
            self.play(FadeOut(plus, scale=0.3), FadeOut(minus, scale=0.3), FadeIn(zero, scale=1.6), run_time=0.5)
        self.play(Transform(self.note, done), run_time=0.5)
        self.play(FadeOut(VGroup(cancel_t, zero, titles[1], titles[2], v2, v3, charts[1], charts[2])), run_time=0.5)

    # ------------------------------------------------------------ F. side by side, and what comes next
    def side_by_side(self):
        cx = (-1.2, 3.7)
        ys = (1.35, 0.5, -0.35)
        heads = [T("Random bit", size=28, bold=True).move_to([cx[0], 2.3, 0]),
                 T("Qubit", size=28, bold=True, color=HILITE).move_to([cx[1], 2.3, 0])]
        names = [T(s, size=24, color=MUTED).move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
                 for s, y in zip(("State", "Operations", "Reading it out"), ys)]
        rules = VGroup(*[Line([-6.3, y, 0], [6.0, y, 0], color=PURPLE, stroke_width=1.5)
                         for y in (1.85, 0.925, 0.075, -0.8)])
        left = [T(s, size=26).move_to([cx[0], y, 0]) for s, y in
                zip(("two probabilities", "stochastic matrices", "look at it"), ys)]
        right = [T("two amplitudes", size=26).move_to([cx[1], ys[0], 0]),
                 T("unitary matrices", size=26, slant=ITALIC).move_to([cx[1], ys[1], 0]),
                 T("measure it", size=26).move_to([cx[1], ys[2], 0])]
        with self.voice("f1"):
            self.play(FadeIn(VGroup(*heads, *names, rules)), run_time=0.8)
        for seg, cells in (("f2", left), ("f3", right)):
            with self.voice(seg):
                for k, cell in enumerate(cells):
                    self.hold(0.9 if k == 0 else 0.6)
                    self.play(FadeIn(cell, shift=RIGHT * 0.2), run_time=0.5)

        stops = ["1.2  States", "1.3  Measurement", "1.4  The Bloch sphere", "1.5  Gates", "1.6  Interference"]
        px = np.linspace(-5.3, 5.3, 5)
        track = Line([px[0], -1.6, 0], [px[-1], -1.6, 0], color=PURPLE, stroke_width=3)
        dots = [Circle(radius=0.13, color=HILITE, stroke_width=2.5, fill_color=BG, fill_opacity=1).move_to([x, -1.6, 0])
                for x in px]
        labs = [T(s, size=19, color=INK).move_to([x, -2.1, 0]) for s, x in zip(stops, px)]
        with self.voice("f4"):
            self.play(Create(track), *[FadeIn(d) for d in dots], run_time=0.7)
            self.hold(1.3)
            for k in range(4):
                self.play(dots[k].animate.set_fill(HILITE, opacity=1), FadeIn(labs[k]), run_time=0.45)
                self.hold(0.35)
        back = self.badge.copy()
        with self.voice("f5"):
            self.play(dots[4].animate.set_fill(HILITE, opacity=1).scale(1.5), FadeIn(labs[4]), run_time=0.6)
            self.hold(1.4)
            self.play(back.animate.scale(0.85).next_to(dots[4], UP, buff=0.25), run_time=0.9)
            self.play(Indicate(back, color=HILITE, scale_factor=1.15), run_time=0.8)
        self.play(FadeOut(VGroup(*heads, *names, rules, *left, *right, track, *dots, *labs, back)), run_time=0.5)

    # ------------------------------------------------------------ R, Q, Z. recap, questions, end card
    def closing(self):
        self.recap([["A random bit is a probability vector.",
                     "Operations are stochastic matrices, read column by column."],
                    ["Probabilities only add.",
                     "No coin can turn randomness back into certainty."],
                    ["A qubit holds amplitudes.",
                     "They can be negative, and their squares total one."]],
                   ["r0", "r1", "r2", "r3"])

        def row(*parts, buff=0.3):
            return VGroup(*parts).arrange(RIGHT, buff=buff)

        half = r"\begin{pmatrix}\tfrac12\\[0.2em]\tfrac12\end{pmatrix}"
        root = r"\begin{pmatrix}\tfrac{1}{\sqrt2}\\[0.2em]\tfrac{1}{\sqrt2}\end{pmatrix}"
        qas = [
            ("q1", "q1a",
             row(T("Is", size=30), M(r"\begin{pmatrix}0.7\\0.5\end{pmatrix}", size=40),
                 T("a probability vector?", size=30)),
             row(T("No.", size=30, bold=True), M(r"0.7 + 0.5 = 1.2 \neq 1", size=38))),
            ("q2", "q2a",
             row(T("What is the second column of", size=30),
                 M(r"\mathrm{NOT} = \begin{pmatrix}0 & ?\\1 & ?\end{pmatrix}", size=40),
                 T("and why?", size=30)),
             row(M(r"\begin{pmatrix}1\\0\end{pmatrix}", size=40),
                 T("An input of 1 certainly becomes 0.", size=28), buff=0.45)),
            ("q3", "q3a",
             row(T("Is", size=30), M(half, size=40), T("a valid pair of amplitudes?", size=30)),
             row(T("No.", size=30, bold=True), M(r"\tfrac14 + \tfrac14 = \tfrac12 \neq 1", size=38),
                 T("The valid pair is", size=26), M(root, size=34))),
        ]
        self.questions(qas, "q0")

        end = T("Next:   1.2   States", size=44, bold=True)
        self.play(FadeOut(VGroup(self.head, self.badge, self.note)), run_time=0.4)
        with self.voice("z1"):
            self.play(FadeIn(end, shift=UP * 0.2), run_time=0.6)
        self.hold(0.8)
        self.play(FadeOut(end), run_time=0.6)
