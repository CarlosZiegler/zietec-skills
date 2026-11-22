# -*- coding: utf-8 -*-
# Forja · contraste WCAG medido por script.
# uso: python3 contrast.py <pasta build>     → lê PAIRS de <build>/brand.py
#      python3 contrast.py "#151412" "#F3F0E8" [ui]
# Em brand.py, declare PAIRS = [("nome", frente, fundo, "text"|"large"|"ui"), ...].
# Limites: texto 4,5:1; texto grande (≥ 24 px, ou ≥ 18,66 px bold) e UI 3:1.
import os, sys, importlib.util


def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def limit(kind):
    return 3.0 if kind in ("large", "ui") else 4.5


def main():
    a = sys.argv[1:]
    if len(a) >= 2 and a[0].startswith('#'):
        kind = a[2] if len(a) > 2 else "text"
        v = ratio(a[0], a[1]); print(f"{v:.2f}:1", "OK" if v >= limit(kind) else "FALHA"); return
    build = a[0] if a else "."
    spec = importlib.util.spec_from_file_location("brand", os.path.join(build, "brand.py"))
    brand = importlib.util.module_from_spec(spec); sys.path.insert(0, build); spec.loader.exec_module(brand)
    bad = 0
    for name, fg, bg, kind in brand.PAIRS:
        v = ratio(fg, bg); ok = v >= limit(kind); bad += not ok
        print(f"{name:32s} {v:5.2f}:1  {kind:5s} {'OK' if ok else 'FALHA'}")
    print("abaixo do mínimo:", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
