"""Extrai os campos de RunResult de um JSON bruto de `runPagespeed`. Nao
inventa metrica/audit que a API nao retornou -- se um audit esperado nao
existir na resposta, o campo correspondente fica None e quem monta o
relatorio deve registrar 'NAO DISPONIVEL NA VERSAO LIGHTHOUSE ATUAL' em vez
de tratar como erro (etapa 6 do runbook)."""

from __future__ import annotations

from .models import LcpElementInfo, MetricValue, Opportunity, RunResult

_SCORE_CATEGORY_KEYS = {
    "performance": "performance",
    "accessibility": "accessibility",
    "best-practices": "best-practices",
    "seo": "seo",
}

# audit_id -> chave curta usada no resto da ferramenta (relatorio/CSV).
_METRIC_AUDITS = {
    "first-contentful-paint": "FCP",
    "largest-contentful-paint": "LCP",
    "total-blocking-time": "TBT",
    "cumulative-layout-shift": "CLS",
    "speed-index": "Speed Index",
    "interactive": "TTI",
    "server-response-time": "TTFB",
    "total-byte-weight": "Total Byte Weight",
    "dom-size": "DOM Size",
    "mainthread-work-breakdown": "Main Thread Work",
    "bootup-time": "Bootup Time",
}

_OPPORTUNITY_AUDITS = {
    # Taxonomia classica (Lighthouse <= ~11).
    "render-blocking-resources",
    "unused-css-rules",
    "unused-javascript",
    "unminified-css",
    "unminified-javascript",
    "modern-image-formats",
    "uses-responsive-images",
    "efficient-animated-content",
    "uses-optimized-images",
    "uses-text-compression",
    "uses-rel-preconnect",
    "uses-rel-preload",
    "font-display",
    "critical-request-chains",
    "offscreen-images",
    "duplicated-javascript",
    "legacy-javascript",
    "preload-lcp-image",
    "third-party-summary",
    "image-size-responsive",
    "non-composited-animations",
    "uses-long-cache-ttl",
    # Taxonomia "Insights" (Lighthouse >= 12, confirmado na resposta real
    # da API em 2026-08-08 -- versao retornada foi 13.4.1). Os audits
    # antigos equivalentes deixaram de existir na resposta; mantemos
    # ambos os conjuntos para nao quebrar se a API voltar a taxonomia
    # classica em algum strategy/versao.
    "render-blocking-insight",
    "image-delivery-insight",
    "cache-insight",
    "legacy-javascript-insight",
    "duplicated-javascript-insight",
    "font-display-insight",
    "forced-reflow-insight",
    "third-parties-insight",
    "document-latency-insight",
    "network-dependency-tree-insight",
}

_DIAGNOSTIC_AUDITS = {
    "dom-size",
    "dom-size-insight",
    "mainthread-work-breakdown",
    "bootup-time",
    "network-requests",
    "network-rtt",
    "network-server-latency",
    "layout-shift-elements",
    "long-tasks",
    "no-document-write",
    "uses-passive-event-listeners",
    "largest-contentful-paint-element",
    "lcp-discovery-insight",
    "lcp-breakdown-insight",
    "cls-culprits-insight",
    "inp-breakdown-insight",
}


def _extract_scores(lighthouse_result: dict) -> dict[str, float | None]:
    categories = lighthouse_result.get("categories", {})
    scores: dict[str, float | None] = {}
    for api_key, our_key in _SCORE_CATEGORY_KEYS.items():
        cat = categories.get(api_key)
        if cat is None or cat.get("score") is None:
            scores[our_key] = None
        else:
            scores[our_key] = round(cat["score"] * 100, 1)
    return scores


def _extract_metrics(audits: dict) -> dict[str, MetricValue]:
    metrics: dict[str, MetricValue] = {}
    for audit_id, short_name in _METRIC_AUDITS.items():
        audit = audits.get(audit_id)
        if audit is None:
            continue
        metrics[short_name] = MetricValue(
            audit_id=audit_id,
            title=audit.get("title", audit_id),
            numeric_value=audit.get("numericValue"),
            numeric_unit=audit.get("numericUnit"),
            score=audit.get("score"),
            display_value=audit.get("displayValue"),
        )

    if "DOM Size" not in metrics:
        # Lighthouse >= 12 substituiu o audit 'dom-size' (com numericValue
        # direto) por 'dom-size-insight' (tabela de estatisticas). O
        # 'Total elements' esta sempre na primeira linha dessa tabela.
        insight = audits.get("dom-size-insight")
        if insight is not None:
            details = insight.get("details", {}) or {}
            for item in details.get("items", []):
                if isinstance(item, dict) and item.get("statistic") == "Total elements":
                    value = (item.get("value") or {}).get("value")
                    if value is not None:
                        metrics["DOM Size"] = MetricValue(
                            audit_id="dom-size-insight",
                            title="DOM Size (Total elements)",
                            numeric_value=value,
                            numeric_unit="element",
                            score=insight.get("score"),
                            display_value=str(value),
                        )
                    break
    return metrics


