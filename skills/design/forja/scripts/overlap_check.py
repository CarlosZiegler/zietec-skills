# -*- coding: utf-8 -*-
# Forja · overlap_check: acha sobreposição que o overflow não pega (nada sai do artboard, mas algo cobre outra coisa).
# Renderiza cada artboard no preview local (holes preenchidos com renderVals() e escapados, como no runtime) e acusa:
#   texto-sobre-texto   caixas de nós de texto visíveis que se cruzam (> 2 px nos dois eixos), fora de ancestral comum direto
#   controle-sobre-texto botão, link, campo ou switch cobrindo texto que não é dele
#   absoluto-com-lista  elemento position:absolute (ou fixed) que contém <table>, <ul> ou <ol>
# Ficam de fora as sobreposições intencionais conhecidas: decorativo (aria-hidden, data-skip), vitrine Stageshow (.stg,
# .phwrap, moldura do celular no pitch), badge/contador (.badge, .n, .tapn, .dot), knob dentro do switch, e camadas de
# sobreposição (sheet, diálogo, toast, dock, tab bar, topo de vidro) contra o que fica por trás delas.
# Uso: python3 scripts/overlap_check.py project/*.dc.html [--fonts <pasta com local.css>] [--max 4]
#      sai com código 1 se houver FAIL. Precisa de node (renderVals) e playwright (chromium).
import os, re, sys, json, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preview as P

CTX_JS = r"""
const fs = require('fs');
const s = fs.readFileSync(process.argv[1], 'utf8');
const m = s.match(/<script type="text\/x-dc" data-dc-script data-props='([^']*)'>([\s\S]*?)<\/script>/);
if (!m) { process.stdout.write('{}'); process.exit(0); }
class DCLogic { constructor() { this.props = {}; this.state = undefined; } setState(o) { this.state = Object.assign({}, this.state || {}, o); } forceUpdate() {} }
let v = {};
try { const C = eval('(function(){' + m[2] + '; return Component; })()'); v = new C().renderVals(); } catch (e) { v = {}; }
process.stdout.write(JSON.stringify(v, (k, x) => typeof x === 'function' ? undefined : x));
"""

JS = r"""(maxOut) => {
  const root = document.querySelector('x-dc > div') || document.body;
  const SKIP = '[aria-hidden="true"],[data-skip],.stg,.phwrap,.phone,.badge,.tapn,.n,.dot,.knob,svg defs,.sr,.sr-only';
  const LAYER = '[role="dialog"],[role="menu"],[role="listbox"],[role="tooltip"],.sheet,.dlg,.sysdlg,.toast,.dock,.tabbar,.topbar,.tbar,.nwrap,.scrim,.scrim2,.edge,.menu,.popover,.sidep,.drawer';
  // texto cortado por overflow (ellipsis, máscara) conta só a parte visível
  const clipOf = (el) => { let c = null; for (let p = el; p && p !== root; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { const b = p.getBoundingClientRect(); c = c ? {l: Math.max(c.l, b.left), r: Math.min(c.r, b.right), t: Math.max(c.t, b.top), b: Math.min(c.b, b.bottom)} : {l: b.left, r: b.right, t: b.top, b: b.bottom}; } } return c; };
  const vis = (el) => { for (let e = el; e && e !== document.body; e = e.parentElement) { const cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false; } return true; };
  const layerOf = (el) => { const l = el.closest(LAYER); return l || null; };
  const desc = (el) => (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : el.tagName.toLowerCase());
  // nós de texto visíveis
  const texts = [];
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let n; while ((n = tw.nextNode())) {
    const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue;
    const el = n.parentElement; if (!el || el.closest(SKIP) || !vis(el)) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const cl = clipOf(el);
    for (const b0 of r.getClientRects()) {
      const b = cl ? {left: Math.max(b0.left, cl.l), right: Math.min(b0.right, cl.r), top: Math.max(b0.top, cl.t), bottom: Math.min(b0.bottom, cl.b)} : b0;
      const bw = b.right - b.left, bh = b.bottom - b.top; if (bw < 2 || bh < 2) continue;
      const pad = (b0.bottom - b0.top) * 0.18;   // caixa do glifo, não a da entrelinha
      texts.push({el, node: n, t: t.slice(0, 28), x1: b.left, x2: b.right, y1: b.top + pad, y2: b.bottom - pad}); }
  }
  const hit = (a, b) => Math.min(a.x2, b.x2) - Math.max(a.x1, b.x1) > 2 && Math.min(a.y2, b.y2) - Math.max(a.y1, b.y1) > 2;
  const out = [];
  const related = (a, b) => a === b || a.contains(b) || b.contains(a);
  for (let i = 0; i < texts.length && out.length < maxOut; i++) for (let j = i + 1; j < texts.length && out.length < maxOut; j++) {
    const A = texts[i], B = texts[j]; if (A.node === B.node || related(A.el, B.el) || !hit(A, B)) continue;
    const la = layerOf(A.el), lb = layerOf(B.el); if (la !== lb && (la || lb)) continue;   // camada de sobreposição sobre o fundo: intencional
    out.push('texto-sobre-texto: "' + A.t + '" × "' + B.t + '" (' + desc(A.el) + ' / ' + desc(B.el) + ')');
  }
  // controle sobre texto
  const ctrls = [...root.querySelectorAll('button, a[href], input, select, textarea, [role="switch"], [role="radio"], [role="checkbox"]')]
    .filter(c => !c.closest(SKIP) && vis(c));
  for (const c of ctrls) { if (out.length >= maxOut) break;
    const b = c.getBoundingClientRect(); if (b.width < 2) continue;
    const box = {x1: b.left, x2: b.right, y1: b.top, y2: b.bottom};
    for (const T of texts) { if (c.contains(T.el) || T.el.contains(c) || T.el.closest('label') && T.el.closest('label').contains(c)) continue;
      const lc = layerOf(c), lt = layerOf(T.el); if (lc !== lt && (lc || lt)) continue;
      if (hit(box, T)) { out.push('controle-sobre-texto: ' + desc(c) + ' cobre "' + T.t + '"'); break; } }
  }
  // absoluto com tabela ou lista que cobre texto de fora dele (a moldura de página que não cobre nada passa)
  for (const e of root.querySelectorAll('*')) { if (out.length >= maxOut) break;
    if (e.closest(SKIP) || e.closest(LAYER)) continue; const cs = getComputedStyle(e);
    if (cs.position !== 'absolute' && cs.position !== 'fixed') continue;
    const lst = e.matches('table, ul, ol') ? e : e.querySelector('table, ul, ol'); if (!lst || !vis(e)) continue;
    const b = e.getBoundingClientRect(); const box = {x1: b.left, x2: b.right, y1: b.top, y2: b.bottom};
    const under = texts.find(T => !e.contains(T.el) && !T.el.contains(e) && !layerOf(T.el) && hit(box, T));
    if (under) out.push('absoluto-com-lista: ' + desc(e) + ' (' + cs.position + ', ' + lst.tagName.toLowerCase() + ') cobre "' + under.t + '"');
  }
  return out;
}"""


