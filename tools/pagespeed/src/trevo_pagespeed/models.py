"""Estruturas de dados do resultado de uma execucao PageSpeed/CrUX. Nenhuma
classe aqui faz rede -- so representa o que ja foi extraido de uma resposta
JSON."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MetricValue:
    """Um valor de metrica de laboratorio de um unico run (ex.: LCP em
    2.3s). `raw_value` fica na unidade nativa do Lighthouse (geralmente ms
    ou score 0-1); `display_value` e o texto formatado que a propria API
    devolveu, quando presente."""

    audit_id: str
    title: str
    numeric_value: float | None
    numeric_unit: str | None
    score: float | None
    display_value: str | None


@dataclass
class Opportunity:
    """Um audit com economia potencial estimada pela propria API (nunca
    inventada por nos)."""

    audit_id: str
    title: str
    score: float | None
    display_value: str | None
    overall_savings_ms: float | None
    overall_savings_bytes: float | None
    description: str | None


@dataclass
class LcpElementInfo:
    node_snippet: str | None
    node_selector: str | None
    url: str | None


@dataclass
class RunResult:
    """Resultado de uma unica chamada `runPagespeed`, ja com os campos que
    o resto da ferramenta consome extraidos do JSON bruto."""

    run_index: int
    strategy: str
    requested_url: str
    timestamp_utc: str
    final_url: str | None
    lighthouse_version: str | None
    fetch_time: str | None
    warnings: list[str]
    scores: dict[str, float | None]  # performance/accessibility/best-practices/seo, 0-100
    metrics: dict[str, MetricValue]
    opportunities: list[Opportunity]
    diagnostics: list[Opportunity]
    lcp_element: LcpElementInfo | None
    environment: dict | None
    total_byte_weight_bytes: float | None
    total_requests: int | None
    raw_path: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass
class CruxResult:
    """Resultado (ou ausencia documentada) de uma consulta CrUX."""

    target: str  # 'page' ou 'origin'
    status: str  # PASS / NO_DATA / BLOCKED / NOT_ENABLED
    metrics: dict[str, dict] = field(default_factory=dict)
    form_factors: list[str] = field(default_factory=list)
    collection_period: dict | None = None
    error: str | None = None


def utc_now_iso(now: datetime) -> str:
    return now.isoformat().replace("+00:00", "Z")
