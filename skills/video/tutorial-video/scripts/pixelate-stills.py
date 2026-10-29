# Screenshots for docs/help pages: pixelate fixed rectangles, crop, scale, and keep a manifest so a
# re-capture reproduces exactly the same crop and rectangles. Pixelate, never blur (blur can be
# reversed or read). Use the same rectangles as the video (timeline.blur) for the same screen.
#
# spec.json: [{"out": "home-1.png", "source": "raw/home.png",
#              "crop": [x, y, w, h],
#              "pixelate": [{"what": "own avatar", "x": 1030, "y": 186, "w": 136, "h": 136}]}]
# Coordinates in the raw screenshot's pixels (xcrun simctl io <udid> screenshot). Sources are
# relative to the spec file. Writes <out-dir>/<out> and <out-dir>/manifest.json (crop,
# rectangles, size, sha256 per image).
# Usage: python3 pixelate-stills.py <spec.json> <out-dir> [--width 1080] [--cell 24] [--max-kb 400]
import argparse, hashlib, json, os
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("out_dir")
ap.add_argument("--width", type=int, default=1080)
ap.add_argument("--cell", type=int, default=24, help="pixel block size in raw px")
ap.add_argument("--max-kb", type=int, default=400, help="quantize harder above this size")
a = ap.parse_args()

base = os.path.dirname(os.path.abspath(a.spec))
os.makedirs(a.out_dir, exist_ok=True)

def pixelate(im, x, y, w, h):
    region = im.crop((x, y, x + w, y + h))
    small = region.resize((max(1, w // a.cell), max(1, h // a.cell)), Image.BOX)
    im.paste(small.resize((w, h), Image.NEAREST), (x, y))

manifest = []
for e in json.load(open(a.spec)):
    im = Image.open(os.path.join(base, e["source"])).convert("RGB")
    raw_size = im.size
    for r in e.get("pixelate", []):
        pixelate(im, r["x"], r["y"], r["w"], r["h"])
    cx, cy, cw, ch = e.get("crop", [0, 0, im.width, im.height])
    im = im.crop((cx, cy, cx + cw, cy + ch))
    im = im.resize((a.width, round(ch * a.width / cw)), Image.LANCZOS)
    path = os.path.join(a.out_dir, e["out"])
    for colors in (256, 128):
        im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)
        if os.path.getsize(path) <= a.max_kb * 1024:
            break
    size = os.path.getsize(path)
    manifest.append({
        "file": e["out"], "source": e["source"], "source_size": list(raw_size),
        "crop": {"x": cx, "y": cy, "w": cw, "h": ch},
        "pixelate": e.get("pixelate", []),
        "output": {"width": im.width, "height": im.height, "bytes": size,
                   "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()},
    })
    print(f"{e['out']:40s} {im.width}x{im.height} {size / 1024:6.1f} KB  {len(e.get('pixelate', []))} rect(s)"
          + ("  OVER" if size > a.max_kb * 1024 else ""))
json.dump(manifest, open(os.path.join(a.out_dir, "manifest.json"), "w"), ensure_ascii=False, indent=1)
