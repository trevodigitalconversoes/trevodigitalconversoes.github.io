# Relatório — migração para o repositório da organização (v1)

## Contexto

O repositório `correa0inaiara/trevo-digital-conversoes` (usado nas
rodadas anteriores) está incorreto e será removido/deletado pelo
usuário. O repositório correto e definitivo é o da organização:

- **Organização:** `trevodigitalconversoes`
- **Repositório:** `trevodigitalconversoes.github.io`
- **Remote:** `https://github.com/trevodigitalconversoes/trevodigitalconversoes.github.io.git`
- **URL raiz:** `https://trevodigitalconversoes.github.io/`

Nesta rodada, a pasta local do repositório antigo
(`trevo-digital-conversoes/`) foi tratada como material de origem
("como se fosse o ZIP"), **sem clonar/extrair nada novo** — o próprio
usuário instruiu a considerar essa pasta como a origem e criar uma pasta
nova, separada, para o repositório correto.

## 1. Verificação de origem e diferenças

`git clone https://github.com/trevodigitalconversoes/trevodigitalconversoes.github.io.git`
foi executado com sucesso em uma pasta nova e irmã da antiga
(`trevodigitalconversoes.github.io/`, mesmo nível de
`trevo-digital-conversoes/`). O clone confirmou:

- O repositório da organização **já existe e está publicado**, com um
  commit anterior (`2ec28d7 — "Implantação site oficial da marca Trevo
  Digital Conversões"`).
- O site institucional (`index.html`, `styles.css`, `assets/`,
  `404.html`, `politica-de-privacidade.html`, `termos-de-uso.html`,
  `robots.txt`) é **byte-idêntico** ao do repositório antigo — nenhum
  conflito de conteúdo entre as duas versões.
- A única diferença encontrada foi o `.gitignore`: ambos os
  repositórios tinham o mesmo `.gitignore` quebrado, contendo apenas a
  linha `README.md` (sem barra inicial), o que faz o Git ignorar
  **qualquer** arquivo `README.md` em qualquer profundidade da árvore —
  por isso nenhum dos dois repositórios tinha um `README.md` versionado
  até agora. Corrigido nesta rodada (ver seção 6).

Não houve necessidade de "preservar a versão mais completa" entre as
duas, pois o conteúdo institucional já era idêntico. A diferença real
estava na estrutura de páginas de vendas (`paginas-de-vendas/aguardando-aprovacao/…`),
que existia **apenas** no repositório antigo e foi trazida/reorganizada
para o novo, conforme pedido.

### Referências antigas encontradas e removidas

| Referência antiga | Onde aparecia | Ação |
|---|---|---|
| `correa0inaiara` (conta/remote) | Apenas em `.git/config` do repo antigo — nunca apareceu em conteúdo (HTML/MD/TS) | Nada a remover no conteúdo; o repositório antigo em si será apagado pelo usuário |
| `trevo-digital-conversoes.github.io` | `codigo-fonte/README.md` (exemplos de `VITE_CONTACT_URL`, `VITE_SITE_URL`, `VITE_BASE_PATH`), `dist/index.html` gerado (canonical/OG/Twitter/assets) | Textos do README reescritos; HTML regerado com `VITE_SITE_URL`/`VITE_BASE_PATH` novos |
| `paginas-de-vendas/aguardando-aprovacao/100-aplicativos-uteis/` | READMEs e docs da landing page | Reescrito para `/aprovacao/100-aplicativos-uteis-cs-rascunho/` |

## 2. URL raiz do GitHub Pages

O site institucional (`index.html`, `styles.css`, `assets/`) já usava
**exclusivamente caminhos relativos** (`assets/logo.png`, `styles.css`,
âncoras internas) — nenhuma mudança foi necessária para ele funcionar
na raiz de `https://trevodigitalconversoes.github.io/`. Ele não é um
projeto Vite, então não há `VITE_SITE_URL`/`VITE_BASE_PATH` para essa
parte do site — essas variáveis existem apenas no projeto React da
landing page.

## 3. Reorganização das páginas de aprovação

Estrutura antiga (repositório errado):
```
paginas-de-vendas/aguardando-aprovacao/100-aplicativos-uteis/
```

Estrutura nova (repositório correto):
```
aprovacao/100-aplicativos-uteis-cs-rascunho/
```

