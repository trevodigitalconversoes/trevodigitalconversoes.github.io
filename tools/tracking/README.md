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
  tests/                        # 46 testes, sem chamar PostHog/Hotmart real

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

## Configuração PostHog

**Histórico da decisão:** a rodada anterior deste PR usava um desenho
mínimo (autocapture/heatmaps/session replay desligados). Em 2026-08-08 o
usuário decidiu explicitamente usar progressivamente mais capacidades do
PostHog já disponíveis no projeto conectado, em vez de limitar o projeto
permanentemente a esse desenho mínimo. Registro completo da decisão,
estado real do projeto PostHog e fontes oficiais consultadas:
[`docs/etapa_5_c_v1_contrato_tracking_microteste01.md`](../../docs/etapa_5_c_v1_contrato_tracking_microteste01.md#revisão-de-escopo--2026-08-08-capacidades-posthog-habilitadas).

```js
{
  person_profiles: 'identified_only', // ver nota abaixo -- 'never' nao existe mais na doc atual
  autocapture: true,
  capture_pageview: true,
  capture_pageleave: true,
  disable_session_recording: false,
  disable_persistence: false,
  save_campaign_params: true,
  save_referrer: false,
  debug: false,
  capture_performance: { web_vitals: true },   // Web Vitals (RUM) -- nao substitui tools/pagespeed/
  capture_heatmaps: true,
  enable_recording_console_log: false,          // decisao explicita: OFF nesta pre-sell
  session_recording: { maskAllInputs: true },   // reforca (nao muda) o default do SDK
  before_send: <sanitiza $current_url pela whitelist antes de enviar>
}
```

**Mudança de API registrada:** `person_profiles: 'never'` não aparece mais
como valor documentado/suportado (revalidado em 2026-08-08) — só
`'identified_only'` (default recomendado) e `'always'`. Mantido
`'identified_only'`: como este código **nunca** chama
`identify()`/`alias()`/`group()`/`setPersonProperties()`, o efeito
prático continua idêntico ao `'never'` original — nenhum person profile é
criado. Autocapture/heatmaps/Web Vitals/Session Replay não exigem pessoa
identificada, então não há conflito com essa escolha.

**Habilitado nesta pre-sell:** autocapture, heatmaps, Web Vitals, Session
Replay (com `maskAllInputs`, sem captura de payload de rede, sem console
recording). **`outbound_hotmart` continua a métrica de conversão
canônica** — autocapture é contexto complementar, nunca a substitui.

**Deliberadamente mantido desligado**, mesmo o projeto permitindo:
console log recording (sem utilidade concreta aqui, risco de vazamento
acidental) e captura de payload de rede (request/response body).

## Privacidade / IP

✅ **Gate encerrado.** `anonymize_ips = true` confirmado no projeto
PostHog conectado (verificação externa, 2026-08-08). Formulação factual
(sem linguagem jurídica absoluta, sem afirmar "nenhum processamento de
IP"): o projeto está configurado para descartar/processar o IP do
visitante conforme essa opção — a requisição HTTP ainda carrega o IP até
o servidor do PostHog antes de qualquer transformação. Detalhe completo
em `docs/etapa_5_c_v1_contrato_tracking_microteste01.md`.

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
- Sampling de Session Replay (gravar 100% das sessões vs. amostra) não é
  configurado em código — é uma decisão econômica/de produto que depende
  de volume real de tráfego, recomendada mas não decidida nesta rodada
  (ver contrato, seção "Sampling / retenção"). Ajuste via configuração do
  projeto no PostHog antes de escalar tráfego pago.
- Nenhuma automação cria a campanha Google Ads — isso é manual, fora
  desta ferramenta, por design.
- Algumas páginas da documentação oficial retornaram conteúdo truncado
  nas consultas desta sessão (ver contrato, lista de fontes) — revalidar
  a doc completa antes do primeiro deploy com tráfego pago real.

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
