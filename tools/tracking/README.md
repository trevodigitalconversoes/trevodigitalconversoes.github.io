# tools/tracking

Ferramenta local para gerar a configuração pública de tracking (PostHog +
Hotmart) do **Microteste Comercial 01** e rodar QA estático antes de
publicar. Contrato completo do tracking:
[`docs/etapa_5_c_v1_contrato_tracking_microteste01.md`](../../docs/etapa_5_c_v1_contrato_tracking_microteste01.md).

## Objetivo

Instrumentar `produtos/fotografia-presets-lightroom/` com:

- `$pageview` (evento padrão do PostHog) em toda visita;
- `outbound_hotmart` (evento customizado) no clique de qualquer CTA que
  leva ao HotLink Hotmart, com `src`/UTMs corretos e sem dado pessoal.

Sem criar campanha Google Ads, sem gastar, sem realizar compra.

## Arquitetura

```
tools/tracking/
  src/trevo_tracking/          # core Python: config, whitelist, SRC, HotLink, config publica
  etapa_5_a_v1_generate_tracking_config.py   # gera assets/js/tracking-config.generated.js
  etapa_5_b_v1_tracking_qa.py                # QA estatico local (sem rede/browser)
  tests/                        # 39 testes, sem chamar PostHog/Hotmart real

assets/js/
  etapa_5_d_v1_tracking.js              # runtime publico (carregado pela pre-sell)
  tracking-config.generated.js          # gerado por etapa_5_a, PUBLICO e commitado de proposito
```

## `.env`

Copie `.env.example` para `.env` (nunca commitado — coberto por
`tools/tracking/.gitignore`):

```
POSTHOG_PROJECT_TOKEN=seu_project_token
POSTHOG_HOST=https://us.i.posthog.com
```

Como obter: PostHog → *Project settings* → "Project API Key".

## Project token × Personal API Key — leia antes de mexer aqui

**Project token** (`POSTHOG_PROJECT_TOKEN`, formato tipicamente
`phc_...`): é o token de **ingestão** do SDK web. Por definição, precisa
rodar no navegador do visitante — não existe forma de usar o SDK web do
PostHog sem ele aparecer no JavaScript que chega ao cliente. Por isso
`etapa_5_a_v1_generate_tracking_config.py` grava esse valor em
`assets/js/tracking-config.generated.js`, que é **público e commitado de
propósito** (mesma lógica de uma chave pública do Google Analytics/GA4 ou
Segment — não é um segredo de servidor).

**Personal API Key**: uma credencial totalmente diferente, usada para
automações/API administrativa do PostHog (ex.: ler dados via API, criar
recursos). **Essa sim é um segredo real**: nunca entra em HTML/JS, nunca é
commitada, nunca é enviada ao navegador. Este microteste **não precisa**
de Personal API Key — nenhum código aqui a usa.

Se algum dia uma Personal API Key for necessária (ex.: consultar eventos
via API para QA — ver seção "Validação real" abaixo), ela deve ficar
**só** em `.env`, nunca em `assets/js/`.

## Comandos

```bash
python -m pip install -e ".[dev]"

# gera assets/js/tracking-config.generated.js a partir do .env
python etapa_5_a_v1_generate_tracking_config.py

# QA estatico (JS sem chamadas proibidas, CTAs instrumentados, contrato SRC/HotLink)
python etapa_5_b_v1_tracking_qa.py

# testes
python -m pytest -q
```

Se `POSTHOG_PROJECT_TOKEN` estiver ausente, `etapa_5_a` para **antes** de
escrever qualquer arquivo e imprime `{"status": "POSTHOG_PROJECT_TOKEN_AUSENTE"}`
(exit 1) — nunca pede para colar o token no chat.

## Configuração PostHog (eventos anônimos)

```js
{
  person_profiles: 'identified_only', // ver nota abaixo
  autocapture: false,
  capture_pageview: true,
  capture_pageleave: false,
  disable_session_recording: true,
  disable_persistence: true,
  save_campaign_params: true,
  save_referrer: false,
  debug: false,
  before_send: <sanitiza $current_url pela whitelist antes de enviar>
}
```

**Mudança de API registrada:** a configuração desejada original era
`person_profiles: 'never'`. A documentação atual do PostHog (confirmada
em 2026-08-08) documenta `'identified_only'` como o valor atual —
default recomendado, que cria um person profile **somente** se
`identify()` for chamado. Como este código **nunca** chama
`identify()`/`alias()`/`group()`/`setPersonProperties()`, o efeito
prático é idêntico ao `'never'` original: nenhum person profile é criado
para nenhum visitante. Ver `tools/tracking/src/trevo_tracking/tracking_config.py`.

