#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pillow"]
# ///
"""Build short app ads from a JSON config.

Title/claim cards are HTML rendered by headless Chrome, screen recordings sit in a
drawn phone (or an open foldable), and voice + music bed + SFX are mixed with ffmpeg.

usage:
  uv run build.py ad.config.json [AD ...]          build all ads, or the named ones
  uv run build.py ad.config.json --check           prep audio, print the voice timing table, render nothing
  uv run build.py ad.config.json --list-vo         print the voice lines as JSON (for a TTS batch)
  uv run build.py ad.config.json --draft-voice say missing voice clips are spoken by macOS `say`
                                                    (or `silent`) so the cut can be checked before real TTS

Needs ffmpeg/ffprobe and Chrome or Chromium (set CHROME=/path if it is not found).
Config schema: ../references/config.md
"""
import argparse, base64, copy, hashlib, json, mimetypes, os, re, shutil, subprocess, sys, time
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
FORMATS = {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)}
FPS = 30

DEFAULT_BRAND = {
    "app": "App",
    "lang": "en",
    "logo": None,           # white/light logo for primary-background cards (svg/png)
    "logo_on_light": None,  # optional dark logo for light-background cards
    "colors": {
        "primary": ["#3b4cca", "#4a5be0", "#2a379e"],   # 160deg gradient of the dark cards
        "accent_on_primary": "#d7dcff",                  # <em> colour on dark cards
        "accent_gradient": ["#3b4cca", "#7a5cff"],      # <em> gradient on light cards
        "light_base": "#f4f5fb",
        "light_glows": ["rgba(170,182,255,.85)", "rgba(186,226,255,.9)", "rgba(226,212,255,.9)"],
        "ink": "#14161f",                                # text on light cards
        "chip_on_light": None,                           # defaults to primary[0]
    },
    "fonts": {
        "display": "Inter Tight", "display_weights": "700;800",
        "body": "Schibsted Grotesk", "body_weights": "500;600",
        "mono": "JetBrains Mono", "mono_weights": "500",
        "css_url": None,  # override the Google Fonts URL (or "" for local fonts only)
    },
}

DEFAULT_MIX = {
    "crossfade": 0.4,
    "voice_lufs": -16, "music_lufs": -22, "music_gain": 1.4,
    "music_fade_in": 0.5, "music_fade_out": 1.8,
    "duck": {"threshold": 0.03, "ratio": 8, "attack": 15, "release": 400},
    "loudnorm": {"I": -16, "TP": -1.5, "LRA": 11},
    "vo_tail": 0.15,      # voice must end this long before its window closes
    "vo_last_tail": 0.6,  # ... and this long before the end of the video
    "sfx": {
        "intro": {"sound": "impact", "at": 0.0, "gain": 0.9},
        "transition": {"sound": "whoosh", "at": -0.3, "gain": 0.55},
        "tap": {"phone": "click", "duo": "pop", "lead": -0.12, "gain": 0.7},
        "outro": {"sound": "chime", "at": 0.15, "gain": 0.5},
    },
}


