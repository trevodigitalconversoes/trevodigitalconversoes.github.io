"""Veredito final (etapa 13/22 do runbook). Nao usa 100/100 como gate;
classifica por impacto (P0/P1/P2/INFO) e decide entre os 4 estados
possiveis."""

from __future__ import annotations

from .findings import Finding

VERDICTS = (
    "PAGESPEED_LAUNCH_READY",
    "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS",
    "PAGESPEED_FIX_BEFORE_LAUNCH",
    "PAGESPEED_BLOCKED",
)


def decide_verdict(findings: list[Finding], *, measurement_ok: bool) -> str:
    if not measurement_ok:
        return "PAGESPEED_BLOCKED"
    if any(f.severity == "P0" for f in findings):
        return "PAGESPEED_FIX_BEFORE_LAUNCH"
    if any(f.severity == "P1" for f in findings):
        return "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS"
    if any(f.severity == "P2" for f in findings):
        return "PAGESPEED_LAUNCH_READY_WITH_OPTIMIZATIONS"
    return "PAGESPEED_LAUNCH_READY"
