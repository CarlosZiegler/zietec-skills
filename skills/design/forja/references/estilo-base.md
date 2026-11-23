# Estilo base da Forja: minimal nativo com vidro

**É o padrão de todo pacote.** Leia antes da direção de arte (seção 4). O produto só sai desta base se o usuário pedir outro estilo com palavras ("quero editorial", "quero retrô"). A variação entre produtos acontece **dentro** da base (seção 9).

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

**Receita** (claro). O vidro tem que *parecer material*: translúcido, com borda de luz em cima, e com conteúdo visível por trás. Branco a 90% com sombra é um cartão branco, não vidro.

```css
.glass {
  background: rgba(250,250,252,.55);
  backdrop-filter: blur(28px) saturate(190%);
  -webkit-backdrop-filter: blur(28px) saturate(190%);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,.85),   /* luz batendo na borda de cima */
    inset 0 0 0 .5px rgba(255,255,255,.5),  /* aro interno claro */
    0 0 0 .5px rgba(15,17,21,.10),          /* contorno fino de fora */
    0 10px 30px rgba(15,17,21,.12);         /* separa do conteúdo */
}
```

**Tab bar de vidro (padrão iOS 26 / app do Claude / Lightyear)**:
- cápsula flutuante a 8–12 px da borda inferior, altura 60–64, 3–5 itens;
- item ativo = **pílula clara e sutil** (`rgba(15,17,21,.07)`, ou vidro mais claro) com ícone em tinta ou acento, **nunca um bloco preto sólido**; inativos em cinza `#5F6570`;
- rótulos de 10–11 px sob os ícones quando há 4+ abas (Apple: nome específico, não "Início");
- **sempre** com conteúdo rolando por trás na artboard (foto, cartão, lista), e um esmaecido suave (scroll edge) entre o conteúdo e a barra.

**CTA flutuante**: o botão sólido flutua **sozinho** (pílula em tinta, sombra macia `0 8px 24px rgba(15,17,21,.18)`), com um esmaecido do fundo por baixo. **Nunca** coloque um botão sólido dentro de outra cápsula de vidro ou com aro cinza (vira "borda dupla"). Apple: nunca empilhe uma superfície translúcida sobre outra.

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

## 5. Detalhes que separam 8 de 10 (Emil Kowalski, Apple, Appllama)

Aplique em toda tela antes de olhar a captura final:

- **Raio concêntrico**: elemento dentro de outro arredondado usa `raio interno = raio externo − espaçamento`. Cartão 24 com respiro 6 → linha selecionada 18. Nada de seleção encostando na borda do cartão.
- **Seleção em lista (planos, opções)**: a linha selecionada fica *inset* (margem de 6 px dentro do cartão), com fundo sutil (`rgba(15,17,21,.04)`) **ou** anel de 1,5 px em tinta/acento, nunca os dois pesados juntos. Marcador = círculo preenchido no acento com check branco (estilo iOS), não um "donut" grosso. Separadores finos (0,5 px) entre linhas não selecionadas, recuados do lado do texto.
- **Uma borda só**: nada de borda cinza em volta de botão sólido, cartão com borda + sombra forte, ou contorno dentro de contorno.
- **Cinzas**: preenchimentos cinza só como camada sutil (≤ 6% de tinta) ou superfície #F2F3F5; um bloco cinza médio chapado parece desabilitado.
- **Pressionar**: `scale(.97)` no `:active` em 100–160 ms; linhas de lista ganham fundo (não escala).
- **Easing**: `cubic-bezier(.23,1,.32,1)` para entrar, `cubic-bezier(.32,.72,0,1)` para sheets; nunca `ease-in`; nada nasce de `scale(0)` (use .95 + opacidade); popover cresce a partir do gatilho.
- **Tipo**: títulos grandes com tracking `-0.02em` e entrelinha 1.05–1.15; corpo com entrelinha 1.45 e no máximo ~65 caracteres; ênfase pelo peso da mesma família (não misture serifa dentro de um título sans).
- **Números**: `tabular-nums` em tudo que conta; "R$ 799" com o centavo/sufixo menor quando for número-herói (estilo Revolut `$19.98`).
- **Avatar e ícone** com `flex-shrink: 0`; nada esmagado.
- **Datas**: relativas até 7 dias, depois absolutas.
- **Plural certo** ("1 aluna", "2 alunas").
- **Toque**: alvos ≥ 44 px; ações destrutivas longe da ação principal.
- **Rótulo de botão centralizado e numa linha só** (regra, não gosto): `.btn`, `.btn2`, pílulas e chips têm `text-align:center; white-space:nowrap`. Se dois botões lado a lado não cabem com o texto inteiro, **empilhe** (coluna de largura total) ou encurte o rótulo; nunca deixe quebrar em duas linhas nem alinhar à esquerda. Vale nos 3 idiomas: alemão é o pior caso.
- **Constância de marcadores**: um só jeito de dizer "feito" no produto inteiro: círculo na tinta (primary) com check branco, em série, exercício, passo, item de lista e confirmação. Verde (`success`) fica para status **com texto** (pílula "Enviado", mensagem "Código certo"), nunca para o círculo de concluído. Seleção (rádio, plano) é outra coisa e tem o seu marcador próprio, também igual em toda parte. Antes de entregar, procure duas formas diferentes para o mesmo significado (check verde aqui, preto ali; pílula num lugar, texto no outro) e una.

