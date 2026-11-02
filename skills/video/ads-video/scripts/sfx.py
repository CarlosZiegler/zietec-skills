#!/usr/bin/env python3
"""Synthesize the five ad sound effects (stdlib only, 44.1 kHz 16-bit stereo WAV).

usage: python3 sfx.py OUT_DIR [--seed N]

  impact  1.40 s  low sine sweep 70 -> 40 Hz + short thump, opens the ad
  whoosh  0.55 s  band-passed noise, filter sweeping up and down, hann envelope, on every scene change
  click   0.09 s  1.8 kHz tick + noise transient, on taps in a phone clip
  pop     0.22 s  sine dropping 600 -> 300 Hz, on taps in a foldable clip
  chime   1.60 s  C6 + G6 bell with a short stagger, on the end card

Peaks and envelopes match the set used for the original ads; build.py sets the gains.
"""
import argparse, math, os, random, struct, wave

SR = 44100


def write(path, x, peak):
    m = max(abs(v) for v in x) or 1.0
    x = [v / m * peak for v in x]
    fade = int(SR * 0.004)  # no clicks at the tail
    for i in range(min(fade, len(x))):
        x[-1 - i] *= i / fade
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<hh", int(v * 32767), int(v * 32767)) for v in x))


def sweep(f0, f1, dur, tau):
    """sine whose frequency glides exponentially f0 -> f1 over `tau` seconds."""
    out, ph = [], 0.0
    for i in range(int(SR * dur)):
        t = i / SR
        f = f1 + (f0 - f1) * math.exp(-t / tau)
        ph += 2 * math.pi * f / SR
        out.append(math.sin(ph))
    return out


def bandpass(x, centers, q):
    """RBJ band-pass biquad with a per-sample centre frequency."""
    y, x1, x2, y1, y2 = [], 0.0, 0.0, 0.0, 0.0
    for i, v in enumerate(x):
        w0 = 2 * math.pi * centers[i] / SR
        al = math.sin(w0) / (2 * q); a0 = 1 + al
        b0, b2, a1, a2 = al / a0, -al / a0, -2 * math.cos(w0) / a0, (1 - al) / a0
        o = b0 * v + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, v, y1, o
        y.append(o)
    return y


def impact(rng):
    n = int(SR * 1.4)
    body = sweep(70, 40, 1.4, 0.12)
    thump = [rng.uniform(-1, 1) for _ in range(n)]
    lp, a = [], 0.0
    for v in thump:  # one-pole low-pass ~ 300 Hz
        a += (v - a) * 0.04
        lp.append(a)
    return [body[i] * math.exp(-i / SR / 0.32) + 3.0 * lp[i] * math.exp(-i / SR / 0.025) for i in range(n)]


def whoosh(rng):
    n = int(SR * 0.55)
    noise = [rng.uniform(-1, 1) for _ in range(n)]
    centers = [2200 + 3800 * math.sin(math.pi * i / n) for i in range(n)]
    y = bandpass(noise, centers, 0.9)
    return [y[i] * math.sin(math.pi * i / n) ** 2 for i in range(n)]


def click(rng):
    n = int(SR * 0.09)
    return [(0.7 * math.sin(2 * math.pi * 1800 * i / SR) + 0.5 * rng.uniform(-1, 1) * math.exp(-i / SR / 0.003))
            * math.exp(-i / SR / 0.011) for i in range(n)]


def pop(_rng):
    s = sweep(600, 300, 0.22, 0.012)
    return [v * math.exp(-i / SR / 0.045) * min(1.0, i / (SR * 0.002)) for i, v in enumerate(s)]


def chime(_rng):
    n, d = int(SR * 1.6), int(SR * 0.08)
    out = []
    for i in range(n):
        t = i / SR
        v = math.sin(2 * math.pi * 1046.5 * t) * math.exp(-t / 0.55)
        v += 0.35 * math.sin(2 * math.pi * 2093 * t) * math.exp(-t / 0.2)  # bell overtone
        if i >= d:
            t2 = (i - d) / SR
            v += 0.8 * math.sin(2 * math.pi * 1568 * t2) * math.exp(-t2 / 0.6)
        out.append(v * min(1.0, i / (SR * 0.003)))
    return out


SOUNDS = {"impact": (impact, 0.63), "whoosh": (whoosh, 0.30), "click": (click, 0.35), "pop": (pop, 0.35), "chime": (chime, 0.22)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = random.Random(a.seed)
    for name, (fn, peak) in SOUNDS.items():
        write(os.path.join(a.out, f"{name}.wav"), fn(rng), peak)
    print("sfx ->", a.out, ", ".join(SOUNDS))
