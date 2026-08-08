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

## Revisão de escopo — 2026-08-08 (capacidades PostHog habilitadas)

O desenho original deste contrato (rodada anterior) desabilitava
explicitamente autocapture, heatmaps e Session Replay, mantendo só
`$pageview` + `outbound_hotmart`. O usuário decidiu explicitamente **não**
limitar o projeto a esse desenho mínimo permanentemente e usar
progressivamente mais capacidades do PostHog já disponíveis/configuradas
no projeto conectado. Este documento registra a decisão revisada.

### Estado real do projeto PostHog (confirmado externamente em 2026-08-08)

| Configuração | Valor |
|---|---|
| `anonymize_ips` | `true` |
| `completed_snippet_onboarding` | `true` |
| `autocapture_opt_out` | `false` (ou seja, autocapture permitido) |
| `autocapture_web_vitals_opt_in` | `true` |
| `heatmaps_opt_in` | `true` |
| `session_recording_opt_in` | `true` |
| `session_recording_retention_period` | `30d` |
| `capture_console_log_opt_in` | `true` |
| `session_recording_masking_config` | `null` |
| `session_recording_network_payload_capture_config` | `null` |
| `ingested_event` | `false` (nenhum evento real ainda ingerido) |

Essas flags dizem o que está **permitido/configurado no projeto**. O que
efetivamente é habilitado no `posthog.init()` desta pre-sell é uma decisão
separada, registrada abaixo — não usamos tudo que o projeto permite
indiscriminadamente.

### Fontes oficiais consultadas em 2026-08-08

