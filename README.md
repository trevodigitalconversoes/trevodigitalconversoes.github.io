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
aprovacao/                                # caso histórico/excepcional (ver aprovacao/README.md) — não é mais o fluxo padrão
  index.html                              # mensagem genérica — NÃO lista páginas
  100-aplicativos-uteis/                  # página histórica ainda em revisão
    index.html, styles.css, fonts/        # HTML+CSS estático, sem build, zero JavaScript
    favicon.svg, og-image.svg
    docs/                                 # compliance e decisão de arquitetura da página
produtos/                                 # pre-sells de produção (fluxo padrão a partir desta etapa)
  fotografia-presets-lightroom/           # migrada de afiliados-mega-lab PR #51
    index.html, styles.css, assets/       # HTML+CSS estático, sem build, zero JavaScript
```

## Regra de publicação — páginas nascem como produção

A partir desta etapa, novas pre-sells/landing pages são implementadas
**diretamente como artefatos de produção**, em `/produtos/<slug>/`,
com metadata real (`index,follow`, canonical final) desde o primeiro
commit. O estado de desenvolvimento (rascunho, QA, revisão, "aguardando
aprovação") pertence a **git/branches/PRs**, nunca ao HTML servido ao
visitante. Uma página pública não deve conter rascunho, placeholder,
nota de QA interno, TODO/FIXME, referência a `docs/` internos, ou
qualquer outro sinal de estado de desenvolvimento. Ver
`docs/ADR_PRESELL_OWNERSHIP.md` para a regra completa e para a exceção
histórica (`/aprovacao/100-aplicativos-uteis/`, criada antes desta
regra existir).

## Site institucional (raiz)

`index.html`, `styles.css` e `assets/` são um site estático simples
(sem framework, sem build), com todos os caminhos relativos — funciona
como site raiz da organização sem qualquer configuração extra de base
path. Inclui uma seção "Produtos anunciados" que, por enquanto, informa
que nenhum produto está sendo anunciado publicamente, e uma orientação
discreta para produtoras que tenham recebido um link de revisão por
e-mail.

## `/aprovacao/` — caso histórico/excepcional, sem listagem pública

**Não é mais o fluxo padrão para novas pre-sells** (ver regra de
publicação acima). A pasta continua existindo para a página histórica
`100-aplicativos-uteis/`, criada antes desta regra.
`/aprovacao/index.html` mostra apenas uma mensagem genérica — **nunca**
liste produtos, produtoras ou slugs ali, na home do site, ou em
qualquer menu público. Cada página nessa pasta fica em
`/aprovacao/<slug-específico>/`, com `noindex,nofollow`, sem link
público, e é compartilhada apenas por e-mail com quem precisa revisar.

**Importante:** isso não é autenticação real. O repositório é público e
GitHub Pages é hospedagem estática sem backend — qualquer pessoa com a
URL exata acessa a página. A proteção é apenas contra indexação por
buscadores e descoberta casual. Ver `aprovacao/README.md` para o
detalhamento completo dessa ressalva.

## `/produtos/` — pre-sells de produção (fluxo padrão)

Pre-sells novas são criadas diretamente aqui, em
`/produtos/<slug>/`, com `robots: index,follow`, canonical final e
hotlink de afiliado real desde o primeiro commit. Podem passar a
aparecer na seção "Produtos anunciados" da home quando estiverem em
campanha ativa.

## Páginas atuais

| Caminho | Produto | Status |
|---|---|---|
| `/aprovacao/100-aplicativos-uteis/` | "+100 Aplicativos Úteis para Produtividade Empreendedora" (Hotmart) | Caso histórico, anterior à regra de publicação — hotlink de afiliado já configurado; aguardando data de verificação de preço/garantia |
| `/produtos/fotografia-presets-lightroom/` | "10 Dicas de Fotografia + 18 Presets de Lightroom" (Hotmart) | Página de produção — migrada do PR #51 de `afiliados-mega-lab` (ver `docs/etapa_3_a_v1_migracao_presell_trevo.md`); hotlink de afiliado configurado; `index,follow`; sem merge do PR #1 ainda (revisão humana pendente) |

### `/aprovacao/100-aplicativos-uteis/` — HTML+CSS estático, zero JavaScript

Reconstruída nesta rodada a partir de uma versão anterior em Vite+React
que dependia de JavaScript para exibir qualquer conteúdo (violava o
requisito de a página funcionar sem JS). Agora é um único `index.html` +
`styles.css`, sem build, **sem nenhuma tag `<script>`** — FAQ e conteúdo
legal (Política de Privacidade/Termos/Contato) usam `<details>`/
`<summary>` nativos do HTML. Ver
`aprovacao/100-aplicativos-uteis/docs/decisao_migracao_html_estatico.md`
para o histórico completo dessa troca, e
`docs/auditoria_100_aplicativos_uteis.md` para a auditoria de
pré-publicação.

**CTA "Ver produto na Hotmart" — hotlink de afiliado configurado:** os
dois botões de CTA usam o link otimizado para Google Ads, derivado do
hotlink de afiliado confirmado na área de Hotlinks da Hotmart, e
preservam o rastreamento de afiliado (`target="_blank"`,
`rel="noopener noreferrer sponsored"`). Ver
`aprovacao/100-aplicativos-uteis/docs/compliance.md` para o link
completo e os testes recomendados antes de qualquer campanha paga.

**Por que não há analytics/tags nesta fase:** a página está em rascunho,
sem aprovação da produtora, e não deve gerar dados de terceiros
(Analytics/GTM/Pixel/Hotjar/Clarity) antes de existir uma política de
privacidade que descreva esse tratamento e uma decisão consciente sobre
LGPD/cookies. **Quando adicionar futuramente:** só depois da aprovação da
produtora e da publicação em `/produtos/`, adicionar a ferramenta de
medição, atualizar a Política de Privacidade desta página (bloco
"Política de Privacidade" em `index.html`) descrevendo exatamente o que é
coletado, e avaliar se algum consentimento de cookies é necessário antes
de carregar o script (a página não usa cookies hoje).

## Como fazer deploy (GitHub Pages)

1. `Settings` → `Pages` → `Deploy from a branch`, branch `main`, pasta
   `/ (root)`. Isso já publica tudo neste repositório na raiz de
   `https://trevodigitalconversoes.github.io/` — sem nome de
   repositório na URL.
