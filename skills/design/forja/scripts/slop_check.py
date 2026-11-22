#!/usr/bin/env python3
"""Forja · passe anti-slop: contagens objetivas sobre os artboards (.dc.html).

Uso:
  python3 slop_check.py <pasta project/> [--radii 4,8,12,16,999] [--max-hues 3]
                        [--allow-gradient arquivo.dc.html ...] [--only M-,D-] [--json saida.json]

Sai com código 1 se houver FAIL. Cada achado traz id, arquivo e exemplo, para corrigir
pela regra e não "deixar mais bonito".

Origem das regras (adaptadas, não copiadas):
- contagens rápidas e contrato de design: uizze anti-ui-slop (Apache-2.0) e o guia AI UI Slop;
- palavras e frases de slop em inglês: taste-skill copy-lint (MIT, © 2026 Leonxlnx);
- tipografia, foco, formulários, imagens e animação: Vercel Web Interface Guidelines (MIT);
- listas PT e DE: Forja.
"""
import argparse, colorsys, glob, html, json, os, re, sys
from collections import Counter, defaultdict

# ---------- listas de copy ----------
SLOP_EN = ['delve', 'tapestry', 'testament to', 'realm', 'embark', 'beacon', 'multifaceted', 'paradigm',
           'myriad', 'plethora', 'meticulous', 'intricate', 'elevate', 'unlock', 'unleash', 'empower',
           'harness', 'supercharge', 'seamless', 'seamlessly', 'effortless', 'effortlessly', 'cutting-edge',
           'revolutionary', 'revolutionize', 'transformative', 'holistic', 'next-level', 'world-class',
           'best-in-class', 'game-changer', 'game-changing', 'state-of-the-art', 'bespoke', 'synergy',
           'leverage', 'reimagine', 'next-generation', 'robust', 'unparalleled']
SLOP_PT = ['revolucionári', 'revolucione', 'potencialize', 'alavanque', 'desbloqueie', 'eleve sua', 'eleve o seu',
           'inovador', 'inovadora', 'disruptiv', 'tecnologia de ponta', 'solução de ponta', 'sem complicação', 'sem complicações',
           'solução completa', 'experiência única', 'próximo nível', 'jornada incrível', 'transforme sua',
           'transforme seu', 'simples e rápid', 'de forma simples', 'tudo em um só lugar', 'sinergia',
           'holístic', 'robusto', 'robusta', 'perfeito para você']
SLOP_DE = ['nahtlos', 'revolutionär', 'revolutioniert', 'innovativ', 'maßgeschneidert', 'ganzheitlich',
           'nächste level', 'nächsten level', 'spielend leicht', 'aus einer hand', 'entfessle', 'synergie',
           'bahnbrechend', 'einzigartiges erlebnis', 'alles an einem ort', 'mühelos']
STOCK = [r"in today'?s (fast-paced|digital|modern|ever-changing|busy)", r'unlock the (power|potential)',
         r'harness the power', r'the future of \w+ is (here|now)', r'say goodbye to', r"whether you'?re an? ",
         r'look no further', r'join (thousands|millions|hundreds) of', r'imagine a world',
         r'ready to (transform|take your|elevate|level up)', r'one-stop shop', r'take (it|your \w+) to the next level',
         r"\b(it'?s|this is) not just (a|an|another)\b", r'\bnot only\b[^.!?]{1,60}\bbut also\b',
         r'\bat your fingertips\b', r'\b\w+ made (simple|easy)\b', r'\bwe.?ve got you covered\b',
         r'não é só (um|uma|mais)', r'chegou a hora de', r'diga adeus', r'na palma da sua mão',
         r'imagine (um|uma) (mundo|vida)', r'mais do que (um|uma) (app|aplicativo|ferramenta)',
         r'nicht nur (ein|eine)\b', r'sag (auf wiedersehen|tschüss) zu', r'stell dir (eine welt|vor, du)']
RESIDUE = [r'lorem ipsum', r'\[(your|seu|sua|dein)[^\]]*\]', r'\bTODO\b', r'\bTBD\b', r'\bcertainly!', r'as an ai',
           r'\[insert', r'placeholder text', r'texto de exemplo']

EMOJI = re.compile('[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF⭐⬆↔-↪]')
HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
RGB = re.compile(r'rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)')


def strip_code(src):
    s = re.sub(r'<script\b.*?</script>', ' ', src, flags=re.S | re.I)
    s = re.sub(r'<style\b.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<svg\b.*?</svg>', ' ', s, flags=re.S | re.I)
    return s


def visible_text(src):
    s = strip_code(src)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\{\{[^}]*\}\}', ' ', s)
    return html.unescape(re.sub(r'\s+', ' ', s))


