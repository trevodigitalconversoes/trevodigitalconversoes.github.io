# Etapa 5c — Contrato de tracking do Microteste Comercial 01

Fonte de verdade do contrato. Qualquer mudança nos parâmetros/eventos
abaixo deve ser refletida em `tools/tracking/src/trevo_tracking/params.py`,
`tools/tracking/src/trevo_tracking/tracking_config.py`,
`assets/js/etapa_5_d_v1_tracking.js` e neste documento, nessa ordem.

## Fluxo

```
Google Ads → pre-sell (fotografia-presets-lightroom) → PostHog (evento anônimo) → HotLink Hotmart → venda/comissão
```

Nenhuma campanha Google Ads foi criada nesta etapa. Este documento define
o contrato que a campanha deve seguir quando for criada.

## Identificadores

- Microteste: `mt01`
- Produto: `foto18` (uso interno/documentação — o `product_slug` real
  enviado ao PostHog é `fotografia-presets-lightroom`, que é o slug real
  da pasta em `produtos/`)

## ValueTrack (Google Ads) — quando a campanha for criada

```
utm_source=google
utm_medium=cpc
utm_campaign=mt01-foto18
utm_content=est01 | est02 | vid01   (por criativo)
campaign_id={campaignid}
ad_group_id={adgroupid}
ad_id={creative}
device={device}
network={network}
```

Quando Search for usado, adicionar também:

```
utm_term={keyword}
matchtype={matchtype}
```

Auto-tagging/GCLID permanece habilitado — `gclid` chega como parâmetro de
URL automático da própria Google Ads, não precisa ser adicionado
manualmente ao Final URL suffix.

Fonte: [Google Ads Help — ValueTrack parameters](https://support.google.com/google-ads/answer/6305348)
(confirmado em 2026-08-08 — `{campaignid}`, `{adgroupid}`, `{creative}`,
`{device}`, `{network}`, `{keyword}`, `{matchtype}` continuam os nomes
oficiais dos placeholders).

## Whitelist de parâmetros aceitos pela pre-sell

Qualquer parâmetro de query fora desta lista é descartado — nunca vira
propriedade de evento nem é repassado a lugar nenhum:

```
utm_source, utm_medium, utm_campaign, utm_content, utm_term,
campaign_id, ad_group_id, ad_id, device, network, matchtype,
gclid, gbraid, wbraid, gad_source
```

Implementado em `tools/tracking/src/trevo_tracking/params.py`
(`ALLOWED_CAMPAIGN_PARAMS`) e espelhado em `assets/js/etapa_5_d_v1_tracking.js`
(via `config.allowedCampaignParams`, gerado a partir do mesmo Python).

## Eventos PostHog

### `$pageview`

Evento padrão do SDK (`capture_pageview: true`). Não criamos um evento
customizado equivalente (seria redundante).

### `outbound_hotmart`

Disparado no clique de qualquer CTA que leva ao HotLink Hotmart, antes da
navegação (a navegação em si nunca depende do sucesso desse `capture`).
Não criamos `cta_click`/`hotmart_click`/`checkout_click` em paralelo — uma
conversão = um evento.

Propriedades:

| Propriedade | Sempre presente? | Origem |
|---|---|---|
| `product_slug` | sim | fixo: `fotografia-presets-lightroom` |
| `experiment_id` | sim | fixo: `mt01` |
| `cta_location` | sim | `data-cta-position` do `<a>` clicado (`hero`, `final`) |
| `creative_code` | só se `utm_content` presente na URL | query string |
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` | só se presentes | query string |
| `campaign_id`, `ad_group_id`, `ad_id`, `device`, `network`, `matchtype`, `gclid` | só se presentes | query string |

Nunca registrado: nome, e-mail, telefone, CPF, endereço, dados de
formulário, fingerprint customizado, conteúdo digitado, dados do
comprador — a pre-sell não tem formulário, então isso é uma garantia
estrutural, não apenas uma promessa de código.

## CTAs reais da página (`produtos/fotografia-presets-lightroom/index.html`)

Dois CTAs existentes, ambos já tinham `data-cta-position` no HTML antes
desta tarefa (usado como `cta_location`, sem inventar nomenclatura):

1. `data-cta-position="hero"` — "Quero conhecer o material"
2. `data-cta-position="final"` — "Quero acessar agora"

Não existe um terceiro CTA "middle" na página real — não foi criado um
para não alterar a estrutura/copy da página.

## SRC Hotmart

Padrão: `<network_prefix>|<experiment_id>|<creative_code>`, ex.:
`g|mt01|est01`.

Regras (confirmadas em
[help.hotmart.com](https://help.hotmart.com/en/article/216441797/how-can-i-track-the-source-of-my-sales-on-hotmart-)
em 2026-08-08): máximo 30 caracteres, `_` proibido (reservado
internamente pela Hotmart), `|` permitido.

`creative_code` vem de `utm_content` quando presente. Sem `utm_content`
(ex.: clique orgânico/QA sem parâmetros), o fallback documentado é
`none` — nunca um criativo inventado. Implementado e testado em
`tools/tracking/src/trevo_tracking/src_builder.py`.

## HotLink

Base (preservar sempre, nunca trocar pelo link público do produto —
é o link de atribuição de comissão):

```
https://go.hotmart.com/V106592210H
```

No clique, o link final adiciona `src` + o subconjunto de UTMs abaixo,
preservando qualquer parâmetro que já exista na URL base:

```
utm_source, utm_medium, utm_campaign, utm_content, utm_term
```

Não propagados ao HotLink (ficam só no PostHog): `gclid`, `campaign_id`,
`ad_group_id`, `ad_id` — a Hotmart não documenta uso desses parâmetros e
não há necessidade comprovada de enviá-los.

Implementado em `tools/tracking/src/trevo_tracking/hotlink_builder.py`
(Python, para QA/testes) e `assets/js/etapa_5_d_v1_tracking.js`
(`buildHotlink`, runtime real via `URL`/`URLSearchParams`).

## Resiliência

O `href` de cada CTA no HTML já é o HotLink base, funcional por si só. O
JS faz *progressive enhancement*: reescreve o `href` com `src`/UTMs assim
que roda. Se o script nunca rodar (bloqueado por ad blocker, erro, JS
desabilitado), o clique ainda leva ao HotLink correto — só sem
enriquecimento de atribuição. Nenhuma chamada ao PostHog pode impedir a
navegação (todas estão em `try/catch`).
