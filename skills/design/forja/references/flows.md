# Telas completas e flows (como num arquivo de Figma ou no Mobbin)

O pacote não para nas 9 telas-amostra. Depois delas (e antes do doc/pitch final), a Forja desenha **o app inteiro**: cada tela do v1 e cada flow passo a passo, com cada ação e cada ramo. É o que o usuário fez no Doro (≈ 90 telas mobile + portal) e no AutoFolio (23 telas no app + uma página por feature, como "Adicionar carro (inteligente)" com 31 passos em 3 linhas).

Também vale **sempre que o usuário trouxer uma feature nova** num pacote existente: uma página nova só daquela feature, com o flow completo, nome terminando em "(aprovar)".

## 1. Inventário de telas (antes de desenhar)

Gere `build/inventario.py` a partir do PRD (user stories + RF), uma linha por tela:

```python
TELAS = [
  # id,          nome,                  área,      flow(s),          origem
  ("M-Hoje",     "Hoje",                "aluna",   ["F3"],           "US-03"),
  ("M-Treino-Serie", "Registrar série", "aluna",   ["F3"],           "US-05"),
  ...
]
FLOWS = [
  # id, nome, quem, gatilho, resultado, telas principais em ordem, ramos
  ("F3", "Fazer o treino do dia", "aluna", "toca Começar treino", "sessão salva com cargas", [...], ["pular exercício", "sem conexão", "sair no meio"]),
]
```

- Toda user story aparece em pelo menos uma tela; toda tela pertence a pelo menos um flow. O script falha se sobrar story sem tela.
- Conte: um v1 típico tem 40–90 telas mobile e 15–40 desktop (com estados). Menos de 30 no total é sinal de amostra, não de app.

## 2. Páginas no canvas

| Página | Conteúdo |
|---|---|
| **App · aluna (mobile)** (nome pelo papel do produto) | todas as telas do inventário, numeradas e na ordem da navegação, em linhas por área (Entrada, Hoje, Treinos, Check-in, Plano, Perfil). Só no idioma-base. |
| **Painel · equipe (desktop)** | o mesmo para o desktop, quando houver. |
| **Flow F1 · <nome>** … uma página por flow | o flow passo a passo (seção 3). |
| **Mapa de flows** | 1 artboard-diagrama: as áreas, os flows e como se ligam (setas), com links para cada página. |

As 9 telas em EN · PT · DE continuam nas páginas Mobile/Desktop do pacote. As páginas de app completo e flows ficam **só no idioma-base** (o seletor de idioma some delas) para o tamanho não explodir; o handoff lista as strings para tradução.

## 3. Como desenhar uma página de flow (padrão AutoFolio)

- **Linhas** com uma nota `title1` em cima de cada uma (≥ 223 px acima):
  1. **Caminho principal** (feliz), do gatilho ao resultado;
  2. **Ramos e estados** (erro, vazio, offline, limite do plano, permissão negada, confiança baixa da IA…);
  3. **Caminhos alternativos** (outra entrada, desfazer, editar depois, outro papel).
- **Cada passo é uma tela inteira** (390×844 ou 1440×…), com o elemento tocado em destaque sutil (anel de 2 px no acento + selo numerado "1" no canto do alvo) e título de board `✓ F3·P4 · Registrar série`.
- **Embaixo de cada tela, um sticky** (`w` igual à tela, ≥ 160 px abaixo) com: **ação** → **resultado**; regra de negócio (RN/RF do PRD); o que acontece se falhar; tempo esperado. Frases curtas.
- **Setas entre passos**: nota `kind: arrow` não é sua; use a ordem + o selo e, nas telas, **links de protótipo** (`<a href="F3-P5.dc.html">`) no elemento tocado, para que `#play-F3-P1` toque o flow inteiro.
- **Sheets, teclados, permissões do sistema e toasts** viram passos próprios (o estado com a folha aberta), não uma nota.
- **No fim da linha principal**, um sticky "Perguntas para você" com as decisões em aberto do flow.
- Espaçamento: 80 px entre telas da mesma linha; 120 px + altura do sticky entre linhas.

## 4. Construção e qualidade

- Reaproveite os componentes do pacote (mesmo `brand.py`, vidro, tab bar, CTA, seleção). Telas de flow não inventam estilo.
- Dados realistas e coerentes entre passos (a mesma aluna, o mesmo treino, os mesmos números do passo anterior).
- Cada flow passa no `slop_check.py`, no checklogic (links do protótipo levam ao próximo passo) e no portão de overflow.
- Olhe o flow em contact sheet por linha: a sequência conta a história sem ler as notas?
- No handoff, `PRD.md` ganha a tabela de flows (id, gatilho, passos, ramos) e `CLAUDE.md` diz "implemente flow por flow, na ordem F1…Fn; cada flow é pronto quando o e2e percorre o caminho principal e os ramos".

## 5. Feature nova num pacote existente

1. Ler o canvas.json publicado e os componentes do build.
2. Inventário só da feature (telas novas + telas que mudam), com os ramos.
3. Página "**<Feature> (aprovar)**" com as 3 linhas da seção 3 e as perguntas.
4. Telas existentes que mudam aparecem no flow com o sufixo "· muda" e uma nota do que mudou.
5. Nada de reescrever as outras páginas; publicar em modo patch.
