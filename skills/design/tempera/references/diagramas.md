# Diagramas, gráficos e explicativos

Três ferramentas, cada uma para um trabalho. Se a skill correspondente estiver instalada na sessão, carregue-a e siga-a; se não, use as regras destiladas aqui. Em qualquer caso, os tokens vêm do produto (`visual.md`), não do padrão de cada ferramenta.

**Primeiro teste:** um leitor aprende mais com o desenho do que com um parágrafo bem escrito ou uma tabela? Se não, não desenhe. Comparação antes/depois e listas viram tabela.

| Precisa mostrar | Use | Onde aparece |
|---|---|---|
| Estrutura, fluxo, sequência, estado, cronograma, matriz | **Diagram Design** (editorial, HTML + SVG estático) | ARD, User Flows, Gantt, matriz competitiva, slides |
| Números (tendência, comparação, composição) | Regras de gráfico abaixo (e a skill `dataviz` se existir) | Doc, pitch, telas de progresso |
| Como um mecanismo funciona, de um jeito que se veja mexendo | **Anatomy** (objeto isométrico vivo) | No máximo 1 por pitch ou landing, só com aprovação |

---

## 1. Diagram Design (padrão para o doc e o pitch)

Fonte: https://github.com/cathrynlavery/diagram-design (MIT).

### Plano antes de desenhar
Declare em uma linha: tipo visual, tamanho (doc-inline, doc-wide, slide-16x9, print-a4) e o que o orçamento vai cortar. Se o usuário pode responder, deixe ele redirecionar.

### Tipo por seção do pacote
- Camadas do ARD → `layers` ou `architecture`
- Entidades → `er` ou `db-schema`
- Fluxo com 2 atores (paciente e profissional) → `swimlane`; com 1 ator → `process` ou `flowchart`
- Link cifrado, autenticação → `sequence`
- Ciclo de vida de um link ou assinatura → `state`
- Cronograma → `gantt`
- Jornada → `journey`; mapa de histórias → `story-map`
- Concorrência em 2 eixos → `quadrant`
- Funil de conversão do modelo de receita → `pyramid` (funil) ou `waterfall`

### Sistema (mapeado para os tokens do produto)
| Papel | Valor |
|---|---|
| Papel (fundo) | fundo do app (`#F4F5F7`) |
| Card | `#FFFFFF` |
| Tinta | texto (`#16171A`) |
| Muted (setas padrão) | texto secundário (`#5B606B`) |
| Acento | cor da marca, em **1–2 elementos** no máximo |
| Link (chamadas de API) | ação (`#0A62D0`) |
| Hairlines | tinta a 10–12% de opacidade |

- **Grade de 4 px**: toda coordenada, largura, altura, gap e tamanho de fonte é divisível por 4 (exceto espessura de traço e opacidade). Fontes 8, 12, 16, 20, 24, 28, 32, 40. Gaps 20–48. Padding 8, 12, 16. Raio 4, 6, 8 (`rx="6"` em caixas).
- **Sem sombras**, linhas de 1 px.
- Nós: focal = tinta do acento + traço do acento; serviço = branco + traço de tinta; armazenamento = tinta a 5% + traço muted; externo = tinta a 3%; opcional/assíncrono = tracejado `4,3`; fronteira de segurança = acento a 5% + tracejado `4,4`.
- Mono só para strings técnicas (portas, URLs, tipos).

### Conectores
- Setas desenhadas antes das caixas. Cotovelos em ângulo reto com raio 8; nada diagonal.
- Rótulo de seta com máscara opaca na cor do papel e folga visível de 6–10 px do traço.
- Conectores nunca se sobrepõem; paralelos com ≥ 12 px; cruzamentos com ponte.
- Cada conector chega num ponto próprio da borda, ≥ 12 px dos outros.
- Nenhum conector passa por trás de uma caixa que não é sua ponta.

### Orçamento
Densidade alvo 4/10. Até 9 nós, 12 setas e 2 elementos com acento. Acima disso, divida em dois diagramas. Teste da remoção: corte nós dispensáveis, junte os que sempre andam juntos, tire setas óbvias pelo layout.

### Legenda e acessibilidade
- Legenda numa faixa horizontal abaixo, atrás de uma hairline; nunca flutuando dentro do desenho.
- `<svg role="img" aria-labelledby="…">` com `<title>` (≤ 60 caracteres) como primeiro filho e `<desc>` de uma frase sobre o conteúdo. IDs prefixados por diagrama e idioma.
- Estático por padrão; motion só com quadro final completo e respeito a `prefers-reduced-motion`.

### Reprovação automática
Glow ciano ou roxo em fundo escuro, caixas idênticas para tudo, acento em muitos nós, grade de três cards iguais, sombras, texto vertical, rótulos de seta sem máscara, layout automático estilo Mermaid.

### Dentro do canvas
O diagrama vira SVG inline dentro do artboard (doc A4 ou slide), com as fontes do produto. Ao paginar o doc, o diagrama é um átomo `keep_whole`.

---

## 2. Gráficos

- Um gráfico, uma pergunta; o título diz a conclusão ("Peso caiu 6 kg em 12 semanas"), não o tipo.
- Barra começa no zero; linha pode não começar, com o eixo indicado.
- Rótulo direto na série em vez de legenda quando houver até 4 séries.
- Cor: a marca para a série principal, cinzas para o contexto. Nunca a cor sozinha carrega o significado.
- Números com `tabular-nums`; o valor exato num `.sr` para leitor de tela.
- Todo número de gráfico vem do `claims.json` ou dos dados fictícios declarados da persona.
- Estimativas (ex.: curva de nível de medicamento) levam aviso fixo visível no próprio gráfico.

---

## 3. Anatomy (explicativo vivo, opcional)

Fonte: https://skills.wheresryan.sh/anatomy (MIT). Princípio: **o objeto é a explicação**. Em vez de caixas e setas, um objeto real, isométrico, cujas peças fazem o que a ideia faz.

Use só quando:
- o produto tem um mecanismo central que fica claro ao se mexer (ex.: o link cifrado como um cofre com duas chaves; a fila de transcrição como uma esteira);
- o usuário pediu ou aprovou, porque custa tempo.

Regras destiladas:
- **Tamanho primeiro**: Figure (40–80 peças, 30–90 min), Hero (80–150 peças, 2–4 h, avise antes), Epic (nunca comece sem o usuário; proponha um Hero).
- **Verdade primeiro**: os números e o comportamento viram um pequeno modelo; o movimento, a leitura ao vivo e o texto para leitor de tela leem desse mesmo modelo.
- Câmera isométrica única, sólidos pintados de trás para frente, quatro tons por face, **um único acento**, nada de setas ou balões, texto fora do desenho.
- Vivo: tour ocioso, pausa no hover/foco, teclado, para quando sai da tela, parado com `prefers-reduced-motion`.
- Verificação como crítico: screenshots, recortes a 4×, até não sobrar nada a corrigir.
- Se a skill estiver instalada, ela gera TypeScript que produz SVG/HTML; embuta o resultado como artboard ou artifact próprio (não cabe na conta de 511 se for pesado).

Não instale nem rode scripts externos (`npx`, `pip`) sem o usuário pedir.
