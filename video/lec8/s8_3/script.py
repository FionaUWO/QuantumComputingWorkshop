"""Narration for Lecture 8, Section 8.3 — Three codes.  DRAFT.

A dialogue: speaker A explains, speaker B asks (rules in video/STYLE_3B1B.md, sections 7 to 9,
and the reply rules in VIDEO_WORKFLOW.md at the project root). One numbered line per turn; ids
with the same first letter form one scene. The wording and the pauses are laid out in
storyboard.md; change both files together.

PAUSE_AFTER is the silence after a line in seconds: 0.95 at the end of a scene, about 0.6
between two lines of the same speaker, 0.35 to 0.45 when the other speaker answers, and 1.1 to
1.3 for a thinking pause (nothing new appears on screen until it ends).

Picks up where 8.2 ends (a code where every single-qubit error is caught: three of them, each
with distance three).
Source: src/content/lectures/08-stabilizer/03-three-codes.mdx
(Nielsen and Chuang 10.5.6, and 10.3.4 for the counting bound).
"""

TITLE = "8.3 — Three codes"
OUTFILE = "L8_3_ThreeCodes"

# (id, speaker, line)
LINES = [
    # --- I. Opening: who we are, then the title of this section
    ('i1', 'A', 'Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University.'),
    ('i2', 'B', 'And today, we meet three codes that can fix any error on a single qubit.'),
    # --- A. Hook: Shor's code uses nine qubits; what is the fewest that could work?
    ('a1', 'A', 'Last time we ended on a question, whether a code can catch every possible error on a single qubit, and the answer is yes, as long as the lightest error that slips past all of its checks has a weight of at least three.'),
    ('a2', 'A', 'Peter Shor found the first code like that in 1995, and it spends nine physical qubits to protect a single qubit of information, which does feel like rather a lot.'),
    ('a3', 'A', "So here's something for you to guess before we start. What do you think is the fewest qubits that could possibly do the job?"),
    ('a4', 'B', 'Hmm, there are three kinds of error, and the bit flip code needed three qubits for just one kind, so nine?'),
    ('a5', 'A', "Well, that's a very natural way to count, and it's the way Shor's code is put together. But the true answer is smaller than nine, and by the end you'll be able to see why, just by counting something else."),
    # --- B. The Shor code as a list of eight checks
    ('b1', 'A', "Let's write Shor's code the way we learned to in the last two sections, as a list of checks, which for nine qubits sitting in three blocks of three comes to eight strings."),
    ('b2', 'A', 'The first six are Z pairs inside each block, just like the checks of the bit flip code, so each block on its own can catch a bit flip on any of its three qubits.'),
    ('b3', 'A', 'The last two put an X on six qubits at a time, and they compare the signs of two neighbouring blocks, which is how a phase flip anywhere inside a block gets noticed.'),
    ('b4', 'A', "If you're wondering how a check like that actually gets measured, here is the circuit for the first one, where an extra ancilla qubit starts in zero and two CNOTs copy the parity of qubits one and two onto it, just as in lecture seven."),
    ('b5', 'A', 'An X check is read the other way round, with a Hadamard on the ancilla before and after, and in between the ancilla controls an X on each of its six qubits, so the ancilla reads one only when that check answers minus one.'),
    ('b6', 'B', 'But the X checks and the Z checks overlap. Do they still commute?'),
    ('b7', 'A', 'They do. Every Z pair sits either completely inside an X check or completely outside it, so the two share either two qubits or none, and an even number of clashes means they commute.'),
    ('b8', 'A', "And with nine qubits and eight independent checks, each one cutting the space in half, we're left with two dimensions, which is one logical qubit."),
    ('b9', 'A', 'Now here is something I found strange the first time I saw it, which is that the operator acting as a logical X on this code is made entirely of Z letters.'),
    ('b10', 'B', 'Wait, so Z on all nine qubits flips the logical bit?'),
    ('b11', 'A', 'Yes. Z on the three qubits of a block turns the plus inside that block into a minus, and logical zero and logical one differ by just those three signs, so Z on all nine swaps them, while X on all nine ends up playing the logical Z.'),
    # --- C. The Steane code: the syndrome spells out the address
    ('c1', 'A', 'Andrew Steane found a code that does the same job with seven qubits, and it comes from a classical idea, which is to write the numbers one to seven in binary as the columns of a table.'),
    ('c2', 'A', 'Each row of this table picks out four of the qubits, so if you draw each row as a circle around its four, you get three overlapping circles with one qubit in every region.'),
    ('c3', 'A', "Every circle carries two checks, X on its four qubits and Z on the same four, so that's six checks on seven qubits, which once again leaves one logical qubit."),
    ('c4', 'A', "And any two circles share two qubits, while a circle's own X and Z checks share all four, so every overlap is even and all six checks commute."),
    ('c5', 'A', 'So now suppose an X error hits qubit five. Before I light anything up, which circles do you think are going to notice it?'),
    ('c6', 'B', "Five sits inside circles one and three, but it's outside circle two."),
    ('c7', 'A', 'Exactly. So the three Z checks answer one, zero, one, and if you read that as a number in binary, it comes out as five.'),
    ('c8', 'A', 'You can watch the same thing happen in the circuit, where each circle gets its own ancilla, and the X on qubit five only reaches the two ancillas that have a CNOT coming from qubit five.'),
    ('c9', 'B', 'Oh, so the syndrome is just the address of the qubit?'),
    ('c10', 'A', "That's it. Each qubit's column in the table is its own number written in binary, so whichever qubit is hit, the syndrome spells out where, and a Z error does the same thing through the X checks."),
    # --- D. The five-qubit code, and why five is the fewest
    ('d1', 'A', 'The smallest code of all uses five qubits, and its four checks are really one string, X Z Z X I, shifted one place along each time.'),
    ('d2', 'A', 'Even a mixed check like this one can be measured the same way, with the ancilla sitting between two Hadamards and controlling an X on the first and fourth qubits and a Z on the second and third.'),
    ('d3', 'A', 'And now we can finally answer the question from the start, where the trick is just to count the different cases that a syndrome has to tell apart.'),
    ('d4', 'A', 'On n qubits, each qubit can suffer an X, a Y or a Z, which makes three n single-qubit errors, and then there is one more case where nothing went wrong at all.'),
    ('d5', 'A', 'With one logical qubit you have n minus one checks, and they give two to the n minus one different syndromes, so if every case needs a syndrome of its own, three n plus one can be at most two to the n minus one.'),
    ('d6', 'B', 'So let me try. Three qubits gives ten cases, but only four syndromes.'),
    ('d7', 'A', 'Right. Four qubits gives thirteen cases and still only eight syndromes, and five gives sixteen cases and exactly sixteen syndromes, so five is the first size that fits, with not a single syndrome left over.'),
    ('d8', 'B', 'So my nine was almost twice what we need.'),
    ('d9', 'A', "It was, but it was a very reasonable nine, since Shor's code was the first one anyone found. And I should be honest that this count assumes every error needs its own syndrome, which Shor's code doesn't bother with, because a Z on qubit one and a Z on qubit two look identical to its checks."),
    ('d10', 'A', "That turns out to be harmless, since the two of them multiply to one of the checks, and fixing the wrong one does nothing at all. A different argument shows that even codes like that can't get below five qubits."),
    # --- E. Closing, pointing to 8.4
    ('e1', 'A', 'So a code that fixes any single-qubit error needs a different syndrome for every way one qubit can go wrong, and five qubits turn out to be just enough room for that.'),
    ('e2', 'B', "Shor's and Steane's checks were all X's or all Z's, though. Is that a coincidence?"),
    ('e3', 'A', "Not a coincidence at all. In section eight point four we'll see how codes like those two can be built from a pair of classical codes, one for each kind of error."),
]

