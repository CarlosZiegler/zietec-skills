# Anti-slop: contrato, contagens e portão

Leia na seção 4, ao fechar a direção de arte, e na seção 9, antes da auto-revisão. A base visual padrão está em `references/estilo-base.md`; este arquivo diz o que não pode aparecer nela. Objetivo: nenhuma tela parecer "feita por IA" nem servir, sem mudança, para um concorrente.

Fontes destiladas (regras reescritas, nada copiado; consulte o original se precisar):

| Fonte | Licença | O que entrou na Forja |
|---|---|---|
| uizze `anti-ui-slop` (github.com/uizze/uizze, derivada do Impeccable) | Apache-2.0 | Contrato de design, contagens rápidas, regra da exceção, playbooks de craft e auditoria |
| ThinkUI `thinkui-anti-slop` (thinkui.xyz/skills) | não declarada | Só a ideia do portão de 6 perguntas, em palavras nossas |
| Taste Skill (github.com/Leonxlnx/taste-skill) | MIT | Lista de palavras e frases prontas, regras de copy, "um sistema", nada de fade no scroll, sem violeta |
| Vercel Web Interface Guidelines (vercel-labs/agent-skills) | MIT | Tipografia, foco, formulários, imagens, animação e copy de interface |
| Emil Kowalski (emilkowalski/skills) | MIT | prototype, mobile-native, choreograph, break-ui, learn-taste; **emil-design-eng, apple-design e ui-cheatsheet** destilados em `estilo-base.md` §3 e §5 |
| Appllama (github.com/Appllama/appllama-skills) | MIT (nome e marca não) | Leis anti-slop e de fidelidade nativa, navegação (portas de mão única), estudar telas reais antes; MCP pago opcional |

**Cuidados.** ThinkUI e uizze vendem um MCP pago de referências reais. É opcional e só entra se o usuário conectar; sem ele, diga que a etapa de evidência ficou de fora, nunca invente uma referência. A Taste Skill instala um hook `Stop` no Claude Code e um gate em Node com Chrome: use só as regras destiladas aqui, sem instalar nada sem o usuário pedir.

---

## 1. Contrato de design (vai no `design_brief.py`)

Escreva, antes da primeira tela, cinco linhas que o resto do pacote obedece:

1. **Um acento** para ação primária, mais no máximo **um apoio de marca**. Erro e ok são semânticos e não contam como acento.
2. **Uma família de cinzas**: quente ou fria, nunca as duas.
3. **Uma escala de raios** (ex.: 6 campos, 12 cartões, 999 pílulas). Valor fora da escala é erro.
4. **Um conjunto de ícones** (SVG de traço próprio ou um set nomeado). Emoji nunca é ícone.
5. **Um rótulo por ação**: "Fazer minha anamnese" é sempre esse texto, em todo lugar. Navegação à parte.

Exceção, que vale para tudo neste arquivo: uma escolha deliberada de marca fica, **se alguém consegue explicar por que o produto a usa**. Escreva o porquê no `design_brief.py`; sem porquê, sai.

## 2. O que conta como slop

**Visual**
- Gradiente de lavagem (roxo, índigo, malha) e brilho em botão. Padrões desenhados com gradiente, como régua, pauta ou máscara, não contam.
- Índigo, violeta ou lavanda sem motivo de marca.
- Vidro em cartão de conteúdo, linha de lista ou fundo inteiro. Na base da Forja o vidro é **obrigatório** no cromo flutuante (botões de topo, tab bar, barra de baixo, sheets, menus) e proibido no conteúdo (`references/estilo-base.md`).
- Fonte manuscrita ou script em qualquer texto de interface (Caveat e afins): é ruim de ler.
- Vários acentos espalhados pelas telas.
- Cinzas quentes e frios misturados.
- Raios aleatórios.
- Grade de cartões ícone + título + texto repetida, gráfico decorativo sem dado, painéis dentro de painéis (mais de 2 caixas de profundidade).
- Palavra em serifa solta no meio do título, brilhos e estrelinhas em títulos.
- Todas as seções entrando igual; cartão aparecendo ao rolar; parallax em texto.
- Legenda explicando a imagem.

