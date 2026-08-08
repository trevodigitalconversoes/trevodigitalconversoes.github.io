from __future__ import annotations

from trevo_pagespeed.analyze import AnalysisResult, StrategySummary
from trevo_pagespeed.extract import extract_run_result
from trevo_pagespeed.report import build_summary_dict, render_csv_rows, render_dashboard_html, render_markdown_report
from trevo_pagespeed.stats import summarize


def _make_analysis(sample_lighthouse_json, config_key: str) -> AnalysisResult:
    run = extract_run_result(
        sample_lighthouse_json, run_index=1, strategy="mobile",
        requested_url="https://example.com", timestamp_utc="2026-08-08T12:00:00Z",
    )
    summary = StrategySummary(strategy="mobile", runs=[run])
    summary.score_summaries["performance"] = summarize([92.0], worst_is_max=False)
    summary.metric_summaries["LCP"] = summarize([2100.0])
    return AnalysisResult(
        url="https://example.com",
        runs_per_strategy=1,
        strategy_summaries={"mobile": summary},
        crux_page=None,
        crux_origin=None,
        findings=[],
    )


def test_build_summary_dict_has_verdict(sample_lighthouse_json):
    analysis = _make_analysis(sample_lighthouse_json, "AIzaFAKEKEY123")
    summary = build_summary_dict(analysis, {"commit_sha": "abc123"})
    assert summary["verdict"] in (
        "PAGESPEED_LAUNCH_READY",
        "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS",
        "PAGESPEED_FIX_BEFORE_LAUNCH",
        "PAGESPEED_BLOCKED",
    )
    assert summary["measurement_ok"] is True


def test_render_csv_rows_has_header_and_data(sample_lighthouse_json):
    analysis = _make_analysis(sample_lighthouse_json, "AIzaFAKEKEY123")
    rows = render_csv_rows(analysis)
    assert rows[0][0] == "strategy"
    assert rows[1][0] == "mobile"


def test_render_markdown_report_contains_verdict_and_no_secret(sample_lighthouse_json):
    analysis = _make_analysis(sample_lighthouse_json, "AIzaFAKEKEY123")
    md = render_markdown_report(analysis, {"commit_sha": "abc123", "generated_at_utc": "2026-08-08T12:00:00Z"})
    assert "## Veredito" in md
    assert "AIzaFAKEKEY123" not in md


def test_render_dashboard_html_has_no_secret_and_is_self_contained(sample_lighthouse_json):
    analysis = _make_analysis(sample_lighthouse_json, "AIzaFAKEKEY123")
    summary = build_summary_dict(analysis, {"commit_sha": "abc123"})
    dashboard = render_dashboard_html(summary)
    assert "AIzaFAKEKEY123" not in dashboard
    assert "<script src=" not in dashboard
    assert "cdn." not in dashboard.lower()


def test_summary_missing_metric_marked_not_available(sample_lighthouse_json):
    raw = {"lighthouseResult": {"audits": {}, "categories": {}}}
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    summary = StrategySummary(strategy="mobile", runs=[run])
    summary.score_summaries["performance"] = summarize([])
    analysis = AnalysisResult(
        url="u", runs_per_strategy=1, strategy_summaries={"mobile": summary},
        crux_page=None, crux_origin=None, findings=[],
    )
    md = render_markdown_report(analysis, {})
    assert "NAO DISPONIVEL NA VERSAO LIGHTHOUSE ATUAL" in md
