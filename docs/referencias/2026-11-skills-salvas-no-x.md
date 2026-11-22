# Levantamento: skills e tools salvas no X (novembro de 2026)

Feito em 2026-11-22 a partir dos Itens salvos de @CarlosZiegler. Versão viva e editável: [doc no Claude](https://claude.ai/artifact/SPsT9deJncwaspxP8BisSs). Lista bruta: [2026-11-x-salvos-lista-bruta.md](./2026-11-x-salvos-lista-bruta.md).

## Resumo

A skill de produto que estava na memória é a **revenue-centric-design**, salva duas vezes em outubro. Para naming e simplificação de design não havia nada salvo, então as skills `nome` e `simplificar-design` foram montadas a partir de referências públicas.

Varredura:

- **Rolagem completa**: 828 posts, de 11/10 a 17/11/2026 (o X parou de carregar antes disso).
- **Busca dentro dos salvos**, cobrindo todo o histórico: skill (152), product (85), produto (9), brand (24), naming (6), nome (5), simplify (6), PRD (3), minimal, clean, less.

## A skill de produto

[revenue-centric-design](https://github.com/heliocosta-dev/revenue-centric-design), de Helio Costa, destila 134 princípios do designer de produto Richard ([@richardrx](https://x.com/richardrx)) sobre SaaS que converte, retém e monetiza. Salva em [13/10](https://x.com/heliocosta/status/2109803905400127819) e [17/10](https://x.com/Hamerti015/status/2111288295825043676).

- **Cobre**: 12 temas, entre eles landing e CRO, onboarding e ativação, pricing (decoy, Good-Better-Best), churn, disciplina de features, ICP e go-to-market.
- **Espinha**: 9 princípios, como "neutralidade é omissão", "valor primeiro, peça depois" e "preço é filtro".
- **Licença**: própria. Exige atribuição e proíbe uso em apostas e cassino.
- **Instalar**: `npx skills add heliocosta-dev/revenue-centric-design`

A skill [`produto`](../../skills/product/produto/SKILL.md) usa essa como consulta, sem copiar o texto. Outras bibliotecas de PM achadas na web: [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) e [phuryn/pm-skills](https://github.com/phuryn/pm-skills).

## Design e UI

| Skill | O que faz | Na Forja v2? |
|---|---|---|
| [craft](https://github.com/diego3g/craft) | Brief DESIGN.md, todos os estados, 3 direções, crítica | Sim |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | prototype, choreograph, learn-taste, gestures, animate-expo, mobile-native, break-ui | Sim |
| [gridlines](https://github.com/pritamux/gridlines) | Passe de alinhamento com linhas-guia | Sim |
| [impeccable](https://github.com/pbakaus/impeccable) | 24 comandos: distill, critique, polish, PRODUCT.md | distill virou `simplificar-design` |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | Direção de arte, assets e checagem no navegador; minimalist-ui | Referência |
| [refactoring-ui-skill](https://github.com/s0xDk/refactoring-ui-skill) | Regras do livro Refactoring UI | Base da `simplificar-design` |
| [variate](https://x.com/nutlope/status/2090476277190836710) | Variações de uma UI para iterar | Coberto pelas 3 direções |
| [unslop-ui](https://x.com/fildotai/status/2123086579388277020) | Tira a cara de "feito por IA" | Não |
| [un-slop 2.0](https://x.com/tobiadonadon_/status/2109682521466446062) | Mesmo objetivo, nativo iOS e Android | Não |
| [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) | DESIGN.md de marcas conhecidas | Formato do `DESIGN.md` do handoff |
| [transitions.dev](https://x.com/Jakubantalik/status/2119464965551931531) | Biblioteca, skill e MCP de transições | Não |
| [device-frames](https://x.com/Ibelick/status/2123077098298282203) | Molduras de iPhone, iPad e Mac em código | Página Lançamento |
| [html-demo](https://x.com/MengTo/status/2112843787777249661) | O app vira uma demo HTML animável | Não |
| [anatomy](https://github.com/wheresryan22/anatomy) | Explicações visuais isométricas e 3D | Não |
| [ui-diff](https://x.com/imuratalpay/status/2123745913063477684) | Screenshots antes e depois em todo PR de UI | `CLAUDE.md` do handoff |
| [HIG skill](https://x.com/PaulSolt/status/2096671265234833498) e [lintapple](https://x.com/Frozune/status/2109309297612013621) | Diretrizes da Apple como guia e como lint | Não |
| [/design do Claude Code](https://x.com/ClaudeDevs/status/2089471692762673408) | Artboards do Claude Design no CLI | Não |

Simplificação: além do distill, os "simplify" salvos são de código: [/simplify](https://x.com/BHolmesDev/status/2085764660515443181) e [Ponytail](https://x.com/Voxyz_ai/status/2113344640959250912).

## Produto, growth e naming

| Item | Por que importa | Fonte |
|---|---|---|
| revenue-centric-design | Conversão, ativação, pricing, churn, ICP | [salvo](https://x.com/Hamerti015/status/2111288295825043676) |
| /grill-me (Matt Pocock) | Interroga a ideia até ela ficar clara | [salvo](https://x.com/erickwendel/status/2123181404309561359) |
| "O ponto de partida é uma dor" | Validar a dor antes da solução | [salvo](https://x.com/gabrielbuzziv/status/2105472007877886029) |
| App de US$ 7k/mês | Nicho validado, reviews dos concorrentes, melhor UI e onboarding | [salvo](https://x.com/frederickjames/status/2080603050327097694) |
| Distribuição por vídeo curto | Formato viral do nicho, vários vídeos por dia, UGC | [salvo](https://x.com/ErnestoSOFTWARE/status/2082137010802712578) |
| /REA-growth | Engenharia reversa do growth de qualquer empresa | [salvo](https://x.com/jasonzhou1993/status/2116122945605222637) |
| /leads-signal | Monitora menções, reclamações e reviews | [salvo](https://x.com/jasonzhou1993/status/2104526470760792424) |
| Workflows dinâmicos (Thariq) | Exemplo literal: brainstorm de nomes e torneio para escolher os 3 melhores | [salvo](https://x.com/trq212/status/2061907337154367865) |
| Brand kit a partir de logos | Identidade rápida depois do nome | [salvo](https://x.com/nutlope/status/2120191610428227595) |
| brand-naming (arnabbagxd) | Estratégia, 7 testes, top 5 | [web](https://github.com/arnabbagxd/brand-building-skills) |
| brand-naming-strategies | SMILE e SCRATCH, matriz, funil, domínio (MIT) | [web](https://github.com/mike-coulbourn/claude-vibes) |
| product-name (pm-skills) | 5 nomes com racional | [web](https://github.com/phuryn/pm-skills) |

## Mobile, Expo e iOS

| Ferramenta | Para quê | Fonte |
|---|---|---|
| expo/skills, Appllama, emilkowalski, vercel-labs, SwiftUI-Agent-Skill | Pacote de 5 skills para app iOS | [salvo](https://x.com/jaimintf/status/2091131151444574515) |
| React Native Deploy | Substituto gratuito do EAS Build | [salvo](https://x.com/bidah/status/2119868337920282760) |
| Xcode no Claude Code | Claude compila, roda no simulador e corrige | [salvo](https://x.com/bidah/status/2119407965203472876) |
| `npx @expo/explore` | Mapa de telas do app | [salvo](https://x.com/DaehyeonMun/status/2120955532060287000) |
| App Flow (Mobile Dev) | Agente mapeia navegação e captura estados | [salvo](https://x.com/hurali97/status/2117943373357355097) |
| Mobile Dev Codex Plugin | Traces de performance no simulador | [salvo](https://x.com/mrousavy/status/2117976155580240156) |
| Argent | Reproduz, mede e verifica performance | [salvo](https://x.com/argent_ai_/status/2118716994866257935) |
| Simlock | Nuvem própria de simuladores para agentes | [salvo](https://x.com/thymikee/status/2116104729558126944) |
| simslim | Simuladores com até 4× menos RAM | [salvo](https://x.com/interlap01/status/2114295627924304226) |
| terminal-phone | iPhone real no terminal; vídeos e screenshots de loja | [salvo](https://x.com/kirtandopamine/status/2119814854660042975) |
| App Store Connect CLI | Publicação e metadados pela linha de comando | [salvo](https://x.com/rudrank/status/2116684860177961035) |
| Native Cook | 750+ blocos de UI mobile em vídeo | [salvo](https://x.com/ngocdevv/status/2117645490057892004) |
| Glassy UI | Componentes liquid glass para React e RN | [salvo](https://x.com/AlexBurlis/status/2112517518581481539) |
| Screenshots de App Store | Serviço e skill de screenshots | [salvo](https://x.com/jaydwivedi_/status/2122633252145918215) |

## Vídeo, motion e marketing

| Ferramenta | Para quê | Fonte |
|---|---|---|
| hyperframes + 19 skills de motion | HTML vira vídeo; lista curada | [salvo](https://x.com/Y0urDumble/status/2119793194435027220) |
| brag | Lê o repo e gera teaser com som e copy | [salvo](https://x.com/shiri_shh/status/2103521939134550246) |
| /stick-scene | Bonecos animados explicando o produto | [salvo](https://x.com/sl1ma4/status/2122649243189932538) |
| Motion in Claude | URL do produto vira vídeo de lançamento | [salvo](https://x.com/motion_so/status/2083992227114520576) |
| Cinetic e earshot | Cenas prontas e sons gerados por código | [salvo](https://x.com/LexnLin/status/2118327859282612400) |
| motion-design-skill (LottieFiles) e mais 19 repos | Timing, easing, coreografia | [salvo](https://x.com/N01ennn/status/2111888466829303973) |
| Styleguide de vídeo | Um guia de estilo de vídeo por produto | [salvo](https://x.com/dieegosf/status/2122312655826526408) |
| ffmpeg-skill | Edição local por agente, 42 ferramentas | [salvo](https://x.com/kebura_P/status/2095736887034212809) |
| Center Stage | Screenshot ou gravação vira product shot | [salvo](https://x.com/davidhaz/status/2111740602832597152) |
| Ava Studio | Vídeos de TikTok e Reels a partir da URL | [salvo](https://x.com/avastudio_/status/2112606581229769030) |

## Agentes, verificação e workflow de código

| Ferramenta | Para quê | Fonte |
|---|---|---|
| Workflows dinâmicos | Fan-out, verificação adversária, torneio, loop até acabar | [salvo](https://x.com/trq212/status/2061907337154367865) |
| /create-verification-skill + e2e | O agente verifica e traz evidência | [salvo](https://x.com/o_kwasniewski/status/2109694443410399543) |
| pstack | create-formal-verification-skill, statechart, unslop | [salvo](https://x.com/poteto/status/2119521036660314339) |
| /show-me | Explica com tipos, árvores e diagramas | [salvo](https://x.com/dexhorthy/status/2087569590268391897) |
| /merge-risk | Nota de risco do PR em 5 categorias | [salvo](https://x.com/BHolmesDev/status/2112653011369807971) |
| security-audit-skill | Auditoria de segurança em 6 fases (Cloudflare) | [salvo](https://x.com/CloudflareDev/status/2118013149538390253) |
| Ponytail e /untangle-codebase | Menos código, sem abstração vazada | [salvo](https://x.com/mazeincoding/status/2118378945557004477) |
| agent-browser e agent-desktop | Navegador e desktop para o agente testar | [salvo](https://x.com/ctatedev/status/2122476614286008392) |
| executor.sh | Um link junta MCPs, skills e CLIs | [salvo](https://x.com/maykbrito/status/2121335037891137713) |
| council | O agente consulta outros CLIs antes de decidir | [salvo](https://x.com/thekitze/status/2096010451251499343) |
| 12 regras de CLAUDE.md | Regras do Karpathy + 8 para trabalho de agente | [salvo](https://x.com/Mnilax/status/2053116311132155938) |

## Lacunas da Forja (resolvidas na v2)

| # | Lacuna | Na v2 |
|---|---|---|
| 1 | Validar o produto | Etapa 0.1 com a skill `produto` |
| 2 | Nome | Etapa 0.2 com a skill `nome` |
| 3 | Onboarding e paywall | Telas 6 (onboarding ativo) e 7 (upgrade no limite) |
| 4 | Simplificar | Passe da `simplificar-design` antes da auto-revisão |
| 5 | Checar fatos com outro agente | Subagente confere cada afirmação na fonte |
| 6 | Passar para código | `DESIGN.md`, `PRD.md`, `CLAUDE.md`; opção Expo no ARD |
| 7 | Material de lançamento | Página Lançamento: screenshots de loja e storyboard do teaser |
| 8 | Distribuição e ativação | Canal e 10 primeiros no PRD e no pitch; evento de ativação no ARD |
