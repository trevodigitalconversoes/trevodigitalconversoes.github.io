# "+100 Aplicativos Úteis" — rascunho aguardando aprovação

Landing page de pré-venda/análise de afiliado sobre o produto Hotmart
"+100 Aplicativos Úteis para Produtividade Empreendedora".

Esta pasta é o conteúdo de **um slug de revisão específico** dentro de
`/aprovacao/` (ver `../README.md` para a convenção geral desta área).
Nada aqui aparece listado em `/aprovacao/` — o único jeito de chegar a
esta página é pelo link direto e completo.

## Arquitetura

HTML + CSS estático, **sem build e sem nenhum JavaScript**:
- `index.html` — todo o conteúdo em HTML semântico puro.
- `styles.css` — estilos, com `@font-face` apontando para `fonts/`.
- `fonts/` — arquivos `.woff2` self-hosted (Sora + Instrument Sans).
- `favicon.svg`, `og-image.svg`.
- `docs/` — copy completa, checklist de compliance e histórico do
  projeto anterior (ver `docs/decisao_migracao_html_estatico.md` para o
  motivo da troca de Vite+React para HTML estático).

Para editar o conteúdo, edite `index.html` diretamente — não há passo de
build.

## URL desta página

```
https://trevodigitalconversoes.github.io/aprovacao/100-aplicativos-uteis/
```

## Status atual

- **JavaScript:** nenhum. Zero `<script>` na página.
- **Robots:** `noindex,nofollow` (rascunho — não deve ser indexado).
- **CTA "Ver produto na Hotmart":** aponta temporariamente para a URL
  pública oficial do produto na Hotmart (sem parâmetro de afiliado):
  `https://hotmart.com/pt-br/marketplace/produtos/100-aplicativos-uteis-para-produtividade-empreendedora/N87977370D`.
  **Este ainda não é o hotlink de afiliado** — é um link real e
  funcional, usado apenas até a aprovação/configuração do hotlink
  definitivo. Isso é avisado explicitamente na seção "Avisos
  importantes" da própria página.
- **Data de verificação (preço/garantia na Hotmart):** ainda não
  preenchida — a seção "Informações observadas na Hotmart" usa o texto
  genérico sem data.
- **Contato:** aponta para `https://trevodigitalconversoes.github.io/#contato`.
- **Aprovação da produtora:** pendente.

## Isso não é autenticação real

`noindex,nofollow` + URL específica/não listada em `/aprovacao/` +
ausência de link público reduzem a chance de descoberta casual ou por
buscadores, mas **não são controle de acesso**. O repositório
`trevodigitalconversoes/trevodigitalconversoes.github.io` é público e
GitHub Pages é hospedagem estática sem backend — qualquer pessoa com a
URL exata (ou que inspecione o histórico público do repositório) acessa
o conteúdo normalmente. Não trate esta pasta como um lugar seguro para
dados sensíveis.

## Pendências antes de rodar anúncios (preencher manualmente)

1. Hotlink de afiliado real da Hotmart — substituir a URL pública oficial
   nos dois `<a class="button primary">` de `index.html`.
2. Data real em que preço/garantia foram conferidos na Hotmart.
3. Canal de contato definitivo do Trevo Digital Conversões, se diferente
   do atual.
4. Aprovação explícita da produtora sobre o conteúdo.
5. Só depois de todo o acima: mover a pasta para
   `/produtos/100-aplicativos-uteis/`, trocar `robots` para
   `index,follow`, e atualizar `canonical`/Open Graph para o novo caminho.
