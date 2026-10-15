// Keeps one signed-in browser open and runs command modules dropped into <workdir>/cmd/ (in name
// order): each `export default async ({ page, ctx, log, S, match }) => {...}`; "cmd/exit" ends it.
// The user signs in by hand (off camera). Usage, from a folder whose node_modules has playwright:
//   node driver.mjs <workdir> <sign-in URL> <regex of a signed-in URL path>
// e.g. node driver.mjs /tmp/rec http://localhost:3000/sign-in '^/([a-z]\d{6})(/|$)'
// Recon pattern: drop small modules that log buttons/dialogs and screenshot, read driver.log.
import { createRequire } from "node:module";
import { appendFileSync, existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";

const require = createRequire(`${process.cwd()}/package.json`);
const { chromium } = require("playwright");
const S = process.argv[2];
mkdirSync(`${S}/cmd`, { recursive: true });
const LOG = `${S}/driver.log`;
writeFileSync(LOG, "");
const log = (l) => appendFileSync(LOG, `${l}\n`);
const ctx = await chromium.launchPersistentContext(`${S}/profile`, {
	executablePath:
		process.env.TUTORIAL_CHROME ??
		`${process.env.HOME}/Library/Caches/ms-playwright/chromium-1248/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`,
	headless: false,
	viewport: { width: 1536, height: 864 },
	deviceScaleFactor: 1.25,
	locale: "de-DE",
	args: ["--lang=de-DE", "--hide-scrollbars"],
});
const page = ctx.pages()[0] ?? (await ctx.newPage());
const START = process.argv[3] ?? "http://localhost:3000/sign-in";
const SIGNED_IN = new RegExp(process.argv[4] ?? "^/(?!sign-in)[^/]+");
await page.goto(START);
log("WAITING_FOR_LOGIN");
let match = null;
for (let i = 0; i < 1800 && !match; i++) {
	await page.waitForTimeout(1000);
	match = new URL(page.url()).pathname.match(SIGNED_IN);
}
if (!match) {
	log("FAIL no login");
	process.exit(1);
}
const slug = match[1] ?? "";
log("SIGNED_IN");
const done = new Set();
while (!existsSync(`${S}/cmd/exit`)) {
	for (const f of readdirSync(`${S}/cmd`).filter((n) => n.endsWith(".mjs")).sort()) {
		if (done.has(f)) continue;
		done.add(f);
		log(`RUN ${f}`);
		try {
			const mod = await import(`${S}/cmd/${f}?t=${Date.now()}`);
			await mod.default({ page, ctx, log, S, slug, match });
			log(`OK ${f}`);
		} catch (e) {
			log(`ERR ${f} ${String(e?.message ?? e).split("\n")[0]}`);
		}
	}
	await page.waitForTimeout(700);
}
await ctx.close();
