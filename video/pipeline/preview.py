"""Contact sheets for checking layouts:  python pipeline/preview.py 1.1 [scene letters, e.g. bc]

Takes one frame at the end of each narration line from the latest 480p draft
(out/<lecture>/<section>/preview/draft.mp4) and tiles them 3 x 3 into
out/<lecture>/<section>/sheets/sheet_NN.png. Frames are in narration order,
left to right, top to bottom; the ids of each sheet are printed.
"""
import json
import subprocess
import sys

from build import out_dir

ep = sys.argv[1]
letters = sys.argv[2] if len(sys.argv) > 2 else ""
d = out_dir(ep)
marks = json.loads((d / "marks_low.json").read_text(encoding="utf-8"))["marks"]
video = d / "preview" / "draft.mp4"
sheets = d / "sheets"
sheets.mkdir(exist_ok=True)
for f in sheets.glob("*.png"):
    f.unlink()
pick = [m for m in marks if not letters or m["id"][0] in letters]
for n, m in enumerate(pick):
    t = m["start"] + m["dur"] + 0.15
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                    "-vf", "scale=640:360", str(sheets / f"f_{n:03d}.png")], check=True)
for k in range(0, len(pick), 9):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-start_number", str(k), "-i", str(sheets / "f_%03d.png"),
                    "-frames:v", "1", "-vf", "tile=3x3", str(sheets / f"sheet_{k // 9:02d}.png")], check=True)
for f in sheets.glob("f_*.png"):
    f.unlink()
for k in range(0, len(pick), 9):
    print(f"sheet_{k // 9:02d}:", " ".join(m["id"] for m in pick[k:k + 9]))
print(len(pick), "frames ->", len(list(sheets.glob("sheet_*.png"))), "sheets in", sheets)
