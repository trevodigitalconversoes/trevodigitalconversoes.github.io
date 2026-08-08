"""Orquestra N runs PageSpeed por strategy + consulta CrUX (page/origin) e
monta o resumo estatistico + achados. Sem I/O de arquivo aqui -- isso fica
em report.py/cli.py, para que este modulo seja facil de testar com
mocks."""

from __future__ import annotations

from dataclasses import dataclass, field

from .client import PageSpeedClient
from .crux import extract_crux_result
from .extract import extract_run_result
from .findings import Finding, classify_category_score, classify_lcp, classify_opportunity, sort_findings
from .models import CruxResult, RunResult
from .stats import Summary, summarize

CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]
STRATEGIES = ["mobile", "desktop"]


@dataclass
class StrategySummary:
    strategy: str
    runs: list[RunResult]
    score_summaries: dict[str, Summary] = field(default_factory=dict)
    metric_summaries: dict[str, Summary] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    url: str
    runs_per_strategy: int
    strategy_summaries: dict[str, StrategySummary]
    crux_page: CruxResult | None
    crux_origin: CruxResult | None
    findings: list[Finding]


def run_analysis(
    client: PageSpeedClient,
    url: str,
    *,
    runs_per_strategy: int,
    now_fn,
    sleep_fn,
    inter_call_delay_seconds: float = 2.0,
    include_crux: bool = True,
) -> AnalysisResult:
    strategy_summaries: dict[str, StrategySummary] = {}
    all_findings: list[Finding] = []

    for strategy in STRATEGIES:
        runs: list[RunResult] = []
        for i in range(runs_per_strategy):
            timestamp = now_fn().isoformat()
            try:
                raw = client.run_pagespeed(url, strategy, CATEGORIES)
                run = extract_run_result(
                    raw,
                    run_index=i + 1,
                    strategy=strategy,
                    requested_url=url,
                    timestamp_utc=timestamp,
                )
            except Exception as exc:  # noqa: BLE001 - registrado, nunca mascarado
                run = RunResult(
                    run_index=i + 1,
                    strategy=strategy,
                    requested_url=url,
                    timestamp_utc=timestamp,
                    final_url=None,
                    lighthouse_version=None,
                    fetch_time=None,
                    warnings=[],
                    scores={},
                    metrics={},
                    opportunities=[],
                    diagnostics=[],
                    lcp_element=None,
                    environment=None,
                    total_byte_weight_bytes=None,
                    total_requests=None,
                    error=str(exc),
                )
            runs.append(run)
            is_last_call = strategy == STRATEGIES[-1] and i == runs_per_strategy - 1
            if not is_last_call:
                sleep_fn(inter_call_delay_seconds)

        summary = StrategySummary(strategy=strategy, runs=runs)
        ok_runs = [r for r in runs if r.ok]

        for category in ["performance", "accessibility", "best-practices", "seo"]:
            values = [r.scores.get(category) for r in ok_runs]
            values = [v for v in values if v is not None]
            score_summary = summarize(values, worst_is_max=False)
            summary.score_summaries[category] = score_summary
            finding = classify_category_score(category, strategy, score_summary)
            if finding:
                all_findings.append(finding)

        for metric_name in ["FCP", "LCP", "TBT", "CLS", "Speed Index", "TTI", "TTFB"]:
            values = [
                r.metrics[metric_name].numeric_value
                for r in ok_runs
                if metric_name in r.metrics and r.metrics[metric_name].numeric_value is not None
            ]
            summary.metric_summaries[metric_name] = summarize(values, worst_is_max=True)

        lcp_summary = summary.metric_summaries.get("LCP")
        lcp_finding = classify_lcp(strategy, lcp_summary.median if lcp_summary else None)
        if lcp_finding:
            all_findings.append(lcp_finding)

        seen_opp_ids: set[str] = set()
        for run in ok_runs:
            for opp in run.opportunities:
                if opp.audit_id in seen_opp_ids:
                    continue
                seen_opp_ids.add(opp.audit_id)
                finding = classify_opportunity(opp, strategy=strategy, category="performance")
                if finding:
                    all_findings.append(finding)

        strategy_summaries[strategy] = summary

    crux_page = None
    crux_origin = None
    if include_crux:
        page_outcome = client.query_crux(url=url)
        crux_page = extract_crux_result(page_outcome, target="page")
        from urllib.parse import urlsplit

        origin = f"{urlsplit(url).scheme}://{urlsplit(url).netloc}"
        origin_outcome = client.query_crux(origin=origin)
        crux_origin = extract_crux_result(origin_outcome, target="origin")

    return AnalysisResult(
        url=url,
        runs_per_strategy=runs_per_strategy,
        strategy_summaries=strategy_summaries,
        crux_page=crux_page,
        crux_origin=crux_origin,
        findings=sort_findings(all_findings),
    )
