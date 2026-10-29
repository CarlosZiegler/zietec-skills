// Mode B — records an extension-popup tutorial: the real built popup (with demo-mock.js) on
// stage.html (from stage-popup.html), driven by Playwright, captured through the Chrome screencast
// with timestamps. Deterministic, touches no account. Each scene holds for its narration
// (out/<lang>/vo.json). Writes out/<lang>/frames/*.jpg + out/<lang>/timeline.json for
// scripts/render-frames.mjs.
// Copy into <extension>/tutorial/ next to stage.html and demo-mock.js; set EXT_BUILD (the built
// extension, e.g. WXT's .output/chrome-mv3) and PLAYWRIGHT_FROM; adapt ACTIONS.
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] ?? "de";
const require = createRequire(join(resolve(process.env.PLAYWRIGHT_FROM ?? here), "package.json"));
const { chromium } = require("playwright");
// The headless shell: its screencast covers the whole 1920×1080 viewport (full Chrome's new
// headless mode cuts the frame to 993 px). TUTORIAL_CHROME overrides.
const CHROME = process.env.TUTORIAL_CHROME;
const BUILD = resolve(here, process.env.EXT_BUILD ?? "../.output/chrome-mv3");

const script = JSON.parse(readFileSync(join(here, `script.${lang}.json`), "utf8"));
const brand = script.brand ?? {};
const vo = JSON.parse(readFileSync(join(here, "out", lang, "vo.json"), "utf8"));
const out = join(here, "out", lang);
const site = join(here, "out", "site");
const framesDir = join(out, "frames");

