# Material, função e configuração H2C

Leia ao escolher filamento, dimensionar peças, mapear hotends ou investigar extrusão/adesão. Consulta das fontes: **2026-09-12**. Use o produto, a placa, o firmware e o perfil efetivos; números de ficha técnica não dimensionam automaticamente a peça.

## Identificar o que existe e o que a peça precisa

Registre polímero, marca/linha, cor, condição de secagem/armazenamento, bico/diâmetro e alimentação. O nome de um preset não comprova o conteúdo da bobina. A cor branca, por exemplo, não diferencia PLA de PETG HF. Confirme pelos dados disponíveis antes de atribuir peças; não presuma estoque ou estado a partir de um projeto antigo.

| Uso | Critério de seleção e consequência no desenho |
|---|---|
| Souvenir, letras e carcaça de mesa | PLA costuma ser uma opção para detalhe/rigidez em ambiente adequado; dimensões leves podem bastar se suportarem manuseio |
| Peça com impacto, flexão ou temperatura diferente | Comparar a ficha do produto e a orientação; PETG não significa automaticamente mais rigidez ou capacidade para qualquer carga |
| Presilha, pé flexível ou amortecedor | Escolher dureza e geometria flexível; TPU for AMS não equivale a TPU macio |
| Sol/calor, ambiente exigente ou material técnico | Consultar HDT/UV, rigidez, deformação, abrasividade e processamento; não substituir o material disponível por ASA/PA/PC sem necessidade |
| Interface removível ou solúvel | Compatibilidade com modelo, corpo do suporte, hotend e placa; acesso de remoção e estabilidade durante o print |

