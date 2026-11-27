# Forja (v2.15)

> Versão atual: **v2.15** (2026-11-27). A v2 começou em 2026-11-22. A v1 continua congelada em [forja-v1](../forja-v1/) (commit `64941bb`), para comparar ou voltar. Histórico completo: [CHANGELOG](../../../docs/forja/CHANGELOG.md).

**Da ideia ao pacote de produto, e de uma versão à próxima sem perder nada.** Uma ideia de app ou micro-SaaS entra (texto, link de um produto parecido, PDF ou print). Sai um pacote completo no Claude Design, pronto para mostrar a sócio, investidor ou cliente e para entregar ao Claude Code.

## O que ela entrega

| Parte | O que é |
|---|---|
| **Veredito de produto** | Antes de qualquer tela: vale construir? ICP, ativação, preço e canal (skill `produto`). |
| **Nome** | Torneio de nomes, com checagem de conotação em PT, DE e EN (skill `nome`). |
| **Pesquisa** | Mercado, concorrentes, preços e flows reais (Mobbin, Appllama), sempre com fonte. |
| **Direções** | Brief de design e 3 direções da tela-chave, com a escolhida marcada. |
| **Design system** | Artifact do tipo Design System com tokens, componentes, matriz de estados e auditoria, instalado no canvas. |
| **Telas** | 9 telas mobile (390) e 9 desktop (1440) com motion. Os papéis são fixos: onboarding ativo, upgrade no limite e assim por diante. |
| **Estados** | Catálogo por tela (vazio, carregando, erro, offline, sem permissão, pior caso) em página própria. |
| **App completo e flows** | Todas as telas do v1 a partir do PRD e uma página por flow, passo a passo, com ramos e estados, como num arquivo de Figma. |
| **Documentação** | A4 paginado em 6 seções: Vision Board, PRD, User Flows, User Stories, ARD e Cronograma. |
| **Pitch** | 14 slides 1920×1080, com roteiro por público e portão obrigatório. |
| **Lançamento** | Screenshots de App Store e roteiro do teaser em vídeo. |
| **Handoff** | `DESIGN.md`, `PRD.md` e `CLAUDE.md` para o Claude Code. |
| **Idiomas** | Tudo em **EN · PT · DE**, com seletor de idioma em cada tela, slide e página. |
| **Versões (v2.15)** | V3, V4…: inventário e paridade (nenhuma prancha some), artifacts organizados com índice de entregas, prints com id estável e deck gerado a partir deles. |

Cada produto tem **direção de arte própria**: cor primária escolhida entre 4 paletas, sem repetir produtos anteriores. A base visual padrão é minimal nativa com vidro. A Forja foi usada em mais de 30 produtos, entre eles Zugang (o piloto), Klarbeleg, Lernlupe, Teilo, Corner, Lumbo, Mossy e Salles Club.

## Como ela roda

1. **Overview antes de construir**, com as correções que a pesquisa trouxe. Se o usuário pedir, a sessão para aqui até o "ok".
2. **Um subagente por produto**. Em lote, a Forja faz o primeiro, espera a aprovação e só então replica.
3. **Gates locais antes de publicar**: tudo é medido no Chromium. Nada é verificado depois de publicado.
4. **Atualização no mesmo link** para ajuste ou pivô. **Versão nova** abre artifacts novos, e as versões antigas ficam congeladas.
5. **Entrega** com a lista de todos os links, agrupados por versão.

## Estrutura

