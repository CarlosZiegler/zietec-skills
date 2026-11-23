# Forja: changelog


### v2.7 (2026-11-23) — constância de UI e bibliotecas de referência
- Feedback do usuário no Salles Squad: rótulos de botão quebrando em duas linhas e alinhados à esquerda; check verde na lista de exercícios e preto nas séries.
- `estilo-base.md` §5: rótulo de botão centralizado e numa linha (empilhar ou encurtar quando não cabe, conferir em alemão); um marcador de "feito" só (tinta + check branco), verde só em status com texto. Checklist com o portão de botões no navegador.
- Nova §11: o que pegar de libraries.dev, pro.beui.dev, uiarc.dev, bencho.dev, boardui.com, affectui.com, kobra.systems e ui.watermelon.sh.
- `design-system.md`: README de componente com anatomia (partes nomeadas e `data-slot`).

### v2.6 (2026-11-23) — design system com craft
- Novo `references/design-system.md` (craft-system/setup/sync de diego3g/craft, MIT): fundamentos por papel, regras de interação únicas, componentes com matriz de estados e índice; artifact do tipo Design System + instalado no canvas (`project/ds/…`, `designSystems`) + páginas "Design system" + `var(--token)` nas telas + auditoria de hex soltos.
- SKILL.md: entregável 1b.

### v2.5 (2026-11-23) — app completo e flows
- Novo `references/flows.md`: inventário de telas a partir do PRD (`build/inventario.py`), página do app completo (mobile e desktop), uma página por flow no padrão do AutoFolio (linhas: caminho principal, ramos/estados, alternativos; tela inteira por passo com o alvo marcado; sticky com ação → resultado, regra e falha; links de protótipo; perguntas no fim) e mapa de flows. Feature nova = página "<Feature> (aprovar)".
- SKILL.md: entregável 4b; app completo e flows só no idioma-base.
- O padrão visual do Salles Squad v3 (v2.3–v2.4) fica como padrão da Forja v2.

### v2.4 (2026-11-23) — detalhes (Emil/Apple/Appllama), vidro de verdade, login
- Feedback do usuário no Salles Squad v3 (nota 8): CTA preto dentro de cápsula com aro cinza, seleção de plano encostando na borda e cinza chapado, tab bar "branca" e não de vidro.
- `estilo-base.md`: receita de vidro com aro de luz e conteúdo por trás; tab bar iOS 26 (ativo em pílula clara, rótulos); CTA sólido flutuando sozinho; nova §5 "Detalhes" (raio concêntrico, seleção inset, uma borda só, press, easing, tipo, números, plural, datas); nova §6 fluxo de entrada (boas-vindas → entrar → código); nova §8 pesquisa no Mobbin/Appllama antes da tela-chave; checklist ampliado.
- SKILL.md: tela 6 passa a incluir o fluxo de entrada (6a–6c); §4.5 pede pesquisa antes e detalhes depois.
- Fontes: emilkowalski/skills (emil-design-eng, apple-design, ui-cheatsheet; MIT), Appllama skills (MIT), Mobbin (padrões de Revolut e Lightyear, sem copiar).

### v2.3 (2026-11-23) — base visual padrão: minimal nativo com vidro
- Novo `references/estilo-base.md`: padrão de todo pacote, na linha do app novo do Claude (nov/2026), Revolut, Flighty e iOS 26. Fundo cinza frio quase branco, Inter/Geist na interface, serifa só em display, vidro obrigatório no cromo flutuante (topo, tab bar, barra de baixo, sheets, menus) e proibido no conteúdo, listas sem cartão por linha, número-herói por tela, ação primária em tinta.
- Seção 4 reescrita: a variação entre produtos acontece dentro da base (acento, marca pequena, serifa de display, fotografia, número-herói, modo). Estilo fora da base só com pedido do usuário.
- Proibidas fontes manuscritas (Caveat e afins): o usuário achou ilegível a nota manuscrita do Salles Squad v2. `slop_check.py` dá FAIL nelas e avisa vidro em conteúdo ou navegação sem vidro.

### v2.2 (2026-11-22) — passe anti-slop
- `references/anti-slop.md`: contrato de design (um acento, uma família de cinzas, escala de raios, um conjunto de ícones, um rótulo por ação, exceção só com porquê), catálogo do que é slop, regras de copy e de interface, metas e portão de 6 perguntas.
- `scripts/slop_check.py`: contagens objetivas nos `.dc.html` (matizes, violeta, gradiente de lavagem, vidro, raios, emoji, rótulos, `...`, aspas, `transition: all`, foco, zoom, `img`, botão de ícone, campo sem rótulo, `onclick` em div, fade no scroll, palavras e frases de slop em EN/PT/DE, resíduo).
- Seção 9 ganha o passe 4 (anti-slop) entre pior caso e auto-revisão; contrato no `design_brief.py`; `DESIGN.md`/`CLAUDE.md` do handoff levam o contrato e a revisão Vercel para o código.
- Fontes: uizze anti-ui-slop (Apache-2.0), ThinkUI (só a ideia, reescrita), Taste Skill (MIT), Vercel Web Interface Guidelines (MIT), Emil Kowalski (MIT, já integrado).
- Testado no Salles Squad v2: 193 artboards, 1 FAIL real ("Unlocks" no doc EN), corrigido; 7 WARN legítimos (shimmer do carregando e fundos das screenshots de loja).

### v2.1.1 (2026-11-22) — aprendido no Salles Squad v2
- Imagens do Codex publicadas como assets do canvas (`/_blob/<id>`), com o mapa em `build/img_blobs.json`. Imagem solta em `project/img/` não aparece.
- Nomes das ferramentas de artifact do servidor `claude-artifacts` (`create_from_type`, `publish_files` em modo patch, `upload_asset`).
- O Codex do Mac do usuário está sempre autorizado. O `device_bash` remoto é uma VM Linux e não chega nele: use device-auth na nuvem.
- Nota de layout: rótulos com `nowrap` em tabelas de 390 px.

## v2.1 (2026-11-22)

- **Imagens com o Codex CLI** (seção 4.6): fotos, cenas e modelos 3D gerados com a geração de imagem do Codex do usuário, no lugar de silhuetas e placeholders. Script `scripts/gen_images.py` e `references/imagens-codex.md` com rotas (Mac, nuvem com `codex login --device-auth`, espaço reservado), prompts e regras.

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

## Snapshot do claude.ai

A cópia da Forja que estava salva na conta do claude.ai antes da v2 (mais simples que a v1 do repositório, com as edições de 22/11 vindas de craft, emilkowalski/skills e gridlines) está em [`snapshots/forja-claude-ai-2026-11-22.SKILL.md`](./snapshots/forja-claude-ai-2026-11-22.SKILL.md).

## Como voltar para a v1

- **No chat**: diga "usa a Forja v1". A skill `forja-v1` existe ao lado da `forja`.
- **No claude.ai**: a skill `forja-v1` fica salva na sua conta junto da `forja`. Para voltar de vez, troque o conteúdo da `forja` pelo SKILL.md de `skills/design/forja-v1/`.
- **No repositório**: `git checkout 64941bb -- skills/design/forja` restaura a pasta da v1 no lugar da v2. Para ter uma tag: `git tag forja-v1.0 64941bb && git push origin forja-v1.0`.
- **Instalação via skills.sh**: `npx skills@latest add CarlosZiegler/zietec-skills --skill forja-v1`.
