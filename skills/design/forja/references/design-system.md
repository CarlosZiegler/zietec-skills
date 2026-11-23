# Design system (craft-system, de diego3g/craft, MIT)

Todo pacote Forja sai com **um design system de verdade**, não só com telas parecidas entre si. Ele nasce logo depois da direção de arte (seção 4) e antes das 9 telas, e todas as telas usam as peças dele.

Origem: `craft-system`, `craft-setup` e `craft-sync` do diego3g/craft (MIT), destilados aqui. Não instale o plugin (ele põe um hook em toda sessão).

## 1. Camadas, nesta ordem (craft-system · create)

1. **Fundamentos**:
   - cores **por papel**, nunca só por valor: `bg`, `surface`, `text`, `text-muted`, `border`, `border-hover`, `fill-1`, `primary`, `primary-pressed`, `accent`, `accent-soft`, `focus`, `success`/`warning`/`danger` com `-bg`, e o vidro (`glass-bg`, `glass-edge`, `glass-shadow`), em claro e escuro;
   - escala de tipo nomeada por uso (`caption` → `display`), com tracking e entrelinha;
   - espaçamento em 4 px;
   - raios (a escala do contrato anti-slop);
   - **no máximo duas sombras**, só para coisas que flutuam;
   - larguras de layout;
   - durações e curvas de motion;
   - um bloco "como escrevemos" (voz, verbo + objeto, números).
2. **Regras de interação, uma vez só**, para três famílias:
   - **com borda**: no hover, só a borda escurece;
   - **sem borda**: tom translúcido;
   - **ação primária**: escada própria.

   Para cada uma: hover, pressionado, foco (só pelo teclado), desabilitado, carregando (mantém o tamanho exato) e selecionado (mais forte que o hover e sem mudar o peso da fonte).
3. **Componentes, um por vez, na ordem em que as telas precisam deles**. Cada um com:
   - anatomia: legenda com a regra e o porquê, e exemplos;
   - **matriz de estados**: variantes × normal, hover, pressionado, foco, desabilitado, carregando, selecionado;
   - linha no **índice de componentes** (nome, variantes, telas que usam).

   Mínimo de um app Forja: Botão (primário, secundário, texto, perigo, só ícone), Botão de vidro circular, Campo de texto, Campo de código, Chip/filtro, Segmentado, Linha de lista, Grupo de seleção (radio/check), Cartão, Número-herói, Barra de progresso/anel, Chip de status, Avatar, Tab bar, Barra de CTA, Sheet, Toast, Diálogo, Item de navegação lateral e Linha de tabela.

Sem ninguém para aprovar, siga direto e deixe "aprovar" na entrega. Com o usuário presente e sem pressa, mostre os fundamentos antes dos componentes.

## 2. Regras firmes (craft)

| Regra | Por quê |
|---|---|
| Toda cor é token; nenhum hex solto nas telas | Valor solto vira quase-duplicata que ninguém muda de uma vez |
| Um conjunto de ícones | Conjuntos misturados parecem produtos misturados |
| Toda peça interativa tem matriz de estados | Estado desenhado na tela nunca concorda com o de outra tela |
| Mudou uma peça compartilhada: liste as telas afetadas antes | Senão uma mudança "pequena" redesenha vinte telas |
| Uma ação primária por tela | Duas primárias = a tela não decidiu |
| Itens empilhados de lista e menu com respiro, nunca encostados | Os destaques se fundem num bloco só |

## 3. Onde ele mora

1. **Artifact do tipo Design System** ("<Produto> · Design System"), criado com `create_from_type` (tipo "Design System"):
   - `project/README.md` (o brand book), `project/tokens.json` (listas, no formato do tipo), `components/<Comp>/README.md` e `preview.html` com cada matriz de estados, `components/bundle.css` com as classes, e a capa (`components/Cover/preview.html`);
   - siga as instruções que o `create_from_type` devolve.
2. **Instalado no canvas** do pacote, como manda o tipo Design (passo 4):
   - `project/ds/<pasta>/tokens.json` copiado do sistema;
   - registro em `designSystems` no `canvas.json`.

   O menu Tema do canvas passa a mostrar os tokens.
3. **Páginas "Design system" no canvas**: Fundamentos, Regras de interação, Componentes (matrizes) e Índice, desenhadas com as próprias peças.
4. **No código das telas**: as cores e medidas saem de `var(--token)`, gerado a partir do `tokens.json`. O passe de auditoria (seção 4) conta os hex soltos.
5. **No handoff**:
   - `DESIGN.md` com o link do sistema e o índice de componentes;
   - `tokens.json` junto, para o Claude Code gerar os tokens do app (craft-sync: o código passa a ser a fonte depois da implementação).

## 4. Auditoria (craft-system · audit), antes da entrega

Relatório por severidade:
- hex soltos fora do `tokens.json`;
- quase-duplicatas (`#f3f3f6` × `#f2f2f5`);
- raios e espaçamentos fora da escala;
- peças sem matriz de estados;
- telas usando variação local em vez de uma variante.

Na Forja, quem constrói é o próprio agente, então corrija tudo o que for mecânico e reporte o resto. Num pacote do usuário que já existe, só reporte e espere ele escolher o que corrigir.

## 5. Lição do Salles Squad

Na matriz, peça de vidro **precisa de conteúdo real por trás**: uma foto do produto recortada na célula. Formas soltas (bolinha colorida + barras cinzas) parecem defeito, e texto atrás vira ruído. No artifact Design System, envie a foto como asset e use a URL `/_blob/` nos previews.
