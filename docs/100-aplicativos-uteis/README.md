# "+100 Aplicativos Úteis" — documentação técnica

Landing page de pré-venda/análise de afiliado sobre o produto Hotmart
"+100 Aplicativos Úteis para Produtividade Empreendedora", publicada
em `/produtos/100-aplicativos-uteis/`.

Este é o registro histórico e técnico da página (arquitetura,
compliance, decisões de migração). A pasta pública com o HTML/CSS/
assets servidos vive em `produtos/100-aplicativos-uteis/` na raiz do
repositório — este `docs/100-aplicativos-uteis/` contém só a
documentação de apoio, não o conteúdo servido.

## Histórico

Esta página existiu anteriormente em `/aprovacao/100-aplicativos-uteis/`
(área de revisão que foi removida em 2026-08-07 — ver
`docs/ADR_PRESELL_OWNERSHIP.md`). Foi promovida a
`/produtos/100-aplicativos-uteis/` na mesma etapa, com metadata de
produção (`index,follow`, canonical final) e fatos comerciais
revalidados na página oficial da Hotmart em 07/08/2026 (preço,
garantia e dados da criadora — ver
`docs/etapa_3_c_v1_remocao_aprovacao_promocao_100_apps.md`).

## Arquitetura

HTML + CSS estático, **sem build e sem nenhum JavaScript**:
- `index.html` — todo o conteúdo em HTML semântico puro.
- `styles.css` — estilos, com `@font-face` apontando para `fonts/`.
- `fonts/` — arquivos `.woff2` self-hosted (Sora + Instrument Sans).
- `favicon.svg`, `og-image.svg`.
- Documentação técnica (este README, `compliance.md`,
  `decisao_migracao_html_estatico.md`) vive em `docs/100-aplicativos-uteis/`,
  fora da pasta pública do produto.

Para editar o conteúdo, edite `produtos/100-aplicativos-uteis/index.html`
diretamente — não há passo de build.

## URL desta página

```
https://trevodigitalconversoes.github.io/produtos/100-aplicativos-uteis/
```

## Status atual

- **JavaScript:** nenhum. Zero `<script>` na página.
- **Robots:** `index,follow` (página de produção).
- **CTA "Ver produto na Hotmart":** hotlink de afiliado configurado —
  usa o link otimizado para Google Ads (derivado do hotlink base
  confirmado na área de Hotlinks da Hotmart), preservando o rastreamento
  de afiliado. Ver `compliance.md` para o link completo e os testes
  recomendados antes de campanha paga.
- **Data de verificação (preço/garantia na Hotmart):** 07/08/2026,
  revalidada diretamente na página oficial do produto no marketplace da
  Hotmart (preço R$ 69,90, garantia 7 dias, criadora Camila Silveira, 7
  anos na plataforma — todos batendo com o que já estava publicado).
- **Contato:** aponta para `https://trevodigitalconversoes.github.io/#contato`.

## Isso não é autenticação real (histórico)

Enquanto a página viveu em `/aprovacao/`, a nota abaixo se aplicava —
preservada aqui apenas como registro, já que `/aprovacao/` não existe
mais: `noindex,nofollow` + URL não listada + ausência de link público
reduziam a chance de descoberta casual, mas nunca foram controle de
acesso real (o repositório é público e GitHub Pages não tem backend).

## Pendências antes de rodar anúncios (preencher manualmente)

1. Testar manualmente o clique no CTA e confirmar que o hotlink redireciona
   corretamente para a página do produto na Hotmart.
2. Confirmar na Hotmart/Google Ads se o link otimizado (com
   `redirectionUrl`) é o formato recomendado para a campanha planejada.

As pendências de data de verificação, aprovação de produtora (não
exigida por padrão — ver ADR) e migração para `/produtos/` já foram
resolvidas nesta etapa.
