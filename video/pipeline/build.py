"""Build one section's video: narration audio -> Manim render -> subtitles -> final MP4.

A section is named by its number, for example 1.1. Its files live in  video/lec1/s1_1/ :
    script.py       narration, pauses and tone (the source of truth for the text)
    scene.py        the Manim scene, class Main
    storyboard.md   what is on screen for each line
Everything generated goes to  video/out/lec1/s1_1/  (ignored by git).

Whole section
    python pipeline/build.py 1.1 tts        voice the narration; only new or changed sentences are sent out
    python pipeline/build.py 1.1 render     Manim render at 1080p (add --low for a quick 480p draft)
    python pipeline/build.py 1.1 mux        audio track, .srt, narration table, final MP4
    python pipeline/build.py 1.1 all        the three steps in order

Fine-tuning
    python pipeline/build.py 1.1 tts --scene a          voice only scene a
    python pipeline/build.py 1.1 preview --scene a      480p clip of one scene, with voice and subtitles
    python pipeline/build.py 1.1 takes --id c9 --n 3    several readings of one sentence to choose from
    python pipeline/build.py 1.1 pick --id c9 --take 2  use the chosen reading
    python pipeline/build.py 1.1 review                 review page (video + sentence list + note boxes)

The voice (engine, voice id, speed) is set in pipeline/voice.json. Run with the Manim
environment:  C:/Users/Yanwe/venvs/manim-video/Scripts/python.exe

Adapted from the pipeline of the series "From qubits to rewrite rules".
"""
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import textwrap
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent      # video/pipeline
ROOT = HERE.parent                          # video
OUT = ROOT / "out"
MAX_CHARS, MAX_LINES = 42, 2
# readings offered by `takes`: (label, stability, style). Lower stability and higher style
# give more emphasis and emotion.
TAKE_STYLES = [("neutral", 0.5, 0.2), ("livelier", 0.38, 0.45), ("emphatic", 0.28, 0.65),
               ("calm", 0.65, 0.05), ("very lively", 0.2, 0.8)]


# ---------------------------------------------------------------- where things are
def _parts(ep):
    lec, sec = ep.split(".")
    return f"lec{int(lec)}", f"s{int(lec)}_{int(sec)}"


def ep_dir(ep):
    """Source folder of a section: video/lec1/s1_1 for "1.1"."""
    a, b = _parts(ep)
    return ROOT / a / b


def out_dir(ep):
    """Output folder of a section: video/out/lec1/s1_1 for "1.1"."""
    a, b = _parts(ep)
    return OUT / a / b


_scripts = {}


def load_script(ep):
    if ep not in _scripts:
        path = ep_dir(ep) / "script.py"
        spec = importlib.util.spec_from_file_location(f"script_{ep.replace('.', '_')}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _scripts[ep] = mod
    return _scripts[ep]


def voice_cfg():
    return json.loads((HERE / "voice.json").read_text(encoding="utf-8"))


def spoken(mod):
    """[{id, say}] for every line: the text sent to the voice."""
    return [{"id": i, "say": say or sub} for i, sub, say in mod.SEGS]


def tone(mod, seg_id):
    """(stability, style) for a line, from the script's TONE and STYLES tables."""
    styles = getattr(mod, "STYLES", {})
    label = getattr(mod, "TONE", {}).get(seg_id, ("neutral", ""))[0]
    return styles.get(label, (None, None))


# ---------------------------------------------------------------- speech engine
def eleven_key():
    """The ElevenLabs key is read from the environment, never from a file in the repository."""
    import os
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:  # set with setx after this shell started: read the user's environment directly
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                key = winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0]
        except OSError:
            key = None
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set")
    return key.strip()


def to_wav(src, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ar", "44100", "-ac", "1",
                    "-c:a", "pcm_s16le", str(dst)], check=True)


