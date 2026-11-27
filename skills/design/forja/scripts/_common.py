# -*- coding: utf-8 -*-
# Forja · base comum dos gates por prancha: lista os .dc.html, monta a pré-visualização (holes preenchidos e escapados,
# fontes locais, /_blob/<id> trocado pelo arquivo local quando há --blobs) e roda um JS de medição em cada prancha.
import os, re, sys, json, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preview as P
import overlap_check as O


def parse(argv):
    """Devolve (arquivos, opções). Aceita pastas de projeto ou arquivos .dc.html; --fonts, --blobs, --json, --only <regex>."""
    a = list(argv); opt = {"fonts": os.environ.get("FORJA_FONTS"), "blobs": None, "json": None, "only": "."}
    for k in ("fonts", "blobs", "json", "only"):
        if "--" + k in a:
            i = a.index("--" + k); opt[k] = a[i + 1]; del a[i:i + 2]
    files = []
    for x in a:
        if os.path.isdir(x):
            files += sorted(os.path.join(x, f) for f in os.listdir(x) if f.endswith(".dc.html"))
        elif x.endswith(".dc.html"):
            files.append(x)
    files = [f for f in files if re.search(opt["only"], os.path.basename(f))]
    return files, opt


def html_of(path, opt):
    js = os.path.join(tempfile.gettempdir(), "forja_ctx.js")
    if not os.path.exists(js):
        open(js, "w").write(O.CTX_JS)
    html = O.prev(path, js, opt["fonts"])
    if opt["blobs"]:
        bm = json.load(open(opt["blobs"]))
        html = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: "file://" + os.path.abspath(bm[m.group(1)]) if m.group(1) in bm else m.group(0), html)
    return html


def run(files, opt, js, arg=None, scale=1, wait=150):
    """Roda js em cada prancha; devolve {arquivo: resultado}."""
    out = {}
    tmp = os.path.join(tempfile.gettempdir(), "forja_gate_prev.html")
    with P.Browser() as br:
        for f in files:
            w, h = O.size_of(open(f).read())
            ctx = br.b.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale, reduced_motion="reduce")
            pg = ctx.new_page(); open(tmp, "w").write(html_of(f, opt))
            pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(wait)
            out[f] = pg.evaluate(js, arg) if arg is not None else pg.evaluate(js); ctx.close()
    return out
