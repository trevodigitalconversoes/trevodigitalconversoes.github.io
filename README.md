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
aprovacao/                                # páginas em revisão (ver aprovacao/README.md)
  index.html                              # mensagem genérica — NÃO lista páginas
  100-aplicativos-uteis/                  # uma página específica em revisão
    index.html, styles.css, fonts/        # HTML+CSS estático, sem build, zero JavaScript
    favicon.svg, og-image.svg
    docs/                                 # compliance e decisão de arquitetura da página
produtos/                                 # (ainda não existe) páginas já aprovadas/públicas
```

## Site institucional (raiz)

`index.html`, `styles.css` e `assets/` são um site estático simples
(sem framework, sem build), com todos os caminhos relativos — funciona
como site raiz da organização sem qualquer configuração extra de base
path. Inclui uma seção "Produtos anunciados" que, por enquanto, informa
que nenhum produto está sendo anunciado publicamente, e uma orientação
discreta para produtoras que tenham recebido um link de revisão por
e-mail.

## `/aprovacao/` — páginas em revisão, sem listagem pública

`/aprovacao/index.html` mostra apenas uma mensagem genérica — **nunca**
liste produtos, produtoras ou slugs de páginas em revisão ali, na home
do site, ou em qualquer menu público. Cada página em revisão fica em
`/aprovacao/<slug-específico>/`, com `noindex,nofollow`, sem link
público, e é compartilhada apenas por e-mail com quem precisa aprovar.

**Importante:** isso não é autenticação real. O repositório é público e
GitHub Pages é hospedagem estática sem backend — qualquer pessoa com a
URL exata acessa a página. A proteção é apenas contra indexação por
buscadores e descoberta casual. Ver `aprovacao/README.md` para o
detalhamento completo dessa ressalva.

## `/produtos/` — páginas aprovadas e públicas (futuro)

Depois que uma página em `/aprovacao/<slug>/` for aprovada pela
produtora/cliente, ela é movida para `/produtos/<slug-definitivo>/`,
com `robots` trocado para `index,follow`, hotlink de afiliado real
configurado, e pode passar a aparecer na seção "Produtos anunciados" da
home, se estiver em campanha ativa. Essa pasta ainda não existe neste
repositório.

## Páginas atuais

| Caminho | Produto | Status |
|---|---|---|
| `/aprovacao/100-aplicativos-uteis/` | "+100 Aplicativos Úteis para Produtividade Empreendedora" (Hotmart) | Rascunho — hotlink de afiliado já configurado; aguardando data de verificação e aprovação da produtora |

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
2. As páginas em `/aprovacao/` são HTML/CSS estático — para "rebuildar",
   basta editar `index.html`/`styles.css` diretamente e commitar. Não há
   passo de build/compilação nesta fase.

Este projeto/documentação **não faz commit nem push automaticamente** —
isso fica a cargo de quem revisar as mudanças localmente.

## Documentação

- `docs/auditoria_100_aplicativos_uteis.md` — auditoria de
  pré-publicação da landing "+100 Aplicativos Úteis" (clareza, conversão,
  confiança, compliance, SEO, acessibilidade, performance,
  compatibilidade, publicação, risco de aprovação).
- `aprovacao/README.md` — convenção da área de revisão (não é servido
  como página pública).
- `aprovacao/100-aplicativos-uteis/README.md` e `docs/` — documentação
  técnica da landing page (arquitetura estática, pendências, decisão de
  usar HTML+CSS estático sem JavaScript).
