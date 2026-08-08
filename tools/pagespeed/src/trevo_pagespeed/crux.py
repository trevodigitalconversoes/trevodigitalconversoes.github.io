"""Extrai CruxResult de um CruxOutcome (client.py). Sem rede aqui."""

from __future__ import annotations

from .client import CruxOutcome
from .models import CruxResult

_CRUX_METRIC_KEYS = {
    "largest_contentful_paint": "LCP",
    "interaction_to_next_paint": "INP",
    "cumulative_layout_shift": "CLS",
    "first_contentful_paint": "FCP",
    "experimental_time_to_first_byte": "TTFB",
}


def extract_crux_result(outcome: CruxOutcome, *, target: str) -> CruxResult:
    if outcome.status != "PASS" or outcome.data is None:
        return CruxResult(target=target, status=outcome.status, error=outcome.error)

    record = outcome.data.get("record", {})
    metrics_raw = record.get("metrics", {})
    key = record.get("key", {})

    metrics: dict[str, dict] = {}
    for api_key, short_name in _CRUX_METRIC_KEYS.items():
        metric = metrics_raw.get(api_key)
        if metric is None:
            continue
        percentiles = metric.get("percentiles", {})
        metrics[short_name] = {
            "p75": percentiles.get("p75"),
            "histogram": metric.get("histogram"),
        }

    form_factor = key.get("formFactor")
    return CruxResult(
        target=target,
        status="PASS",
        metrics=metrics,
        form_factors=[form_factor] if form_factor else [],
        collection_period=record.get("collectionPeriod"),
        error=None,
    )
