# Versões, paridade e deck (V2 → V3 → V4 sem perder nada)

Vale quando o pacote já passou da primeira entrega e o usuário pede **uma nova versão** (V3, V4…), não um ajuste no mesmo link. Nasceu no Salles Club. Foram 4 versões em 5 dias, com mais de 500 pranchas, deck de 73 slides e reunião com o cliente. As reclamações que viraram regra:

- "não quero a cada versão perder conteúdos";
- "quero os artifacts organizados";
- "imagens do celular encavaladas, telas cortando";
- "diagramas feios".

Ajuste ou pivô no mesmo link continua em `atualizar-produto.md`.

## 1. Antes de construir: alinhar e inventariar

1. **Alinhe o que vai ser entregue** antes de começar (AskUserQuestion, uma vez). Pergunte quais superfícies entram, se o site/checkout entra, se o deck é atualizado ou novo, e se a entrega sai de uma vez ou em partes. "V4 completa no padrão Forja" quer dizer estados, design system, **todas** as telas e flows, documentação e deck.
2. **Inventário das versões anteriores.** Rode `python3 scripts/parity_check.py --old <proj_v2> <proj_v3> --new <proj_v4> --map state/paridade.json`. A primeira rodada grava o rascunho: o que casa pelo nome vira "mantida" e o resto vira "faltando".
3. Leia também as **notas de reunião** e os pedidos do usuário desde a última versão. Cada pedido vira uma linha no **Mapa de features**, com a feature, a tela onde ela mora e o status. Esse mapa vai numa página do canvas Produto. Feature pedida e sem tela é falha, igual a uma prancha faltando.

## 2. Artifacts organizados

- **Versão nova = artifacts novos.** Nunca sobrescreva V1, V2 ou V3: o cliente pode ter os links. Rodadas dentro da mesma versão (V4.1) republicam os **mesmos** artifacts da V4.
- **Títulos no padrão** `<Produto> · V<n> · <superfície>`: App, Painel, Dono, Site e checkout, Dobráveis, Produto (doc, flows, paridade, mapa de features) e Design System.
- **Páginas na ordem**: Início/índice → telas por fluxo → estados → variantes → idiomas → escuro.
- **Artifact "Índice de entregas"**: uma página simples com todos os links de todas as versões, dos decks e dos docs. A versão atual vem marcada. O deck termina com um slide de links que aponta para ele.
- Na entrega, liste os links agrupados por versão. O usuário vai pedir "todos os links de todas as versões".

## 3. Paridade: nenhuma prancha some

Cada prancha antiga precisa de um destino no `state/paridade.json`, com um destes status:

| Status | Quando |
|---|---|
| mantida | existe na nova, mesma tela |
| trazida de volta | tinha sumido numa versão intermediária e voltou |
| equivalente | outra prancha cumpre o papel (aponte qual) |
| incorporada na doc | virou seção da documentação |
| mudou de canvas | mora em outro artifact da nova versão |
| descontinuada | saiu por decisão; motivo obrigatório (do usuário ou registrado na reunião) |
| fora do canvas | nunca foi prancha (ex.: arquivo de apoio) |
| em aberto | depende do usuário; vira pergunta na entrega |
| faltando | proibido na entrega |

`parity_check.py` falha se houver prancha sem destino, destino inexistente, descontinuada sem motivo ou qualquer "faltando". O mapa vira a página **"Paridade V<n-1> → V<n>"** no canvas Produto, com link para cada prancha. O resumo (contagens por status) vai para a entrega.

Variantes também contam: escuro, EN/ES, 130 %, cores de coleção ou de plano e dobráveis. A documentação também conta: épicos, histórias e regras de negócio da versão anterior continuam na nova.

## 4. Barras fixas e a dobra (o "encavalado")

Achado no Salles V4: o composer do chat cobria a última mensagem, o home indicator riscava texto e a tab bar flutuava com conteúdo aparecendo por baixo. Foram 323 achados, que caíram para 0 depois da correção no kit.

- **A barra ocupa espaço no fluxo.** Tab bar, dock, composer e CTA fixo ficam no fim da coluna (flex), e a `<main class="scr">` rola acima deles. A rolagem termina 8 px acima da barra, e a área segura de 34 px fica livre.
- **Encaixe da dobra no print padrão (390×844).** O último elemento visível termina inteiro, e o resto começa abaixo da dobra. Não deixe título, autor ou rótulo órfão no fim.
- **Versão longa** separada para telas que rolam (`prints.py` grava em `longas/`).
- Listas que cortam de propósito (carrossel) levam `data-rolagem="intencional"` e `data-fade`.
- Gates: `python3 scripts/bars_check.py project --fonts build/fonts [--blobs blobmap.json]` e `python3 scripts/trunc_check.py project …`, os dois com 0 falhas em todos os canvases. Esses gates pegam o que `overlap_check.py` não vê. O overlap compara texto com texto. Estes comparam o conteúdo com as barras, com a borda e com o recorte de cada caixa.
- Remendo de emergência (deck de reunião em 1 h): no print, um degradê do fundo atrás da barra esconde o conteúdo de baixo. Isso só vale para o print. A correção de verdade é no kit.

