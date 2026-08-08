"""Whitelist de parametros de campanha (etapa 10 do runbook). Usada tanto
pelo QA/testes em Python quanto espelhada no JS publico
(assets/js/etapa_5_d_v1_tracking.js) -- qualquer mudanca aqui deve ser
replicada la, ver README."""

from __future__ import annotations

ALLOWED_CAMPAIGN_PARAMS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_content",
        "utm_term",
        "campaign_id",
        "ad_group_id",
        "ad_id",
        "device",
        "network",
        "matchtype",
        "gclid",
        "gbraid",
        "wbraid",
        "gad_source",
    }
)

# Subconjunto que e propagado ao HotLink Hotmart (etapa 13 do runbook).
# Identificadores exclusivos do Google (gclid, ad_id, ad_group_id,
# campaign_id) ficam apenas no PostHog -- Hotmart nao os documenta e nao
# ha necessidade comprovada de envia-los.
HOTMART_FORWARDED_PARAMS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")


def sanitize_query_params(params: dict[str, str]) -> dict[str, str]:
    """Retorna somente os pares cuja chave esta na whitelist. Parametros
    desconhecidos sao descartados silenciosamente (nao viram propriedade
    de analytics nem sao repassados a lugar nenhum)."""
    return {k: v for k, v in params.items() if k in ALLOWED_CAMPAIGN_PARAMS}
