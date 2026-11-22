---
name: produto
description: Decide se uma ideia de app ou micro-SaaS vale construir e afia o produto antes de desenhar: dor, ICP, proposta, preço, ativação, retenção, distribuição e veredito. Também audita produtos existentes.
---

# Produto: da ideia ao veredito

Entra uma ideia (1–2 frases) ou um produto que já existe (URL, telas, PRD). Sai um **Brief de Produto** de 1 página com veredito **Construir / Ajustar / Parar**, no idioma do usuário. A Forja lê esse brief antes de desenhar as telas.

**Base de consulta**: `revenue-centric-design` (heliocosta-dev, princípios de Richard, @richardrx).

- Se estiver instalada, abra só o tema da pergunta e cite o princípio pelo nome.
- Se não estiver, use as regras abaixo e sugira `npx skills add heliocosta-dev/revenue-centric-design`.
- A licença dela exige atribuição e proíbe uso em apostas, cassino e jogos de azar. Recuse produtos desse tipo.

## Modos

- **Ideia nova**: passos 1 a 9.
- **Auditoria** ("revisa", "por que não converte", "o que melhorar"): vá para a seção Auditoria. Não redesenhe nada.
- **Rápido** (chamado pela Forja): passos 1 a 9 com o mínimo de cada um, sem perguntas, em até uma página.

## Entradas (pergunte uma vez, só o que bloqueia)

Use AskUserQuestion com opção recomendada:

- mercado e país;
- quem paga;
- ambição: renda extra, negócio próprio ou parceria.

Sem ninguém para responder: assuma e diga o que assumiu.

## 1. Dor antes da solução

- Escreva o problema sem citar o produto: quem sofre, em que momento e quanto custa hoje (tempo, dinheiro, risco).
- Junte evidência real: reviews de 1 a 3 estrelas dos concorrentes, Reddit, fóruns, grupos. Guarde 5 sinais com fonte, parafraseados ou citados em menos de 15 palavras.
- O que a pessoa faz hoje (planilha, WhatsApp, agência, nada) é o concorrente real.
- Sem evidência de dor, o veredito é no máximo **Ajustar**.

## 2. ICP estreito

- Escolha um nicho deliberadamente mal atendido, nunca "todo mundo".
- Nomeie quem paga e quem usa, separados.
- Teste: dá para listar 20 pessoas ou empresas reais desse ICP e onde elas estão? Se não dá, estreite.

## 3. Proposta e categoria

- Uma frase: para [ICP] que [dor], [produto] [resultado], diferente de [alternativa] porque [mecanismo].
- Quem é igual compete por preço; quem é diferente compete por categoria. Nomeie o contraste: mecanismo, narrativa ou experiência.
- A promessa tem o tamanho da prova. Diga qual prova o produto entrega no primeiro uso.

## 4. Primeiro valor e ativação

- **Momento aha**: a ação que, feita, prevê retenção. Defina o evento de ativação (ex.: "primeiro relatório exportado em 24 h").
- **Tempo até o valor**: meta em minutos.
- Entregue o resultado prometido antes de ensinar a mecânica. Onboarding ativo, nunca tour.
- Corte atrito administrativo (cadastro longo). Mantenha o atrito declarativo que qualifica a pessoa.
- Nunca dashboard vazio: dado de exemplo ou primeiro passo guiado.

## 5. Preço e modelo

- Piso = custo + margem. Teto = valor percebido. Nunca "concorrente menos 20%".
- Preço é filtro: escolhe quem entra, quem fica e quem expande.
- Freemium só quando servir o usuário grátis custa pouco.
- Três planos (Good-Better-Best) com o do meio como alvo.
- Upgrade no momento do limite, enquadrado como perda, nunca por interrupção.
- Cobre dos 10 primeiros desde o dia 1.
- Todo preço próprio vai marcado como hipótese.

## 6. Retenção

- Por que a pessoa voltaria na semana 2? Defina o gatilho recorrente (dado novo, lembrete útil, colaboração).
- Perda percebida retém mais que benefício prometido. Diga o que ela perde ao sair (histórico, dados, relatórios).
- Churn antes de 30 dias é problema de onboarding, não falta de feature.

## 7. Escopo da v1

- Liste as features e corte até sobrar o núcleo que entrega o aha. A adoção média de features é baixa, e toda feature custa manutenção.
- Pedido de feature não compra feature. O padrão é o parking lot.
- Separe dentro e fora da v1, com o porquê de cada item fora.

## 8. Distribuição

- Construir é a zona de conforto; vender é o jogo.
- Um canal principal, escolhido depois de testar 3 (Bullseye). Nunca cinco ao mesmo tempo.
- Plano para os 10 primeiros pagantes: onde estão, mensagem, oferta.
- App de consumo: o formato de vídeo curto que já viraliza no nicho. B2B: canal ou parceiro (agência, contador, associação).
- Matemática do funil: meta de receita → pagantes → trials → visitas, com as taxas marcadas como hipótese.

## 9. Hipóteses, parada e veredito

- **5 hipóteses**: precisa ser verdade / como testo em até 2 semanas / sinal de sucesso. A mais arriscada vem primeiro.
- **Teste barato antes do código**: landing com lista de espera, venda manual (concierge) ou protótipo clicável com 5 entrevistas.
- **Critério de parada**: o que, se acontecer, faz largar a ideia.
- **Scorecard** de 1 a 5, cada nota com uma linha de porquê: Dor, ICP, Diferença, Disposição a pagar, Alcance do canal, Facilidade de construir, Encaixe com o fundador.
- **Veredito**:
  - Construir: total ≥ 25 e Dor ≥ 4.
  - Ajustar: diga exatamente o que mudar.
  - Parar: diga por quê.

Seja honesto. Ideia fraca se diz fraca.

## Auditoria (produto existente)

1. Ache o gargalo:
   - não entra ninguém → distribuição;
   - entra e sai sem pagar → onboarding, design ou preço;
   - paga e cancela → retenção ou expectativa.
2. Mapeie a jornada até o valor e ataque a maior queda, não a primeira etapa.
3. Ranqueie os achados por impacto na receita. Cada achado leva princípio nomeado, o movimento e como medir.
4. Pare e deixe o usuário escolher o que fazer.

## Regras

- **Números**: nunca invente. Use fonte, ou marque como hipótese ou `[A DEFINIR]`.
- **Lei e regulação**: confirme em 2 fontes oficiais antes de escrever.
- **Nomeie o mecanismo** (decoy, ancoragem, aversão à perda, efeito Zeigarnik, níveis de consciência de Schwartz). Nomear a alavanca é metade do valor.
- Citações de fontes sempre curtas; o resto, parafraseado.

## Saída: Brief de Produto (1 página)

1. Problema e evidência (com fontes)
2. ICP: quem paga e quem usa
3. Proposta em 1 frase e o contraste
4. Aha, evento de ativação e tempo até o valor
5. Preço e modelo (hipótese)
6. Gatilho de retenção
7. Escopo da v1: dentro e fora
8. Canal principal e plano dos 10 primeiros
9. 5 hipóteses e critério de parada
10. Scorecard e veredito
11. Fontes

**Formato**:

- Lido uma vez: na resposta.
- Para guardar ou compartilhar: um doc.
- Dentro da Forja: vira `produto_brief.py`, lido pelo Vision Board, pelo PRD e pelo pitch.

**Próximos passos naturais**: skill `nome` (se ainda não houver nome), depois `forja`.
