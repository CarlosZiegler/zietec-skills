# -*- coding: utf-8 -*-
# Forja · i18n_check: acha T(...) avaliado na carga do módulo (constante de topo como REG = [(..., T(...))]).
# T() lê o idioma corrente quando roda; no topo do módulo ele roda uma vez só, no idioma da importação,
# e as versões EN/DE saem com o texto em PT. Ponha essas listas dentro de uma função (def reg(): return [...]).
# Uso: python3 scripts/i18n_check.py build/*.py   (sai com código 1 se achar)
import ast, sys


def frozen(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    out = []
    for n in tree.body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            if isinstance(n.value, ast.Lambda):   # lambda: [...] só roda quando chamada: ok
                continue
            calls = [c for c in ast.walk(n) if isinstance(c, ast.Call) and getattr(c.func, "id", "") == "T"]
            if calls:
                tgt = n.targets[0] if isinstance(n, ast.Assign) else n.target
                out.append((n.lineno, ast.unparse(tgt), len(calls)))
    return out


if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        for ln, name, k in frozen(f):
            bad += 1
            print(f"FAIL {f}:{ln} {name} tem {k} T() no topo do módulo")
    print("fail:", bad)
    sys.exit(1 if bad else 0)
