---
name: simplificar-design
description: Simplifica telas, fluxos e interfaces removendo o que não ganha seu lugar: uma ação principal, menos elementos, cores, tamanhos e passos, sem perder função nem acessibilidade. Use para "simplifica", "tá poluído", "limpa essa tela".
---

# Simplificar design

Simplicidade não é tirar feature. É tirar o que fica entre a pessoa e o objetivo dela. Todo elemento justifica sua existência ou sai.

## Modos

- **Revisão** ("o que dá para tirar?"): só relatório. Nada muda até o usuário escolher.
- **Aplicar** ("simplifica", "limpa"): corta, renderiza antes e depois, relata.
- **Autocheck**: chamado por outra skill (ex.: Forja antes da auto-revisão). Corta dentro do escopo e devolve a lista do que mudou.

## 1. Ache a essência

- Qual é o trabalho da tela e a **uma** próxima ação? Se não der para dizer em uma frase, pergunte. Não chute.
- Quais 20% entregam 80% do valor?
- Leia o brief, o DESIGN.md ou o sistema de design. Onde o sistema define um valor, o sistema vence.

## 2. Inventário com números (antes)

Renderize a tela e conte:

- elementos interativos;
- ações com cara de primária;
- cores saturadas;
- tamanhos de fonte e pesos;
- níveis de contêineres aninhados e cards dentro de cards;
- passos do fluxo;
- palavras na tela.

Esses números são o "antes".

## 3. Classifique cada elemento

| Decisão | Quando |
|---|---|
| Manter | serve à ação principal ou à decisão da pessoa |
| Fundir | dois blocos dizem ou fazem a mesma coisa |
| Esconder | é raro: vai para "Mais", acordeão ou etapa seguinte |
| Mover | é usado em outro lugar e deve ficar lá |
| Remover | ninguém sentiria falta |

Cada decisão leva 1 linha de porquê.

## 4. Corte por dimensão

**Arquitetura**

- Uma ação primária, poucas secundárias, o resto terciário ou escondido.
- Nada repetido que já foi dito em outro lugar.

**Visual**

- 1 a 2 cores de marca mais neutros. Cores de status ficam, sempre com forma ou texto junto.
- Uma família de fonte, 3 a 4 tamanhos, 2 a 3 pesos.
- Tire bordas, sombras e fundos que não servem à hierarquia.
- Nunca card dentro de card. Espaço e alinhamento no lugar de caixas.

**Layout**

- Fluxo vertical simples quando der.
- Um alinhamento por grupo.
- Uma escala de espaçamento, com respiro generoso.

**Interação**

- Menos escolhas.
- Padrões inteligentes no lugar de opções.
- Edição no lugar em vez de modal.
- Se o fluxo pode perder um passo, ele perde.

**Texto**

- Corte enchimento, não sentido.
- Voz ativa: "Salvar alterações", não "As alterações serão salvas".
- Sem jargão. Sem título que repete a introdução.
- Botão = verbo + objeto.

**Código** (quando a tela é código)

- CSS morto e componentes órfãos saem.
- Três variantes costumam cobrir 90% dos casos.
- Árvore de componentes mais rasa.
- Prefira o componente que já existe e o recurso nativo do navegador ao feito à mão.

## 5. Nunca sacrifique

- acessibilidade: rótulos, contraste, alvos de pelo menos 44 px, foco visível;
- informação de que a pessoa precisa para decidir;
- os estados: vazio, erro, carregando, offline;
- hierarquia: alguma coisa ainda precisa vencer o primeiro olhar;
- a complexidade real do domínio: simples demais vira mistério;
- função necessária: o que sai de vista precisa de um caminho de acesso.

## 6. Verifique (depois)

- Renderize de novo nos mesmos tamanhos (390 e 1440 px).
- Refaça a contagem do passo 2.
- Teste de 5 segundos: o que se vê primeiro é o mais importante?
- A tarefa principal ficou mais rápida? Tudo o que é necessário continua alcançável?

## 7. Relatório

- Tabela antes e depois com os números do passo 2.
- O que saiu, fundiu ou foi escondido: porquê e onde ficou o acesso.
- O que ficou de propósito, apesar de parecer cortar.
- No modo Revisão: achados ranqueados (bloqueia ou engana > atrasa > parece descuidado). Pare até o usuário escolher.

## Regras

- Mudar uma peça compartilhada (um botão usado em 20 telas) não é corte local: liste as telas afetadas antes de mudar.
- Diga não a boas ideias para dar espaço à execução ótima.
- Na dúvida entre esconder e remover, esconda e registre.

Base: distill (pbakaus/impeccable, Apache-2.0), regras de crítica do craft (diego3g, MIT) e Refactoring UI.
