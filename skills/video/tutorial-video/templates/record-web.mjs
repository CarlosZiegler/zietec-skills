// Mode A — records a tutorial of a signed-in web app. Run as a command module of
// scripts/driver.mjs (default export receives { page, slug, log }). Copy into <app>/tutorial/,
// then adapt BASE, the overlay tokens and ACTIONS (one function per scene id of script.<lang>.json).
// Writes out/<lang>/frames/*.jpg + out/<lang>/timeline.json for scripts/render-frames.mjs.
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const BASE = process.env.APP_URL ?? "http://localhost:3000";
// Path of the skill's overlay.js (copy it next to this file, or point here).
const OVERLAY = process.env.TUTORIAL_OVERLAY ?? join(HERE, "overlay.js");

export default async ({ page, log }) => {
	const lang = process.env.TUTORIAL_LANG ?? "de";
	const script = JSON.parse(readFileSync(join(HERE, `script.${lang}.json`), "utf8"));
	const vo = JSON.parse(readFileSync(join(HERE, "out", lang, "vo.json"), "utf8"));
	const out = join(HERE, "out", lang);
	const framesDir = join(out, "frames");
	rmSync(framesDir, { recursive: true, force: true });
	mkdirSync(framesDir, { recursive: true });

	// The overlay with its tokens filled. Inline SVG for the logo: an <img> may be blocked by CSP.
	const brand = script.brand ?? {};
	const logoSvg = brand.logoOnDark
		? readFileSync(join(HERE, brand.logoOnDark), "utf8")
				.replace(/<\?xml[^>]*>/, "")
				.replace("<svg ", '<svg style="height:54px;width:auto" ')
				.replace(/\s+/g, " ")
		: "";
	const overlay = readFileSync(OVERLAY, "utf8")
		.replaceAll("__BRAND__", brand.color ?? "#4f46e5")
		.replaceAll("__LOGO__", logoSvg)
		.replaceAll("__END_TITLE__", script.endTitle ?? script.title)
		.replaceAll("__END_SUBTITLE__", script.endSubtitle ?? "");
	await page.addInitScript(overlay);
	await page.evaluate(() => sessionStorage.removeItem("tut"));
	await page.goto(`${BASE}/`, { waitUntil: "domcontentloaded" });
	await page.waitForTimeout(3000);
	await page.evaluate(overlay);

	const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
	const stage = (fn, ...args) => page.evaluate(([name, a]) => window.__stage?.[name](...a), [fn, args]);
	/** After a navigation: overlay back, the page's own content (`ready`) visible. */
	const settle = async (ready) => {
		await page.waitForLoadState("domcontentloaded");
		await page.waitForFunction(() => Boolean(window.__stage), null, { timeout: 30000 });
		if (ready) await ready.waitFor({ state: "visible", timeout: 30000 });
		await sleep(900);
	};
	const clickOn = async (locator, move = 750) => {
		await locator.scrollIntoViewIfNeeded().catch(() => {});
		await sleep(250); // let a smooth scroll settle before measuring
		const box = await locator.boundingBox();
		if (!box) throw new Error("no box");
		await stage("move", box.x + Math.min(box.width / 2, 120), box.y + box.height / 2, move);
		await sleep(move + 120);
		await stage("click");
		await locator.click();
	};
	// A highlight is decoration: it never holds a scene up.
	const ringOn = async (locator) => {
		try {
			await locator.first().scrollIntoViewIfNeeded({ timeout: 3000 });
			await stage("ring", await locator.first().boundingBox({ timeout: 3000 }));
		} catch {
			// no ring then
		}
	};
	const ringOff = () => stage("ring", null);
	// Sidebars often exist twice (desktop + hidden mobile sheet): the visible one, by target.
	const nav = (hrefPart) => page.locator(`a[href*="${hrefPart}"]:visible`).first();

	const frames = [];
	const cdp = await page.context().newCDPSession(page);
	cdp.on("Page.screencastFrame", async ({ data, metadata, sessionId }) => {
		const file = join(framesDir, `${String(frames.length).padStart(6, "0")}.jpg`);
		frames.push({ file, t: metadata.timestamp });
		writeFileSync(file, Buffer.from(data, "base64"));
		await cdp.send("Page.screencastFrameAck", { sessionId }).catch(() => {});
	});
	await cdp.send("Page.startScreencast", { format: "jpeg", quality: 90, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });

	// EXAMPLE scenes — replace selectors and steps with the app's own.
	const ACTIONS = {
		intro: async (at, d) => {
			await stage("title", script.title, script.subtitle, true);
			await at(d - 700);
			await stage("title", script.title, script.subtitle, false);
		},
		overview: async (at) => {
			await at(900);
			await ringOn(page.getByRole("heading").first());
			await at(5000);
			await ringOff();
		},
		action: async (at) => {
			await clickOn(nav("/dashboard"));
			await settle(page.getByRole("button", { name: /Start/ }).first());
			await at(2500);
			await clickOn(page.getByRole("button", { name: /Start/ }).first());
		},
		form: async (at) => {
			await clickOn(page.getByRole("button", { name: /Confirm/ }).first(), 700);
			const dialog = page.getByRole("dialog").first();
			await dialog.waitFor();
			// Read a dialog off camera first: it may need a reason or a checkbox.
			await at(5000);
			await clickOn(dialog.getByRole("button", { name: /^Confirm$/ }), 600);
		},
		outro: async () => {
			await stage("move", 2400, 1400, 400);
			await stage("caption", "");
			await stage("end", true);
		},
	};

	// Fail fast: a missing element must not freeze the video for 30 s.
	page.setDefaultTimeout(9000);
	await stage("sync", true);
	await sleep(300);
	await stage("sync", false);
	await sleep(300);

	const timeline = { frames: [], scenes: [] };
	for (const scene of script.scenes) {
		const duration = Math.round(vo.scenes[scene.id].duration * 1000);
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
			log(`  scene ${scene.id}: ${String(e.message).split("\n")[0]}`);
		}
		await at(duration + 600);
		timeline.scenes.push({ id: scene.id, start: start / 1000, end: Date.now() / 1000, voStart: start / 1000 + 0.25 });
		log(`  ${scene.id}: ${((Date.now() - start) / 1000).toFixed(2)} s`);
	}
	await sleep(2200);
	await cdp.send("Page.stopScreencast");
	await sleep(300);
	page.setDefaultTimeout(30000);
	timeline.frames = frames;
	timeline.end = Date.now() / 1000;
	writeFileSync(join(out, "timeline.json"), JSON.stringify(timeline));
	log(`  ${frames.length} frames`);
};
