// Mode C — records an iOS app tutorial on the simulator: `simctl io recordVideo` captures the
// screen while taps go to elements found by accessibility label (argent `describe` / `gesture-tap`)
// or, when the element tree cannot be read, to coordinates measured on a screenshot.
// Copy into <app>/tutorial/, set SIM_UDID (and APP_SCHEME for deep links), adapt SCREENS and
// ACTIONS (one per scene id of script.<lang>.json).
// Writes out/<lang>/sim.mp4, out/<lang>/timeline.json (scene starts, taps, pixelation windows) and
// out/<lang>/check/*.png (one screenshot per scene) for scripts/render-phone.mjs.
// FINAL=0 = rehearsal: irreversible taps are skipped (see `if (!FINAL)` below).
import { execFileSync, spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { cpus, homedir, loadavg, tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] ?? "de";
// One simulator per job, named in every call: never "booted" (another job may own it).
const UDID = process.env.SIM_UDID; // xcrun simctl list devices
const SCHEME = process.env.APP_SCHEME ?? "myapp://";
if (!UDID) throw new Error("set SIM_UDID");
const FINAL = process.env.FINAL !== "0";
const out = join(here, "out", lang);
const checkDir = join(out, "check");
mkdirSync(checkDir, { recursive: true });
const script = JSON.parse(readFileSync(join(here, `script.${lang}.json`), "utf8"));
const vo = JSON.parse(readFileSync(join(out, "vo.json"), "utf8"));

// Under heavy load the simulator drops frames and taps land late: check before every take.
const load = loadavg()[0];
if (load > cpus().length) console.log(`WARNING: load ${load.toFixed(1)} > ${cpus().length} cores — wait or expect lag`);

const npx = join(homedir(), ".npm/_npx");
const argentBin = readdirSync(npx)
	.map((d) => join(npx, d, "node_modules/.bin/argent"))
	.find((p) => existsSync(p));
if (!argentBin) throw new Error("argent not found: run `npx -y @swmansion/argent --help` once");
const argent = (...args) => execFileSync(argentBin, ["run", ...args, "--udid", UDID], { encoding: "utf8", cwd: tmpdir() });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const now = () => Date.now() / 1000;
const taps = [];

// --- Taps by accessibility label (works with debug builds; release builds may expose no tree).
const LINE = /^\s*(AX\w+)\s+"([^"]*)"(?:\s+\S+="[^"]*")*\s+\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)/;
const describe = () => {
	const raw = argent("describe", "--json");
	const text = JSON.parse(raw).description ?? raw;
	return text
		.split("\n")
		.map((l) => LINE.exec(l))
		.filter(Boolean)
		.map(([, role, label, x, y, w, h]) => ({ role, label, x: +x, y: +y, w: +w, h: +h }));
};
const find = (pattern, roles = /AXButton|AXLink|AXGroup|AXCell/) =>
	describe().find((e) => pattern.test(e.label) && roles.test(e.role) && e.y > 0.04 && e.y < 0.98);
const tap = async (pattern, { wait = 1200, required = true } = {}) => {
	const el = find(pattern);
	if (!el) {
		if (required) console.log(`  not found: ${pattern} — on screen: ${describe().map((e) => e.label).filter(Boolean).slice(0, 25).join(" | ")}`);
		return false;
	}
	const x = el.x + el.w / 2;
	const y = el.y + el.h / 2;
	taps.push({ t: now(), x, y });
	argent("gesture-tap", "--x", String(x), "--y", String(y));
	await sleep(wait);
	return true;
};

// --- Taps by coordinates. When the element tree cannot be read without relaunching the app (a
// relaunch may sign the user out), measure positions on a downscaled screenshot
// (`xcrun simctl io <udid> screenshot s.png && sips -Z 900 s.png`) and verify every step with a
// screenshot. SHOT = the size of that downscaled screenshot.
const SHOT = { w: Number(process.env.SHOT_W ?? 414), h: Number(process.env.SHOT_H ?? 900) };
const tapAt = async (px, py, wait = 900) => {
	const x = px / SHOT.w;
	const y = py / SHOT.h;
	taps.push({ t: now() + 0.1, x, y });
	argent("gesture-tap", "--x", x.toFixed(4), "--y", y.toFixed(4));
	await sleep(wait);
};
const swipeAt = async (x1, y1, x2, y2, ms = 900, wait = 300) => {
	argent(
		"gesture-swipe", "--fromX", (x1 / SHOT.w).toFixed(4), "--fromY", (y1 / SHOT.h).toFixed(4),
		"--toX", (x2 / SHOT.w).toFixed(4), "--toY", (y2 / SHOT.h).toFixed(4), "--durationMs", String(ms), "--momentum", "false",
	);
	await sleep(wait);
};
const shot = (file) => {
	execFileSync("xcrun", ["simctl", "io", UDID, "screenshot", "--type=png", file], { stdio: "ignore" });
	return file;
};
// A label's position on a fresh screenshot by template matching (scripts/find-label.py; the
// template is a crop of an earlier screenshot at full resolution, x = its left edge in raw px).
// Returns the y to pass to tapAt, or null.
const FIND_LABEL = process.env.FIND_LABEL ?? join(here, "find-label.py");
const findLabel = async (template, xRaw, { maxDiff = 30, tries = 6 } = {}) => {
	for (let i = 0; i < tries; i++) {
		const [yFrac, diff] = execFileSync("python3", [FIND_LABEL, shot(join(out, "find.png")), template, String(xRaw)], { encoding: "utf8" })
			.trim()
			.split(" ")
			.map(Number);
		if (diff < maxDiff) return yFrac * SHOT.h;
		await sleep(400);
	}
	console.log(`  label not found: ${template}`);
	return null;
};

