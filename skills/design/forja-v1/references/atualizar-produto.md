# Atualizar um pacote já publicado

Vale para ajustes de ideia, pivôs, novos links e referências, e retrofit de idiomas. A regra de ouro é **mesmo artifact, mesmo link**: o usuário já compartilhou ou guardou a URL.

## 0. Sempre antes de mudar

1. `Artifact action=list scope=files url=<URL>` e `action=read path=project/canvas.json`. Parta **dessa** versão.
2. Compare os tamanhos dos `.dc.html` publicados com os locais. Se o usuário editou um arquivo, preserve a edição (aplique no gerador ou não regenere aquele arquivo) e diga isso no retorno.
3. O editor re-salva o `canvas.json`: reordena chaves, põe `w: 240` nos títulos e tira `fill`. Isso não é edição do usuário.
4. Se o build local não existir mais (sessão nova), baixe os arquivos publicados e edite os `.dc.html` com cuidado, ou reconstrua o gerador a partir deles.
5. Faça uma cópia de segurança de `build/` e `project/` antes de começar.

## 1. Ajuste de ideia + "referencie os links que te passei"

Exemplo real: o usuário mandou um concorrente (site) e o próprio repositório antigo dele.

- Leia os dois (WebFetch; repositório privado → `gh api` ou o navegador do usuário).
- Responda primeiro no chat com um comparativo (tabela) e uma recomendação de posicionamento.
- No pacote, quando ele pedir:
  - **Vision Board**: mantenha a matriz e o concorrente real; acrescente um bloco "Vizinhos, não concorrentes" quando o produto citado for complementar.
  - **PRD**: um fato novo no contexto (com fonte); ajuste um risco existente (mantenha 8).
  - **ARD**: alinhe a stack ao que já existe (ex.: o repositório vira base técnica) e acrescente um ADR ("Partir do X em vez de começar do zero"). Atualize asserts e textos que citam contagens ("Sete decisões" → "Oito").
  - **Cronograma**: o sprint 1 passa a "herdar o X"; folga marcada como hipótese, sem número inventado.
  - **Nova seção final "Referências e links"** (EN "References and links", DE "Referenzen und Links"), com entrada no sumário: os links do usuário em destaque, com 1 linha de descrição cada, depois as fontes já citadas. Use `<a href>` com a URL visível (para impressão) e nunca invente URL; fonte sem URL no build é citada pelo nome.
  - **Pitch**: o slide de concorrência e o de plano recebem o bloco novo; o slide de riscos fica alinhado ao PRD.
- Traduções novas nos 3 idiomas. Nas tabelas de tradução chaveadas por hash do texto PT, todo texto PT novo ou alterado precisa de uma entrada EN e DE.

## 2. Pivô ("não, o que eu queria era…")

Exemplo real: um manual 3D B2B (para marcas) virou B2C ("o usuário fotografa o manual e a IA cria o guia").

- Confirme no chat, em 1–3 linhas, o novo entendimento e os cuidados que entram no produto (ex.: guia privado por causa de direito autoral; 3D honesto com nível de confiança e foto original quando a IA não tem certeza).
- **Retome o mesmo subagente** (`SendMessage`), porque ele tem o build. Mantenha a direção de arte se ela continuar servindo.
- Refaça pesquisa, modelo de negócio, telas (troque as que não servem mais), doc e pitch nos 3 idiomas.
- Remova os arquivos que ficaram sem uso com `null` na publicação.
- Atualize o título do artifact se o publish permitir; senão, avise o usuário que pode renomear pelo menu.
- Repita **todos** os portões, inclusive olhar os 42 slides.

## 3. Retrofit de idiomas (pacote antigo só em 1 idioma)

O mecanismo é por **variantes estáticas**: cada artboard tem o próprio state, então o seletor é um conjunto de links, não um toggle.

- **Nomes**: o idioma-base mantém os nomes atuais (não renomeie). Os outros idiomas levam sufixo antes de `.dc.html`: `Main-EN`, `M-Hoje-DE`, `Pitch-EN-01`, `Doc-DE-01`. A contagem de páginas do doc pode diferir por idioma.
- **Seletor**: componente único, na ordem EN · PT · DE. O idioma atual é `<span aria-current="true">`; os outros são `<a href hreflang lang title="English|Português|Deutsch">`, dentro de `<nav aria-label="Language · Idioma · Sprache">`. Altura de 32–36 px.
- **Posição**: landing no nav; app na barra do topo ou numa linha acima do título grande; desktop no topo do main; pitch na moldura do topo; doc no cabeçalho, compacto, levando ao **início da mesma seção** no outro idioma.
- **Tradução**: PT-BR com "você"; EN natural com grafia americana; DE com "Sie" para B2B e "du" para consumidor. Termos legais ficam no original, explicados na 1ª ocorrência. Use números, datas e moeda no formato do idioma, mas a moeda continua a do mercado. Mantenha personas, números e contagens iguais. `[A DEFINIR]` vira `[TBD]` e `[offen]`.
- **Canvas**:
  - `mobile` com 3 linhas, uma por idioma, com um `title1` acima de cada linha;
  - `desktop` com 3 blocos empilhados (folga ≥ 600 px);
  - `pitch`/`pitch-en`/`pitch-de` e `doc`/`doc-en`/`doc-de`, para o Export PDF gerar um PDF por idioma;
  - `is_interactive: true` em todo artboard com o seletor.
- **Pitch**: os celulares do slide de produto mostram as telas no idioma do pitch, sem `href` dentro.
- **Verificação extra**:
  - links: todo `href="*.dc.html"` existe, e o seletor aponta para o equivalente certo;
  - idioma: sobras do idioma errado em cada conjunto (`scripts/check_links.py`);
  - alemão ~30% mais longo: olhe as telas DE.

## 4. Publicação de atualização

- Uma chamada com `url` = o mesmo, `root` = a pasta-mãe de `project/` e `files` só com os arquivos novos ou regerados + `canvas.json`. Órfãos saem com `null`. Sem `icon`. Nunca `force`.
- Se houver conflito, a resposta traz a versão atual: faça o merge do `canvas.json` e publique de novo.
- Depois, `action=list scope=files`.
- Retorno: o que mudou por seção, as contagens (antes → agora), onde estão os links novos e os problemas conhecidos. Atualize a linha do produto na lista de todos os apps.
