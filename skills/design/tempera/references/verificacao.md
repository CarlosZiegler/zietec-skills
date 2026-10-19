# Verificação (harness)

Toda verificação acontece localmente, antes de publicar. O tipo Design pede para não verificar depois de publicar sem o usuário pedir.

O ciclo, adaptado do "Verification Harness for Coding Agents":

| Passo | No pacote de produto |
|---|---|
| Reproduzir | Renderizar cada artboard no estado padrão e guardar a linha de base (screenshot + altura) |
| Instrumentar | Rodar os scripts e a réplica de fluxos; coletar erros de console |
| Corrigir | A menor correção justificada; nada de refazer o que passou |
| Repetir | Rodar de novo a mesma réplica e comparar com a linha de base |
| Prevenir | Correção repetida vira checagem em script ou regra na skill |

Reaproveite o harness: os scripts desta pasta e o renderizador mínimo são os mesmos em toda rodada. Não invente um setup novo a cada projeto.

## 1. Fontes locais

`curl` com user-agent de Chrome em `fonts.googleapis.com/css2?...`, depois baixe os woff2 e gere um `local.css`. Nunca desligue TLS.

## 2. Renderizador mínimo

Preenche `{{hole}}`, `sc-for` e `sc-if` com o estado padrão e remove `support.js` e o bloco de lógica. Serve para medir a altura natural e tirar screenshots. Para a réplica de fluxos, use a versão que mantém a lógica: rode a `class Component` com um `DCLogic` falso e re-renderize a cada `setState`.

## 3. Scripts

```bash
# afirmações: valores nas peças x registro; fontes e datas dos verified
python3 scripts/check_claims.py claims.json project/
# rastreabilidade: cobertura e arquivos existentes
python3 scripts/check_trace.py trace.json --root project/
```

- Saída 0 = passou; 1 = há erros (listados). Avisos não reprovam, mas entram no pacote de evidências.
- `check_claims.py` procura valores com moeda (€, US$, R$, $), percentuais e magnitudes (mil, mi, bi, k, M) no texto visível de `.html`, `.md` e `.json` de conteúdo. Medidas de layout (px) e números soltos são ignorados. Valores legítimos que não são afirmações vão em `"ignore"`.
- Os scripts usam só a biblioteca padrão do Python 3.

## 4. Réplica de fluxos

Para cada fluxo do `trace.json`:
1. abra a tela do primeiro passo no Chromium (Playwright) com o renderizador que mantém a lógica;
2. execute `do` (`click <seletor>`, `fill <seletor> <texto>`, `goto <tela>`);
3. confira `expect` (texto visível, elemento presente, estado do `sc-if`);
4. screenshot por passo em `verify/flows/<fluxo>/<n>.png`;
5. erro de console reprova o passo.

Passo que não pôde rodar (tela estática, interação fora do runtime) é marcado "não verificado", nunca "ok".

## 5. Checagens por artboard

- overflow horizontal e vertical;
- lógica: cada `class Component` no Node com um DCLogic falso; chame os handlers e confirme que todo hole do template existe em `renderVals()`;
- JSON do `data-props` válido;
- nenhum `{{` fora do lugar;
- contraste medido; alvos ≥ 44 px (segmented de 34–36 é aceitável);
- estados vazio e erro presentes;
- teste "parece feito por IA?" (lista em `visual.md`).

Screenshots em modo reduced-motion (estado final) e alguns no meio da animação (scan, sheet, contagem). Olhe todos.

## 6. Consistência entre idiomas e peças

- Mesmo conjunto de telas por idioma (compare a lista de `id`).
- Mesmos valores por idioma (o `check_claims.py` cobre os números; compare também nomes de persona e marcas fictícias).
- Telas mostradas no pitch existem e estão na mesma versão.

## 7. Revisão de texto

Uma passada nas frases contra regras fixas, como um lint:
- regras do domínio do PRD (ex.: nenhuma recomendação de dose; nenhum "trata", "cura", "previne");
- sinais de design ou texto gerado por IA;
- idioma certo em cada peça e nas notas de fala;
- nomes de pessoas e empresas iguais ao `people` do registro;
- hipóteses marcadas como hipótese onde aparecem.

## 8. Revisão de design

Antes de publicar: contraste medido, alvos, estados, consistência de componentes, teste "parece feito por IA?". Corrigir antes de publicar.

## 9. Limites

- 2 tentativas falhas na mesma checagem: pare e reporte o que tentou, o que observou e o que precisa do usuário.
- Ferramentas externas de revisão que enviam dados para fora (ex.: modos "Pro" de design-review, `npx impeccable` do critique) só com pedido explícito.

## Lições registradas

Acrescente aqui, com data, cada correção que virou regra.

- 2026-10 · Doro: nome de quem apresenta o deck errado → pessoas reais só do brief (`people`).
- 2026-10 · Doro: cenário com taxa diferente do modelo base → cenários herdam taxas; diferença vira afirmação própria.
- 2026-10 · Doro: limite de 511 arquivos atingido → orçamento antes do build.
- 2026-10 · Doro: decks com Inter → revisão visual vale para decks.