def eleven_one(text, dst, cfg, before=None, after=None, stability=None, style=None):
    """One ElevenLabs request (paid, online): sends `text` and its neighbours to ElevenLabs."""
    import time
    import urllib.error
    import urllib.request

    st = dict(cfg.get("settings", {}))
    if stability is not None:
        st["stability"] = stability
    if style is not None:
        st["style"] = style
    body = {"text": text, "model_id": cfg.get("model", "eleven_multilingual_v2"),
            "voice_settings": {"stability": st.get("stability", 0.5),
                               "similarity_boost": st.get("similarity_boost", 0.75),
                               "style": st.get("style", 0.2), "use_speaker_boost": True,
                               "speed": round(1 + cfg.get("rate", 0) / 100, 2)}}
    if before:
        body["previous_text"] = before
    if after:
        body["next_text"] = after
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice']}?output_format=mp3_44100_128"
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"xi-api-key": eleven_key(), "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                audio = r.read()
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 5:
                time.sleep(5 + 5 * attempt)
                continue
            raise SystemExit(f"ElevenLabs refused the request: HTTP {e.code} {msg}")
    mp3 = Path(str(dst) + ".mp3")
    mp3.write_bytes(audio)
    to_wav(mp3, dst)
    mp3.unlink()


def trim(path):
    """Cut the silence at both ends of a recording."""
    with wave.open(str(path)) as w:
        fr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    loud = np.nonzero(np.abs(x.astype(np.int32)) > 300)[0]
    a, b = max(loud[0] - fr // 25, 0), min(loud[-1] + fr // 10, len(x))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fr)
        w.writeframes(x[a:b].tobytes())


def retime(src, dst, tempo):
    """Change the pace without changing the pitch; returns the new length in seconds."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", f"atempo={tempo}",
                    "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(dst)], check=True)
    with wave.open(str(dst)) as w:
        return round(w.getnframes() / w.getframerate(), 3)


def seg_key(cfg, say, tone_pair=(None, None)):
    blob = json.dumps([cfg["engine"], cfg["voice"], cfg.get("rate", 0), cfg.get("model"),
                       cfg.get("settings"), say, list(tone_pair)], sort_keys=True)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def retime_all(ep, cfg, items):
    """Bring every recording to the final pace and write durations.json. A line recorded with the
    voice's own speed setting (native.json) is sped up by less, so all lines end at the same pace."""
    d = out_dir(ep)
    nf = d / "native.json"
    native = json.loads(nf.read_text(encoding="utf-8")) if nf.exists() else {}
    durs = {}
    for it in items:
        src = d / "raw" / f"{it['id']}.wav"
        if src.exists():
            tempo = round(cfg.get("tempo", 1.0) / native.get(it["id"], 1.0), 4)
            durs[it["id"]] = retime(src, d / "wav" / f"{it['id']}.wav", tempo)
    (d / "durations.json").write_text(json.dumps(durs, indent=1), encoding="utf-8")
    return durs


def eleven_timed(text, cfg, before=None, after=None, speed=1.0):
    """One ElevenLabs request (paid, online) that also says when each character is spoken.
    Returns (mp3 bytes, characters, start times, end times)."""
    import base64
    import time
    import urllib.error
    import urllib.request

    st = cfg.get("settings", {})
    body = {"text": text, "model_id": cfg.get("model", "eleven_multilingual_v2"),
            "voice_settings": {"stability": st.get("stability", 0.5),
                               "similarity_boost": st.get("similarity_boost", 0.75),
                               "style": st.get("style", 0.2), "use_speaker_boost": True, "speed": speed}}
    if before:
        body["previous_text"] = before
    if after:
        body["next_text"] = after
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice']}/with-timestamps"
           "?output_format=mp3_44100_128")
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"xi-api-key": eleven_key(), "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 5:
                time.sleep(5 + 5 * attempt)
                continue
            raise SystemExit(f"ElevenLabs refused the request: HTTP {e.code} {msg}")
    al = data["alignment"]
    return (base64.b64decode(data["audio_base64"]), al["characters"],
            al["character_start_times_seconds"], al["character_end_times_seconds"])


