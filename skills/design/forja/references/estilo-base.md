# Estilo base da Forja: minimal nativo com vidro

**É o padrão de todo pacote.** Leia antes da direção de arte (seção 4). O produto só sai desta base se o usuário pedir outro estilo com palavras ("quero editorial", "quero retrô"). A variação entre produtos acontece **dentro** da base (seção 6).

Referências do usuário (nov/2026):
- **App novo do Claude** (iOS/Android, nov/2026): quase vazio, saudação em serifa no centro, uma marca pequena colorida, controles de vidro flutuando sobre o conteúdo, tab bar em pílula, sheets com cantos grandes, listas sem cartão.
- **Revolut**: número grande no topo, ações em círculos com rótulo embaixo, cartões agrupados com raio grande, fundo que respira.
- **Flighty**: dado em primeiro lugar, números grandes e tabulares, status com cor + texto, linha do tempo, densidade sem bagunça.
- **iOS 26 (Liquid Glass)**: vidro só no cromo que flutua sobre o conteúdo.

Não copie telas, marcas ou ícones dessas referências. Pegue a **disciplina**: pouca coisa na tela, uma hierarquia clara, vidro no lugar certo.

## 1. Cor

| Papel | Claro | Escuro |
|---|---|---|
| Fundo | `#F2F3F5` (cinza frio quase branco) | `#0B0C0E` |
| Superfície (cartão, sheet sólido) | `#FFFFFF` | `#16171A` |
| Texto | `#0F1115` | `#F4F5F7` |
| Texto secundário | `#5F6570` (≥ 4,5:1 no fundo) | `#A1A6AF` |
| Linha | `rgba(15,17,21,.08)` | `rgba(255,255,255,.08)` |
| Ação primária | tinta (`#0F1115`), botão preto em pílula ou círculo | branco |
| **Acento do produto** | **um**, escolhido por produto (seção 6) | o mesmo, ajustado |

- O acento aparece pouco: a marca do produto, o estado ativo, o número-herói, um indicador. Nunca em blocos grandes de fundo.
- Status (erro, alerta, ok) sempre com forma + texto, nunca só cor.
- Uma família de cinzas (fria). Nada de bege, creme ou papel nesta base.

## 2. Tipografia (legibilidade primeiro)

- **Sans para toda a interface**: Inter (padrão) ou Geist, pelo Google Fonts. Corpo 16 px no mobile (mínimo 15), 15–16 px no desktop, altura de linha 1,4–1,5, peso 400/500/600.
- **Uma serifa só para momentos de display**: saudação, título de tela vazia, capa do pitch. Opções: Newsreader, Source Serif 4 ou Fraunces (opsz baixo). Nunca em botão, rótulo, tabela ou parágrafo longo de interface.
- **Números**: sans 600–700, `tabular-nums`, tracking levemente negativo nos grandes (estilo Flighty/Revolut). Um número-herói por tela, no máximo.
- **Proibido**: fonte manuscrita ou script (Caveat, Kalam, Pacifico, Dancing Script, Indie Flower, Permanent Marker, Shadows Into Light…), condensada no corpo, monoespaçada fora de produto dev, caixa-alta longa com tracking largo.
- Títulos com `text-wrap: balance`; nenhum texto abaixo de 12 px (legendas 12–13 px com contraste ≥ 4,5:1).

## 3. Vidro (regra, não enfeite)

**Onde o vidro é obrigatório** (cromo que flutua sobre conteúdo):
- botões circulares de topo (menu, perfil, fechar, ações): 40–44 px;
- **tab bar flutuante** em pílula (4–5 ícones, o ativo com uma pílula sólida por trás);
- barra de entrada ou de CTA flutuante no rodapé;
- **bottom sheets** e modais (raio 28–32 px, alça de arrasto, cabeçalho com X em círculo + título + ação);
- menus, popovers e toolbar do desktop.

**Onde o vidro é proibido**: cartões de conteúdo, linhas de lista, gráficos, tabelas, fundo de tela inteira. Conteúdo é sólido ou sem container.

**Receita** (claro):

```css
background: rgba(255,255,255,.72);
backdrop-filter: blur(24px) saturate(180%);
-webkit-backdrop-filter: blur(24px) saturate(180%);
border: 1px solid rgba(255,255,255,.65);
box-shadow: 0 0 0 .5px rgba(15,17,21,.08), 0 8px 24px rgba(15,17,21,.08);
```