**Catálogo do Impeccable** (impeccable.style/slop, 62 checagens; pbakaus/impeccable, Apache-2.0), o que ainda não estava acima:
- Rótulo ou "pílula" acima do título (eyebrow, "Novo", "Apresentando"): proibido; o título carrega o próprio peso. Números de seção (01, 02) só quando a sequência importa.
- Cartão com borda fina **e** sombra larga ("cartão fantasma"): declare a elevação uma vez, borda **ou** sombra.
- Barra colorida num lado só de um cartão arredondado; sombra dura deslocada sem desfoque; texto em gradiente; listras de gradiente; grade de fundo decorativa.
- Template de "métrica-herói" (número grande, rótulo pequeno, stats e acento) como estrutura de página; grade de cartões idênticos; cartão dentro de cartão.
- Paleta bege/creme por reflexo; roxo e ciano de "IA"; halo radial e holofote atrás do conteúdo; modo escuro com brilho neon.
- Ponto pulsando sem nada ter mudado; cursor piscando decorativo; letreiro rolando sem pausa; mola/overshoot em ação de rotina.
- Uma palavra sozinha na última linha; título com cauda curta; mais espaço abaixo do título do que acima; parágrafo justificado; texto colado na borda.
- Travessão em quase toda frase; slogan "não é X, é Y"; superlativo genérico; o mesmo texto repetido dentro de um cartão.
- Superfícies do navegador sem tema: `::selection`, `caret-color`, `accent-color`, barra de rolagem e anel de foco ficam no padrão do browser. Dê a cor do produto.
- Ilustração rabiscada em SVG imitando desenho; máscara geométrica fingindo recorte de foto.
- Escolher claro ou escuro pela categoria: escolha pela cena de uso (quem, onde, com que luz).

Onde a Forja diverge do Impeccable, de propósito: **Inter/Geist** continuam o padrão porque o usuário escolheu o visual do app do Claude, mas a fonte de interface pode variar por produto junto com a paleta (§9 do estilo-base); **raio de cartão** fica em 20–24 px no mobile (iOS nativo) e 16 px no desktop; o **número-herói** só vale quando é o dado principal real do produto (dinheiro, dias, carga), nunca como template.

**Conteúdo**
- Nome genérico, número redondo inventado ("10.000 usuários"), depoimento ou cliente inventado.
- Palavras de slop: em EN *seamless, unlock, elevate, empower, cutting-edge, game-changer, revolutionary, robust, leverage*; em PT *revolucionário, potencialize, desbloqueie, inovador, sem complicação, solução completa, tudo em um só lugar*; em DE *nahtlos, innovativ, maßgeschneidert, ganzheitlich, aufs nächste Level, spielend leicht*. Lista completa no `scripts/slop_check.py`.
- Frases que servem para qualquer negócio: "não é só um app", "diga adeus a", "na palma da sua mão", "imagine um mundo", "nicht nur ein".
- Resíduo: lorem ipsum, `[SEU NOME]`, TODO.

**Comportamento**
- Só o estado de sucesso construído. Botão que não faz nada. Formulário sem erro. Tela vazia sem explicação. Carregando com layout diferente do final.

## 3. Regras de copy (todas as telas, slides e doc)

- O h1 da landing diz **a categoria e para quem** ("Consultoria online de treino feminino"), com **um fato concreto** na primeira tela.
- Todo título tem um substantivo; todo botão é **verbo + objeto** ("Enviar check-in", não "Continuar").
- Mensagem de erro diz o que fazer a seguir.
- Voz ativa, segunda pessoa, números em algarismos ("8 dias úteis").
- `…` e não `...`; "Carregando…"; aspas tipográficas (“ ” em PT/EN, „ “ em DE).
- Leia em voz alta: se a frase serve para o concorrente sem mudar nada, reescreva com um fato do brief.

## 4. Regras de interface (Vercel, adaptadas ao `.dc.html`)

