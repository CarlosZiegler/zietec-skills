# -*- coding: utf-8 -*-
# Forja · deck_check: revisão de um deck do tipo Slides antes de publicar (nascido no deck do Salles V4).
# Para cada slide da ordem do deck.json acusa:
#   fora da área     elemento além da área segura (96 px da borda de baixo e da direita, em 1920×1080)
#   cover corta      imagem com object-fit: cover cuja proporção (caixa de conteúdo, sem borda) difere > 3 % da imagem:
#                    corta as laterais ou o topo da tela fotografada. Ajuste a altura da caixa à proporção do print.
#   cortada          imagem recortada por um ancestral com overflow ≠ visible
#   sobrepõe         duas imagens que se cruzam (celulares encavalados). Se a sobreposição for de propósito, data-sobrepoe.
#   saindo do slide  imagem fora de 1920×1080
# E grava um PNG por slide em --shots para olhar (o gate não substitui olhar cada slide).
# Uso: python3 scripts/deck_check.py <pasta com project/deck.json> [--blobs blobs.json (id→arquivo local)] [--shots /tmp/deck] [ids...]
import os, re, sys, json

JS = r"""() => { const out = []; const ims = [...document.querySelectorAll('section img')].map(e => [e, e.getBoundingClientRect()]);
 document.querySelectorAll('section *').forEach(e => { if (e.closest('svg') && e.tagName != 'svg') return; const b = e.getBoundingClientRect();
   if (b.width && (b.bottom > 1080 - 96 || b.right > 1920 - 96)) out.push('fora da área: ' + e.tagName.toLowerCase() + '.' + (e.className.baseVal ?? e.className) + ' ' + Math.round(b.bottom) + '/' + Math.round(b.right)); });
 for (let i = 0; i < ims.length; i++) { const [e, a] = ims[i]; const cs = getComputedStyle(e); const n = e.alt || e.src.slice(-12);
   if (a.left < -1 || a.right > 1921 || a.bottom > 1081 || a.top < -1) out.push('saindo do slide: ' + n);
   for (let p = e.parentElement; p && p.tagName != 'SECTION'; p = p.parentElement) { if (getComputedStyle(p).overflow != 'visible') { const r = p.getBoundingClientRect();
     if (a.left < r.left - 1 || a.right > r.right + 1 || a.top < r.top - 1 || a.bottom > r.bottom + 1) { out.push('cortada: ' + n); break; } } }
   if (cs.objectFit == 'cover' && e.naturalWidth) { const bw = parseFloat(cs.borderLeftWidth) * 2, bh = parseFloat(cs.borderTopWidth) * 2;
     const rn = e.naturalWidth / e.naturalHeight, rb = (a.width - bw) / (a.height - bh); if (Math.abs(rn / rb - 1) > 0.03) out.push('cover corta: ' + n + ' ' + rn.toFixed(2) + ' vs ' + rb.toFixed(2)); }
   for (let j = i + 1; j < ims.length; j++) { const [f, b] = ims[j]; if (e.closest('[data-sobrepoe]') || f.closest('[data-sobrepoe]')) continue;
     const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
     if (ox > 4 && oy > 4) out.push('sobrepõe: ' + n + ' × ' + (f.alt || f.src.slice(-12))); } }
 return [...new Set(out)]; }"""


def main():
    a = sys.argv[1:]
    def opt(k, d=None):
        if k in a:
            i = a.index(k); v = a[i + 1]; del a[i:i + 2]; return v
        return d
    blobs, shots = opt("--blobs"), opt("--shots", "/tmp/forja_deck")
    D = a.pop(0); ids = a
    P = os.path.join(D, "project"); deck = json.load(open(os.path.join(P, "deck.json")))
    css = "".join(open(os.path.join(D, f)).read() for f in deck.get("format", {}).get("shared", []) if os.path.exists(os.path.join(D, f)))
    bm = json.load(open(blobs)) if blobs else {}
    os.makedirs(shots, exist_ok=True); bad = 0
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for sid in ids or deck["order"]:
            s = open(os.path.join(P, "slides", sid + ".html")).read()
            s = re.sub(r"<aside>.*?</aside>", "", s, flags=re.S)
            s = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: "file://" + os.path.abspath(bm[m.group(1)]) if m.group(1) in bm else m.group(0), s)
            h = f"<html><head><meta charset='utf-8'><style>body{{margin:0}}{css} section{{width:1920px;height:1080px;overflow:hidden}} .fade-up{{animation:none!important}}</style></head><body>{s}</body></html>"
            t = os.path.join(shots, "_s.html"); open(t, "w").write(h)
            pg = b.new_page(viewport={"width": 1920, "height": 1080}); pg.goto("file://" + t, wait_until="networkidle"); pg.wait_for_timeout(200)
            r = pg.evaluate(JS); pg.screenshot(path=os.path.join(shots, sid + ".png")); pg.close()
            if r:
                bad += 1; print("FAIL", sid); [print("   ", x) for x in r[:6]]
        b.close()
    print("slides:", len(ids or deck["order"]), "com problema:", bad, "· prints em", shots)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
