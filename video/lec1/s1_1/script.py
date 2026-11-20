"""Narration for Lecture 1, Section 1.1 — From bits to amplitudes.  DRAFT, not yet voiced.

Same idea as the pipeline in
  .../FT_Rewrite_Search/lessons/Research_Training/video/  (see WORKFLOW.md there):
one numbered line per sentence, ids with the same first letter form one scene.

Three things make the voice sound like a person rather than a reader:

  1. WORDING. The lines are written to be spoken: contractions, "let's", "here's the
     trick", short questions. A voice model reads a sentence the way it is written.
  2. PAUSES. Inside a line, write [0.6] for a 0.6-second breath. Between lines, PAUSE_AFTER
     gives the silence after a line, in seconds of the finished video.
  3. TONE. Each line has one of four readings (STYLES) and a note saying which word
     carries the stress.

SEGS is what build.py consumes: (id, subtitle text, text sent to the speech engine).
The subtitle is the line with the pause marks removed. See USE_BREAK_TAGS at the end
for what is sent to the voice.

Source for every statement: src/content/lectures/01-qubit/01-from-bits-to-amplitudes.mdx
(Nielsen and Chuang, Section 1.2).
"""
import re

TITLE = "1.1 — From bits to amplitudes"
OUTFILE = "L1_1_From_bits_to_amplitudes"

