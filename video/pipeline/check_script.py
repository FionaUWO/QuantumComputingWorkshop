"""Measure a narration script against the wording rules in STYLE_3B1B.md, section 9.

    python pipeline/check_script.py 1.2            (from video/)
    python pipeline/check_script.py 1.2 --scene c
    python pipeline/check_script.py some_transcript.txt     (one sentence per line, for comparison)

It counts; it does not judge. A script can pass every number and still read badly, so read it
aloud after it passes. The targets are what four 3Blue1Brown transcripts measure (the table in
section 9), loosened a little because our explainer is interrupted by a second speaker.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# words that tie a sentence to the one before it, or point at the picture
LINKS = ["so", "now", "but", "and", "well", "in fact", "for example", "that is", "this", "that", "these", "those",
         "then", "also", "of course", "remember", "notice", "here", "which", "because", "okay", "all right",
         "right", "yes", "exactly", "good", "instead", "still", "in other words", "that way", "after all"]
TARGETS = [  # (name, low, high, why)
    ("mean words per sentence", 14, 30, "short clipped sentences sound like slide bullets read aloud"),
    ("share of sentences with 8 words or fewer", 0, 0.25, "a short sentence is a punch; it only works when rare"),
    ("share of sentences that open with a link", 0.33, 1, "each sentence should lean on the one before"),
    ("share of sentences that say you", 0.15, 1, "talk to one person"),
    ("share of sentences that say I or we", 0.20, 1, "a person is explaining, not a textbook"),
    ("share of sentences that are questions", 0.03, 0.12, "questions carry weight when they are rare"),
]


def sentences(text):
    text = re.sub(r"\[[^\]]*\]\s*", "", text)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]


def measure(sents):
    n = len(sents)
    words = [len(s.split()) for s in sents]
    low = [s.lower() for s in sents]
    return {
        "mean words per sentence": sum(words) / n,
        "share of sentences with 8 words or fewer": sum(w <= 8 for w in words) / n,
        "share of sentences that open with a link": sum(any(re.match(re.escape(k) + r"\b", s) for k in LINKS)
                                                        for s in low) / n,
        "share of sentences that say you": sum(bool(re.search(r"\byou(r|'ll|'d|'re|'ve)?\b", s)) for s in low) / n,
        "share of sentences that say I or we": sum(bool(re.search(r"\b(i|i'll|i'm|i'd|i've|me|my|we|we'll|we're|us|our|let's)\b", s))
                                                   for s in low) / n,
        "share of sentences that are questions": sum(s.endswith("?") for s in sents) / n,
    }


def show(title, sents):
    got = measure(sents)
    print(f"{title}: {len(sents)} sentences, {sum(len(s.split()) for s in sents)} words")
    bad = 0
    for name, lo, hi, why in TARGETS:
        v = got[name]
        ok = lo <= v <= hi
        bad += not ok
        val = f"{v:5.1f}" if "mean" in name else f"{v:5.0%}"
        want = f"{lo}-{hi}" if "mean" in name else f"{lo:.0%}-{hi:.0%}"
        print(f"  {'ok ' if ok else 'NO '} {val}  {name} (want {want})" + ("" if ok else f"   <- {why}"))
    return bad


def main():
    arg = sys.argv[1]
    if arg.endswith(".txt"):
        show(arg, [x.strip() for x in Path(arg).read_text(encoding="utf-8").splitlines() if x.strip()])
        return
    import build as B
    mod = B.load_script(arg)
    scene = sys.argv[sys.argv.index("--scene") + 1] if "--scene" in sys.argv else None
    lines = [(i, getattr(mod, "SPEAKER", {}).get(i, "A"), say) for i, _, say in mod.SEGS if not scene or i[0] == scene]
    # what the explainer says in a row is one turn; measure its sentences
    a_text = " ".join(t for _, who, t in lines if who == "A")
    bad = show(f"{arg} explainer", sentences(a_text))
    b_lines = [(i, t) for i, who, t in lines if who != "A"]
    if b_lines:
        total = sum(len(re.sub(r"\[[^\]]*\]", "", t).split()) for _, _, t in lines)
        b_words = sum(len(t.split()) for _, t in b_lines)
        print(f"  questioner: {len(b_lines)} lines, {b_words / total:.0%} of the words (want at most 20%)")
        # after the questioner speaks, the explainer's next words should pick up hers
        stop = set("the a an of to and is it in on that this i you so but are be at as with for they there's".split())
        for k, (i, who, t) in enumerate(lines[:-1]):
            if who == "A" or lines[k + 1][1] != "A":
                continue
            hers = {w for w in re.findall(r"[a-z']+", t.lower()) if w not in stop}
            reply = sentences(lines[k + 1][2])[0] if sentences(lines[k + 1][2]) else ""
            his = set(re.findall(r"[a-z']+", reply.lower()))
            if not hers & his:
                bad += 1
                print(f"  NO  {lines[k + 1][0]} does not pick up any word of {i}: \"{t}\" -> \"{reply}\"")
    print("all counts are inside the targets; now read it aloud" if not bad else f"{bad} thing(s) to look at")


if __name__ == "__main__":
    main()