Escuro: `rgba(28,29,33,.62)` com borda `rgba(255,255,255,.08)`. O vidro precisa de algo atrás para aparecer: deixe o conteúdo rolar por baixo da tab bar e dos botões de topo; nas artboards estáticas, mostre conteúdo passando por trás. Se o navegador não suportar `backdrop-filter`, o fallback é a superfície sólida a 94%.

## 4. Layout e componentes

- **Respiro**: margem lateral 20 px no mobile; grade de 4/8 px; uma ação primária por tela.
- **Listas como no app do Claude**: linhas simples com ícone de traço à esquerda, texto, metadado discreto à direita; cabeçalho de seção pequeno e cinza; nada de cartão por linha.
- **Cartões só para agrupar** (estilo Revolut): raio 20–24 px, superfície branca, sem borda pesada, sombra quase nula; no máximo 2 níveis de caixa.
- **Topo**: título grande à esquerda (34 px, 700) ou serifa centralizada em tela vazia; botões circulares de vidro nos cantos.
- **Ações rápidas** (estilo Revolut): círculos de 52–56 px com ícone e rótulo de 12–13 px embaixo.
- **Dados** (estilo Flighty): número grande + unidade pequena, linha do tempo vertical, chip de status com ponto colorido + texto, comparação "antes → agora".
- **Estado vazio**: quase nada na tela, uma frase em serifa, a marca pequena, a ação na barra de baixo.
- **Ícones**: um conjunto de traço 1,5–1,75 px (estilo Lucide), em SVG inline. Sem emoji.
- **Raios**: 12 (campos e chips), 20–24 (cartões), 28–32 (sheets), 999 (pílulas e círculos).
- **Pitch e doc**: a mesma base. Slides e páginas brancas ou cinza frio, Inter no texto, a serifa de display nos títulos grandes, um número-herói por slide, fotos do Codex em cartões de raio 20–24. Nada de fonte manuscrita nem textura de papel.
- **Desktop**: mesma base; sidebar clara e silenciosa (lista como no mobile), conteúdo com largura máxima, toolbar e diálogos de vidro, tabelas densas com `tabular-nums`.

## 5. Motion (com as skills do Emil)

- Sheets sobem com mola curta (`cubic-bezier(.32,.72,0,1)`, 380–450 ms), fundo escurece 20%.
- Botões: escala 0,97 no toque, 120 ms. Tab bar: a pílula do ativo desliza entre ícones.
- Números mudam com rolagem de dígitos; nada de fade-in em cada cartão ao rolar.
- `prefers-reduced-motion` respeitado em tudo.

## 6. O que varia de produto para produto

Dentro da base, escolha e grave no `design_brief.py`:
1. **Acento** (um), com contraste medido; diferente dos últimos pacotes do conjunto a evitar.
2. **Marca pequena**: símbolo, monograma ou glifo próprio, usado como o "spark" do Claude, pequeno e raro.
3. **Serifa de display** (uma das 3) ou nenhuma.
4. **Fotografia** do Codex: luz e tratamento coerentes com o produto, sempre recortadas em cartões de raio 20–24 ou sangrando sob o vidro.
5. **Número-herói e vocabulário de dados** do produto.
6. **Modo**: claro por padrão; escuro quando o uso é noturno ou de "cabine" (ex.: viagem, foco, monitoramento).

A página Direções continua com 3 direções, mas **todas dentro da base**: elas variam em estrutura (o que é o herói da tela, onde fica a ação, densidade), não em estética.

## 7. Checklist da base (entra no passe anti-slop)

- [ ] Fundo cinza frio quase branco (ou escuro) e superfícies brancas; nada de creme ou papel.
- [ ] Inter/Geist em toda a interface; serifa só em display; nenhuma fonte manuscrita.
- [ ] Corpo ≥ 15 px no mobile; contraste medido.
- [ ] Vidro em todo cromo flutuante (topo, tab bar, barra de baixo, sheets, menus) e em nenhum conteúdo.
- [ ] Um acento, usado pouco; ação primária em tinta.
- [ ] Listas sem cartão por linha; cartões só para agrupar.
- [ ] Um número-herói por tela, no máximo.
