# Forja

**Da ideia ao pacote de produto.** Uma ideia de app ou micro-SaaS entra; sai um canvas do Claude Design com:

- 9 telas mobile e 9 desktop com motion;
- pitch de 14 slides;
- documentação de produto A4 em 6 seções (Vision Board, PRD, User Flows, User Stories, ARD, Cronograma);
- tudo em **EN · PT · DE**, com seletor de idioma e direção de arte própria em cada produto.

A Forja foi usada em mais de 30 produtos, entre eles Zugang (o piloto), Klarbeleg, Lernlupe e Teilo. Este pacote descreve a skill do jeito que ela roda na prática:

- overview antes de construir;
- um subagente por produto;
- portões obrigatórios, principalmente o do pitch;
- atualização no mesmo link;
- a lista de todos os apps no fim de cada entrega.

A [Têmpera](../tempera/) parte da Forja e acrescenta registro de evidências, rastreabilidade e réplica de fluxos. As duas existem lado a lado para comparar.

## Estrutura

```
forja/
├── SKILL.md                         # o que sai e as regras (conteúdo, canvas, direção de arte, telas, doc, pitch, idiomas, verificação, entrega)
├── references/
│   ├── fluxo-de-trabalho.md         # como a sessão anda: ideia → overview → subagente → portões → entrega
│   ├── brief-novo-produto.md        # modelo de prompt para o subagente que constrói um produto
│   ├── atualizar-produto.md         # ajuste, pivô, links/referências, retrofit de idiomas
│   └── build-e-publicacao.md        # motor local, contagens, ordem de build, publicação, notas aprendidas
└── scripts/
    ├── fetch_fonts.py               # Google Fonts → woff2 + local.css (para medir e fotografar sem rede)
    ├── preview.py                   # renderizador mínimo de .dc.html (holes, sc-for, sc-if) + Playwright
    ├── verify_pages.py              # overflow do doc (main ≤ 948) e do pitch + screenshots
    ├── checklogic.js                # roda cada class Component no Node: holes, handlers e testes de interação
    ├── check_links.py               # links, seletor EN·PT·DE, <html lang>, '{{' solto, sobras de idioma
    ├── contrast.py                  # contraste WCAG dos pares declarados em brand.py
    └── i18n.py                      # T(pt, en, de), nomes de arquivo por idioma, formatos de número/data/moeda
```

Requisitos dos scripts: Python 3.11+, Playwright com Chromium (para `preview.py` e `verify_pages.py`) e Node 18+ (para `checklogic.js`).

## Uso rápido

```sh
python3 scripts/fetch_fonts.py "family=Space+Grotesk:wght@400..700&family=Martian+Mono:wght@400..600" build/fonts
node scripts/checklogic.js project build/logic_tests.js
python3 scripts/check_links.py project --screen-base de --doc-pages build/doc_pages.json
cd build && python3 ../scripts/verify_pages.py ../project "Pitch-*" all
python3 scripts/contrast.py build
```

## Requisitos de ambiente

- Ferramenta **Artifact** com o tipo **Design** (Claude Design) para publicar o canvas.
- Agent tool, para delegar cada produto a um subagente (recomendado; dá para rodar sem).
- WebSearch/WebFetch para a pesquisa.
