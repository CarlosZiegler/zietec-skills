# Canvas e telas

## Canvas (tipo Design)

1. **Criação**: liste os tipos (`Artifact action=list scope=types`), depois publish com `type_url` + `title` + `auto_open: after_first_write`. Siga as instruções que o tipo devolve; elas valem mais que este arquivo se divergirem.

2. **Páginas** (`canvas.json`): `mobile`, `desktop`, `pitch`, `doc`. No modo Completo, opcionais: `portal` (segundo ator), `estudos`, `indice`. Abertura: `{"view":"canvas","page":"mobile"}`.

3. **Nomes de arquivo**: ASCII, sem espaço. `Main.dc.html` é a landing mobile (a entrada); depois `M-*.dc.html`, `D-*.dc.html`, `P-*.dc.html` (portal), `Pitch-NN.dc.html`, `Doc-NN.dc.html`. Com idiomas em arquivos separados: sufixo `.pt`, `.en`, `.de` antes de `.dc.html`. O `id` no `trace.json` é o nome sem sufixo de idioma.

4. **Layout no canvas**:

   | Página | Posição dos artboards |
   |---|---|
   | Mobile | x = i·470; idiomas em linhas, y = l·1100 |
   | Desktop | landing em x 0, teste grátis em x 1520; grade do app em x 3120 / 4640 / 6160, linhas com +120 |
   | Portal | grade de 3 colunas como a do desktop, começando em x 0 |
   | Pitch | 4 por linha: x = c·2000, y = r·1200 |
   | Documentação | 8 por linha: x = c·874, y = r·1243 |

   - Notas `kind:title1` ficam ≥ 223 px acima de cada linha.
   - Cada página tem 1 sticky amarelo explicando Play, Export PDF ou Tweaks › Idioma.
   - Artboards com links ou estado levam `is_interactive: true`.

5. **Publicar**: uma chamada só, com `root` + `files` em formato de mapa. Arquivo antigo sai com `null`.

6. **Revisar um canvas existente**: leia `project/canvas.json` logo antes de publicar. Preserve chaves desconhecidas (ex.: `attachments`) e mude só as suas.

7. **Limite**: 511 arquivos por versão. Conte antes (etapa 2.3 da SKILL).

8. **Regras que quebram em silêncio**:
   - A linha `<script src="./support.js"></script>` vai exata.
   - Raiz com tamanho fixo igual a w/h e ao `$preview`.
   - Todo atributo entre aspas, inclusive `checked=""`.
   - **Nunca `{{` em texto estático.** Cuidado com amostras de código Liquid ou Twig.
   - Nada de onClick em div: use `<button>`.
   - Holes `{{ x.y }}` são só lookup; calcule tudo em `renderVals()`.
   - No Python 3.11, f-string não aceita barra invertida dentro de `{}`: use variáveis auxiliares.

## Telas

### Mobile (390 px)
- Altura natural, mínimo 844.
- Tab bar absoluta no rodapé do frame.
- **Sem status bar falsa.**
- Conteúdo com `padding-bottom` de cerca de 110 px, para não ficar sob a tab bar.

### Desktop (1440 px)
- Sidebar de 264 px + main com padding 32×40.
- Mesmos componentes do mobile.
- Landing com hero em 2 colunas.
- Páginas web fluidas quando a peça é um site (`expand: fill`).

### Conjunto padrão (9 telas)
1. **Landing**: hero com card do produto sobre um painel na cor da marca, fatos em carrossel com scroll-snap, 3 passos com mini-ilustração de UI, diferencial, preços com toggle Mensal/Anual interativo, bloco de canal/agência, CTA escuro, rodapé.
2. **Primeiro valor**: ex. teste grátis com timeline animada (camada de progresso que some; o resultado entra com atraso de cerca de 2,6 s).
3. **Visão geral**: score em anel, blocos de contagem, "Como próximo passo", alertas.
4. **Lista com filtro**: segmented interativo, `sc-for` sobre dados JSON na lógica.
5. **Detalhe**: ação principal que abre um sheet (`sc-if`) com progresso e depois sucesso (`z-pop`). No desktop vira diálogo centralizado. O scrim é um `<button tabindex="-1" aria-label>` e o sheet tem botão X.
6–8. **Recursos secundários**, conforme o produto.
9. **Visão do canal** (agência/time) com white-label.

O mínimo são **3 interações reais**: toggle, filtro e sheet. A lógica usa `class Component extends DCLogic` com `this.state` e `setState`. Cada interação tem `id` estável no botão para a réplica de fluxos.

### Segundo ator (portal)
Quando outra pessoa consome o produto (profissional, cliente final, agência):
- entrada sem cadastro quando possível (link + senha), com estados de link expirado, revogado e senha errada;
- resumo de uma tela ("me preparo em 2 minutos"), detalhes por categoria e exportação;
- só aparece o que o dono dos dados liberou — e as telas mostram isso.

### Estados obrigatórios
Para cada tela de lista ou dado: vazio, carregando (se houver espera real) e erro. Para cada ação destrutiva: confirmação.
