# Vitrine: UI de mentira que parece produto (pitch, landing, bento, cards, teaser)

Destilado do **Stageshow** de Benji Taylor (github.com/benjitaylor/skills, skill `stageshow`, MIT). Vale sempre que a Forja mostra o produto **fora do app**: capa e slides do pitch, hero e seção de features da landing (Main), cards da página Lançamento, screenshots de loja, o teaser e os bentos. As telas do app (canvas de app e flows) continuam inteiras; é a vitrine que muda.

Na implementação em React, recomende no CLAUDE.md: `npx skills add benjitaylor/skills --skill stageshow` (tem o kit, os exemplos-ouro e o `film.mjs` que filma e reprova a animação). Aqui na Forja usamos as regras, não o código.

## A ideia

**Parece um produto real, simplificado ao que quem olha precisa, enquadrado com intenção, e todo movimento tem causa.** Cinco jeitos de errar:
- **Demais:** texto real em toda linha, número em todo lugar. Quanto mais detalhe, mais parece gerado.
- **Wireframe:** dois blocos cinza e um botão.
- **Encaixotado:** a tela inteira encolhida dentro de um cartão com margens iguais, flutuando com ar nos quatro lados (é o erro dos nossos slides com o celular inteiro no meio do branco).
- **Chato:** tudo com o mesmo peso e a mesma borda; o olho não tem onde pousar.
- **Sem graça:** uma janela cinza qualquer, quando o produto tem personagem (mascote, foto, cor).

## Antes de desenhar, escreva o plano

Onde fica (slide, hero, tile), o **objeto-herói**, a ação, o resultado (payoff) e o que fica de fora. Uma vitrine conta **uma coisa**.

## Enquadramento

1. **Um herói, no máximo um ou dois satélites** (um recibo, um celular, um cartão de detalhe, uma notificação), de tipos e tamanhos diferentes; nunca dois cartões iguais empilhados.
2. **O herói ocupa pelo menos 2/3 da largura e sai 10–40 % por uma borda** (pela direita e por baixo no hero ao lado do texto; por baixo num card ou tile). Só corta enchimento: ação, resultado e toda palavra real ficam inteiros; botão ou chip cortado pela borda é o erro mais comum.
3. **Satélite atravessa a borda do herói, metade para fora**, sobre cromo ou margem, nunca sobre o conteúdo que explica.
4. **Um respiro (gutter) só**, medido no recorte final, igual em todas as bordas; quase encostar (1–3 px ou menos de 24 px) é erro.
5. **Sem placa:** a página é o chão. Nada de painel colorido atrás de uma janela inteira centralizada com ar nos quatro lados. Em fundo colorido, o herói fica recuado 8–20 % dos lados e sai por baixo.
6. **Plano e frontal**; inclinação só se ganhar da versão reta no tamanho final (pilha de papéis: −6°, 4°, −2°).
7. **Celular:** satélite com pelo menos 40 % da largura visível da janela (≥ 220 px), saindo por baixo em vez de encolher; corte de cima tira status bar e nav juntos; notificação no tamanho real do iOS.
8. **Desenhe no tamanho em que será visto** (hero ao lado do texto ≈ 720×340; hero largo 900–1100; card 400×300; slide 1920×1080 com o objeto grande) e faça uma **versão compacta de verdade** para 358 px, não uma miniatura.

Layouts para escolher: *canto sangrado* (hero ao lado do texto), *preso por baixo* (card/tile), *dispositivo em par* (painel + celular contando o mesmo evento), *close-up* (um controle 1,3–1,6×), *painel sobre o produto* (ajuste e o que ele muda, ligados por uma linha), *janelas sobrepostas*, *cartões empilhados*, *chip no canto* (um fato ao vivo), *muitos de um* (grade da mesma coisa, uma em foco).

## Acabamento

