# -*- coding: utf-8 -*-
# Forja · verifica overflow de artboards de tamanho fixo (Doc e Pitch) e tira screenshots (reduced-motion).
# uso: python3 verify_pages.py <pasta project> "Doc-*" [shots: lista separada por vírgula | all]
# Doc: main.scrollHeight <= main.clientHeight (área útil 948). Pitch: nada sai do corpo do slide.
# Marque com data-skip elementos cortados de propósito (ex.: celulares dentro do slide).
# Rode a partir de build/ (usa preview.localize e build/fonts; screenshots em build/shots).
import os, re, sys, glob, json
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.getcwd()
PROJ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "project")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True); os.makedirs(os.path.join(HERE, "verify"), exist_ok=True)
pat = sys.argv[2] if len(sys.argv) > 2 else "*.dc.html"
shots = sys.argv[3].split(",") if len(sys.argv) > 3 else []
from preview import localize
files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(PROJ, pat)))
bad = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in files:
        raw = open(os.path.join(PROJ, f)).read()
        html = localize(raw)
        m = re.search(r'"\$preview":\{"width":(\d+),"height":(\d+)\}', raw)
        w, h = int(m.group(1)), int(m.group(2))
        path = os.path.join(HERE, "verify", "_v.html"); open(path, "w").write(html)
        pg = b.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
        pg.goto("file://" + path); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(350)
        r = pg.evaluate("""() => {
          const root = document.querySelector('x-dc > div'); const main = root.querySelector('main');
          const rr = root.getBoundingClientRect(); const out = {rootSH: root.scrollHeight, rootCH: root.clientHeight, rootSW: root.scrollWidth, rootCW: root.clientWidth};
          if (main) { out.mainSH = main.scrollHeight; out.mainCH = main.clientHeight; out.mainSW = main.scrollWidth; out.mainCW = main.clientWidth; }
          const wide = [];
          root.querySelectorAll('*').forEach(e => { if (e.closest('[data-skip]') || e.ownerSVGElement) return; const bb = e.getBoundingClientRect(); if (bb.width && (bb.right > rr.right + 1 || bb.bottom > rr.bottom + 1)) wide.push(e.tagName + ' ' + (e.textContent || '').trim().slice(0, 40)); });
          out.outside = wide.slice(0, 4);
          if (main) { const mr = main.getBoundingClientRect(); const ww = []; main.querySelectorAll('*').forEach(e => { if (e.ownerSVGElement) return; const bb = e.getBoundingClientRect(); if (bb.width && bb.right > mr.right + 0.5) ww.push(e.tagName + ' ' + (e.textContent || '').trim().slice(0, 30) + ' r=' + (bb.right - mr.left).toFixed(1)); }); out.mainWide = ww.slice(0, 3); }
          if (root.clientWidth === 1920) { const body = root.children[1]; const bb0 = body.getBoundingClientRect(); const over = [];
            body.querySelectorAll('*').forEach(e => { if (e.closest('[data-skip]') || e.ownerSVGElement) return; const bb = e.getBoundingClientRect(); if (bb.width && (bb.bottom > bb0.bottom + 1 || bb.right > bb0.right + 1)) over.push(e.tagName + ' ' + (e.textContent || '').trim().slice(0, 30) + ' b=' + Math.round(bb.bottom)); });
            if (over.length) out.outside = over.slice(0, 3); }
          return out; }""")
        if r.get("mainSH", 0) > r.get("mainCH", 1e9) or r["rootSH"] > r["rootCH"] or r["rootSW"] > r["rootCW"] or r.get("mainSW", 0) > r.get("mainCW", 1e9) or r["outside"]:
            bad.append((f, r))
        if f in shots or "all" in shots:
            pg.screenshot(path=os.path.join(SHOTS, f.replace(".dc.html", ".png")))
        pg.close()
    b.close()
print("checked", len(files), "problems", len(bad))
for f, r in bad:
    print(f, json.dumps(r)[:300])
