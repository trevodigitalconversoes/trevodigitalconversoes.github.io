"""Estatisticas simples sobre uma lista de valores numericos de multiplos
runs. Sem numpy -- a lista tem no maximo poucas dezenas de itens."""

from __future__ import annotations

import statistics
from dataclasses import dataclass


@dataclass
class Summary:
    n: int
    minimum: float | None
    maximum: float | None
    mean: float | None
    median: float | None
    worst: float | None  # alias semantico de minimo ou maximo, ver worst_is_max


def summarize(values: list[float], *, worst_is_max: bool = True) -> Summary:
    """Resume uma lista de valores. `worst_is_max=True` para metricas onde
    maior e pior (ex.: LCP em ms); False para metricas onde maior e melhor
    (ex.: score 0-100)."""
    clean = [v for v in values if v is not None]
    if not clean:
        return Summary(n=0, minimum=None, maximum=None, mean=None, median=None, worst=None)
    minimum = min(clean)
    maximum = max(clean)
    worst = maximum if worst_is_max else minimum
    return Summary(
        n=len(clean),
        minimum=minimum,
        maximum=maximum,
        mean=statistics.fmean(clean),
        median=statistics.median(clean),
        worst=worst,
    )