## 5. Prints com id estável

- `python3 scripts/prints.py app=app/project painel=painel/project --out prints --fonts build/fonts --blobs blobmap.json` fotografa tudo em 2x e mantém `prints/index.json`.
- **O id não muda quando a tela muda.** Deck, doc e landing apontam para o id. O índice guarda `uid` (canvas/arquivo), `novo` e `longa`. Depois de cada rodada, liste os prints que mudaram (`state/prints_mudancas_<rodada>.json`) para atualizar só esses no deck.

## 6. Deck a partir dos prints

- **Fonte de cada imagem = chave → id do print.** Use um mapa `src.py` (chave → título ou prefixo do print) e converta para webp com no máximo 1920 de largura. Nos slides, escreva `/_blob/K:<chave>`. O build troca pela URL do asset (`img/blobs.json`: chave → id do blob). Assim o slide sobrevive à troca de imagem.
- **Upload**: `upload_asset` em lotes de 10. Atualize o `blobs.json` e reconstrua.
- **A caixa tem a proporção do print.** Para o celular, a caixa de conteúdo (sem a borda da moldura) é 390:844. Para print de desktop alto cortado, a caixa tem a proporção do corte. `object-fit: cover` com proporção diferente corta as laterais da tela, e o usuário vê "dashboard cortado".
- **Celulares lado a lado, sem encavalar**, mesmo na capa. Se a sobreposição for de propósito, ponha `data-sobrepoe`.
- **Nada repetido**: o mesmo print ou o mesmo tópico não aparece em dois slides. Corte slides que o usuário não quer (slide de "o que mudou" e de gaps internos raramente vão para o cliente).
- Gate: `python3 scripts/deck_check.py <pasta> --blobs <id→arquivo> --shots /tmp/deck`. Ele cobre área segura de 96 px, cover que corta, imagem cortada, imagens sobrepostas e imagem fora do slide. Depois olhe os PNGs.
- **Publicar**: `publish_files` em modo patch com `base_version`, mandando `deck.json` e os slides. Para tirar slides, use `remove`. O deck da versão anterior fica congelado.
- **Reunião marcada**: perto do horário, corrija só o que o usuário apontou e não troque o conteúdo do deck. O que estiver em andamento vai num artifact separado depois.

## 7. Diagramas medidos

Diagrama bonito não se desenha com coordenada fixa. O ajuste é este:

- **Layout no fluxo** (CSS grid com raias: `grid-template-columns: 170px repeat(n, 1fr)` e linhas `minmax(120px, auto)`). O nó tem altura automática, então o texto nunca é cortado ("Sugere 3 substitutos / Equivalentes, do protocolo dela." aparecia cortado).
- **Meça no Chromium** a caixa de cada nó (`[data-diagram]`) e só então desenhe as setas num `<svg>` por cima.
- **Conectores ortogonais** com cantos arredondados e `marker` de seta. O raio é limitado por `r = min(R, |dy|/2, gap/2)`, e a folga entre nós é de pelo menos 2r + seta. Com folga de 24 px e raio de 12 px, o último segmento ficava negativo e a seta saía ao contrário.
- Texto do nó ≥ 24 px no slide de 1920. O gate mede o texto cortado e o ponto mais baixo (≤ área segura).

## 8. Marca com pessoa real

Quando a marca é uma pessoa (o especialista, o influenciador), ela precisa aparecer em evidência. Mesmo assim, **não gere o rosto dela nem copie fotos dela**. Use molduras com a legenda "Foto oficial de <nome> · arquivo da <marca>". Antes & Depois entra só como moldura para fotos reais autorizadas. As molduras e a autorização entram como ponto aberto na entrega.

## 9. Tema por plano ou coleção

Se o produto vende planos ou coleções com cor própria, o app pode tender à cor do plano. Faça assim:

- tokens por plano no DS (claro e escuro);
- uma página "Cor do plano";
- contraste medido em cada cor;
- o conflito com o manual da marca, se houver, registrado para o cliente validar.

## 10. Entrega de uma versão

1. Links agrupados por versão, com o índice primeiro.
2. Resumo da paridade (contagens) e do mapa de features.
3. O que mudou nesta rodada: os gates, com os números antes → depois.
4. Pontos em aberto, como perguntas.