```
forja/
├── SKILL.md                         # o que sai e as regras (conteúdo, canvas, direção de arte, telas, doc, pitch, idiomas, verificação, entrega)
├── references/
│   ├── fluxo-de-trabalho.md         # como a sessão anda: ideia → overview → subagente → portões → entrega
│   ├── brief-novo-produto.md        # modelo de prompt para o subagente que constrói um produto
│   ├── atualizar-produto.md         # ajuste, pivô, links/referências, retrofit de idiomas (mesmo link)
│   ├── versoes-e-paridade.md        # v2.15: versão nova (V3, V4…) sem perder telas, artifacts organizados, prints, deck, diagramas
│   ├── build-e-publicacao.md        # motor local, contagens, ordem de build, publicação, notas aprendidas
│   ├── estilo-base.md               # base visual padrão: minimal nativo com vidro, legibilidade, componentes, o que varia
│   ├── design-system.md             # craft-system: fundamentos, regras, componentes com matriz de estados, auditoria
│   ├── estados-e-qualidade.md       # catálogo de estados, pior caso, mobile-native, coreografia, gridlines, auto-revisão
│   ├── flows.md                     # inventário do app, página por flow, pesquisa no Mobbin/Appllama
│   ├── padroes-ui.md                # régua, gráficos, quadro de fila, estados de IA, papéis, configurações, página de IA
│   ├── anti-slop.md                 # contrato de design, catálogo Impeccable, contagens e as 6 perguntas
│   ├── vitrine-stageshow.md         # enquadramento de UI para pitch, landing, bento, loja e teaser
│   ├── imagens-codex.md             # imagens geradas com o Codex CLI do usuário
│   └── lancamento-e-handoff.md      # screenshots de loja, storyboard do teaser, DESIGN.md/PRD.md/CLAUDE.md
└── scripts/                         # veja a tabela abaixo
```

## Scripts

Os gates saem com código 1 quando há falha. A entrega só sai com todos em zero.

| Script | O que faz |
|---|---|
| `fetch_fonts.py` | Baixa as fontes do Google Fonts para woff2 e gera um `local.css`, para medir e fotografar sem rede. |
| `preview.py` | Renderizador mínimo de `.dc.html`: preenche holes (escapados, como no runtime), `sc-for` e `sc-if`, e mede no Playwright. |
| `verify_pages.py` | Overflow das páginas de tamanho fixo (doc A4 e pitch), com screenshots. |
| `checklogic.js` | Roda cada `class Component` no Node: JSON do `data-props`, holes do template contra `renderVals()` e todos os handlers. |
| `check_links.py` | Links entre arquivos, seletor EN·PT·DE, `<html lang>`, `{{` solto e sobras do idioma errado. |
| `contrast.py` | Contraste WCAG dos pares de cor declarados em `brand.py`. |
| `i18n.py` | `T(pt, en, de)`, nomes de arquivo por idioma e formatos de número, data e moeda. |
| `i18n_check.py` | Gate: `T()` no topo do módulo congela o idioma (EN/DE saíam em PT). |
| `holes_check.py` | Gate: hole com HTML no valor (um `<svg>` de ícone) aparece como código na tela. |
| `overlap_check.py` | Gate: texto sobre texto, controle sobre texto, elemento absoluto com lista cobrindo a tela. |
| `bars_check.py` | **v2.15.** Gate: conteúdo atrás de tab bar, dock, composer, CTA fixo ou home indicator, e elemento cortado pela dobra ou pela lateral. |
| `trunc_check.py` | **v2.15.** Gate: texto cortado por largura, por reticências ou pelo recorte de cartão, pílula ou nó. |
| `parity_check.py` | **v2.15.** Gate entre versões: cada prancha antiga tem destino (mantida, equivalente, descontinuada com motivo…). Zero "faltando". |
| `prints.py` | **v2.15.** Prints 2x de todas as pranchas com id estável em `prints/index.json`, e versão longa das telas que rolam. |
| `deck_check.py` | **v2.15.** Gate do deck (tipo Slides): área segura, `object-fit: cover` que corta a tela, imagem cortada, celulares encavalados. Grava um PNG por slide. |
| `_common.py` | **v2.15.** Base dos gates por prancha: pré-visualização, fontes locais, `/_blob/<id>` trocado pelo arquivo local. |
| `slop_check.py` | Passe anti-slop: contagens objetivas de gradiente, sombra, cartão dentro de cartão, travessão etc. |
| `gen_images.py` | Gera as imagens do pacote com o Codex CLI do usuário. |

Requisitos: Python 3.11+, Playwright com Chromium e Node 18+ (para `checklogic.js` e para o contexto de holes dos gates).

## Uso rápido

