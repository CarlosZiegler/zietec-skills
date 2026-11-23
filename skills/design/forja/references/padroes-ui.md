# Padrões de UI reutilizáveis (destilados de bibliotecas de referência)

Componentes e padrões que valem para qualquer produto da Forja, dentro da base do `estilo-base.md`. Cada um diz **quando usar**, **anatomia** e **regras**. Antes de inventar um componente, procure aqui; antes de desenhar um flow, faça a pesquisa do `flows.md` §1b.

Fontes (padrões, nunca código nem visual copiado): bencho.dev, uiarc.dev, boardui.com, pro.beui.dev, kobra.systems, affectui.com, libraries.dev, ui.watermelon.sh (nov/2026). Para a estrutura de flows, Mobbin e Appllama.

## 1. Entrada de número

**Régua de seleção** (bencho): faixa horizontal de traços com o valor grande acima; arrastar com o polegar, encaixe a cada passo com háptico.
- Use para: número que a pessoa ajusta perto do valor anterior (carga, repetições, peso corporal, minutos, porções, quantidade).
- Anatomia: `valor` (número-herói, tabular) · `unidade` · `régua` (traços a cada passo, traço maior a cada 5/10) · `marcador` central fixo · `anterior` (traço com ponto do último valor).
- Regras: passo do domínio (2,5 kg, 1 rep); toque no número abre o teclado numérico (acessibilidade e valor longe); `±` de 44 px nas pontas; nunca a única forma de entrada.

**Stepper** para inteiros pequenos (1–10) e **campo numérico** para valores com muitas casas.

## 2. Gráficos (no estilo da base: tinta, um acento, cinzas)

- **Linha de base pessoal** (uiarc): a série de hoje contra a média da própria pessoa, com faixa sombreada do "normal" e o rótulo "8% acima do seu normal". Use em progresso de qualquer produto (gasto, sono, carga, tempo de foco). Melhor que comparar com outros.
- **Heatmap de atividade** (boardui): grade de dias com intensidade em 4–5 tons da tinta; seletor Semanal · Mensal · Anual em segmento; número-resumo acima ("22 dias ativos"). O dia de hoje no acento.
- **Anel com parciais** (boardui, Pumpy): número no centro + 2–3 parciais em legenda com barra fina (ex.: sono 49/50, energia 29/30; proteína/carbo/gordura). Ticks radiais quando o valor é "consumo contra meta".
- **Barras por período** com segmento Dia/Semana e a última barra em tinta cheia; as anteriores em cinza.
- **Barra empilhada única** (bencho "context"): composição de um total (volume por músculo, gasto por categoria) com chips de legenda embaixo.
- Regras: um gráfico conta uma coisa; título é a conclusão ("+17,5 kg desde o protocolo 1"), não o nome da métrica; eixos mínimos; números tabulares; cor só para o destaque; o detalhe vem ao tocar (tooltip ou folha), não tudo na tela.

## 3. Filas e quadros (painéis de equipe)

**Quadro "precisa de você · em andamento · feito"** (affectui): três colunas ou três seções; cada cartão com quem, o quê, há quanto tempo e a próxima ação. "Precisa de você" sempre primeiro e com contagem. Use em qualquer painel de operação (atendimento, revisão, aprovação). Ação em lote no topo; item aberto em painel lateral, não em página nova.

**Nota enfileirada**: a pessoa deixa uma instrução enquanto algo ainda roda (processamento, revisão), e ela aparece como pendente.

## 4. Estados de espera e de IA

Estados de espera das bibliotecas de IA (libraries.dev, kobra): **orbe/anel "pensando"** discreto em vez de spinner quando há IA ou processamento longo, **texto que aparece em streaming**, **passos de raciocínio** recolhíveis e **loader que vira o resultado** (a imagem nasce do esboço). Na base: uma cor só (tinta ou acento), sem neon nem degradê arco-íris, e sempre com texto do que está acontecendo ("Lendo o exame · 3 de 5 marcadores").

## 5. Microinterações por gesto

Use o catálogo do bencho como checklist do que cada componente faz ao toque: **press** (escala .97), **drag** (segue o dedo, solta com mola), **slide** (régua, seletor), **swipe** (ação de linha com desfazer), **type** (validação inline), **select** (seleção inset), **loading** (skeleton no formato do conteúdo). Som desligado por padrão.

## 6. Documentação de componente (kobra)

Cada componente do design system (`design-system.md`) tem:
- **Anatomia**: as partes nomeadas e o `data-slot` de cada uma (`otp.root`, `otp.group`, `otp.slot`, `otp.separator`), para o código estilizar por parte;
- **Props/estados** em tabela;
- um **`prompt.md`** curto para o agente de código ("use quando…, nunca…, combine com…").
OTP: 6 dígitos em grupos de 3–3 com separador; colar preenche tudo.

## 7. Cobertura de telas (beUI Pro)

Catálogo por categoria (entrada, núcleo, comunicação, pagamento, perfil e configurações, **estados**) usado como checklist no inventário: `flows.md` §1.

## 8. O que não trazer

Brilho neon e "border beam" como enfeite fixo, gooey, globos e galáxias decorativos, avatares 3D de mascote, landing de template genérico (watermelon) e degradê de fundo: tudo isso fere o `anti-slop.md`. Entram só se o produto pedir e o usuário aprovar.
