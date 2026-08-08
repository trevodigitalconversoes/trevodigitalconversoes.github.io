"""Monta a config publica injetada em assets/js/tracking-config.generated.js.

O POSTHOG_PROJECT_TOKEN aparece aqui de proposito -- ver
tools/tracking/README.md ("Project token x Personal API Key"). Este
modulo nunca lida com Personal API Key.
"""

from __future__ import annotations

from .config import Config
from .params import ALLOWED_CAMPAIGN_PARAMS

EXPERIMENT_ID = "mt01"
PRODUCT_SLUG = "fotografia-presets-lightroom"
HOTLINK_BASE = "https://go.hotmart.com/V106592210H"

# Opcoes de posthog.init() para este microteste. Revalidado em 2026-08-08
# apos decisao do usuario de habilitar progressivamente Product Analytics/
# Web Analytics/autocapture/heatmaps/Web Vitals/Session Replay -- ver
# tools/tracking/README.md ("Historico da decisao") e
# docs/etapa_5_c_v1_contrato_tracking_microteste01.md para o registro
# completo e as fontes oficiais consultadas.
#
# `person_profiles: 'never'` foi revalidado nesta rodada: a documentacao
# atual do posthog-js (posthog.com/docs/data/anonymous-vs-identified-events,
# consultada em 2026-08-08) so lista `'identified_only'` (default
# recomendado) e `'always'` -- `'never'` nao aparece mais como valor
# suportado. Mantido `'identified_only'`: como este projeto NUNCA chama
# identify()/alias()/group()/setPersonProperties(), nenhum person profile
# e criado de qualquer forma -- o efeito pratico e identico ao `'never'`
# original. Autocapture/heatmaps/Session Replay/Web Vitals nao exigem
# pessoa identificada (anexam a um distinct_id/sessao anonimos), entao
# nao ha conflito com essa escolha.
POSTHOG_INIT_OPTIONS = {
    "person_profiles": "identified_only",
    "autocapture": True,
    "capture_pageview": True,
    "capture_pageleave": True,
    "disable_session_recording": False,
    "disable_persistence": False,
    "save_campaign_params": True,
    "save_referrer": False,
    "debug": False,
    # Web Vitals autocapture -- observacao de campo (real user monitoring),
    # complementar ao PageSpeed/Lighthouse (laboratorio). Nunca substitui
    # o baseline PRE/POST_TRACKING do tools/pagespeed/.
    "capture_performance": {"web_vitals": True},
    # Nome atual confirmado em posthog.com/docs/references/posthog-js/
    # types/PostHogConfig em 2026-08-08 ('enable_heatmaps' aparece como
    # nome legado/deprecado em outras paginas da doc).
    "capture_heatmaps": True,
    # Decisao explicita: o projeto PostHog permite console recording
    # (capture_console_log_opt_in=true a nivel de projeto), mas nao ha
    # utilidade concreta para isso nesta pre-sell e o risco de vazar algo
    # inesperado no console (mesmo sem PII conhecida hoje) supera o
    # beneficio. Mantido desligado para este consumidor especificamente
    # -- nao mudamos a configuracao global do projeto.
    "enable_recording_console_log": False,
    # Session Replay: input fields (email/senha/etc.) ja sao mascarados
    # por padrao pelo SDK (posthog.com/docs/session-replay/privacy,
    # 2026-08-08); `maskAllInputs: True` aqui e explicito por escolha do
    # runbook ("configurar explicitamente em vez de depender so do
    # default implicito"), nao uma mudanca de comportamento. Texto geral
    # da pagina NAO e mascarado por padrao -- aceitavel aqui porque a
    # pre-sell nao tem formulario/checkout e todo o texto e copy publica.
    # Network payload capture (request/response bodies) e deliberadamente
    # NAO habilitado -- e opt-in na doc oficial e permanece no estado
    # default (desligado), preservando `session_recording_network_
    # payload_capture_config = null` observado no projeto.
    "session_recording": {"maskAllInputs": True},
}


def build_public_config(config: Config) -> dict:
    """Retorna o dict que vira `window.__TREVO_TRACKING_CONFIG__` no
    JavaScript publico. Levanta ValueError se o token estiver ausente --
    quem chama (etapa_5_a) deve checar `config.has_token` ANTES de chegar
    aqui e nunca gerar um arquivo publico com token vazio."""
    if not config.has_token:
        raise ValueError("POSTHOG_PROJECT_TOKEN ausente -- nao gerar config publica sem token")

    return {
        "posthogProjectToken": config.posthog_project_token,
        "posthogHost": config.posthog_host,
        "posthogInitOptions": dict(POSTHOG_INIT_OPTIONS),
        "experimentId": EXPERIMENT_ID,
        "productSlug": PRODUCT_SLUG,
        "hotlinkBase": HOTLINK_BASE,
        "allowedCampaignParams": sorted(ALLOWED_CAMPAIGN_PARAMS),
    }
