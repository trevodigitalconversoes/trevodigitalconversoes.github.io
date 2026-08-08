from __future__ import annotations

from trevo_pagespeed.findings import Finding
from trevo_pagespeed.verdict import decide_verdict


def _finding(severity: str) -> Finding:
    return Finding(
        severity=severity, category="performance", strategy="mobile", audit_id="x",
        title="x", evidence="x", impact="x", probable_cause="x", recommendation="x",
    )


def test_verdict_blocked_when_measurement_failed():
    assert decide_verdict([], measurement_ok=False) == "PAGESPEED_BLOCKED"


def test_verdict_fix_before_launch_on_p0():
    findings = [_finding("P0"), _finding("P2")]
    assert decide_verdict(findings, measurement_ok=True) == "PAGESPEED_FIX_BEFORE_LAUNCH"


def test_verdict_ready_with_optimizations_on_p1():
    findings = [_finding("P1")]
    assert decide_verdict(findings, measurement_ok=True) == "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS"


def test_verdict_ready_with_optimizations_on_p2_only():
    findings = [_finding("P2")]
    assert decide_verdict(findings, measurement_ok=True) == "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS"


def test_verdict_ready_when_no_findings():
    assert decide_verdict([], measurement_ok=True) == "PAGESPEED_LAUNCH_READY"


def test_verdict_ready_when_only_info():
    findings = [_finding("INFO")]
    assert decide_verdict(findings, measurement_ok=True) == "PAGESPEED_LAUNCH_READY"
