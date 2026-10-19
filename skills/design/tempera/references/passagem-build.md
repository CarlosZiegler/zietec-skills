# Passagem para build

Modo opcional, depois do pacote aprovado. O objetivo: um agente de código abre o repositório e encontra tudo o que precisa sem perguntar ao usuário.

## 1. Pacote `docs/<produto>/`

| Caminho | Conteúdo |
|---|---|
| `README.md` | Ordem de leitura, tabela de conteúdo e links dos artifacts originais |
| `ROADMAP.md` | Escopo, referências, stack, resumo dos ADRs, fases, épicos e tarefas, blockers, Definition of Done, riscos |
| `AGENTS.<produto>.md` | Regras do produto para anexar ao `AGENTS.md` da raiz |
| `prd/` | Documentação de produto em markdown, um arquivo por idioma |
| `adr/` | Um arquivo por ADR |
| `design/SCREENS.md` | Índice de telas gerado do `trace.json` (título, área, histórias, links) |
| `design/screens/<lang>/` | Telas em HTML |
| `design/png/` | Renders de página inteira |
| `design/diagrams/` | Diagramas do ARD e do roadmap |
| `design/TOKENS.md` | Cores, tipografia, sombras e cores de gráfico |
| `data/` | Seeds de domínio (catálogos, listas) |
| `research/` | `claims.json` e pesquisas em JSON |
| `trace.json` | O mesmo mapa da verificação |

## 2. Roadmap mastigado

- IDs estáveis: `EP-NN` (épico), `T-N.N` (tarefa), `BL-NN` (blocker), `ADR-NN`, `Q-NN` (pergunta aberta).
- Cada tarefa: referências (US, RF, telas, ADRs), passos, "pronto quando" testável, "depois" (o que desbloqueia).
- Blockers listam o que travam e quem destrava (jurídico, parceiro, decisão do usuário).
- Épicos futuros ficam em tabela, sem tarefas; o agente quebra em tarefas num PR próprio antes de começar.

## 3. Skills de agente do produto

Gere em `.agents/skills/` (ou na pasta de skills do repositório) no mínimo:
- `<produto>-design-reference`: como achar a tela certa, tokens, i18n.
- `<produto>-<dominio>-compliance`: as regras "nunca" e "sempre" do PRD, com checklist de PR.
- `<produto>-verification`: os fluxos do `trace.json` como roteiros para rodar o app de verdade (Playwright no web, simulador no mobile), com linha de base e pacote de evidências. É a ponte com o harness de código: reproduzir, instrumentar, corrigir, repetir, prevenir.
- Uma skill de arquitetura quando há uma regra que não pode quebrar (ex.: `local-first`: dado de saúde nunca chega ao servidor em texto puro).

## 4. Regras de execução para os agentes

- Reformular a tarefa nas próprias palavras antes da primeira edição.
- Reproduzir na `main` atual antes de corrigir; guardar a linha de base.
- Menor mudança justificada; reaproveitar o que existe antes de escrever código novo.
- 2 tentativas falhas → escalar.
- Merge, gasto e publicação → aprovação.
- Relatório final em linguagem simples, com o que continua sem verificação.
- Correção repetida vira regra, lint ou skill antes de aumentar a autonomia.