- `<button>` para ação, `<a href>` para navegação; nunca `onclick` em `div`/`span`.
- Botão só de ícone com `aria-label`; ícone decorativo com `aria-hidden="true"`.
- Todo campo com `<label>` (ou `aria-label`), `type` e `inputmode` certos, `autocomplete` com sentido.
- Foco visível com `:focus-visible`; nunca `outline: none` sem substituto.
- `<img>` com `alt` no idioma do arquivo e `width`/`height` (ou `aspect-ratio`).
- Animação só em `transform`/`opacity`, nunca `transition: all`, `prefers-reduced-motion` respeitado, animação interrompível.
- Números em tabela e comparação com `font-variant-numeric: tabular-nums`; títulos com `text-wrap: balance`.
- Texto longo não quebra o layout: `min-width: 0` em filhos flex, `overflow-wrap`, `line-clamp` onde couber.
- Ação destrutiva pede confirmação ou oferece desfazer.
- Data, moeda e número no formato do locale (é o que o `i18n` da Forja já faz).
- Nada de bloquear zoom (`user-scalable=no`).

## 5. O passe (seção 9, depois do pior caso e antes da auto-revisão)

1. **Contagens**:

   ```bash
   python3 build/slop_check.py project --radii <escala do contrato> [--allow-gradient <arquivo>]
   ```

   Metas: matizes saturados ≤ 4 (acento + apoio + erro + ok), **0** raio fora da escala, **0** emoji em navegação, botão ou título, **0** gradiente de lavagem sem motivo escrito, **0** palavra ou frase de slop, **0** FAIL de interface. Corrija todo FAIL. Para cada WARN, corrija ou escreva o porquê no `design_brief.py`. Os INFO de rótulos diferentes para o mesmo destino você confere à mão: a navegação pode ter nome curto, a ação primária não pode mudar de nome.

2. **Portão de 6 perguntas**, uma linha de resposta cada, gravadas em `build/anti_slop.md`:
   - **Específico**: esta tela funcionaria sem mudança para um concorrente? Se sim, o que muda nela?
   - **Evidência**: qual decisão foi resolvida por uma referência real (produto, pesquisa, foto da realidade do usuário) e o que ela mudou?
   - **Estados**: vazio, carregando, erro e pior caso foram vistos com conteúdo real?
   - **Conteúdo**: sobrou nome de exemplo, número redondo inventado ou texto que ninguém do produto diria?
   - **Hierarquia**: qual é o elemento dominante de cada tela-chave, e um estranho apontaria o mesmo?
   - **Limites honestos**: o que não foi renderizado, testado ou corrigido?

   Um "não" é trabalho que falta, não motivo para baixar a régua.

   **Crítica com rubrica** (do `critique` do Impeccable), gravada no mesmo arquivo para as telas-chave:
   - **Carga cognitiva**, 8 itens: foco único, grupos de ≤ 4, agrupamento visível, hierarquia, uma decisão por vez, ≤ 4 opções visíveis num ponto de decisão, nada para decorar de uma tela para outra, revelação progressiva. 0–1 falha = ok; 2–3 = corrigir; 4+ = crítico.
   - **Heurísticas de Nielsen** de 0 a 4 cada (4 é excelente de verdade), e cada problema com severidade **P0–P3** (P0 bloqueia a tarefa).
   - **Revisão de movimento** (Emil, `review-animations`): liste cada animação com a causa; aprove ou bloqueie; o que não ajuda a entender sai (`remove-animations`); 60 fps; overshoot só em celebração.
   - **Originalidade** (MengTo, `audit-reference-originality`): compare as telas com as referências do Mobbin/Appllama usadas; se alguma tela parece cópia de uma referência (layout, texto e ordem iguais), refaça.

3. **Feche o ciclo**: corrija em lote, renderize de novo as telas e tamanhos afetados (390 e 1440, DE incluso), olhe as capturas e rode o `slop_check.py` outra vez. Pare quando passar; não invente trabalho. Se algo não se resolve no escopo, vai para "problemas conhecidos" da entrega.

## 6. Na entrega e no handoff

- A entrega cita: as contagens finais do `slop_check.py`, os WARN mantidos com o porquê, e as 6 respostas.
- O `DESIGN.md` do handoff carrega o contrato da seção 1 e as metas da seção 5, para o Claude Code manter as mesmas regras na implementação (e rodar o `web-design-guidelines` da Vercel no código React/Expo).
