# -*- coding: utf-8 -*-
# Forja · parity_check: nenhuma versão nova perde conteúdo da anterior (regra nascida no Salles V4: "não quero a cada
# versão perder conteúdos"). Cada prancha das versões antigas precisa de um destino declarado na nova.
#
# 1ª rodada (sem --map ou com mapa inexistente): monta o inventário das pastas antigas e grava um rascunho do mapa,
#    casando pelo nome do arquivo (igual, ou igual trocando o número da versão: V3 → V4); o resto sai como "faltando".
# Rodadas seguintes: valida o mapa. Falha se uma prancha antiga não estiver no mapa, se o status não for um dos válidos,
#    se "equivalente"/"trazida de volta"/"mantida" apontar para prancha que não existe na nova, se "descontinuada" não
#    tiver motivo, ou se houver qualquer "faltando".
#
# Status válidos: mantida · trazida de volta · equivalente · incorporada na doc · mudou de canvas · descontinuada (motivo
#   obrigatório, decisão do usuário ou registrada) · fora do canvas · em aberto (pergunta para o usuário) · faltando.
# O mapa vira página "Paridade <antiga> → <nova>" no canvas Produto (tabela com link de cada prancha) e resumo no deck.
#
# Uso: python3 scripts/parity_check.py --old <proj_v2> <proj_v3> ... --new <proj_v4> ... --map state/paridade.json
import os, re, sys, json

OK = ["mantida", "trazida de volta", "equivalente", "incorporada na doc", "mudou de canvas", "descontinuada",
      "fora do canvas", "em aberto", "faltando"]
PRECISA_DESTINO = ("mantida", "trazida de volta", "equivalente", "mudou de canvas")


def boards(dirs):
    out = {}
    for d in dirs:
        tag = os.path.basename(os.path.dirname(os.path.abspath(d))) or d
        cj = os.path.join(d, "canvas.json")
        names = {}
        if os.path.exists(cj):
            c = json.load(open(cj))
            for f, b in c.get("boards", {}).items():
                names[f] = b.get("name") or b.get("title") or f
        for f in sorted(os.listdir(d)):
            if f.endswith(".dc.html"):
                raw = open(os.path.join(d, f)).read()
                t = re.search(r"<title>(.*?)</title>", raw)
                out[tag + "/" + f[:-8]] = {"origem": tag, "arquivo": f[:-8], "titulo": names.get(f) or (t.group(1) if t else f[:-8])}
    return out


def norm(n):
    return re.sub(r"(?i)\bv\d+\b|-v\d+-|v\d+", "V#", n)


def main():
    a = sys.argv[1:]
    def take(flag):
        if flag not in a:
            return []
        i = a.index(flag); j = i + 1
        while j < len(a) and not a[j].startswith("--"):
            j += 1
        v = a[i + 1:j]; del a[i:j]; return v
    old, new, mp = take("--old"), take("--new"), (take("--map") or ["state/paridade.json"])[0]
    O, N = boards(old), boards(new)
    nfiles = {v["arquivo"] for v in N.values()}
    nnorm = {norm(v["arquivo"]): v["arquivo"] for v in N.values()}
    if not os.path.exists(mp):
        rows = []
        for k, v in O.items():
            dst = v["arquivo"] if v["arquivo"] in nfiles else nnorm.get(norm(v["arquivo"]), "")
            rows.append(dict(v, chave=k, nova=dst, status="mantida" if dst else "faltando", motivo=""))
        os.makedirs(os.path.dirname(mp) or ".", exist_ok=True)
        json.dump(rows, open(mp, "w"), ensure_ascii=False, indent=1)
        f = sum(r["status"] == "faltando" for r in rows)
        print(f"rascunho gravado em {mp}: {len(rows)} pranchas antigas, {f} sem destino. Classifique cada 'faltando' e rode de novo.")
        sys.exit(1)
    rows = json.load(open(mp)); por = {r.get("chave") or (r.get("origem", "") + "/" + r.get("arquivo", r.get("antiga", ""))): r for r in rows}
    erros, cont = [], {}
    for k, v in O.items():
        r = por.get(k)
        if not r:
            erros.append(f"sem destino: {k} ({v['titulo']})"); continue
    for r in rows:
        st = (r.get("status") or "").split(" (")[0].strip()
        cont[st] = cont.get(st, 0) + 1
        nome = r.get("chave") or r.get("arquivo") or r.get("antiga")
        if st not in OK:
            erros.append(f"status inválido '{r.get('status')}': {nome}")
        if st in PRECISA_DESTINO and new and (r.get("nova") or r.get("v4")) not in nfiles:
            erros.append(f"destino não existe na nova ({r.get('nova') or r.get('v4')}): {nome}")
        if st == "descontinuada" and not (r.get("motivo") or "(" in (r.get("status") or "")):
            erros.append(f"descontinuada sem motivo: {nome}")
        if st == "faltando":
            erros.append(f"faltando: {nome}")
    for s in OK:
        if cont.get(s):
            print(f"  {s}: {cont[s]}")
    for e in erros[:40]:
        print("FAIL", e)
    print("pranchas antigas:", len(O) or len(rows), "· problemas:", len(erros))
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
