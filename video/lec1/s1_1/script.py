"""Narration for Lecture 1, Section 1.1 — From bits to amplitudes.  DIALOGUE VERSION, draft.

Rewritten on 2026-11-20 from the single-voice script (kept in git history) as a dialogue, at
the user's request: speaker A explains, speaker B asks. The ids and the order of the lines are
unchanged, because the scene shows its pictures by id; only the wording and the speaker of each
line are new. Rules: video/STYLE_3B1B.md, sections 7 to 9. In particular:

  - A speaks in connected sentences of about twenty words, not in clipped points.
  - After B speaks, A's first words affirm her and pick up what she said.
  - About 0.6 s between two sentences of one speaker, 0.35 s when the other speaker answers,
    0.95 s at the end of a scene, and 1.1 s or more where the viewer should think.

No line may announce what is coming ("in this section we'll see...", a list of the next
sections): the user ruled that out for every film on 2026-11-23. A teaser is fine; an outline is not.

Source for every statement: src/content/lectures/01-qubit/01-from-bits-to-amplitudes.mdx
(Nielsen and Chuang, Section 1.2).
"""
import re

TITLE = "1.1 — From bits to amplitudes"
OUTFILE = "L1_1_From_bits_to_amplitudes"

# (id, speaker, line)
LINES = [
    # --- I. Opening: the logo, the lab's name, then the title of the section
    ("i1", "A", "Hello everyone, and welcome. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University."),
    ("i2", "B", "And today, we want to find out what makes a qubit different from a random bit."),

    # --- A. The puzzle: a coin stays random, a qubit under two H gates does not
    ("a1", "A", "Let's start with something familiar: if you flip a fair coin, what you get is a random bit."),
    ("a2", "A", "Flip it again and it's still random, and even if you flip it a hundred times, it never gets any easier to predict."),
    ("a3", "A", "Now, a qubit behaves differently, and this is where it gets strange."),
    ("a4", "A", "There is a gate called H, and if you apply it once and then measure the qubit, the result is a fair coin flip."),
    ("a5", "A", "But apply it a second time, and the outcome is certain again."),
    ("a6", "B", "Wait, so where did the randomness go?"),
    ("a7", "A", "That's exactly the question, where the randomness goes, and the answer is stranger than you might expect."),

    # --- B. A random bit is a probability vector
    ("b1", "A", "So let's begin with a bit that we're unsure about."),
    ("b2", "A", "We can describe it with two numbers, the probability that it is zero, and the probability that it is one."),
    ("b3", "A", "If you stack those two numbers in a column, like this, you get what's called a probability vector."),
    ("b4", "B", "So both numbers are at least zero, and together they add up to one?"),
    ("b5", "A", "Yes, at least zero and adding up to one, always. For example, a bit that is zero seven times out of ten is the vector zero point seven, zero point three."),
    ("b6", "A", "Two of these vectors are special: this one, E zero, means the bit is certainly zero, and this one, E one, means it is certainly one."),
    ("b7", "A", "And every other probability vector is a mixture of these two, so a fair coin, for instance, is just half of each."),

    # --- C. Operations: read a matrix by columns
    ("c1", "A", "Now let's actually do something to the bit, and take the NOT gate, which turns a zero into a one, and a one into a zero."),
    ("c2", "A", "To write down what an operation like this does, we use a matrix, and here's the trick I'd like you to remember: read it one column at a time."),
    ("c3", "A", "The first column tells you what happens to a bit that is certainly zero, and the second column, what happens to a bit that is certainly one."),
    ("c4", "A", "So for NOT, a zero certainly becomes a one, which makes the first column zero, one."),
    ("c5", "B", "Then a one certainly becomes a zero, so the second column must be one, zero."),
    ("c6", "A", "Exactly, one, zero. Now let's try a noisy channel, which flips the bit only with some small probability, epsilon."),
    ("c7", "A", "Here a zero stays zero with probability one minus epsilon, and becomes a one with probability epsilon, and that gives us the first column."),
    ("c8", "B", "And in the second column, a one stays one with probability one minus epsilon, and flips to zero with probability epsilon."),
    ("c9", "A", "Exactly right, so that's epsilon on top and one minus epsilon below. Notice that each column is itself a probability vector, and matrices like this are called stochastic matrices."),
    ("c10", "A", "Here's one more example: suppose we throw the bit away and just flip a fair coin instead, so that both columns are one half, one half."),
    ("c11", "A", "If you apply that twice, nothing changes, because a fair coin that's flipped again is still a fair coin."),

    # --- D. Why no coin can do what H does
    ("d1", "B", "So couldn't one of these stochastic matrices just do what H does?"),
    ("d2", "A", "Good question, so let's suppose one of them does. Say some matrix M turns a certain zero into a fair coin."),
    ("d3", "A", "Now we apply M a second time, at a point where the bit is zero half of the time, and one the other half."),
    ("d4", "A", "And the thing I want you to notice is that M acts on each of those cases separately."),
    ("d5", "A", "So follow the first case, where the bit is zero and M makes it a fair coin again, which means that one quarter of the time, we end up at one."),
    ("d6", "A", "Now for the second case, and here's the point: whatever M does down here, it can only add probability, and it can never take that quarter away."),
    ("d7", "B", "So outcome one keeps a probability of at least a quarter, whatever happens."),
    ("d8", "A", "Right, at least a quarter, and that means certainty never comes back. Probabilities add. They never cancel."),

    # --- E. Two changes: amplitudes may be negative, and their squares total one
    ("e1", "A", "So what does quantum theory do differently? Surprisingly little, actually, because it keeps the same picture, a column of two numbers that gets acted on by matrices."),
    ("e2", "A", "Let's start again from the fair coin, one half, one half."),
    ("e3", "A", "And now here is a qubit, whose entries are one over root two, and minus one over root two."),
    ("e4", "A", "That really is a minus sign, and no probability vector could ever look like that. So this is the first change: the entries are allowed to be negative, and they're called amplitudes."),
    ("e4b", "A", "They can even be complex numbers, but real ones are all we'll need for now."),
    ("e5", "A", "So what keeps numbers like these in check? Well, try squaring each one, and you get one half and one half, which together make exactly one."),
    ("e6", "A", "And that's the second change: it's the squares that have to total one, not the numbers themselves."),
    ("e7", "A", "If you drop the minus sign you get another qubit, one over root two, one over root two, and its squares total one as well. On the sphere we saw at the start, these two qubits point in opposite directions."),
    ("e8", "A", "There's one more rule, and it's the one that connects amplitudes to what we actually see: the square of each amplitude is the probability of that outcome."),
    ("e9", "B", "So if I measure either of these, I get zero half the time and one half the time. They both look like a fair coin."),
    ("e10", "A", "Exactly, they both look like a fair coin, and that is what a single H produces, at least as far as a measurement can tell."),
    ("e11", "A", "But look closely at the two vectors, because they are not the same: they differ by a sign."),
    ("e12", "A", "A measurement can't see that sign, but a second H can, and it sends the first vector back to certainly zero, and the other one to certainly one."),
    ("e13", "A", "And the reason it works is that amplitudes can cancel, a negative number against a positive one."),

    # --- F. The two worlds side by side, and what comes next
    ("f1", "A", "So here are the two worlds we've met, side by side."),
    ("f2", "A", "A random bit is two probabilities, which are changed by stochastic matrices, and you read it out simply by looking."),
    ("f3", "A", "A qubit is two amplitudes, which are changed by unitary matrices, and you read it out by measuring."),
    ("f5", "A", "But the puzzle we started with is still open, because we haven't yet watched that cancellation happen between the two H gates."),

    # (The recap and the three check-yourself questions were removed on 2026-11-23 at the user's
    #  request: the film ends by pointing to section 1.2 and nothing else.)


    # --- Z. End card
    ("z1", "A", "And that's where we go next, starting with section one point two, on states."),
]

