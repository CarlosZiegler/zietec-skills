# Finds a label on a simulator screenshot by template matching, for taps by coordinates when the
# accessibility tree cannot be read. The template is a crop of an earlier full-resolution
# screenshot (the label and a little around it); x is the template's left edge in that screenshot.
# Searches the column at x top to bottom (downscaled 3x) and prints
#   "<y of the template centre as a fraction of the screen height> <mean abs difference>"
# A difference under ~30 means found; compare against the value on a screen where it is known.
# Usage: python3 find-label.py <screenshot.png> <template.png> <x_raw>
import sys
from PIL import Image, ImageChops, ImageStat

im = Image.open(sys.argv[1]).convert("L")
tp = Image.open(sys.argv[2]).convert("L")
x = int(sys.argv[3])
s = 3
ims = im.resize((im.width // s, im.height // s))
tps = tp.resize((tp.width // s, tp.height // s))
xs = x // s
best = (1e9, 0)
for y in range(0, ims.height - tps.height):
    d = ImageStat.Stat(ImageChops.difference(ims.crop((xs, y, xs + tps.width, y + tps.height)), tps)).mean[0]
    if d < best[0]:
        best = (d, y)
print(f"{(best[1] * s + tp.height / 2) / im.height:.4f} {best[0]:.2f}")