LINES = [
    # --- I. Opening: who we are and what today is about.
    # The lab's logo on a white disc, "QAICON Lab" and its full name; then the title of the section.
    ("i1", "Hello everyone. We are QAICON Lab, [0.3] the Quantum and AI for Computing, "
           "Optimization, and Networking Lab, at Western University."),
    ("i2", "Today, we're going to talk about what makes a qubit different from a random bit."),

    # --- A. The puzzle.
    # Left: a coin flips, lands, flips again; a row of 100 dots fills in about half and half both times.
    # Right: a Bloch sphere. One H swings the arrow from the pole to the equator; dots half and half.
    # A second H swings it back to the pole; all 100 dots the same. Question mark between the two halves.
    ("a1", "Flip a fair coin. [0.4] You get a random bit."),
    ("a2", "Flip it again. [0.3] Still random. [0.3] Flip it a hundred times, and it never gets easier to predict."),
    ("a3", "Now, a qubit behaves differently."),
    ("a4", "There is a gate called H. Apply it once, and measuring the qubit is a fair coin flip."),
    ("a5", "Apply it a second time, and [0.5] the outcome is certain again."),
    ("a6", "So where did the randomness go? [0.8] That's the question this lecture answers."),
    ("a7", "In this first section, we show that ordinary probability can't do it. "
           "Then we see what quantum theory changes."),

    # --- B. A random bit.
    # A box with "?" inside. Two bars labelled 0 and 1 grow to heights p0 and p1, then fold into a
    # column vector (p0, p1). Example (0.7, 0.3). Then e0 = (1, 0) and e1 = (0, 1) with captions
    # "certainly 0" / "certainly 1", and the fair coin written as 1/2 e0 + 1/2 e1.
    ("b1", "Let's start with a bit we're unsure about."),
    ("b2", "We describe it with two numbers: the probability that it is zero, [0.3] "
           "and the probability that it is one."),
    ("b3", "Stack them in a column. [0.3] This is a probability vector."),
    ("b4", "Both numbers are at least zero, and they add up to one."),
    ("b5", "For example, a bit that is zero seven times in ten is the vector "
           "zero point seven, zero point three."),
    ("b6", "Two vectors are special. E zero means certainly zero. [0.3] E one means certainly one."),
    ("b7", "Every probability vector is a mixture of these two. A fair coin is half of each."),

    # --- C. Operations: read a matrix by columns.
    # An empty 2x2 matrix. Column 1 is highlighted with the caption "input is certainly 0",
    # column 2 with "input is certainly 1". NOT is filled in one column at a time, each with a
    # small arrow diagram 0 -> 1, 1 -> 0. Then the noisy channel: arrows 0 -> 0 (1 - eps) and
    # 0 -> 1 (eps) fill column 1; column 2 by symmetry. Then F with both columns (1/2, 1/2),
    # and F applied twice to a bar chart that stays flat.
    ("c1", "Now let's do something to the bit. Take the NOT gate: [0.3] it turns zero into one, and one into zero."),
    ("c2", "To write down what an operation does, we use a matrix. [0.4] And here's the trick: read it one column at a time."),
    ("c3", "The first column says what happens to a bit that is certainly zero. [0.4] "
           "The second column, to a bit that is certainly one."),
    ("c4", "For NOT, zero certainly becomes one, so the first column is zero, one."),
    ("c5", "One certainly becomes zero, so the second column is one, zero."),
    ("c6", "Now a noisy channel. It flips the bit with a small probability, epsilon."),
    ("c7", "A zero stays zero with probability one minus epsilon, [0.3] "
           "and becomes one with probability epsilon. That is the first column."),
    ("c8", "The second column works the same way."),
    ("c9", "Each column is itself a probability vector. "
           "Matrices like this are called stochastic matrices."),
    ("c10", "One more example. Throw the bit away, and just flip a fair coin. "
            "Both columns are one half, one half."),
    ("c11", "Apply it twice, and nothing changes. [0.3] A fair coin, flipped again, is still a fair coin."),

    # --- D. Why no coin can do what H does.
    # A branching tree, left to right. Start: "certainly 0". First M: two branches of weight 1/2
    # to "0" and "1". Second M from the upper "0": two branches of 1/2, so the leaf "1" carries
    # 1/2 x 1/2 = 1/4, drawn as a solid block. Second M from the lower "1": a grey cloud "unknown,
    # but >= 0". The 1/4 block drops into a bar labelled "probability of 1", with the cloud able
    # to stack on top but never remove it. Final card: "Probabilities add. They never cancel."
    ("d1", "Now for the key question. [0.4] Could some stochastic matrix behave like H?"),
    ("d2", "Let's suppose one does. A matrix M turns a certain zero into a fair coin."),
    ("d3", "Apply M a second time. The bit is now zero half the time, and one half the time."),
    ("d4", "M acts on each case separately."),
    ("d5", "Follow the first case. The bit is zero, and M makes it a fair coin again. [0.3] "
           "So one quarter of the time, we end at one."),
    ("d6", "Now the second case. And here's the point. [0.4] Whatever M does here, it can only add probability. "
           "It can never take that quarter away."),
    ("d7", "So outcome one keeps a probability of at least one quarter."),
    ("d8", "Certainty doesn't come back. [0.6] Probabilities add. [0.5] They never cancel."),

    # --- E. Two changes. Examples first, the rules named afterwards.
    # The coin's vector (1/2, 1/2) on the left. On the right a column no coin could have:
    # (1/sqrt2, -1/sqrt2), the minus sign in orange; only then is it named "amplitudes".
    # Each entry grows a square whose area is its square; the two areas re-form into one
    # unit square ("= 1"). A third column (1/sqrt2, 1/sqrt2) does the same. Then the areas
    # turn into the bars 1/2, 1/2: identical to the coin's bars. An H box takes the two
    # qubit vectors to (1, 0) and (0, 1).
    ("e1", "So what does quantum theory do differently? [0.5] Surprisingly little. "
           "It keeps the same picture: a column of two numbers, acted on by matrices."),
    ("e2", "Start with the fair coin: [0.3] one half, one half."),
    ("e3", "Now here's a qubit. One over root two, [0.4] minus one over root two."),
    ("e4", "A minus sign. [0.4] No probability vector looks like that. "
           "That's the first change: the entries may be negative. They're called amplitudes."),
    ("e4b", "They can even be complex, [0.3] but real numbers are all we need for now."),
    ("e5", "So what keeps these numbers in check? [0.3] Square each one. "
           "You get one half, and one half, [0.3] and together they make one."),
    ("e6", "That's the second change: the squares must total one, not the numbers themselves."),
    ("e7", "Drop the minus sign, and you get another qubit: one over root two, one over root two. "
           "Its squares total one as well."),
    ("e8", "One more rule connects amplitudes to what we see. "
           "The square of each amplitude is the probability of that outcome."),
    ("e9", "So both of these qubits give zero and one half the time each. "
           "Measured, each looks exactly like a fair coin."),
    ("e10", "That is what one H produces: a fair coin, as far as a measurement can tell."),
    ("e11", "But look closely. [0.4] The two vectors are different. They differ by a sign."),
    ("e12", "A measurement can't see that sign. [0.4] A second H can. [0.4] "
            "It sends the first vector back to certainly zero, and the other to certainly one."),
    ("e13", "And it works because amplitudes can cancel: [0.4] a negative number against a positive one."),

    # --- F. The two worlds side by side, and what comes next.
    # A two-column table builds row by row: state / reading it out / operations. Then the lecture's
    # section list 1.2 ... 1.6 appears as a path, with 1.6 marked "back to the two H gates".
    ("f1", "Here are the two worlds, side by side."),
    ("f2", "A random bit: two probabilities, changed by stochastic matrices, read by looking."),
    ("f3", "A qubit: two amplitudes, changed by unitary matrices, read by measuring."),
    ("f4", "The next sections take these one at a time: states, measurement, "
           "a picture of a qubit, and gates, [0.3] which is where unitary matrices get explained."),
    ("f5", "Then, in section one point six, we come back to the two H gates, [0.3] "
           "and watch the cancellation happen."),

    # --- R. Recap: three numbered bullets slide in.
    ("r0", "Let's recap."),
    ("r1", "One. [0.4] A random bit is a probability vector. "
           "Operations are stochastic matrices, read column by column."),
    ("r2", "Two. [0.4] Probabilities only add. So no coin can turn randomness back into certainty."),
    ("r3", "Three. [0.4] A qubit holds amplitudes. They can be negative, and their squares total one."),

    # --- Q. Check yourself: question, 5-second bar, answer in green.
    ("q0", "Three quick questions. Try each one yourself, before the answer appears."),
    ("q1", "Question one. Is zero point seven, zero point five a probability vector?"),
    ("q1a", "No. [0.4] The entries add up to one point two, not one."),
    ("q2", "Question two. What is the second column of the NOT matrix, and why?"),
    ("q2a", "One, zero. [0.3] An input of one certainly becomes zero."),
    ("q3", "Question three. Is one half, one half a valid pair of amplitudes?"),
    ("q3a", "No. [0.4] The squares add up to one half. One over root two, twice, is the valid pair."),

    # --- Z. End card.
    ("z1", "Next up, section one point two: states."),
]

