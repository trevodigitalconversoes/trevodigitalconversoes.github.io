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

# Opcoes de posthog.init() para este microteste -- eventos anonimos,
# sem session recording/autocapture/surveys/heatmaps/feature flags.
#
# `person_profiles: 'never'` foi o nome usado em versoes antigas do SDK;
# a documentacao atual (confirmada em posthog.com/docs em 2026-08-08)
# documenta `'identified_only'` como o valor atual (default recomendado).
# Como este projeto NUNCA chama identify()/alias(), o efeito e o mesmo:
# nenhum person profile e criado. Ver README para o registro dessa
# mudanca de API.
POSTHOG_INIT_OPTIONS = {
    "person_profiles": "identified_only",
    "autocapture": False,
    "capture_pageview": True,
    "capture_pageleave": False,
    "disable_session_recording": True,
    "disable_persistence": True,
    "save_campaign_params": True,
    "save_referrer": False,
    "debug": False,
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