Como exemplo da diferença entre propriedades, [PLA Basic V3.0](https://store.bblcdn.com/s7/default/b189de92249a4b9ebed28b8ea1f080f0/Bambu_PLA_Basic_Technical_Data_Sheet.pdf) informa módulo XY de 2580 MPa, enquanto [PETG HF V1.0](https://store.bblcdn.com/ce12d65176a94f1086e6aefa238e62e2.pdf) informa 1810 MPa. A escolha requer função e condições: rigidez, impacto e resistência térmica não são a mesma medida. Leia também valores XY/Z e método de ensaio; uma peça fina impressa em outra orientação não herda a resistência do corpo de prova.

O guia de [PLA Basic/PETG como interface](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support) é específico de produtos Bambu. Para usá-lo, confirme identidade e direção modelo/interface; siga [suporte e processo](support-and-process-tuning.md), sem substituir os perfis térmicos de uma variante pela outra.

## Limites que dependem da H2C

O [manual H2C V1.0, pp.90–91](https://csm.bblcdn.com/hub/eff78da43720461787dc8bbe5fa0372d.pdf) diferencia regiões e alturas por hotend. Consulte o perfil atual: peça, suporte, interface e torre precisam estar alcançáveis pelos hotends que os imprimem. O envelope total não é o volume comum para multimateriais. Não copiar um perfil H2D/X1 para liberar uma área ou evitar erro.

Verifique o [H2C Filament Printing Guide](https://wiki.bambulab.com/en/h2c/h2c-filament-printing-guide) antes do mapeamento. Ele contém restrições para flexíveis macios, percurso de materiais abrasivos e combinação de PVA/PETG entre hotends. Não deduza compatibilidade só pela temperatura máxima do bico ou pelo fato de a bobina caber no AMS.

Na consulta registrada, a seção “PET/PPA/PPS-CF” restringe esses materiais com fibra de carbono ao esquerdo; o guia lista TPU macio à direita e proíbe PVA/PETG simultâneos em hotends opostos por exposição térmica do PVA. A alternativa PVA/PETG descrita usa apenas o direito com trocas via AMS. Verifique essa configuração no guia/perfil atual; recursos anunciados como futuros não contam como disponíveis. Não generalize a restrição de descarga de TPU macio para TPU for AMS.

O [TPU for AMS](https://store.bblcdn.eu/s8/default/0b83dc5419534babb4287686cb8c7375/Bambu_TPU_for_AMS_Technical_Data_Sheet.pdf) da ficha consultada é 68D, diferente de TPU 95A. Confirme dureza, versão do AMS, alimentação, diâmetro de bico e restrições Vortek do produto escolhido. A opção de material no Studio não prova a montagem física.

Para filamentos com fibras/cargas, confira abrasividade e bico/caminho adequados. Não trate adição de fibra como garantia de resistência entre camadas ou aceitação de qualquer detalhe fino. Material técnico deve vir acompanhado da sua ficha e preset compatível, não de uma tabela universal desta skill.

## Calibração: três controles diferentes

Comece pelo preset compatível. Não calibre sobre filamento degradado/úmido ou possível obstrução sem investigar a condição primeiro.

| Controle | O que muda | Quando investigar |
|---|---|---|
| Flow ratio / Flow Rate | Quantidade de extrusão | Excesso/lacunas persistentes em trajetórias que existem no slice |
| Flow Dynamics / K | Resposta da extrusão à variação de velocidade | Cantos/transições; mudança relevante de hotend, material ou condição |
| Maximum volumetric speed | Limite de vazão em mm³/s | Subextrusão/qualidade que piora ao aumentar velocidade, altura ou largura |

Os guias [Flow Rate](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate) e [Flow Dynamics](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa) cobrem diferentes gerações de máquina. Descubra o método suportado na H2C instalada; não copie a sequência de calibração, Lidar ou limitações de uma X1/A1. Salve resultado associado ao material/hotend e confirme seu uso no projeto.

A aproximação **Q ≈ largura × altura × velocidade** ajuda a detectar uma exigência incoerente: `0,45 × 0,20 × 200 = 18 mm³/s`. É uma conta ilustrativa, não velocidade recomendada. O preview e o perfil determinam a vazão efetiva; aumentar o limite configurado não aumenta a capacidade de fusão. [Bambu: volumetric speed](https://wiki.bambulab.com/en/knowledge-sharing/volumetric-speed).

## Secagem, resfriamento e placa

- **Secagem:** método e temperatura importam. PETG HF da ficha consultada indica 65 °C/8 h em ar forçado; isso não é receita para PLA, mesa aquecida ou qualquer AMS. Consulte [secagem Bambu](https://wiki.bambulab.com/en/filament-acc/filament/dry-filament), limites do carretel/equipamento e instruções atuais. Embalagem nova, dessecante ou umidade baixa da caixa não provam filamento seco.
- **Cooling:** diferencie ventilação da peça, auxiliar e ambiente/câmara. Ajuste por material e sintoma. Duas TDS oficiais PETG HF V1.0 apresentam orientações de cooling diferentes ([ficha alternativa](https://store.bblcdn.com/s6/default/20423d7f839c4a66b9712508549c68b4/Bambu_PETG_HF_TDS.pdf)); registre a fonte e o preset, sem tornar um percentual regra geral. Testes de [temperatura](https://www.cnckitchen.com/blog/the-influence-of-extrusion-temperature-on-layer-adhesion) e [ventilação do CNC Kitchen](https://www.cnckitchen.com/blog/transparent-fdm-3d-prints-are-clearly-stronger) também mostram resultados condicionais, não melhora ilimitada ao subir temperatura ou desligar fan.
- **Placa:** confirmar superfície física e preset. A orientação de cola da [Smooth PEI/High Temperature Plate](https://wiki.bambulab.com/en/general/high-temperature-plate-not-working-as-expected) inclui proteção/separação para certos materiais; não significa “mais cola em qualquer plate”. Limpeza e remoção seguem a superfície específica. Uma base no ar continua no ar após limpar a mesa.
- **Perfis:** JSON pode herdar parâmetros e guardar listas. O [perfil público PETG HF/H2C](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/filament/Bambu%20PETG%20HF%20%40BBL%20H2C.json) é uma referência mutável, não a configuração instalada. Não substituir o pacote local inteiro por `master` nem escolher arbitrariamente o primeiro elemento de uma lista.

Agrupe por cor **e material/processo compatível**. Suporte de outro polímero pode exigir dois materiais no mesmo plate. Se houver conflito de alimentação, temperatura ou área de hotend, explique a exceção e preserve a intenção de montagem. Nunca atribua PETG à peça só por coincidir com a cor desejada sem rever geometria e processo.

## Registrar o conhecimento útil para o próximo projeto

Guarde fabricante/variante/cor, secagem, bico, placa, versões, largura/altura, orientação, ajustes, cupom/peça e resultado. Separe “documentação recomenda”, “relato comunitário”, “teste neste conjunto” e “não verificado”. Reutilize um perfil aprovado quando as condições forem equivalentes; não transforme um teste isolado em garantia para outros materiais ou geometrias.