def size_of(raw):
    m = re.search(r'"\$preview": ?\{"width": ?(\d+), ?"height": ?(\d+)\}', raw)
    return (int(m.group(1)), int(m.group(2))) if m else (1440, 1024)


def ctx_of(path, js_file):
    r = subprocess.run(["node", js_file, path], capture_output=True, text=True)
    try:
        return json.loads(r.stdout or "{}")
    except ValueError:
        return {}


def prev(path, js_file, fonts):
    raw = open(path).read()
    m = re.search(r"<x-dc>(.*)</x-dc>", raw, re.S)
    html = raw[:m.start(1)] + P.fill(m.group(1), ctx_of(path, js_file)) + raw[m.end(1):]
    if fonts and os.path.exists(os.path.join(fonts, "local.css")):
        html = P.localize(html, fonts)
    else:
        html = html.replace('<script src="./support.js"></script>', "")
        html = re.sub(r'<script type="text/x-dc".*?</script>', "", html, flags=re.S)
    img = os.path.abspath(os.path.join(os.path.dirname(path), "img"))
    html = html.replace('src="./img/', 'src="file://' + img + "/").replace("<helmet>", "").replace("</helmet>", "")
    return html


def main():
    args = sys.argv[1:]
    fonts = os.environ.get("FORJA_FONTS")
    mx = 4
    if "--fonts" in args:
        i = args.index("--fonts"); fonts = args[i + 1]; del args[i:i + 2]
    if "--max" in args:
        i = args.index("--max"); mx = int(args[i + 1]); del args[i:i + 2]
    files = [f for f in args if f.endswith(".dc.html")]
    js_file = os.path.join(tempfile.gettempdir(), "forja_overlap_ctx.js")
    open(js_file, "w").write(CTX_JS)
    bad = 0
    tmp = os.path.join(tempfile.gettempdir(), "forja_overlap_prev.html")
    with P.Browser() as br:
        for f in files:
            w, h = size_of(open(f).read())
            pg = br.page(w, h, reduced=True)
            open(tmp, "w").write(prev(f, js_file, fonts))
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(60)
            o = pg.evaluate(JS, mx); pg.context.close()
            if o:
                bad += 1
                print("FAIL", os.path.basename(f))
                for x in o:
                    print("   ", x)
    print("files:", len(files), "fail:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
