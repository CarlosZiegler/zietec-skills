// Voice-over from clips made elsewhere (e.g. Higgsfield `text2speech_v2` with an ElevenLabs preset
// voice, or a studio recording): one file per scene, named <scene-id>.mp3 (or .wav/.m4a), in
// <clips-dir>. Trims the silence at both ends (keeps 120 ms at the end), converts to 48 kHz mono
// wav in out/<lang>/vo/ and writes out/<lang>/vo.json — the same format voice.mjs writes, so the
// recorders and renderers read it unchanged. Prints each clip's length and the projected video
// length (each scene holds its clip + 0.6 s, plus a short tail).
//   node vo-from-files.mjs <lang> <tutorial-dir> <clips-dir> [--engine label] [--target 45-55]
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const [lang = "de", dirArg = ".", clipsArg] = process.argv.slice(2).filter((a, i, all) => !a.startsWith("--") && !all[i - 1]?.startsWith("--"));
const flag = (name) => {
	const i = process.argv.indexOf(`--${name}`);
	return i > 0 ? process.argv[i + 1] : undefined;
};
if (!clipsArg) throw new Error("usage: vo-from-files.mjs <lang> <tutorial-dir> <clips-dir> [--engine label] [--target 45-55]");
const base = resolve(dirArg);
const clips = resolve(clipsArg);
const script = JSON.parse(readFileSync(join(base, `script.${lang}.json`), "utf8"));
const out = join(base, "out", lang, "vo");
mkdirSync(out, { recursive: true });

const HOLD = 0.6; // a scene holds its narration + 0.6 s (record-*.mjs)
const TAIL = 0.8;
const CLIP_MAX = 12; // 6–12 s per scene reads well; longer clips are flagged
const duration = (file) =>
	Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file], { encoding: "utf8" }).trim());

const result = { engine: flag("engine") ?? "files", scenes: {} };
let total = TAIL;
for (const scene of script.scenes) {
	const src = ["mp3", "wav", "m4a"].map((ext) => join(clips, `${scene.id}.${ext}`)).find((f) => existsSync(f));
	if (!src) throw new Error(`no clip for scene "${scene.id}" in ${clips}`);
	const wav = join(out, `${scene.id}.wav`);
	execFileSync("ffmpeg", [
		"-y", "-loglevel", "error", "-i", src,
		"-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,apad=pad_dur=0.12,areverse",
		"-ar", "48000", "-ac", "1", wav,
	]);
	const d = duration(wav);
	total += d + HOLD;
	result.scenes[scene.id] = { file: wav, duration: d };
	const words = scene.vo.split(/\s+/).filter(Boolean).length;
	console.log(`${scene.id.padEnd(20)} ${d.toFixed(2).padStart(6)} s  raw ${duration(src).toFixed(2).padStart(6)} s  ${(words / d).toFixed(2)} words/s${d > CLIP_MAX ? `  > ${CLIP_MAX} s` : ""}`);
}
writeFileSync(join(base, "out", lang, "vo.json"), JSON.stringify(result, null, "\t"));
const target = flag("target")?.split("-").map(Number);
const verdict = target ? (total < target[0] ? "short" : total > target[1] ? "over" : "ok") : "";
console.log(`projected video ${total.toFixed(1)} s${target ? ` (target ${target[0]}–${target[1]} s: ${verdict})` : ""}`);