# --- Silence after a line, in seconds of the finished video ---------------------
# Lines not listed get DEFAULT_PAUSE. The last line of a scene gets SCENE_PAUSE unless listed.
# These gaps are added when the audio is assembled, after the 1.25x speed-up, so they cost
# no voice credits and are not shortened by the speed-up.
DEFAULT_PAUSE = 0.35
SCENE_PAUSE = 1.0
PAUSE_AFTER = {
    "i1": 0.6,
    "i2": 1.0,   # the opening ends; the coin comes in
    "a2": 0.7,   # let "never gets easier" land before the turn
    "a5": 1.0,   # the surprise: hold on the all-same dots
    "a6": 1.2,   # the question hangs
    "b3": 0.6,   # a new term
    "c2": 0.5,
    "c9": 0.7,   # a new term
    "d1": 0.9,   # the key question hangs
    "d4": 0.6,
    "d6": 0.8,
    "d8": 1.6,   # the heaviest line of the video
    "e3": 0.8,   # the minus sign
    "e4": 0.5,   # a new term
    "e4b": 0.6,
    "e5": 0.6,   # the unit square
    "e6": 0.6,
    "e11": 0.7,
    "e13": 1.4,  # the answer in miniature
    "f5": 1.2,
    "q1": 5.0, "q2": 5.0, "q3": 5.0,   # time for the viewer to answer
}

