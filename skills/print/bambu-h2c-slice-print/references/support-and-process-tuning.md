# Suporte removível e ajustes de processo

Use após decidir que a geometria deve ser preservada, ou ao investigar um defeito específico. Fontes consultadas em **2026-09-12**. Os nomes/opções dependem da versão: registre configuração efetiva e compare o slice, não só a tela de parâmetros.

## Primeiro escolher a estratégia de apoio

A [documentação Bambu de suporte](https://wiki.bambulab.com/en/software/bambu-studio/support) favorece Normal/Hybrid para grandes faces planas e Tree/Hybrid para apoios pequenos e distribuídos. Ela distingue separação vertical, afastamento lateral, corpo e interface; distância zero pressupõe material destacável apropriado. O ângulo de suporte automático é medido **a partir da horizontal**: aumentar o threshold gera mais apoio. Confira essa convenção antes de transportar números de outra ferramenta.

Para a peça concreta:

| Pergunta | Decisão a registrar |
|---|---|
| O vão tem função? | Se é apenas um detalhe inventado, avaliar fundo plano/reorientação/divisão; preservar acesso e encaixes funcionais |
| Como o suporte chega à face? | Conferir caminho a partir da mesa ou do modelo; “on build plate only” não resolve todo teto interno |
| Quais regiões precisam dele? | Pintar regiões críticas quando útil, inspecionar blockers e opções de pontes/pequenos overhangs |
| Como será removido? | Garantir acesso de ferramenta e saída; suporte fechado dentro de cavidade não é removível só por ter gap |
| Quão estável é o apoio? | Avaliar corpo, contato na mesa, altura/ramificações e colisão; interface boa sobre árvore quebrada não funciona |
| Quais materiais realmente se encontram? | Identificar modelo, corpo e interface, por hotend; consultar [compatibilidade](materials-and-h2c.md) |

Pintura não altera por si só o tipo de suporte. Em Auto, regiões automáticas e pintadas podem coexistir; em Manual, o apoio depende de enforcers. Revise a parte inferior e outras faces após pintar: a ferramenta Sphere pode atingir faces fora da vista. [Bambu: support painting](https://wiki.bambulab.com/en/software/bambu-studio/support-painting).

## Ajustar sem trocar todas as variáveis

| Defeito observado | Experimento dirigido | O que pode piorar |
|---|---|---|
| Suporte fundido/difícil de retirar | Conferir material e separação Z/XY; variar uma dimensão em torno do perfil atual | Aumentar separação pode piorar o acabamento ou deixar a primeira trajetória sem apoio |
| Face apoiada com linhas caídas | Ver cobertura, interface e distância real; ensaiar interface mais contínua ou menor separação compatível | Mais contato pode dificultar remoção; não zerar PLA/PLA por tentativa |
| Interface destaca durante a impressão | Rever aderência entre corpo/interface/modelo e estabilidade; usar combinação documentada/testada | “Soltar fácil depois” não serve se já solta durante a deposição |
| Árvore/corpo quebra ou tomba | Melhorar apoio/estrutura ou trocar estratégia nessa região | Mais rigidez/material pode criar marcas ou prender o suporte |
| Ponte sem apoio cede | Ver direção, duas ancoragens e vão; só depois testar velocidade, fluxo e resfriamento de ponte | Aumentar fluxo pode criar acúmulo; fan/velocidade máximos não são soluções universais |

Esses experimentos são hipóteses diagnósticas; não são um preset. Use uma região representativa e compare estabilidade, face inferior e esforço de retirada. Não confunda espaçamento da interface com gap Z: um muda a malha de linhas, o outro a separação da peça. Mais interface pode ajudar o acabamento, mas não é garantia. [Bambu: suporte](https://wiki.bambulab.com/en/software/bambu-studio/support).

### Materiais distintos e trocas

A [receita oficial PLA Basic/PETG HF ou Basic](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support) tem escopo de **produtos Bambu específicos** e distingue qual deles é modelo/interface. Não se estende automaticamente a Matte, Silk, CF, Translucent ou terceiros. Comece pela interface apenas quando indicada; confira temperatura comum da mesa, ambiente e compatibilidade. Não importe o 3MF de exemplo substituindo o perfil H2C da entrega. Consulte os valores da direção escolhida no guia, depois valide no equipamento/perfil real.

O [relato PLA/PETG no fórum H2](https://forum.bambulab.com/t/pla-as-support-for-petg/172107) contém tanto remoção difícil quanto baixa aderência de pares diferentes. É uma razão para testar o par real, não evidência de um valor ótimo. Se houver troca no mesmo hotend, revise purga e união das camadas seguintes; com hotends separados, respeite priming e torre do perfil H2C. Não desative recursos com base em receitas de X1/P1.

## Camadas, paredes, velocidade e acabamento

| Controle | Quando ajuda | Verificação e limite |
|---|---|---|
| Altura de camada / variável | Curvas e degraus em Z; refinar só a faixa que precisa | Não melhora automaticamente resolução XY nem sustenta ilhas; recalcular espessura sólida em mm |
| Classic / Arachne / largura de linha | Detalhes que desaparecem, paredes estreitas, transições de contorno | Arachne pode alargar traços; confira todas as camadas do detalhe e encaixes, não selecionar sempre o mesmo gerador |
| Perímetros / infill / sólidos | Rigidez, fixações e fechamento do topo | Comparar seção real e reforço localizado; 100% não substitui orientação ou material |
| Velocidade / limite volumétrico | Subextrusão em trajetórias rápidas ou largas | Conferir vazão e temperatura efetivas; máximo anunciado da máquina não é velocidade de toda peça |
| Cooling / tempo mínimo de camada | Pontas pequenas deformadas ou camada que não resfria | Equilibrar forma e união entre camadas; considerar material e ventilação local |
| Seam / acabamento superior | Marca visível ou ressalto no encaixe | Posicionar seam fora de superfície funcional; ironing só após fluxo/topo corretos e se acabamento justificar o tempo |
| Compensação de pé de elefante / XY | Diferença dimensional identificada em região específica | Medir modelo, slice e cupom; não compensar a mesma folga no CAD e no slicer sem contabilizar ambas |

A [documentação de camada variável Bambu](https://wiki.bambulab.com/en/software/bambu-studio/adaptive-layer-height) registra incompatibilidade com Tree Organic e restrições da torre quando vários objetos usam perfis de altura diferentes. Verifique a versão instalada; não desligue a torre apenas para eliminar o aviso. Respeite o intervalo permitido pelo perfil de bico; o exemplo de bico 0,4 mm no guia não define todos os hotends H2C. Suporte com altura independente exige ler **Z real**, não comparar apenas números de camada.

Nos [padrões de infill descritos pela Prusa](https://help.prusa3d.com/article/infill-patterns_177130), Grid cruza trajetórias na mesma camada e pode acumular material nos encontros; Gyroid/Rectilinear são alternativas a avaliar quando há colisão nesses pontos. Não atribua todo ruído a infill: um canto levantado, overhang enrolado ou fluxo incorreto também precisa ser investigado. Confirme no Studio os padrões disponíveis.

[Arachne na Prusa](https://help.prusa3d.com/article/arachne-perimeter-generator_352769) explica limites de detalhe e alargamento de linhas. Um [relato com resposta de desenvolvedor Bambu](https://github.com/bambulab/BambuStudio/issues/4387) mostra por que transições precisam de inspeção por camada; não prova que a versão atual tenha o mesmo defeito. [Compensação de pé de elefante](https://help.prusa3d.com/article/elephant-foot-compensation_114487) atua na região inicial; não corrige contração geral ou todos os furos.

## Experimento e critério de aceitação

Preserve um preset de referência. Registre material exato/estado, máquina, bico, placa, orientação, largura/altura de linha e parâmetros alterados. Escolha uma variável por comparação; uma correção de geometria/suporte pode precisar de um conjunto coerente de mudanças, explicitado como tal.

Avalie: detalhe presente, região sustentada, suporte removível, dimensão dentro da tolerância da montagem e resistência compatível com a função. Para calibração de extrusão/material, use [materiais e H2C](materials-and-h2c.md). Não use compensação dimensional para esconder erro de unidade, nem fluxo para esconder uma região que nasce no ar.

Finalize com o [preflight de camadas críticas](../../fdm-print-preflight/SKILL.md). Guarde perfil validado com versão e contexto; um relato de fórum é hipótese, um cupom aprovado cobre suas condições, e a peça final exige sua própria conferência.
