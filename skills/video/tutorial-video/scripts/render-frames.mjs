// Stitches the tutorial: screencast frames (each shown for its real duration, 30 fps), the
// voice-over placed at each scene's start, a quiet generated pad ducked under the voice
// (sidechain), loudness normalised to -16 LUFS. Writes out/<lang>/$TUTORIAL_NAME-<lang>.mp4.
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] ?? "de";
// The tutorial folder (out/<lang>/timeline.json, frames, vo.json): second argument, default cwd.
const base = resolve(process.argv[3] ?? process.cwd());
const out = join(base, "out", lang);
const timeline = JSON.parse(readFileSync(join(out, "timeline.json"), "utf8"));
const vo = JSON.parse(readFileSync(join(out, "vo.json"), "utf8"));
const music = process.env.MUSIC !== "0";
// TUTORIAL_CROP=w:h:x:y trims frame edges first (a headed browser leaves a white strip right/bottom).

// The sync flash: the video starts with the first frame after the magenta ones.
const isMagenta = (file) => {
	const rgb = execFileSync("ffmpeg", ["-loglevel", "error", "-i", file, "-vf", "crop=4:4:958:538,scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]);
	return rgb[0] > 200 && rgb[1] < 60 && rgb[2] > 200;
};
let first = 0;
let seen = false;
for (let i = 0; i < Math.min(60, timeline.frames.length); i++) {
	const magenta = isMagenta(timeline.frames[i].file);
	if (magenta) seen = true;
	else if (seen) {
		first = i;
		break;
	}
}
if (!seen) throw new Error("sync flash not found");
const frames = timeline.frames.slice(first);
const t0 = frames[0].t;

const lines = ["ffconcat version 1.0"];
frames.forEach((f, i) => {
	const next = frames[i + 1]?.t ?? timeline.end;
	lines.push(`file '${f.file}'`, `duration ${Math.max(0.001, next - f.t).toFixed(4)}`);
});
lines.push(`file '${frames.at(-1).file}'`);
const list = join(out, "frames.ffconcat");
writeFileSync(list, lines.join("\n"));
const total = timeline.end - t0;

const inputs = ["-f", "concat", "-safe", "0", "-i", list];
const filters = [];
const voLabels = [];
timeline.scenes.forEach((scene, i) => {
	inputs.push("-i", vo.scenes[scene.id].file);
	const delay = Math.max(0, Math.round((scene.voStart - t0) * 1000));
	filters.push(`[${i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${delay}|${delay}[v${i}]`);
	voLabels.push(`[v${i}]`);
});
filters.push(`${voLabels.join("")}amix=inputs=${voLabels.length}:normalize=0,apad=whole_dur=${total.toFixed(2)}[vo]`);
if (music) {
	// A slow, breathing pad (Am–F–C–G, 4 s each) with an echo; quiet, then ducked under speech.
	const chord = (n) => `if(eq(mod(floor(t/4),4),0),${n[0]},if(eq(mod(floor(t/4),4),1),${n[1]},if(eq(mod(floor(t/4),4),2),${n[2]},${n[3]})))`;
	const root = chord([220, 174.61, 196, 196]);
	const third = chord([261.63, 220, 246.94, 246.94]);
	const fifth = chord([329.63, 261.63, 293.66, 293.66]);
	const env = "pow(sin(PI*mod(t,4)/4),0.6)";
	const expr = `${env}*(0.5*sin(2*PI*${root}*t)+0.35*sin(2*PI*${third}*t)+0.3*sin(2*PI*${fifth}*t)+0.15*sin(2*PI*${root}/2*t))`;
	filters.push(
		`aevalsrc='${expr}':s=48000:d=${total.toFixed(2)},aformat=channel_layouts=stereo,lowpass=f=900,aecho=0.8:0.7:120|240:0.35|0.2,volume=0.06,afade=t=in:d=2,afade=t=out:st=${(total - 3).toFixed(2)}:d=3[bed]`,
		"[vo]asplit=2[vo1][vo2]",
		"[bed][vo2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=1500[ducked]",
		"[vo1][ducked]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[aout]",
	);
} else {
	filters.push("[vo]loudnorm=I=-16:TP=-1.5:LRA=11[aout]");
}

const name = process.env.TUTORIAL_NAME ?? "tutorial";
const file = join(out, `${name}-${lang}.mp4`);
execFileSync(
	"ffmpeg",
	[
		"-y", "-loglevel", "error", ...inputs,
		"-filter_complex", filters.join(";"),
		"-map", "0:v", "-map", "[aout]",
		"-vf", `${process.env.TUTORIAL_CROP ? `crop=${process.env.TUTORIAL_CROP},` : ""}scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p`,
		"-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "stillimage",
		"-c:a", "aac", "-b:a", "160k", "-ar", "48000",
		"-movflags", "+faststart", "-t", total.toFixed(2), file,
	],
	{ stdio: "inherit" },
);
console.log(`${file} (${total.toFixed(1)} s)`);