Configuração da landing page nesta rodada:
```env
VITE_SITE_URL=https://trevodigitalconversoes.github.io/aprovacao/100-aplicativos-uteis-cs-rascunho
VITE_BASE_PATH=/aprovacao/100-aplicativos-uteis-cs-rascunho/
VITE_ROBOTS=noindex,nofollow
```

O build (`npm run build:staging`) foi regenerado com esses valores e
publicado na raiz de `aprovacao/100-aplicativos-uteis-cs-rascunho/`
(confirmado por inspeção do `index.html` gerado: canonical, og:url,
og:image, twitter:image e os caminhos de `<script>`/`<link>` do
bundle todos apontam para o novo domínio/caminho).

## 4. `/aprovacao/` sem listagem pública

Criado `aprovacao/index.html`: página com mensagem genérica
("Esta área é usada apenas para revisão de páginas específicas. Use o
link direto enviado por e-mail.") e um botão de volta para a home.
**Não lista** nenhuma página, produto, produtora ou slug. `noindex,nofollow`
aplicado a essa página também. Nenhum link para
`aprovacao/100-aplicativos-uteis-cs-rascunho/` foi adicionado em
nenhum lugar público (nem na home, nem em `aprovacao/index.html`).

## 5. Página inicial — "Produtos anunciados"

Adicionada a seção `#produtos` em `index.html` (entre "Como atuamos" e
"Transparência"), com:
- Título "Produtos anunciados".
- Texto: "Nenhum produto está sendo anunciado publicamente no momento."
- Orientação discreta: "Recebeu um link de revisão? Acesse exatamente
  o endereço enviado por e-mail."
- Item de menu correspondente adicionado à navegação.
- Nenhum link para páginas em `/aprovacao/` foi incluído.

## 6. Correção do `.gitignore` (ambos os repositórios tinham o mesmo problema)

O `.gitignore` continha apenas a linha `README.md`, o que em sintaxe
Git ignora qualquer arquivo `README.md` em qualquer subdiretório do
repositório — por isso nenhum README (nem o do site institucional, nem
os das landing pages) havia sido versionado até hoje em nenhum dos dois
repositórios. Substituído por regras de `.env`/`node_modules`/`dist`,
que é o que realmente precisa ficar de fora do controle de versão.

## 7. Landing page "+100 Aplicativos Úteis" — status mantido como rascunho

Confirmado que a landing page continua:
- `noindex,nofollow` (sem alteração — já era o padrão).
- Sem hotlink real (`VITE_HOTMART_HOTLINK` continua placeholder — CTA
  desabilitado por `CtaButton.tsx`/`links.ts`, comportamento herdado
  das rodadas anteriores, não alterado).
- Sem prints da Hotmart, foto/e-mail/dados pessoais da produtora, logos
  reais de aplicativos ou promessas de resultado (nenhum desses itens
  existia no projeto; nada foi adicionado).
- Deixa claro que é página de pré-venda/review de afiliado e que compra
  e acesso ocorrem pela Hotmart (textos herdados, não alterados nesta
  rodada).

## 8. Copy da seção "Sobre a criadora" / "Análise responsável da curadoria"

`src/data/product.ts` — campo `CREATOR.complement` reescrito (era um
texto mais raso, focado só em "não avaliar a trajetória completa da
criadora"). Novo texto reforça explicitamente que a página apresenta
"uma análise independente e responsável deste produto específico",
seguindo a direção sugerida, sem qualquer tom negativo sobre a criadora
ou outros produtos dela. `docs/copy.md` (documento de leitura) atualizado
em espelho.

## 9. Avisos no final da página

Confirmado (sem necessidade de mudança): `ImportantNoticesSection` já
está posicionada como penúltima seção em `App.tsx`, depois do FAQ e
antes do CTA final — todos os avisos legais/de afiliado/de escopo já
ficam concentrados ali, não no meio da página. O único aviso "no meio"
é a barra superior discreta (`TOP_BAR_TEXT`, uma linha), que já era
enxuta e não foi alterada.

## 10. Página pública futura (`/produtos/100-aplicativos-uteis/`)

Documentado em `README.md` (raiz), `aprovacao/README.md` e
`aprovacao/100-aplicativos-uteis-cs-rascunho/README.md`: depois da
aprovação, a pasta deve ser movida para
`/produtos/100-aplicativos-uteis/`, com `VITE_SITE_URL`/`VITE_BASE_PATH`
atualizados, `VITE_ROBOTS=index,follow`, hotlink real configurado, e
inclusão opcional na seção "Produtos anunciados" da home. **Essa
mudança não foi feita agora**, conforme pedido.

## 11. GitHub Pages e publicação

Repositório e organização corretos confirmados por clone real
(`trevodigitalconversoes/trevodigitalconversoes.github.io`). Nenhuma
configuração administrativa do GitHub (visibilidade, permissões,
colaboradores, branch protection, Pages settings, secrets) foi
consultada ou alterada — apenas arquivos de conteúdo/código/documentação
no working tree local.

## 12. Comandos executados e resultados

Todos rodados dentro de
`aprovacao/100-aplicativos-uteis-cs-rascunho/codigo-fonte/`:

```
npm install
  → added 51 packages, 0 vulnerabilities

npm run lint
  → oxlint — sem saída de warnings/erros (0 problemas)

npx tsc -b
  → sem erros

npm run build:staging
  → build gerado com sucesso (dist/index.html + assets)

npm run check:prod:source
  → 2 avisos (VITE_HOTMART_VERIFICATION_DATE e VITE_ROBOTS ausentes —
    ambos com fallback seguro documentado) e 2 erros bloqueantes
    esperados (VITE_HOTMART_HOTLINK e VITE_SITE_URL ainda placeholder
    neste ambiente sem .env real) — comportamento correto por design,
    não uma regressão.
```

Nenhum comando foi inventado; todos já existiam no projeto
(`package.json`). `check:prod:dist`/`build:prod` não foram usados nesta
rodada de validação porque dependem de um `.env` real (hotlink), que
ainda não foi fornecido — a validação de build de produção completa
(com `.env` fictício de teste) já havia sido feita e documentada na
rodada anterior (`docs/relatorio_ajustes_produtora_v2.md`, dentro de
`codigo-fonte/docs/`), com o novo base path confirmado manualmente por
inspeção do `dist/index.html` publicado (canonical/og:url/script/link
todos apontando para `trevodigitalconversoes.github.io/aprovacao/...`).

O build de staging publicado em
`aprovacao/100-aplicativos-uteis-cs-rascunho/{index.html,assets/}` foi
gerado com um `.env` fictício (`VITE_SITE_URL`, `VITE_BASE_PATH`,
`VITE_ROBOTS` — sem hotlink, sem data de verificação) e **removido em
seguida**; ele nunca foi commitado.

## 13. Pendências manuais

1. Confirmar exclusão do repositório antigo
   `correa0inaiara/trevo-digital-conversoes` (ação do usuário no
   GitHub — não realizada por mim).
2. `VITE_HOTMART_HOTLINK` — link real de afiliado da Hotmart.
3. `VITE_HOTMART_VERIFICATION_DATE` — data real de verificação de
   preço/garantia na Hotmart.
4. `VITE_CONTACT_URL` — canal de contato real do Trevo Digital
   Conversões (opcional, ex.: `https://trevodigitalconversoes.github.io/#contato`).
5. Confirmar se o GitHub Pages do repositório
   `trevodigitalconversoes/trevodigitalconversoes.github.io` está
   configurado para publicar a partir da raiz da branch `main`
   (`Settings → Pages → Deploy from a branch → main → / (root)`) — não
   foi alterado nem verificado por mim (configurações administrativas
   estão fora do escopo desta tarefa).
6. Decisão sobre manter `noindex,nofollow` até aprovação explícita da
   produtora (mantido por padrão).
7. **Nenhum commit ou push foi feito.** Todas as mudanças estão apenas
   no working tree local de `trevodigitalconversoes.github.io/`.

## 14. Próximos passos sugeridos

1. Revisar as mudanças localmente (`git status`, `git diff` dentro de
   `trevodigitalconversoes.github.io/`).
2. Quando estiver de acordo, autorizar/rodar `git add` + `git commit` +
   `git push` para `trevodigitalconversoes/trevodigitalconversoes.github.io`
   (branch `main`) — nenhum desses comandos foi executado nesta rodada.
3. Confirmar nas configurações do GitHub (fora do escopo desta tarefa)
   que o Pages está publicando a partir da raiz de `main`.
4. Enviar o link
   `https://trevodigitalconversoes.github.io/aprovacao/100-aplicativos-uteis-cs-rascunho/`
   por e-mail para a produtora, quando o repositório já estiver
   publicado.
5. Depois da aprovação: preencher hotlink real, data de verificação,
   mover a pasta para `/produtos/100-aplicativos-uteis/`, trocar
   `VITE_ROBOTS` para `index,follow` e gerar um novo build/deploy.
