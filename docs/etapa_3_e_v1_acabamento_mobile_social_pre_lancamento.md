# Etapa 3E — Acabamento pré-lançamento: mobile, thumbnail +100 Apps, Instagram

- **Status:** `TREVO_PRELAUNCH_POLISH_READY`. Correções técnicas
  concluídas e validadas; publicação no Instagram e revisão visual
  completa de `/produtos/100-aplicativos-uteis/` permanecem como
  ações humanas/futuras, fora do escopo desta etapa.
- **Objetivo:** pequena rodada de acabamento descoberta após a Rodada
  2 do Visual QA, antes do lançamento da campanha "10 Dicas de
  Fotografia + 18 Presets de Lightroom".

## Achado 1 — e-mail quebra/estoura no mobile

### Causa

`trevodigitalconversoes@hotmail.com` é um token único, sem espaços.
Nenhuma regra CSS no site definia comportamento de quebra para texto
sem espaço — o comportamento padrão do navegador (`overflow-wrap:
normal`) não quebra uma palavra que não cabe no container, causando
overflow horizontal em telas estreitas (~320–375px). Afetava
`index.html` (seção Contato), `politica-de-privacidade.html` e
`termos-de-uso.html` — as três páginas que exibem esse e-mail, todas
usando `styles.css` (raiz).

### Correção — sistêmica, não pontual

Adicionada uma única regra global, no seletor `html` já existente em
`styles.css`:

```diff
 html {
   scroll-behavior: smooth;
+  overflow-wrap: anywhere;
 }
```

`overflow-wrap: anywhere` só age quando uma palavra realmente não cabe
— não afeta a quebra normal de texto com espaços, não reduz fonte, não
esconde conteúdo, sem `text-overflow: ellipsis`. Uma regra cobre as
três páginas afetadas (e qualquer texto longo futuro), em vez de três
correções pontuais.

### Resultado

Testado com `getBoundingClientRect()` em 320px: o link do e-mail
(`rect.right ≈ 271px`) fica dentro do container `.contact-box`
(`container.right ≈ 300px`) — sem overflow do elemento nem da página
(`scrollWidth === clientWidth` em todas as larguras testadas). Link
continua clicável (`mailto:`), texto continua completo e legível, sem
ellipsis.

## Novo piso responsivo — 320px

A partir desta etapa, **320px passa a ser a largura mínima obrigatória
de QA** deste site, além de 375/390/425px, com regressão em 768
(tablet) e 1440 (desktop). Registrado em `README.md`, `CLAUDE.md` e
`AGENTS.md` (regra 11).

## Auditoria de overflow — 6 páginas × 6 larguras

Servidor HTTP local customizado (o mesmo `gh_pages_404_server.py` da
etapa 3D — fallback 404 real, nunca `file://`), rodando em 2 portas
diferentes ao longo da sessão. Para cada largura, `document.
documentElement.scrollWidth <= clientWidth` foi verificado
programaticamente nas 6 páginas em escopo.

| Página | 320 | 375 | 390 | 425 | 768 | 1440 |
|---|---|---|---|---|---|---|
| Home | OK | OK | OK | OK | OK | OK |
| Catálogo | OK | OK | OK | OK | OK | OK |
| Fotografia + Presets | OK | OK | OK | OK | OK (regressão, sem alteração de arquivo) | OK |
| Política de Privacidade | OK | OK | OK | OK | — | OK |
| Termos de Uso | OK | OK | OK | OK | — | OK |
| 404 (rota inexistente por largura) | OK | OK | OK | OK | — | — |

Nenhum overflow em nenhuma combinação. Nenhum erro de console real
(os únicos erros observados são o próprio `404` esperado do documento
principal, ao navegar para as rotas de teste). `/produtos/fotografia-
presets-lightroom/` **não foi alterada** nesta etapa — nenhuma copy,
headline, hero, imagem, CTA ou disclosure foi tocada; QA aqui é
regressão pura.

## Achado 2 — thumbnail de +100 Apps

### Situação anterior

O card de "+100 Aplicativos Úteis" na home e no catálogo usava
`produtos/100-aplicativos-uteis/og-image.svg` — um banner 1200×630
desenhado para preview de compartilhamento social (Open Graph), com
texto secundário pequeno (`font-size: 24–30`) que perde legibilidade
quando o mesmo SVG é escalado para o tamanho de um card (~280–400px de
largura no grid).

### Inventário de material existente

