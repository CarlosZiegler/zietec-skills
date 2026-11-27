# -*- coding: utf-8 -*-
# Forja · prints: fotografa todas as pranchas (2x, sem margem, estado final com movimento reduzido) e mantém
# prints/index.json com ids ESTÁVEIS: quem já estava no índice (mesmo canvas/arquivo) mantém o id, mesmo que a tela mude;
# tela nova ganha id novo pelo título. Deck, doc e landing apontam para o id, nunca para o nome do arquivo.
# Mobile com rolagem ganha também a versão longa em prints/<canvas>/longas/ (campo "longa").
# Entradas: id, uid (canvas/arquivo), arquivo, titulo, superficie, pagina, tamanho, novo, longa.
# Uso: python3 scripts/prints.py <canvas>=<pasta project> [...] [--out prints] [--fonts build/fonts] [--blobs blobmap.json] [--only regex]
#      ex.: prints.py app=app/project painel=painel/project --out prints
import os, re, sys, json, tempfile, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import overlap_check as O

LONG_JS = """() => { const r = document.querySelector('x-dc > div'); const m = r.querySelector('main.scr') || r.querySelector('main');
  if (!m) return 0; const extra = Math.max(0, m.scrollHeight - m.clientHeight); if (!extra) return 0;
  r.style.height = (r.getBoundingClientRect().height + extra) + 'px'; m.style.overflow = 'visible'; m.style.maxHeight = 'none'; m.style.height = m.scrollHeight + 'px';
  return extra; }"""


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "tela"


def main():
    a = sys.argv[1:]
    out = "prints"
    if "--out" in a:
        i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    pairs = [x.split("=", 1) for x in a if "=" in x and not x.startswith("--")]
    _, opt = C.parse([x for x in a if "=" not in x])
    idx_path = os.path.join(out, "index.json")
    old = {e["uid"] if "uid" in e else e["arquivo"]: e for e in (json.load(open(idx_path)) if os.path.exists(idx_path) else [])}
    used = {e["id"] for e in old.values()}
    index = [e for e in old.values() if e.get("canvas") not in {c for c, _ in pairs}]
    tmp = os.path.join(tempfile.gettempdir(), "forja_print.html")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for cv, proj in pairs:
            os.makedirs(os.path.join(out, cv, "longas"), exist_ok=True)
            cj = os.path.join(proj, "canvas.json"); c = json.load(open(cj)) if os.path.exists(cj) else {}
            order = c.get("order") or sorted(f for f in os.listdir(proj) if f.endswith(".dc.html"))
            pages = {x["id"]: x["name"] for x in c.get("pages", [])}
            for f in order:
                if not re.search(opt["only"], f):
                    continue
                path = os.path.join(proj, f); bd = c.get("boards", {}).get(f, {})
                w, h = (bd["w"], bd["h"]) if "w" in bd else O.size_of(open(path).read())
                titulo = bd.get("name") or f[:-8]; uid = cv + "/" + f[:-8] + ".png"
                e = old.get(uid) or old.get(cv + "/" + f[:-8] + ".png")
                if e:
                    pid = e["id"]
                else:
                    pid = slug(titulo); k = 2
                    while pid in used:
                        pid = f"{slug(titulo)}-{k}"; k += 1
                    used.add(pid)
                open(tmp, "w").write(C.html_of(path, opt))
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, reduced_motion="reduce"); pg = ctx.new_page()
                pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
                png = os.path.join(out, cv, f[:-8] + ".png")
                pg.screenshot(path=png, clip={"x": 0, "y": 0, "width": w, "height": h})
                longa = None
                if w <= 430:
                    extra = pg.evaluate(LONG_JS)
                    if extra:
                        longa = os.path.join(cv, "longas", f[:-8] + ".png")
                        pg.screenshot(path=os.path.join(out, longa), clip={"x": 0, "y": 0, "width": w, "height": h + extra})
                ctx.close()
                index.append({"id": pid, "uid": uid, "canvas": cv, "arquivo": os.path.join(cv, f[:-8] + ".png"), "titulo": titulo,
                              "superficie": "mobile" if w <= 430 else "tablet" if w < 1100 else "desktop",
                              "pagina": pages.get(bd.get("page"), bd.get("page", "")), "tamanho": [w, h], "novo": not e, "longa": longa})
                print(pid, "←", f)
        b.close()
    json.dump(index, open(idx_path, "w"), ensure_ascii=False, indent=1)
    print("prints:", len(index), "· novos:", sum(1 for e in index if e.get("novo")))


if __name__ == "__main__":
    main()
