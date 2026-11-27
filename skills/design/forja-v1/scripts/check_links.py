# -*- coding: utf-8 -*-
# Forja · checa links, seletor de idioma, <html lang> e sobras de idioma num project/ trilíngue.
# uso: python3 check_links.py <pasta project> [--screen-base en|de|pt] [--doc-pages build/doc_pages.json]
# Convenção de nomes:
#   telas:  <Base>.dc.html no idioma-base das telas; <Base>-EN/-PT/-DE.dc.html nos outros
#   pitch:  Pitch-NN.dc.html (PT) · Pitch-EN-NN · Pitch-DE-NN
#   doc:    Doc-NN.dc.html (PT) · Doc-EN-NN · Doc-DE-NN
# doc_pages.json (opcional) = {"start": {"pt": {"s01": 3, ...}, "en": {...}, "de": {...}}} — início de cada seção por idioma,
# para conferir que o seletor do doc leva ao início da mesma seção.
import os, re, sys, json

args = sys.argv[1:]
proj = args[0] if args and not args[0].startswith("--") else "."
opt = dict(zip(args[1::2], args[2::2])) if len(args) > 1 else {}
SB = opt.get("--screen-base", "en")
docp = json.load(open(opt["--doc-pages"])) if "--doc-pages" in opt else None
LANGS = ["en", "pt", "de"]
HL = {"en": "en", "pt": "pt-BR", "de": "de"}
WORDS = {  # palavras frequentes que denunciam texto no idioma errado (ajuste para o produto)
    "pt": [r"\bvocê\b", r"\bnão\b", r"\bPágina\b", r"\bpara\b", r"\buma\b", r"\bestá\b", r"ções\b"],
    "de": [r"\bund\b", r"\bnicht\b", r"\bSeite\b", r"\bfür\b", r"\bwerden\b", r"\bdeine?\b"],
    "en": [r"\bthe\b", r"\byour\b", r"\bwith\b", r"\bPage\b", r"\bwhich\b"],
}
files = sorted(f for f in os.listdir(proj) if f.endswith(".dc.html"))
FS = set(files)


def classify(f):
    m = re.fullmatch(r"(Pitch|Doc)-(?:(EN|DE)-)?(\d\d)\.dc\.html", f)
    if m:
        return m.group(1).lower(), (m.group(2) or "PT").lower(), int(m.group(3))
    m = re.fullmatch(r"(Main|[MD]-[A-Za-z0-9]+?)(?:-(EN|PT|DE))?\.dc\.html", f)
    if m:
        return "screen", (m.group(2) or SB.upper()).lower(), m.group(1)
    return None, None, None


def name_for(kind, l, key):
    if kind == "screen":
        return key + ("" if l == SB else "-" + l.upper()) + ".dc.html"
    pre = "Pitch" if kind == "pitch" else "Doc"
    return f"{pre}-{key:02d}.dc.html" if l == "pt" else f"{pre}-{l.upper()}-{key:02d}.dc.html"


def expected(kind, l, key):
    if kind == "doc" and docp:
        st = docp["start"][l]
        sec = [k for k, p in sorted(st.items(), key=lambda kv: kv[1]) if p <= key][-1]
        return {x: name_for("doc", x, docp["start"][x][sec]) for x in LANGS}
    return {x: name_for(kind, x, key) for x in LANGS}


def visible_text(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)


problems, leftovers = [], []
for f in files:
    s = open(os.path.join(proj, f), encoding="utf-8").read()
    kind, l, key = classify(f)
    if not kind:
        problems.append((f, "nome fora da convenção")); continue
    m = re.search(r'<html[^>]*\blang="([^"]+)"', s)
    if m and m.group(1) != HL[l]:
        problems.append((f, f"<html lang> = {m.group(1)}, esperado {HL[l]}"))
    for h in set(re.findall(r'href="([^"#?]+\.dc\.html)', s)):
        if h not in FS:
            problems.append((f, "link quebrado → " + h))
    nav = re.search(r'<nav[^>]*aria-label="Language · Idioma · Sprache"[^>]*>(.*?)</nav>', s, re.S)
    if not nav:
        problems.append((f, "sem seletor EN · PT · DE"))
    else:
        exp = expected(kind, l, key)
        if nav.group(1).count('aria-current="true"') != 1:
            problems.append((f, "seletor sem exatamente 1 aria-current"))
        for x in LANGS:
            if x == l:
                continue
            if f'href="{exp[x]}"' not in nav.group(1):
                problems.append((f, f"seletor {x.upper()} deveria levar a {exp[x]}"))
    if "{{" in re.sub(r"<x-dc>.*?</x-dc>", "", s, flags=re.S):
        problems.append((f, "'{{' fora do template"))
    txt = visible_text(s)
    for other, pats in WORDS.items():
        if other == l:
            continue
        hits = sum(len(re.findall(p, txt)) for p in pats)
        if hits >= 3:
            leftovers.append((f, other, hits))

print("arquivos", len(files), "· problemas", len(problems), "· possíveis sobras de idioma", len(leftovers))
for f, p in problems[:200]:
    print("  ✗", f, p)
for f, o, n in leftovers[:60]:
    print("  ?", f, f"{n} palavras {o.upper()} (revise: pode ser nome próprio ou termo legal)")
sys.exit(1 if problems else 0)