- [Anonymous vs identified events](https://posthog.com/docs/data/anonymous-vs-identified-events) — valores válidos de `person_profiles`.
- [PostHogConfig reference](https://posthog.com/docs/references/posthog-js/types/PostHogConfig) — `enable_recording_console_log`, `capture_heatmaps` (nome atual, substitui `enable_heatmaps`).
- [JS SDK config](https://posthog.com/docs/libraries/js/config) — `autocapture`, `capture_pageview`, `disable_session_recording`, mudança `enable_heatmaps` → `capture_heatmaps`.
- [Session Replay — Privacy](https://posthog.com/docs/session-replay/privacy) — masking default de inputs, texto geral não mascarado por padrão.
- [Session Replay — Network recording](https://posthog.com/docs/session-replay/network-recording) — captura de payload é opt-in; URL/timing sempre capturados; deny-list fixa de headers (`authorization`, `cookie`, `set-cookie`) nunca capturados independentemente de config.
- [Web Vitals](https://posthog.com/docs/web-analytics/web-vitals) — via `capture_performance: { web_vitals: true }`.
- [Heatmaps](https://posthog.com/docs/toolbar/heatmaps) — chave de config (nota: esta página ainda cita o nome legado `enable_heatmaps`; usamos `capture_heatmaps` por ser o nome documentado como atual na referência de tipos).
- [Google Ads ValueTrack](https://support.google.com/google-ads/answer/6305348) e [Hotmart — SRC](https://help.hotmart.com/en/article/216441797/how-can-i-track-the-source-of-my-sales-on-hotmart-) — já confirmados na rodada anterior, sem mudança.

Algumas páginas retornaram conteúdo truncado nas consultas desta sessão
(ex.: shape completo de `session_recording`, defaults exatos de
`capture_performance`) — as decisões abaixo usam o que foi confirmado com
alta confiança; qualquer ponto assinalado como "confirmar antes do
primeiro deploy real" deve ser revalidado lendo a doc completa (não só o
fetch parcial) antes de gerar tráfego pago.

### `person_profiles` — revalidado

`'never'` **não aparece mais** como valor documentado/suportado
(`posthog.com/docs/data/anonymous-vs-identified-events` só lista
`'identified_only'` e `'always'`). Mantido `'identified_only'`: como o
código nunca chama `identify()`/`alias()`/`group()`/`setPersonProperties()`,
nenhum person profile é criado de qualquer forma — equivalente prático ao
`'never'` original. **Sem conflito** com autocapture/heatmaps/Web
Vitals/Session Replay: nenhuma dessas capacidades exige pessoa
identificada, todas funcionam sobre `distinct_id`/sessão anônimos.

### Capacidades habilitadas nesta pre-sell e por quê

| Capacidade | Habilitada? | Config | Motivo |
|---|---|---|---|
| Product/Web Analytics (`$pageview`) | sim | `capture_pageview: true`, `capture_pageleave: true` | já existia; `capture_pageleave` ligado agora para métricas de engajamento do Web Analytics |
| `outbound_hotmart` | sim (inalterado) | evento customizado explícito | continua a métrica canônica de conversão — autocapture NÃO a substitui |
| Autocapture | sim | `autocapture: true` | pedido explícito do usuário; página não tem campo sensível hoje |
| Heatmaps | sim | `capture_heatmaps: true` | pedido explícito; objetivo declarado: entender interação com FAQ/CTAs |
| Web Vitals | sim | `capture_performance: { web_vitals: true }` | observação de campo (RUM), complementar ao PageSpeed/Lighthouse (laboratório) — não substitui o baseline `tools/pagespeed/` |
| Session Replay | sim | `disable_session_recording: false` | pedido explícito; ver decisões de privacidade abaixo |
| Console log recording | **não** | `enable_recording_console_log: false` | permitido pelo projeto, mas sem utilidade concreta aqui e com risco de vazamento acidental — decisão específica desta pre-sell, não uma mudança de config global |
| Captura de payload de rede | **não** | ausente do config (fica no default/opt-in não usado) | preserva `session_recording_network_payload_capture_config = null` observado no projeto; a doc confirma que é opt-in e que headers de auth/cookie nunca são capturados de qualquer forma |
| Persistência (cookies/localStorage do PostHog) | sim, agora | `disable_persistence: false` | necessária para Session Replay/heatmaps correlacionarem uma sessão entre interações; era `true` no desenho mínimo original — mudança relevante de privacidade, registrada aqui explicitamente |
| `identify()`/person profile | não | `person_profiles: 'identified_only'`, sem chamada a `identify()` | inalterado |

### Masking (Session Replay)

Input fields (e-mail, senha etc.) são mascarados **por padrão** pelo SDK
(`posthog.com/docs/session-replay/privacy`), então `maskAllInputs: true`
no config é uma confirmação explícita de um comportamento que já seria o
default — feito assim de propósito, para não depender só do default
implícito. Texto geral da página **não** é mascarado por padrão; aceitável
aqui porque a pre-sell não tem formulário/checkout e todo o texto visível
é copy comercial pública, sem dado gerado pelo usuário.

### Rede

Nenhuma opção de captura de payload de rede foi adicionada ao config.
Captura de URL + timing continua acontecendo (parte do Session
Replay/Web Vitals padrão), mas nunca corpo de request/response, nunca
headers sensíveis — e mesmo que fosse habilitado no futuro, a doc
confirma uma deny-list fixa do PostHog que nunca captura
`authorization`/`cookie`/`set-cookie`.

### Sampling / retenção

Retenção observada no projeto: `session_recording_retention_period = 30d`
— registrado aqui, **não alterado** nesta rodada (sem necessidade
comprovada de mudar).

Sampling de Session Replay (gravar 100% das sessões vs. uma amostra) é
uma decisão econômica/de produto que depende de volume de tráfego real —
que ainda não existe (microteste não lançado). Recomendação, não
implementada em código: começar com 100% das sessões dado o volume baixo
esperado no primeiro microteste, e revisitar a amostragem (via
configuração do projeto no PostHog, não via este código) antes de
escalar tráfego pago. Fica registrado como decisão pendente de revisão
humana antes de qualquer campanha real.

### IP — gate encerrado

`anonymize_ips = true` confirmado no projeto PostHog conectado. O gate de
privacidade de IP desta pre-sell está **PASS**. Formulação factual (sem
linguagem jurídica absoluta): o projeto está configurado para
processar/descartar o endereço IP do visitante conforme essa opção do
PostHog, não para "não processar IP algum" — a requisição HTTP
inevitavelmente carrega o IP de origem até o servidor do PostHog antes de
qualquer transformação ser aplicada.
