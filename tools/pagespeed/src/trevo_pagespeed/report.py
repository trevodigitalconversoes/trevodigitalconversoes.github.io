"""Monta o resumo estruturado (JSON), o relatorio Markdown, as linhas de
CSV e o dashboard HTML autocontido a partir de um AnalysisResult. Sem rede,
sem I/O de arquivo -- quem grava em disco e o cli.py."""

from __future__ import annotations

import html
from dataclasses import asdict
from typing import Any

from .analyze import AnalysisResult
from .findings import Finding
from .models import CruxResult, MetricValue, Opportunity, RunResult
from .stats import Summary
from .verdict import decide_verdict


def _summary_to_dict(s: Summary) -> dict[str, Any]:
    return {"n": s.n, "min": s.minimum, "max": s.maximum, "mean": s.mean, "median": s.median, "worst": s.worst}


def _run_to_dict(r: RunResult) -> dict[str, Any]:
    return {
        "run_index": r.run_index,
        "strategy": r.strategy,
        "requested_url": r.requested_url,
        "final_url": r.final_url,
        "timestamp_utc": r.timestamp_utc,
        "lighthouse_version": r.lighthouse_version,
        "fetch_time": r.fetch_time,
        "warnings": r.warnings,
        "scores": r.scores,
        "metrics": {
            k: {
                "numeric_value": v.numeric_value,
                "numeric_unit": v.numeric_unit,
                "score": v.score,
                "display_value": v.display_value,
            }
            for k, v in r.metrics.items()
        },
        "total_byte_weight_bytes": r.total_byte_weight_bytes,
        "total_requests": r.total_requests,
        "lcp_element": asdict(r.lcp_element) if r.lcp_element else None,
        "error": r.error,
        "ok": r.ok,
    }


def _crux_to_dict(c: CruxResult | None) -> dict[str, Any] | None:
    if c is None:
        return None
    return {
        "target": c.target,
        "status": c.status,
        "metrics": c.metrics,
        "form_factors": c.form_factors,
        "collection_period": c.collection_period,
        "error": c.error,
    }


def _finding_to_dict(f: Finding) -> dict[str, Any]:
    return {
        "severity": f.severity,
        "category": f.category,
        "strategy": f.strategy,
        "audit_id": f.audit_id,
        "title": f.title,
        "evidence": f.evidence,
        "impact": f.impact,
        "probable_cause": f.probable_cause,
        "recommendation": f.recommendation,
        "estimated_savings_ms": f.estimated_savings_ms,
        "estimated_savings_bytes": f.estimated_savings_bytes,
    }


def build_summary_dict(analysis: AnalysisResult, meta: dict[str, Any]) -> dict[str, Any]:
    measurement_ok = any(
        any(r.ok for r in s.runs) for s in analysis.strategy_summaries.values()
    )
    verdict = decide_verdict(analysis.findings, measurement_ok=measurement_ok)
    return {
        "meta": meta,
        "url": analysis.url,
        "runs_per_strategy": analysis.runs_per_strategy,
        "measurement_ok": measurement_ok,
        "strategies": {
            strategy: {
                "runs": [_run_to_dict(r) for r in s.runs],
                "score_summaries": {k: _summary_to_dict(v) for k, v in s.score_summaries.items()},
                "metric_summaries": {k: _summary_to_dict(v) for k, v in s.metric_summaries.items()},
            }
            for strategy, s in analysis.strategy_summaries.items()
        },
        "crux_page": _crux_to_dict(analysis.crux_page),
        "crux_origin": _crux_to_dict(analysis.crux_origin),
        "findings": [_finding_to_dict(f) for f in analysis.findings],
        "verdict": verdict,
    }


def render_csv_rows(analysis: AnalysisResult) -> list[list[str]]:
    header = [
        "strategy",
        "run_index",
        "ok",
        "performance",
        "accessibility",
        "best-practices",
        "seo",
        "FCP_ms",
        "LCP_ms",
        "TBT_ms",
        "CLS",
        "SpeedIndex_ms",
        "TTFB_ms",
        "total_byte_weight_bytes",
        "total_requests",
    ]
    rows = [header]
    for strategy, s in analysis.strategy_summaries.items():
        for r in s.runs:
            def m(name: str) -> str:
                mv: MetricValue | None = r.metrics.get(name)
                return "" if mv is None or mv.numeric_value is None else str(mv.numeric_value)

            rows.append(
                [
                    strategy,
                    str(r.run_index),
                    str(r.ok),
                    str(r.scores.get("performance", "")),
                    str(r.scores.get("accessibility", "")),
                    str(r.scores.get("best-practices", "")),
                    str(r.scores.get("seo", "")),
                    m("FCP"),
                    m("LCP"),
                    m("TBT"),
                    m("CLS"),
                    m("Speed Index"),
                    m("TTFB"),
                    "" if r.total_byte_weight_bytes is None else str(r.total_byte_weight_bytes),
                    "" if r.total_requests is None else str(r.total_requests),
                ]
            )
    return rows


