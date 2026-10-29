# Contact sheet of a rendered tutorial: 6-8 frames, looked at before a take counts.
# With a timeline (out/<lang>/timeline.json) one frame per scene at a fraction of the scene
# (default 0.7), thinned evenly to --frames; without one, --frames frames spread over the video.
# For mode C (phone on the stage) it also writes <out>-phone.png with the phone screens larger.
# Usage: python3 contact-sheet.py <video.mp4> <out.png> [--timeline timeline.json] [--frames 8]
#        [--at 0.7] [--extra 12.5,30] [--phone]
import argparse, json, os, subprocess, tempfile
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("out")
ap.add_argument("--timeline")
ap.add_argument("--frames", type=int, default=8)
ap.add_argument("--at", type=float, default=0.7)
ap.add_argument("--extra", default="")
ap.add_argument("--phone", action="store_true", help="also crop the phone screen (stage-phone.html layout)")
a = ap.parse_args()

PHONE = (1208, 70, 1640, 1009)  # the screen on templates/stage-phone.html (render-phone SCREEN)

def duration(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], text=True))

times = []
if a.timeline:
    sc = json.load(open(a.timeline))["scenes"]
    t0 = sc[0]["start"]
    for i, s in enumerate(sc):
        lo = s["start"] - t0
        hi = (sc[i + 1]["start"] if i + 1 < len(sc) else s["end"]) - t0
        times.append((s["id"], lo + (hi - lo) * a.at))
    if len(times) > a.frames:
        step = (len(times) - 1) / (a.frames - 1)
        times = [times[round(i * step)] for i in range(a.frames)]
else:
    d = duration(a.video)
    times = [(f"#{i + 1}", d * (i + 0.5) / a.frames) for i in range(a.frames)]
times += [(f"t={float(t):.1f}", float(t)) for t in a.extra.split(",") if t]
times.sort(key=lambda x: x[1])

tmp = tempfile.mkdtemp()
thumbs, phones = [], []
for i, (label, t) in enumerate(times):
    p = os.path.join(tmp, f"{i}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", a.video, "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB")
    tag = f"{label} {t:.1f}s"
    if a.phone:
        ph = im.crop(PHONE).resize((300, 652))
        d = ImageDraw.Draw(ph)
        d.rectangle([0, 0, 170, 18], fill=(0, 0, 0))
        d.text((4, 3), tag, fill=(255, 255, 255))
        phones.append(ph)
    im.thumbnail((640, 360))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 200, 22], fill=(0, 0, 0))
    d.text((6, 5), tag, fill=(255, 255, 255))
    thumbs.append(im)

def sheet(images, cols, w, h, path):
    rows = (len(images) + cols - 1) // cols
    s = Image.new("RGB", (cols * w, rows * h), (255, 255, 255))
    for i, im in enumerate(images):
        s.paste(im, ((i % cols) * w, (i // cols) * h))
    s.save(path)

sheet(thumbs, 2, 640, 360, a.out)
if phones:
    sheet(phones, 4, 300, 652, os.path.splitext(a.out)[0] + "-phone.png")
print(a.out, len(thumbs), "frames")
