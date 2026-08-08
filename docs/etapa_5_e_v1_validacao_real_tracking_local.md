# Etapa 5e — Primeira validação real do tracking (local, sem deploy)

Evidência sanitizada da primeira execução real do SDK PostHog com o
Project Token real, feita localmente (`http://localhost:8080`, servidor
estático) antes de qualquer deploy/merge. Nenhum token aparece neste
documento.

## Metadados

- **Data/hora (UTC):** 2026-08-08, ~18:39–19:10
- **Commit base:** `0c94742` (branch `feat/tracking-microteste01-fotografia`)
- **`qa_run_id`:** `qa_mt01_20260808_183941`
- **`traffic_type`:** `qa`
- **SDK PostHog (posthog-js):** `1.414.0`
- **Host confirmado no client:** `https://us.i.posthog.com`

## Mecanismo do `qa_run_id`

Não foi adicionado ao código do produto. Foi injetado manualmente via
DevTools (`posthog.register({...})`/`posthog.capture(...)` direto no
console do navegador) só durante esta sessão de QA local — não existe
nenhum parâmetro de URL nem lógica no `assets/js/etapa_5_d_v1_tracking.js`
para isso. Documentado aqui por transparência, conforme pedido.

## O que foi confirmado

| Item | Resultado |
|---|---|
| `.env` carregado | PASS — `POSTHOG_PROJECT_TOKEN` lido, nunca impresso pela ferramenta |
| Config pública gerada | PASS — `assets/js/tracking-config.generated.js`, token no formato esperado (`phc_...`), sem Personal API Key |
| SDK PostHog inicializa | PASS — `window.posthog.__loaded === true`, sem exceção |
| Evento capturado internamente (`eventCaptured`) | PASS — confirmado via listener `posthog.on('eventCaptured', ...)` |
| `$pageview`/pageview manual | PASS — capturado internamente com propriedades esperadas |
| `outbound_hotmart` no clique do CTA | PASS — exatamente 1 evento, propriedades corretas (ver abaixo) |
| `$autocapture` no clique do CTA | PASS — 1 evento, `$el_text` = copy pública do botão, sem dado sensível |
| Session Replay iniciado | PASS — `posthog.sessionRecordingStarted() === true`, evento `$snapshot` observado |
| `$pageleave` | PASS — observado ao simular saída de página |
| Web Vitals | **CAPABILITY_READY, não observado** — `$web_vitals_enabled_server_side: true` confirmado na propriedade do evento, módulo carregado, mas nenhum evento de métrica (LCP/CLS) chegou a ser emitido na janela síncrona desta sessão de QA (finalização real de LCP depende de navegação/idle mais longos que o ambiente de teste permitiu). Não declarado como validado por ausência de evidência de ingestão. |
| Heatmaps | **CAPABILITY_READY** — módulo `posthog.heatmaps` presente e carregado; população real do heatmap requer mais dados/sessões, não exigida nesta rodada |
| `person_profiles`/identificação | PASS — `$is_identified: false`, `$process_person_profile: false` no evento capturado; nenhuma chamada a `identify()`/`alias()`/`group()` existe no código (confirmado estaticamente e reforçado aqui) |
| Whitelist / sanitização de `$current_url` | **PASS** — URL de teste incluía `parametro_desconhecido=NAO_DEVE_IR`; o `$current_url` capturado (via `before_send`) **não contém** esse parâmetro, só os da whitelist |
| Resiliência (CTA sem PostHog) | PASS — já demonstrado na rodada anterior deste PR (config ausente → `href` permanece o HotLink base, zero erro) e reforçado pelos testes automatizados (`test_early_return_when_config_missing`, `test_cta_href_is_rewritten_before_any_network_dependent_step`) |
| Console recording da pre-sell | PASS (confirmado desligado) — `enable_recording_console_log: false` no config aplicado |
| Captura de payload de rede | PASS (confirmado não habilitada) — nenhuma chave de config relacionada presente |
| Personal API Key no cliente | PASS — inspecionado `tracking-config.generated.js`: um único campo de token (`posthogProjectToken`), formato `phc_...`, nenhum segundo campo tipo chave/segredo |

## Propriedades observadas em `outbound_hotmart` (QA)

`cta_location=hero`, `product_slug=fotografia-presets-lightroom`,
`experiment_id=mt01`, `creative_code=est01`, `utm_source=google`,
`gclid=QA-NAO-REAL`, `campaign_id=111111` (e demais UTMs/IDs presentes na
URL de teste) — nenhum dado pessoal.

## HotLink/SRC/UTM observados

`href` do CTA, já reescrito no DOM:
`https://go.hotmart.com/V106592210H?src=g%7Cmt01%7Cest01&utm_source=google&utm_medium=cpc&utm_campaign=qa-mt01-foto18&utm_content=est01`
— `campaign_id`/`ad_group_id`/`ad_id`/`device`/`network`/`gclid`
corretamente **ausentes** do link (ficam só no evento PostHog). Nenhuma
compra foi realizada; nenhuma navegação real até o checkout Hotmart
ocorreu.

## Erro de execução (registrado por transparência)

Durante a inspeção manual de um evento capturado via DevTools, um comando
imprimiu a propriedade automática `token` (que o próprio SDK do PostHog
anexa a cada evento, igual ao Project Token configurado) sem mascará-la
antes — violando a instrução explícita de nunca exibir esse valor. Todos
os comandos seguintes passaram a mascarar esse campo antes de qualquer
output. Como se trata do mesmo Project Token que já está, por design,
publicamente embutido em `assets/js/tracking-config.generated.js` (token
de ingestão do SDK web, não uma Personal API Key), isso não constitui uma
nova exposição de segredo além do que já será commitado propositalmente
— mas é um erro de processo real, registrado aqui sem omissão.

## Gaps não bloqueantes

- Web Vitals: capacidade confirmada habilitada, evento não observado
  nesta janela de QA síncrona (ver acima).
- Heatmap populado: não aplicável ainda (precisa de volume real de
  sessões).
- Verificação independente da ingestão pelo lado do PostHog (dashboard/
  API) não foi feita nesta execução — recomendada como próximo passo
  antes do merge.
