# -*- coding: utf-8 -*-
# Forja · renderizador mínimo de pré-visualização local para .dc.html (holes, sc-for, sc-if) — só para medir e revisar.
# Uso como módulo: from preview import fill, localize, Browser, natural_height, overflow_report
# - fill(html, ctx): preenche holes/sc-for/sc-if com o estado padrão (ctx = Component().renderVals() serializado)
# - localize(html, fonts_dir): troca o <link> do Google Fonts pelo local.css baixado (scripts/fetch_fonts.py)
#   e remove support.js e o bloco de lógica.
# FORJA_FONTS (variável de ambiente) ou o argumento fonts_dir apontam a pasta das fontes (padrão: ./fonts ao lado do build).
import re, os
from playwright.sync_api import sync_playwright

HERE = os.environ.get("FORJA_BUILD", os.getcwd())


def lookup(ctx, path):
    path = path.strip()
    if path in ("true", "false"):
        return path == "true"
    cur = ctx
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part, "")
        else:
            return ""
    return cur


def _match(html, start, tag):
    """Índice do fechamento correspondente (com aninhamento) de <tag ...> que abre em start."""
    depth, pos = 0, start
    op, cl = "<" + tag, "</" + tag + ">"
    while True:
        a = html.find(op, pos)
        b = html.find(cl, pos)
        if b < 0:
            raise ValueError("unclosed " + tag)
        if 0 <= a < b:
            depth += 1; pos = a + len(op)
        else:
            depth -= 1
            if depth == 0:
                return b
            pos = b + len(cl)


def fill(html, ctx):
    out, pos = [], 0
    rx = re.compile(r'<(sc-for|sc-if)\s([^>]*)>')
    while True:
        m = rx.search(html, pos)
        if not m:
            out.append(html[pos:]); break
        out.append(html[pos:m.start()])
        tag, attrs = m.group(1), m.group(2)
        end = _match(html, m.start(), tag)
        body = html[m.end():end]
        if tag == "sc-for":
            lst = lookup(ctx, re.search(r'list="\{\{\s*([^}]+?)\s*\}\}"', attrs).group(1))
            var = re.search(r'as="([^"]+)"', attrs).group(1)
            for k, it in enumerate(lst or []):
                c = dict(ctx); c[var] = it; c["$index"] = k
                out.append(fill(body, c))
        else:
            v = lookup(ctx, re.search(r'value="\{\{\s*([^}]+?)\s*\}\}"', attrs).group(1))
            if v:
                out.append(fill(body, ctx))
        pos = end + len("</" + tag + ">")
    html = "".join(out)

    def rep_hole(m):
        v = lookup(ctx, m.group(1))
        if callable(v) or isinstance(v, dict):
            return ""
        if isinstance(v, bool):
            return "true" if v else "false"
        return str(v)
    html = re.sub(r"\{\{\s*([^}]+?)\s*\}\}", rep_hole, html)
    html = re.sub(r'\sonClick="[^"]*"', "", html)
    return html


def localize(html, fonts_dir=None):
    fonts_dir = fonts_dir or os.environ.get("FORJA_FONTS", os.path.join(HERE, "fonts"))
    local = open(os.path.join(fonts_dir, "local.css")).read()
    local = re.sub(r"url\(([A-Za-z0-9_-]+\.woff2)\)", lambda m: "url(file://" + os.path.join(fonts_dir, m.group(1)) + ")", local)
    html = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^"]*">', "<style>" + local + "</style>", html)
    html = html.replace('<script src="./support.js"></script>', "")
    # remove o bloco de lógica (não roda localmente)
    html = re.sub(r'<script type="text/x-dc".*?</script>', "", html, flags=re.S)
    return html


class Browser:
    def __enter__(self):
        self.p = sync_playwright().start()
        self.b = self.p.chromium.launch()
        return self

    def __exit__(self, *a):
        self.b.close(); self.p.stop()

    def page(self, w, h, reduced=False):
        ctx = self.b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference")
        return ctx.new_page()

    def load(self, html, w, h, reduced=False, wait=200):
        pg = self.page(w, h, reduced)
        os.makedirs(os.path.join(HERE, "verify"), exist_ok=True)
        path = os.path.join(HERE, "verify", "_prev.html")
        open(path, "w").write(html)
        pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(wait)
        return pg


def natural_height(pg):
    return pg.evaluate("""() => {
      const root = document.querySelector('x-dc > div');
      const rt = root.getBoundingClientRect().top; let b = 0;
      for (const c of root.children) { const cs = getComputedStyle(c); if (cs.position === 'absolute' || cs.position === 'fixed') continue; b = Math.max(b, c.getBoundingClientRect().bottom); }
      return b - rt;
    }""")


def overflow_report(pg):
    return pg.evaluate("""() => {
      const root = document.querySelector('x-dc > div'); const rr = root.getBoundingClientRect(); const out = [];
      root.querySelectorAll('*').forEach(e => {
        if (e.ownerSVGElement) return;
        if (e.closest('[style*="overflow-x: auto"]') && e.closest('[style*="overflow-x: auto"]') !== e) return;
        const b = e.getBoundingClientRect(); if (b.width === 0) return;
        if (b.right > rr.right + 1 || b.left < rr.left - 1) out.push(e.tagName + ':' + (e.textContent || '').trim().slice(0, 30) + ' r=' + Math.round(b.right));
      });
      return out.slice(0, 6);
    }""")
