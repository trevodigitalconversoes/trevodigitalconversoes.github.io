# Etapa 3D — Correções da Rodada 1 de Visual QA (campanha Lightroom)

- **Status:** `TREVO_VISUAL_QA_ROUND1_FIXES_READY`. QA técnico completo
  nas 6 páginas em escopo; aprovação visual humana e segunda rodada
  formal do `visual-qa-capture` ainda pendentes.
- **Pacote revisado:** `trevo-digital-conversoes_20260807_210001_visual_qa.zip`
  (primeira captura completa: 7 páginas/experiências, desktop/tablet/
  mobile, 42 screenshots principais + segmentos + manifestos).

## Mudança de escopo após a primeira captura

A primeira captura cobriu as 7 páginas do inventário
(`docs/etapa_3_c_v1_remocao_aprovacao_promocao_100_apps.md`). Após a
captura, a revisão e correção visual de `/produtos/100-aplicativos-uteis/`
foi **adiada** para depois do lançamento da primeira campanha
(Fotografia + Presets):

```
100_APPS_VISUAL_REVIEW_DEFERRED_UNTIL_AFTER_LIGHTROOM_LAUNCH
```

A página continua no site, na home e no catálogo — apenas não foi
revisada, criticada, aprovada ou reprovada nesta rodada, e nenhum
arquivo específico dela foi tocado (confirmado por `git status`: só
`404.html`, `produtos/index.html` e `styles.css` mudaram nesta etapa).

Escopo real desta rodada de correção — 6 experiências:

1. `/` (home)
2. `/produtos/` (catálogo)
3. `/produtos/fotografia-presets-lightroom/`
4. `/politica-de-privacidade.html`
5. `/termos-de-uso.html`
6. `404.html` (via rota inexistente)

## Achado 1 — 404 sem identidade visual (bloqueador)

### Causa raiz

`404.html` referenciava seu CSS, favicon e link de retorno com
caminhos **relativos** (`styles.css`, `assets/logo-social.png`,
`index.html`). O GitHub Pages serve `404.html` para qualquer rota
inexistente, preservando a URL solicitada na barra de endereço — o
navegador resolve caminhos relativos contra essa URL, não contra a
localização real do arquivo. Em uma rota como
`/a/b/c/rota-inexistente/`, `styles.css` relativo resolvia para
`/a/b/c/rota-inexistente/styles.css`, que não existe → `404` para o
CSS → HTML cru, sem identidade visual.

Confirmado que o site é servido na raiz do domínio (`trevodigitalconversoes/trevodigitalconversoes.github.io`,
"URL raiz (produção): `https://trevodigitalconversoes.github.io/`",
sem prefixo de nome de repositório) — então paths **root-relative**
(`/styles.css`) são a solução correta e sempre resolvem para a raiz
real do site, independente da profundidade da rota solicitada.

### Correção aplicada

Em `404.html`:

```diff
- <link rel="icon" href="assets/logo-social.png">
+ <link rel="icon" href="/assets/logo-social.png">
- <link rel="stylesheet" href="styles.css">
+ <link rel="stylesheet" href="/styles.css">
...
- <a class="button primary" href="index.html">Voltar para o início</a>
+ <a class="button primary" href="/index.html">Voltar para o início</a>
```

Nenhuma mudança de conteúdo/copy — só os três caminhos.

### Estratégia de validação — servidor com fallback 404 real

O `python -m http.server` padrão (`SimpleHTTPRequestHandler`) não
replica o comportamento do GitHub Pages: uma rota inexistente retorna
a página de erro genérica do próprio servidor Python
(`Cannot GET ...`/`Error response`), não `404.html`. Testar contra
esse servidor não seria evidência válida — foi rejeitado
explicitamente nesta rodada.

Para o QA real, foi criado um servidor HTTP temporário
(`gh_pages_404_server.py`, fora do repositório, no diretório de
scratchpad da sessão — nunca commitado): um `SimpleHTTPRequestHandler`
customizado que, para qualquer rota sem arquivo/`index.html`
correspondente, responde com **status HTTP 404** e o **conteúdo real**
de `404.html`. Bindado só em `127.0.0.1`, porta `8091`, encerrado
(`taskkill`) ao final da sessão de QA.

