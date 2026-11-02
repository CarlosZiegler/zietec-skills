#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pillow"]
# ///
"""Look at a recording or a finished ad without opening an editor.

usage:
  uv run review.py sheet VIDEO OUT.png [--start S] [--end E] [--step 0.5] [--cols 8] [--width 240]
      timestamped contact sheet: pick clip in/out points and tap times from a raw recording
  uv run review.py check VIDEO [OUT.png]
      size, length, codecs, loudness (target -16 LUFS / <= -1.5 dBTP) and a 12-frame sheet
"""
import argparse, json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw


def probe(path):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
                                     capture_output=True, text=True, check=True).stdout)


def frame(video, t, width):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        out = f.name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-vf", f"scale={width}:-2", out],
                   check=True)
    im = Image.open(out).convert("RGB"); os.remove(out)
    return im


def sheet(video, out, times, cols, width):
    ims = []
    for t in times:
        im = frame(video, t, width)
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 86, 24), fill=(0, 0, 0)); d.text((6, 5), f"{t:6.2f}s", fill=(255, 255, 255))
        ims.append(im)
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    c = Image.new("RGB", (cols * w + (cols + 1) * 6, rows * h + (rows + 1) * 6), (40, 40, 40))
    for i, im in enumerate(ims):
        c.paste(im, (6 + (i % cols) * (w + 6), 6 + (i // cols) * (h + 6)))
    c.save(out)
    print("sheet ->", out, f"({len(ims)} frames)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet"); s.add_argument("video"); s.add_argument("out")
    s.add_argument("--start", type=float, default=0); s.add_argument("--end", type=float)
    s.add_argument("--step", type=float, default=0.5); s.add_argument("--cols", type=int, default=8)
    s.add_argument("--width", type=int, default=240)
    c = sub.add_parser("check"); c.add_argument("video"); c.add_argument("out", nargs="?")
    a = ap.parse_args()
    dur = float(probe(a.video)["format"]["duration"])
    if a.cmd == "sheet":
        end = min(a.end or dur, dur - 0.05); times, t = [], a.start
        while t <= end:
            times.append(t); t += a.step
        sheet(a.video, a.out, times, a.cols, a.width)
        return
    info = probe(a.video)
    v = next(x for x in info["streams"] if x["codec_type"] == "video")
    au = [x for x in info["streams"] if x["codec_type"] == "audio"]
    print(f"{os.path.basename(a.video)}: {v['width']}x{v['height']} {v['codec_name']} {v['r_frame_rate']} fps, {dur:.2f}s, "
          f"{os.path.getsize(a.video) / 1e6:.1f} MB, audio: {au[0]['codec_name'] + ' ' + au[0]['sample_rate'] + ' Hz' if au else 'NONE'}")
    if au:
        err = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.video, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S).group(0))
        i, tp = float(m["input_i"]), float(m["input_tp"])
        print(f"loudness {i:.1f} LUFS ({'ok' if abs(i + 16) <= 1.5 else 'target -16'}), true peak {tp:.1f} dBTP "
              f"({'ok' if tp <= -1.0 else 'too hot'}), LRA {float(m['input_lra']):.1f} LU")
    out = a.out or os.path.splitext(a.video)[0] + "-sheet.png"
    sheet(a.video, out, [dur * (k + 0.5) / 12 for k in range(12)], 6, 270 if v["height"] > v["width"] else 360)


if __name__ == "__main__":
    sys.exit(main())
