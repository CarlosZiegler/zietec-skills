# Forja: changelog

## v2 (2026-11-22)

A v2 parte da v1 e acrescenta etapas antes das telas (produto e nome), durante (direções e estados) e depois (qualidade, lançamento e handoff). Nada da v1 foi removido.

**Antes das telas**

- **0.1 Produto**: skill `produto` em modo rápido. Dor com evidência, ICP, aha e evento de ativação, preço, retenção, canal, hipótese mais arriscada e veredito Construir, Ajustar ou Parar.
- **0.2 Nome**: skill `nome` em modo rápido. Torneio, checagem em PT/DE/EN e sinal de disponibilidade; top 3 no overview.
- **Checagem por outro agente**: um subagente confere cada afirmação de pesquisa na fonte antes do conteúdo.

**Design**

- `design_brief.py` (formato DESIGN.md do craft) junto da direção de arte.
- **4.5 Três direções da tela-chave** em eixos de estrutura, com protótipo e seletor (prototype do Emil Kowalski) e parada para escolha.
- Coreografia de motion: papéis, escalonamento que encolhe, uma entrada por contêiner, saídas mais curtas.
- Base mobile-native no kit de CSS.

**Telas**

- Tela 6 vira **onboarding ativo** e tela 7 vira **upgrade no limite**.
- **Página Estados** com catálogo por tela e **pior caso** da lista.

**Conteúdo**

- Taxa de ativação nos objetivos do PRD; canal principal e 10 primeiros pagantes no PRD e no slide 8.
- Opção de stack Expo + Expo UI para app de consumo mobile-first.
- Evento de ativação e de upgrade no ARD.

**Verificação**

- Passes em ordem: simplificar, gridlines, pior caso, auto-revisão por grupos.

**Depois dos portões**

- **Página Lançamento**: 6 screenshots de App Store e storyboard do teaser (`teaser.json` para a skill `ads-video`).
- **Handoff**: `DESIGN.md`, `PRD.md` e `CLAUDE.md` para o Claude Code.
- Regras novas a partir das correções do usuário, propostas como edição da skill.

**Arquivos novos**: `references/estados-e-qualidade.md`, `references/lancamento-e-handoff.md`.

**Fontes**: [craft](https://github.com/diego3g/craft), [emilkowalski/skills](https://github.com/emilkowalski/skills), [gridlines](https://github.com/pritamux/gridlines), [impeccable](https://github.com/pbakaus/impeccable), [revenue-centric-design](https://github.com/heliocosta-dev/revenue-centric-design) e o [levantamento dos salvos do X](../referencias/2026-11-skills-salvas-no-x.md).

## v1 (2026-10-20)

A Forja que gerou mais de 30 pacotes: pesquisa, 9 + 9 telas com motion, doc A4 em 6 seções, pitch de 14 slides, EN · PT · DE, direção de arte própria por produto, subagente por produto, portão do pitch e atualização no mesmo link. Congelada em `skills/design/forja-v1/` e na commit `64941bb`.

## Como voltar para a v1

- **No chat**: diga "usa a Forja v1". A skill `forja-v1` existe ao lado da `forja`.
- **No claude.ai**: a skill `forja-v1` fica salva na sua conta junto da `forja`. Para voltar de vez, troque o conteúdo da `forja` pelo SKILL.md de `skills/design/forja-v1/`.
- **No repositório**: `git checkout 64941bb -- skills/design/forja` restaura a pasta da v1 no lugar da v2. Para ter uma tag: `git tag forja-v1.0 64941bb && git push origin forja-v1.0`.
- **Instalação via skills.sh**: `npx skills@latest add CarlosZiegler/zietec-skills --skill forja-v1`.
