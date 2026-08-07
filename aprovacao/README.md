# ⚠ `/aprovacao/` — caso histórico/excepcional (não é um índice público)

Este arquivo é documentação para quem mantém o repositório — **não é
servido como página**. O que os visitantes veem em
`https://trevodigitalconversoes.github.io/aprovacao/` é `index.html`
nesta mesma pasta: uma mensagem genérica, sem listar nenhuma página,
produto ou produtora.

**Esta pasta não é mais o fluxo padrão para novas pre-sells.** A
partir da etapa registrada em
`docs/etapa_3_a_v1_migracao_presell_trevo.md`, novas páginas nascem
diretamente em `/produtos/<slug>/`, como artefatos de produção
(`index,follow`, canonical final desde o primeiro commit) — o estado
de desenvolvimento fica em git/branches/PR, não no HTML público. Ver
`docs/ADR_PRESELL_OWNERSHIP.md`, seção "Regra de publicação".

`/aprovacao/` continua existindo apenas para casos históricos ou
excepcionais (hoje, só `100-aplicativos-uteis/`, criada antes desta
regra). Uma página aqui **não implica** que foi ou será enviada a uma
produtora para aprovação — contato com produtora segue a mesma regra
de sempre: só quando uma exigência explícita determinar (ver
`docs/ADR_PRESELL_OWNERSHIP.md`).

## Convenção

Cada página em revisão vive em `/aprovacao/<slug-único-da-página>/`,
com um slug específico (ex.: `100-aplicativos-uteis/`). Regras:

- **Nunca** adicionar links para essas subpastas em `index.html` desta
  pasta, na home do site (`/index.html`) ou em qualquer menu/nav
  público.
- **Nunca** criar um índice/listagem (nem em HTML, nem em JSON, nem em
  um sitemap público) enumerando os slugs existentes.
- Cada página em `/aprovacao/<slug>/` deve manter
  `<meta name="robots" content="noindex,nofollow">`.
- O link de revisão é compartilhado **apenas** por e-mail (ou outro
  canal privado) diretamente com quem precisa aprovar o conteúdo.

## Isso não é autenticação real

`noindex,nofollow` + slug não listado/não previsível + ausência de
links públicos reduzem a chance de descoberta casual ou via
buscadores — mas **não são controle de acesso**. O repositório
`trevodigitalconversoes/trevodigitalconversoes.github.io` é público, e
GitHub Pages é hospedagem estática sem backend: qualquer pessoa com a
URL exata acessa o conteúdo normalmente, e o histórico de commits do
repositório também é público (então o próprio nome do slug pode ficar
visível ali). Não use esta área para dados sensíveis, e não a apresente
como um mecanismo de segurança real — é apenas discrição operacional.
Se um controle de acesso de verdade for necessário no futuro, isso
exige um backend/autenticação, o que está fora do escopo de GitHub
Pages puro.

## Quando mover uma página histórica para `/produtos/`

Esta seção se aplica ao caso excepcional de uma página que ainda vive
em `/aprovacao/` (fluxo antigo). Novas pre-sells não passam por aqui —
nascem direto em `/produtos/`.

Não existe uma exigência geral de aprovação da produtora antes de
publicar. Contato com a produtora só é necessário quando uma regra
explícita exigir (regra do produto, da Hotmart, da plataforma de
anúncios usada, contrato, ou legislação aplicável — ver
`docs/ADR_PRESELL_OWNERSHIP.md`). Fora desses casos, a página pode
avançar para `/produtos/` assim que:

1. Quando aplicável, a exigência específica de aprovação (se houver
   uma) foi cumprida.
2. Os valores reais estão preenchidos diretamente no HTML da página
   (hotlink de afiliado real da Hotmart, data de verificação de
   preço/garantia).
3. A pasta foi movida de `/aprovacao/<slug>/` para
   `/produtos/<slug-definitivo>/`, com `canonical`/Open Graph
   atualizados para o novo caminho (as páginas atuais são HTML/CSS
   estático, sem build — não há mais variáveis de ambiente envolvidas).
4. `<meta name="robots">` foi trocado para `index,follow`.
5. Se a página estiver em campanha ativa, ela pode ser incluída na
   seção "Produtos anunciados" da home (`/index.html`).
