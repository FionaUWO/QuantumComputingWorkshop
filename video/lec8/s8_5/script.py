"""Narration for Lecture 8, Section 8.5 — The surface code.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 to 9,
and the reply rules in VIDEO_WORKFLOW.md at the project root). One numbered line per turn; ids
with the same first letter form one scene. The wording and the pauses are laid out in
storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds: 0.95 at the end of a scene, about 0.6
between two lines of the same speaker, 0.35 to 0.45 when the other speaker answers, and 1.1 to
1.3 for a thinking pause (nothing new appears on screen until it ends).

Picks up where 8.4 ends (a CSS code whose checks only touch four neighbouring qubits on a grid).
Source: src/content/lectures/08-stabilizer/05-the-surface-code.mdx (Kitaev 2003; Dennis,
Kitaev, Landahl and Preskill 2002; not in Nielsen and Chuang).
Keep word choice varied: no single word repeated over and over (the user's note on 8.3).
"""

TITLE = "8.5 — The surface code"
OUTFILE = "L8_5_SurfaceCode"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are, then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we meet the code that most quantum hardware is betting on.'),
    # --- A. Hook: to fix more errors, do the checks have to get bigger?
    ('a1', 'A', "Every code we've built so far has distance three, so each one can fix a single error and no more, and a real machine with thousands of qubits is going to need a lot more than that."),
    ('a2', 'A', 'So here is a question for you. If we want a code that can fix many errors at once, do you think its checks will have to reach across more and more qubits?'),
    ('a3', 'B', 'I would think so. More errors to catch, so each check has to look at more qubits?'),
    ('a4', 'A', "Well, that's what the codes so far would suggest, since Shor's checks already touch six qubits. But the surface code can be made as strong as you like, and every one of its checks still touches just four qubits sitting next to each other."),
    # --- B. The lattice and its two kinds of check
    ('b1', 'A', "Here's how it's laid out. Draw a square grid, put one qubit on every edge rather than on the points, and then glue the top edge to the bottom and the left edge to the right."),
    ('b2', 'A', "That gluing turns the flat sheet into the surface of a doughnut, and it's why this first version is called the toric code. With L squares in each direction, you end up with two L squared qubits."),
    ('b3', 'A', 'At every point where four edges meet, we put an X check on those four edges, and around every little square we put a Z check on the four edges of its border.'),
    ('b4', 'B', 'And a point and a square never clash?'),
    ('b5', 'A', "They don't, because a point and a square either share no edges at all or share two of them, and two clashes cancel, the same even overlap we needed for CSS codes in the last section."),
    ('b6', 'A', 'In hardware, each check gets an ancilla of its own placed in the middle of its four qubits, and four CNOTs to its nearest neighbours are all the wiring it needs.'),
    ('b7', 'A', "Counting is quick. Multiplying every point check together gives nothing, and so does multiplying every square check, so two of the checks aren't independent, and two L squared qubits minus two L squared minus two checks leaves two logical qubits."),
    # --- C. Errors are chains; the checks see only their ends
    ('c1', 'A', 'Now let a few Z errors land on edges that join up into a path, like this chain of four, and think about which point checks will notice.'),
    ('c2', 'A', 'Before I light anything up, take a guess. Which checks along this path do you think will fire?'),
    ('c3', 'B', 'All the ones along the path, I suppose?'),
    ('c4', 'A', 'Well, that seems natural, since every point on the path touches an error. But a point in the middle of the chain touches two errored edges, and two clashes cancel, so the checks that fire are just the two at its ends.'),
    ('c5', 'A', 'So the syndrome never shows you the chain, it shows you where the chain stops, and the decoder has to work backwards from those endpoints.'),
    ('c6', 'A', 'X errors behave the same way on the shifted grid whose points are the centres of the squares, so a chain of X errors lights up two square checks at its ends.'),
    # --- D. Loops: harmless ones and the ones that wrap around
    ('d1', 'A', 'And a chain that closes up into a loop has no ends at all, so it trips no check, and that is where the danger is.'),
    ('d2', 'A', 'If the loop just encloses a patch of the grid, it is the product of the square checks inside it, so it did nothing to the encoded state, much like the innermost region from section eight point two.'),
    ('d3', 'B', 'And a loop that goes all the way around the doughnut?'),
    ('d4', 'A', "A loop around the doughnut is the dangerous one, because it can't be written as a product of checks, so it slips past every test and still changes the encoded state, which makes it a logical operator."),
    ('d5', 'A', 'The shortest loop around the torus has L edges, so the distance is L, and that is the whole trick of this code: to make it stronger, you simply make the grid bigger, and the checks stay the same size.'),
    ('d6', 'B', 'So it really is two L squared, two, L.'),
    ('d7', 'A', "Right. And that last L is the part I like most, because whether an error is harmless or fatal now comes down to one geometric question, whether its loop can be shrunk to a point."),
    # --- E. Decoding by matching, and the flat version
    ('e1', 'A', "So how does the decoder work? It's handed a set of lit-up points, and it joins them in pairs with paths that are as short as possible, then applies errors along those paths to cancel them out."),
    ('e2', 'A', 'If its guess and the real error together form a loop that can be shrunk away, the encoded state comes back untouched, even if the guess took a different route.'),
    ('e3', 'A', 'It only fails when error and correction together wrap around the torus, and that takes about L over two errors lined up in a row, which gets rare fast as the grid grows.'),
    ('e4', 'A', 'Pairing points with the least total length is a classical matching problem, and there are algorithms that solve it in polynomial time.'),
    ('e5', 'A', 'And since nobody builds a doughnut-shaped chip, in practice the torus is cut open into a flat patch with two kinds of boundary, which holds one logical qubit and uses about d squared data qubits for distance d.'),
    # --- F. Closing, pointing to 8.6
    ('f1', 'A', 'So the surface code turns errors into chains, sees only their ends, and fails only when a chain wraps all the way around, which you can push as far away as you like by growing the grid.'),
    ('f2', 'B', 'But every gate that measures those checks can go wrong as well. Does adding more qubits really help?'),
    ('f3', 'A', "Adding qubits does help, but only if the hardware is good enough to begin with, and in section eight point six we'll see where that line sits, which is called the threshold."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,    # the other speaker answers
    'i2': 0.95,   # end of a scene
    'a1': 0.6,
    'a2': 1.2,    # thinking pause: do the checks have to get bigger?
    'a3': 0.35,   # the other speaker answers
    'a4': 0.95,   # end of a scene
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.45,   # the other speaker answers
    'b4': 0.35,   # the other speaker answers
    'b5': 0.6,
    'b6': 0.6,
    'b7': 0.95,   # end of a scene
    'c1': 0.6,
    'c2': 1.2,    # thinking pause: which checks fire?
    'c3': 0.35,   # the other speaker answers
    'c4': 0.6,
    'c5': 0.6,
    'c6': 0.95,   # end of a scene
    'd1': 0.6,
    'd2': 0.45,   # the other speaker answers
    'd3': 1.1,    # thinking pause: what does a loop around the torus do?
    'd4': 0.6,
    'd5': 0.45,   # the other speaker answers
    'd6': 0.35,   # the other speaker answers
    'd7': 0.95,   # end of a scene
    'e1': 0.6,
    'e2': 0.6,
    'e3': 0.6,
    'e4': 0.6,
    'e5': 0.95,   # end of a scene
    'f1': 0.45,   # the other speaker answers
    'f2': 0.35,   # the other speaker answers
    'f3': 0.95,   # end of the film
}

SPEAKER = {i: who for i, who, _ in LINES}
# build.py consumes (id, subtitle text, text sent to the voice)
# (a [tag] in a line is a direction to the voice: it is spoken to, never shown)
import re

# how the voice must say a word it would otherwise misread (the subtitle keeps the spelling);
# the lab name is said "Q A Con" (the user's correction, 2026-11-23)
# CNOT is said "C-not", not spelled out (the user's correction, 2026-11-24); the plural first
SAY = {'QAICON Lab': 'Q A Con Lab', 'CNOTs': 'C-nots', 'CNOT': 'C-not'}


def spoken(t):
    for word, say in SAY.items():
        t = t.replace(word, say)
    return t


SEGS = [(i, re.sub(r"\[[^\]]*\]\s*", "", t), spoken(t)) for i, _, t in LINES]
