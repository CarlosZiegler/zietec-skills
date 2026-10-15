// Injected into every page of the web app while the tutorial records (Playwright addInitScript):
// cursor, click ripple, highlight ring, chapter chip, captions, title and end cards. Hides dev-only
// UI and blurs any e-mail address on screen. State survives navigations via sessionStorage.
// Tokens filled by the recorder: __BRAND__ (CSS color), __LOGO__ (inline <svg> markup — an <img>
// may be blocked by the app's CSP), __END_TITLE__, __END_SUBTITLE__.
(() => {
	const css = `
	#tut-root { position: fixed; inset: 0; pointer-events: none; z-index: 2147483000; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
	#tut-cursor { position: absolute; left: 0; top: 0; width: 28px; height: 28px; opacity: 0; transition-property: transform; transition-timing-function: cubic-bezier(.45,.05,.25,1); filter: drop-shadow(0 3px 4px rgba(0,0,0,.35)); }
	.tut-ripple { position: absolute; width: 46px; height: 46px; margin: -23px 0 0 -23px; border-radius: 50%; border: 3px solid __BRAND__; animation: tut-ripple .6s ease-out forwards; }
	@keyframes tut-ripple { from { transform: scale(.3); opacity: .9 } to { transform: scale(1.6); opacity: 0 } }
	#tut-ring { position: absolute; border: 3px solid __BRAND__; border-radius: 12px; box-shadow: 0 0 0 6px color-mix(in srgb, __BRAND__ 15%, transparent); opacity: 0; transition: all .35s; }
	#tut-ring.on { opacity: 1; }
	#tut-chapter { position: absolute; top: 14px; left: 50%; transform: translateX(-50%); padding: 6px 14px; border-radius: 999px; background: rgba(24,24,27,.86); color: #fff; font-size: 14px; font-weight: 600; }
	#tut-chapter:empty { display: none; }
	#tut-caption { position: absolute; left: 50%; bottom: 22px; transform: translateX(-50%); max-width: 1100px; padding: 11px 20px; border-radius: 12px; background: rgba(24,24,27,.88); color: #fff; font-size: 20px; line-height: 1.35; text-align: center; }
	#tut-caption:empty { display: none; }
	.tut-card { position: absolute; inset: 0; display: grid; place-items: center; background: linear-gradient(160deg, #1c1c21, #26262d); color: #fff; opacity: 0; transition: opacity .6s; }
	.tut-card.on { opacity: 1; }
	.tut-card .in { display: grid; gap: 22px; justify-items: center; text-align: center; }
	.tut-card img { height: 54px !important; width: auto !important; max-width: none !important; display: block !important; }
	.tut-card h1 { margin: 0; font-size: 60px; letter-spacing: -.02em; }
	.tut-card p { margin: 0; font-size: 24px; color: #c9c9d2; }
	.tut-card .rule { width: 70px; height: 4px; border-radius: 2px; background: __BRAND__; }
	#tut-sync { position: absolute; inset: 0; background: #ff00ff; display: none; }
	button[aria-label="Open TanStack Devtools"], .tsqd-open-btn-container, [class*="TanStackRouterDevtools"] { display: none !important; }
	.tut-blur { filter: blur(6px) !important; }
	`;
	const mount = () => {
		// The newest copy wins: a re-recorded tutorial replaces the overlay an earlier take left.
		for (const r of document.querySelectorAll("#tut-root")) r.remove();
		const style = document.createElement("style");
		style.textContent = css;
		document.head.appendChild(style);
		const root = document.createElement("div");
		root.id = "tut-root";
		root.innerHTML = `
			<div id="tut-sync"></div>
			<div id="tut-ring"></div>
			<div id="tut-chapter"></div>
			<div id="tut-caption"></div>
			<div class="tut-card" id="tut-title"><div class="in">__LOGO__<h1 id="tut-title-h"></h1><div class="rule"></div><p id="tut-title-p"></p></div></div>
			<div class="tut-card" id="tut-end"><div class="in">__LOGO__<h1>__END_TITLE__</h1><div class="rule"></div><p>__END_SUBTITLE__</p></div></div>
			<svg id="tut-cursor" viewBox="0 0 24 24"><path d="M4 2l15 9.2-6.6 1.4L16 20l-2.8 1.3-3.5-7.6L4 18z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`;
		document.body.appendChild(root);
		const saved = JSON.parse(sessionStorage.getItem("tut") || "{}");
		const $ = (id) => document.getElementById(id);
		const set = (patch) => sessionStorage.setItem("tut", JSON.stringify({ ...JSON.parse(sessionStorage.getItem("tut") || "{}"), ...patch }));
		let cx = saved.cx ?? 768, cy = saved.cy ?? 900;
		$("tut-cursor").style.transform = `translate(${cx - 5}px, ${cy - 3}px)`;
		// Hidden until it first moves (the intro card has no cursor).
		if (saved.cursorShown) $("tut-cursor").style.opacity = "1";
		$("tut-chapter").textContent = saved.chapter ?? "";
		$("tut-caption").textContent = saved.caption ?? "";
		// The account footer of the sidebar carries the e-mail: never on screen.
		const blur = () => {
			for (const el of document.querySelectorAll("button, a, div")) {
				if (el.childElementCount < 6 && /@[a-z0-9.-]+\.[a-z]{2,}/i.test(el.textContent || "") && (el.textContent || "").length < 80) el.classList.add("tut-blur");
			}
		};
		blur();
		new MutationObserver(blur).observe(document.body, { childList: true, subtree: true });
		window.__stage = {
			sync: (on) => { $("tut-sync").style.display = on ? "block" : "none"; },
			chapter: (t) => { $("tut-chapter").textContent = t; set({ chapter: t }); },
			caption: (t) => { $("tut-caption").textContent = t; set({ caption: t }); },
			move: (x, y, ms = 700) => {
				const c = $("tut-cursor");
				c.style.transitionDuration = `${ms}ms`;
				c.style.transform = `translate(${x - 5}px, ${y - 3}px)`;
				c.style.opacity = "1";
				cx = x; cy = y; set({ cx, cy, cursorShown: true });
			},
			click: () => {
				const r = document.createElement("div");
				r.className = "tut-ripple"; r.style.left = `${cx}px`; r.style.top = `${cy}px`;
				$("tut-root").appendChild(r); setTimeout(() => r.remove(), 700);
			},
			ring: (rect) => {
				const ring = $("tut-ring");
				if (!rect) { ring.classList.remove("on"); return; }
				Object.assign(ring.style, { left: `${rect.x - 7}px`, top: `${rect.y - 7}px`, width: `${rect.width + 14}px`, height: `${rect.height + 14}px` });
				ring.classList.add("on");
			},
			title: (h, p, on) => { $("tut-title-h").textContent = h; $("tut-title-p").textContent = p; $("tut-title").classList.toggle("on", on); },
			end: (on) => $("tut-end").classList.toggle("on", on),
		};
	};
	if (document.body) mount();
	else document.addEventListener("DOMContentLoaded", mount, { once: true });
})();