// The site: the extension build + the stage + a demo page that loads the popup with the mocks.
rmSync(site, { recursive: true, force: true });
cpSync(BUILD, site, { recursive: true });
mkdirSync(join(site, "stage"), { recursive: true });
if (brand.logo) cpSync(resolve(here, brand.logo), join(site, "stage", "logo.svg"));
if (brand.logoOnDark) cpSync(resolve(here, brand.logoOnDark), join(site, "stage", "logo-white.svg"));
cpSync(join(here, "stage.html"), join(site, "stage.html"));
cpSync(join(here, "demo-mock.js"), join(site, "demo-mock.js"));
// The popup's entry chunk and stylesheet (WXT names them popup-<hash>); adjust for other bundlers.
const find = (dir, prefix) => (existsSync(join(site, dir)) ? readdirSync(join(site, dir)).find((f) => f.startsWith(prefix)) : undefined);
const chunk = find("chunks", "popup-");
const css = find("assets", "popup-");
if (!chunk) throw new Error(`popup chunk not found in ${BUILD}/chunks`);
const color = brand.color ?? "#4f46e5";
writeFileSync(
	join(site, "demo.html"),
	`<!doctype html><html lang="${lang}"><head><meta charset="utf-8">${css ? `<link rel="stylesheet" href="/assets/${css}">` : ""}<style>html{zoom:1.3}.demo-ring{outline:3px solid ${color}!important;outline-offset:4px;transition:outline-color .3s}</style><script src="/demo-mock.js"></script></head><body><div id="root"></div><script type="module" src="/chunks/${chunk}"></script></body></html>`,
);

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml", ".json": "application/json" };
const server = createServer((req, res) => {
	const path = decodeURIComponent(new URL(req.url, "http://x").pathname);
	try {
		const body = readFileSync(join(site, path === "/" ? "stage.html" : path));
		res.writeHead(200, { "content-type": TYPES[extname(path)] ?? "application/octet-stream" });
		res.end(body);
	} catch {
		res.writeHead(404).end();
	}
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;

rmSync(framesDir, { recursive: true, force: true });
mkdirSync(framesDir, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROME, headless: true, args: ["--hide-scrollbars"] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, screen: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(`${base}/stage.html`);
const popup = page.frameLocator("#popupFrame");
// Wait for real content in the popup before recording (EXAMPLE: its first button).
await popup.getByRole("button").first().waitFor();

const frames = [];
const cdp = await page.context().newCDPSession(page);
cdp.on("Page.screencastFrame", async ({ data, metadata, sessionId }) => {
	const file = join(framesDir, `${String(frames.length).padStart(6, "0")}.jpg`);
	frames.push({ file, t: metadata.timestamp });
	writeFileSync(file, Buffer.from(data, "base64"));
	await cdp.send("Page.screencastFrameAck", { sessionId }).catch(() => {});
});
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const stage = (fn, ...args) => page.evaluate(([name, a]) => window.__stage[name](...a), [fn, args]);
const demo = (fn, ...args) =>
	page.evaluate(([name, a]) => document.getElementById("popupFrame").contentWindow.__demo[name](...a), [fn, args]);
const ext = page.locator("#ext");

/** Moves the cursor onto a locator (popup or stage), then clicks it with a ripple. */
const clickOn = async (locator, { move = 750, click = true } = {}) => {
	const box = await locator.boundingBox();
	if (!box) throw new Error("no box");
	await stage("move", box.x + box.width / 2, box.y + box.height / 2, move);
	await sleep(move + 120);
	if (!click) return;
	await stage("click");
	await locator.click();
};
/** Highlights an element: inside the popup an outline on it, on the stage a ring around it. */
const ringOn = async (locator) => {
	if (locator === ext) {
		await stage("ring", await locator.boundingBox());
		return;
	}
	await locator.evaluate((el) => el.classList.add("demo-ring"));
};
const ringOff = async () => {
	await stage("ring", null);
	await popup.locator(".demo-ring").evaluateAll((els) => {
		for (const el of els) el.classList.remove("demo-ring");
	});
};

if (brand.color) await stage("brand", brand.color);

// EXAMPLE scenes — replace with the popup's own buttons and the story of the script.
// `at(ms)` waits until that offset into the scene; `d` is the narration's length.
const ACTIONS = {
	intro: async (at, d) => {
		await stage("title", script.title, script.subtitle, true);
		await at(d - 700);
		await stage("title", script.title, script.subtitle, false);
	},
	install: async (at, d) => {
		await stage("overlay", "install", true);
		await at(600);
		await stage("step", 1);
		await at(d * 0.38);
		await stage("step", 2);
		await at(d * 0.66);
		await stage("step", 3);
		await at(d - 500);
		await stage("overlay", "install", false);
	},
	connect: async (at) => {
		await clickOn(ext);
		await stage("popup", true);
		await at(1900);
		await clickOn(popup.getByRole("button", { name: /Sign in/ }));
		await sleep(500);
		await stage("popup", false);
		await stage("page", "connect");
		await at(6000);
		await clickOn(page.locator("#connectButton"));
		await stage("connected");
		await demo("connected");
		await at(8500);
		await stage("page", "portal");
		await clickOn(ext);
		await stage("popup", true);
	},
	start: async (at) => {
		// The demo day starts at a fixed time, whatever the scenes before took.
		await demo("setNow", "2026-01-15T08:01:58.000Z");
		const button = popup.getByRole("button", { name: "Start" });
		await button.waitFor();
		await ringOn(button);
		await at(1300);
		await ringOff();
		await clickOn(button);
		await at(4600);
		await ringOn(ext); // the badge now counts
		await at(7000);
		await ringOff();
	},
	notice: async (at, d) => {
		await demo("setNow", "2026-01-15T13:48:20.000Z"); // jump the clock: hours later
		await at(900);
		await stage("notify", "Break due", "You have worked almost 6 hours without a break.");
		await at(d - 400);
		await stage("unnotify");
	},
	stop: async (at) => {
		await clickOn(popup.getByRole("button", { name: "Stop" }), { move: 600 });
		await at(3300);
		await clickOn(popup.getByRole("button", { name: "Confirm" }), { move: 600 });
	},
	security: async (at, d) => {
		await stage("move", 960, 1200, 600);
		await stage("popup", false);
		await stage("overlay", "security", true);
		await at(d - 400);
		await stage("overlay", "security", false);
	},
	outro: async () => {
		await stage("end", true, script.endTitle ?? script.title, script.endSubtitle ?? "");
	},
};

// Sync marker: one magenta flash at the start (render-frames.mjs starts after it).
await stage("sync", true);
await sleep(300);
await stage("sync", false);
await sleep(300);

const timeline = { frames: [], scenes: [] };
for (const scene of script.scenes) {
	const duration = Math.round(vo.scenes[scene.id].duration * 1000);
	const hold = duration + 600;
	const start = Date.now();
	await stage("chapter", scene.chapter);
	await stage("caption", scene.id === "intro" || scene.id === "outro" ? "" : scene.vo);
	const at = async (ms) => {
		const wait = start + ms - Date.now();
		if (wait > 0) await sleep(wait);
	};
	try {
		await ACTIONS[scene.id]?.(at, duration);
	} catch (e) {
		console.log(`  scene ${scene.id}: ${String(e.message).split("\n")[0]}`);
	}
	await at(hold);
	timeline.scenes.push({ id: scene.id, start: start / 1000, end: Date.now() / 1000, voStart: start / 1000 + 0.25 });
	console.log(`${scene.id}: ${((Date.now() - start) / 1000).toFixed(2)} s`);
}
await stage("caption", "");
await sleep(2200);
await cdp.send("Page.stopScreencast");
await sleep(300);
timeline.frames = frames.map((f) => ({ file: f.file, t: f.t }));
timeline.end = Date.now() / 1000;
writeFileSync(join(out, "timeline.json"), JSON.stringify(timeline));
await browser.close();
server.close();
console.log(`${frames.length} frames`);