SPEAKER = {i: who for i, who, _ in LINES}

# --- Silence after a line, in seconds of the finished video ---------------------
DEFAULT_PAUSE = 0.6
SCENE_PAUSE = 0.5       # the change of picture adds about 0.5 s, so scenes are about 1 s apart
TURN_GAP = 0.35
_THINK = {
    "a5": 1.0,    # the surprise: hold on the all-same dots
    "a6": 1.1,    # her question hangs
    "d1": 1.1,    # the key question hangs
    "d6": 0.8,
    "d8": 0.8,    # the heaviest line of the film (the change of picture adds 0.9 s)
    "e3": 0.8,    # the minus sign
    "c3": 1.1,    # review: half a second more before c4
    "e7": 1.1,    # review: half a second more before e8
    "e11": 0.8,
    "e13": 0.7,   # the answer in miniature (the change of picture adds 1 s)
    "c9": 0.2, "r3": 0.1, "q3a": 0.35,   # the picture changes after these lines and makes the pause
    "q1": 5.0, "q2": 5.0, "q3": 5.0,   # time for the viewer to answer (the bar on screen)
}
_ids = [i for i, _, _ in LINES]
PAUSE_AFTER = {}
for _k, _i in enumerate(_ids):
    _last = _k == len(_ids) - 1 or _ids[_k + 1][0] != _i[0]
    if _i in _THINK:
        PAUSE_AFTER[_i] = _THINK[_i]
    elif _last:
        PAUSE_AFTER[_i] = SCENE_PAUSE
    elif SPEAKER[_ids[_k + 1]] != SPEAKER[_i]:
        PAUSE_AFTER[_i] = TURN_GAP
    else:
        PAUSE_AFTER[_i] = DEFAULT_PAUSE

# build.py consumes (id, subtitle text, text sent to the voice); a [tag] is for the voice only
# How the voice is told to say a word that it would otherwise spell out. The user picked this
# reading of the lab's name on 2026-11-23: "Q", "A", "con", said together as one name (they first
# picked "Q-Icon" from three takes, then asked for this instead); the subtitles and the screen
# keep the real spelling.
SAY_AS = {"QAICON": "Q-A-Con"}


def _spoken(text):
    for word, sound in SAY_AS.items():
        text = text.replace(word, sound)
    return text


SEGS = [(i, re.sub(r"\[[^\]]*\]\s*", "", t), _spoken(t)) for i, _, t in LINES]
