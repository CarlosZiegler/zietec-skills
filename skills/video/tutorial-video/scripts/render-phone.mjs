// Composes the app tutorial: one stage image per scene (stage.html, rendered with Playwright), the
// simulator recording in the phone, a red ring on every tap, the voice-over at each scene's start
// and a quiet generated pad ducked under it. Writes out/<lang>/$TUTORIAL_NAME-<lang>.mp4.
// The recording (out/<lang>/sim.mp4) is first re-encoded with macOS `avconvert` (see below), and
// the rectangles in timeline.blur are pixelated while they are on screen.
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const lang = process.argv[2] ?? "de";
// The tutorial folder (script.<lang>.json, stage.html, out/): second argument, default cwd.
const here = resolve(process.argv[3] ?? process.cwd());
const out = join(here, "out", lang);
const script = JSON.parse(readFileSync(join(here, `script.${lang}.json`), "utf8"));
const brand = script.brand ?? {};
const vo = JSON.parse(readFileSync(join(out, "vo.json"), "utf8"));
const tl = JSON.parse(readFileSync(join(out, "timeline.json"), "utf8"));
// Playwright from the project (run from a folder whose node_modules has it, or set PLAYWRIGHT_FROM).
const require = createRequire(join(resolve(process.env.PLAYWRIGHT_FROM ?? here), "package.json"));
const { chromium } = require("playwright");

// Phone screen on the stage (stage.html: phone at 1196,50, 456×980).
const SCREEN = { x: 1208, y: 70, w: 432, h: 939 };
const CARDS = new Set(["intro", "outro"]);

// 1. Stage images.
const stageDir = join(out, "stage");
mkdirSync(stageDir, { recursive: true });
cpSync(join(here, "stage.html"), join(stageDir, "stage.html")); // copied from templates/stage-phone.html
// brand.logo (on light) and brand.logoOnDark, paths relative to the tutorial folder.
if (brand.logo) cpSync(resolve(here, brand.logo), join(stageDir, "logo.svg"));
if (brand.logoOnDark) cpSync(resolve(here, brand.logoOnDark), join(stageDir, "logo-dark.svg"));
// TUTORIAL_CHROME, else Playwright's own headless shell, else the newest one installed (the
// project's Playwright may be newer than the browsers in the cache).
const pwCache = join(process.env.HOME, "Library/Caches/ms-playwright");
const newestShell = () => {
	const dir = (existsSync(pwCache) ? readdirSync(pwCache) : [])
		.filter((d) => /^chromium_headless_shell-\d+$/.test(d))
		.sort((a, b) => Number(a.split("-")[1]) - Number(b.split("-")[1]))
		.at(-1);
	return dir && join(pwCache, dir, "chrome-headless-shell-mac-arm64/chrome-headless-shell");
};
const browser = await chromium.launch({
	executablePath: process.env.TUTORIAL_CHROME ?? (existsSync(chromium.executablePath()) ? undefined : newestShell()),
});
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
for (const scene of script.scenes) {
	const q = new URLSearchParams(
		scene.id === "intro"
			? { mode: "title", title: script.title, subtitle: script.subtitle }
			: scene.id === "outro"
				? { mode: "end", endTitle: script.endTitle ?? script.title, endSubtitle: script.endSubtitle ?? "" }
				: { chapter: scene.chapter, caption: scene.vo },
	);
	if (brand.color) q.set("brand", brand.color);
	await page.goto(`${pathToFileURL(join(stageDir, "stage.html"))}?${q}`);
	await page.waitForTimeout(250);
	await page.screenshot({ path: join(stageDir, `${scene.id}.png`) });
}
await browser.close();

// 2. Rounded screen corners: the mask is the stage itself around a rounded hole, so the
//    recording's square corners show exactly what lies behind them (bezel or background).
//    Plus the tap ring.
const firstPhoneScene = script.scenes.find((s) => !CARDS.has(s.id))?.id;
execFileSync("python3", [
	"-c",
	`
from PIL import Image, ImageDraw
x,y,w,h,r=${SCREEN.x},${SCREEN.y},${SCREEN.w},${SCREEN.h},58
bg=Image.open("${join(stageDir, `${firstPhoneScene}.png`)}").convert("RGBA").crop((x,y,x+w,y+h))
hole=Image.new("L",(w,h),255); ImageDraw.Draw(hole).rounded_rectangle([0,0,w-1,h-1],radius=r,fill=0)
bg.putalpha(hole); bg.save("${join(stageDir, "mask.png")}")
s=72; g=Image.new("RGBA",(s,s),(0,0,0,0)); d=ImageDraw.Draw(g)
c=tuple(int("${(brand?.color ?? "#dd083b").slice(1)}"[i:i+2],16) for i in (0,2,4))
d.ellipse([4,4,s-5,s-5],outline=c+(255,),width=6); d.ellipse([22,22,s-23,s-23],fill=c+(110,)); g.save("${join(stageDir, "tap.png")}")
`,
]);