Nunca habilitados neste microteste: session replay, autocapture geral,
console recording, surveys, heatmaps, feature flags, exception tracking.

## Privacidade / IP

⚠️ **Gate manual, fora do código.** O projeto PostHog conectado foi
observado com `anonymize_ips = false`. É necessário confirmar
manualmente em **Settings → Project → Privacy → IP data capture
configuration → Discard client IP data** que o descarte está ativo antes
de declarar o tracking pronto. Nenhum script aqui consegue confirmar isso
automaticamente sem uma Personal API Key (que este projeto
deliberadamente não usa) — por isso esse gate fica **pendente por
padrão** até confirmação humana explícita. Enquanto pendente, o veredito
correto é `TRACKING_PRIVACY_GATE_PENDING`, nunca um veredito "pronto".

## Eventos

Ver contrato completo em
[`docs/etapa_5_c_v1_contrato_tracking_microteste01.md`](../../docs/etapa_5_c_v1_contrato_tracking_microteste01.md):
`$pageview` (padrão) e `outbound_hotmart` (customizado, propriedades
documentadas lá).

## UTMs / ValueTrack / SRC / HotLink

Também documentados no contrato acima. Resumo:

- Whitelist de parâmetros aceitos: `tools/tracking/src/trevo_tracking/params.py`.
- SRC (`g|mt01|<creative>`, máx 30 chars, sem `_`): `src_builder.py`.
- HotLink final (`src` + subconjunto de UTMs, preserva query existente,
  usa `URL`/`URLSearchParams`, nunca concatenação manual):
  `hotlink_builder.py` (Python, espelhado no JS).

## Como testar sem comprar

1. Gere a config: `python etapa_5_a_v1_generate_tracking_config.py`.
2. Rode o QA estático: `python etapa_5_b_v1_tracking_qa.py`.
3. Abra a pre-sell localmente com parâmetros sintéticos, ex.:
   `?utm_source=google&utm_medium=cpc&utm_campaign=mt01-foto18&utm_content=est01&gclid=TESTE-NAO-REAL`.
4. Confirme no DevTools: console sem erro, `href` dos CTAs reescrito com
   `src`/UTMs corretos, evento `$pageview` disparado, evento
   `outbound_hotmart` disparado ao clicar (Network tab, requisições para
   `i.posthog.com`) — **sem clicar de fato até o checkout Hotmart**, ou,
   se clicar, **nunca completar a compra**.
5. No PostHog (Activity/Live events), confirme que os dois eventos de
   teste chegaram com as propriedades esperadas e nenhum dado pessoal.

## Como reexecutar

Rode `etapa_5_a` de novo sempre que o `.env` mudar (ex.: token rotacionado).
O arquivo gerado é sobrescrito — não é necessário limpar nada antes.

## Como desligar o tracking

Remova (ou comente) as duas tags `<script>` no fim de
`produtos/fotografia-presets-lightroom/index.html`. Sem
`window.__TREVO_TRACKING_CONFIG__` definido, `etapa_5_d_v1_tracking.js`
retorna imediatamente (nenhum efeito) mesmo que o arquivo continue
carregado — ver o primeiro `if` do arquivo.

## Limitações

- CrUX/`ruff`/`mypy` fora de escopo aqui (mesmo padrão de
  `tools/instagram`/`tools/pagespeed`).
- O gate de descarte de IP não é verificável por código nesta
  configuração (ver seção "Privacidade / IP").
- Nenhuma automação cria a campanha Google Ads — isso é manual, fora
  desta ferramenta, por design.

## Troubleshooting

- **`POSTHOG_PROJECT_TOKEN_AUSENTE`**: crie `tools/tracking/.env` a
  partir de `.env.example` e preencha o token real.
- **CTA não é reescrito / evento não dispara**: confira se
  `assets/js/tracking-config.generated.js` existe e foi publicado (é
  gerado localmente e precisa ser commitado — ver "Comandos" acima);
  confira se `a.cta-button` no HTML tem `href` começando com o HotLink
  base (`https://go.hotmart.com/V106592210H`) — é assim que o script
  encontra os CTAs para instrumentar.
- **Ad blocker bloqueando `i.posthog.com`**: esperado para uma fração do
  tráfego real. O CTA continua funcionando (ver "Resiliência" no
  contrato) — é uma perda de medição aceitável, não um bug.
