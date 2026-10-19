# Documentação de Produto (A4) e Pitch

## Documentação de Produto (A4, páginas fixas)

O modo Flow não repete cabeçalho e rodapé. Por isso o documento é uma **série de artboards A4 de 794×1123**. "Exportar todos os artboards" desta página gera um PDF único. Com vários idiomas, uma série por idioma, em linhas separadas.

### Pipeline
1. **Átomos**: o conteúdo vira blocos com as propriedades `keep_next` (títulos), `keep_whole` (tabelas curtas, matrizes e diagramas) e `page_break` (início de seção).
2. **Medição**: cada átomo é medido no Chromium (Playwright) com as fontes baixadas localmente. Nas tabelas, mede-se caption, thead e cada linha, com `table-layout: fixed`.
3. **Paginação** com área útil de 940 px e gap de 14:
   - tabela partida repete o cabeçalho e ganha "(continuação)";
   - cadeias `keep_next` vão juntas para a página seguinte.
4. **Moldura** em cada página:
   - margem de 64;
   - cabeçalho no topo até 64: logo + "Documentação de Produto" | seção atual;
   - conteúdo em top 92, altura 948;
   - rodapé em top 1063: produto · versão · data · "Rascunho para validação" | "Página N de T".
5. **Capa e sumário** (páginas 1 e 2). O sumário recebe os números de página numa segunda passada.
6. **Tipografia de impressão**: corpo 16 px, tabelas 13–13,5, legendas ≥ 12 px, linhas finas #D3D6DC, cards com borda de 1 px e raio 14–18.
7. **Verificação**: renderize todas as páginas e confirme `main.scrollHeight ≤ 948`. Espaço vazio no fim de uma seção é aceitável.

### Seção de evidências (nova)
Última seção do documento: tabela do `claims.json` (afirmação, status, fonte, data) e a lista do que não foi verificado. Quem lê o PDF sem o chat sabe o que é fato e o que é hipótese.

---

## Pitch (14 slides de 1920×1080 no canvas)

**Moldura**:
- logo + rótulo no topo (top 56);
- rodapé "Pitch · data" e "n / N";
- padding lateral 112, conteúdo entre top 150 e bottom 110;
- título 72–88 px, texto ≥ 22 px;
- slides de tese e fechamento com fundo escuro;
- CSS `@media print` para neutralizar animações.

**Celulares nos slides**: use o HTML interno real das telas mobile, escalado com `transform: scale(.66)` dentro de uma moldura escura arredondada. Antes, remova `sc-if`, `onClick`, `id` e `for`. O slide registra no `trace.json` quais telas mostra.

### Roteiro por público

**Sócio ou mentor** (padrão):
1. Capa
2. Por que agora
3. Problema (linha do tempo da solução atual envelhecendo + citação da persona)
4. Público
5. Tese
6. Produto (3 celulares)
7. Concorrência (matriz ✓ / ½ / ×)
8. Modelo e canais
9. 5 hipóteses (precisa ser verdade / como testo / sinal)
10. Riscos
11. Plano de 60 dias + critério da v1
12. Como decido (critério para parar)
13. O que eu peço (mentor vs sócio)
14. Fechamento com 3 perguntas

**Investidor**: troque 9, 12 e 13 por mercado (com fonte), validação/tração, time, uso do dinheiro e pedido.

**Agências/canal**: por que revender, margem, white-label, onboarding e próximos passos.

### Pitch para destinatário real (modo próprio)
Quando há uma pessoa ou empresa concreta do outro lado, o deck sai do canvas e vira um artifact do tipo Slides (ou o tipo de deck disponível), com notas de fala.

1. **Pesquisa do destinatário**: só informação pública de negócio, com fonte e data no `claims.json`. Quem decide o quê (ele decide sozinho? há um sócio, um fundo, uma diretoria?) e os critérios públicos de investimento.
2. **Resumo na página 2**: problema, mercado, por que interessa a ele, o que já existe, a proposta.
3. **Maturidade honesta**: três colunas — pronto, planejado, em aberto (sem usuários, sem receita, sem parceria assinada quando for o caso).
4. **Encaixe**: como o produto se conecta ao que ele já tem (portfólio, marcas, alcance). Marcas nas telas continuam fictícias.
5. **Modelo e cenários**: taxas iguais às do modelo base; cenário marcado como cenário, não previsão.
6. **Caminhos de colaboração**: 2–3 opções, cada uma com "quem decide".
7. **Documento interno separado** para quem apresenta: mudanças por slide, pontos a confirmar antes de enviar, temas sensíveis a evitar. Nunca nos slides.
8. **Idiomas**: um deck por idioma pedido, com notas de fala no idioma do deck.

**Contato**: não use e-mail de trabalho do usuário em projeto paralelo. Coloque só o nome, a menos que ele dê o contato. Nome de quem apresenta vem do brief.
