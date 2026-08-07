# Trevo Digital Conversões — site oficial (GitHub Pages)

Repositório oficial do site institucional Trevo Digital Conversões e
das landing pages de pré-venda/análise de afiliado hospedadas junto a
ele, tudo servido pelo GitHub Pages da organização.

- **Organização GitHub:** `trevodigitalconversoes`
- **Repositório:** `trevodigitalconversoes.github.io`
- **Remote:** `https://github.com/trevodigitalconversoes/trevodigitalconversoes.github.io.git`
- **URL raiz (produção):** `https://trevodigitalconversoes.github.io/`

> Repositório **público**. Nenhum arquivo `.env` real, token, senha, chave
> de API, cookie, sessão, credencial ou dado sensível deve ser commitado —
> ver `.gitignore`. Links de afiliado usados publicamente nas páginas
> podem aparecer no HTML quando fizerem parte da página publicada.

## Estrutura

```
index.html, styles.css, assets/          # site institucional (estático, sem build)
404.html, robots.txt
politica-de-privacidade.html, termos-de-uso.html
docs/                                     # documentação/relatórios do repositório
produtos/                                 # ÚNICO namespace público de pre-sells/produtos
  index.html                              # catálogo: grid de produtos anunciados
  fotografia-presets-lightroom/           # migrada de afiliados-mega-lab PR #51
    index.html, styles.css, assets/       # HTML+CSS estático, sem build, zero JavaScript
  100-aplicativos-uteis/                  # migrada de /aprovacao/ (removido) em 2026-08-07
    index.html, styles.css, fonts/        # HTML+CSS estático, sem build, zero JavaScript
    favicon.svg, og-image.svg
```

## Regra de publicação — páginas nascem como produção

Novas pre-sells/landing pages são implementadas **diretamente como
artefatos de produção**, em `/produtos/<slug>/`, com metadata real
(`index,follow`, canonical final) desde o primeiro commit. O estado de
desenvolvimento (rascunho, QA, revisão, "aguardando aprovação")
pertence a **git/branches/PRs**, nunca ao HTML servido ao visitante.
Uma página pública não deve conter rascunho, placeholder, nota de QA
interno, TODO/FIXME, referência a `docs/` internos, ou qualquer outro
sinal de estado de desenvolvimento. Ver `docs/ADR_PRESELL_OWNERSHIP.md`
para a regra completa.

**Não existe mais uma área pública separada de revisão/aprovação**
(`/aprovacao/` foi removido em 2026-08-07 — ver
`docs/etapa_3_c_v1_remocao_aprovacao_promocao_100_apps.md`). Revisão
técnica acontece inteiramente em
`branch → PR → ambiente local → QA → revisão humana → merge`.

## Site institucional (raiz)

`index.html`, `styles.css` e `assets/` são um site estático simples
(sem framework, sem build), com todos os caminhos relativos — funciona
como site raiz da organização sem qualquer configuração extra de base
path. Inclui uma seção "Produtos anunciados" com um card institucional
por produto de produção existente (imagem, título e descrição
factual/reaproveitada da copy já aprovada, nunca o hotlink diretamente
no card) e um link para o catálogo completo em `/produtos/`.

## `/produtos/` — catálogo público + pre-sells de produção (único fluxo)

`/produtos/index.html` é o **catálogo público**: página própria, com a
identidade visual do site (header/nav/footer consistentes), grid de
cards (mesmo padrão da seção "Produtos anunciados" da home) e link
para cada produto — **nunca** listagem de diretório do servidor.

Pre-sells novas são criadas diretamente em `/produtos/<slug>/`, com
`robots: index,follow`, canonical final e hotlink de afiliado real
desde o primeiro commit. Todo produto de produção deve aparecer tanto
no catálogo quanto na seção "Produtos anunciados" da home.

**Presença no catálogo não implica campanha paga ativa** — são
decisões independentes (ver `docs/ADR_PRESELL_OWNERSHIP.md`, seção
"`/produtos/` é o catálogo público").

## Páginas atuais

| Caminho | Produto | Status |
|---|---|---|
| `/produtos/` | Catálogo público (sem produto próprio) | Lista os produtos de produção existentes |
| `/produtos/fotografia-presets-lightroom/` | "10 Dicas de Fotografia + 18 Presets de Lightroom" (Hotmart) | Página de produção — migrada do PR #51 de `afiliados-mega-lab` (ver `docs/etapa_3_a_v1_migracao_presell_trevo.md`); hotlink de afiliado configurado; `index,follow`; listada na home e no catálogo; sem merge do PR #1 ainda (revisão humana pendente) |
| `/produtos/100-aplicativos-uteis/` | "+100 Aplicativos Úteis para Produtividade Empreendedora" (Hotmart) | Página de produção — promovida de `/aprovacao/` (removido) em 2026-08-07; fatos comerciais revalidados na Hotmart (07/08/2026); hotlink de afiliado configurado; `index,follow`; listada na home e no catálogo; sem merge do PR #1 ainda (revisão humana pendente) |

