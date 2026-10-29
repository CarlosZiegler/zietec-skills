---
name: tutorial-video
description: Produce narrated product tutorial videos automatically — script, voice-over (ElevenLabs, OpenAI, Higgsfield or macOS say), a real recording driven by Playwright (web app, browser-extension popup) or the iOS simulator (mobile app), cursor/tap highlights, captions, ducked music, title and end cards, 1080p mp4. Use when the user wants a tutorial, demo, walkthrough, onboarding or sales video of an app, or wants to re-record one in another language.
---

# Tutorial videos

Script → voice per scene → recording that holds each scene exactly as long as its narration → ffmpeg. No manual editing. Proven on a web portal, a Chrome extension popup and an Expo app (debug and release builds).

## Ground rules (ask first, never assume)

- **Real actions only on a test account**, and only after the user says so. Recordings click for real (clock in, confirm, approve). Prefer a stage with mocks (mode B) when the account must stay untouched.
- **Every real action has an undo.** Before the first take, list each action the video performs and how it is undone (withdraw the request, delete the upload, remove the stamped period). Undo off camera after every take and verify it (screenshot or list). Rehearsals leave traces too — e.g. a time-tracking editor cannot save an empty day, so a rehearsal's entries cannot simply be removed. For irreversible flows plan rehearsal-free takes: rehearse up to the irreversible step (`FINAL=0`), then one final take.
- **Never show credentials or personal data.** The user signs in off camera (the driver waits for it). Blur e-mails (overlay does it). Names, avatars, company names, IDs: pixelate in post with fixed rectangles (pixelate, not blur), the same rectangles for stills and video. Dev logs may print inputs (passwords): never grep them into the conversation; redact log files.
- **Language = native voice**, not just translated text. ElevenLabs: pick a voice whose library language is the target language (a native speaker), not a premade English voice. OpenAI `gpt-4o-mini-tts` keeps an American accent unless the instruction says so. Working setup (German): voice `marin` + instruction "Sprache: Deutsch. Sprich wie eine deutsche Muttersprachlerin aus Deutschland, klares Hochdeutsch … kein amerikanischer Akzent … Speak German as a native speaker; no American accent." Let the user pick by ear (generate 4–6 voice samples of one sentence, publish them with audio players).
- **Takes**: a take counts only after its contact sheet (6–8 frames, `scripts/contact-sheet.py`) has been looked at. At most 3 takes per video; if the third fails, stop and report what breaks.

## Layout in the project

```
<app>/tutorial/
  script.<lang>.json   title, subtitle, endTitle, endSubtitle, brand {color, logo, logoOnDark}, voice, scenes [{id, chapter, vo}]
  record.mjs           project-specific: what each scene does (copy a template)
  stage.html           mode B/C only (copy a template)
  out/                 git-ignored: vo/, frames/, timeline.json, the mp4
```

