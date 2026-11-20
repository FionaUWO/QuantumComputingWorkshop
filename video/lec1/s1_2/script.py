"""Narration for Lecture 1, Section 1.2 — States.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 and 8).
One numbered line per turn; ids with the same first letter form one scene. The wording and
the pauses were agreed in storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds. The long ones (1.5 s and more) are thinking
pauses: nothing new appears on screen until they end. They were 1.5 to 2 s at first; the user
found the explainer's pauses too long (2026-11-20), so they are now 1.1 to 1.3 s, the other
pauses at most 0.45 s, and the explainer has a few light fillers ("Hmm", "Well", "um").

Source: src/content/lectures/01-qubit/02-states.mdx (Nielsen and Chuang 1.2, 2.1.4, 2.2.1).
"""

TITLE = "1.2 — States"
OUTFILE = "L1_2_States"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are (the same card as section 1.1), then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we want to see what the state of a qubit actually looks like.'),
    # --- A. Hook: two states the bars cannot tell apart
    ('a1', 'A', 'Last time, we ended on two columns of amplitudes that differ by nothing but a minus sign in the bottom entry.'),
    ('a2', 'A', 'And if you square the entries of either one, you get exactly the same thing, a half and a half, fifty-fifty.'),
    ('a3', 'B', "So if I measure them, I can't tell them apart."),
    ('a4', 'A', "You can't tell them apart, at least not by measuring like this, because either way every result looks like the flip of a fair coin."),
    ('a5', 'B', 'Then are they the same state?'),
    ('a6', 'A', "Well... no. They're not the same state, and seeing why is really the whole point of this section."),
    ('a7', 'A', 'What we need is a picture of a state where that minus sign is something you can actually see.'),
    # --- B. A state is an arrow of length one
    ('b1', 'A', "Let's start by drawing two axes, a horizontal one for the outcome zero and a vertical one for the outcome one."),
    ('b2', 'A', 'A column of two amplitudes is then just a point in this plane, so we can draw an arrow from the origin out to it, like this.'),
    ('b3', 'A', 'Now remember the rule from last time, that the squares of the two amplitudes have to add up to one.'),
    ('b4', 'B', "That's Pythagoras. So the arrow has length one."),
    ('b5', 'A', 'It is Pythagoras, and it means that every state of a qubit is an arrow of length one, so as the state changes, its tip just moves around this circle.'),
    ('b6', 'A', 'Physicists write an arrow like this with an angle bracket around its label, and they call it a ket.'),
    ('b7', 'A', 'The arrow lying along the zero axis is called ket zero, and the one pointing straight up the other axis is ket one.'),
    ('b8', 'A', 'Any other arrow you can build by taking some amount of ket zero, then some amount of ket one, and placing them tip to tail.'),
    ('b9', 'A', 'And when both of those amounts are non-zero, the state is called a superposition.'),
    ('b10', 'B', "I've heard that one. It means the qubit is zero and one at the same time, right?"),
    ('b11', 'A', "Well, zero and one at the same time is how it's usually put, and honestly I think that hides the picture. There is only one arrow here, and it just isn't pointing along either axis."),
    # --- C. The minus sign is a direction
    ('c1', 'A', "Now let's go back to those two columns from the start, and draw the first one as an arrow, like this."),
    ('c2', 'A', 'It sits exactly halfway between the two axes, and this particular arrow comes up so often that it has its own name, ket plus.'),
    ('c3', 'A', 'The second column is the same except for that minus sign on the bottom entry, so before I draw it, where do you think it points?'),
    ('c4', 'B', 'Same distance along zero, but down instead of up?'),
    ('c5', 'A', 'Down instead of up, exactly, because the bottom entry is the one that tells you how far to go along the ket one axis. This one is called ket minus.'),
    ('c6', 'A', "Now look over at the bars for these two states, and you'll see they are exactly the same, fifty-fifty both times."),
    ('c7', 'A', 'But the arrows themselves could hardly be more different.'),
    ('c8', 'B', "Wait, they're at a right angle."),
    ('c9', 'A', "Yes, they are at a right angle, and that's really the whole point. A probability can never be negative, so a random bit has nowhere to keep this difference, while a qubit keeps it in the direction of its arrow."),
    # --- D. Overlap: how much of one arrow lies along another
    ('d1', 'B', 'Is there a way to compute that right angle, without drawing it?'),
    ('d2', 'A', 'Definitely, there is a way to compute it, and it comes from asking how much of one arrow lies along the other, like the shadow you see here.'),
    ('d3', 'A', 'When the amplitudes are real numbers, you find that by multiplying the matching entries of the two columns and adding up the results.'),
    ('d4', 'A', 'So try it yourself for ket plus and ket minus, before I fill in the answer.'),
    ('d5', 'B', 'A half minus a half. Zero.'),
    ('d6', 'A', "You're right, a half minus a half, so the overlap is exactly zero, and that is what a right angle means. Two states like that are called orthogonal."),
    ('d7', 'A', 'The way we write an overlap is with a full bracket, where the left half is called a bra and the right half is the ket you already know.'),
    ('d8', 'A', 'And if you take the overlap of an arrow with itself, you get its length squared, which for a state is always one.'),
    # --- E. Another pair of axes
    ('e1', 'A', 'Now, two arrows of length one at a right angle is all that a pair of axes ever was, so nothing stops us from using these two as our axes instead.'),
    ('e2', 'A', 'In other words, ket plus and ket minus are just as good a basis as ket zero and ket one, and I can turn the whole picture so that they sit level.'),
    ('e3', 'A', "Notice that the arrow itself hasn't moved. Only its coordinates have changed, and each new coordinate is its overlap with one of the new axes."),
    ('e4', 'A', "So here's a quick check for you. In this new basis, what are the coordinates of ket zero?"),
    ('e5', 'B', 'It sits halfway between them. One over root two, twice.'),
    ('e6', 'A', "Halfway between them, yes, one over root two both times, and the squares still add to one, because the length of an arrow doesn't care which axes you measure it with."),
    # --- F. What was left out: complex amplitudes
    ('f1', 'A', "Okay, so I owe you a confession. Every arrow I've drawn so far had real numbers for its entries."),
    ('f2', 'A', 'In general the amplitudes can be complex numbers, and then each entry is itself a little arrow, sitting in its own disc.'),
    ('f3', 'B', "So a size, and a direction it's turned."),
    ('f4', 'A', "A size and a turn, that's exactly it, and here is one example that we'll carry with us through the rest of the lecture."),
    ('f5', 'A', "Its first entry has size one over root three and isn't turned at all, while the second is longer, and turned by forty-five degrees."),
    ('f6', 'A', 'If you square just the sizes you get one third and two thirds, which add up to one, so this really is a state.'),
    ('f7', 'A', 'And that minus sign from before turns out to be the simplest case of all, a pointer turned exactly halfway round.'),
    ('f8', 'A', "There's one last detail. With complex entries, the bra undoes each turn before multiplying, which is what keeps the overlap of an arrow with itself equal to its length squared."),
    # --- G. Close, towards 1.3
    ('g1', 'A', 'So a state carries more than a pair of probabilities. It also carries the signs and the turns of its amplitudes, which is why these two arrows are different states.'),
    ('g2', 'B', 'But measuring only showed me the bars.'),
    ('g3', 'A', "It only showed you the bars, and that's the question we're left with. How much of the arrow does a measurement actually let us see?"),
    ('g4', 'A', "That's what we'll take up next, in section one point three."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,   # the other speaker answers
    'i2': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'a1': 0.6,
    'a2': 0.45,   # the other speaker answers
    'a3': 0.35,   # the other speaker answers
    'a4': 0.4,   # the other speaker answers
    'a5': 0.5,   # the other speaker answers
    'a6': 0.6,
    'a7': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.35,   # the other speaker answers
    'b4': 0.45,   # the other speaker answers
    'b5': 0.6,
    'b6': 0.6,
    'b7': 0.6,
    'b8': 0.6,
    'b9': 0.4,   # the other speaker answers
    'b10': 1.1,   # thinking pause
    'b11': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'c1': 0.5,   # the user's own number (review 2)
    'c2': 0.6,
    'c3': 1.1,   # thinking pause
    'c4': 0.35,   # the other speaker answers
    'c5': 0.6,
    'c6': 0.6,
    'c7': 1.1,   # thinking pause
    'c8': 0.35,   # the other speaker answers
    'c9': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'd1': 0.45,   # the other speaker answers
    'd2': 0.6,
    'd3': 0.6,
    'd4': 1.1,   # thinking pause
    'd5': 0.35,   # the other speaker answers
    'd6': 0.6,
    'd7': 0.6,
    'd8': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'e1': 0.6,
    'e2': 0.85,
    'e3': 0.6,
    'e4': 1.3,   # thinking pause
    'e5': 0.6,   # the other speaker answers
    'e6': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'f1': 0.6,
    'f2': 0.45,   # the other speaker answers
    'f3': 0.35,   # the other speaker answers
    'f4': 0.6,
    'f5': 0.6,
    'f6': 0.6,
    'f7': 0.95,
    'f8': 0.95,   # end of a scene: 0.5 to 1 s before the next one
    'g1': 0.45,   # the other speaker answers
    'g2': 1.1,   # thinking pause
    'g3': 0.6,
    'g4': 0.95,   # end of a scene: 0.5 to 1 s before the next one
}

SPEAKER = {i: who for i, who, _ in LINES}
# build.py consumes (id, subtitle text, text sent to the voice)
# (a [tag] in a line is a direction to the voice: it is spoken to, never shown)
import re

SEGS = [(i, re.sub(r"\[[^\]]*\]\s*", "", t), t) for i, _, t in LINES]