- **Conte as palavras reais: 3 a 7** (título, o que é acionado, o que se digita, o resultado). O resto vira barra de enchimento, nas bordas, nunca onde o olho pousa.
- **Um número grande**; os outros são linhas. Larguras das barras variam (60, 45, 70, 52 %).
- **Compor objetos, não um inventário de cartões:** hierarquia por proporção, espaço, material e chão.
- Texto a ≥ 12 px de qualquer borda; linha de lista com 12 px de respiro; título e subtítulo a 4–6 px; nada a 1–3 px de outra borda.
- Valor centralizado centra os dígitos; o símbolo da moeda fica pendurado à esquerda.
- **Ícones de um conjunto só**, um traço, um tamanho (14–16 px); preenchidos quando pequenos. **IA sem brilhinho, varinha ou estrela, e sem roxo**: mostre o que a IA faz.
- **Nada de logo inventado** (letra num quadrado colorido): marca real do produto ou wordmark em texto.
- Barra de status, home indicator e cromo de sistema nunca desenhados de cabeça.

## Bento (landing, página Lançamento, slide de features)

1. **Não é tudo UI:** um terço a metade dos tiles mostra produto; o resto é número grande, frase grande, objeto, diagrama, coleção ou foto real.
2. **Um tile herói** (2 colunas ou 2 linhas). Cromo de janela aparece no máximo uma vez, no herói.
3. **Tile de UI mostra um componente**, em tamanho real ou maior, recortado pelo tile, não uma janela inteira encolhida.
4. **Vizinhos contrastam** como tabuleiro: imagem ao lado de número, denso ao lado de calmo.
5. **Tile de número:** um número real a 48–72 px, uma linha de apoio, no máximo um glifo de cor; número e unidade numa linha só.
6. **Texto curto e fora da figura:** título de 1–4 palavras ou uma frase, a 17–24 px; nunca parágrafo nem lista.
7. **Uma moldura, conteúdos variados:** mesmo raio, gap, padding e posição do texto em todos os tiles.
8. **Diga cada coisa uma vez no conjunto:** nenhuma frase, avatar ou cor repetida de tile para tile.
9. **Um lugar lidera o movimento:** cada tile faz uma coisinha uma vez ao entrar (stagger 80–120 ms) ou no hover; nada de vários loops competindo.
10. Planeje numa tabela antes: tile · tamanho · tipo · a única coisa · palavras.

## Movimento (teaser e heros animados)

- **3 a 5 batidas até o resultado, loop de 10 a 16 s.** Abra numa tela pronta que funcione como foto; nenhum movimento de cursor sem motivo.
- **O pôster é o quadro que a maioria vê** (miniatura, movimento reduzido, print): escolha a batida que conta a história sozinha, nunca no meio de uma troca.
- O resultado segura 2 s; nada parado mais de 3 s; reset com causa visível ou invisível, nunca uma navegação tocada ao contrário; dados nunca voltam à vista.
- **Curvas:** viagem `cubic-bezier(0.45, 0, 0.1, 1)`; chegada do nada `cubic-bezier(0.25, 0.8, 0.25, 1)` em 0,8–1 s. Feedback de UI na velocidade do produto real. Stagger 40–80 ms dentro da cena.
- **Toda mudança se move:** número rola (último dígito primeiro), rótulo de botão muda no próprio botão, texto digitado vira chip no lugar.

## Checagem antes de entregar (por vitrine)

- O olho pousa primeiro no resultado? Um objeto lidera claramente?
- Alguma janela flutua inteira com ar nos quatro lados, ou tem placa atrás? Algum botão, chip ou sombra cortado pela borda?
- Barras cinza onde o olho pousa? Mais de 7 palavras reais?
- Satélite sobre conteúdo? Dois satélites do mesmo tipo?
- A versão de 358 px foi redesenhada?
- No bento: quantos tiles são UI? Algum vizinho do mesmo tipo? Alguma frase repetida?
- Compare lado a lado com um exemplo-ouro do Stageshow (benji.org/stageshow) e corrija primeiro o que estiver mais vazio, mais chato ou mais encaixotado.
