# Linguagem visual (padrão herdado da forja)

Inspirada na Apple, sem copiar. É o padrão; se o produto herda a identidade de outro app do usuário, troque os tokens e registre no `brief.md`.

## Tokens

| Token | Valor |
|---|---|
| Fundo do app | `#F4F5F7` |
| Superfície | `#FFFFFF` |
| Texto | `#16171A` |
| Texto secundário | `#5B606B` (5,8:1 no fundo) |
| Linha fina | `#E3E5E9` |
| Ação / link | `#0A62D0` (5,7:1 no branco) |
| Status (texto / fundo) | vermelho `#C62B1F`/`#FDECEA`, laranja `#A84B00`/`#FFF1E3`, âmbar `#7A5600`/`#FFF4D1`, verde `#1E7B3F`/`#E6F4EA`, roxo `#6B3FD1`/`#F1ECFD` |

**Cor da marca**: uma por produto, usada com parcimônia. Calcule o contraste por script: ≥ 4,5:1 para texto, ≥ 3:1 para texto grande e UI.

## Tipografia

Geist e Geist Mono (Google Fonts, `css2`). Vale para telas, doc **e decks**.
- Display: letter-spacing de −0,035 a −0,06em, line-height 0,95–1,05.
- Corpo: 16–17 px, line-height 1,5.
- Números com `tabular-nums`.
- **Sem rótulos em caixa alta.**

## Sombras

- **sm**: `0 2px 3px -1px rgba(0,0,0,.1), 0 1px 0 0 rgba(25,28,33,.02), 0 0 0 1px rgba(25,28,33,.08)`
- **md**: `0 0 0 1px rgba(0,0,0,.06)` + camadas 1/3/6/12/24 px, todas a .06
- **lg**: `0 2.8px 2.2px .034, 0 6.7px 5.3px .048, 0 12.5px 10px .06, 0 22.3px 17.9px .072, 0 41.8px 33.4px .086, 0 100px 80px .12`

Diagramas não usam sombra (ver `diagramas.md`).

## Raios

Controles 12, cards 20–24, sheet 28 no topo, pílulas 999. Raio externo = raio interno + padding.

## Vidro (barras e tab bar)

`rgba(255,255,255,.72)` + `backdrop-filter: blur(20px) saturate(180%)` + borda de 0,5 px. Nunca vidro sobre vidro.

## Componentes

- título grande (34 px) e barra superior de vidro com "voltar";
- tab bar com pílula de cor da marca no item ativo e badge numérico;
- lista agrupada inset;
- segmented control;
- anel de progresso (path com `pathLength=100`);
- barras de sparkline;
- toggle como `<button role="switch">`;
- pílulas de status com forma + texto (nunca só cor);
- botões primary (tinta), brand (cor da marca), tinted e secondary.

## Sinais de design gerado por IA (evitar em tudo, inclusive decks)

Gradiente de fundo, glow escuro, card com borda lateral ou superior colorida, emoji, Inter/Roboto, grade de cards idênticos, uma palavra destacada no título, "→" em botão, rótulos em caixa alta mono.

## CSS de motion (coloque no `<helmet><style>` de cada artboard)

```css
:focus-visible{outline:2px solid #0A62D0;outline-offset:2px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.tn{font-variant-numeric:tabular-nums}
.z-press{transition:transform 160ms cubic-bezier(.23,1,.32,1),box-shadow 160ms ease-out;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
.z-press:active{transform:scale(.97)}
@media (hover:hover) and (pointer:fine){.z-lift{transition:transform 200ms cubic-bezier(.23,1,.32,1)}.z-lift:hover{transform:translateY(-2px)}}
@keyframes z-in{from{opacity:0;transform:translateY(12px);filter:blur(4px)}}  .z-in{animation:z-in 480ms cubic-bezier(.23,1,.32,1) both}
@keyframes z-rise{from{opacity:0;transform:translateY(24px) scale(.98)}} .z-rise{animation:z-rise 640ms cubic-bezier(.23,1,.32,1) both}
@keyframes z-ring{from{stroke-dashoffset:100}} .z-ring{animation:z-ring 1400ms cubic-bezier(.23,1,.32,1) both}
@keyframes z-draw{from{stroke-dashoffset:1}} .z-draw{stroke-dasharray:1;animation:z-draw 1600ms cubic-bezier(.77,0,.175,1) both}
@keyframes z-bar{from{transform:scaleX(0)}} .z-bar{transform-origin:left;animation:z-bar 900ms cubic-bezier(.23,1,.32,1) both}
@property --n{syntax:'<integer>';initial-value:0;inherits:false}
@keyframes z-count{from{--n:0}} .zc{animation:z-count 1400ms cubic-bezier(.23,1,.32,1) both;counter-reset:n var(--n)} .zc::after{content:counter(n)}
/* por valor: .zc64{--n:64}; o número real vai num .sr ao lado, e o span animado leva aria-hidden */
@keyframes z-sheet{from{transform:translateY(100%)}} .z-sheet{animation:z-sheet 420ms cubic-bezier(.32,.72,0,1) both}
@keyframes z-pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.06)}}
@keyframes z-fill{from{transform:scaleX(0)}} /* barra de progresso de 2400ms */
@keyframes z-out{0%,86%{opacity:1;visibility:visible}100%{opacity:0;visibility:hidden}} .z-scanlayer{animation:z-out 3000ms forwards}
/* atrasos: .d0 … .d90 = i·60ms */
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-delay:0ms!important;transition-duration:.01ms!important}.z-scanlayer{display:none!important}}
@media (prefers-reduced-transparency:reduce){.z-glass{backdrop-filter:none!important;background:#fff!important}}
@media print{*{animation:none!important;transition:none!important}.z-scanlayer{display:none!important}}
```

## Regras de motion

- **Um momento orquestrado por tela**: anel que se desenha + contagem, e entradas escalonadas de 60 ms.
- **Nunca anime ações frequentes.**
- **Easing**: saída/entrada `cubic-bezier(.23,1,.32,1)`, movimento `(.77,0,.175,1)`, sheet `(.32,.72,0,1)`.
- **Durações**: toque 160 ms, UI até 300 ms, sheet 420 ms.
- Hover só dentro de `(hover:hover)`.
- Em estados que podem ser interrompidos, use `transition`, não `keyframes`.
