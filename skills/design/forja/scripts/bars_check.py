# -*- coding: utf-8 -*-
# Forja · bars_check: barra fixa e corte na dobra (gate nascido no Salles V4.1, 323 achados → 0).
# Mede cada prancha no tamanho do print padrão (rolagem no topo) e acusa:
#   sobrepõe barra     texto ou imagem do conteúdo cruzando tab bar, dock, composer, CTA fixo, elemento fixed/sticky ou home indicator
#   cortado embaixo    elemento de conteúdo cortado pela borda de baixo do que se vê (fim da <main> rolável ou da prancha)
#   cortado na lateral (desktop) elemento cortado pela borda direita da prancha
# Elemento de conteúdo = linha de texto, imagem/vídeo, controle (botão, campo, chip, selo) ou caixa com fundo/borda de até 200 px.
# Exceções: camadas (dialog, sheet, scrim, alert, status, [data-sobrepoe]) e listas com data-rolagem="intencional" + data-fade.
# Correção certa (não esconder): a barra ocupa espaço no fluxo; a rolagem termina 8 px acima dela e da área segura (34 px);
# o último item visível termina inteiro (o resto começa abaixo da dobra) e não fica título/autor órfão no fim.
# Uso: python3 scripts/bars_check.py <project|arquivos.dc.html> [--fonts build/fonts] [--blobs blobmap.json] [--only regex] [--json saida.json]
#      sai com código 1 se houver falha.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