Investigados: `produtos/100-aplicativos-uteis/favicon.svg` (ícone,
não serve como thumbnail), `produtos/100-aplicativos-uteis/og-image.svg`
(avaliado acima, texto pequeno demais), `assets/banner-square.png` e
`assets/banner-wide.png` (banners **institucionais da marca Trevo**,
com o slogan "O ponto de encontro entre o produto e o comprador" —
não identificam o produto "+100 Aplicativos Úteis" especificamente,
então não servem como thumbnail de card de catálogo). Nenhum material
oficial do produtor específico para "+100 Aplicativos Úteis" existe
neste repositório além do próprio `og-image.svg`.

### Asset criado

`assets/produtos/100-aplicativos-uteis-thumb.svg` — novo, exclusivo
para navegação/catalogação (não é criativo comercial). Reaproveita a
mesma paleta de cores e gradiente do `og-image.svg` já existente
(identidade já associada a esse produto), em proporção 800×500 (16:10,
igual ao `aspect-ratio` do CSS `.product-card-image`), com **menos
texto e fontes maiores** (`+100` em 88px, "Aplicativos Úteis" em 56px,
subtítulo único em 32px — contra 72/56/30/24px espalhados em 4 linhas
no original). Nenhuma promessa, benefício, desconto, urgência,
depoimento, avaliação, garantia, bônus ou resultado foi adicionado —
só o título do produto e um subtítulo já usado no material original
("para a rotina empreendedora").

### Arquivos alterados

- `index.html` — `src` do card trocado de
  `produtos/100-aplicativos-uteis/og-image.svg` para
  `assets/produtos/100-aplicativos-uteis-thumb.svg`.
- `produtos/index.html` — mesma troca (caminho relativo
  `../assets/produtos/...`).
- **Nenhum arquivo dentro de `produtos/100-aplicativos-uteis/` ou
  `docs/100-aplicativos-uteis/` foi alterado** — confirmado por
  `git status` ao final da etapa (zero diff nessas pastas).

### Resultado

Thumbnail carrega `200` em ambos os contextos (home e catálogo,
confirmado via `fetch()`), aspect-ratio do card preservado, sem
overflow em nenhuma largura testada.

## +100 Aplicativos Úteis — revisão visual continua adiada

```
VISUAL_REVIEW_DEFERRED_UNTIL_AFTER_LIGHTROOM_LAUNCH
```

A página individual não foi revisada visualmente nem redesenhada
nesta etapa — apenas referenciada (via `src`) por um asset novo que
vive fora de sua pasta. Ela continua presente na home e no catálogo.

## Achado 3 — Instagram com presença mínima

### Estado atual

Perfil: `https://www.instagram.com/trevodigitalconversoes/` (único
link para Instagram encontrado em todo o repositório — em
`index.html`, seção Contato — confirmado correto, nenhuma alteração
necessária). O perfil tem identidade/logo e link para o site, mas
praticamente nenhum conteúdo publicado (post 1, já existente,
corresponde ao slogan institucional "O ponto de encontro entre o
produto e o comprador" — mesmo texto do `assets/banner-square.png`
já presente no repositório).

### Onde os assets de marca/social ficam

`assets/social/` (nova pasta) — assets institucionais da marca para
redes sociais, deliberadamente fora de `produtos/fotografia-presets-
lightroom/` e `produtos/100-aplicativos-uteis/` (que são pastas de
produto, não de marca). Documentado em `README.md`.

### Post 2 — institucional

**Asset:** `assets/social/post-02-institucional.png`, `1080×1350`
(proporção 4:5, padrão de feed do Instagram). Gerado localmente com
Pillow (Python), reaproveitando: a logo oficial (`assets/logo.png`),
a paleta de cores institucional já usada no site (`--bg: #06110f`,
`--bg-2: #0b2f27`, `--green: #50d06a`), o eyebrow verbatim do hero
("Marketing digital • Afiliados • Curadoria") e uma versão reduzida
(por espaço, não por invenção) do primeiro parágrafo da seção "Sobre
a marca" da home.

**Legenda proposta** (texto integralmente reaproveitado de
`index.html`, seção `#sobre`, sem nenhuma frase nova):

> A Trevo Digital Conversões atua na análise, seleção e divulgação de
> produtos digitais de terceiros. O objetivo é apresentar soluções
> úteis para públicos específicos, sempre com comunicação clara e sem
> promessas irreais.
>
> A Trevo Digital Conversões pode participar de programas de
> afiliados. Isso significa que, ao clicar em alguns links ou
> anúncios e realizar uma compra, podemos receber uma comissão.
>
> trevodigitalconversoes.github.io

