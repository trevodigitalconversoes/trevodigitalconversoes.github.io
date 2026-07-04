# ⚠ `/aprovacao/` — revisão de páginas específicas (não é um índice público)

Este arquivo é documentação para quem mantém o repositório — **não é
servido como página**. O que os visitantes veem em
`https://trevodigitalconversoes.github.io/aprovacao/` é `index.html`
nesta mesma pasta: uma mensagem genérica, sem listar nenhuma página,
produto ou produtora.

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

## Quando mover uma página para `/produtos/`

1. A produtora/cliente aprovou o conteúdo (quando aplicável).
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
