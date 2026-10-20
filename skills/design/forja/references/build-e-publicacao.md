# Motor local, verificação e publicação

## Estrutura de um build

```
<WS>/forja/<slug>/
├── build/
│   ├── brand.py            # tokens próprios do produto (paleta, fontes, raios, sombras, logo SVG)
│   ├── i18n.py             # T(pt, en, de), set_lang, fname/pitch_file/doc_file, formatos  (scripts/i18n.py)
│   ├── ui.py / icons.py    # componentes e ícones na direção de arte do produto
│   ├── data.py             # dados fictícios compartilhados (personas, domínios .example, números)
│   ├── content_a/b/c.py    # doc: 01–02, 03–04, 05–06, com assert nas contagens
│   ├── screens_m.py / screens_d.py   # 9 + 9 telas, com class Component extends DCLogic
│   ├── pitch.py            # 14 slides por idioma
│   ├── doc_blocks.py / paginate.py   # átomos, medição no Chromium, paginação A4 e moldura
│   ├── build_screens.py / build_pitch.py / build_doc.py / build_canvas.py
│   ├── preview.py / verify_pages.py / checklogic.js / check_links.py / contrast.py   (scripts/)
│   └── fonts/              # woff2 + local.css  (scripts/fetch_fonts.py)
└── project/                # o que é publicado: canvas.json + *.dc.html
```

O motor de um produto serve de ponto de partida para o próximo: copie **a mecânica**, troque `brand.py`, componentes, conteúdo e layouts. Nunca reaproveite o visual.

## Contagens que os asserts devem garantir

| Seção | Itens |
|---|---|
| Vision Board | 4 grupos de público, 5–6 capacidades, 4 objetivos, matriz com 5 alternativas |
| PRD | 7 objetivos, 3 personas, 32 RF (~20 Must / 9 Should / 2 Could / 1 Won't), 12 RNF, 12 regras, 8 riscos |
| Flows | 7 fluxos com passos pessoa/sistema e exceções |
| Stories | 8 épicos, 38 histórias, Fibonacci, sprints de ~40 pts coerentes com 60 dias, cada história em exatamente 1 sprint |
| ARD | 4 princípios, 6 camadas, 22 entidades, ~30 endpoints, 12 eventos, 7 ADRs (+1 quando um ajuste pede) |
| Cronograma | Gantt, critério da v1 em 1 frase, 8 condições rastreadas a US/RNF |

Quando um ajuste muda uma contagem, atualize o assert **e** todos os textos que a citam, nos 3 idiomas, no doc e no pitch.

## Ordem de build

1. `python3 scripts/fetch_fonts.py "<css2 query>" build/fonts`, uma vez por produto.
2. Gere as telas nos 3 idiomas e meça a altura natural das mobile (`preview.natural_height`). Grave `sizes.json`.
3. Gere o pitch nos 3 idiomas.
4. Gere o doc: átomos → medição → paginação → 2ª passada do sumário, por idioma. Grave `doc_pages.json` com o início de cada seção por idioma (o seletor do doc usa).
5. Gere o `canvas.json`.
6. Rode as verificações:

```sh
node scripts/checklogic.js project [build/logic_tests.js]   # lógica + holes + testes de interação do produto
python3 scripts/check_links.py project --screen-base en      # links, seletor EN·PT·DE, <html lang>, sobras de idioma
python3 scripts/verify_pages.py project "Doc-*"              # overflow do doc (main ≤ 948)
python3 scripts/verify_pages.py project "Pitch-*" all        # overflow + screenshots de todos os slides
python3 scripts/contrast.py build                            # pares de cor do brand.py
```

7. Monte uma contact sheet dos slides e das páginas (Pillow ou screenshot de uma grade HTML) e **olhe** com Read, idioma por idioma.

## Publicação no tipo Design

1. `Artifact action=quickstart intent=design design_systems=false` devolve o `type_url`.
2. Publish com `type_url`, `title` = "<Nome> · <descrição curta>", `auto_open: "after_first_write"`, sem arquivos. Leia as instruções do tipo: elas mandam no formato do `canvas.json`.
3. Publish com `url`, `root` = `<WS>/forja/<slug>` (a **pasta-mãe** de `project/`) e `files` = `{"project/canvas.json": "project/canvas.json", "project/Main.dc.html": "project/Main.dc.html", …}`.
4. `Artifact action=list scope=files url=<url>`: tudo sob `project/`, nada solto na raiz (se houver, remova com `null`).
5. Não verifique visualmente depois de publicar, a não ser que o usuário peça.

## Notas aprendidas

- **Publicação na raiz errada**: com `root` = `project/`, o `canvas.json` foi parar na raiz do artifact. Use a pasta-mãe e chaves `project/...`.
- **Stickies**: o tipo não aceita `fill: "yellow"`; omita `fill` (o padrão já é amarelo).
- **Falsos positivos do verify**: carrossel horizontal, conteúdo cortado dentro dos celulares do pitch, animação de entrada medida no meio, nomes próprios que são palavras comuns ("Zugang" = acesso).
- **Pitch incompleto** (reclamação real): os riscos mostravam 5 de 8, a matriz estava cheia de "?" e havia slides com o meio vazio. Portão obrigatório: olhar os 42 slides.
- **Overflow de pílula de status** no desktop: rótulos curtos, ícone em coluna própria e `text-overflow: ellipsis`.
- **Render de 42 slides** pode passar do limite de 2 min de um comando: rode em segundo plano ou divida por idioma.
- **Tradução por hash**: tabelas `tr_*.py` chaveadas pelo hash do texto PT; mudar o PT exige entrada EN+DE nova. Mantenha um `verify_i18n`/`check_links` que acuse chave faltando.
- **Doc em alemão** fica ~5–10% mais longo em páginas; normal.
- **Datas**: o próximo passo do pitch tem data real, posterior ao dia da entrega.
- **Contato**: nunca o e-mail de trabalho do usuário; no pitch, só o nome.
