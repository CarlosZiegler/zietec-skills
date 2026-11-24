# -*- coding: utf-8 -*-
# Forja · holes_check: acha hole {{ a.b }} em posição de texto cujo valor, no bloco de lógica, é HTML (ex.: um <svg>).
# O runtime escapa todo hole, então esse HTML aparece como código na tela. Ícone por item: renderize os N ícones
# no template e mostre só o da categoria por classe (class="mi ic-{{ x.c }}" + CSS), ou use sc-if por categoria.
# Uso: python3 scripts/holes_check.py project/*.dc.html   (sai com código 1 se houver FAIL)
import re,sys
def check(src):
    out=[]
    body=src.split('data-dc-script')[0]
    # remove atributos para ficar só com holes de texto
    noattr=re.sub(r'="[^"]*"','=""',body)
    keys=set(m.group(1) for m in re.finditer(r'>[^<]*\{\{\s*[\w$]+\.(\w+)\s*\}\}',noattr))
    keys|=set(m.group(1) for m in re.finditer(r'>[^<]*\{\{\s*(\w+)\s*\}\}',noattr))
    logic=src[src.find('data-dc-script'):] if 'data-dc-script' in src else ''
    for k in keys:
        if re.search(r'"%s":\s*"\s*<'%re.escape(k),logic) or re.search(r"\b%s\s*:\s*'<"%re.escape(k),logic):
            out.append(k)
    return out
if __name__=="__main__":
    bad=0
    for f in sys.argv[1:]:
        r=check(open(f).read())
        if r:
            t=re.search(r'<title>([^<]*)',open(f).read()); bad+=1
            print("FAIL",f.split('/')[-1],t.group(1) if t else '',r)
    print("files:",len(sys.argv)-1,"fail:",bad)
    sys.exit(1 if bad else 0)
