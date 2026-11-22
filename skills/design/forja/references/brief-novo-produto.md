# Brief para o subagente: produto novo

Modelo do prompt que o orquestrador manda a um subagente para construir **um** pacote Forja. Troque `<…>` e mantenha o resto. `<WS>` é a pasta de trabalho da sessão (scratchpad); `<forja>` é a pasta desta skill.

---

Construa e publique o pacote Forja v2 completo de UMA ideia nova: Direções, Mobile (9 telas), Desktop (9), Estados, Pitch (14 slides), Documentação de Produto (A4, 6 seções) e Lançamento, **em EN · PT · DE desde o início** (Direções, Estados e Lançamento só no idioma-base), com seletor de idioma, num canvas novo do tipo Design. Gere também os arquivos de handoff (`DESIGN.md`, `PRD.md`, `CLAUDE.md`).

## Leia primeiro, nesta ordem

1. `<forja>/SKILL.md`, a skill autoritativa. Siga à risca, principalmente a seção 4 (direção de arte própria), a 7 (portão do pitch) e a 8 (idiomas).
2. `<forja>/references/build-e-publicacao.md`: motor, verificação, publicação e notas aprendidas.
2b. `<forja>/references/estados-e-qualidade.md` e `<forja>/references/lancamento-e-handoff.md`.
3. `<forja>/scripts/`: ferramentas reutilizáveis.
4. Referência de código, se existir na sessão: `<WS>/forja/<produto-mais-recente>/build/`. Reaproveite a **mecânica** (preview, medição, paginação, verificação, lógica, i18n), **não o visual**.
5. A documentação do tipo Design que o `quickstart` devolver (`format.md`, `print.md`).

## Pasta

`<WS>/forja/<slug>/build/` com o motor e `<WS>/forja/<slug>/project/` vazia.

- Crie `brand.py` com os tokens próprios e reescreva os componentes de que precisar.
- No fim, procure sobras de produtos anteriores (nomes, fontes, cores) em `build/*.py project/`; o resultado deve voltar vazio, salvo menção justificada.

## A ideia

<Descrição completa: produto de referência (link e fatos), versão proposta, fluxo, mercado, quem paga, preço de referência.>

**Núcleo já comunicado ao usuário (mantenha):** <bullets do overview>

**Correções já comunicadas (aprofunde com pesquisa):** <concorrente direto, PI, regra legal…>

**Pesquise (2 fontes para afirmação legal; preços com fonte; nada inventado):** <lista específica>

**Brief de produto (etapa 0.1, mantenha):** <cole o `produto_brief.py` ou o resumo: ICP, aha, evento de ativação, preço, retenção, canal, hipótese mais arriscada, veredito>

## Idiomas e público

- Telas: idioma-base <EN|DE|PT>, com os outros 2 pelo seletor. Alemão "<du|Sie>" (consumidor: du; B2B: Sie).
- Pitch e doc: base PT, com EN e DE. Público do pitch: <sócio ou mentor>. Contato só "<Nome do usuário>", nunca e-mail.

## Telas

<O que as 9 telas mobile e as 9 desktop devem cobrir neste produto, com no mínimo 3 interações reais. Se houver 3D ou gráfico, peça CSS 3D / SVG, sem CDN.>

## Nome

<Nome escolhido na etapa 0.2 e as 2 alternativas.> Use o escolhido em tudo. Se não houver nome ainda, rode a skill `nome` em modo rápido (ou: curto, funciona em EN/DE/PT, checagem de conflito na App Store e na web, DPMA/EUIPO [A DEFINIR] sem busca formal, conotações nos 3 idiomas) e justifique.

## Direção de arte (caprichar)

Direção inicial: <referência do mundo real, paleta-base, par de fontes, arquétipo de layout, assinatura de motion>. Pode refinar, mas:

- evite o "conjunto a evitar": leia o `brand.py` de todos os produtos anteriores e não repita fonte + paleta + arquétipo;
- meça o contraste por script; alvos ≥ 44 px (≥ 48–56 px quando a mão está ocupada ou o público é infantil); sem emoji e sem gradiente de fundo.

## Direções

<"Pare nas direções": construa as 3 direções da tela-chave (SKILL.md 4.5), devolva o `direcoes.html` e a tabela de eixos e espere a escolha. Ou: "Siga a recomendada" (lote ou usuário ausente).>

## Estados, onboarding e upgrade

- Marque o catálogo de estados por tela e desenhe a página Estados, com o pior caso da lista.
- Tela 6 = onboarding ativo até o evento de ativação; tela 7 = upgrade no limite com os 3 planos.

## Portões (obrigatórios)

- Renderize e **olhe** os 42 slides: matriz sem "?", 8 riscos visíveis, Gantt visual, próximo passo com data posterior a hoje, nenhum miolo vazio ou texto cortado.
- Doc: todas as páginas com `main.scrollHeight ≤ 948` nos 3 idiomas.
- Telas: `checklogic.js` passa em todas, links e seletor corretos, sem overflow.
- Passes de qualidade feitos, nesta ordem: simplificar, gridlines, pior caso, auto-revisão. Guarde o que mudou.
- Lançamento: 6 screenshots 1290×2796 e o storyboard; `teaser.json` no formato do `ads-video`.
- Handoff: `DESIGN.md`, `PRD.md`, `CLAUDE.md` em `build/handoff/`.

## Publicação

1. `Artifact action=quickstart intent=design design_systems=false` → `type_url`.
2. Publish com `type_url`, `title` = "<Nome> · <descrição curta em PT>" e `auto_open: "after_first_write"`. Siga as instruções do tipo.
3. `project/canvas.json` com 11 páginas: direcoes, mobile, desktop, estados, pitch, pitch-en, pitch-de, doc, doc-en, doc-de e lancamento.
4. Publish com `url` do artifact, `root` = `<WS>/forja/<slug>` e chaves `"project/..."` (em duas chamadas se o tipo pedir `canvas.json` + `Main` primeiro).
5. `action=list scope=files` para confirmar. Não verifique visualmente depois de publicar.

## Retorno (curto, em português)

- URL do artifact.
- Nome e por quê.
- Direção de arte em 2 linhas (hex, fontes, arquétipo, motion) e a direção de estrutura escolhida.
- O que os passes de qualidade mudaram e os estados em aberto.
- Caminhos dos arquivos de handoff e do `teaser.json`.
- 3–5 hipóteses.
- Correções factuais em relação à ideia.
- Contagens por idioma (telas, slides, páginas do doc) e problemas conhecidos.
- Fontes (URLs).
- **Descrição de 1 linha do produto** para a lista de apps.
