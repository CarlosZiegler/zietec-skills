---
name: nome
description: Cria e escolhe nomes para apps, produtos e empresas: estratégia, geração ampla, filtro de deal-breakers, torneio, checagem em PT, DE e EN e disponibilidade. Use para dar nome ou avaliar nomes.
---

# Nome: do brief ao nome escolhido

Primeiro estratégia, depois quantidade, depois corte. Nunca uma lista rápida de nomes soltos.

## Modos

- **Gerar**: veio uma ideia ou um brief.
- **Avaliar**: o usuário trouxe nomes e quer opinião ou ranking.
- **Os dois**: gera e, no fim, compara com os nomes dele numa seção à parte.
- **Rápido** (chamado pela Forja): todas as etapas, sem perguntas, entregando só o top 3 e a recomendação.

## 1. Brief de naming

Pergunte uma vez, só o que falta (AskUserQuestion quando houver escolhas):

- o que é, para quem, mercados e idiomas. Padrão do usuário: Alemanha e Brasil, então o nome precisa funcionar em **português, alemão e inglês**;
- sentimento (2–3 palavras) e "nunca soar como";
- arquitetura: nome solto ou família (ex.: AutoFolio e HomeFolio); expansão futura;
- concorrentes, nomes a evitar, palavras que ama ou odeia;
- restrições: domínio desejado, handles, nome de app na loja (título de até 30 caracteres).

Se veio da skill `produto`, use o Brief de Produto e não pergunte de novo.

## 2. Estratégia

Escreva antes de gerar:

- a marca em 1 linha;
- o território emocional;
- temas e metáforas a explorar; clichês a evitar;
- **3 a 5 direções**, cada uma numa posição da matriz:
  - abordagem: descritivo → sugestivo → abstrato (padrão para produto novo: sugestivo);
  - construção: palavra real → composta → inventada.

## 3. Geração ampla

Quantidade vem antes de qualidade.

- Gere internamente pelo menos **150 candidatos**, cerca de 30 por direção.
- Varie as técnicas: palavra real deslocada, composta, portmanteau, raízes (latim, grego, alemão, tupi), metáfora, verbo de ação, grafia alternativa com cuidado.
- Use simbolismo sonoro de propósito: plosivas (b, k, p) fixam na memória; l, m, n soam acolhedoras; v soa viva.
- Se o ambiente tiver subagentes ou workflows, faça fan-out: um agente por direção.
- Não mostre a lista inteira por padrão.

## 4. Filtro de deal-breakers

Corte todo nome que:

- parece erro de digitação;
- lembra marca existente;
- prende o produto e impede crescer;
- é trocadilho forçado;
- é descritivo e sem graça;
- só faz sentido para quem é de dentro;
- é difícil de pronunciar em algum dos idiomas-alvo.

Corte também:

- sufixos genéricos (-ify, -ly, -io, -hub, -labs) sem razão estratégica;
- nomes com cara de gerado por IA (Nexa, Zyra, Lumio, Velora, Fluxo e parecidos);
- qualquer nome a uma letra de distância de um concorrente.

Devem sobrar 20 a 30.

## 5. Torneio

1. Dê nota de 1 a 5 a cada sobrevivente: sugestivo, memorável, imagem mental, fôlego (dá para construir marca em volta), emoção, pronúncia em PT/DE/EN, grafia depois de ouvir uma vez, distinto na categoria.
2. Os 8 melhores vão para **confronto em pares**: em cada par, qual nome vence para este ICP e por quê, em uma frase. Comparar é mais confiável que dar nota.
3. Se houver subagentes, use juízes separados de quem gerou os nomes.
4. Sai um ranking de 5.

## 6. Checagem linguística

Para cada um dos 5:

- o que significa ou lembra em português, alemão e inglês, incluindo gírias, palavrões e conotações históricas (lição: "Anschluss");
- como um alemão e um brasileiro pronunciariam;
- se a grafia sobrevive a um ditado por telefone.

Marque o risco como Baixo, Médio ou Alto.

## 7. Disponibilidade

É um sinal, não um parecer jurídico.

- **Produtos e empresas**: busca na web por homônimos na mesma categoria, na App Store e no Google Play.
- **Marcas**: pesquise EUIPO e DPMA (Alemanha e UE), INPI (Brasil) e USPTO quando for global. Registre só o que viu, com link.
- **Domínios**: .com, .app, .de, .com.br, get[nome], [nome]app. Se não der para confirmar daqui, diga.
- **Handles**: X, Instagram, TikTok.

Nunca diga que um nome está livre sem ter visto a fonte.

## 8. Entrega

- **Top 3** numa tabela: nome, significado, direção, nota, risco linguístico, sinal de disponibilidade.
- **Recomendação**: um nome, com o porquê estratégico (posicionamento, ICP, expansão), nunca "porque soa bem". Inclua uma tagline de exemplo.
- **Antes de fechar**:
  - checar a marca no registro oficial ou com advogado;
  - comprar o domínio logo;
  - dizer o nome em voz alta para alguém de fora e ver se a pessoa soletra certo.
- Ofereça mostrar todas as direções ou rodar outra rodada usando o motivo da rejeição.

## Modo Avaliar

Para cada nome trazido:

- o que sugere e o que faz sentir;
- encaixe na categoria; parece premium ou barato;
- fácil de dizer e de soletrar;
- risco em PT, DE e EN;
- sinal de disponibilidade;
- nota.

Depois ranqueie do mais forte ao mais fraco, uma linha de porquê por nome, e recomende um. Nome fraco se diz fraco, com o motivo.

## Ligações

- Vem depois da skill `produto`.
- Alimenta a `forja`: o nome escolhido vira o nome do canvas, das telas e do pitch.

Base: brand-naming (arnabbagxd), brand-naming-strategies com SMILE e SCRATCH (mike-coulbourn, MIT) e o padrão de torneio dos workflows dinâmicos do Claude Code.