def merge(base, over):
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def layout_for(W, H):
    """Default positions per aspect family; every key can be overridden by config.layout."""
    if H >= 1.5 * W:  # 9:16 (the original style)
        return {"pad": 90, "logo_top": 120, "logo_h": 70, "card_top": round(H * .333), "h1": 110, "p": 36,
                "clip_text": {"left": 90, "top": 150, "width": W - 180, "size": 96},
                "duo_text": {"left": 90, "top": 150, "width": W - 180, "size": 96},
                "phone": {"width": 720, "x": (W - 720) // 2, "y": 520},
                "duo": {"width": 960, "x": None, "y": 760}, "chips_top": 1620}
    if W >= 1.5 * H:  # 16:9
        return {"pad": 140, "logo_top": 90, "logo_h": 64, "card_top": 300, "h1": 110, "p": 36,
                "clip_text": {"left": 140, "top": "center", "width": 860, "size": 96},
                "duo_text": {"left": 120, "top": "center", "width": 640, "size": 80},
                "phone": {"width": 540, "x": W - 140 - 540 - 80, "y": 110},
                "duo": {"width": 1000, "x": W - 100 - 1036, "y": None}, "chips_top": None}
    # 1:1 and 4:5
    return {"pad": 80, "logo_top": 80, "logo_h": 60, "card_top": round(H * .3), "h1": 96, "p": 32,
            "clip_text": {"left": 80, "top": 110, "width": 500, "size": 64},
            "duo_text": {"left": 80, "top": 80, "width": W - 160, "size": 72},
            "phone": {"width": 400, "x": W - 70 - 400, "y": 90},
            "duo": {"width": 760, "x": None, "y": None}, "chips_top": None}


def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(map(str, args[:6]))} ...\n{r.stderr[-2000:]}")
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def find_chrome():
    for c in (os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium", shutil.which("google-chrome"),
              shutil.which("google-chrome-stable"), shutil.which("chromium"), shutil.which("chromium-browser")):
        if c and os.path.exists(c):
            return c
    sys.exit("Chrome/Chromium not found: set CHROME=/path/to/chrome")


