# Conteúdo: o que cada seção da documentação contém

Escreva tudo como dados Python em módulos (`content_a.py`, `content_b.py`, `content_c.py`) e valide com `assert`: total de pontos, histórias por sprint, cada história em exatamente um sprint, MoSCoW, entidades. Não faça essas contas de cabeça. Os mesmos dados alimentam `trace.json` (gere-o a partir dos módulos, não à mão).

As quantidades abaixo são do modo **Padrão**. No modo **Completo** elas podem crescer, desde que cada item novo passe pela escada de escopo e entre no `trace.json`.

## 01 · Product Vision Board (Pichler estendido)

- **Visão**: 1 frase.
- **Público**: 4 grupos. Quem paga, canal de revenda, beneficiário final e parceiro de indicação.
- **Necessidades**: por grupo.
- **Produto**: 5–6 capacidades.
- **Objetivos de negócio**: 4.
- **Receita, custos e canais**: preço marcado como hipótese (`claims.json`, status `hypothesis`).
- **Matriz competitiva**: 5 alternativas. A coluna do concorrente real fica destacada, seguida de um parágrafo "por que ele é o concorrente real". Cada célula ✓ / ½ / × que afirma algo sobre um concorrente tem fonte no registro.

## 02 · PRD

- **Contexto**: fatos com fonte.
- **Hipótese central**: 1 frase de efeito + teste mensurável. Exemplos: "O relatório não é o produto — a prova é." / "O registro não é o produto — a conversa com o profissional é."
- **7 objetivos**: ID, objetivo, linha de base, meta.
- **3 personas** (mais 1 por segundo ator): iniciais, nome e idade, papel, contexto, 3 objetivos, 3 frustrações, citação.
- **Escopo**: dentro e fora da v1.
- **32 requisitos funcionais em MoSCoW**: cerca de 20 Must, 9 Should, 2 Could e 1 Won't explicado.
- **12 requisitos não funcionais**: inclua "o próprio produto cumpre WCAG 2.1 AA".
- **12 regras de negócio**: trial, limites, validade, cancelamento, linguagem jurídica segura.
- **Regras do domínio** (quando sensível): "nunca" e "sempre" do produto. Ex. saúde: nunca recomendar ou calcular dose; nunca dizer que trata, cura ou previne; sempre aviso fixo em estimativas.
- **8 riscos**: probabilidade, impacto, mitigação.

## 03 · User Flows

7 fluxos, cada um com:
- ator e gatilho;
- passos numerados marcados como **pessoa** ou **sistema** (sistema destacado em roxo);
- exceções.

Cada passo aponta para uma tela (`board`) e, quando há interação, para o seletor e o resultado esperado. É isso que a réplica de fluxos executa. O diagrama de cada fluxo segue `diagramas.md` (swimlane quando há dois atores, process quando é um).

## 04 · User Stories

- 8 épicos e 38 histórias no formato "Como…, quero…, para…".
- Critério de aceite testável, pontos Fibonacci e prioridade.
- Resumo por épico.
- Total de pontos convertido em sprints semanais de cerca de 40 pts, coerente com o cronograma de 60 dias.

## 05 · ARD

- 4 princípios.
- **Stack conforme o produto** (registre como ADR):
  - SaaS web: TanStack Start + React + TS, PostgreSQL + Drizzle, fila no Postgres, workers isolados.
  - App mobile: Expo + Expo UI; local-first quando a privacidade é argumento.
  - Hospedagem na UE quando o mercado é europeu.
- 6 camadas, com diagrama (tipo `layers` ou `architecture`).
- 22 entidades, com as imutáveis marcadas (diagrama `er` se ajudar).
- Cerca de 30 endpoints.
- 12 eventos e automações.
- **IA**: tabela por função (onde roda, entrada, saída, validação, confirmação do usuário, custo).
- **Proteção de dados**: DSGVO ou LGPD, conforme o mercado. Inclua sempre **um caso delicado** resolvido e a lista de subprocessadores.
- Ambientes.
- 7 ADRs: contexto, decisão, consequências + e −.

## 06 · Cronograma e critério de aceite

- Gantt de sprints e marcos (tipo `gantt`).
- **Critério de aceite da v1** em 1 frase. Ex.: "Da URL à declaração publicada em menos de 30 minutos — sem falar com ninguém."
- 8 condições verificáveis, cada uma rastreada a uma US ou RNF.

## Consistência

Personas, domínios fictícios (`.example`), marcas fictícias, números e status precisam ser os mesmos em telas, documento, pitch e em todos os idiomas. O `check_claims.py` pega números; nomes e status você confere na revisão de texto.
