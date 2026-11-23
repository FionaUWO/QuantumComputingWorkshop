"""Narration for Lecture 8, Section 8.2 — Stabilizer codes.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 to 9,
and the reply rules in VIDEO_WORKFLOW.md at the project root). One numbered line per turn; ids
with the same first letter form one scene. The wording and the pauses are laid out in
storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds: 0.95 at the end of a scene, about 0.6
between two lines of the same speaker, 0.35 to 0.45 when the other speaker answers, and 1.1 to
1.3 for a thinking pause (nothing new appears on screen until it ends).

Picks up where 8.1 ends (the dimmed boxes, and the answers that come back minus one).
Source: src/content/lectures/08-stabilizer/02-stabilizer-codes.mdx
(Nielsen and Chuang 10.5.1 and 10.5.5).
"""

TITLE = "8.2 — Stabilizer codes"
OUTFILE = "L8_2_StabilizerCodes"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are, then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we find out what a code can actually see when something goes wrong.'),
    # --- A. Hook: an X on qubit one is caught, a Z on qubit one is not, and yet it did damage
    ('a1', 'A', 'At the end of the last section we flipped the first qubit of the bit flip code, and the state moved out to a box where the first check answers minus one, so we knew straight away that something had happened.'),
    ('a2', 'A', "Now let's hit the same qubit with a different error, a Z instead of an X, and ask both checks again."),
    ('a3', 'A', 'This time both checks answer plus one, exactly as if nothing had happened at all.'),
    ('a4', 'B', "Hmm, so a Z on one qubit just doesn't bother this code?"),
    ('a5', 'A', 'Well... it does bother it, quite a lot. If you look at the encoded state, zero zero zero plus one one one has turned into zero zero zero minus one one one, which is a different state, and not one of the checks noticed.'),
    ('a6', 'A', 'So the checks never look at the error itself, they only learn something about it, and the question for us is what exactly they learn, and what can slip past them unseen.'),
    # --- B. The syndrome: commute and the answer stays plus one, anticommute and it becomes minus one
    ('b1', 'A', "Let's start with a state in the code and a single check, which the state answers with plus one, so applying the check just gives the state back."),
    ('b2', 'A', 'Now suppose an error E hits first. If E commutes with the check, you can slide the check straight past it, and the damaged state still answers plus one.'),
    ('b3', 'A', 'But if E anticommutes with the check, sliding past it throws off a minus sign, like the ones we counted last time, and now the damaged state answers minus one.'),
    ('b4', 'B', "Every time? It isn't random?"),
    ('b5', 'A', "Not random at all, no. The answer depends only on the error and the check, and not on which encoded state you started from, which is why we can measure the checks without learning, or disturbing, the information we've stored."),
    ('b6', 'A', 'So if you write a one for every check that answers minus one, and a zero for every check that answers plus one, you get a short string of bits, which is called the syndrome.'),
    ('b7', 'A', "For the bit flip code, the three single flips give three different syndromes, one zero, one one, and zero one, and that's exactly why the three dimmed boxes could tell them apart."),
    # --- C. Syndromes add, and two flips can pass for one
    ('c1', 'A', 'Now, here is one for you to try. If qubits one and two both flip at once, what does each check say?'),
    ('c2', 'B', 'The first check sees two flips, so they cancel. And the second sees one, so zero one?'),
    ('c3', 'A', 'Spot on. Each check just counts the minus signs it gets from both errors together, so syndromes add up, with two ones making a zero, the way a parity does.'),
    ('c4', 'A', 'But zero one is also the syndrome of a single flip on qubit three, so a decoder that trusts it will flip qubit three, and now all three qubits have been flipped.'),
    ('c5', 'B', "Wait, so it lands on one one one? That's the other code word."),
    ('c6', 'A', "Right. X on all three qubits turns zero zero zero into one one one and back again, it passes both checks, and it isn't a check itself, so the code has quietly been turned into a different encoded state."),
    # --- D. Three kinds of error
    ('d1', 'A', 'So every Pauli error you could name lands in one of three regions, depending on what the checks say about it, and the innermost region is the easiest.'),
    ('d2', 'A', "If the error is one of the checks, or a product of them, like Z Z on the first two qubits, then it fixes every state in the code, so it did nothing at all and there's nothing to repair."),
    ('d3', 'A', "If the error anticommutes with at least one check, the syndrome isn't all zeros, and we say the error is detected, which covers every single flip in the bit flip code."),
    ('d4', 'A', 'And then there is this region in between, the errors that commute with every check without being checks themselves, like the Z on qubit one, or the X on all three.'),
    ('d5', 'B', 'So those are the ones that change the state and nobody notices.'),
    ('d6', 'A', "Exactly. An error in there passes every test and still changes the encoded state, so it's called a logical error, and the strings that live there are called the logical operators."),
    ('d7', 'A', 'I like that the same strings play both parts, because a logical operator applied by accident is a failure, while the same operator applied on purpose is a gate on the encoded qubit.'),
    # --- E. Weight and distance
    ('e1', 'A', "So how strong a code is comes down to how short its shortest logical error is, and we measure a string by counting the letters in it that aren't the identity, which is called its weight."),
    ('e2', 'A', 'The smallest weight of any logical error is the distance of the code, and an error lighter than that can never be a logical error, so it is either caught by the checks or does nothing at all.'),
    ('e3', 'A', 'So for the bit flip code, what do you think the distance is?'),
    ('e4', 'B', 'X X X is the logical error, so three?'),
    ('e5', 'A', "Well, that's the natural guess, because it's the logical error we just met. But remember the Z on qubit one from the start, which sits in the same region with a weight of only one, so the distance of this code is one."),
    ('e6', 'A', 'And that matches what you saw in lecture seven, where this code could fix any one bit flip but not a general error on a single qubit.'),
    ('e7', 'A', 'In general, a set of errors can all be corrected as long as no two of them multiply to a logical error, and that is just what went wrong before, since X one X two times X three is X on all three.'),
    ('e8', 'A', 'So with distance d, any two errors of weight at most d minus one over two, rounded down, multiply to something lighter than d, and a code of distance d corrects every one of them.'),
    # --- F. Close, towards 8.3
    ('f1', 'A', 'So the checks never see an error itself, only the pattern of which checks it anticommutes with, and a code is only as strong as the lightest error that none of them can see.'),
    ('f2', 'B', 'Then can we build a code where every single-qubit error gets caught?'),
    ('f3', 'A', "We can, and in section eight point three we'll meet three of them, each with distance three, so any error on a single qubit is not only caught but corrected."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,    # the other speaker answers
    'i2': 0.95,   # end of a scene
    'a1': 0.6,
    'a2': 0.6,
    'a3': 0.45,   # the other speaker answers
    'a4': 1.1,    # thinking pause: did the Z do nothing?
    'a5': 0.6,
    'a6': 0.95,   # end of a scene
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.45,   # the other speaker answers
    'b4': 0.35,   # the other speaker answers
    'b5': 0.6,
    'b6': 0.6,
    'b7': 0.95,   # end of a scene
    'c1': 1.2,    # thinking pause: what does each check say for X1 X2?
    'c2': 0.35,   # the other speaker answers
    'c3': 0.6,
    'c4': 1.1,    # thinking pause: what has the decoder done?
    'c5': 0.35,   # the other speaker answers
    'c6': 0.95,   # end of a scene
    'd1': 0.6,
    'd2': 0.6,
    'd3': 0.6,
    'd4': 0.45,   # the other speaker answers
    'd5': 0.35,   # the other speaker answers
    'd6': 0.6,
    'd7': 0.95,   # end of a scene
    'e1': 0.6,
    'e2': 0.6,
    'e3': 1.2,    # thinking pause: what is the distance?
    'e4': 0.35,   # the other speaker answers
    'e5': 0.6,
    'e6': 0.6,
    'e7': 0.6,
    'e8': 0.95,   # end of a scene
    'f1': 0.45,   # the other speaker answers
    'f2': 0.35,   # the other speaker answers
    'f3': 0.95,   # end of the film
}

SPEAKER = {i: who for i, who, _ in LINES}
# build.py consumes (id, subtitle text, text sent to the voice)
# (a [tag] in a line is a direction to the voice: it is spoken to, never shown)
import re

SEGS = [(i, re.sub(r"\[[^\]]*\]\s*", "", t), t) for i, _, t in LINES]
