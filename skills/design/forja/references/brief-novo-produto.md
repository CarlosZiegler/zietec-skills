# Brief para o subagente: produto novo

Modelo do prompt que o orquestrador manda a um subagente para construir **um** pacote Forja. Troque `<…>` e mantenha o resto. `<WS>` é a pasta de trabalho da sessão (scratchpad); `<forja>` é a pasta desta skill.

---

Construa e publique o pacote Forja completo de UMA ideia nova: Mobile (9 telas), Desktop (9), Pitch (14 slides) e Documentação de Produto (A4, 6 seções), **em EN · PT · DE desde o início**, com seletor de idioma, num canvas novo do tipo Design.

## Leia primeiro, nesta ordem

1. `<forja>/SKILL.md`, a skill autoritativa. Siga à risca, principalmente a seção 4 (direção de arte própria), a 7 (portão do pitch) e a 8 (idiomas).
2. `<forja>/references/build-e-publicacao.md`: motor, verificação, publicação e notas aprendidas.
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

## Idiomas e público

- Telas: idioma-base <EN|DE|PT>, com os outros 2 pelo seletor. Alemão "<du|Sie>" (consumidor: du; B2B: Sie).
- Pitch e doc: base PT, com EN e DE. Público do pitch: <sócio ou mentor>. Contato só "<Nome do usuário>", nunca e-mail.

## Telas

<O que as 9 telas mobile e as 9 desktop devem cobrir neste produto, com no mínimo 3 interações reais. Se houver 3D ou gráfico, peça CSS 3D / SVG, sem CDN.>

## Nome

Curto, funciona em EN/DE/PT. Faça uma checagem rápida de conflito (App Store, web; DPMA/EUIPO fica [A DEFINIR] se não houver busca formal) e de conotações nos 3 idiomas. Proponha e justifique.

## Direção de arte (caprichar)

Direção inicial: <referência do mundo real, paleta-base, par de fontes, arquétipo de layout, assinatura de motion>. Pode refinar, mas:

- evite o "conjunto a evitar": leia o `brand.py` de todos os produtos anteriores e não repita fonte + paleta + arquétipo;
- meça o contraste por script; alvos ≥ 44 px (≥ 48–56 px quando a mão está ocupada ou o público é infantil); sem emoji e sem gradiente de fundo.

## Portões (obrigatórios)

- Renderize e **olhe** os 42 slides: matriz sem "?", 8 riscos visíveis, Gantt visual, próximo passo com data posterior a hoje, nenhum miolo vazio ou texto cortado.
- Doc: todas as páginas com `main.scrollHeight ≤ 948` nos 3 idiomas.
- Telas: `checklogic.js` passa em todas, links e seletor corretos, sem overflow.

## Publicação

1. `Artifact action=quickstart intent=design design_systems=false` → `type_url`.
2. Publish com `type_url`, `title` = "<Nome> · <descrição curta em PT>" e `auto_open: "after_first_write"`. Siga as instruções do tipo.
3. `project/canvas.json` com 8 páginas: mobile, desktop, pitch, pitch-en, pitch-de, doc, doc-en e doc-de.
4. Publish com `url` do artifact, `root` = `<WS>/forja/<slug>` e chaves `"project/..."` (em duas chamadas se o tipo pedir `canvas.json` + `Main` primeiro).
5. `action=list scope=files` para confirmar. Não verifique visualmente depois de publicar.

## Retorno (curto, em português)

- URL do artifact.
- Nome e por quê.
- Direção de arte em 2 linhas (hex, fontes, arquétipo, motion).
- 3–5 hipóteses.
- Correções factuais em relação à ideia.
- Contagens por idioma (telas, slides, páginas do doc) e problemas conhecidos.
- Fontes (URLs).
- **Descrição de 1 linha do produto** para a lista de apps.