// 3. Timing: t = 0 at the first scene's start.
const t0 = tl.scenes[0].start;
const end = tl.scenes.at(-1).end + 1.2;
const total = end - t0;
const sceneSpans = tl.scenes.map((s, i) => ({
	id: s.id,
	from: s.start - t0,
	to: (tl.scenes[i + 1]?.start ?? end) - t0,
}));
const phoneOn = sceneSpans
	.filter((s) => !CARDS.has(s.id))
	.map((s) => `between(t,${s.from.toFixed(2)},${s.to.toFixed(2)})`)
	.join("+");
const simOffset = Math.max(0, t0 - tl.videoStart);

// 3b. The recording. `simctl io recordVideo` writes H.264 that ffmpeg mis-times after long still
//     periods (pictures up to ~7 s out of place, a whole screen can vanish). Apple's own decoder
//     reads it right, so ffmpeg only ever sees an avconvert copy. SIM_AVCONVERT=0 skips it,
//     SIM_AVCONVERT_PRESET picks another preset (`avconvert --help` lists them).
const sizeOf = (f) =>
	execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f], {
		encoding: "utf8",
	})
		.trim()
		.split(",")
		.map(Number);
let simFile = join(out, "sim.mp4");
const [origW] = sizeOf(simFile);
if (process.env.SIM_AVCONVERT !== "0") {
	const av = join(out, "sim-av.mov");
	execFileSync(
		"avconvert",
		["--source", simFile, "--output", av, "--preset", process.env.SIM_AVCONVERT_PRESET ?? "PresetHighestQuality", "--replace"],
		{ stdio: "ignore" },
	);
	simFile = av;
}
const [rawW, rawH] = sizeOf(simFile);
const scale = rawW / origW; // a scaling preset (e.g. Preset1920x1080) shrinks the recording: scale the rectangles too

// Pixelation: timeline.blur = [{x, y, w, h, from, to}] — rectangles in the original recording's pixels,
// times in wall-clock seconds; timeline.noBlur = [{from, to}] cuts windows (e.g. a full-screen
// sheet covers the rectangles). Fixed rectangles, pixelated (not blurred): the same rectangles
// can be reused for stills.
const cutOut = (list, gaps) =>
	gaps.reduce(
		(acc, g) => acc.flatMap((b) => (g.to <= b.from || g.from >= b.to ? [b] : [{ ...b, to: g.from }, { ...b, from: g.to }])),
		list,
	);
const even = (n) => Math.max(2, Math.round(n / 2) * 2);
const blurGroups = new Map();
for (const b of cutOut(tl.blur ?? [], tl.noBlur ?? [])) {
	if (!(b.to > b.from)) continue;
	const x = Math.max(0, Math.round(b.x * scale));
	const y = Math.max(0, Math.round(b.y * scale));
	const w = even(Math.min(b.w * scale, rawW - x));
	const h = even(Math.min(b.h * scale, rawH - y));
	const k = `${x},${y},${w},${h}`;
	if (!blurGroups.has(k)) blurGroups.set(k, { x, y, w, h, spans: [] });
	blurGroups.get(k).spans.push([Math.max(0, b.from - tl.videoStart), Math.max(0, b.to - tl.videoStart)]);
}
const blocks = [...blurGroups.values()];
const CELL = Number(process.env.PIXEL_CELL ?? 22);

