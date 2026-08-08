from __future__ import annotations

from trevo_pagespeed.client import CruxOutcome
from trevo_pagespeed.crux import extract_crux_result


def test_extract_crux_pass():
    outcome = CruxOutcome(
        status="PASS",
        data={
            "record": {
                "key": {"formFactor": "PHONE"},
                "metrics": {
                    "largest_contentful_paint": {"percentiles": {"p75": 2100}, "histogram": []},
                },
                "collectionPeriod": {"firstDate": {}, "lastDate": {}},
            }
        },
        error=None,
    )
    result = extract_crux_result(outcome, target="page")
    assert result.status == "PASS"
    assert result.metrics["LCP"]["p75"] == 2100
    assert result.form_factors == ["PHONE"]


def test_extract_crux_no_data():
    outcome = CruxOutcome(status="NO_DATA", data=None, error="sem dados")
    result = extract_crux_result(outcome, target="page")
    assert result.status == "NO_DATA"
    assert result.metrics == {}


def test_extract_crux_not_enabled():
    outcome = CruxOutcome(status="NOT_ENABLED", data=None, error="API desabilitada")
    result = extract_crux_result(outcome, target="origin")
    assert result.status == "NOT_ENABLED"