# --- Lines voiced together ---------------------------------------------------------
# `build.py 1.1 tts --grouped` sends each group to the voice as one request, so its sentences
# are read in one breath and in one tone; the recording is then cut back into lines. Inside a
# group the pause after a line is the one the voice made, so PAUSE_AFTER is zero there.
# A line that needs a long, deliberate silence after it should end its group.
# A group ends where the script wants a deliberate silence, so those silences stay under
# our control. Each group is voiced with no "next text", so its last sentence comes down
# to a full stop instead of rising as if more were coming.
GROUPS = [
    ["i1"], ["i2"],
    ["a1", "a2"], ["a3", "a4", "a5"], ["a6"], ["a7"],
    ["b1", "b2", "b3"], ["b4", "b5"], ["b6", "b7"],
    ["c1"], ["c2", "c3"], ["c4", "c5"], ["c6", "c7", "c8"], ["c9"], ["c10", "c11"],
    ["d1"], ["d2", "d3", "d4"], ["d5", "d6"], ["d7"], ["d8"],
    ["e1"], ["e2", "e3"], ["e4", "e4b"], ["e5", "e6"], ["e7"], ["e8", "e9", "e10"], ["e11"], ["e12"], ["e13"],
    ["f1", "f2", "f3"], ["f4", "f5"],
    ["r0", "r1", "r2", "r3"],
    ["q0"], ["q1"], ["q1a"], ["q2"], ["q2a"], ["q3"], ["q3a"],
    ["z1"],
]
for _g in GROUPS:
    for _i in _g[:-1]:
        PAUSE_AFTER[_i] = 0.0

# --- Tone of each line ------------------------------------------------------------
# The readings the pipeline's build.py can produce (its TAKE_STYLES). The numbers are
# ElevenLabs (stability, style): lower stability and higher style give more emotion.
STYLES = {
    "calm":     (0.65, 0.05),
    "neutral":  (0.50, 0.20),
    "livelier": (0.38, 0.45),
    "emphatic": (0.28, 0.65),
}

