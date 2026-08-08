"""Classificacao de achados por severidade (etapa 13 do runbook).

Regras de classificacao (heuristica declarada, nao arbitraria por
audit-a-audit):

- P0 (BLOCKER DE CAMPANHA): score de performance mediano mobile < 50, ou
  qualquer erro fatal que tenha impedido a medicao (ex.: pagina nao
  carregou), ou LCP mediano mobile > 4s (limiar oficial de "Poor" do
  Core Web Vitals).
- P1 (CORRIGIR ANTES DO LANCAMENTO): opportunity com overall_savings_ms
  >= 300ms, ou score de categoria < 90 em qualquer categoria, ou LCP
  mediano mobile entre 2.5s e 4s ("Needs Improvement").
- P2 (OTIMIZAR DEPOIS): opportunity com savings > 0 mas < 300ms, ou score
  de categoria entre 90 e 99.
- INFO: sem acao necessaria (score 100, ou audit 'notApplicable').

Nunca inventamos uma estimativa de economia -- `overall_savings_ms` e
`overall_savings_bytes` so aparecem quando a propria API os retornou.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import Opportunity
from .stats import Summary

LCP_POOR_MS = 4000
LCP_NEEDS_IMPROVEMENT_MS = 2500
PERFORMANCE_P0_THRESHOLD = 50


@dataclass
class Finding:
    severity: str  # P0 / P1 / P2 / INFO
    category: str  # performance / accessibility / best-practices / seo
    strategy: str  # mobile / desktop / ambos
    audit_id: str
    title: str
    evidence: str
    impact: str
    probable_cause: str
    recommendation: str
    estimated_savings_ms: float | None = None
    estimated_savings_bytes: float | None = None


SAVINGS_BYTES_P1_THRESHOLD = 500_000  # 500 KB
SAVINGS_BYTES_P2_THRESHOLD = 50_000  # 50 KB


def classify_opportunity(opp: Opportunity, *, strategy: str, category: str) -> Finding | None:
    savings_ms = opp.overall_savings_ms or 0
    savings_bytes = opp.overall_savings_bytes or 0

    if savings_ms >= 300 or savings_bytes >= SAVINGS_BYTES_P1_THRESHOLD:
        severity = "P1"
    elif savings_ms > 0 or savings_bytes >= SAVINGS_BYTES_P2_THRESHOLD:
        severity = "P2"
    elif opp.score is not None and opp.score < 0.9:
        severity = "P2"
    else:
        return None  # score maximo e sem economia relatada: nada a reportar

    evidence = opp.display_value or f"score={opp.score}"
    impact_parts = []
    if opp.overall_savings_ms:
        impact_parts.append(f"{opp.overall_savings_ms:.0f} ms")
    if opp.overall_savings_bytes:
        impact_parts.append(f"{opp.overall_savings_bytes / 1024:.0f} KiB")
    impact = (
        f"Economia estimada pela API: {' / '.join(impact_parts)}"
        if impact_parts
        else "Sem estimativa numerica de economia fornecida pela API"
    )

    return Finding(
        severity=severity,
        category=category,
        strategy=strategy,
        audit_id=opp.audit_id,
        title=opp.title,
        evidence=evidence,
        impact=impact,
        probable_cause=opp.title,
        recommendation=opp.description or opp.title,
        estimated_savings_ms=opp.overall_savings_ms,
        estimated_savings_bytes=opp.overall_savings_bytes,
    )


def classify_category_score(
    category: str, strategy: str, summary: Summary
) -> Finding | None:
    if summary.median is None:
        return None
    if summary.median < 50:
        severity = "P0"
    elif summary.median < 90:
        severity = "P1"
    elif summary.median < 100:
        severity = "P2"
    else:
        return None
    return Finding(
        severity=severity,
        category=category,
        strategy=strategy,
        audit_id=f"category-score-{category}",
        title=f"Score de {category} abaixo do ideal ({strategy})",
        evidence=f"mediana={summary.median:.1f}, pior={summary.worst:.1f}",
        impact=f"Categoria {category} nao esta no patamar ideal em {strategy}",
        probable_cause="Ver audits individuais da categoria no relatorio detalhado",
        recommendation="Revisar audits com score < 1 nesta categoria",
    )


def classify_lcp(strategy: str, median_lcp_ms: float | None) -> Finding | None:
    if median_lcp_ms is None:
        return None
    if median_lcp_ms > LCP_POOR_MS:
        severity = "P0"
    elif median_lcp_ms > LCP_NEEDS_IMPROVEMENT_MS:
        severity = "P1"
    else:
        return None
    return Finding(
        severity=severity,
        category="performance",
        strategy=strategy,
        audit_id="largest-contentful-paint",
        title=f"LCP mediano acima do limiar 'bom' em {strategy}",
        evidence=f"LCP mediano = {median_lcp_ms:.0f} ms (limiar bom <= {LCP_NEEDS_IMPROVEMENT_MS} ms)",
        impact="Core Web Vitals (lab data) fora do patamar 'Good'",
        probable_cause="Ver elemento LCP e cadeia critica no relatorio detalhado",
        recommendation="Investigar prioridade/preload do recurso do elemento LCP",
    )


def sort_findings(findings: list[Finding]) -> list[Finding]:
    order = {"P0": 0, "P1": 1, "P2": 2, "INFO": 3}
    return sorted(findings, key=lambda f: (order.get(f.severity, 9), f.category, f.strategy))
