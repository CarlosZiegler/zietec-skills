# Têmpera

**Da ideia ao pacote de produto verificado.** A forja dá forma; a têmpera endurece.

Têmpera parte da skill **forja** (um canvas do Claude Design com telas mobile e desktop, pitch e documentação A4) e acrescenta o que faltou quando o pacote cresceu no piloto Doro: provar cada afirmação, rastrear cada tela até uma história, repetir os fluxos como um usuário e entregar um relatório dizendo o que ainda não foi verificado.

A forja continua existindo sem alteração. Use as duas lado a lado para comparar.

## O que muda em relação à forja

| | Forja | Têmpera |
|---|---|---|
| Início | Perguntas de entrada | Modo (rápido, padrão, completo, pitch para destinatário, passagem para build) + reformulação do pedido |
| Números | "Nunca invente" | `claims.json` com status, fonte e data; script cruza com telas, doc e pitch |
| Escopo | Conjunto fixo de 9 telas | Escada de escopo (inspirada no Ponytail) + orçamento de 511 arquivos |
| Coerência | Revisão manual | `trace.json`: história → requisito → fluxo → tela → slide, checado por script |
| Verificação | Checagens por artboard | + réplica de fluxos, consistência entre idiomas, revisão de texto |
| Diagramas | Livre | Regras do Diagram Design (grade de 4 px, um acento, sem sombras) e Anatomy para explicativos vivos |
| Stack no ARD | TanStack Start fixo | Conforme o produto, registrada como ADR |
| Pitch | 14 slides para público genérico | + modo para destinatário real, com pesquisa pública e documento interno |
| Mudanças | — | Changelog + lista de propagação em todas as peças e idiomas |
| Entrega | Resumo curto | Pacote de evidências: gerado, checagens, hipóteses, não verificado, melhoria proposta |
| Depois | — | Passagem para build: roadmap, ADRs, `docs/`, skills de agente |

## Estrutura

```
tempera/
├── SKILL.md                      # fluxo completo e portões
├── references/
│   ├── conteudo.md               # Vision Board, PRD, flows, stories, ARD, cronograma
│   ├── canvas-e-telas.md         # canvas, nomes, layout, telas e portal
│   ├── visual.md                 # tokens, tipografia, componentes, CSS de motion
│   ├── diagramas.md              # Diagram Design, gráficos, Anatomy
│   ├── documento-e-pitch.md      # paginação A4 e roteiros de pitch
│   ├── verificacao.md            # harness, réplica de fluxos, lições
│   └── passagem-build.md         # pacote docs/ e skills de agente
└── scripts/
    ├── check_claims.py           # valores nas peças x registro de evidências
    └── check_trace.py            # cobertura do mapa de rastreabilidade
```

Os scripts usam só a biblioteca padrão do Python 3.

## Referências

- Verification Harness for Coding Agents (fluxo reproduzir → instrumentar → corrigir → repetir → prevenir)
- [Ponytail](https://github.com/DietrichGebert/ponytail) — escopo mínimo sem cortar validação, segurança e acessibilidade
- [Diagram Design](https://github.com/cathrynlavery/diagram-design) — diagramas editoriais em HTML + SVG
- [Anatomy](https://skills.wheresryan.sh/anatomy) — explicativos como objetos vivos