const open = async (path, wait = 2500) => {
	execFileSync("xcrun", ["simctl", "openurl", UDID, `${SCHEME}${path}`]);
	await sleep(wait);
};

// --- Pixelation windows. Rectangles in the recording's own pixels (the full-resolution
// screenshot size), per screen; `enter(name)` marks which screen is visible from now on. During a
// transition the rectangles are widened to the left edge for a moment (content slides in).
const SCREENS = {
	// home: [{ what: "own avatar", x: 1030, y: 186, w: 136, h: 136 }],
};
const blur = [];
const noBlur = []; // [{from, to}]: nothing pixelated (a full-screen sheet covers the rectangles)
let screen = null;
const enter = (name) => {
	const t = now();
	if (screen) {
		for (const r of SCREENS[screen.name] ?? []) {
			const wide = { ...r, x: 0, w: r.x + r.w };
			blur.push({ ...wide, from: screen.since - 0.2, to: screen.since + 0.6 });
			blur.push({ ...r, from: screen.since + 0.5, to: t + 0.05 });
			blur.push({ ...wide, from: t, to: t + 0.9 });
		}
	}
	screen = name ? { name, since: t } : null;
};

// Off camera: the start state (here: the app's start screen). Set it up and check it with a
// screenshot before the recorder starts.
await open("", 3500);
shot(join(checkDir, "00-start.png"));

const video = join(out, "sim.mp4");
rmSync(video, { force: true });
const recorder = spawn("xcrun", ["simctl", "io", UDID, "recordVideo", "--codec=h264", "--force", video], { stdio: "ignore" });
const recStart = now();
enter("home");
await sleep(1500);

// EXAMPLE scenes — replace labels / coordinates with the app's own (read labels with
// `argent run describe`, measure coordinates on a screenshot). Navigate in-app (tap rows, "Back"):
// deep links lag on a deep stack.
const ACTIONS = {
	intro: async () => {},
	overview: async () => {},
	action: async (at) => {
		await tap(/^Settings/);
		await at(2600);
		await tap(/^Start$/);
	},
	form: async (at) => {
		await tapAt(207, 760, 1600); // measured on a 414×900 screenshot
		enter("form");
		await at(3000);
		if (!FINAL) return; // rehearsal: stop before the irreversible step
		await tap(/^Confirm$/, { required: false });
	},
	outro: async () => {},
};

const timeline = { recStart, scenes: [], taps, blur, noBlur };
for (const [i, scene] of script.scenes.entries()) {
	const duration = Math.round(vo.scenes[scene.id].duration * 1000);
	const start = Date.now();
	const at = async (ms) => {
		const wait = start + ms - Date.now();
		if (wait > 0) await sleep(wait);
	};
	try {
		await ACTIONS[scene.id]?.(at, duration);
	} catch (e) {
		console.log(`  scene ${scene.id}: ${String(e.message).split("\n")[0]}`);
	}
	await at(duration + 600);
	timeline.scenes.push({ id: scene.id, start: start / 1000, end: Date.now() / 1000, voStart: start / 1000 + 0.25 });
	shot(join(checkDir, `${String(i + 1).padStart(2, "0")}-${scene.id}.png`));
	console.log(`${scene.id}: ${((Date.now() - start) / 1000).toFixed(2)} s (late ${((Date.now() - start - duration - 600) / 1000).toFixed(2)})`);
}
enter(null);
await sleep(800);
recorder.kill("SIGINT");
const recStop = now();
await new Promise((r) => recorder.on("exit", r));
await sleep(500);
const duration = Number(
	execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], { encoding: "utf8" }).trim(),
);
// recordVideo writes frames only when the screen changes: the file starts at recStart but ends at
// the last change — never derive the start from stop − duration.
timeline.videoStart = recStart;
timeline.videoDuration = duration;
timeline.recStop = recStop;
writeFileSync(join(out, "timeline.json"), JSON.stringify(timeline, null, "\t"));
console.log(`video ${duration.toFixed(1)} s, ${taps.length} taps, ${blur.length} pixelation windows, FINAL=${FINAL}`);
console.log(`check the screenshots in ${checkDir} before the take counts`);