### `/produtos/100-aplicativos-uteis/` — HTML+CSS estático, zero JavaScript

Reconstruída em rodada anterior a partir de uma versão em Vite+React
que dependia de JavaScript para exibir qualquer conteúdo (violava o
requisito de a página funcionar sem JS). É um único `index.html` +
`styles.css`, sem build, **sem nenhuma tag `<script>`** — FAQ e conteúdo
legal (Política de Privacidade/Termos/Contato) usam `<details>`/
`<summary>` nativos do HTML. Ver
`docs/100-aplicativos-uteis/decisao_migracao_html_estatico.md`
para o histórico completo dessa troca,
`docs/auditoria_100_aplicativos_uteis.md` para a auditoria de
pré-publicação, e `docs/etapa_3_c_v1_remocao_aprovacao_promocao_100_apps.md`
para a promoção a `/produtos/`.

**CTA "Ver produto na Hotmart" — hotlink de afiliado configurado:** os
dois botões de CTA usam o link otimizado para Google Ads, derivado do
hotlink de afiliado confirmado na área de Hotlinks da Hotmart, e
preservam o rastreamento de afiliado (`target="_blank"`,
`rel="noopener noreferrer sponsored"`). Ver
`docs/100-aplicativos-uteis/compliance.md` para o link completo e os
testes recomendados antes de qualquer campanha paga.

**Por que não há analytics/tags nesta fase:** a página não deve gerar
dados de terceiros (Analytics/GTM/Pixel/Hotjar/Clarity) antes de
existir uma decisão consciente sobre LGPD/cookies e uma atualização da
Política de Privacidade desta página descrevendo exatamente o que
seria coletado (a página não usa cookies hoje).

## Como fazer deploy (GitHub Pages)

1. `Settings` → `Pages` → `Deploy from a branch`, branch `main`, pasta
   `/ (root)`. Isso já publica tudo neste repositório na raiz de
   `https://trevodigitalconversoes.github.io/` — sem nome de
   repositório na URL.
2. As páginas em `/produtos/` são HTML/CSS estático — para
   "rebuildar", basta editar `index.html`/`styles.css` diretamente e
   commitar. Não há passo de build/compilação nesta fase.

Este projeto/documentação **não faz commit nem push automaticamente** —
isso fica a cargo de quem revisar as mudanças localmente.

## Documentação

- `docs/ADR_PRESELL_OWNERSHIP.md` — decisão arquitetural: este
  repositório é o proprietário das pre-sells públicas, papel do
  repositório `afiliados-mega-lab`, GitHub Pages como hospedagem
  atual, `/produtos/` como único namespace público, e a regra sobre
  quando contato com produtora é (ou não) necessário. **Leia antes de
  implementar qualquer pre-sell/landing.**
- `CLAUDE.md` / `AGENTS.md` — resumo das regras acima para agentes de
  código, apontando para o ADR.
- `docs/auditoria_100_aplicativos_uteis.md` — auditoria de
  pré-publicação da landing "+100 Aplicativos Úteis" (clareza, conversão,
  confiança, compliance, SEO, acessibilidade, performance,
  compatibilidade, publicação, risco de aprovação) — relatório
  histórico, anterior à promoção para `/produtos/`.
- `docs/etapa_3_a_v1_migracao_presell_trevo.md` — migração da pre-sell
  "10 Dicas de Fotografia + 18 Presets de Lightroom" do PR #51 de
  `afiliados-mega-lab` para este repositório.
- `docs/etapa_3_b_v1_plano_tracking_nivel_0.md` — investigação e plano
  (sem implementação) de tracking mínimo para as pre-sells de
  produção.
- `docs/etapa_3_c_v1_remocao_aprovacao_promocao_100_apps.md` — remoção
  completa de `/aprovacao/` e promoção de "+100 Aplicativos Úteis"
  para `/produtos/`.
- `docs/100-aplicativos-uteis/` — documentação técnica da landing
  "+100 Aplicativos Úteis" (arquitetura estática, compliance, decisão
  de usar HTML+CSS estático sem JavaScript).
