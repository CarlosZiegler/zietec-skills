# Lançamento e handoff (Forja v2)

Detalhe da seção 10 do `SKILL.md`. Roda depois dos portões, quando o pacote já está verificado.

## 1. Página Lançamento

### Screenshots de App Store

- 6 artboards de **1290×2796** (iPhone 6,7"/6,9"), `L-01` a `L-06`, no idioma-base.
- Cada um: título de benefício em cima (no máximo 2 linhas, 80–96 px), a tela real dentro de uma moldura de iPhone desenhada em CSS (raio externo, ilha, sombra em camadas), fundo na direção de arte do produto.
- Use o HTML interno real da tela mobile, como nos celulares do pitch: sem `sc-if`, `onClick`, `id`, `for` e `href`.
- História na ordem: 1 aha, 2 prova, 3 diferencial, 4 retenção, 5 canal/colaboração, 6 preço ou confiança.
- Títulos falam do resultado, não da feature: "Pronto para a auditoria em 30 minutos", não "Relatórios automáticos".
- Nada de dado pessoal real; marcas fictícias `.example`.

### Storyboard do teaser

- Um artboard `L-07` com 6–8 cenas em grade. Cada cena: miniatura da tela, frase de narração (até 12 palavras), duração e a ação na tela.
- Total de 15–30 s, formato 9:16, primeira cena com o gancho em até 2 s, última com nome + CTA.
- Grave o roteiro também como `teaser.json` no formato de configuração da skill `ads-video` (cenas, textos, durações, telas). Gerar o vídeo é um passo à parte, só a pedido do usuário.

## 2. Arquivos de handoff

Gere em `build/handoff/` e envie com SendUserFile. Não vão para o canvas.

### `DESIGN.md`

```markdown
# DESIGN.md · <Produto>

> Se este arquivo e o código discordarem, o código vence até o dono decidir. Anote o conflito em Perguntas em aberto.

## Produto
## Público e voz
## Clima (palavras + nunca parecer)
## Marca (cores com hex e papel, fontes, logo)
## Referências (pegar / evitar)
## Restrições (plataformas, WCAG, alvos, tema, ícones, motion)
## Tokens
<cores por papel: text, text-muted, surface, fill-1, border, primary, focus, status-*; escala de tipo; espaçamento; raios; sombras; durações e easing>
## Componentes e matriz de estados
## Estados de tela (do catálogo, por tela)
## Direção escolhida (e as descartadas, com o porquê)
## Decisões (data, decisão, porquê)
## Perguntas em aberto
```

### `PRD.md`

O PRD do doc em markdown, no idioma-base: contexto, hipótese central, objetivos (com a taxa de ativação), personas, escopo, requisitos MoSCoW, RNF, regras de negócio, riscos, user stories com critério de aceite e pontos, eventos (ativação e upgrade no limite) e o critério de aceite da v1. IDs iguais aos do doc.

### `CLAUDE.md`

```markdown
# <Produto>

Antes de mexer em UI, leia DESIGN.md. Antes de mexer em escopo, leia PRD.md.

## Stack
<web: TanStack Start + React + TS, PostgreSQL + Drizzle, fila no Postgres>
<ou app: Expo + Expo UI, mesmo backend>

## Comandos
<dev, test, lint, typecheck, e2e>

## Regras
- Tokens só por papel; nenhum hex solto em componente.
- Toda tela com os estados do DESIGN.md.
- Interface em EN · PT · DE; nenhum texto fixo fora dos arquivos de tradução.
- Mudou algo compartilhado: liste as telas afetadas antes.
- Falhe alto: "pronto" só com a verificação abaixo passando.

## Verificar o próprio trabalho
- Teste e2e do fluxo de ativação (do primeiro acesso ao evento de ativação).
- Screenshot antes e depois em toda mudança de UI.
- Itens que só um aparelho real confirma (hover preso, teclado, safe area): listar no PR.

## Skills recomendadas
- web: emil-design-eng, gridlines, simplificar-design
- app: expo/skills, animate-expo, mobile-native, gestures
- verificação: create-verification-skill, security-audit-skill
```

Ajuste o `CLAUDE.md` à stack escolhida no ARD. Não invente comandos: se o projeto ainda não existe, escreva os comandos padrão da stack e marque `[confirmar no setup]`.
