# Decisões de projeto para FDM

Leia antes de definir geometria, espessuras e orientação. Síntese de documentação e ensaios consultados em **2026-09-12**; os exemplos de projeto abaixo são pontos de partida para avaliação, não especificações certificadas da H2C.

## Começar pela função e pelo material

Defina uso, tamanho, acabamento visível, carga/direção, flexão repetida, calor/sol e montagem. Para um souvenir de mesa, não invente requisito estrutural; para uma presilha ou suporte funcional, não assuma que um perfil decorativo basta. Escolha o filamento antes de fechar paredes e folgas, usando [materiais e H2C](../../bambu-h2c-slice-print/references/materials-and-h2c.md).

Registre por peça: face na mesa, espessura mínima local, parede externa, fundo/teto, detalhes finos, fixações e orientação da carga. Diferencie espessura da geometria, número de linhas de parede e espessura das camadas sólidas: são decisões relacionadas, não sinônimos.

## Evitar suporte por projeto, quando a intenção permitir

Antes de acrescentar pés, relevos e rebaixos, veja a peça **por baixo** e imagine a primeira camada de cada região.

| Situação | Opção a avaliar primeiro | O que preservar/conferir |
|---|---|---|
| Fundo decorativo que ficaria suspenso por pequenos pés | Fundo plano na orientação de impressão; detalhes na face visível ou pés separados | Aparência solicitada, altura final e montagem; não criar o vão apenas para parecer industrial |
| Rebaixo para encaixe, passagem, sensor ou acesso | Orientar a abertura para cima, dividir em partes ou dar apoio removível | Volume funcional e acesso; não preencher só para eliminar o alerta |
| Aresta inferior arredondada | Chanfro compatível com a forma | O fillet inferior começa com avanço abrupto; não proibir fillets em outras regiões |
| Tubo, furo horizontal ou cavidade com teto | Mudar orientação, dividir ou alterar o teto quando a função permitir | Diâmetro útil, passagem e montagem; forma em gota/chanfro é opção de redesenho, não substituição automática de um furo circular |
| Nome, logotipo e ornamento | Face plana para colagem/impressão e detalhe voltado para cima | Texto presente no slice, espessura do traço e resultado visual |
| Encaixe ou nervura sob carga | Orientar a seção crítica e suavizar mudanças de seção | Carga entre camadas e área de união; não fazer a nervura nascer no ar |

Essas opções aplicam os princípios de [orientação, divisão e chanfro da Prusa](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) ao projeto solicitado. Compare soluções por aparência, montagem, remoção, gramas e tempo. Suporte é uma solução válida quando preserva melhor a função e a forma.

**Três situações diferentes:** um overhang recebe apoio parcial da camada anterior; uma ponte tem trajetórias ancoradas nas duas pontas; uma ilha começa sem apoio. Diminuir a camada pode reduzir o avanço lateral de um overhang, mas não cria material sob uma ilha ou um teto amplo. Uma reentrância de 0,25 mm ainda precisa dessa análise. Use as trajetórias reais, não só um ângulo de malha.

## Espessura por função, sem engrossar tudo