def hexrgb(h):
    h = h.lower()
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hue_of(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return h * 360, l, s


def colors_in(src):
    out = [hexrgb(m.group(1)) for m in HEX.finditer(src)]
    out += [tuple(int(x) / 255 for x in m.groups()) for m in RGB.finditer(src)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('project')
    ap.add_argument('--radii', default='', help='escala de raios em px, ex.: 4,8,12,16,999')
    ap.add_argument('--max-hues', type=int, default=4, help='matizes saturados aceitos: acento + 1 apoio de marca + erro + ok')
    ap.add_argument('--allow-gradient', nargs='*', default=[])
    ap.add_argument('--only', default='', help='prefixos de arquivo separados por vírgula (ex.: M-,D-,Main)')
    ap.add_argument('--json', default='')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.project, '*.dc.html')))
    if a.only:
        pre = tuple(p.strip() for p in a.only.split(',') if p.strip())
        files = [f for f in files if os.path.basename(f).startswith(pre)]
    radii = {float(x) for x in a.radii.split(',') if x.strip()}

    finds = []  # (nivel, id, arquivo, exemplo)
    hues = Counter()
    hue_ex = {}
    labels_by_href = defaultdict(set)

    def add(level, fid, f, ex):
        finds.append((level, fid, os.path.basename(f), ex[:140]))

    for f in files:
        src = open(f, encoding='utf-8').read()
        low = src.lower()
        text = visible_text(src)
        tlow = text.lower()

        # cor: matizes saturados (acento único + semânticos)
        for rgb in colors_in(src):
            h, l, s = hue_of(rgb)
            if s > 0.35 and 0.18 < l < 0.82:
                b = int(h // 20) * 20
                hues[b] += 1
                hue_ex.setdefault(b, '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb))
                if 235 <= h <= 295 and s > 0.3:
                    add('WARN', 'cor-violeta', f, hue_ex[b] + ' (índigo, violeta ou lavanda só com motivo de marca)')

        # gradientes, vidro
        # só gradiente "de lavagem" conta: repeating-* e paradas duras (réguas, pautas, máscaras) são desenho
        ng = 0
        for m in re.finditer(r'(?<!repeating-)(linear|radial|conic)-gradient\(([^;"]{0,200})', low):
            stops = re.findall(r'(\d+(?:\.\d+)?%)', m.group(2))
            cols = re.findall(r'#[0-9a-f]{3,8}\b|rgba?\([^)]*\)|transparent', m.group(2))
            if len(stops) != len(set(stops)) or len(set(cols)) <= 1:
                continue  # parada dura ou cor chapada
            ng += 1
        if ng and os.path.basename(f) not in a.allow_gradient:
            add('WARN', 'gradiente', f, f'{ng} gradiente(s) de lavagem: mantenha só com motivo de marca escrito no design_brief')
        nb = low.count('backdrop-filter')
        if nb > 1:
            add('WARN', 'vidro', f, f'{nb} backdrop-filter: vidro só na superfície rara que precisa')

        # raios fora da escala
        if radii:
            for m in re.finditer(r'border-radius\s*:\s*([0-9.]+)px', low):
                v = float(m.group(1))
                if v not in radii and v < 999:
                    add('FAIL', 'raio-fora-da-escala', f, f'{v:g}px (escala: {a.radii})')

        # emoji em navegação, botões e títulos
        for tag in ('button', 'a', 'nav', 'h1', 'h2', 'h3', 'h4', 'label'):
            for m in re.finditer(rf'<{tag}\b[^>]*>(.*?)</{tag}>', src, flags=re.S | re.I):
                inner = re.sub(r'<[^>]+>', '', strip_code(m.group(1)))
                if EMOJI.search(inner):
                    add('FAIL', 'emoji-como-icone', f, f'<{tag}> {inner.strip()}')

        # rótulos diferentes para o mesmo destino
        for m in re.finditer(r'<a\b[^>]*href="([^"#][^"]*)"[^>]*>(.*?)</a>', src, flags=re.S | re.I):
            lbl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', strip_code(m.group(2)))).strip()
            if lbl and len(lbl) < 40 and not re.fullmatch(r'(EN|PT|DE)', lbl):
                labels_by_href[m.group(1)].add(lbl)

        # tipografia (Vercel)
        for m in re.finditer(r'\w\.\.\.(?!\w)', text):
            add('FAIL', 'reticencias', f, text[max(0, m.start() - 30):m.end() + 5] + '  → use …')
        sq = re.findall(r'(?<![=\w])"[^"<>{}]{3,60}"', text)
        if sq:
            add('WARN', 'aspas-retas', f, sq[0] + '  → “ ” (PT/EN) ou „ “ (DE)')
        if re.search(r'<(table|th)\b', low) and 'tabular-nums' not in low:
            add('WARN', 'tabular-nums', f, 'tabela sem font-variant-numeric: tabular-nums')

        # foco, animação, imagens, formulários (Vercel)
        if re.search(r'transition\s*:\s*all\b', low):
            add('FAIL', 'transition-all', f, 'transition: all → liste as propriedades')
        if re.search(r'outline\s*:\s*(none|0)\b', low) and 'focus-visible' not in low:
            add('FAIL', 'foco-removido', f, 'outline removido sem :focus-visible substituto')
        if 'user-scalable=no' in low or 'maximum-scale=1' in low:
            add('FAIL', 'zoom-bloqueado', f, 'viewport bloqueia zoom')
        for m in re.finditer(r'<img\b[^>]*>', src, flags=re.I):
            t = m.group(0).lower()
            if 'alt=' not in t:
                add('FAIL', 'img-sem-alt', f, m.group(0))
            if not ('width=' in t or 'width:' in t) or not ('height=' in t or 'height:' in t or 'aspect-ratio' in t):
                add('WARN', 'img-sem-dimensao', f, m.group(0))
        for m in re.finditer(r'<button\b([^>]*)>(.*?)</button>', src, flags=re.S | re.I):
            attrs, inner = m.group(1).lower(), m.group(2)
            if not re.sub(r'<[^>]+>|\s|\{\{[^}]*\}\}', '', strip_code(inner)) and '{{' not in inner \
                    and 'aria-label' not in attrs and 'title=' not in attrs:
                add('FAIL', 'botao-icone-sem-nome', f, '<button' + m.group(1)[:80] + '>')
        for m in re.finditer(r'<input\b([^>]*)>', src, flags=re.I):
            attrs = m.group(1).lower()
            if 'type="hidden"' in attrs:
                continue
            idm = re.search(r'\bid="([^"]+)"', attrs)
            has_label = 'aria-label' in attrs or (idm and f'for="{idm.group(1)}"' in low)
            if not has_label:
                # rótulo envolvendo o input
                before = low[:m.start()]
                if before.rfind('<label') <= before.rfind('</label>'):
                    add('FAIL', 'campo-sem-rotulo', f, '<input' + m.group(1)[:80] + '>')
        for m in re.finditer(r'<(div|span|li)\b[^>]*\bonclick=', low):
            add('FAIL', 'clique-em-div', f, f'<{m.group(1)} onclick>: use <button> ou <a>')
        if 'intersectionobserver' in low:
            add('WARN', 'fade-no-scroll', f, 'IntersectionObserver: nada de cartão aparecendo ao rolar')
        if re.search(r'<h[12]\b', low) and 'text-wrap' not in low and 'balance' not in low:
            add('WARN', 'titulo-sem-balance', f, 'h1/h2 sem text-wrap: balance')

        # copy
        for w in SLOP_EN + SLOP_PT + SLOP_DE:
            if re.search(r'(?<![\w-])' + re.escape(w), tlow):
                i = tlow.find(w)
                add('FAIL', 'palavra-slop', f, f'“{w}” em: …{text[max(0, i - 30):i + 40]}…')
        for p in STOCK:
            m = re.search(p, tlow)
            if m:
                add('FAIL', 'frase-pronta', f, text[max(0, m.start() - 10):m.end() + 20])
        for p in RESIDUE:
            m = re.search(p, tlow)
            if m:
                add('FAIL', 'residuo', f, text[max(0, m.start() - 10):m.end() + 20])

    # agregados
    sat = [(b, n) for b, n in hues.most_common() if n >= 3]
    if len(sat) > a.max_hues:
        finds.append(('FAIL', 'matizes-demais', '(todos)',
                      'matizes saturados: ' + ', '.join(f'{b}°×{n} {hue_ex[b]}' for b, n in sat)))
    for href, lbls in labels_by_href.items():
        if len(lbls) > 2:
            finds.append(('INFO', 'rotulos-diferentes', '(todos)', f'{href}: ' + ' | '.join(sorted(lbls))[:120]))

    # relatório
    by = Counter((l, i) for l, i, _, _ in finds)
    print(f'slop_check · {len(files)} artboards')
    print('contagens: ' + ', '.join(f'{b}°×{n}' for b, n in sat) + f'  (máx. {a.max_hues} matizes)')
    for (lvl, fid), n in sorted(by.items(), key=lambda x: (x[0][0] != 'FAIL', -x[1])):
        ex = [x for x in finds if x[0] == lvl and x[1] == fid][:3]
        print(f'{lvl:4} {fid:22} {n:4}  ' + ' ; '.join(f'{e[2]}: {e[3]}' for e in ex))
    nf = sum(n for (l, _), n in by.items() if l == 'FAIL')
    print(f'\n{nf} FAIL, {sum(n for (l, _), n in by.items() if l == "WARN")} WARN '
          '(INFO = confira à mão: um rótulo por ação, nav à parte)')
    if a.json:
        json.dump([dict(nivel=l, id=i, arquivo=f, exemplo=e) for l, i, f, e in finds],
                  open(a.json, 'w'), ensure_ascii=False, indent=1)
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
