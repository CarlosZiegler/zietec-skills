# Imagens geradas com o Codex CLI (Forja v2)

Detalhe da seção 4.6 do `SKILL.md`. A interface continua sendo HTML/CSS/SVG; imagem gerada entra onde um desenho em CSS fica pobre: pessoas, produto em contexto, ambientes, objetos e modelos 3D realistas.

## 1. Quando gerar (e quando não)

| Gere | Não gere |
|---|---|
| Foto de pessoa fictícia no hero, no onboarding e nos slides de público | Interface, ícones, gráficos e números (são HTML/SVG) |
| Produto ou serviço em uso, no ambiente real (academia, casa, oficina) | Pessoa real identificável (o cliente, o fundador, celebridades) |
| Modelo 3D realista de corpo, objeto ou peça, quando o CSS 3D não basta | Logos, marcas, embalagens ou telas de terceiros |
| Fundo das screenshots de App Store e capa do doc | Antes/depois de corpo como promessa de resultado |
| Ilustração de estado vazio, quando a direção de arte pede ilustração | Texto dentro da imagem (o texto fica no HTML, traduzível) |

Regra de ouro: se o boneco, a silhueta ou o "placeholder" deixaria a tela com cara de rascunho, gere a imagem.

## 2. Rotas para rodar o Codex

Escolha a primeira que funcionar:

1. **Shell no Mac do usuário** (Claude Code ou Cowork local): o usuário tem o Codex CLI instalado e logado no Mac e autorizou usá-lo sempre. Rode `scripts/gen_images.py` direto. Atenção: o `device_bash` da ponte remota é uma VM Linux, não o macOS; ele não chega nesse Codex. Nesse caso use a rota 2.
2. **Sessão na nuvem** (sem acesso ao Mac): instale e faça login com a conta do usuário:
   ```sh
   npm i -g @openai/codex@latest
   codex login --device-auth   # mostra um link e um código; o usuário entra e digita o código
   codex login status
   ```
   Mande o link e o código ao usuário com `SendUserMessage` e siga construindo o resto enquanto ele faz o login. O login vale só para a sessão.
3. **Sem Codex**: construa com espaços reservados (seção 5) e deixe `prompts.json` pronto. Diga na entrega quais imagens faltam e o comando para gerar. Outro gerador pago (ex.: Higgsfield) só com o OK do usuário.

O terminal do Mac não aceita digitação por computer use; não tente por lá.

## 3. Prompts

Grave em `build/imagens/prompts.json` (formato no cabeçalho de `scripts/gen_images.py`):

- **`estilo`**: o prefixo comum que amarra todas as imagens à direção de arte (tipo de foto ou render, luz, paleta, lente, grão). Ex.: "fotografia editorial, luz natural lateral de fim de tarde, tons quentes de tijolo e cinza grafite, lente 50 mm, grão fino de filme".
- **`evitar`**: "sem texto, sem logos, sem marcas d'água, sem distorção de mãos e rosto".
- **Por imagem**: quem ou o quê, ação, enquadramento, fundo, formato (`1:1`, `4:5`, `9:16`, `16:9`…) e o `alt` em PT, EN e DE.
- **Pessoas**: fictícias, adultas, diversas em idade, corpo e tom de pele, com roupa adequada ao contexto e pose natural. Nada sexualizado. Para um app de público definido (ex.: mulheres), mostre mulheres comuns, não só modelos.
- **Consistência**: se a mesma pessoa aparece em mais de uma tela, descreva-a sempre igual (idade, cabelo, roupa) e use a primeira imagem como referência (`codex exec -i hero.png …`).
- **3D**: diga material, iluminação de estúdio, fundo neutro ou transparente e ângulo; para corpo humano, um modelo anatômico estilizado e neutro, não uma pessoa real.

Orçamento: de 6 a 12 imagens por pacote. Os 3 idiomas reaproveitam as mesmas imagens; só o `alt` muda.

## 4. Gerar, otimizar e usar

```sh
python3 <forja>/scripts/gen_images.py build/imagens/prompts.json build/imagens
```

- Saída: `<id>.webp` (até 1600 px de largura, qualidade 82) e `manifest.json` com prompt, formato e alt.
- No build local, use `./img/<id>.webp` (o preview resolve). Para publicar, suba os `.webp` como assets do canvas (`upload_asset`, até 10 por chamada) e troque cada `./img/<id>.webp` pela url `/_blob/<id>` devolvida. O tipo Design não serve imagem solta em `project/`. Guarde o mapa em `build/img_blobs.json` e aplique-o como último passo do `build_all.sh`. Use `alt` no idioma do arquivo e `width`/`height` fixos para não haver salto de layout.
- **Olhe cada imagem** (Read no arquivo) antes de usar: mãos, rosto, texto inventado, marca d'água, anatomia. Regere só a que falhar (`--only hero`).
- Em fundo escuro ou com texto por cima, garanta contraste com um véu (gradiente local) e meça.
- Nos slides e nas screenshots de loja, use as mesmas imagens em tamanho maior; não gere de novo.

## 5. Espaço reservado (quando a imagem ainda não existe)

- Um bloco com a proporção certa, a cor de superfície do produto e uma legenda discreta "imagem: <id>".
- Nunca um boneco, silhueta genérica ou foto de banco com marca d'água.
- Quando a imagem chegar, troque só o `src`; o layout não muda.