2. As páginas em `/aprovacao/` e `/produtos/` são HTML/CSS estático —
   para "rebuildar", basta editar `index.html`/`styles.css`
   diretamente e commitar. Não há passo de build/compilação nesta
   fase.

Este projeto/documentação **não faz commit nem push automaticamente** —
isso fica a cargo de quem revisar as mudanças localmente.

## Documentação

- `docs/ADR_PRESELL_OWNERSHIP.md` — decisão arquitetural: este
  repositório é o proprietário das pre-sells públicas, papel do
  repositório `afiliados-mega-lab`, GitHub Pages como hospedagem
  atual, e a regra sobre quando contato com produtora é (ou não)
  necessário. **Leia antes de implementar qualquer pre-sell/landing.**
- `CLAUDE.md` / `AGENTS.md` — resumo das regras acima para agentes de
  código, apontando para o ADR.
- `docs/auditoria_100_aplicativos_uteis.md` — auditoria de
  pré-publicação da landing "+100 Aplicativos Úteis" (clareza, conversão,
  confiança, compliance, SEO, acessibilidade, performance,
  compatibilidade, publicação, risco de aprovação).
- `docs/etapa_3_a_v1_migracao_presell_trevo.md` — migração da pre-sell
  "10 Dicas de Fotografia + 18 Presets de Lightroom" do PR #51 de
  `afiliados-mega-lab` para este repositório, incluindo a correção de
  caminho para `/produtos/`.
- `docs/etapa_3_b_v1_plano_tracking_nivel_0.md` — investigação e plano
  (sem implementação) de tracking mínimo para as pre-sells de
  produção.
- `aprovacao/README.md` — convenção da área de revisão (não é servido
  como página pública).
- `aprovacao/100-aplicativos-uteis/README.md` e `docs/` — documentação
  técnica da landing page (arquitetura estática, pendências, decisão de
  usar HTML+CSS estático sem JavaScript).