def step_tts_groups(ep, scene=None, force=False):
    """Voice the lines the script lists in GROUPS one group per request, so the sentences of a
    group are read in one breath with one tone, then cut the recording back into its lines.

    Every line keeps the natural pause that follows it, so the lines laid end to end are the
    recording as it was spoken. All groups use the settings of voice.json (the per-line TONE
    table is not used), at the voice's own speed `group_speed`."""
    cfg = voice_cfg()
    mod = load_script(ep)
    d = out_dir(ep)
    raw = d / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (d / "wav").mkdir(exist_ok=True)
    items = spoken(mod)
    order = [it["id"] for it in items]
    say = {it["id"]: it["say"] for it in items}
    speed = cfg.get("group_speed", 1.0)
    cache_file, nf = d / "cache.json", d / "native.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    native = json.loads(nf.read_text(encoding="utf-8")) if nf.exists() else {}
    groups = [g for g in getattr(mod, "GROUPS", []) if not scene or g[0].startswith(scene)]
    todo = []
    for g in groups:
        text = " ".join(say[i] for i in g)
        key = seg_key(cfg, text, ("group", speed, "no next text"))
        if force or cache.get("group:" + g[0]) != key or not all((raw / f"{i}.wav").exists() for i in g):
            todo.append((g, text, key))
    print(f"{ep}: voicing {len(todo)} of {len(groups)} groups ({sum(len(t) for _, t, _ in todo)} characters): "
          f"{[g for g, _, _ in todo]}")
    for g, text, key in todo:
        k0 = order.index(g[0])
        # no next_text: told that more follows, the voice ends the group on a rising, unfinished
        # note; without it the last sentence comes down to a full stop
        mp3, chars, t0, t1 = eleven_timed(text, cfg, before=say[order[k0 - 1]] if k0 else None, speed=speed)
        whole = raw / f"group_{g[0]}.wav"
        mp3_file = raw / f"group_{g[0]}.mp3"
        mp3_file.write_bytes(mp3)
        to_wav(mp3_file, whole)
        (raw / f"group_{g[0]}.json").write_text(json.dumps({"chars": chars, "start": t0, "end": t1}),
                                                encoding="utf-8")
        with wave.open(str(whole)) as w:
            fr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        joined, pos, spans = "".join(chars), 0, []
        for i in g:                     # when each line starts and stops being spoken
            s = joined.index(say[i], pos)
            e = s + len(say[i]) - 1
            spans.append((t0[s], t1[e]))
            pos = e + 1
        loud = np.nonzero(np.abs(x.astype(np.int32)) > 300)[0]
        cuts = [max(loud[0] / fr - 0.04, 0.0)]
        cuts += [max(spans[k][1], spans[k + 1][0] - 0.08) for k in range(len(g) - 1)]
        cuts += [min(loud[-1] / fr + 0.10, len(x) / fr)]
        for k, i in enumerate(g):
            piece = x[int(cuts[k] * fr):int(cuts[k + 1] * fr)]
            with wave.open(str(raw / f"{i}.wav"), "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(fr)
                w.writeframes(piece.tobytes())
            native[i] = speed
            cache[i] = seg_key(cfg, say[i], tone(mod, i))
            gap = f", then {spans[k + 1][0] - spans[k][1]:.2f} s before the next line" if k + 1 < len(g) else ""
            print(f"  {i}: spoken {spans[k][0]:.2f}-{spans[k][1]:.2f} s{gap}")
        cache["group:" + g[0]] = key
        cache_file.write_text(json.dumps(cache, indent=1), encoding="utf-8")
        nf.write_text(json.dumps(native, indent=1), encoding="utf-8")
    durs = retime_all(ep, cfg, items)
    print(f"{ep}: {len(durs)} of {len(items)} lines have a recording")


# ---------------------------------------------------------------- steps
def step_tts(ep, force=False, scene=None):
    """Voice the narration. A sentence is sent out again only if its text, tone or the voice changed.
    With `scene`, only the lines whose id starts with that letter are voiced."""
    cfg = voice_cfg()
    if cfg["engine"] != "eleven":
        raise SystemExit("this pipeline is set up for the ElevenLabs voice (voice.json: engine = eleven)")
    mod = load_script(ep)
    d = out_dir(ep)
    raw = d / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (d / "wav").mkdir(exist_ok=True)
    cache_file = d / "cache.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    items = spoken(mod)
    (d / "tts.json").write_text(json.dumps(items, indent=1), encoding="utf-8")
    wanted = [n for n, it in enumerate(items) if not scene or it["id"].startswith(scene)]
    todo = [n for n in wanted
            if force or cache.get(items[n]["id"]) != seg_key(cfg, items[n]["say"], tone(mod, items[n]["id"]))
            or not (raw / f"{items[n]['id']}.wav").exists()]
    chars = sum(len(items[n]["say"]) for n in todo)
    print(f"{ep}: voicing {len(todo)} of {len(wanted)} sentences ({chars} characters): "
          f"{[items[n]['id'] for n in todo]}")
    for n in todo:
        it = items[n]
        dst = raw / f"{it['id']}.wav"
        stab, style = tone(mod, it["id"])
        eleven_one(it["say"], dst, cfg, before=items[n - 1]["say"] if n else None,
                   after=items[n + 1]["say"] if n + 1 < len(items) else None, stability=stab, style=style)
        trim(dst)
        cache[it["id"]] = seg_key(cfg, it["say"], tone(mod, it["id"]))
        cache_file.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    durs = retime_all(ep, cfg, items)
    subs = {i: sub for i, sub, _ in mod.SEGS}
    words = sum(len(subs[i].split()) for i in durs)
    total = sum(durs.values())
    print(f"{ep}: {len(durs)} of {len(items)} sentences voiced, {words} words, {total:.1f} s of speech "
          f"at tempo x{cfg.get('tempo', 1.0)}, {words / total * 60:.0f} words per minute")


def step_takes(ep, seg_id, n, text=None):
    """Record several readings of one sentence so the user can pick one by ear."""
    cfg = voice_cfg()
    mod = load_script(ep)
    items = spoken(mod)
    k = [it["id"] for it in items].index(seg_id)
    say = text if text else items[k]["say"]
    d = out_dir(ep) / "takes"
    d.mkdir(parents=True, exist_ok=True)
    print(f"{ep} {seg_id}: \"{say}\"  ({len(say) * n} characters for {n} takes)")
    for t in range(n):
        label, stab, style = TAKE_STYLES[t % len(TAKE_STYLES)]
        rawf = d / f"{seg_id}_take{t + 1}_raw.wav"
        eleven_one(say, rawf, cfg, before=items[k - 1]["say"] if k else None,
                   after=items[k + 1]["say"] if k + 1 < len(items) else None, stability=stab, style=style)
        trim(rawf)
        dur = retime(rawf, d / f"{seg_id}_take{t + 1}.wav", cfg.get("tempo", 1.0))
        print(f"  take {t + 1} ({label}: stability {stab}, style {style}): "
              f"{d / f'{seg_id}_take{t + 1}.wav'}  {dur:.1f} s")
    (d / f"{seg_id}_text.json").write_text(json.dumps({"say": say}), encoding="utf-8")


def use_recording(ep, seg_id, raw_wav):
    """Make an existing raw recording the voice of this line (no request is sent)."""
    cfg = voice_cfg()
    mod = load_script(ep)
    d = out_dir(ep)
    (d / "raw").mkdir(parents=True, exist_ok=True)
    say_now = {it["id"]: it["say"] for it in spoken(mod)}[seg_id]
    shutil.copy(raw_wav, d / "raw" / f"{seg_id}.wav")
    trim(d / "raw" / f"{seg_id}.wav")
    cache_file = d / "cache.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    cache[seg_id] = seg_key(cfg, say_now, tone(mod, seg_id))
    cache_file.write_text(json.dumps(cache, indent=1), encoding="utf-8")


def step_pick(ep, seg_id, take):
    """Use one of the recorded readings for this sentence."""
    mod = load_script(ep)
    d = out_dir(ep)
    say_now = {it["id"]: it["say"] for it in spoken(mod)}[seg_id]
    said = json.loads((d / "takes" / f"{seg_id}_text.json").read_text(encoding="utf-8"))["say"]
    if said != say_now:
        raise SystemExit(f"the take says \"{said}\" but script.py says \"{say_now}\": "
                         "change the script to the new wording first")
    use_recording(ep, seg_id, d / "takes" / f"{seg_id}_take{take}_raw.wav")
    step_tts(ep, scene=seg_id[0])
    print(f"{ep} {seg_id}: now uses take {take}")


def step_render(ep, low):
    d = out_dir(ep)
    q = ["-ql"] if low else ["-r", "1920,1080", "--fps", "30"]
    name = "low.mp4" if low else "silent.mp4"
    cmd = [sys.executable, "-m", "manim", "render", *q, "--media_dir", str(d / "media"),
           "-o", name, "--disable_caching", str(ep_dir(ep) / "scene.py"), "Main"]
    r = subprocess.run(cmd, cwd=ep_dir(ep), capture_output=low, text=True)
    if r.returncode:
        if low:
            print((r.stdout or "")[-3000:], (r.stderr or "")[-6000:])
        raise SystemExit("manim render failed")
    shutil.copy(d / "marks.json", d / ("marks_low.json" if low else "marks_hd.json"))


def find_render(ep, low=False):
    hits = sorted((out_dir(ep) / "media").rglob("low.mp4" if low else "silent.mp4"),
                  key=lambda p: p.stat().st_mtime)
    if not hits:
        raise SystemExit("no rendered video found; run the render step first")
    return hits[-1]


def wrap_cues(text):
    """Split one narration segment into subtitle cues of at most 2 lines x 42 characters.

    The lines are balanced: the narrowest width that still fits the text into the same
    number of cues is used, so no cue ends with a single orphan word.
    """
    text = " ".join(text.split())
    n_cues = -(-len(textwrap.wrap(text, MAX_CHARS)) // MAX_LINES)
    lines = textwrap.wrap(text, MAX_CHARS)
    for width in range(12, MAX_CHARS + 1):
        trial = textwrap.wrap(text, width)
        if len(trial) <= n_cues * MAX_LINES and max(len(x) for x in trial) <= MAX_CHARS:
            lines = trial
            break
    return [lines[k:k + MAX_LINES] for k in range(0, len(lines), MAX_LINES)]


def ts(t, sep=","):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}"


def load_marks(ep, low=False):
    return json.loads((out_dir(ep) / ("marks_low.json" if low else "marks_hd.json")).read_text(encoding="utf-8"))


LEVEL_DB = -20.0      # every line is brought to this loudness (RMS of its voiced part, dB full scale)


def polish(x, rate, level_db=LEVEL_DB):
    """Even out one recorded line before it goes into the track: bring its voiced part to the
    common loudness (at most 6 dB either way) and fade both ends, so a recording that starts
    or stops in the middle of a sound does not click. Costs nothing; the recording is untouched."""
    n = rate // 20
    frames = np.array([np.sqrt(np.mean(x[k:k + n] ** 2)) for k in range(0, max(len(x) - n, 1), n)])
    voiced = frames[frames > 32768 * 10 ** (-45 / 20)]
    if len(voiced):
        now = 20 * np.log10(np.sqrt(np.mean(voiced ** 2)) / 32768)
        x = x * 10 ** (float(np.clip(level_db - now, -6, 6)) / 20)
    a, b = min(int(0.012 * rate), len(x) // 2), min(int(0.045 * rate), len(x) // 2)
    x[:a] *= np.linspace(0, 1, a, dtype=np.float32)
    x[len(x) - b:] *= np.linspace(1, 0, b, dtype=np.float32)
    return x


def step_mux(ep, low=False, even=True):
    """Audio track + subtitles + video. With low=True this makes the 480p draft used for previews;
    a draft may cover only the scenes written so far."""
    mod = load_script(ep)
    d = out_dir(ep)
    marks = load_marks(ep, low)
    subs = {i: sub for i, sub, _ in mod.SEGS}
    missing = [i for i in subs if i not in {m["id"] for m in marks["marks"]}]
    if missing and not low:
        raise SystemExit(f"segments never used in the scene: {missing}")
    # ---- audio track
    rate = 44100
    track = np.zeros(int((marks["total"] + 0.5) * rate), dtype=np.float32)
    silent = []
    for m in marks["marks"]:
        f = d / "wav" / f"{m['id']}.wav"
        if not f.exists():
            silent.append(m["id"])
            continue
        with wave.open(str(f)) as w:
            assert w.getframerate() == rate and w.getnchannels() == 1 and w.getsampwidth() == 2
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
        if even:
            x = polish(x.copy(), rate)
        a = int(m["start"] * rate)
        track[a:a + len(x)] += x[:len(track) - a]
    if silent:
        if not low:
            raise SystemExit(f"no recording for {silent}; run the tts step first")
        print(f"draft: no recording yet for {silent}")
    track = np.clip(track, -32767, 32767).astype(np.int16)
    audio = d / ("narration_low.wav" if low else "narration.wav")
    with wave.open(str(audio), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(track.tobytes())
    # ---- subtitles
    srt, n = [], 0
    for m in marks["marks"]:
        cues = wrap_cues(subs[m["id"]])
        sizes = [sum(len(x) for x in c) for c in cues]
        t = m["start"]
        for c, size in zip(cues, sizes):
            dur = m["dur"] * size / sum(sizes)
            for line in c:
                assert len(line) <= MAX_CHARS, line
            n += 1
            srt.append(f"{n}\n{ts(t)} --> {ts(t + dur)}\n" + "\n".join(c) + "\n")
            t += dur
    srt_name = "draft.srt" if low else "subtitles.srt"
    (d / srt_name).write_text("\n".join(srt), encoding="utf-8")
    if not low:  # narration script with timestamps, kept beside the script
        rows = [f"# {mod.TITLE} — narration script with timestamps", "",
                "Times are positions in the final video (mm:ss.s). "
                "Generated by `build.py` from the render; do not edit by hand.", "",
                "| Start | End | Id | Narration |", "|---|---|---|---|"]
        for m in marks["marks"]:
            a, b = m["start"], m["start"] + m["dur"]
            rows.append(f"| {int(a // 60):02d}:{a % 60:04.1f} | {int(b // 60):02d}:{b % 60:04.1f} "
                        f"| {m['id']} | {subs[m['id']]} |")
        words = sum(len(s.split()) for s in subs.values())
        rows += ["", f"Total length {marks['total'] / 60:.1f} min, {words} words of narration, "
                     f"{words / sum(m['dur'] for m in marks['marks']) * 60:.0f} words per minute while speaking."]
        (ep_dir(ep) / "narration.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
        shutil.copy(d / srt_name, ep_dir(ep) / "subtitles.srt")
    # ---- video with burned-in subtitles (ffmpeg runs inside the output folder so the
    #      subtitle filter gets a plain relative file name)
    style = ("FontName=Segoe UI,FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H30202020,"
             "BorderStyle=3,Outline=1,Shadow=0,MarginV=7")
    (d / "preview").mkdir(parents=True, exist_ok=True)
    final = d / "preview" / "draft.mp4" if low else d / f"{mod.OUTFILE}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(find_render(ep, low)), "-i", str(audio),
           "-vf", f"subtitles={srt_name}:force_style='{style}'",
           "-c:v", "libx264", "-preset", "veryfast" if low else "medium", "-crf", "23" if low else "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", str(final)]
    subprocess.run(cmd, check=True, cwd=d)
    print(f"wrote {final}  ({marks['total'] / 60:.1f} min)")
    return final


def scene_ranges(ep, low=False):
    """Start and end time of every scene; a scene is the group of narration ids sharing a letter."""
    marks = load_marks(ep, low)
    first = {}
    for m in marks["marks"]:
        first.setdefault(m["id"][0], m["start"])
    keys = list(first)
    return {k: (first[k], first[keys[n + 1]] if n + 1 < len(keys) else marks["total"])
            for n, k in enumerate(keys)}


def step_preview(ep, scene):
    """Quick 480p draft of everything written so far, then cut out one scene (or keep all of it)."""
    step_render(ep, low=True)
    draft = step_mux(ep, low=True)
    if not scene:
        return draft
    a, b = scene_ranges(ep, low=True)[scene]
    clip = out_dir(ep) / "preview" / f"scene_{scene}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(a - 0.3, 0):.2f}", "-to", f"{b:.2f}",
                    "-i", str(draft), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                    "-c:a", "aac", str(clip)], check=True)
    print(f"wrote {clip}  (scene {scene}: {a:.0f}-{b:.0f} s of the draft)")
    return clip


def step_review(ep):
    """Review page: the final video beside the sentence list, with a note box per sentence."""
    mod = load_script(ep)
    marks = load_marks(ep)
    subs = {i: sub for i, sub, _ in mod.SEGS}
    data = {"ep": ep, "title": mod.TITLE, "video": f"{mod.OUTFILE}.mp4", "total": marks["total"],
            "scenes": getattr(mod, "SCENES", {}),
            "segs": [{"id": m["id"], "start": m["start"], "dur": m["dur"], "text": subs[m["id"]]}
                     for m in marks["marks"]]}
    html = (HERE / "review_template.html").read_text(encoding="utf-8")
    html = html.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
    page = out_dir(ep) / f"{mod.OUTFILE}_review.html"
    page.write_text(html, encoding="utf-8")
    print(f"wrote {page}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", help="section number, for example 1.1")
    ap.add_argument("step", choices=["tts", "render", "mux", "all", "preview", "takes", "pick", "review"])
    ap.add_argument("--low", action="store_true", help="render: quick 480p15 draft")
    ap.add_argument("--force", action="store_true", help="tts: voice every sentence again")
    ap.add_argument("--grouped", action="store_true",
                    help="tts: voice the script's GROUPS, one request per group of sentences")
    ap.add_argument("--scene", help="tts/preview: scene letter, for example d (omit for everything)")
    ap.add_argument("--id", help="takes/pick: narration id, for example c9")
    ap.add_argument("--n", type=int, default=3, help="takes: how many readings")
    ap.add_argument("--text", help="takes: try this wording instead of the script's")
    ap.add_argument("--take", type=int, help="pick: which reading to use")
    a = ap.parse_args()
    if not (ep_dir(a.ep) / "script.py").exists():
        raise SystemExit(f"no script at {ep_dir(a.ep) / 'script.py'}")
    if a.step == "tts" and a.grouped:
        step_tts_groups(a.ep, a.scene, a.force)
    elif a.step in ("tts", "all"):
        step_tts(a.ep, a.force, a.scene)
    if a.step in ("render", "all"):
        step_render(a.ep, a.low)
    if a.step in ("mux", "all"):
        step_mux(a.ep)
        step_review(a.ep)
    if a.step == "preview":
        step_preview(a.ep, a.scene)
    if a.step == "takes":
        step_takes(a.ep, a.id, a.n, a.text)
    if a.step == "pick":
        step_pick(a.ep, a.id, a.take)
    if a.step == "review":
        step_review(a.ep)