# id -> (reading, note). Lines not listed are "neutral". The note is for the person who
# listens to the take: which word carries the stress, what the feeling is. It is not sent
# to the voice.
TONE = {
    # A. The puzzle: start quietly, turn at a3, land the question at a6.
    "a1": ("calm",     "像在跟人聊天，不要像念稿"),
    "a2": ("neutral",  "Still random 带一点无奈；重音在 never"),
    "a3": ("livelier", "Now 之后微顿；differently 上扬，带点卖关子"),
    "a4": ("neutral",  "H 读清楚；fair coin flip 平着读"),
    "a5": ("emphatic", "停顿之后带惊讶；重音在 certain"),
    "a6": ("emphatic", "真的在好奇地发问；第二句放松下来"),
    "a7": ("calm",     "交代路线，语速略快"),
    # B. A random bit: patient, definitions slowed down.
    "b1": ("calm",     "放慢，重新起头，语气亲切"),
    "b3": ("neutral",  "probability vector 是新名词，放慢读"),
    "b5": ("livelier", "举例，轻快一点"),
    "b6": ("neutral",  "两个 certainly 都重读"),
    # C. Operations: a recipe, lively when a new example starts.
    "c1": ("livelier", "新话题起头；NOT 读清楚"),
    "c2": ("livelier", "像在分享一个小窍门；one column at a time 一词一顿"),
    "c3": ("neutral",  "前后两句对称"),
    "c4": ("neutral",  "承接上一句，不用重新起头"),
    "c6": ("livelier", "新例子起头；epsilon 读清楚"),
    "c7": ("neutral",  "放慢；one minus epsilon 和 epsilon 对比着读"),
    "c8": ("calm",     "快速带过，轻松"),
    "c9": ("neutral",  "stochastic matrices 是新名词，放慢读"),
    "c10": ("livelier", "just flip a fair coin 带一点玩笑感"),
    "c11": ("calm",    "still a fair coin 收得平，略带笑意"),
    # D. The argument: the most serious scene; d8 is the heaviest line of the video.
    "d1": ("emphatic", "认真起来；Could 起调高"),
    "d2": ("neutral",  "Let's suppose one does 像在和观众一起试"),
    "d4": ("calm",     "放慢，each case separately 读清楚"),
    "d5": ("neutral",  "重音在 one quarter"),
    "d6": ("emphatic", "here's the point 压低放慢；重音在 only add 和 never"),
    "d7": ("neutral",  "重音在 at least"),
    "d8": ("emphatic", "三个短句一句比一句沉；全片最重的一句"),
    # E. Two changes: relief after D, then build to the cancellation.
    "e1": ("livelier", "换一口气；Surprisingly little 带一点意外"),
    "e2": ("calm",     "平稳，回到熟悉的东西"),
    "e3": ("livelier", "重音在 minus，前面微顿；带一点卖关子"),
    "e4": ("neutral",  "A minus sign 放慢；amplitudes 是新名词，放慢读"),
    "e4b": ("calm",    "顺带一提，轻轻带过"),
    "e5": ("neutral",  "问句真的在问；Square each one 干脆；重音在最后的 one"),
    "e6": ("neutral",  "重音在 squares"),
    "e7": ("calm",     "快速带过，轻松"),
    "e9": ("neutral",  "重音在 exactly"),
    "e10": ("calm",    "as far as a measurement can tell 压低"),
    "e11": ("emphatic", "But look closely 压低，像提醒人注意；重音在 different 和 sign"),
    "e12": ("livelier", "A second H can 短而有力"),
    "e13": ("emphatic", "重音在 cancel；像揭开谜底"),
    # F. Side by side and what comes next.
    "f1": ("calm",     "平稳"),
    "f2": ("neutral",  "三段并列，节奏均匀"),
    "f3": ("neutral",  "和 f2 同样的节奏，便于对照"),
    "f5": ("livelier", "预告，带期待感"),
    # R. Recap: even and unhurried.
    "r0": ("calm",     "平稳"),
    "r2": ("neutral",  "重音在 only add"),
    "r3": ("neutral",  "重音在 negative"),
    # Q. Check yourself: questions rise, answers are short and flat.
    "q0": ("livelier", "邀请的语气"),
    "q1": ("neutral",  "疑问上扬"),
    "q1a": ("calm",    "No 干脆"),
    "q2": ("neutral",  "疑问上扬"),
    "q2a": ("calm",    "平稳"),
    "q3": ("neutral",  "疑问上扬"),
    "q3a": ("calm",    "No 干脆"),
    "z1": ("livelier", "收尾，轻快"),
}

# --- What build.py reads ----------------------------------------------------------
# The in-line marks [0.5] can be sent to the voice as break tags. A test on line a5
# (2026-11-19) showed the tag works, but the reading without it sounded better, so the
# marks are not sent: they stay in LINES as a note of where a breath belongs, and the
# voice finds its own from the punctuation. Set to True to try the tags again.
USE_BREAK_TAGS = False

_MARK = re.compile(r"\s*\[(\d+(?:\.\d+)?)\]\s*")


def _subtitle(text):
    """The line as shown on screen: pause marks removed."""
    return _MARK.sub(" ", text).strip()


def _spoken(text):
    """The line as sent to the voice."""
    if USE_BREAK_TAGS:
        out = _MARK.sub(lambda m: f' <break time="{m.group(1)}s" /> ', text).strip()
    else:
        out = _subtitle(text)
    # (A rule here once meant to lower-case "NOT" for the voice, but its pattern held two stray
    # control characters and never matched. The takes in use were made from "NOT" as written
    # and were approved by ear, so the text is now sent unchanged.)
    return out


SEGS = [(i, _subtitle(t), _spoken(t)) for i, t in LINES]