const inputs = [];
const filters = [];
sceneSpans.forEach((s, i) => {
	inputs.push("-loop", "1", "-t", (s.to - s.from).toFixed(3), "-i", join(stageDir, `${s.id}.png`));
	filters.push(`[${i}:v]fps=30,format=yuv420p,setsar=1[s${i}]`);
});
filters.push(`${sceneSpans.map((_, i) => `[s${i}]`).join("")}concat=n=${sceneSpans.length}:v=1:a=0[bg]`);
const simIdx = sceneSpans.length;
inputs.push("-i", simFile);
// Pixelate in the recording's own pixels and time, before it is trimmed and scaled.
filters.push(`[${simIdx}:v]fps=30,format=yuv420p${blocks.length ? `,split=${blocks.length + 1}[px0]${blocks.map((_, i) => `[pc${i}]`).join("")}` : "[px0]"}`);
let simLast = "px0";
blocks.forEach((b, i) => {
	const enable = b.spans.map(([a, z]) => `between(t,${a.toFixed(2)},${z.toFixed(2)})`).join("+");
	filters.push(
		`[pc${i}]crop=${b.w}:${b.h}:${b.x}:${b.y},scale=${Math.max(1, Math.round(b.w / CELL))}:${Math.max(1, Math.round(b.h / CELL))},scale=${b.w}:${b.h}:flags=neighbor[pp${i}]`,
		`[${simLast}][pp${i}]overlay=${b.x}:${b.y}:enable='${enable}'[px${i + 1}]`,
	);
	simLast = `px${i + 1}`;
});
filters.push(
	`[${simLast}]trim=start=${simOffset.toFixed(3)},setpts=PTS-STARTPTS,scale=${SCREEN.w}:${SCREEN.h},tpad=stop_mode=clone:stop_duration=${total.toFixed(1)}[sim]`,
);
const maskIdx = simIdx + 1;
inputs.push("-loop", "1", "-i", join(stageDir, "mask.png"));
const tapIdx = maskIdx + 1;
inputs.push("-loop", "1", "-i", join(stageDir, "tap.png"));
filters.push(`[bg][sim]overlay=${SCREEN.x}:${SCREEN.y}:enable='${phoneOn}'[v1]`);
filters.push(`[v1][${maskIdx}:v]overlay=${SCREEN.x}:${SCREEN.y}:shortest=1:enable='${phoneOn}'[v2]`);
let last = "v2";
filters.push(`[${tapIdx}:v]split=${Math.max(1, tl.taps.length)}${tl.taps.map((_, i) => `[tp${i}]`).join("") || "[tp0]"}`);
tl.taps.forEach((tap, i) => {
	const t = tap.t - t0;
	const x = Math.round(SCREEN.x + tap.x * SCREEN.w - 36);
	const y = Math.round(SCREEN.y + tap.y * SCREEN.h - 36);
	// The ring shows just before and during the tap: the screen reacts ~0.3 s after it.
	filters.push(`[${last}][tp${i}]overlay=${x}:${y}:enable='between(t,${(t - 0.3).toFixed(2)},${(t + 0.25).toFixed(2)})'[t${i}]`);
	last = `t${i}`;
});
filters.push(`[${last}]format=yuv420p[vout]`);

// 4. Audio: the voice at each scene's start, a quiet pad ducked under it (as in the extension's render).
const voLabels = [];
let audioIdx = tapIdx + 1;
tl.scenes.forEach((scene, i) => {
	inputs.push("-i", vo.scenes[scene.id].file);
	const delay = Math.round((scene.voStart - t0) * 1000);
	filters.push(`[${audioIdx}:a]aresample=48000,aformat=channel_layouts=stereo,adelay=${delay}|${delay}[a${i}]`);
	voLabels.push(`[a${i}]`);
	audioIdx++;
});
filters.push(`${voLabels.join("")}amix=inputs=${voLabels.length}:normalize=0,apad=whole_dur=${total.toFixed(2)}[vo]`);
const chord = (n) => `if(eq(mod(floor(t/4),4),0),${n[0]},if(eq(mod(floor(t/4),4),1),${n[1]},if(eq(mod(floor(t/4),4),2),${n[2]},${n[3]})))`;
const expr = `pow(sin(PI*mod(t,4)/4),0.6)*(0.5*sin(2*PI*${chord([220, 174.61, 196, 196])}*t)+0.35*sin(2*PI*${chord([261.63, 220, 246.94, 246.94])}*t)+0.3*sin(2*PI*${chord([329.63, 261.63, 293.66, 293.66])}*t))`;
filters.push(
	`aevalsrc='${expr}':s=48000:d=${total.toFixed(2)},aformat=channel_layouts=stereo,lowpass=f=900,aecho=0.8:0.7:120|240:0.35|0.2,volume=0.06,afade=t=in:d=2,afade=t=out:st=${(total - 3).toFixed(2)}:d=3[bed]`,
	"[vo]asplit=2[vo1][vo2]",
	"[bed][vo2]sidechaincompress=threshold=0.015:ratio=10:attack=20:release=1500[ducked]",
	"[vo1][ducked]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[aout]",
);

const file = join(out, `${process.env.TUTORIAL_NAME ?? "app"}-${lang}.mp4`);
writeFileSync(join(out, "filter.txt"), filters.join(";\n"));
execFileSync(
	"ffmpeg",
	[
		"-y", "-loglevel", "error", ...inputs,
		"-/filter_complex", join(out, "filter.txt"),
		"-map", "[vout]", "-map", "[aout]",
		"-c:v", "libx264", "-preset", "slow", "-crf", "20",
		"-c:a", "aac", "-b:a", "160k", "-ar", "48000",
		"-movflags", "+faststart", "-t", total.toFixed(2), file,
	],
	{ stdio: "inherit" },
);
console.log(`${file} (${total.toFixed(1)} s, ${blocks.length} pixelated rectangles)`);
