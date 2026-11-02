# ad.config.json

Paths are relative to the config file. Everything except `ads` has a default (see `DEFAULT_BRAND`, `DEFAULT_MIX`, `layout_for` in `scripts/build.py`).

```jsonc
{
  "format": "9:16",                 // 9:16 | 4:5 | 1:1 | 16:9 | "WxH"; per ad: ads.<name>.format; CLI: --format
  "out_dir": "out", "work_dir": "work",
  "output": "{app}-ad-{ad}-{ratio}.mp4",
  "sfx_dir": null,                  // folder with impact/whoosh/click/pop/chime.wav; null = synthesize into work/sfx
  "draft_say_voice": null,          // macOS `say` voice for --draft-voice say (default by brand.lang: de Anna, en Samantha)

  "brand": {
    "app": "Acme", "lang": "de",    // lang goes into <html lang> and picks the draft voice
    "logo": "brand/logo-white.svg", // shown on primary-background cards (svg/png); omit for none
    "logo_on_light": null,          // optional dark logo for light-background cards
    "colors": {
      "primary": ["#3b4cca", "#4a5be0", "#2a379e"], // 160deg gradient: start, 45 %, end
      "accent_on_primary": "#d7dcff",               // <em> on primary backgrounds
      "accent_gradient": ["#3b4cca", "#7a5cff"],    // <em> on light backgrounds (gradient text)
      "light_base": "#f4f5fb",
      "light_glows": ["rgba(…)", "rgba(…)", "rgba(…)"], // three radial glows at 20/30 %, 85/55 %, 30/90 %
      "ink": "#14161f",                             // text on light backgrounds
      "chip_on_light": null                         // chip fill on light backgrounds (default primary[0])
    },
    "fonts": { "display": "Inter Tight", "body": "Schibsted Grotesk", "mono": "JetBrains Mono",
               "css_url": null }    // null = Google Fonts URL from the families; "" = local fonts only
  },

  "device": {
    "phone": { "mockup": null,      // optional PNG of a phone; its screen area is cut out
               "screen": [0.05088, 0.02209, 0.89824, 0.95581, 0.13725], // x, y, w, h (fractions of the mockup), corner radius (fraction of w)
               "aspect": 2.0372,    // phone height / width
               "frame": "#2a2a2e", "glass": "#0a0a0c", "highlight": "#5a5a60" },
    "duo":   { "screen_aspect": 0.7034, "frame": "#111113", "edge": "#3a3a3e" } // open foldable: inner screen h / w
  },

  "layout": {                       // per format, merged over the defaults
    "9:16": { "card_top": 640, "h1": 110, "p": 36, "pad": 90, "logo_top": 120, "logo_h": 70,
              "clip_text": { "left": 90, "top": 150, "width": 900, "size": 96 },   // top may be "center"
              "duo_text":  { "left": 90, "top": 150, "width": 900, "size": 96 },
              "phone": { "width": 720, "x": null, "y": 520 },                     // x null = centred
              "duo":   { "width": 960, "x": null, "y": 760 },                     // y null = automatic
              "chips_top": 1620 }                                                 // null = chips under the clip headline
  },

  "mix": {
    "crossfade": 0.4, "voice_lufs": -16, "music_lufs": -22, "music_gain": 1.4,
    "music_fade_in": 0.5, "music_fade_out": 1.8,
    "duck": { "threshold": 0.03, "ratio": 8, "attack": 15, "release": 400 },
    "loudnorm": { "I": -16, "TP": -1.5, "LRA": 11 },
    "vo_tail": 0.15, "vo_last_tail": 0.6,
    "sfx": {                         // set any of these to null to drop it
      "intro":      { "sound": "impact", "at": 0.0,  "gain": 0.9 },
      "transition": { "sound": "whoosh", "at": -0.3, "gain": 0.55 },  // relative to each scene start
      "tap":        { "phone": "click", "duo": "pop", "lead": -0.12, "gain": 0.7 },
      "outro":      { "sound": "chime",  "at": 0.15, "gain": 0.5 }    // relative to the last scene start
    }
  },

  "ads": {
    "<name>": {
      "music": "music/bright.wav", "music_offset": 0,   // seconds of the bed to skip
      "scenes": [ /* see below */ ]
    }
  }
}
```

## Scenes

Common: `bg` (`"primary"` | `"light"`), `eyebrow`, `title` (HTML: `<br>`, `<em>` for the accent line), `vo`, `sfx`.

```jsonc
{ "type": "card", "duration": 2.8,
  "text": "One line under the headline.",       // optional
  "chips": ["Two-factor", "Face ID"],           // optional pills
  "footer": "App · CTA line.",                  // optional, under the chips
  "logo": false,                                // optional: hide the logo
  "top": 560 }                                  // optional: headline block position

{ "type": "clip", "device": "phone",            // or "duo" (open foldable)
  "recording": "rec/day.mov", "start": 15.6, "end": 22.0,  // seconds in the recording = scene length
  "taps": [16.8],                               // recording seconds of taps -> click/pop
  "filter": "crop=iw:ih-120:0:120",            // optional ffmpeg filter on the recording first
  "size": 88,                                   // optional headline size
  "chips": ["A", "B"] }

"vo":  { "text": "Spoken line.", "file": "vo/02.mp3", "offset": 0.4, "span": 1 }
        // offset: seconds after the scene starts; span 2 lets the line run through the next scene too
"sfx": [ { "sound": "pop", "at": 2.0, "gain": 0.6 } ]   // extra cues, seconds after the scene starts
```

Scene length: cards = `duration`, clips = `end − start`. Scene *i* starts at the sum of the previous lengths minus one crossfade each. A voice line's window closes `vo_tail` before scene *i + span* starts (or `vo_last_tail` before the end).
