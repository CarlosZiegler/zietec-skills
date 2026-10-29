// Mode B — the popup's world for the tutorial: chrome.* and the app's API answered in the page,
// with a clock the recorder can move (window.__demo). Loaded before the popup bundle (demo.html).
// Example data only, no server. EXAMPLE: a time tracker with start / pause / stop; replace
// ROUTES and `world` with what the real popup calls.
(() => {
	const MIN = 60000;
	let anchorDemo = Date.parse("2026-01-15T08:02:00.000Z");
	let anchorReal = performance.now();
	const realNow = Date.now.bind(Date);
	const demoNow = () => anchorDemo + (performance.now() - anchorReal);
	Date.now = () => Math.floor(demoNow());

	const world = {
		state: "IDLE", // IDLE | WORKING | PAUSED | DONE
		blocks: [], // {type: "WORK" | "PAUSE", from, to}
		signedIn: false,
		open: [
			{ date: "2026-01-12", minutes: 480 },
			{ date: "2026-01-13", minutes: 472 },
		],
		listeners: [],
	};
	const iso = (ms) => new Date(ms).toISOString();
	const minutesOf = (type) =>
		world.blocks
			.filter((b) => b.type === type)
			.reduce((sum, b) => sum + ((b.to ? Date.parse(b.to) : demoNow()) - Date.parse(b.from)) / MIN, 0);
	const snapshot = () => ({
		state: world.state,
		since: world.blocks.find((b) => !b.to)?.from ?? null,
		serverTime: iso(demoNow()),
		workMinutes: Math.round(minutesOf("WORK")),
		pauseMinutes: Math.round(minutesOf("PAUSE")),
		blocks: world.blocks,
	});
	const act = (action) => {
		const now = iso(demoNow());
		const running = world.blocks.find((b) => !b.to);
		if (running) running.to = now;
		if (action === "start" || action === "resume") world.blocks.push({ type: "WORK", from: now, to: null });
		if (action === "pause") world.blocks.push({ type: "PAUSE", from: now, to: null });
		world.state = { start: "WORKING", resume: "WORKING", pause: "PAUSED", stop: "DONE" }[action] ?? world.state;
		return snapshot();
	};

	// chrome.* — the parts a popup usually touches.
	const store = { session: {}, local: {} };
	const area = (name) => ({
		get: async (keys) => {
			const out = {};
			for (const k of [].concat(keys ?? Object.keys(store[name]))) if (k in store[name]) out[k] = store[name][k];
			return out;
		},
		set: async (items) => Object.assign(store[name], items),
		remove: async (keys) => {
			for (const k of [].concat(keys)) delete store[name][k];
		},
		onChanged: { addListener() {}, removeListener() {} },
		setAccessLevel: async () => {},
	});
	const ev = { addListener() {}, removeListener() {}, hasListener: () => false };
	globalThis.chrome = {
		runtime: {
			id: "demo",
			getManifest: () => ({ version: "1.0.0", manifest_version: 3 }),
			getURL: (p) => p,
			onMessage: ev,
			sendMessage: async (message) => {
				if (message?.type === "connect") {
					// The stage plays the web app's connect page; resolves once "Connect" was clicked.
					await new Promise((resolve) => world.listeners.push(resolve));
					store.session.auth = { token: "demo", expiresAt: iso(realNow() + 7 * 86400000) };
					world.signedIn = true;
				}
				if (message?.type === "signOut") store.session = {};
				return { ok: true };
			},
		},
		commands: { getAll: async () => [{ name: "_execute_action", shortcut: "Alt+Shift+S" }] },
		storage: { session: area("session"), local: area("local"), sync: area("local"), managed: area("local"), onChanged: ev },
	};
	globalThis.browser = globalThis.chrome;

	// The API: path → handler(input). Answers are JSON; adapt the envelope to the client (tRPC,
	// REST, GraphQL …).
	const ROUTES = {
		"/api/me": () => ({ name: "Alex Example", company: "Example Ltd", locale: "en" }),
		"/api/timer/state": () => snapshot(),
		"/api/timer/start": () => act("start"),
		"/api/timer/pause": () => act("pause"),
		"/api/timer/resume": () => act("resume"),
		"/api/timer/stop": () => act("stop"),
		"/api/days/open": () => ({ days: world.open }),
		"/api/days/confirm": (input) => {
			world.open = world.open.filter((d) => d.date !== input?.date);
			return { confirmed: [input?.date] };
		},
	};
	window.fetch = async (url, init) => {
		const path = new URL(url, location.href).pathname;
		const input = init?.body ? JSON.parse(init.body) : undefined;
		await new Promise((r) => setTimeout(r, 260)); // a real round trip, so spinners show
		const handler = ROUTES[path];
		if (!handler) return new Response("not mocked", { status: 404 });
		return Response.json(handler(input));
	};

	window.__demo = {
		/** Move the demo clock to an instant (ISO); the popup's timers continue from there. */
		setNow: (isoTime) => {
			anchorDemo = Date.parse(isoTime);
			anchorReal = performance.now();
		},
		/** The stage's "Connect" button was clicked. */
		connected: () => {
			for (const resolve of world.listeners.splice(0)) resolve();
		},
		/** What the toolbar badge shows (polled by stage-popup.html). */
		badge: () => {
			if (world.state === "WORKING") {
				const m = minutesOf("WORK");
				return { text: `${Math.floor(m / 60)}:${String(Math.floor(m % 60)).padStart(2, "0")}`, tone: "" };
			}
			if (world.state === "PAUSED") return { text: "P", tone: "pause" };
			return { text: world.signedIn && world.open.length ? String(world.open.length) : "", tone: "alert" };
		},
		world,
	};
})();