Scripts live in this skill (`scripts/`), templates in `templates/` (starting points: replace selectors, labels and routes with the app's own). Run scripts from a folder whose `node_modules` has `playwright` (or set `PLAYWRIGHT_FROM`).

## Workflow

1. **Script** (`templates/script.example.json`): 6–10 scenes, one sentence or two each (≈6–12 s spoken). Scene ids drive the recorder's `ACTIONS`. Intro/outro are cards. Write the narration in the target language as a native would; captions show the same text.
2. **Voice**: `node <skill>/scripts/voice.mjs <lang> <tutorial-dir>` → `out/<lang>/vo/*.wav` + `vo.json` (durations). Engines: **ElevenLabs** (default when `script.voice.elevenlabs.voiceId` is set and `ELEVENLABS_API_KEY` is found), **OpenAI** (`OPENAI_API_KEY`), or `VOICE=say` for a free macOS draft; force one with `VOICE=elevenlabs|openai|say`. Keys come from env, the nearest `.env` upwards, or the keychain (`elevenlabs-api-key` / `openai-api-key`) and are never printed. Silence at both ends is trimmed. ElevenLabs defaults to `eleven_v4` with `language_code` and text normalisation on (dates like "14.10." are spoken right); v4 takes only stability/similarity_boost. With a v2/flash model each scene also gets its neighbours (`previous_text`/`next_text`). The installed `text-to-speech` skill (elevenlabs/skills) documents the API, models and settings.
   - **Picking an ElevenLabs voice**: `node <skill>/scripts/voice-samples.mjs <out-dir> de "<one sentence>"` downloads the free previews of native German voices from the shared library and speaks the sentence with the account's own voices (credits). Publish the mp3s as a page with `<audio>` players; the user picks. A shared voice must be added to the account (`POST /v1/voices/add/{public_owner_id}/{voice_id}`) before TTS can use it — ask before adding. Model `eleven_v4` (default, best); `eleven_flash_v2_5` is cheaper; `eleven_multilingual_v2` refuses `language_code`.
   - **Higgsfield** (claude.ai Higgsfield connector, MCP) — useful when the own ElevenLabs account is on the Free plan. `list_voices` → pick an ElevenLabs preset voice (e.g. the German preset "Petra"); `generate_audio_batch` with `model: "text2speech_v2"`, `variant: "elevenlabs"`, `voice_type: "preset"`, `voice_id`, `prompt` = the scene's `vo`; `jobs_wait`. Generate all clips of all videos in one session so the voice stays the same; at most 8 in parallel per batch, retry 429s in the next batch; about 0.31 credits per clip (Oct 2026). Download each mp3 as `<clips>/<scene-id>.mp3`, then `node <skill>/scripts/vo-from-files.mjs <lang> <tutorial-dir> <clips> --engine higgsfield-elevenlabs --target 45-55` trims the silence, writes 48 kHz mono wavs and `vo.json` (the format the recorders and renderers read) and prints each clip's length (> 12 s flagged) and the projected video length. Job ids and voice ids stay out of the repo.
3. **Record** (pick the mode):
   - **A · Web app, signed in** — `scripts/driver.mjs <workdir> <sign-in URL> <signed-in path regex>` opens Chrome for Testing headed; the user signs in; then drop command modules into `<workdir>/cmd/` (recon → off-camera reset → `templates/record-web.mjs`, e.g. `export default async (a) => (await import("/abs/path/record-web.mjs")).default(a)`). Crop the headed browser's white right/bottom strip at render: `TUTORIAL_CROP=1896:1066:0:0`. The recorder injects `scripts/overlay.js` (cursor, ripple, ring, chapter, captions, cards; fill `__BRAND__`, `__LOGO__` with inline SVG markup, `__END_TITLE__`, `__END_SUBTITLE__`) and captures with CDP `Page.startScreencast`.
   - **B · Extension popup / UI with mocks** — `templates/stage-popup.html` (a browser frame, the real built popup in an iframe) + `templates/demo-mock.js` (chrome.* and the API answered in the page, a movable clock `__demo.setNow`) + `templates/record-stage.mjs`. Deterministic, touches no account.
   - **C · iOS app** — `templates/record-sim.mjs`: `simctl io recordVideo` + taps by accessibility label via argent (`describe` / `gesture-tap`), or by coordinates (`tapAt`). Then `scripts/render-phone.mjs` composes the phone into `templates/stage-phone.html` with chapter + captions beside it and a ring on every tap.
     - **One dedicated simulator per job**, its UDID in every call (`SIM_UDID`; never `booted` — other jobs may own a booted device). Install a release-type simulator build from the cloud (CI/EAS simulator build + `simctl install`): no Metro, no dev menu, the real app. Check `uptime` before each take — under heavy load frames drop and taps land late (the template warns when load > cores).
     - **No element tree?** A release build may expose none to argent until the app is relaunched, and a relaunch can sign the user out. Then tap by coordinates measured on a screenshot (`simctl io <udid> screenshot` + `sips -Z 900`; `tapAt(x, y)` in that size), find moving rows by template matching (`scripts/find-label.py`), and verify every step with a screenshot (the template saves one per scene to `out/<lang>/check/`).
     - **Pixelation**: list rectangles per screen in `SCREENS` (recording pixels), call `enter(screen)` when it changes; the windows land in `timeline.blur` and render-phone pixelates them. `noBlur` windows switch them off while a full-screen sheet covers them.
4. **Render**: A/B `TUTORIAL_NAME=x node <skill>/scripts/render-frames.mjs <lang> <dir>`; C `TUTORIAL_NAME=x node <skill>/scripts/render-phone.mjs <lang> <dir>` (re-encodes `sim.mp4` with `avconvert` first, pixelates `timeline.blur`). Output: H.264 1080p30, AAC, -16 LUFS, pad ducked 16–23 dB under the voice.
5. **Review** `python3 <skill>/scripts/contact-sheet.py out/<lang>/<name>.mp4 out/<lang>/contact.png --timeline out/<lang>/timeline.json [--phone]`, fix, re-take (undo the real actions off camera first), then publish (artifact with `<video>` players for the user; copy mp4 + poster where the product page needs it).

## Stills (help pages, docs)

Capture raw screenshots on the same simulator, then `python3 <skill>/scripts/pixelate-stills.py spec.json <out-dir>`: per image a crop and the pixelation rectangles (raw pixels), output scaled to 1080 px wide, plus `manifest.json` (crop, rectangles, size, sha256). Keep the spec with the sources so a re-capture reproduces the same crop and rectangles; reuse the video's rectangles for the same screen.

## Gotchas that cost hours

- **Frame size**: full Chrome's new headless crops the screencast to 993 px high — use the *headless shell* (`ms-playwright/chromium_headless_shell-*/…/chrome-headless-shell`) for B; headed Chrome for Testing with `deviceScaleFactor: 1.25` on a 1536×864 viewport gives ~1920×1080 for A (render crops/scales to exactly 1920×1080).
- **Sync**: A/B start with a magenta flash; render finds the first frame after it. C: `recordVideo` writes frames only on screen changes — the file starts at the spawn time (`recStart`) but **ends at the last change**, so never use `stop − duration`.
- **Waiting**: dev servers compile on first visit (5–15 s). Wait for real content (`locator.waitFor`), set `page.setDefaultTimeout(9000)` while recording so a missing element skips instead of freezing 30 s; highlights must never block (`boundingBox({timeout})` in try/catch).
- **Selectors**: sidebars often exist twice (desktop + hidden mobile sheet) → `a[href*="…"]:visible`. Disabled rows (locked weeks) → `:not([disabled])`. Groups may need expanding first. Do a read-only recon module (buttons, dialogs, checkbox states, screenshot) before scripting a scene.
- **Dialogs** in real apps often need extra input (a reason ≥3 chars, a "notices checked" box, times per day). Inspect them off camera; never tick a box you have not read (one take ticked "did not work this day").
- **State between takes**: every real take changes data. Write an off-camera `reset` (end the running shift, confirm, close dialogs) and run it until the start state is back. "Später"/"later" dismissals may not persist across navigation.
- **Overlay**: `addInitScript` accumulates per take — the overlay removes older roots and the newest wins. Logos as `<img>` (path or data:) can be blocked by the app's CSP → inline SVG markup. Hide dev-only UI (TanStack devtools button, Expo tools FAB).
- **Expo dev client FAB** (gear in every screenshot): `xcrun simctl spawn <udid> defaults write <bundle-id> EXDevMenuShowFloatingActionButton -bool NO`, relaunch. Use the installed app's real bundle id (`simctl listapps`).
- **Deep links** on a deep navigation stack lag or do nothing (modal open) → navigate in-app (back, tap rows); it also looks more natural.
- **Simulator recordings mis-timed by ffmpeg**: the H.264 from `simctl io recordVideo` is decoded with wrong timestamps after long still periods — pictures up to ~7 s out of place, a whole screen can vanish. Convert with macOS `avconvert` (`--preset PresetHighestQuality`, or `Preset1920x1080`) before ffmpeg touches it; render-phone does this. Any other ffmpeg step on a raw recording (joining two segments, extracting frames) must read the avconvert copy too.
- **Long off-camera waits** (a clock that must run a few minutes): stop the recorder, wait, start a second recording, shift the second segment's timeline back by the gap and join the two avconvert copies — the video shows no wait and no frozen screen.
- **Login detection** on the simulator: don't guess from pixels (it tapped during the user's password entry); wait for the app's first signed-in request in the Metro log.
- **ffmpeg 8** removed `-filter_complex_script` → `-/filter_complex <file>`. Odd widths break yuv420p → scale/crop to 1920×1080.
- **Lockfiles**: adding tooling to a pnpm workspace can re-resolve shared deps — check `git diff pnpm-lock.yaml | grep '^-[^-]'`.

## Other languages

Copy `script.de.json` → `script.<lang>.json`, translate as a native writer (not word order of the source), set the voice instruction for that language, run voice + render; re-record only when the UI language must change too.
