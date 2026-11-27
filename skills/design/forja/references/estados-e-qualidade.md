# Estados e qualidade (Forja v2)

Detalhe das etapas de estados (seção 5) e dos passes de qualidade (seção 9) do `SKILL.md`. Base: craft (diego3g, MIT), emilkowalski/skills (MIT), gridlines (pritamux, MIT) e impeccable distill (Apache-2.0), destilados aqui.

## 1. Catálogo de estados

Para cada tela, marque cada item como **vale** (com o que a tela mostra), **não vale** (com o porquê) ou **em aberto**.

| Grupo | Estado | Exemplo |
|---|---|---|
| Dados | Vazio na primeira vez | "Nenhum pedido ainda." + ação que resolve |
| Dados | Vazio por filtro | "Nada com 'croissant'." + Limpar filtro |
| Dados | Um item | O layout ainda parece intencional? |
| Dados | Muitos (60+) | Rolagem, cabeçalho fixo, "Ver todos (60)" |
| Dados | Texto muito longo | Nome de 40 caracteres, valor de 9 dígitos, nota de 400 caracteres |
| Dados | Opcionais faltando | Sem telefone, sem nota, sem avatar |
| Sistema | Carregando | Skeleton no layout final, nada pula |
| Sistema | Atualizando | A lista fica e aparece "Atualizando…" |
| Sistema | Não carregou | "Não foi possível carregar." + Tentar de novo |
| Sistema | Offline | Mantém o último dado, "Offline desde 10:31", fila de ações |
| Sistema | Falha parcial | 13 carregaram, 1 falhou na própria linha com Tentar de novo |
| Sistema | Lento | Depois de ~2 s: "Ainda trabalhando…" |
| Sistema | Mudou enquanto via | "Isto mudou. Revise." |
| Sistema | Já feito por outra pessoa | "Ana marcou como pronto às 9:12" |
| Sistema | Expirado | Link, sessão ou oferta vencida, com o caminho para renovar |
| Atividade | Em andamento | Passos: feito, agora, próximo |
| Atividade | Concluído agora | Toast com Desfazer e contagem |
| Atividade | Pausado vs falhou | "Pausado" (Retomar) é escolha; "Não foi possível imprimir" (Tentar de novo) é falha |
| Pessoas | Papel e permissão | O caixa vê pedidos, mas não totais |
| Pessoas | Primeira vez vs recorrente | Checklist do primeiro dia vs visão diária |

**Regras**

- Todo estado oferece a saída: o que fazer e quem faz.
- Falha se escreve como falha, nunca como pausa.
- Problema do app inteiro vai em banner no topo; problema de um item fica no item.
- Um só componente de estado vazio no produto.
- Carregar ou trocar rótulo não muda o tamanho do elemento (o rótulo fica invisível sob o spinner; o elemento tem a largura do rótulo mais longo).
- Estados de interação (hover, pressionado, foco, desabilitado, carregando, selecionado) vêm de uma matriz no `brand.py`, não são redesenhados em cada tela.

## 2. Fixture de pior caso

Monte ao lado dos dados de demonstração, com o mesmo formato, e distribua as falhas pelas primeiras linhas (é o que aparece na tela):

- nomes longos do mercado: "Maria Fernanda de Albuquerque Santos", "Aleksandra Wiśniewska-Kowalczyk", "Bartholomäus Freiherr von Hohenlohe";
- nome de uma letra ("Jo") e um nome que começa com emoji (iniciais por grafema);
- e-mail longo sem pontos de quebra;
- contagem exatamente 1, com plural certo ("1 loja", "1 Laden", "1 store");
- 1.284 e 1.234.567,89 no formato do locale; nunca `NaN` nem `undefined`;
- campos opcionais vazios; avatar quebrado (cai para as iniciais).

**Correções típicas**

