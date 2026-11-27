# -*- coding: utf-8 -*-
# Forja · trunc_check: texto cortado (gate nascido no Salles V4, 27 achados → 0: reticências na lista "Depois", chips e
# carrosséis cortados, código Pix, rótulos Antes/Depois sob o divisor, pílula "Semana 2 de 4" colada no topo).
# Acusa, em elementos com overflow hidden/clip, text-overflow: ellipsis ou line-clamp:
#   largura            texto mais largo que a caixa
#   altura             texto com reticências/line-clamp que não cabe
#   sai do recorte     linha de texto que passa da borda do ancestral que recorta (cartão, pílula, nó de fluxo)
# Ignora a rolagem natural da tela (raiz, <main class="scr">, .scr, .r e a moldura [data-viewport]).
# Reticências por desenho não são desculpa: se o texto real não cabe, a caixa cresce, quebra linha ou o texto encurta.
# Uso: python3 scripts/trunc_check.py <project|arquivos.dc.html> [--fonts build/fonts] [--blobs blobmap.json] [--only regex]
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

JS = r"""() => {
 const root = document.querySelector('x-dc > div'); const out = new Set();
 const skipAnc = e => e === root || e.matches('main.scr, .scr, .r, [data-viewport], x-dc, body, html');
 const clips = e => { const cs = getComputedStyle(e); return /(hidden|clip)/.test(cs.overflowX + cs.overflowY) };
 for (const e of root.querySelectorAll('*')) {
   const cs = getComputedStyle(e); if (!e.textContent.trim() || e.closest('[aria-hidden="true"],svg')) continue;
   const r = e.getBoundingClientRect(); if (!r.width || cs.visibility === 'hidden') continue;
   const ell = cs.textOverflow === 'ellipsis' || cs.webkitLineClamp !== 'none' && cs.webkitLineClamp !== '';
   if ((ell || clips(e)) && !skipAnc(e) && !e.matches('img,video,input')) {
     if (e.scrollWidth > e.clientWidth + 1 && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) out.add('largura: ' + e.textContent.trim().slice(0, 40));
     if (ell && e.scrollHeight > e.clientHeight + 1) out.add('altura: ' + e.textContent.trim().slice(0, 40));
   }
 }
 const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n;
 while ((n = w.nextNode())) { const t = n.textContent.trim(); if (!t) continue; const p = n.parentElement; if (!p || p.closest('[aria-hidden="true"],svg')) continue;
   const cs = getComputedStyle(p); if (cs.visibility === 'hidden' || cs.textOverflow === 'ellipsis') continue;
   let a = p; while (a && a !== root && !(clips(a) && !skipAnc(a))) a = a.parentElement; if (!a || a === root) continue;
   const A = a.getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(n);
   for (const b of rg.getClientRects()) { if (!b.width) continue; if (b.right > A.right + 1.5 || b.left < A.left - 1.5 || b.bottom > A.bottom + 1.5) { out.add('sai do recorte (' + (a.className || a.tagName) + '): ' + t.slice(0, 40)); break; } } }
 return [...out];
}"""


def main():
    files, opt = C.parse(sys.argv[1:])
    res = C.run(files, opt, JS)
    bad = 0
    for f, o in res.items():
        if o:
            bad += 1; print("CORTE", os.path.basename(f), "|", " ; ".join(o[:4]))
    print("pranchas:", len(files), "com corte:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
