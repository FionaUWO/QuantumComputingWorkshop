"""Draw the lab logo with a round Q (the user's choice, 2026-11-20).

The original logo (branding/logo-original.png, 1254 px) has a hand-drawn, uneven Q. This keeps its
letters "AI" as they are and replaces the Q with a true circle and a straight handle, in the same
place, thickness and colour, with the same gap where the handle passes through the ring.

    python branding/make_logo.py        (from the repository root; needs Pillow and numpy)

Writes, all with a transparent background (Q + AI only, no white disc):
    public/assets/img/logo.png        2048 px   the high-resolution logo
    public/assets/img/logo-800.png     800 px   used by the videos
    public/assets/img/lab-logo.png     192 px   the site header and favicon
and, for places that need an opaque square picture (a YouTube channel picture):
    branding/logo-on-white-800.png     800 px   the logo on white, with room for a circular crop
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "branding" / "logo-original.png"
IMG = ROOT / "public" / "assets" / "img"
PURPLE = (114, 30, 146, 255)
# geometry of the Q in units of an 800 px canvas (measured on the original)
CX, CY, R_OUT, R_IN = 390, 377, 363, 285
GAP = (41, 67)                      # degrees clockwise from 3 o'clock: where the ring is open
H0, H1, H_WIDTH = (528, 598), (702, 757), 84


def letters(size):
    """The original's "AI" (everything that is not the purple Q), on a transparent canvas."""
    a = np.array(Image.open(SRC).convert("RGBA")).astype(np.int32)
    purple = (a[..., 0] > a[..., 1] + 25) & (a[..., 3] > 0)
    a[purple, 3] = 0
    return Image.fromarray(a.astype(np.uint8), "RGBA").resize((size, size), Image.LANCZOS)


def round_q(size, over=4):
    """The Q as a ring with a gap and a handle with round ends, drawn large and scaled down."""
    n = size * over
    k = n / 800
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    box = lambda r: [(CX - r) * k, (CY - r) * k, (CX + r) * k, (CY + r) * k]
    d.pieslice(box(R_OUT), GAP[1], GAP[0] + 360, fill=PURPLE)
    d.ellipse(box(R_IN), fill=(0, 0, 0, 0))
    p0, p1, w = (H0[0] * k, H0[1] * k), (H1[0] * k, H1[1] * k), H_WIDTH * k
    d.line([p0, p1], fill=PURPLE, width=int(round(w)))
    for x, y in (p0, p1):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=PURPLE)
    return im.resize((size, size), Image.LANCZOS)


def logo(size):
    return Image.alpha_composite(letters(size), round_q(size))


def main():
    for name, size in (("logo.png", 2048), ("logo-800.png", 800), ("lab-logo.png", 192)):
        logo(size).save(IMG / name)
        print("wrote", IMG / name, size)
    # opaque version: the logo at 62% of a white square, so a circular crop keeps all of it
    side, inner = 800, 496
    card = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    card.alpha_composite(logo(inner), ((side - inner) // 2, (side - inner) // 2))
    card.convert("RGB").save(ROOT / "branding" / "logo-on-white-800.png")
    print("wrote", ROOT / "branding" / "logo-on-white-800.png")


if __name__ == "__main__":
    main()
