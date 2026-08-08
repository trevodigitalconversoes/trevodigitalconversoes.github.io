from __future__ import annotations

from trevo_pagespeed.findings import classify_category_score, classify_lcp, classify_opportunity
from trevo_pagespeed.models import Opportunity
from trevo_pagespeed.stats import summarize


def test_classify_opportunity_high_savings_is_p1():
    opp = Opportunity(
        audit_id="unused-css-rules", title="Reduce unused CSS", score=0.6,
        display_value="Potential savings of 400 ms", overall_savings_ms=400,
        overall_savings_bytes=10000, description="desc",
    )
    finding = classify_opportunity(opp, strategy="mobile", category="performance")
    assert finding is not None
    assert finding.severity == "P1"
    assert finding.estimated_savings_ms == 400


def test_classify_opportunity_low_savings_is_p2():
    opp = Opportunity(
        audit_id="x", title="x", score=0.9, display_value="Potential savings of 50 ms",
        overall_savings_ms=50, overall_savings_bytes=None, description=None,
    )
    finding = classify_opportunity(opp, strategy="mobile", category="performance")
    assert finding.severity == "P2"


def test_classify_opportunity_perfect_score_no_savings_is_none():
    opp = Opportunity(
        audit_id="x", title="x", score=1.0, display_value=None,
        overall_savings_ms=None, overall_savings_bytes=None, description=None,
    )
    assert classify_opportunity(opp, strategy="mobile", category="performance") is None


def test_classify_opportunity_never_invents_savings():
    opp = Opportunity(
        audit_id="x", title="x", score=0.5, display_value=None,
        overall_savings_ms=None, overall_savings_bytes=None, description=None,
    )
    finding = classify_opportunity(opp, strategy="mobile", category="performance")
    assert finding.estimated_savings_ms is None
    assert "Sem estimativa" in finding.impact


def test_classify_category_score_p0_below_50():
    summary = summarize([40.0, 45.0, 42.0], worst_is_max=False)
    finding = classify_category_score("performance", "mobile", summary)
    assert finding.severity == "P0"


def test_classify_category_score_p1_below_90():
    summary = summarize([80.0, 85.0, 82.0], worst_is_max=False)
    finding = classify_category_score("performance", "mobile", summary)
    assert finding.severity == "P1"


def test_classify_category_score_p2_below_100():
    summary = summarize([92.0, 95.0, 93.0], worst_is_max=False)
    finding = classify_category_score("performance", "mobile", summary)
    assert finding.severity == "P2"


def test_classify_category_score_perfect_is_none():
    summary = summarize([100.0, 100.0, 100.0], worst_is_max=False)
    assert classify_category_score("performance", "mobile", summary) is None


def test_classify_category_score_no_data_is_none():
    summary = summarize([])
    assert classify_category_score("performance", "mobile", summary) is None


def test_classify_lcp_poor_is_p0():
    finding = classify_lcp("mobile", 4500.0)
    assert finding.severity == "P0"


def test_classify_lcp_needs_improvement_is_p1():
    finding = classify_lcp("mobile", 3000.0)
    assert finding.severity == "P1"


def test_classify_lcp_good_is_none():
    assert classify_lcp("mobile", 2000.0) is None


def test_classify_lcp_missing_value_is_none():
    assert classify_lcp("mobile", None) is None


def test_classify_opportunity_large_byte_savings_is_p1_even_without_ms():
    opp = Opportunity(
        audit_id="image-delivery-insight", title="Improve image delivery", score=0,
        display_value="Est savings of 6,225 KiB", overall_savings_ms=None,
        overall_savings_bytes=6_374_000, description="desc",
    )
    finding = classify_opportunity(opp, strategy="mobile", category="performance")
    assert finding.severity == "P1"
    assert "KiB" in finding.impact


def test_classify_opportunity_small_byte_savings_is_p2():
    opp = Opportunity(
        audit_id="cache-insight", title="cache", score=0, display_value=None,
        overall_savings_ms=None, overall_savings_bytes=60_000, description=None,
    )
    finding = classify_opportunity(opp, strategy="mobile", category="performance")
    assert finding.severity == "P2"