def _fmt(v: Any, unit: str = "") -> str:
    if v is None:
        return "NAO DISPONIVEL NA VERSAO LIGHTHOUSE ATUAL"
    if isinstance(v, float):
        return f"{v:.1f}{unit}"
    return f"{v}{unit}"


def render_markdown_report(analysis: AnalysisResult, meta: dict[str, Any]) -> str:
    verdict = decide_verdict(
        analysis.findings,
        measurement_ok=any(any(r.ok for r in s.runs) for s in analysis.strategy_summaries.values()),
    )

    lines: list[str] = []
    lines.append(f"# Relatorio de Performance — {analysis.url}")
    lines.append("")
    lines.append("## 1-9. Objetivo, metodologia e execucao")
    lines.append(f"- **URL:** {analysis.url}")
    lines.append(f"- **Commit:** `{meta.get('commit_sha', 'desconhecido')}`")
    lines.append(f"- **Data/hora (UTC):** {meta.get('generated_at_utc', 'desconhecido')}")
    lines.append(f"- **API:** PageSpeed Insights API v5 (`runPagespeed`), Chrome UX Report API v1")
    lines.append(f"- **Runs por strategy:** {analysis.runs_per_strategy}")
    lines.append(
        f"- **Baseline:** {meta.get('baseline_label', 'PRE_TRACKING_BASELINE')} "
        "(antes de adicionar PostHog/tracking)"
    )
    lines.append("")

    lines.append("## Scores (mediana / pior run, 0-100)")
    lines.append("")
    lines.append("| Strategy | Categoria | Mediana | Pior | Min | Max |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for strategy, s in analysis.strategy_summaries.items():
        for category, summ in s.score_summaries.items():
            lines.append(
                f"| {strategy} | {category} | {_fmt(summ.median)} | {_fmt(summ.worst)} "
                f"| {_fmt(summ.minimum)} | {_fmt(summ.maximum)} |"
            )
    lines.append("")

    lines.append("## Metricas de laboratorio (mediana / pior run)")
    lines.append("")
    lines.append("| Strategy | Metrica | Mediana | Pior run | Unidade |")
    lines.append("|---|---|---:|---:|---|")
    for strategy, s in analysis.strategy_summaries.items():
        for metric_name, summ in s.metric_summaries.items():
            unit = "ms" if metric_name != "CLS" else ""
            lines.append(
                f"| {strategy} | {metric_name} | {_fmt(summ.median, unit)} | {_fmt(summ.worst, unit)} | {unit or 'score'} |"
            )
    lines.append("")

    lines.append("## Comparacao mobile x desktop")
    lines.append("")
    lines.append("| Metrica | Mobile mediana | Mobile pior | Desktop mediana | Desktop pior |")
    lines.append("|---|---:|---:|---:|---:|")
    mobile = analysis.strategy_summaries.get("mobile")
    desktop = analysis.strategy_summaries.get("desktop")
    compare_metrics = ["performance", "FCP", "LCP", "TBT", "CLS", "Speed Index"]
    for metric in compare_metrics:
        m_summary = None
        d_summary = None
        if mobile:
            m_summary = mobile.score_summaries.get(metric) or mobile.metric_summaries.get(metric)
        if desktop:
            d_summary = desktop.score_summaries.get(metric) or desktop.metric_summaries.get(metric)
        lines.append(
            f"| {metric} | {_fmt(m_summary.median if m_summary else None)} "
            f"| {_fmt(m_summary.worst if m_summary else None)} "
            f"| {_fmt(d_summary.median if d_summary else None)} "
            f"| {_fmt(d_summary.worst if d_summary else None)} |"
        )
    lines.append("")
    lines.append("_Mobile tem prioridade na decisao de lancamento._")
    lines.append("")

    lines.append("## Core Web Vitals (field data / CrUX)")
    lines.append("")
    for label, crux in (("Page", analysis.crux_page), ("Origin", analysis.crux_origin)):
        if crux is None:
            lines.append(f"- **{label}:** consulta CrUX nao executada nesta rodada")
            continue
        if crux.status == "PASS":
            metric_bits = ", ".join(
                f"{k}(p75)={v.get('p75')}" for k, v in crux.metrics.items()
            )
            lines.append(f"- **{label}:** dados reais disponiveis — {metric_bits or 'sem metricas retornadas'}")
        else:
            token = "CRUX_PAGE_DATA_NOT_AVAILABLE" if label == "Page" else "CRUX_ORIGIN_DATA_NOT_AVAILABLE"
            reason = crux.status
            lines.append(f"- **{label}:** `{token}` (status={reason}) — {crux.error or 'sem detalhe adicional'}")
    lines.append("")
    lines.append(
        "_TBT (lab) e uma metrica de diagnostico de responsividade; nao substitui INP real "
        "(field data), que so vem do CrUX._"
    )
    lines.append("")

    lines.append("## Elemento LCP")
    lines.append("")
    for strategy in ("mobile", "desktop"):
        s = analysis.strategy_summaries.get(strategy)
        if not s or not s.runs:
            continue
        run_with_lcp = next((r for r in s.runs if r.lcp_element), None)
        if run_with_lcp and run_with_lcp.lcp_element:
            el = run_with_lcp.lcp_element
            lines.append(f"- **{strategy}:** `{el.node_selector or 'seletor indisponivel'}`"
                         f" — asset: {el.url or 'n/a'}")
        else:
            lines.append(f"- **{strategy}:** elemento LCP nao identificado na resposta")
    lines.append("")

    lines.append("## Achados por severidade")
    lines.append("")
    for severity in ("P0", "P1", "P2", "INFO"):
        subset = [f for f in analysis.findings if f.severity == severity]
        lines.append(f"### {severity} ({len(subset)})")
        if not subset:
            lines.append("_Nenhum achado nesta severidade._")
        for f in subset:
            savings = ""
            if f.estimated_savings_ms:
                savings = f" — economia estimada: {f.estimated_savings_ms:.0f} ms"
            lines.append(
                f"- **[{f.strategy}] {f.title}** (`{f.audit_id}`){savings}\n"
                f"  - Evidencia: {f.evidence}\n"
                f"  - Impacto: {f.impact}\n"
                f"  - Recomendacao: {f.recommendation}"
            )
        lines.append("")

    lines.append("## Baseline")
    lines.append("")
    lines.append(f"`{meta.get('baseline_label', 'PRE_TRACKING_BASELINE')}_CAPTURED`")
    lines.append("")

    lines.append("## Veredito")
    lines.append("")
    lines.append(f"**{verdict}**")
    lines.append("")

    return "\n".join(lines)


def render_dashboard_html(summary: dict[str, Any]) -> str:
    """HTML autocontido (sem JS pesado, sem CDN, sem segredo). Barras
    simples via CSS -- suficiente para visualizar scores/mediana/pior run
    por strategy e a lista de achados por severidade."""

    def esc(s: Any) -> str:
        return html.escape(str(s))

    verdict = esc(summary.get("verdict", ""))
    url = esc(summary.get("url", ""))

    score_rows = []
    for strategy, data in summary.get("strategies", {}).items():
        for category, s in data.get("score_summaries", {}).items():
            median = s.get("median")
            worst = s.get("worst")
            width = 0 if median is None else max(2, min(100, median))
            score_rows.append(
                f'<div class="bar-row"><span class="bar-label">{esc(strategy)} / {esc(category)}</span>'
                f'<div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div>'
                f'<span class="bar-value">mediana {esc(median)} · pior {esc(worst)}</span></div>'
            )

    severity_colors = {"P0": "#d13438", "P1": "#e8a33d", "P2": "#3a8ee6", "INFO": "#6b7280"}
    findings_html = []
    for severity in ("P0", "P1", "P2", "INFO"):
        subset = [f for f in summary.get("findings", []) if f["severity"] == severity]
        color = severity_colors[severity]
        items = "".join(
            f'<li><strong>[{esc(f["strategy"])}] {esc(f["title"])}</strong><br>'
            f'<span class="muted">{esc(f["evidence"])}</span></li>'
            for f in subset
        )
        empty_marker = '<li class="muted">Nenhum achado</li>'
        list_content = items or empty_marker
        findings_html.append(
            f'<section class="severity-block"><h3 style="color:{color}">{severity} ({len(subset)})</h3>'
            f'<ul>{list_content}</ul></section>'
        )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Dashboard PageSpeed — {url}</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 24px;
         background: #0f1115; color: #e6e8eb; }}
  @media (prefers-color-scheme: light) {{
    body {{ background: #f7f7f8; color: #1a1a1a; }}
  }}
  h1 {{ font-size: 1.4rem; }}
  .verdict {{ display: inline-block; padding: 6px 14px; border-radius: 999px;
             background: #1f6feb22; border: 1px solid #1f6feb; font-weight: 600; }}
  .bar-row {{ display: flex; align-items: center; gap: 12px; margin: 8px 0; }}
  .bar-label {{ width: 220px; font-size: 0.85rem; }}
  .bar-track {{ flex: 1; background: #2a2d34; border-radius: 4px; height: 10px; overflow: hidden; }}
  .bar-fill {{ background: #3fb950; height: 100%; }}
  .bar-value {{ font-size: 0.8rem; color: #9aa0a6; white-space: nowrap; }}
  .severity-block {{ margin-bottom: 16px; }}
  .muted {{ color: #9aa0a6; font-size: 0.85rem; }}
  ul {{ padding-left: 18px; }}
  li {{ margin-bottom: 8px; }}
</style>
</head>
<body>
  <h1>Dashboard PageSpeed — {url}</h1>
  <p class="verdict">{verdict}</p>
  <h2>Scores por strategy/categoria</h2>
  {"".join(score_rows) or '<p class="muted">Sem dados.</p>'}
  <h2>Achados por severidade</h2>
  {"".join(findings_html)}
</body>
</html>
"""