DEFAULT_PAUSE = 0.6
TURN_GAP = 0.2      # between turns that follow straight on
PAUSE_AFTER = {
    'i1': 0.4,   # the other speaker answers
    'i2': 0.95,   # end of a scene
    'a1': 0.6,
    'a2': 0.6,
    'a3': 1.2,   # thinking pause: how few qubits could do it?
    'a4': 0.35,   # the other speaker answers
    'a5': 0.95,   # end of a scene
    'b1': 0.6,
    'b2': 0.6,
    'b3': 0.6,
    'b4': 0.6,
    'b5': 0.45,   # the other speaker answers
    'b6': 0.35,   # the other speaker answers
    'b7': 0.6,
    'b8': 0.6,
    'b9': 0.45,   # the other speaker answers
    'b10': 1.1,   # thinking pause: how can Z letters make a logical X?
    'b11': 0.95,   # end of a scene
    'c1': 0.6,
    'c2': 0.6,
    'c3': 0.6,
    'c4': 0.6,
    'c5': 1.2,   # thinking pause: which circles notice X on qubit five?
    'c6': 0.35,   # the other speaker answers
    'c7': 0.6,
    'c8': 0.45,   # the other speaker answers
    'c9': 0.35,   # the other speaker answers
    'c10': 0.95,   # end of a scene
    'd1': 0.6,
    'd2': 0.6,
    'd3': 0.6,
    'd4': 0.6,
    'd5': 0.45,   # the other speaker answers
    'd6': 0.35,   # the other speaker answers
    'd7': 1.1,   # thinking pause: sixteen cases fill sixteen syndromes exactly
    'd8': 0.35,   # the other speaker answers
    'd9': 0.6,
    'd10': 0.95,   # end of a scene
    'e1': 0.45,   # the other speaker answers
    'e2': 0.35,   # the other speaker answers
    'e3': 0.95,   # end of the film
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
