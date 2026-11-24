"""Narration for Lecture 8, Section 8.4 — CSS codes.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 to 9,
and the reply rules in VIDEO_WORKFLOW.md at the project root). One numbered line per turn; ids
with the same first letter form one scene. The wording and the pauses are laid out in
storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds: 0.95 at the end of a scene, about 0.6
between two lines of the same speaker, 0.35 to 0.45 when the other speaker answers, and 1.1 to
1.3 for a thinking pause (nothing new appears on screen until it ends).

Picks up where 8.3 ends (Shor's and Steane's checks are all X's or all Z's: not a coincidence).
Source: src/content/lectures/08-stabilizer/04-css-codes.mdx (Nielsen and Chuang 10.4.1, 10.4.2).
Words to keep sparing (the user's note on 8.3): "exactly".
"""

TITLE = "8.4 — CSS codes"
OUTFILE = "L8_4_CSSCodes"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are, then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we build quantum codes out of classical ones.'),
    # --- A. Hook: copy a classical table into X checks and Z checks; does that always work?
    ('a1', 'A', "At the end of the last section we noticed that every check in Shor's code and in Steane's code is made entirely of X's or entirely of Z's, and in Steane's code both halves come from the same table of ones and zeros."),
    ('a2', 'A', 'That table is older than quantum computing by decades, since it belongs to the Hamming code, which engineers have used since the nineteen fifties to repair a single flipped bit in a message.'),
    ('a3', 'A', "So here's a tempting recipe. Take a classical code you like, write its table once with X's and once with Z's, and call the result a quantum code. Do you think that always works?"),
    ('a4', 'B', 'Hmm, the Z checks catch bit flips and the X checks catch phase flips, so as long as the code is good, right?'),
    ('a5', 'A', "Well, that's half of the answer, because a good code is certainly needed. But the half that's missing is the one genuinely quantum part of the story, so let's go and find it."),
    # --- B. What the table does classically
    ('b1', 'A', 'So what does a table like this actually do for a classical message? Each row picks out a few positions, and it asks whether the bits sitting in those positions add up to an even number.'),
    ('b2', 'A', 'A message passes when every row says even, and the messages that pass are the code, which in linear algebra is called the kernel of the table, with all the arithmetic done mod two.'),
    ('b3', 'A', 'Now if one bit flips, the rows that contain it start saying odd, and the pattern of odd rows you get is the column of the table at the position that flipped.'),
    ('b4', 'B', "Oh, that's the address trick from Steane's code."),
    ('b5', 'A', "Right. Now you can see where Steane's code got it from, and nothing quantum happens in this picture at all, it's an ordinary parity check, the kind of check the memory in your computer runs all day long."),
    # --- C. Two tables, and the one condition that makes them commute
    ('c1', 'A', "So now you take two tables with the same number of columns, which we'll call H X and H Z, and turn every row of the first into an X check and every row of the second into a Z check."),
    ('c2', 'A', 'Two X checks always commute, and so do two Z checks, since a letter never clashes with itself, which leaves just one kind of pair to worry about, an X check against a Z check.'),
    ('c3', 'A', 'And as we saw last time, an X and a Z clash on every qubit they share, so the pair commutes when they share an even number of qubits and anticommutes when that number is odd.'),
    ('c4', 'A', 'Let me try the tempting recipe on the smallest table we know, the two rows of the bit flip code, written once with X and once with Z.'),
    ('c5', 'B', 'X X I and I Z Z only share qubit two. So they anticommute!'),
    ('c6', 'A', "That's it. Qubit two is the single clash, so a perfectly good classical code still breaks the recipe, because one row of one table overlaps one row of the other an odd number of times."),
    ('c7', 'A', 'So the missing half is this. Every row of H X has to share an even number of ones with every row of H Z, and if you collect all those overlaps into one product, the condition reads H X times H Z transpose equals zero, mod two.'),
    ('c8', 'A', 'When that holds, the checks define a code, and the number of logical qubits is n minus the number of independent X checks minus the number of independent Z checks, the same halving count as before.'),
    # --- D. Two kinds of error, two classical decoders
    ('d1', 'A', "Once the checks commute, the two kinds of error stay out of each other's way. A bit flip only trips the Z checks, and the pattern it leaves is H Z times the error, so you can decode that half like an ordinary classical code."),
    ('d2', 'A', 'A phase flip trips nothing but the X checks, leaving H X times its pattern, and that half gets a classical decoder of its own.'),
    ('d3', 'B', 'And a Y error, which is a bit flip and a phase flip at once?'),
    ('d4', 'A', 'It lights up both halves at the same time, and each decoder fixes its own part of it, one undoing the bit flip and the other the phase flip, without ever needing to talk to each other.'),
    ('d5', 'A', "I find that the nicest part of the construction, because all the hard work of decoding a quantum code turns into two classical problems that people already knew how to solve."),
    # --- E. Back to Steane: the Hamming code contains its dual
    ('e1', 'A', "So let's go back to Steane's code, where both tables are the same H, and the condition becomes H times its own transpose equals zero."),
    ('e2', 'A', 'If you check, any two rows of the Hamming table share two ones, and each row shares four with itself, so every overlap is even, and the condition holds.'),
    ('e3', 'B', 'So the bit flip table failed, but the Hamming table passes.'),
    ('e4', 'A', "Right. Classical coding theorists have a name for a table like that, they say the code contains its dual, and it's the one extra demand that a quantum code makes on top of the classical theory."),
    # --- F. Closing, pointing to 8.5
    ('f1', 'A', 'So two classical codes laid over the same qubits, one for each kind of error, give you a quantum code as long as their tables overlap evenly, and codes built this way are called CSS codes, after Calderbank, Shor and Steane.'),
    ('f2', 'B', 'But these checks still reach right across the whole code. Do they have to?'),
    ('f3', 'A', "They don't, and in section eight point five we'll meet the surface code, a CSS code whose checks only ever touch four neighbouring qubits on a flat grid."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,    # the other speaker answers
    'i2': 0.95,   # end of a scene
    'a1': 0.6,
    'a2': 0.6,
    'a3': 1.2,    # thinking pause: does the recipe always work?
    'a4': 0.35,   # the other speaker answers
    'a5': 0.95,   # end of a scene
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.45,   # the other speaker answers
    'b4': 0.35,   # the other speaker answers
    'b5': 0.95,   # end of a scene
    'c1': 0.6,
    'c2': 0.6,
    'c3': 0.6,
    'c4': 1.2,    # thinking pause: do X X I and I Z Z commute?
    'c5': 0.35,   # the other speaker answers
    'c6': 0.6,
    'c7': 0.6,
    'c8': 0.95,   # end of a scene
    'd1': 0.6,
    'd2': 0.45,   # the other speaker answers
    'd3': 1.1,    # thinking pause: what does a Y do?
    'd4': 0.6,
    'd5': 0.95,   # end of a scene
    'e1': 0.6,
    'e2': 0.45,   # the other speaker answers
    'e3': 0.35,   # the other speaker answers
    'e4': 0.95,   # end of a scene
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
