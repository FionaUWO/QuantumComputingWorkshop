"""Narration for Lecture 8, Section 8.1 — The Pauli group and stabilizers.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 to 9).
One numbered line per turn; ids with the same first letter form one scene. The wording and the
pauses are laid out in storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds, following what was settled for section 1.2:
0.95 at the end of a scene, about 0.6 between two lines of the same speaker, 0.35 to 0.45 when
the other speaker answers, and 1.1 to 1.3 for a thinking pause (nothing new appears on screen
until it ends).

Cut to about six minutes on 2026-11-23 at the user's request (it was about eight): the three
quick commutation examples, the proof that anticommuting strings share no state, the balance
that shows why each check keeps exactly half, and the remark about minus the identity went.

Source: src/content/lectures/08-stabilizer/01-the-pauli-group-and-stabilizers.mdx
(Nielsen and Chuang 10.5.1).
"""

TITLE = "8.1 — The Pauli group and stabilizers"
OUTFILE = "L8_1_Stabilizers"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are, then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we want a much shorter way to write down a quantum code.'),
    # --- A. Hook: two descriptions of one code, and what happens to each as the code grows
    ('a1', 'A', 'In lecture seven we described the bit flip code in two quite different ways, without making any fuss about it.'),
    ('a2', 'A', 'The first way was to write out its states, so here are all eight basis states of three qubits, and you can see that the code only ever uses these two.'),
    ('a3', 'A', 'The second way was a pair of questions, do the first two bits agree, and do the last two agree, which we wrote as Z Z on one pair and Z Z on the other.'),
    ('a4', 'A', 'Now watch what happens to each of these descriptions as I keep adding qubits.'),
    ('a5', 'B', "The left one explodes. But couldn't you just store the amplitudes that aren't zero?"),
    ('a6', 'A', "Storing only the ones that aren't zero is a good instinct, but for the codes at the end of this lecture, even those keep doubling as the code grows, while the list on the right just gets a few lines longer."),
    ('a7', 'A', 'So in this section I want to show you how a short list of questions can pin down a state, and how you can read off, from the list alone, how much room it leaves.'),
    # --- B. The alphabet: Pauli strings, and why a string is a question
    ('b1', 'A', "Let's start with the alphabet these questions are written in, which has only four letters, the identity and the three Pauli matrices X, Y and Z."),
    ('b2', 'A', 'To act on several qubits you just line the letters up, one for each qubit, so this string means X on the first qubit, nothing on the second, and Z on the third.'),
    ('b3', 'A', 'We also allow a sign out in front, and all the strings you can make this way are together called the Pauli group.'),
    ('b4', 'B', 'You called them questions, though. How is a string of matrices a question?'),
    ('b5', 'A', "It's a question because each string we'll use has only two possible answers, plus one and minus one."),
    ('b6', 'A', 'Take Z Z on the first two qubits, and feed it this state, where the first two bits agree. Each Z turns a one into a minus sign, the two signs cancel, and the answer is plus one.'),
    ('b7', 'A', 'But here the first two bits disagree, so only one minus sign appears, nothing cancels it, and the answer is minus one.'),
    # --- C. Two questions at once: commute or anticommute
    ('c1', 'A', 'Now, once you have two questions, you need to know whether one state can answer plus one to both, and that comes down to whether the two strings commute.'),
    ('c2', 'A', "For a single qubit you already know how this goes, because X followed by Z is minus Z followed by X, and that's what we mean when we say the two anticommute."),
    ('c3', 'A', 'For longer strings you compare them slot by slot, and every slot where the two hold different letters, with neither of them the identity, contributes one of these minus signs.'),
    ('c4', 'A', "So here's one for you to try. This is X X on two qubits, and this is Z Z on the same two. Do they commute?"),
    ('c5', 'B', "X and Z don't commute, so I'd say no."),
    ('c6', 'A', "You're right that X and Z don't commute, but notice that there are two slots here, and each of them gives a minus sign. Those two minus signs cancel, so these strings commute after all."),
    ('c7', 'A', "And that's the whole rule. An even number of clashing slots means the two strings commute, while an odd number means they anticommute, and then no state at all can answer plus one to both."),
    # --- D. The space a list fixes; the Bell state from two strings
    ('d1', 'A', "So let's take a list of strings that do commute, and collect every state that answers plus one to all of them."),
    ('d2', 'A', 'With two qubits there are four basis states, and the question Z Z keeps the two where the bits agree, zero zero and one one.'),
    ('d3', 'A', 'The question X X swaps those two with each other, so answering plus one to it means carrying the same amplitude on both.'),
    ('d4', 'B', "So that leaves one state. Isn't that the Bell state?"),
    ('d5', 'A', 'Yes, it leaves exactly one state, the Bell state from lecture two, and look at what it took to pin it down, two short strings instead of four amplitudes.'),
    ('d6', 'A', 'The set of states that a list fixes like this is called the space stabilized by the list, and the list itself, together with all the products of its strings, is called the stabilizer.'),
    ('d7', 'A', 'The strings you actually write down are its generators, and those are the only ones you ever need to check.'),
    # --- E. Every check halves the space
    ('e1', 'A', 'Now we can go back to the bit flip code, and watch its two checks do their work on all eight dimensions of three qubits.'),
    ('e2', 'A', 'The first check, Z Z on qubits one and two, answers plus one on exactly half of them, so it keeps this half, and we can dim the rest.'),
    ('e3', 'A', "The second check asks about qubits two and three, and it cuts across the first one, so again only half of what's left survives."),
    ('e4', 'A', 'So with three qubits and two checks, how many dimensions do you think are left?'),
    ('e5', 'B', "Eight, then four, then two. That's one qubit."),
    ('e6', 'A', "Yes, two dimensions, which is one qubit's worth of room, and those two are exactly zero zero zero and one one one, the code space we started with."),
    ('e7', 'A', "And the same thing happens for any number of qubits. You start with two to the n dimensions, every new check halves that, and after n minus k checks you're left with two to the k, which is room for k qubits."),
    ('e8', 'B', 'Any check at all? What if I add Z on one and Z on three?'),
    ('e9', 'A', "Good, Z on one and three is a nice one to try, because it's just the product of the two checks we already have, so this cut removes nothing."),
    ('e10', 'A', "That's why the count only works for independent checks, where none of them is a product of the others."),
    # --- F. The cost of each description; what was left out
    ('f1', 'A', 'So for fifty qubits, the list is at most fifty strings of fifty letters, which is about five thousand bits, while the amplitudes come to two to the fifty complex numbers, around a million billion.'),
    ('f2', 'B', 'So can every state be written as a list like this?'),
    ('f3', 'A', "No, not every state, and I should be honest about that. Only very special states can be written as a list like this, but they happen to include every code we'll meet in the rest of the lecture."),
    # --- G. Close, towards 8.2
    ('g1', 'A', "So a code doesn't have to be handed to you as a table of amplitudes. You can hand over a short list of questions instead."),
    ('g2', 'B', 'And the three boxes we dimmed, are those just thrown away?'),
    ('g3', 'A', "They're not thrown away at all, and I think that's the best part. Those three boxes are where a single bit flip sends the code, and which box you land in tells you which qubit was flipped."),
    ('g4', 'A', "That's what we'll take up next, in section eight point two, where the answers that come back minus one turn into the syndrome."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,    # the other speaker answers
    'i2': 0.95,   # end of a scene
    'a1': 0.6,
    'a2': 0.6,
    'a3': 0.6,
    'a4': 0.45,   # the picture grows, then the other speaker answers
    'a5': 1.1,    # thinking pause: would storing the non-zero ones be enough?
    'a6': 0.6,
    'a7': 0.95,   # end of a scene
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.4,    # the other speaker answers
    'b4': 0.45,   # the other speaker answers
    'b5': 0.6,
    'b6': 0.6,
    'b7': 0.95,   # end of a scene
    'c1': 0.6,
    'c2': 0.6,
    'c3': 0.6,
    'c4': 1.3,    # thinking pause: do XX and ZZ commute?
    'c5': 0.35,   # the other speaker answers
    'c6': 0.6,
    'c7': 0.95,   # end of a scene
    'd1': 0.6,
    'd2': 0.6,
    'd3': 0.45,   # the other speaker answers
    'd4': 0.35,   # the other speaker answers
    'd5': 0.6,
    'd6': 0.6,
    'd7': 0.95,   # end of a scene
    'e1': 0.6,
    'e2': 0.6,
    'e3': 0.6,
    'e4': 1.2,    # thinking pause: how many dimensions are left?
    'e5': 0.35,   # the other speaker answers
    'e6': 0.6,
    'e7': 0.4,    # the other speaker answers
    'e8': 0.45,   # the other speaker answers
    'e9': 0.6,
    'e10': 0.95,  # end of a scene
    'f1': 0.45,   # the other speaker answers
    'f2': 0.45,   # the other speaker answers
    'f3': 0.95,   # end of a scene
    'g1': 0.45,   # the other speaker answers
    'g2': 1.1,    # thinking pause: are the dimmed boxes wasted?
    'g3': 0.6,
    'g4': 0.95,   # end of the film
}

SPEAKER = {i: who for i, who, _ in LINES}
# build.py consumes (id, subtitle text, text sent to the voice)
# (a [tag] in a line is a direction to the voice: it is spoken to, never shown)
import re

SEGS = [(i, re.sub(r"\[[^\]]*\]\s*", "", t), t) for i, _, t in LINES]