```sh
python3 scripts/fetch_fonts.py "family=Space+Grotesk:wght@400..700&family=Martian+Mono:wght@400..600" build/fonts
node scripts/checklogic.js project build/logic_tests.js
python3 scripts/check_links.py project --screen-base de --doc-pages build/doc_pages.json
cd build && python3 ../scripts/verify_pages.py ../project "Pitch-*" all && cd ..
python3 scripts/contrast.py build
FORJA_FONTS=build/fonts python3 scripts/overlap_check.py project/*.dc.html
python3 scripts/bars_check.py project --fonts build/fonts --blobs build/blobmap.json
python3 scripts/trunc_check.py project --fonts build/fonts

# versão nova de um pacote
python3 scripts/parity_check.py --old ../v3/app/project --new app/project --map state/paridade.json
python3 scripts/prints.py app=app/project painel=painel/project --out prints --fonts build/fonts
python3 scripts/deck_check.py deck --blobs deck/blobs_local.json --shots /tmp/deck
```

## v1 × v2: o que mudou

| | v1 (2026-10-20, congelada) | v2 (2026-11-22 → v2.15) |
|---|---|---|
| **Antes das telas** | Pesquisa e telas | Veredito de produto, nome, pesquisa, brief e **3 direções** da tela-chave |
| **Visual** | Direção de arte por produto, livre | Base minimal nativa com vidro, primária própria entre 4 paletas, contrato anti-slop |
| **Design system** | Implícito no CSS | Artifact Design System com tokens, componentes, matriz de estados e auditoria |
| **Telas** | 9 mobile + 9 desktop | As mesmas 9 + 9, com onboarding ativo e upgrade no limite, **página Estados**, pior caso, **app completo e flows** passo a passo |
| **Doc e pitch** | 6 seções A4 e 14 slides | Iguais, mais ativação, canal, 10 primeiros pagantes, papéis, configurações em 3 níveis e página de IA |
| **Depois do pitch** | — | **Lançamento** (loja e teaser) e **handoff** (`DESIGN.md`, `PRD.md`, `CLAUDE.md`) |
| **Verificação** | Overflow, lógica, links, contraste | Isso e mais: simplificar, gridlines, pior caso, anti-slop, holes, idioma congelado, sobreposição, **barras e dobra, truncamento, paridade e deck** |
| **Scripts** | 7 | 18 |
| **Versões** | Atualizar no mesmo link | Isso e mais: **versão nova sem perder conteúdo** (paridade), artifacts organizados com índice, prints com id estável, deck a partir dos prints, diagramas medidos |
| **Imagens** | Geradas no fluxo | Codex CLI do usuário, como assets `/_blob/`; pessoa real só em moldura |

Resumo por versão da v2:
- **2.1–2.4**: imagens com o Codex, passe anti-slop, base visual nativa com vidro.
- **2.5–2.6**: app completo e flows, design system com craft.
- **2.7–2.9**: constância de UI, bibliotecas de referência, papéis, configurações e página de IA.
- **2.10–2.12**: cor própria por produto, Stageshow, Impeccable, Solid Glass.
- **2.13–2.14**: gates de hole, idioma e sobreposição.
- **2.15**: versões, paridade, barras e dobra, truncamento, prints e deck.

## Voltar para a v1

- **No chat**: diga "usa a Forja v1". A skill `forja-v1` existe ao lado da `forja`.
- **No repositório**: `git checkout 64941bb -- skills/design/forja`.
- **Via skills.sh**: `npx skills@latest add CarlosZiegler/zietec-skills --skill forja-v1`.

## Requisitos de ambiente

- Ferramenta **Artifact** com os tipos **Design**, **Design System** e **Slides**.
- Agent tool, para delegar cada produto a um subagente. É recomendado, mas dá para rodar sem.
- WebSearch/WebFetch para a pesquisa. Opcionais: o Chrome do usuário (Mobbin) e o Codex CLI (imagens).

A [Têmpera](../tempera/) parte da Forja e acrescenta registro de evidências, rastreabilidade e réplica de fluxos. As duas existem lado a lado para comparar.