## 6. Fluxos de entrada (login e cadastro)

Estude 10–20 telas reais antes (seção 8). O padrão que funciona (Revolut, Lightyear, app do Claude):
1. **Boas-vindas**: 2–3 slides curtos (título grande + 1 linha + imagem), indicador de progresso em segmentos no topo, e **dois botões empilhados de largura total**: primário "Criar conta" e secundário "Entrar".
2. **Entrar**: Apple / Google primeiro (botões de largura total com o ícone da marca do provedor), depois e-mail; ou só telefone/e-mail com **link mágico ou código de 6 dígitos** (campos separados, colar preenche tudo, reenviar com contagem).
3. **Código**: teclado numérico, foco automático, erro inline ("Código incorreto. Faltam 2 tentativas"), sem botão "Continuar" quando o 6º dígito já envia.
4. **Permissões** (notificações, fotos) pedidas **no momento do uso**, com uma tela de pré-pedido explicando o ganho.
5. Navegação: login é porta de mão única (voltar não volta ao login); login pedido por uma ação abre como modal e conclui a ação.
Todo pacote tem esse fluxo no mobile (dentro da tela 6, Onboarding ativo, ou como telas 6a–6c) e um login simples no desktop quando houver painel.

## 7. Motion (com as skills do Emil)

- Sheets sobem com mola curta (`cubic-bezier(.32,.72,0,1)`, 380–450 ms), fundo escurece 20%.
- Botões: escala 0,97 no toque, 120 ms. Tab bar: a pílula do ativo desliza entre ícones.
- Números mudam com rolagem de dígitos; nada de fade-in em cada cartão ao rolar.
- `prefers-reduced-motion` respeitado em tudo.

## 8. Pesquisa de referência antes da tela-chave

Antes das direções (§4.5 da skill), estude telas reais do mesmo tipo:
- **Mobbin** (o usuário está logado no Chrome dele): busque o app de referência (Revolut, Lightyear, Flighty…) e o tipo de tela/fluxo (Onboarding, Logging in, Paywall, Home). Anote o *padrão* (esqueleto, hierarquia, onde fica o CTA, como mostra progresso), nunca copie pixels nem marcas.
- **Appllama** (MCP pago, opcional; skills MIT em github.com/Appllama/appllama-skills): 20–30 telas da categoria quando o MCP estiver conectado.
- Registre em `design_brief.py` → Referências: "pegar: …; evitar: …" com o app e a tela.
- Para os **flows** (app completo), a pesquisa é por flow e obrigatória: `flows.md` §1b.

## 9. O que varia de produto para produto

Dentro da base, escolha e grave no `design_brief.py`:
1. **Acento** (um), com contraste medido; diferente dos últimos pacotes do conjunto a evitar.
2. **Marca pequena**: símbolo, monograma ou glifo próprio, usado como o "spark" do Claude, pequeno e raro.
3. **Serifa de display** (uma das 3) ou nenhuma.
4. **Fotografia** do Codex: luz e tratamento coerentes com o produto, sempre recortadas em cartões de raio 20–24 ou sangrando sob o vidro.
5. **Número-herói e vocabulário de dados** do produto.
6. **Modo**: claro por padrão; escuro quando o uso é noturno ou de "cabine" (ex.: viagem, foco, monitoramento).

A página Direções continua com 3 direções, mas **todas dentro da base**: elas variam em estrutura (o que é o herói da tela, onde fica a ação, densidade), não em estética.

## 10. Checklist da base (entra no passe anti-slop)

- [ ] Fundo cinza frio quase branco (ou escuro) e superfícies brancas; nada de creme ou papel.
- [ ] Inter/Geist em toda a interface; serifa só em display; nenhuma fonte manuscrita.
- [ ] Corpo ≥ 15 px no mobile; contraste medido.
- [ ] Vidro em todo cromo flutuante (topo, tab bar, barra de baixo, sheets, menus) e em nenhum conteúdo.
- [ ] Um acento, usado pouco; ação primária em tinta.
- [ ] Listas sem cartão por linha; cartões só para agrupar.
- [ ] Um número-herói por tela, no máximo.
- [ ] Tab bar de vidro de verdade (translúcida, aro de luz, conteúdo por trás, ativo em pílula clara, não bloco preto).
- [ ] CTA sólido flutuando sozinho, sem cápsula/aro em volta.
- [ ] Seleções inset com raio concêntrico; nenhuma seleção encostando na borda.
- [ ] Fluxo de entrada (boas-vindas → entrar → código) desenhado.
- [ ] Detalhes da §5 conferidos na captura em 2× (zoom), não só no tamanho normal.
- [ ] Nenhum rótulo de botão quebrando linha ou estourando (portão no navegador: `scrollWidth > clientWidth` em `.btn,.btn2,.gpill,.chip,.pill`, ignorando selos e `::after`), nos 3 idiomas.
- [ ] Um marcador de "feito" só (tinta + check branco); verde só em status com texto.

## 11. Padrões de componentes e pesquisa de flows

- Componentes reutilizáveis (régua numérica, gráficos com linha de base, heatmap, anel com parciais, quadro de fila, estados de IA, anatomia de componente): `padroes-ui.md`.
- Estrutura de cada flow pesquisada no Mobbin e no Appllama antes de desenhar: `flows.md` §1b. O visual já está decidido aqui; a pesquisa é para passos, ramos, erro e desfazer.