### Resultado

| Rota testada | Documento principal | CSS | Console | Visual |
|---|---|---|---|---|
| `/__visual_qa_404_inexistente__/` | `404` (conteúdo = `404.html`) | `200` | só o 404 esperado do próprio documento | Identidade Trevo aplicada (fundo `rgb(6,17,15)`, botão com gradiente verde) |
| `/produtos/teste` | `404` | `200`/`304` | idem | idem |
| `/a/b/c/inexistente/` | `404` | `200` | idem | idem, sem overflow em 390px |

Nenhum `Cannot GET ...` foi usado como evidência em nenhum momento —
todas as validações usaram o servidor com fallback 404 customizado.
Link de retorno (`/index.html`) resolve corretamente em todas as
profundidades testadas. Nenhum failed request de stylesheet.

## Achado 2 — Espaço excessivo no catálogo (desktop)

### Causa raiz

A classe global `.section` (`styles.css`) aplica
`padding: clamp(56px, 8vw, 105px) ...` (topo **e** base) em qualquer
elemento com essa classe. Em `produtos/index.html`, a introdução do
catálogo (`eyebrow` + `h1` + `lead`) e o grid de produtos estavam em
**duas** seções `.section` consecutivas — a base da primeira (até
105px) somava com o topo da segunda (até 105px), abrindo um vão de até
~210px entre o parágrafo de introdução e o primeiro card, em desktop
1440×900 isso empurrava os cards para perto do fim do viewport.

Na home esse problema não existia porque a seção de produtos é
antecedida pelo hero (que já tem altura própria) e o grid está dentro
da **mesma** seção do título, não em uma seção separada.

### Correção aplicada

Em `produtos/index.html`, o `<div class="product-grid">` foi movido
para **dentro** da mesma `<section class="section">` da introdução
(eliminando a seção extra só para o grid) — mesmo padrão já usado na
home. O espaçamento entre o parágrafo `lead` e o grid passa a vir só
de `.product-grid { margin: 34px auto 0; }`, já existente, sem
nenhuma regra CSS nova.

```diff
  <section class="section">
    <p class="eyebrow">Catálogo</p>
    <h1>Produtos anunciados</h1>
    <p class="lead">...</p>
-  </section>
-
-  <section class="section">
    <div class="product-grid">
      ...
    </div>
  </section>
```

Nenhum offset mágico foi adicionado — a correção é estrutural (remover
a duplicação de padding), não um ajuste numérico arbitrário.

### Resultado

- **Desktop (1440×900 real, 1425px de viewport útil):** topo do grid
  agora em `y ≈ 415px` dentro de um viewport de `900px` — bem dentro
  do primeiro scroll, contra o comportamento anterior (cards só perto
  do fim do viewport). `h1` em `y ≈ 217px`.
- **Tablet (768px):** sem overflow, grid presente, layout preservado
  (a seção "notice" após o grid não foi alterada).
- **Mobile (390px):** sem overflow, 2 cards presentes, layout
  preservado.

## Achado 3 — Header sticky ocupando espaço em mobile

### Causa raiz

`.site-header` (`styles.css`) tem `position: sticky; top: 0;` sem
override em nenhum breakpoint. Em mobile (~390px), o header já vira
duas linhas (`flex-direction: column`, regra existente desde antes
desta rodada, breakpoint `@media (max-width: 800px)`) — combinado com
`sticky`, essa versão de duas linhas permanece fixa no topo durante
toda a rolagem, ocupando uma fração relevante da altura útil do
viewport em páginas longas (home, catálogo).

### Correção aplicada

Adicionada `position: static;` dentro do **mesmo** bloco
`@media (max-width: 800px)` que já existia e já modificava
`.site-header` (menor risco: reaproveita o breakpoint já usado pelo
design, não introduz um novo):

```diff
 @media (max-width: 800px) {
   .site-header {
+    position: static;
     align-items: flex-start;
     flex-direction: column;
   }
```

Nenhum JavaScript foi introduzido. Nenhum item de navegação foi
removido ou reestruturado — apenas o comportamento de fixação durante
o scroll.

### Escopo do impacto