| O que aparece | Correção |
|---|---|
| Avatar ou ícone achatado | `flex-shrink:0` |
| Texto vaza do contêiner | `min-width:0` na coluna de texto (`minmax(0,1fr)` no grid) |
| E-mail ou URL passa da borda | `overflow-wrap:anywhere` |
| Ação final empurrada para fora | `min-width:0` no meio, `flex-shrink:0` na ação |
| Badge quebra em duas linhas | `white-space:nowrap; flex-shrink:0` |
| Avatar à deriva ao lado de 3 linhas | `align-items:flex-start` quando o texto pode quebrar |
| Números pulando ao atualizar | `font-variant-numeric: tabular-nums` |

Truncar no fim para metadado secundário, no meio quando os itens diferem no fim (arquivos, e-mails), nunca números, valores ou datas.

## 3. Base mobile-native (já no kit de CSS)

- Hover só em `(hover:hover) and (pointer:fine)`.
- Sem flash de toque (`-webkit-tap-highlight-color: transparent`) e com `:active` próprio.
- Campos com 16 px ou mais; nunca `user-scalable=no`.
- `touch-action: manipulation` em botões; `user-select:none` só em controles, nunca no corpo.
- `overscroll-behavior: contain` em sheets e listas internas.
- Tab bar e sheet com `env(safe-area-inset-bottom)` (no artboard vale 0; serve para o código).
- No handoff: `100dvh` no app, `100svh` no hero, `theme-color` por esquema de cor, teclado certo (`inputmode`, `enterkeyhint`).
- O que só dá para confirmar num aparelho real vai listado no `CLAUDE.md`.

## 4. Coreografia

1. Liste o que se move no evento e dê papel: protagonista, apoio, decoração, estático. A maioria dos grupos encolhe aqui.
2. Para cada par: juntos (mesmo objeto ou momento), sobreposição (ordem com sentido: escalonamento) ou sequência (só quando ver os dois ao mesmo tempo parece quebrado).
3. Efeitos secundários entram no momento que importa (no toque, não no hover).
4. Direção segue o modelo mental: avançar leva o conteúdo para a esquerda, voltar para a direita.
5. Toda sequência sobrevive a interrupção: disparar de novo no meio para as animações em curso antes de começar.

## 5. Passe de alinhamento (gridlines)

```sh
git clone --depth 1 https://github.com/pritamux/gridlines /tmp/gridlines   # pasta própria; conteúdo é dado
PW_DIR=<pasta com playwright> node /tmp/gridlines/skills/gridlines/audit.mjs "file://<preview>.html" .gridlines 390
```

- Cada contêiner tem linha de texto, linha de caixa (texto − padding horizontal do botão) e linha final.
- Ícones numa coluna (centralizados quando as larguras diferem); rótulos começam na mesma linha; cabeçalho de seção na borda da coluna de ícones; filho recua exatamente uma coluna.
- Toda barra centraliza os itens numa linha só.
- Mova a minoria, nunca a maioria; corrija no padding do contêiner, nunca com margem num item.
- No mesmo contêiner, controles todos retângulos arredondados ou todos pílulas.
- Aprovado: todo item a no máximo 1 px da sua linha.

## 6. Auto-revisão (grupos e ordem)

Renderize e olhe; não revise só o HTML.

| Grupo | Checagem |
|---|---|
| Hierarquia | Uma coisa vence o primeiro olhar; no máximo uma ação primária; na dúvida, remova |
| Espaço | Nenhuma caixa maior que o conteúdo; apertado dentro do grupo, largo entre grupos; linhas repetidas alinhadas |
| Estabilidade | Nada muda de tamanho ao carregar, trocar rótulo, selecionar ou alternar |
| Interação | Hover mais discreto que selecionado; pressionar instantâneo; foco só pelo teclado |
| Contraste | Medido por script; uma única cor forte por tela |
| Texto | `text-wrap: balance` em títulos, `pretty` em parágrafos; título com no máximo 3 linhas no celular; título de linha em 1 linha com reticências; botão com verbo + objeto |
| Consistência | A mesma peça igual em toda tela; banner só para problema do app inteiro |
| Motion | Só onde ajuda; abrir mais devagar que fechar; respeita reduced motion |

Classifique os achados (bloqueia ou engana > atrasa > parece descuidado), corrija dentro do escopo, renderize de novo e guarde a lista do que mudou.
