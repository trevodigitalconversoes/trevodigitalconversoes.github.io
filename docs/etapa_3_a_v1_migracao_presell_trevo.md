# Etapa 3A — Migração da pre-sell "Fotografia + Presets" para o Trevo

- **Status:** `CANDIDATA_APROVADA_TECNICAMENTE`, não `VALIDADA_EM_FLUXO_REAL`.
- **Objetivo:** corrigir o erro arquitetural do
  [PR #51](https://github.com/correa0inaiara/afiliados-mega-lab/pull/51)
  (`afiliados-mega-lab`), que implementou a pre-sell pública "10 Dicas
  de Fotografia + 18 Presets de Lightroom" dentro do repositório
  operacional/experimental em vez do repositório proprietário das
  páginas públicas. Ver `docs/ADR_PRESELL_OWNERSHIP.md` para a decisão
  arquitetural completa.

## Origem

- Repositório: `correa0inaiara/afiliados-mega-lab`.
- PR: [#51](https://github.com/correa0inaiara/afiliados-mega-lab/pull/51)
  (`feature/claude/presell-fotografia-presets-figma`), estado `OPEN`,
  **não mesclado**.
- Commit final referenciado no PR: `c395cce`.
- Fontes autoritativas usadas pelo PR #51 (preservadas aqui):
  1. **Figma aprovado** — "Pre-sell v1 — arOS aprovado"
     (`https://www.figma.com/design/JfFVjorjpwQdfDrrgCo66k`).
  2. **Copy comercial** — extraída literalmente dos layers do Figma
     aprovado (a resposta bruta da arOS para a landing nunca foi
     preservada no AML — divergência documentada pelo próprio PR #51,
     não escondida).
  3. **Assets oficiais** — 5 imagens fornecidas pela produtora,
     hashes SHA-256 confirmados.

## O que foi reaproveitado literalmente

- **Toda a copy comercial** de
  `apps/web/src/lib/presell/content.ts` (headline, corpo, CTAs,
  legendas dos 3 presets, bullets do que está incluído, público
  "é para você / não é para você", passos de "como funciona",
  parágrafos de transparência/disclosure) — transcrita sem alteração
  de palavra para `aprovacao/fotografia-presets-lightroom/index.html`.
- **A ordem e o conjunto de seções**: Hero → Problema → Demonstrações
  (3 presets) → O que está incluído → Público-alvo → Como funciona →
  Transparência → CTA final. Idêntico ao `page.tsx` do PR #51.
- **Os 5 assets oficiais**, byte-idênticos (ver seção Hashes).
- **O hotlink de afiliado** (`https://go.hotmart.com/V106592210H`),
  revalidado como a mesma URL documentada em
  `src/lib/presell/affiliateLink.ts` do PR #51 e no corpo do próprio
  PR. Nenhum parâmetro foi anexado (mesma decisão do PR #51: não há
  evidência de que a Hotmart repasse UTM/query string arbitrários).
- **Os atributos de segurança dos CTAs externos**:
  `target="_blank" rel="noopener noreferrer sponsored"`.
- **A ausência de FAQ** — o Figma aprovado não tem essa seção; não foi
  inventada uma.
- **O ajuste mobile aprovado** documentado no PR #51 (mais espaço
  vertical entre o rótulo do preset e a legenda, só na faixa mobile).

## O que precisou ser adaptado

- **Arquitetura**: de Next.js 15 / React 19 / TypeScript / CSS Modules
  (`apps/web` do AML) para HTML + CSS estático, sem build e sem
  JavaScript, seguindo o padrão já usado em
  `aprovacao/100-aplicativos-uteis/` deste repositório (ver
  `docs/ADR_PRESELL_OWNERSHIP.md`, regra 8). Os componentes React
  (`Hero`, `ProblemSection`, `PresetShowcase`+`PresetCard`,
  `IncludedItems`, `Audience`, `HowItWorks`, `Transparency`,
  `FinalCta`) viraram seções `<section>` no único `index.html`; o
  `AffiliateCtaButton` virou um `<a>` estático (sem `onClick`
  de tracking — ver seção "Tracking" abaixo).
- **CSS Modules → CSS global com classes** em
  `aprovacao/fotografia-presets-lightroom/styles.css`, preservando os
  mesmos breakpoints (`900px`, `640px`), espaçamentos e hierarquia
  tipográfica dos arquivos `.module.css` originais.
- **Caminho da rota**: de `/presell/fotografia-presets-lightroom`
  (Next.js) para `/aprovacao/fotografia-presets-lightroom/` (GitHub
  Pages, área de revisão interna — ver `aprovacao/README.md`).
  `robots: noindex,nofollow` preservado (era `metadata.robots` no
  PR #51, agora é a tag `<meta name="robots">`).
- **Tokens de cor do Figma — gap herdado, não resolvido**: o PR #51
  importava `@/styles/presell/tokens.module.css` no `page.tsx`, mas
  esse arquivo **nunca foi commitado** em nenhum commit da branch
  (confirmado com `git log --all -- '*tokens.module.css'` no clone
  local do PR — nenhum resultado). Ou seja, o próprio PR #51 já tinha
  esse gap, não documentado explicitamente nele. Tentei reconsultar o
  Figma diretamente nesta migração (`get_variable_defs` via Figma MCP)
  para obter os valores exatos, mas o **limite de chamadas do plano
  Starter já estava esgotado** (mesma limitação que o PR #51 registrou
  para screenshots). Os únicos 4 valores literais que existem por
  escrito são os citados na seção "Limitações conhecidas" do PR #51:
  `#e0deeb` / `#e5e3f0` (texto em painel escuro) e `#edebf5` /
  `#f0edf7` (marcadores em painel escuro) — usei o primeiro de cada
  par (`--presell-dark-muted: #e0deeb`, `--presell-dark-bullet:
  #edebf5`). Os demais tokens (`--presell-ink`, `--presell-muted`,
  `--presell-accent`, `--presell-dark-bg`, `--presell-soft-pink`,
  raios de borda, largura máxima) são uma **estimativa razoável de
  contraste e hierarquia**, não uma leitura literal do Figma — ver
  comentário no topo de `styles.css`. Isso mantém a página
  `CANDIDATA_APROVADA_TECNICAMENTE`: a estrutura, copy e comportamento
  estão corretos; a fidelidade cromática exata ao Figma ainda não foi
  confirmada.

## Hashes dos assets (origem → destino)

Origem: `afiliados-mega-lab`, branch
`feature/claude/presell-fotografia-presets-figma`,
`apps/web/public/presell/fotografia-presets-lightroom/`.

Destino: `aprovacao/fotografia-presets-lightroom/assets/`.

| Arquivo | SHA-256 origem | SHA-256 destino | Idêntico? |
|---|---|---|---|
| `mockup-hero-04.jpg` | `c7a9846ac119ac9409957e3a6765830e1b593b48e021f653156531542c280517` | `c7a9846ac119ac9409957e3a6765830e1b593b48e021f653156531542c280517` | Sim |
| `mockup-conteudo-03.jpg` | `113727ca33c6ce0690fd4fbb5ae7cd12939aa2ec07fdf3d9f25cf3c9ce5e6e30` | `113727ca33c6ce0690fd4fbb5ae7cd12939aa2ec07fdf3d9f25cf3c9ce5e6e30` | Sim |
| `preset-quente.jpg` | `9b9bfde5cb1cd0f2ffd6c279bd449e84300be4aa599a5fe62e02f0856b856ed8` | `9b9bfde5cb1cd0f2ffd6c279bd449e84300be4aa599a5fe62e02f0856b856ed8` | Sim |
| `preset-mistico.jpg` | `2ef43295338ce1ad8322f8db6094e6de68818dd2082391ba6bee757759fee0bf` | `2ef43295338ce1ad8322f8db6094e6de68818dd2082391ba6bee757759fee0bf` | Sim |
| `preset-cinematografico.jpg` | `7c1b88c1ed5f82ac31d9199ded8581d01eb588fca5b550f289a1f28f060b8738` | `7c1b88c1ed5f82ac31d9199ded8581d01eb588fca5b550f289a1f28f060b8738` | Sim |

Nenhuma transformação foi aplicada — cópia byte a byte
(`cp` a partir de um clone local do PR #51).

## Tracking (Nível 0 — não concluído)

O PR #51 tinha um endpoint de tracking **opcional e no-op**
(`NEXT_PUBLIC_PRESELL_ANALYTICS_ENDPOINT`, sem configurar = evento
descartado silenciosamente, nunca bloqueia a página). Isso **não é**
tracking comprovado — é só código preparado para um endpoint que nunca
existiu de fato.

Nesta migração para HTML estático, **nenhum código de tracking foi
incluído** (nem no-op): a página não tem `<script>`, seguindo o mesmo
padrão de `aprovacao/100-aplicativos-uteis/` (zero JavaScript). Se
medição for necessária no futuro, ela deve ser adicionada só depois de
uma decisão consciente sobre LGPD/cookies e da atualização da Política
de Privacidade da página — mesma regra já documentada no `README.md`
raiz para a outra pre-sell.

**Nível 0 de tracking permanece não concluído** (nem no-op, nem real).

## Validações executadas

Servidor estático local (`python -m http.server 8080` via
`preview_start`), Browser pane deste ambiente.

- [x] `GET /aprovacao/fotografia-presets-lightroom/` → título da aba
      bate com a headline aprovada.
- [x] 0 erros no console do navegador.
- [x] 5 assets oficiais servidos via `fetch()` direto, `200`,
      `image/jpeg`, tamanho em bytes idêntico ao arquivo original
      (`136973`, `164721`, `1559644`, `2834618`, `1860823`).
- [x] 2 CTAs inspecionados (nunca clicados) — mesmo `href`
      (`https://go.hotmart.com/V106592210H`), `target="_blank"`,
      `rel="noopener noreferrer sponsored"`.
- [x] Sem overflow horizontal em 375px (mobile), 768px (tablet,
      753px de viewport nativo do Browser pane) e 1440px (desktop,
      1425px de viewport nativo do Browser pane) —
      `scrollWidth === clientWidth` nas três larguras.
- [x] `<meta name="robots" content="noindex,nofollow">` presente.
- [x] Todas as imagens (`6/6`) têm `alt` descritivo.
- [x] Nenhuma seção de FAQ presente (o Figma aprovado não tem FAQ).
- [x] Nenhum claim proibido/inventado — a única ocorrência da palavra
      "garantia" no texto da página é uma negação de garantia
      ("Nenhum conteúdo desta página deve ser interpretado como
      garantia de resultado"), não uma promessa comercial fabricada.
      Sem preço, comissão, urgência, escassez ou depoimento em nenhum
      lugar da página.
- [x] Copy comparada linha a linha contra
      `apps/web/src/lib/presell/content.ts` do PR #51 (fonte).

**Limitação registrada (herdada do mesmo ambiente que o PR #51
enfrentou):** o Browser pane não permitiu compositar frames para
screenshot em pixel nesta sessão
(`screenshot failed: the Browser pane is not displayed`). A validação
visual usou inspeção de DOM/CSS computado + ausência de overflow
horizontal via JavaScript, não comparação pixel a pixel com o Figma.

## Diferenças em relação ao Figma / ao PR #51

- Tokens de cor exatos do Figma não confirmados (ver seção "O que
  precisou ser adaptado" acima) — maior divergência conhecida desta
  migração.
- Sem breakpoint intermediário explícito no Figma (só 1440/390),
  mesma limitação já documentada pelo PR #51 — a faixa ~768–899px usa
  o layout mobile empilhado até 899px.
- Sem FAQ (mesmo do PR #51 — não existe no Figma aprovado).
- Sem código de tracking, nem mesmo no-op (diferença deliberada desta
  migração: zero JavaScript, mesmo padrão de `100-aplicativos-uteis`).

## Limitações e pendências

- Tokens de cor exatos do Figma pendentes de confirmação (requer novo
  acesso ao Figma MCP, fora do plano Starter já esgotado, ou acesso
  manual ao arquivo).
- Nenhuma validação real de fluxo externo (clique real no hotlink) foi
  feita — permanece `CANDIDATA_APROVADA_TECNICAMENTE`.
- Nenhum screenshot pixel a pixel foi gerado (limitação do Browser
  pane nesta sessão).
- `robots: noindex,nofollow` aplicado — reversível quando a
  publicação em `/produtos/` for decidida (não depende de aprovação de
  produtora por padrão — ver `docs/ADR_PRESELL_OWNERSHIP.md`).

## Estado final do PR #51 (AML)

Não mesclado. Após a abertura do PR correspondente neste repositório
(Trevo), o PR #51 deve ser atualizado com um comentário registrando o
link do novo PR e que a implementação foi *superseded*
arquiteturalmente por esta migração — preservado como fonte histórica,
sem merge no AML.

## Confirmações

- Nenhuma compra, checkout, campanha, gasto ou clique real no hotlink
  em nenhum momento desta migração.
- Nenhum envio desta página para a produtora — permanece em
  `/aprovacao/` como revisão/QA interna, o que não implica envio
  externo (ver `docs/ADR_PRESELL_OWNERSHIP.md`).
- Nenhuma alteração de DNS/produção.
- Nenhuma promessa/preço/garantia/escassez/depoimento/contador/
  autoridade inventados.
- PR deste repositório aberto como **draft**, não mesclado.