JS = r"""() => {
 const root = document.querySelector('x-dc > div'); const RR = root.getBoundingClientRect(); const W = RR.width, H = RR.height; const mob = W <= 430;
 const out = []; const T = 1.5;
 const vis = e => { for (let a = e; a && a !== root; a = a.parentElement) { const cs = getComputedStyle(a); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false; } return true; };
 const isOverlay = e => !!e.closest('[role="dialog"],.sheet,.scrim,[role="alert"],[role="status"],[data-sobrepoe]');
 // barras
 const bars = [];
 for (const e of root.querySelectorAll('*')) {
   if (!vis(e) || isOverlay(e)) continue; const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
   const named = e.matches('.tabbar,.dock,.cdock,.composer,.home-ind');
   const fixed = cs.position === 'fixed' || cs.position === 'sticky';
   const bottomBar = cs.position === 'absolute' && !e.closest('main') && r.bottom - RR.top >= H - 140 && r.top - RR.top >= H * .55 && r.width >= W * .5 && e.parentElement === root;
   if (named || fixed || bottomBar) bars.push(e);
 }
 const inBar = n => bars.some(b => b.contains(n));
 // recorte vertical/lateral visível de um nó
 const clipOf = e => { let L = RR.left, Rt = RR.right, Tp = RR.top, Bt = RR.bottom, edge = 'prancha';
   for (let a = e.parentElement; a && a !== root; a = a.parentElement) { const cs = getComputedStyle(a);
     if (/(hidden|clip|auto|scroll)/.test(cs.overflowY + cs.overflowX)) { const r = a.getBoundingClientRect();
       if (/(auto|scroll)/.test(cs.overflowY) || /(hidden|clip)/.test(cs.overflowY)) { if (r.bottom < Bt) { Bt = r.bottom; edge = a.matches('main') ? 'fim da rolagem' : /(auto|scroll)/.test(cs.overflowY) ? 'rolagem' : 'recorte'; } if (r.top > Tp) Tp = r.top; }
       if (/(auto|scroll|hidden|clip)/.test(cs.overflowX)) { if (r.right < Rt) Rt = r.right; if (r.left > L) L = r.left; } } }
   return {L, Rt, Tp, Bt, edge}; };
 const intencional = e => { const l = e.closest('[data-rolagem="intencional"]'); return !!(l && (l.hasAttribute('data-fade') || l.querySelector('[data-fade]'))); };
 const rectsOf = n => { if (n.nodeType === 3) { const g = document.createRange(); g.selectNodeContents(n); return [...g.getClientRects()].filter(b => b.width > 1 && b.height > 1); } const r = n.getBoundingClientRect(); return r.width && r.height ? [r] : []; };
 const label = n => (n.nodeType === 3 ? n.textContent : (n.getAttribute('alt') || n.getAttribute('aria-label') || n.textContent || n.tagName)).trim().replace(/\s+/g, ' ').slice(0, 50);
 // conteúdo
 const items = [];
 const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let n;
 while ((n = tw.nextNode())) { if (!n.textContent.trim()) continue; const p = n.parentElement; if (!p || p.closest('[aria-hidden="true"],svg,style,script') || !vis(p) || inBar(p) || isOverlay(p)) continue; items.push([n, p, 'texto']); }
 for (const e of root.querySelectorAll('img,video,svg[role="img"],button,input,select,textarea,.btn,.btn2,.chip,.selo,.inp,.ib,*')) {
   if (e.closest('[aria-hidden="true"]') && !e.matches('img') || !vis(e) || inBar(e) || isOverlay(e)) continue;
   const media = e.matches('img,video,svg[role="img"]'); const ctrl = e.matches('button,input,select,textarea,.btn,.btn2,.chip,.selo,.inp,.ib');
   let box = false;
   if (!media && !ctrl) { const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
     box = r.height <= 200 && r.height > 8 && (cs.borderTopWidth !== '0px' && cs.borderTopStyle !== 'none' && cs.borderBottomWidth !== '0px' || (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== getComputedStyle(e.parentElement).backgroundColor)) && !e.matches('main,.r,.sb,.nav,i,hr') && e.parentElement !== root; }
   if (media || ctrl || box) items.push([e, e, media ? 'imagem' : ctrl ? 'controle' : 'caixa']);
 }
 const seen = new Set();
 for (const [nd, el, kind] of items) {
   const c = clipOf(el);
   for (const b of rectsOf(nd)) {
     // parte visível
     const vt = Math.max(b.top, c.Tp), vb = Math.min(b.bottom, c.Bt), vl = Math.max(b.left, c.L), vr = Math.min(b.right, c.Rt);
     if (vb - vt <= T || vr - vl <= T) continue;
     // (a) sobreposição com barra
     if (kind === 'texto' || kind === 'imagem') for (const bar of bars) { if (bar.contains(el) || el.contains(bar)) continue; const q = bar.getBoundingClientRect();
       if (vl < q.right - T && vr > q.left + T && vt < q.bottom - T && vb > q.top + T) { const k = 'a|' + label(nd) + '|' + (bar.className || bar.tagName); if (!seen.has(k)) { seen.add(k); out.push({tipo: 'sobrepõe barra', barra: String(bar.className || bar.tagName).split(' ')[0], item: kind, texto: label(nd), y: Math.round(vt - RR.top)}); } break; } }
     // (b) corte pela borda de baixo
     if (b.top < c.Bt - T && b.bottom > c.Bt + T && c.edge !== 'recorte' && !intencional(el)) { const k = 'b|' + label(nd); if (!seen.has(k)) { seen.add(k); out.push({tipo: 'cortado embaixo', borda: c.edge, item: kind, texto: label(nd), y: Math.round(c.Bt - RR.top)}); } }
     if (!mob && b.left < c.Rt - T && b.right > c.Rt + T && c.edge !== 'recorte' && !intencional(el) && Math.abs(c.Rt - RR.right) < 2) { const k = 'c|' + label(nd); if (!seen.has(k)) { seen.add(k); out.push({tipo: 'cortado na lateral', item: kind, texto: label(nd)}); } }
     break;
   }
 }
 return out;
}"""


def main():
    files, opt = C.parse(sys.argv[1:])
    res = C.run(files, opt, JS)
    fal = [dict(x, prancha=os.path.basename(f)) for f, o in res.items() for x in (o or [])]
    for f, o in res.items():
        if o:
            print("FAIL", os.path.basename(f))
            for x in o[:6]:
                print("   ", x["tipo"], "|", x.get("barra", x.get("borda", "")), "|", x["texto"])
    if opt["json"]:
        json.dump({"pranchas": len(files), "falhas": fal}, open(opt["json"], "w"), ensure_ascii=False, indent=1)
    print("pranchas:", len(files), "com falha:", sum(1 for o in res.values() if o), "falhas:", len(fal))
    sys.exit(1 if fal else 0)


if __name__ == "__main__":
    main()
