# Fluxo de trabalho: como a Forja roda na prática

Este é o jeito que a Forja foi usada em mais de 30 produtos. O `SKILL.md` diz **o que** sai; este arquivo diz **como** a sessão anda.

```
Ideia → Pesquisa rápida → Overview → Brief → Construção (subagente) → Portões → Publicação → Entrega + lista de todos os apps
```

## 1. A ideia chega

Formatos comuns:

- texto colado, às vezes longo, escrito por outra IA ou pelo próprio usuário;
- link de um produto parecido ("algo como isso, mas para a Alemanha", "mas para mobile");
- PDFs, prints ou vídeo de um produto existente;
- várias ideias numa mensagem só.

Regras:

- **Não pergunte o óbvio.** Mercado, idioma e público costumam estar no texto ou no histórico. Use os padrões (EN · PT · DE, pitch para sócio ou mentor) e diga o que assumiu.
- **Leia o link** (WebFetch) antes de qualquer coisa. Descreva o produto de referência com fatos: público, fluxo, preço, empresa.
- **Várias ideias**: faça uma pergunta só para cada ponto em aberto (mercado, idioma) e depois construa em lote.

## 2. Pesquisa rápida + overview

Antes de construir, faça 3–6 buscas para achar:

- o gancho de "por que agora" (lei, prazo, mudança de hábito), confirmado em 2 fontes;
- quem já faz exatamente isso (concorrente direto) e o que o cliente faz hoje (concorrente real);
- riscos que mudam o produto: propriedade intelectual (manuais, marcas, catálogos de terceiros), dados de crianças, saúde, AI Act, cópia privada.

Mande então um **overview curto** com `SendUserMessage`:

- 1 parágrafo sobre o produto de referência;
- a versão proposta (gancho local, fluxo, o que é específico do mercado);
- **correções que mudam o plano** (ex.: "o BILT já faz isso", "não dá para usar BILLY sem licença", "o BuT não paga app");
- "Já comecei o pacote completo… no fim te mando a lista com todos os apps".

Se o usuário pediu "antes me manda um overview", **pare aqui** e espere a aprovação. Caso contrário, siga construindo.

Se o usuário corrigir a ideia depois ("não, o que eu queria era…"), confirme em 1–3 linhas o novo entendimento e os cuidados que entram no produto, e refaça no **mesmo** artifact (ver `atualizar-produto.md`).

## 3. Delegar a construção

Cada pacote é grande: ~220 arquivos, pesquisa, 3 idiomas, verificação. Delegue a construção a **um subagente por produto** (Agent tool, tipo general-purpose), com o brief de `brief-novo-produto.md` preenchido:

- a ideia com os fatos já levantados e as correções comunicadas ao usuário ("mantenha esse núcleo");
- idioma-base das telas, tom do alemão (du/Sie), público do pitch;
- slug da pasta e onde copiar o motor (o build mais recente);
- direção de arte inicial, diferente das anteriores, e o "conjunto a evitar";
- os portões obrigatórios (pitch completo, doc sem overflow, checklogic, links);
- o formato do retorno, incluindo uma descrição de 1 linha para a lista de apps.

Em **lote** (2–5 produtos), dispare os subagentes juntos, cada um com uma direção de arte inicial diferente (fonte + paleta + arquétipo).

O orquestrador (você) não reconstrói nada: lê o retorno, confere se os portões foram cumpridos e, se faltar algo, **retoma o mesmo subagente** com `SendMessage` (ele mantém o contexto e o build). Exemplos de retomada:

- "olhe todos os 28 slides EN e DE, não só uma amostra";
- "alinhe o slide 10 ao novo risco R2";
- "o selo 'Aguardando assinatura' estoura a pulseira no desktop".

## 4. Portões antes de dar como pronto

- Pitch completo nos 3 idiomas (ver o portão no `SKILL.md`).
- Doc: todas as páginas com `main.scrollHeight ≤ 948`, sumário com números certos.
- Telas: lógica testada, links e seletor de idioma corretos, nenhum overflow.
- Nenhum e-mail do usuário em lugar nenhum; contato no pitch = só o nome.
- `Artifact action=list scope=files` confirma tudo sob `project/`.

## 5. Entrega

Resposta curta, no idioma do usuário:

1. O que é o produto em 1 frase e o que o canvas tem.
2. Correções da pesquisa (concorrente direto, regra legal, dado antigo).
3. Hipótese principal e preço (marcados como hipótese).
4. Direção de arte em 1 linha.
5. **Lista de todos os apps Forja**, com link e 1 linha cada (o mais novo primeiro).
6. Fontes com links.

Não descreva cada tela; o usuário abre o canvas.

## 6. Pedidos depois da entrega

| Pedido | O que fazer |
|---|---|
| "Ajusta a ideia e referencia os links que te passei" | `atualizar-produto.md`: reposicionamento + seção "Referências e links" no doc + slides afetados |
| "Não, o que eu queria era…" (pivô) | Mesmo artifact, mesmo build; refaça telas, doc e pitch; remova órfãos com `null` |
| "Adiciona seletor de idioma" (pacote antigo) | Retrofit de idiomas em `atualizar-produto.md` |
| "Compara com este concorrente / meu repositório" | Leia (WebFetch, `gh api`, ou o navegador do usuário se o repositório for privado), compare em tabela, recomende e ofereça atualizar o pacote |
| "Quais outros nichos?" | Responda no chat com opções e ofereça construir |