**Alt text proposto:** "Banner institucional da Trevo Digital
Conversões, fundo verde escuro com a logo da marca, o texto Marketing
digital, Afiliados, Curadoria e o nome Trevo Digital Conversões."

### Post 3 — produto Lightroom (dependência registrada, não criado)

Não foi criada uma nova copy comercial para Instagram nesta etapa —
conforme instrução explícita. O Post 3 deve derivar de **um dos
criativos estáticos oficiais da campanha Lightroom**, que ainda será
finalizado em um bloco de criativos separado (fora do escopo deste
repositório/etapa). Especificação registrada para quando esse bloco
existir:

- Formato: `1080×1350` (4:5), consistente com o Post 2.
- Fonte de copy: o mesmo `content.ts`/copy aprovada já usada em
  `produtos/fotografia-presets-lightroom/` — headline e/ou um dos
  pares antes/depois dos presets, sem nenhuma persuasão nova.
- Nenhum placeholder visível foi criado para este post (nem asset,
  nem legenda) — apenas esta nota de dependência, conforme instrução
  explícita de não criar placeholder de publicação.

### Confirmações

Nenhum login no Instagram, nenhuma publicação, nenhum agendamento,
nenhuma DM, nenhum novo "seguir", nenhuma compra de mídia, nenhuma API
paga foi usada ou acionada nesta etapa. A publicação dos posts é uma
ação humana futura (ou automação explicitamente autorizada depois).

## Performance local

Medido via `performance.getEntriesByType('navigation'/'resource')` no
Browser pane, servidor HTTP local (não é medição de produção/HTTPS):

| Página | DOMContentLoaded | load | requests (no momento da medição) | recursos > limiar |
|---|---|---|---|---|
| Home | 160 ms | 233 ms | 4 | nenhum |
| Catálogo | 59 ms | 60 ms | 2 (imagens lazy ainda não carregadas no momento da medição) | nenhum |
| Fotografia + Presets | 74 ms | 91 ms | 2 (idem) | nenhum |

Nenhuma reprodução local do achado anterior de "~26s" — nenhum tempo
de carregamento anômalo foi observado em nenhuma das 3 páginas
medidas. Interpretação: provável ruído de DevTools/rede/sessão da
inspeção manual anterior, não um problema real do site neste momento.
**Observação registrada, não correção:** os 3 presets de imagem em
`produtos/fotografia-presets-lightroom/assets/` são grandes para web
(`preset-mistico.jpg` ≈ 2,8 MB, `preset-cinematografico.jpg` ≈ 1,86 MB,
`preset-quente.jpg` ≈ 1,56 MB — hashes/tamanhos já confirmados em
`docs/etapa_3_a_v1_migracao_presell_trevo.md`); nenhuma otimização foi
feita nesta etapa por não haver evidência de que isso seja hoje um
problema real (todas as medições locais deram rápidas), e essa página
está fora do escopo de alteração desta rodada. Medição oficial de
performance continuará sendo feita após o deploy em HTTPS real.

## 404 — regressão + novo piso 320px

Mesma estratégia de validação da etapa 3D (servidor local com fallback
404 real — `Cannot GET ...` nunca usado como evidência). Testado em
320/375/390/425px com rotas inexistentes distintas por largura:
documento principal sempre `404`, conteúdo sempre o `404.html` real do
Trevo, CSS sempre `200`, sem overflow em nenhuma largura.

## Documentação

- Este arquivo (`docs/etapa_3_e_v1_acabamento_mobile_social_pre_lancamento.md`).
- `README.md` — nova seção "QA mínimo — piso de 320px", documentação
  de `assets/produtos/` e `assets/social/`.
- `CLAUDE.md` / `AGENTS.md` — regras 10 (legibilidade de thumbnail,
  atualizada) e 11 (nova: piso de 320px).

## Segurança/comercial

- Nenhuma copy comercial reescrita (a copy do Post 2 é 100%
  reaproveitada de texto institucional já publicado no site; nenhuma
  copy nova foi escrita para o Post 3, que não foi criado).
- Nenhum clique em hotlink da Hotmart.
- Nenhum checkout, compra ou campanha ativada.
- Nenhum gasto.
- Nenhum contato com produtora.
- Nenhuma publicação no Instagram, nenhum login, nenhuma credencial
  manipulada.

## Próximo passo

Validação com `visual-qa-capture` incluindo 320px (ferramenta em
desenvolvimento em outra sessão, não modificada aqui). Depois,
retomar o plano de Tracking Mínimo do Nível 0
(`docs/etapa_3_b_v1_plano_tracking_nivel_0.md`).