Use a largura de linha efetiva `w` para estimar o espaço das paredes. Com `w=0,45 mm`, duas e quatro linhas sugerem aproximadamente `0,9` e `1,8 mm`; sobreposição e largura variável mudam o resultado. Isso **não** impõe múltiplos exatos de `w` nem prova resistência. Confira a seção fatiada. [Arachne](https://help.prusa3d.com/article/arachne-perimeter-generator_352769) pode alargar detalhes finos ou omiti-los conforme seus limites; compare com Classic quando o resultado se afastar do desenho.

| Função | Como escolher material na peça | Verificação necessária |
|---|---|---|
| Letra, tampa ou carcaça decorativa | Ensaiar poucas linhas contínuas, reforçando bordas de manuseio quando necessário | Detalhes presentes, sem transparência ou flexão indesejada; uma parede imprimível pode ser frágil |
| Painel/fundo largo | Comparar espessura, nervuras e distância entre apoios | Flexão, fechamento do topo e warping; não resolver automaticamente com 100% de infill |
| Parafuso, pino ou apoio carregado | Mais material na fixação e no caminho da carga | Espessura ao redor do furo, orientação, aperto e seção real; considerar insertos apenas se fazem parte da montagem |
| Presilha/encaixe flexível | Comprimento flexível, transição arredondada e material apropriado | Flexão e ciclos; engrossar pode impedir o movimento ou elevar a deformação local |

Perímetros, orientação e preenchimento têm funções diferentes. A [orientação oficial sobre infill](https://help.prusa3d.com/article/infill_42) e o [ensaio de reforço localizado do CNC Kitchen](https://www.cnckitchen.com/blog/gradient-infill-for-3d-prints) apoiam avaliar onde o material trabalha; o ganho depende da forma e da carga. Use modificadores locais de processo quando fizerem sentido, sem alterar a geometria funcional silenciosamente.

Para fundos e tetos, defina também espessura em **mm**. Em camadas uniformes, `n = ceil(espessura_alvo / altura_da_camada)` é uma conta inicial: `0,8 mm` pede quatro camadas de `0,20`, cinco de `0,16` ou sete de `0,12 mm`. Com altura variável, confira a soma real e o mínimo de espessura do slicer. Mais camadas finas não significam automaticamente mais material. O teto inicial faz ponte sobre o infill; avalie seu apoio antes de só acrescentar camadas. [Prusa: layers and perimeters](https://help.prusa3d.com/article/layers-and-perimeters_1748).

## Resolução, tolerâncias e exportação no Blender

- Altura de camada melhora resolução em Z; letras e encaixes em XY dependem da geometria, bico e largura de linha. Escolha camada variável apenas onde ajuda, verificando as [restrições de suporte e torre](../../bambu-h2c-slice-print/references/support-and-process-tuning.md).
- Preserve folga de montagem no modelo. Registre folga radial/diametral; teste com as mesmas orientações e materiais. Não combine aumento do furo no Blender, escala global e compensação XY sem medir o efeito acumulado.
- `Shade Smooth` e normais de sombreamento não acrescentam polígonos ao STL. Defina resolução geométrica suficiente para curvas/furos sem arquivos desnecessariamente pesados. Reimporte e meça.
- [Solidify no Blender 4.5](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/solidify.html) usa coordenadas locais; escala não uniforme altera espessuras e “Even Thickness” é aproximado. Faça ajustes em cópia e meça a parede final, especialmente após Boolean/Bevel, nos encontros de faces e nas regiões estreitas.
- Use os checks disponíveis de [3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html) para interseções, degenerações, distorção, espessura e overhang. O manual 4.1 descreve a versão antiga: na instalação atual, descubra a extensão e os operadores presentes. “Check All” não autoriza executar “Make Manifold” na fonte original.
- Verifique se a exportação usa a malha avaliada de **viewport ou render**, inclusive visibilidade e níveis de modifiers. A [extensão 1.4.1](https://extensions.blender.org/add-ons/print3d-toolbox/) registra uma correção de exportação STL para Blender 5.2. Não presuma comportamento igual em todas as versões; compare a geometria exportada com a que foi conferida.

## Cupom que responde à dúvida

Para folga, imprima pares de teste. Para apoio, preserve vão, direção de ponte, altura de início e área de contato; reduzir o tamanho pode apagar o defeito. Para carga, preserve seção crítica, orientação e material. Registre critério de aceitação antes do teste. Um único cupom de ponte não valida todos os tetos, nem um cubo valida uma presilha.

Ao concluir, registre por que um relevo foi mantido/removido, onde foi acrescentada espessura e qual região precisa de suporte/teste. Continue com o [preflight](../../fdm-print-preflight/SKILL.md); essa análise de projeto não substitui o slice final.