class Ad:
    def __init__(self, cfg_path, args):
        self.cfg_path = os.path.abspath(cfg_path)
        self.root = os.path.dirname(self.cfg_path)
        self.cfg = json.load(open(self.cfg_path))
        self.args = args
        self.brand = merge(DEFAULT_BRAND, self.cfg.get("brand"))
        self.mix = merge(DEFAULT_MIX, self.cfg.get("mix"))
        self.work = self.p(self.cfg.get("work_dir", "work"))
        self.out_dir = self.p(args.out or self.cfg.get("out_dir", "out"))
        for d in ("cards", "norm", "parts", "draft-vo"):
            os.makedirs(os.path.join(self.work, d), exist_ok=True)
        os.makedirs(self.out_dir, exist_ok=True)
        self.sfx_dir = self.p(self.cfg["sfx_dir"]) if self.cfg.get("sfx_dir") else self.ensure_sfx()
        self.chrome = None

    def p(self, rel):
        return rel if os.path.isabs(rel) else os.path.join(self.root, rel)

    def ensure_sfx(self):
        d = os.path.join(self.work, "sfx")
        if not os.path.exists(os.path.join(d, "chime.wav")):
            subprocess.run([sys.executable, os.path.join(HERE, "sfx.py"), d], check=True)
        return d

    # ---------- geometry ----------
    def setup_format(self, fmt):
        self.fmt = fmt
        self.W, self.H = FORMATS[fmt] if fmt in FORMATS else tuple(map(int, fmt.lower().split("x")))
        self.L = merge(layout_for(self.W, self.H), self.cfg.get("layout", {}).get(fmt, {}))
        dev = merge({"phone": {"mockup": None, "screen": [.05088, .02209, .89824, .95581, .13725],
                               "aspect": 2082 / 1022, "frame": "#2a2a2e", "glass": "#0a0a0c"},
                     "duo": {"screen_aspect": 2006 / 2852, "frame": "#111113", "edge": "#3a3a3e"}},
                    self.cfg.get("device"))
        ph = self.L["phone"]; PW = ph["width"]; PH = round(PW * dev["phone"]["aspect"])
        fx, fy, fw, fh, fr = dev["phone"]["screen"]
        self.phone = dict(PW=PW, PH=PH, PX=ph["x"] if ph["x"] is not None else (self.W - PW) // 2, PY=ph["y"],
                          sx=round(PW * fx), sy=round(PH * fy), sw=round(PW * fw) // 2 * 2, sh=round(PH * fh) // 2 * 2)
        self.phone["sr"] = round(self.phone["sw"] * fr)
        du = self.L["duo"]; DSW = du["width"] // 2 * 2; DSH = round(DSW * dev["duo"]["screen_aspect"]) // 2 * 2; pad = round(DSW * 18 / 960)
        DW, DH = DSW + 2 * pad, DSH + 2 * pad
        self.duo = dict(DSW=DSW, DSH=DSH, pad=pad, DW=DW, DH=DH,
                        DX=du["x"] if du["x"] is not None else (self.W - DW) // 2,
                        DY=du["y"] if du["y"] is not None else (self.H - DH) // 2 if self.W > self.H else self.H - DH - 60)
        self.bezel = self.draw_phone(dev["phone"])
        self.duo_frame = self.draw_duo(dev["duo"])

    def draw_phone(self, d):
        g = self.phone; PW, PH = g["PW"], g["PH"]
        out = os.path.join(self.work, f"bezel-{PW}.png")
        if d.get("mockup"):  # user-supplied mockup PNG: cut the screen out, draw the island back
            m = Image.open(self.p(d["mockup"])).convert("RGBA").resize((PW, PH), Image.LANCZOS)
        else:  # drawn: metal band, black glass, rounded screen hole (supersampled 3x)
            S = 3; r_o = (g["sr"] + g["sx"]) * S; band = max(2, round(PW * .012)) * S
            m = Image.new("RGBA", (PW * S, PH * S), (0, 0, 0, 0)); dr = ImageDraw.Draw(m)
            dr.rounded_rectangle((0, 0, PW * S - 1, PH * S - 1), radius=r_o, fill=d["frame"])
            dr.rounded_rectangle((band // 3, band // 3, PW * S - 1 - band // 3, PH * S - 1 - band // 3), radius=r_o - band // 3,
                                 outline=d.get("highlight", "#5a5a60"), width=max(1, S))
            dr.rounded_rectangle((band, band, PW * S - 1 - band, PH * S - 1 - band), radius=r_o - band, fill=d["glass"])
            m = m.resize((PW, PH), Image.LANCZOS)
        hole = Image.new("L", (PW * 3, PH * 3), 0)  # a hair smaller than the screen so no seam shows
        ImageDraw.Draw(hole).rounded_rectangle((g["sx"] * 3 + 2, g["sy"] * 3 + 2, (g["sx"] + g["sw"]) * 3 - 3, (g["sy"] + g["sh"]) * 3 - 3),
                                               radius=g["sr"] * 3, fill=255)
        hole = hole.resize((PW, PH), Image.LANCZOS)
        self.phone_mask = self.screen_mask(g["sw"], g["sh"], g["sr"])
        a = m.getchannel("A"); a.paste(0, mask=hole); m.putalpha(a)
        iw, ih = round(PW * .27), round(PH * .029)  # dynamic island over the recording
        ImageDraw.Draw(m).rounded_rectangle(((PW - iw) // 2, round(PH * .033), (PW + iw) // 2, round(PH * .033) + ih),
                                            radius=ih // 2, fill=(5, 5, 5, 255))
        m.save(out)
        return out

    def screen_mask(self, w, h, r):
        """rounded alpha mask for the recording, so its corners never poke past the frame."""
        out = os.path.join(self.work, f"mask-{w}x{h}-{r}.png")
        m = Image.new("L", (w * 3, h * 3), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), radius=r * 3, fill=255)
        m.resize((w, h), Image.LANCZOS).save(out)
        return out

    def draw_duo(self, d):
        g = self.duo; DW, DH, pad, k = g["DW"], g["DH"], g["pad"], g["DSW"] / 960
        out = os.path.join(self.work, f"duo-{DW}.png")
        im = Image.new("RGBA", (DW, DH), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, DW - 1, DH - 1), radius=round(46 * k), fill=d["frame"],
                                             outline=d["edge"], width=max(2, round(3 * k)))
        hole = Image.new("L", (DW, DH), 0)
        ImageDraw.Draw(hole).rounded_rectangle((pad, pad, pad + g["DSW"] - 1, pad + g["DSH"] - 1), radius=round(30 * k), fill=255)
        self.duo_mask = self.screen_mask(g["DSW"], g["DSH"], round(30 * k))
        a = im.getchannel("A"); a.paste(0, mask=hole); im.putalpha(a)
        fold = Image.new("RGBA", (DW, DH), (0, 0, 0, 0)); fd = ImageDraw.Draw(fold); cx = DW // 2
        fd.rectangle((cx - 3, pad, cx - 1, pad + g["DSH"]), fill=(0, 0, 0, 30))      # hinge shadow
        fd.rectangle((cx, pad, cx + 1, pad + g["DSH"]), fill=(255, 255, 255, 80))    # hinge highlight
        fd.rectangle((cx + 2, pad, cx + 4, pad + g["DSH"]), fill=(0, 0, 0, 30))
        Image.alpha_composite(im, fold).save(out)
        return out

    # ---------- cards ----------
    def logo_tag(self, light):
        path = self.brand.get("logo_on_light") if light else self.brand.get("logo")
        if not path:
            return ""
        if not os.path.exists(self.p(path)):
            sys.exit(f"logo not found: {self.p(path)}")
        mime = mimetypes.guess_type(path)[0] or "image/png"
        data = base64.b64encode(open(self.p(path), "rb").read()).decode()
        return f'<img class="logo" alt="{self.brand["app"]}" src="data:{mime};base64,{data}">'

    def html(self, sc, kind):
        B, C, F, L, W, H = self.brand, self.brand["colors"], self.brand["fonts"], self.L, self.W, self.H
        light = sc.get("bg", "primary") == "light"
        p0 = C["primary"][0]
        rgb = tuple(int(p0[i:i + 2], 16) for i in (1, 3, 5))
        bg = (f"linear-gradient(160deg,{C['primary'][0]} 0%,{C['primary'][1]} 45%,{C['primary'][2]} 100%)" if not light else
              ",".join(f"radial-gradient({round(W * .48)}px {round(W * .39)}px at {x}, {c}, transparent 70%)"
                       for x, c in zip(("20% 30%", "85% 55%", "30% 90%"), C["light_glows"])) + f", {C['light_base']}")
        em = (f"background:linear-gradient(92deg,{C['accent_gradient'][0]},{C['accent_gradient'][1]});"
              "-webkit-background-clip:text;background-clip:text;color:transparent") if light else f"color:{C['accent_on_primary']}"
        fonts_url = F.get("css_url")
        if fonts_url is None:
            fam = lambda n, w: n.replace(" ", "+") + f":wght@{w}"
            fonts_url = (f"https://fonts.googleapis.com/css2?family={fam(F['display'], F['display_weights'])}"
                         f"&family={fam(F['body'], F['body_weights'])}&family={fam(F['mono'], F['mono_weights'])}&display=block")
        link = f'<link rel="stylesheet" href="{fonts_url}">' if fonts_url else ""
        chips_html = lambda items: "".join(f"<span>{c}</span>" for c in items)
        if kind == "card":
            top = sc.get("top", L["card_top"])
            inner = ("" if sc.get("logo") is False else self.logo_tag(light)) + f'<div class="t" style="top:{top}px">'
            inner += f'<div class="eb">{sc.get("eyebrow", "")}</div><h1>{sc["title"]}</h1>'
            inner += f'<p>{sc["text"]}</p>' if sc.get("text") else ""
            inner += f'<div class="chips">{chips_html(sc["chips"])}</div>' if sc.get("chips") else ""
            inner += f'<p style="margin-top:{80 if sc.get("chips") else 30}px">{sc["footer"]}</p>' if sc.get("footer") else ""
            inner += "</div>"
        else:
            t = L["duo_text" if sc.get("device") == "duo" else "clip_text"]
            pos = "top:50%;transform:translateY(-50%)" if t["top"] == "center" else f"top:{t['top']}px"
            inner = (f'<div class="t" style="left:{t["left"]}px;width:{t["width"]}px;right:auto;{pos}"><div class="eb">{sc.get("eyebrow", "")}</div>'
                     f'<h1 style="font-size:{sc.get("size", t["size"])}px">{sc["title"]}</h1>')
            if sc.get("chips") and L["chips_top"] is None:
                inner += f'<div class="chips{" dark" if light else ""}">{chips_html(sc["chips"])}</div>'
            inner += "</div>"
            if sc.get("chips") and L["chips_top"] is not None:
                inner += f'<div class="t" style="top:{L["chips_top"]}px"><div class="chips{" dark" if light else ""}">{chips_html(sc["chips"])}</div></div>'
        s = min(W, H) / 1080
        ring = f"rgba({rgb[0]},{rgb[1]},{rgb[2]},.14)" if light else "rgba(255,255,255,.18)"
        return f"""<!doctype html><html lang="{B['lang']}"><head><meta charset="utf-8">{link}
<style>*{{box-sizing:border-box}}html,body{{margin:0}}
.c{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg};font-family:"{F['display']}",sans-serif;color:{C['ink'] if light else '#fff'}}}
.ring{{position:absolute;border-radius:999px;border:4px solid {ring}}}
.logo{{position:absolute;left:{L['pad']}px;top:{L['logo_top']}px;height:{L['logo_h']}px}}
.eb{{font:500 {round(26 * s)}px/1 "{F['mono']}",monospace;letter-spacing:.14em;opacity:.75;margin-bottom:{round(24 * s)}px;text-transform:uppercase}}
h1{{margin:0;font-size:{L['h1']}px;line-height:.94;letter-spacing:-0.045em;font-weight:800}}
h1 em{{font-style:normal;{em}}}
.t{{position:absolute;left:{L['pad']}px;right:{L['pad']}px}}
p{{font:500 {L['p']}px/1.4 "{F['body']}",sans-serif;margin:{round(30 * s)}px 0 0;opacity:.92}}
.chips{{display:flex;gap:{round(16 * s)}px;flex-wrap:wrap;margin-top:{round(40 * s)}px}}
.chips span{{font:600 {round(30 * s)}px/1 "{F['body']}",sans-serif;padding:{round(20 * s)}px {round(26 * s)}px;border-radius:999px;background:#fff;color:#1a1718}}
.chips.dark span{{background:{C.get('chip_on_light') or p0};color:#fff}}
</style></head><body><div class="c">
<div class="ring" style="width:{round(900 * s)}px;height:{round(900 * s)}px;left:{round(-380 * s)}px;top:{round(H * .6)}px"></div>
<div class="ring" style="width:{round(620 * s)}px;height:{round(620 * s)}px;left:{round(W * .65)}px;top:{round(-260 * s)}px"></div>
{inner}</div></body></html>"""

    def render_card(self, page_html):
        key = hashlib.sha1(page_html.encode()).hexdigest()[:16]
        out = os.path.join(self.work, "cards", f"{key}-{self.W}x{self.H}.png")
        if os.path.exists(out):
            return out
        self.chrome = self.chrome or find_chrome()
        page = os.path.join(self.work, "cards", f"{key}.html")
        open(page, "w").write(page_html)
        for attempt in range(6):  # headless Chrome fails now and then under load: fresh profile, retry
            prof = os.path.join(self.work, f"chrome-{os.getpid()}-{attempt}")
            r = subprocess.run([self.chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--hide-scrollbars",
                                "--force-device-scale-factor=1", f"--window-size={self.W},{self.H}", "--virtual-time-budget=8000",
                                f"--screenshot={out}", f"file://{page}"], capture_output=True)
            shutil.rmtree(prof, ignore_errors=True)
            if r.returncode == 0 and os.path.exists(out):
                break
            print("chrome retry", attempt, r.stderr[-200:], flush=True); time.sleep(3)
        else:
            sys.exit("chrome failed to render a card")
        os.remove(page)
        return out

    # ---------- audio ----------
    def prep(self, src, kind):
        src = self.p(src)
        if not os.path.exists(src):
            sys.exit(f"missing audio: {src}")
        lufs = self.mix["voice_lufs"] if kind == "voice" else self.mix["music_lufs"]
        key = hashlib.sha1(f"{src}{os.path.getmtime(src)}{kind}{lufs}".encode()).hexdigest()[:16]
        out = os.path.join(self.work, "norm", f"{kind}-{key}.wav")
        if not os.path.exists(out):
            trim = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03"
            af = (f"{trim},areverse,{trim},areverse," if kind == "voice" else "") + f"loudnorm=I={lufs}:TP=-2:LRA=11"
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", "44100", "-ac", "2", out])
        return out

    def voice_file(self, ad, i, vo):
        f = vo.get("file")
        if f and os.path.exists(self.p(f)):
            return self.p(f)
        if not self.args.draft_voice:
            sys.exit(f"missing voice clip for {ad} scene {i}: {f} (generate it, or pass --draft-voice say|silent)")
        mode = self.args.draft_voice
        out = os.path.join(self.work, "draft-vo", f"{ad}-{i}-{mode}-{hashlib.sha1(vo['text'].encode()).hexdigest()[:8]}.wav")
        if not os.path.exists(out):
            if self.args.draft_voice == "say":
                voices = {"de": "Anna", "en": "Samantha", "pt": "Luciana", "fr": "Thomas", "es": "Monica"}
                v = self.cfg.get("draft_say_voice") or voices.get(self.brand["lang"][:2], "Samantha")
                aiff = out + ".aiff"
                run(["say", "-v", v, "-o", aiff, vo["text"]])
                run(["ffmpeg", "-v", "error", "-y", "-i", aiff, "-ar", "44100", "-ac", "2", out]); os.remove(aiff)
            else:  # silent placeholder, ~2.6 words per second (prep leaves it untouched)
                secs = max(0.8, len(vo["text"].split()) / 2.6)
                run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{secs:.2f}", out])
        return out

    # ---------- build ----------
    def enc(self, args, out):
        run(["ffmpeg", "-v", "error", "-y", *args, "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", out])

    def scene_part(self, name, i, sc):
        bg = self.render_card(self.html(sc, sc["type"]))
        out = os.path.join(self.work, "parts", f"{name}-{self.fmt.replace(':', 'x')}-{i}.mp4")
        if sc["type"] == "card":
            self.enc(["-loop", "1", "-t", str(sc["duration"]), "-i", bg, "-vf", f"fps={FPS}"], out)
            return out, float(sc["duration"])
        s, e = float(sc["start"]), float(sc["end"])
        pre = (sc["filter"] + ",") if sc.get("filter") else ""   # e.g. "crop=iw:ih-80:0:80" to drop a status bar
        if sc.get("device", "phone") == "duo":
            g = self.duo; w, h, x, y, ov, ox, oy = g["DSW"], g["DSH"], g["DX"] + g["pad"], g["DY"] + g["pad"], self.duo_frame, g["DX"], g["DY"]
            mask = self.duo_mask
        else:
            g = self.phone; w, h, x, y, ov, ox, oy = g["sw"], g["sh"], g["PX"] + g["sx"], g["PY"] + g["sy"], self.bezel, g["PX"], g["PY"]
            mask = self.phone_mask
        fc = (f"[1:v]{pre}fps={FPS},trim={s}:{e},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=3,"
              f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}:(iw-{w})/2:0,format=yuva420p[a0];"
              f"[3:v]format=gray[m];[a0][m]alphamerge[app];"
              f"[0:v][app]overlay={x}:{y}:shortest=1[t];[t][2:v]overlay={ox}:{oy}[v]")
        self.enc(["-loop", "1", "-i", bg, "-i", self.p(sc["recording"]), "-i", ov, "-loop", "1", "-i", mask,
                  "-filter_complex", fc, "-map", "[v]", "-t", f"{e - s:.3f}"], out)
        return out, round(e - s, 3)

    def timeline(self, scenes):
        XF = self.mix["crossfade"]
        durs = [float(sc["duration"]) if sc["type"] == "card" else round(float(sc["end"]) - float(sc["start"]), 3) for sc in scenes]
        starts = [0.0]
        for d in durs[:-1]:
            starts.append(starts[-1] + d - XF)
        return durs, starts, starts[-1] + durs[-1]

    def voice_cues(self, name, scenes, starts, total, report=True):
        cues, bad = [], []
        for i, sc in enumerate(scenes):
            vo = sc.get("vo")
            if not vo:
                continue
            src = self.voice_file(name, i, vo)
            f = src if "-silent-" in os.path.basename(src) else self.prep(src, "voice")
            t0 = starts[i] + float(vo.get("offset", 0.3)); d = duration(f)
            j = i + int(vo.get("span", 1))
            limit = starts[j] - self.mix["vo_tail"] if j < len(scenes) else total - self.mix["vo_last_tail"]
            over = t0 + d - limit
            cues.append((f, t0))
            if over > 0:
                bad.append(i)
            if report:
                print(f"  scene {i:<2} {sc['type']:<4} voice {t0:6.2f}-{t0 + d:6.2f}s  window ends {limit:6.2f}s  "
                      + ("OK" if over <= 0 else f"OVER by {over:.2f}s -> lengthen the scene or retake shorter (never atempo)"))
        return cues, bad

    def build(self, name, ad):
        self.setup_format(ad.get("format", self.cfg.get("format", "9:16")))
        scenes, M, S = ad["scenes"], self.mix, self.mix["sfx"]
        durs, starts, total = self.timeline(scenes)
        print(f"{name} [{self.fmt}] {total:.1f}s  scenes " + " ".join(f"{d:.1f}" for d in durs), flush=True)
        vo, bad = self.voice_cues(name, scenes, starts, total)
        if bad and not self.args.force:
            sys.exit(f"{name}: voice overruns its window in scene(s) {bad} (use --force to build anyway for a draft)")
        if self.args.check:
            return
        files = [self.scene_part(name, i, sc)[0] for i, sc in enumerate(scenes)]

        snd = lambda s: os.path.join(self.sfx_dir, f"{s}.wav")
        cues = []  # (wav, time, gain)
        if S.get("intro"):
            cues.append((snd(S["intro"]["sound"]), S["intro"]["at"], S["intro"]["gain"]))
        for i in range(1, len(scenes)):
            if S.get("transition"):
                cues.append((snd(S["transition"]["sound"]), starts[i] + S["transition"]["at"], S["transition"]["gain"]))
        for i, sc in enumerate(scenes):
            if sc["type"] == "clip" and S.get("tap"):
                for t in sc.get("taps", []):
                    cues.append((snd(S["tap"][sc.get("device", "phone")]), starts[i] + (t - float(sc["start"])) + S["tap"]["lead"], S["tap"]["gain"]))
            for c in sc.get("sfx", []):
                cues.append((snd(c["sound"]), starts[i] + c["at"], c.get("gain", 0.6)))
        if S.get("outro"):
            cues.append((snd(S["outro"]["sound"]), starts[-1] + S["outro"]["at"], S["outro"]["gain"]))

        XF = M["crossfade"]
        va = ["ffmpeg", "-v", "error", "-y"]
        for f in files:
            va += ["-i", f]
        chain, last, off = "", "[0:v]", 0.0
        for i in range(1, len(files)):
            off += durs[i - 1] - XF
            chain += f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}];"
            last = f"[x{i}]"
        n = len(files)
        va += ["-i", self.prep(ad["music"], "music"), "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
        va += ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]  # second silence for an empty SFX list
        for f, _ in vo:
            va += ["-i", f]
        for f, _, _ in cues:
            va += ["-i", f]
        fmt = "aformat=sample_rates=44100:channel_layouts=stereo"
        mo = float(ad.get("music_offset", 0.0))
        a = (f"[{n}:a]{fmt},atrim=start={mo}:duration={total:.3f},asetpts=PTS-STARTPTS,volume={M['music_gain']},"
             f"afade=t=in:d={M['music_fade_in']},afade=t=out:st={total - M['music_fade_out']:.3f}:d={M['music_fade_out']}[mus];")
        vl = [f"[{n + 1}:a]"]
        for j, (_, t) in enumerate(vo):
            a += f"[{n + 3 + j}:a]{fmt},adelay={int(t * 1000)}:all=1[v{j}];"; vl.append(f"[v{j}]")
        a += "".join(vl) + f"amix=inputs={len(vl)}:normalize=0:duration=longest,apad=whole_dur={total:.3f}[vo];[vo]asplit[vo1][vosc];"
        sl = [f"[{n + 2}:a]"] if not cues else []
        for j, (_, t, g) in enumerate(cues):
            a += f"[{n + 3 + len(vo) + j}:a]{fmt},volume={g},adelay={max(0, int(t * 1000))}:all=1[s{j}];"; sl.append(f"[s{j}]")
        a += "".join(sl) + f"amix=inputs={len(sl)}:normalize=0:duration=longest[sfx];"
        d = M["duck"]; ln = M["loudnorm"]
        a += f"[mus][vosc]sidechaincompress=threshold={d['threshold']}:ratio={d['ratio']}:attack={d['attack']}:release={d['release']}[bed];"
        a += f"[bed][vo1][sfx]amix=inputs=3:normalize=0:duration=first,loudnorm=I={ln['I']}:TP={ln['TP']}:LRA={ln['LRA']},aresample=44100[aout]"
        slug = re.sub(r"[^a-z0-9]+", "-", self.brand["app"].lower()).strip("-") or "app"
        out = os.path.join(self.out_dir, self.cfg.get("output", "{app}-ad-{ad}-{ratio}.mp4").format(
            app=slug, ad=name, ratio=self.fmt.replace(":", "x")))
        va += ["-filter_complex", chain + a, "-map", last, "-map", "[aout]", "-t", f"{total:.3f}",
               "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
               "-ar", "44100", "-movflags", "+faststart", out]
        run(va)
        print(f"  -> {out}", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config"); ap.add_argument("ads", nargs="*")
    ap.add_argument("--check", action="store_true", help="timing table only, no render")
    ap.add_argument("--list-vo", action="store_true", help="print voice lines as JSON")
    ap.add_argument("--draft-voice", choices=["say", "silent"], help="stand-in for missing voice clips")
    ap.add_argument("--format", help="override the format of every ad (9:16, 4:5, 1:1, 16:9 or WxH)")
    ap.add_argument("--force", action="store_true", help="build even if a voice line overruns its window")
    ap.add_argument("--out", help="output directory (default: config out_dir)")
    args = ap.parse_args()
    if args.list_vo:
        cfg = json.load(open(args.config))
        print(json.dumps([{"ad": k, "scene": i, "file": sc["vo"].get("file"), "text": sc["vo"]["text"]}
                          for k, ad in cfg["ads"].items() if not args.ads or k in args.ads
                          for i, sc in enumerate(ad["scenes"]) if sc.get("vo")], ensure_ascii=False, indent=1))
        return
    b = Ad(args.config, args)
    for k in args.ads or list(b.cfg["ads"]):
        ad = dict(b.cfg["ads"][k])
        if args.format:
            ad["format"] = args.format
        b.build(k, ad)


if __name__ == "__main__":
    main()
