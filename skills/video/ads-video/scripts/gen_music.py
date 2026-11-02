#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["transformers", "torch", "soundfile", "numpy"]
# ///
"""Generate music beds for the ads.

usage:
  uv run gen_music.py OUT_DIR [--mood bright calm drive] [--seconds 30] [--provider auto|musicgen|lyria]
  uv run gen_music.py OUT_DIR --prompt "..." --name mybed

Providers:
  lyria     Google Lyria via `npx hyperframes bgm --provider lyria` (needs GEMINI_API_KEY or GOOGLE_API_KEY);
            better quality, 48 kHz stereo.
  musicgen  facebook/musicgen-small locally (~300 MB download on first run, 32 kHz mono, ~50 tokens per second).
  auto      lyria when a key is set and npx exists, else musicgen.

Generate each bed a few seconds longer than the longest ad; build.py trims, fades and offsets it
(`music_offset` skips a weak intro).
"""
import argparse, os, shutil, subprocess, sys

MOODS = {
    "bright": "modern upbeat corporate tech music, light plucky synths, soft claps, warm bass, positive and confident, 112 bpm, clean mix, no vocals",
    "calm": "calm modern minimal electronic, soft piano and warm pads, gentle beat, trustworthy and calm, 96 bpm, no vocals",
    "drive": "energetic modern pop electronic, punchy drums, bright synth arps, motivating product launch, 120 bpm, no vocals",
}


def lyria(prompt, seconds, out):
    subprocess.run(["npx", "--yes", "hyperframes", "bgm", "--provider", "lyria", "--duration", str(seconds),
                    "--prompt", prompt, "--negative-prompt", "vocals", "-o", out], check=True)


def musicgen(jobs, seconds):
    import soundfile as sf, torch
    from transformers import AutoProcessor, MusicgenForConditionalGeneration
    proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    dev = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    try:
        model = model.to(dev)
    except Exception:
        dev = "cpu"
    sr = model.config.audio_encoder.sampling_rate
    for prompt, out in jobs:
        inputs = proc(text=[prompt], padding=True, return_tensors="pt").to(dev)
        with torch.no_grad():
            audio = model.generate(**inputs, max_new_tokens=int(seconds * 50), do_sample=True, guidance_scale=3.0)
        a = audio[0, 0].cpu().numpy()
        sf.write(out, a, sr)
        print(os.path.basename(out), f"{len(a) / sr:.1f}s", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out")
    ap.add_argument("--mood", nargs="*", default=list(MOODS), choices=list(MOODS))
    ap.add_argument("--prompt"); ap.add_argument("--name", default="custom")
    ap.add_argument("--seconds", type=float, default=30)
    ap.add_argument("--provider", default="auto", choices=["auto", "musicgen", "lyria"])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    jobs = [(a.prompt, os.path.join(a.out, f"{a.name}.wav"))] if a.prompt else [(MOODS[m], os.path.join(a.out, f"{m}.wav")) for m in a.mood]
    prov = a.provider
    if prov == "auto":
        prov = "lyria" if (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")) and shutil.which("npx") else "musicgen"
    print("provider:", prov, flush=True)
    if prov == "lyria":
        for prompt, out in jobs:
            lyria(prompt, a.seconds, out)
    else:
        musicgen(jobs, a.seconds)


if __name__ == "__main__":
    sys.exit(main())