Essa classe (`.site-header`) só existe em `index.html` (home) e
`produtos/index.html` (catálogo) — as pre-sells
(`fotografia-presets-lightroom/`, `100-aplicativos-uteis/`) têm sua
própria folha de estilos e sua própria barra superior
(`.top-bar`), sem `.site-header`, então não são afetadas por esta
mudança.

### Resultado

| Largura | `position` computado |
|---|---|
| 1440px (desktop) | `sticky` (preservado) |
| 768px (tablet) | `static` (agrupado com mobile no breakpoint existente de 800px, comportamento já era "duas linhas" antes desta correção) |
| 390px (mobile) | `static` (corrigido — não fica mais sobre o conteúdo durante o scroll) |

## Fotografia + Presets — regressão

Nenhuma alteração de arquivo nesta página nesta rodada. QA de
regressão executado (desktop/tablet/mobile): headline preservada
("Suas fotos podem ter muito mais estilo..."), 5/5 assets `200`, 2
CTAs com o mesmo `href`/`rel`/`target` de sempre
(`https://go.hotmart.com/V106592210H`,
`rel="noopener noreferrer sponsored"`, `target="_blank"`), sem
overflow em nenhuma largura testada. Nenhum clique no CTA. Copy
comercial confirmada intacta (não editada).

## Política de Privacidade e Termos de Uso

Nenhuma alteração de arquivo. Regressão básica: `200`, sem overflow em
1440px, sem erros de console.

## +100 Aplicativos Úteis

```
VISUAL_REVIEW_DEFERRED_UNTIL_AFTER_LIGHTROOM_LAUNCH
```

- Não revisada visualmente nesta rodada.
- Não alterada: `git status` confirma que nenhum arquivo em
  `produtos/100-aplicativos-uteis/` ou `docs/100-aplicativos-uteis/`
  aparece no diff desta etapa.
- Continua presente na home (seção "Produtos anunciados") e no
  catálogo `/produtos/`, sem alteração de posição, copy ou layout.

## QA (6 páginas em escopo)

| Página/experiência | Desktop 1440 | Tablet 768 | Mobile 390 | HTTP | Console | Overflow | Resultado |
|---|---|---|---|---|---|---|---|
| Home | OK, header sticky preservado | OK, header static | OK, header static | 200 | 0 erros próprios da página | Nenhum | Passou |
| Catálogo | OK, grid visível cedo (`y≈415px`/900px) | OK | OK | 200 | 0 erros próprios | Nenhum | Passou |
| Fotografia | OK, sem regressão | OK | OK | 200 | 0 erros | Nenhum | Passou |
| Privacidade | OK | — | — | 200 | 0 erros | Nenhum | Passou |
| Termos | OK | — | — | 200 | 0 erros | Nenhum | Passou |
| 404 (3 rotas testadas) | Visual Trevo aplicado | — | Sem overflow (390px) | 404 (documento) / 200 (CSS) | Só o 404 esperado do documento | Nenhum | Passou |

## Documentação

Este arquivo (`docs/etapa_3_d_v1_correcoes_visual_qa_rodada_1.md`)
registra achados, causas raiz, correções, validação e resultado da
Rodada 1. Nenhuma nota de desenvolvimento foi inserida em nenhuma
página pública.

## Segurança/comercial

- Nenhuma copy comercial reescrita (nem na pre-sell, nem nos cards, nem
  no 404).
- Nenhum clique em hotlink da Hotmart.
- Nenhum checkout, compra ou campanha ativada.
- Nenhum gasto.
- Nenhum contato com produtora.

## Próximo passo

Segunda execução formal do `visual-qa-capture` (sessão externa,
responsável pela ferramenta), cobrindo as 6 páginas desta rodada, para
nova revisão visual humana comparando com a primeira captura.
`/produtos/100-aplicativos-uteis/` permanece fora do escopo de revisão
visual até depois do lançamento da campanha Lightroom.

## Limitações

- QA desta rodada é técnico (DOM, CSS computado, network, console) —
  não substitui a segunda captura formal de screenshots nem a
  aprovação visual humana.
- O servidor de fallback 404 usado para validação é uma aproximação do
  comportamento do GitHub Pages (baseada no comportamento documentado:
  rota inexistente → status 404 + conteúdo de `404.html`) — o
  comportamento exato em produção só é confirmável após o merge e
  deploy reais.
