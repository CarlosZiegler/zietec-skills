// Mode C — records an iOS app tutorial on the simulator: `simctl io recordVideo` captures the
// screen while taps go to elements found by accessibility label (argent `describe` / `gesture-tap`).
// Copy into <app>/tutorial/, set SIM_UDID and APP_SCHEME, adapt ACTIONS (one per scene id).
// Writes out/<lang>/sim.mp4 + out/<lang>/timeline.json for scripts/render-phone.mjs.
import { execFileSync, spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] ?? "de";
const UDID = process.env.SIM_UDID; // xcrun simctl list devices booted
const SCHEME = process.env.APP_SCHEME ?? "myapp://";
if (!UDID) throw new Error("set SIM_UDID");
const out = join(here, "out", lang);
mkdirSync(out, { recursive: true });
const script = JSON.parse(readFileSync(join(here, `script.${lang}.json`), "utf8"));
const vo = JSON.parse(readFileSync(join(out, "vo.json"), "utf8"));

const npx = join(homedir(), ".npm/_npx");
const argentBin = readdirSync(npx)
	.map((d) => join(npx, d, "node_modules/.bin/argent"))
	.find((p) => existsSync(p));
if (!argentBin) throw new Error("argent not found: run `npx -y @swmansion/argent --help` once");
const argent = (...args) => execFileSync(argentBin, ["run", ...args, "--udid", UDID], { encoding: "utf8", cwd: "/tmp" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
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

const taps = [];
const tap = async (pattern, { wait = 1200, required = true } = {}) => {
	const el = find(pattern);
	if (!el) {
		if (required) console.log(`  not found: ${pattern} — on screen: ${describe().map((e) => e.label).filter(Boolean).slice(0, 25).join(" | ")}`);
		return false;
	}
	const x = el.x + el.w / 2;
	const y = el.y + el.h / 2;
	taps.push({ t: Date.now() / 1000, x, y });
	argent("gesture-tap", "--x", String(x), "--y", String(y));
	await sleep(wait);
	return true;
};
const open = async (path, wait = 2500) => {
	execFileSync("xcrun", ["simctl", "openurl", UDID, `${SCHEME}${path}`]);
	await sleep(wait);
};

await open("", 3500); // the app's start screen

const video = join(out, "sim.mp4");
rmSync(video, { force: true });
const recorder = spawn("xcrun", ["simctl", "io", UDID, "recordVideo", "--codec=h264", "--force", video], { stdio: "ignore" });
const recStart = Date.now() / 1000;
await sleep(1500);

// EXAMPLE scenes — replace labels with the app's own (read them with `argent run describe`).
// Navigate in-app (tap rows, "Back"): deep links lag on a deep stack.
const ACTIONS = {
	intro: async () => {},
	overview: async () => {},
	action: async (at) => {
		await tap(/^Settings/);
		await at(2600);
		await tap(/^Start$/);
	},
	form: async (at) => {
		await tap(/^Confirm$/, { wait: 1600 });
		await at(3000);
		await tap(/^Back$/, { required: false });
	},
	outro: async () => {},
};

const timeline = { recStart, scenes: [], taps };
for (const scene of script.scenes) {
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
	console.log(`${scene.id}: ${((Date.now() - start) / 1000).toFixed(2)} s`);
}
await sleep(800);
recorder.kill("SIGINT");
await new Promise((r) => recorder.on("exit", r));
await sleep(500);
const duration = Number(
	execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], { encoding: "utf8" }).trim(),
);
// recordVideo writes frames only when the screen changes: the file starts at recStart but ends at
// the last change — never derive the start from stop − duration.
timeline.videoStart = recStart;
timeline.videoDuration = duration;
writeFileSync(join(out, "timeline.json"), JSON.stringify(timeline, null, "\t"));
console.log(`video ${duration.toFixed(1)} s, ${taps.length} taps`);
