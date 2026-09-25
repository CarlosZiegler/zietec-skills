# Suportes e camadas críticas

Use quando uma peça tem pés, rebaixos, tetos, tubos, molduras elevadas ou quando o slicer/uma foto mostra cantilever ou espaguete.

## O que o teste de geometria pode dizer

Uma casca fechada pode ter poucos pés na mesa e um teto amplo alguns milímetros acima. O mínimo Z e o volume permanecem corretos. Vistas superiores escondem isso. Examine as faces inferiores, a área que toca a mesa e o primeiro aparecimento de cada região.

O helper `audit_stl.py` usa coordenadas exatas para conectividade, sem soldar vértices. Soma áreas de triângulos com normal geométrica voltada para baixo. Reporta sua altura e agrupa faces quase horizontais com a tolerância Z informada (padrão 0,001 mm). Não calcule comprimento de ponte a partir dessa soma: patches distintos podem estar no mesmo grupo. Normais incorretas, cascas sobrepostas ou auto-interseções tornam essa área inadequada para conclusões físicas; resolva o problema de malha separadamente.

Uma face inclinada cujo máximo Z supera a mesa também gera revisão, mesmo se puder ser autoportante. Essa triagem conservadora **não é um gerador de suportes** nem um teste completo de manifold por vértice. Uma peça que passa ainda pode ser muito fina, instável ou apresentar overhang não representado por faces horizontais.

## Como fechar um achado

Uma cavidade fechada legítima tem uma casca interna com volume orientado negativo. O helper sinaliza para revisão quando os limites dessa casca cabem nos de uma casca positiva; isso é apenas uma candidata a cavidade, não uma prova de contenção. Confira a geometria e o slice antes de inverter normais ou preencher vazios. O helper não calcula o aninhamento exato entre cascas.

Registre peça, região, altura, material/perfil e decisão:

- **Reorientação:** maior apoio, face aceitável e dimensões preservadas; valide todas as novas superfícies inferiores após girar.
- **Redesenho/divisão:** elimine o vão, separe pés ou adicione chanfros, preservando forma e montagem autorizadas. Não preencha uma cavidade funcional sem considerar sua função.
- **Ponte sem suporte:** meça vão e ancoragem nas trajetórias reais; justifique por teste aplicável ao material, direção e perfil. Um teto classificado como “Bridge” pelo slicer pode continuar impossível na prática.
- **Suporte:** confirme acesso de remoção, caminho de apoio, interface e parâmetros efetivos por objeto. Brim não alcança um teto elevado. Distância zero depende de par de materiais compatível, não de usar outro bico.

No Studio, confira tipo/estilo, “on build plate only”, blockers/enforcers, “don't support bridges”, threshold e distâncias de interface. Uma dessas opções pode impedir apoio mesmo com suporte ativado. Não altere todos os objetos quando apenas uma base precisa disso.

No preview por tipo de linha, veja **antes/no início/depois da altura crítica**. O suporte deve ocupar a região relevante e chegar perto da face, respeitando a separação definida. Alturas de suporte podem diferir das camadas do modelo; use Z real, não apenas índice. Para remover, siga material/perfil e espere a peça esfriar; não há prazo universal de duas horas.

G-code pode ajudar: confirme versão, modo absoluto/relativo, extrusões positivas, alturas e coordenadas/transformações do objeto. `; FEATURE: Support` em outra região não valida a base. Um aviso ausente, um total de gramas maior ou um log com retorno 0 também não prova apoio.

## Caso de regressão: base com pés

No projeto que motivou esta revisão, a base cinza era uma malha fechada, com mínimo Z em 0, dimensões aproximadas de **189,5 × 90 × 16 mm**, contato plano de cerca de **2.260 mm²** e uma grande face inferior de aproximadamente **11.971 mm² a Z=2 mm**. O projeto estava com suporte desligado. O slicer concluiu o trabalho sem warning de suporte, mas a impressão falhou na região da base.

A correção preservou as malhas e os quatro plates por cor. Ativou suporte normal somente na base, a partir da mesa, permitindo apoio sob pontes, com interface de três camadas, distância superior de 0,20 mm e mesmo PLA cinza. O fatiamento gerou suporte na região; a impressão física corrigida ainda não tinha sido testada ao registrar o caso. Esses valores descrevem esse projeto, **não um preset geral**.

**Resultado esperado da triagem:** a base deve exigir revisão apesar de ser fechada e tocar a mesa. Um modelo com rebaixo de **0,25 mm** também deve ser sinalizado. O STL permanece sinalizado depois de configurar suporte no 3MF: a geometria não mudou; a evidência para fechar o achado é o apoio no slice final.

Os testes do repositório geram uma base simplificada fechada com quatro pés e plataforma em Z=2 mm. Eles não dependem de fotos, arquivos privados ou da impressora.

## Fontes e alcance

- [Bambu Studio: parâmetros de suporte](https://wiki.bambulab.com/en/software/bambu-studio/support) e [support painting](https://wiki.bambulab.com/en/software/bambu-studio/support-painting).
- [Bambu Studio: CLI, prioridades e exemplos](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage).
- [Prusa: modelagem para impressão e suporte](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135).

O caso numérico e os checks do helper são evidência local/heurísticas desta skill. Não são uma especificação de tolerância ou capacidade da fabricante.
