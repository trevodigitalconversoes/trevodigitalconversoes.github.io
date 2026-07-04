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
- `docs/` — checklist de compliance (`compliance.md`) e o registro da
  decisão de arquitetura (`decisao_migracao_html_estatico.md`).

Para editar o conteúdo, edite `index.html` diretamente — não há passo de
build.

## URL desta página

```
https://trevodigitalconversoes.github.io/aprovacao/100-aplicativos-uteis/
```

## Status atual

- **JavaScript:** nenhum. Zero `<script>` na página.
- **Robots:** `noindex,nofollow` (rascunho — não deve ser indexado até
  aprovação da produtora).
- **CTA "Ver produto na Hotmart":** hotlink de afiliado já configurado —
  usa o link otimizado para Google Ads (derivado do hotlink base
  confirmado na área de Hotlinks da Hotmart), preservando o rastreamento
  de afiliado. Ver `docs/compliance.md` para o link completo e os testes
  recomendados antes de campanha paga.
- **Data de verificação (preço/garantia na Hotmart):** ainda não
  preenchida — a seção "Informações observadas na Hotmart" usa o
  placeholder `[INSERIR_DATA_DE_VERIFICACAO]`.
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

1. Testar manualmente o clique no CTA e confirmar que o hotlink redireciona
   corretamente para a página do produto na Hotmart.
2. Confirmar na Hotmart/Google Ads se o link otimizado (com
   `redirectionUrl`) é o formato recomendado para a campanha planejada.
3. Data real em que preço/garantia foram conferidos na Hotmart.
4. Canal de contato definitivo do Trevo Digital Conversões, se diferente
   do atual.
5. Aprovação explícita da produtora sobre o conteúdo.
6. Só depois de todo o acima: mover a pasta para
   `/produtos/100-aplicativos-uteis/`, trocar `robots` para
   `index,follow`, e atualizar `canonical`/Open Graph para o novo caminho.