def _sum_item_field(details: dict, field: str) -> float | None:
    """Soma um campo numerico (ex.: wastedBytes/wastedMs) presente
    diretamente nos itens de `details.items`, quando o audit nao traz um
    total agregado (`overallSavingsMs`/`overallSavingsBytes`). Ainda e um
    valor que a propria API retornou -- so agregamos, nunca inventamos.
    Ignora itens que nao sejam dict ou que nao tenham o campo (ex.: linhas
    de checklist sem essa metrica)."""
    items = details.get("items")
    if not isinstance(items, list):
        return None
    total = 0.0
    found = False
    for item in items:
        if not isinstance(item, dict):
            continue
        value = item.get(field)
        if isinstance(value, (int, float)):
            total += value
            found = True
    return total if found else None


def _extract_opportunities(audits: dict, audit_ids: set[str]) -> list[Opportunity]:
    results = []
    for audit_id in audit_ids:
        audit = audits.get(audit_id)
        if audit is None:
            continue
        # Audits "informativos" (scoreDisplayMode == 'notApplicable' ou
        # 'informative' com score None) ainda sao relevantes para
        # diagnostico -- so pulamos os que nem rodaram (erro do proprio
        # Lighthouse), marcados como 'error'.
        if audit.get("scoreDisplayMode") == "error":
            continue
        details = audit.get("details", {}) or {}
        savings_ms = details.get("overallSavingsMs")
        savings_bytes = details.get("overallSavingsBytes")
        if savings_ms is None:
            savings_ms = _sum_item_field(details, "wastedMs")
        if savings_bytes is None:
            savings_bytes = _sum_item_field(details, "wastedBytes")
        results.append(
            Opportunity(
                audit_id=audit_id,
                title=audit.get("title", audit_id),
                score=audit.get("score"),
                display_value=audit.get("displayValue"),
                overall_savings_ms=savings_ms,
                overall_savings_bytes=savings_bytes,
                description=audit.get("description"),
            )
        )
    return results


def _extract_lcp_element(audits: dict) -> LcpElementInfo | None:
    """Tenta a taxonomia classica primeiro (`largest-contentful-paint-
    element`); se ausente (Lighthouse >= 12), procura o elemento dentro dos
    items de `lcp-discovery-insight`/`lcp-breakdown-insight` -- nesses
    audits `details.items` mistura linhas de checklist/tabela com um item
    que descreve o proprio elemento (tem `node` ou `snippet`/`path`)."""
    audit = audits.get("largest-contentful-paint-element")
    if audit is not None:
        details = audit.get("details", {}) or {}
        items = details.get("items", [])
        if items:
            first = items[0]
            node = first.get("node") or {}
            return LcpElementInfo(
                node_snippet=node.get("snippet"),
                node_selector=node.get("selector"),
                url=first.get("url"),
            )

    for audit_id in ("lcp-discovery-insight", "lcp-breakdown-insight"):
        audit = audits.get(audit_id)
        if audit is None:
            continue
        details = audit.get("details", {}) or {}
        for item in details.get("items", []):
            if not isinstance(item, dict):
                continue
            node = item.get("node") or {}
            # A forma do item varia por audit/versao: o seletor e o
            # snippet podem vir direto no item (lcp-discovery-insight) ou
            # aninhados em 'node' (lcp-breakdown-insight, taxonomia
            # classica). Tentamos ambos.
            selector = item.get("selector") or node.get("selector")
            snippet = item.get("snippet") or node.get("snippet")
            if selector or snippet:
                return LcpElementInfo(
                    node_snippet=snippet,
                    node_selector=selector,
                    url=item.get("url") or node.get("url"),
                )
    return None


def _total_requests(audits: dict) -> int | None:
    audit = audits.get("network-requests")
    if audit is None:
        return None
    details = audit.get("details", {}) or {}
    items = details.get("items")
    if items is None:
        return None
    return len(items)


def extract_run_result(
    raw: dict, *, run_index: int, strategy: str, requested_url: str, timestamp_utc: str
) -> RunResult:
    lighthouse_result = raw.get("lighthouseResult", {}) or {}
    audits = lighthouse_result.get("audits", {}) or {}

    return RunResult(
        run_index=run_index,
        strategy=strategy,
        requested_url=requested_url,
        timestamp_utc=timestamp_utc,
        final_url=lighthouse_result.get("finalUrl") or lighthouse_result.get("finalDisplayedUrl"),
        lighthouse_version=lighthouse_result.get("lighthouseVersion"),
        fetch_time=lighthouse_result.get("fetchTime"),
        warnings=list(lighthouse_result.get("runWarnings", [])),
        scores=_extract_scores(lighthouse_result),
        metrics=_extract_metrics(audits),
        opportunities=_extract_opportunities(audits, _OPPORTUNITY_AUDITS),
        diagnostics=_extract_opportunities(audits, _DIAGNOSTIC_AUDITS),
        lcp_element=_extract_lcp_element(audits),
        environment=lighthouse_result.get("environment"),
        total_byte_weight_bytes=(audits.get("total-byte-weight") or {}).get("numericValue"),
        total_requests=_total_requests(audits),
    )
