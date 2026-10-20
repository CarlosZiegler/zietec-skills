# -*- coding: utf-8 -*-
# Forja · baixa fontes do Google Fonts para uso local (medição e screenshots no Chromium sem rede).
# uso: python3 fetch_fonts.py "family=Space+Grotesk:wght@400..700&family=Martian+Mono:wght@400..600" build/fonts
# Gera <pasta>/g.css (original), os woff2 (f0.woff2, f1.woff2, …) e <pasta>/local.css com url() relativas.
# Usa o user-agent de um Chrome atual para receber woff2. Nunca desliga TLS (respeita o proxy/CA do ambiente).
import os, re, sys, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__ or "uso: fetch_fonts.py <query css2> <pasta>")
    query, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    css = get("https://fonts.googleapis.com/css2?" + query.lstrip("?") + ("" if "display=" in query else "&display=swap")).decode()
    open(os.path.join(out, "g.css"), "w").write(css)
    urls, n = {}, 0
    for u in re.findall(r"url\((https://[^)]+\.woff2)\)", css):
        if u not in urls:
            name = f"f{n}.woff2"; n += 1
            open(os.path.join(out, name), "wb").write(get(u))
            urls[u] = name
    local = re.sub(r"url\((https://[^)]+\.woff2)\)", lambda m: "url(" + urls[m.group(1)] + ")", css)
    open(os.path.join(out, "local.css"), "w").write(local)
    print("fontes:", n, "arquivos em", out)


if __name__ == "__main__":
    main()
