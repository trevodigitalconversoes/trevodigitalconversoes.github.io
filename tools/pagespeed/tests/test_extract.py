from __future__ import annotations

import pytest

from trevo_pagespeed.extract import extract_run_result


def test_extract_scores(sample_lighthouse_json):
    run = extract_run_result(
        sample_lighthouse_json,
        run_index=1,
        strategy="mobile",
        requested_url="https://example.com",
        timestamp_utc="2026-08-08T12:00:00Z",
    )
    assert run.scores["performance"] == 92.0
    assert run.scores["accessibility"] == 98.0
    assert run.scores["best-practices"] == 100.0
    assert run.scores["seo"] == 100.0


def test_extract_metrics_present(sample_lighthouse_json):
    run = extract_run_result(
        sample_lighthouse_json, run_index=1, strategy="mobile",
        requested_url="u", timestamp_utc="t",
    )
    assert run.metrics["LCP"].numeric_value == 2100.0
    assert run.metrics["FCP"].numeric_value == 1200.5


def test_extract_metric_missing_from_response_is_absent():
    raw = {"lighthouseResult": {"audits": {}, "categories": {}}}
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    assert "TTI" not in run.metrics
    assert run.scores["performance"] is None


def test_extract_lcp_element(sample_lighthouse_json):
    run = extract_run_result(
        sample_lighthouse_json, run_index=1, strategy="mobile",
        requested_url="u", timestamp_utc="t",
    )
    assert run.lcp_element is not None
    assert "mockup-hero-04.jpg" in (run.lcp_element.url or "")


def test_extract_total_requests(sample_lighthouse_json):
    run = extract_run_result(
        sample_lighthouse_json, run_index=1, strategy="mobile",
        requested_url="u", timestamp_utc="t",
    )
    assert run.total_requests == 3


def test_extract_opportunities_skip_error_audits():
    raw = {
        "lighthouseResult": {
            "categories": {},
            "audits": {
                "unused-css-rules": {
                    "title": "x",
                    "scoreDisplayMode": "error",
                    "score": None,
                }
            },
        }
    }
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    assert run.opportunities == []


def test_extract_run_is_ok_without_error():
    raw = {"lighthouseResult": {"audits": {}, "categories": {}}}
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    assert run.ok is True
    assert run.error is None


def test_extract_lcp_element_falls_back_to_insight_audit():
    """Lighthouse >= 12 (confirmado: 13.4.1 na resposta real de
    2026-08-08) nao retorna mais 'largest-contentful-paint-element' --
    o elemento aparece dentro de 'lcp-discovery-insight'."""
    raw = {
        "lighthouseResult": {
            "categories": {},
            "audits": {
                "lcp-discovery-insight": {
                    "title": "LCP request discovery",
                    "details": {
                        "items": [
                            {"type": "checklist", "items": {"eagerlyLoaded": {"value": True}}},
                            {
                                "nodeLabel": "hero",
                                "snippet": "<img src=hero.jpg>",
                                "url": "https://example.com/hero.jpg",
                            },
                        ]
                    },
                }
            },
        }
    }
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    assert run.lcp_element is not None
    assert run.lcp_element.url == "https://example.com/hero.jpg"


def test_extract_dom_size_falls_back_to_insight_audit():
    raw = {
        "lighthouseResult": {
            "categories": {},
            "audits": {
                "dom-size-insight": {
                    "score": 1,
                    "details": {
                        "items": [
                            {"statistic": "Total elements", "value": {"value": 145}},
                            {"statistic": "DOM depth", "value": {"value": 8}},
                        ]
                    },
                }
            },
        }
    }
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    assert run.metrics["DOM Size"].numeric_value == 145


def test_extract_opportunity_sums_item_level_wasted_bytes_when_no_aggregate():
    """image-delivery-insight (Lighthouse >= 12) nao traz
    overallSavingsBytes agregado -- so wastedBytes por item. A ferramenta
    deve somar isso (agregacao de valor real da API, nunca invencao)."""
    raw = {
        "lighthouseResult": {
            "categories": {},
            "audits": {
                "image-delivery-insight": {
                    "title": "Improve image delivery",
                    "score": 0,
                    "displayValue": "Est savings of 6,225 KiB",
                    "details": {
                        "items": [
                            {"url": "a.jpg", "wastedBytes": 2750318, "totalBytes": 2834618},
                            {"url": "b.jpg", "wastedBytes": 1500000, "totalBytes": 1600000},
                        ]
                    },
                }
            },
        }
    }
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    opp = next(o for o in run.opportunities if o.audit_id == "image-delivery-insight")
    assert opp.overall_savings_bytes == pytest.approx(4250318)


def test_extract_opportunity_without_items_has_no_invented_savings():
    raw = {
        "lighthouseResult": {
            "categories": {},
            "audits": {
                "document-latency-insight": {
                    "title": "Server responds quickly",
                    "score": 1,
                    "details": {"debugData": {"serverResponseTime": 1}, "items": {}},
                }
            },
        }
    }
    run = extract_run_result(raw, run_index=1, strategy="mobile", requested_url="u", timestamp_utc="t")
    opp = next(o for o in run.opportunities if o.audit_id == "document-latency-insight")
    assert opp.overall_savings_bytes is None
    assert opp.overall_savings_ms is None
