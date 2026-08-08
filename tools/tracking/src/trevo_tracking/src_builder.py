"""Constroi o parametro `src` do Hotmart HotLink (etapa 12 do runbook).

Regras oficiais confirmadas em help.hotmart.com em 2026-08-08:
  - maximo 30 caracteres;
  - `_` (underscore) e reservado internamente pela Hotmart -- proibido;
  - `|` (pipe) e permitido e usado para organizar caracteristicas da
    campanha.

Padrao v1 deste projeto: `<network_prefix>|<experiment_id>|<creative_code>`
(ex.: `g|mt01|est01`).
"""

from __future__ import annotations

import re

MAX_SRC_LENGTH = 30
FALLBACK_CREATIVE_CODE = "none"  # sentinela documentado, nao um criativo inventado

_INVALID_CHARS_RE = re.compile(r"[^a-z0-9-]")


class InvalidSrcError(ValueError):
    pass


def _sanitize_segment(value: str) -> str:
    """Minusculas, espaco/underscore viram hifen, qualquer outro
    caractere fora de [a-z0-9-] e removido. Nunca aceita o valor bruto
    sem passar por aqui -- e o unico jeito de um creative_code arbitrario
    virar parte do src."""
    lowered = value.strip().lower().replace("_", "-").replace(" ", "-")
    cleaned = _INVALID_CHARS_RE.sub("", lowered)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned


def build_hotmart_src(
    *, experiment_id: str, creative_code: str | None, network_prefix: str = "g"
) -> str:
    """Monta e valida o src. Levanta InvalidSrcError se o resultado violar
    as regras da Hotmart (>30 chars ou contem '_') -- nunca retorna um src
    invalido silenciosamente."""
    safe_network = _sanitize_segment(network_prefix) or "g"
    safe_experiment = _sanitize_segment(experiment_id)
    safe_creative = _sanitize_segment(creative_code) if creative_code else ""
    if not safe_creative:
        safe_creative = FALLBACK_CREATIVE_CODE

    if not safe_experiment:
        raise InvalidSrcError(f"experiment_id invalido apos sanitizacao: {experiment_id!r}")

    src = f"{safe_network}|{safe_experiment}|{safe_creative}"

    if "_" in src:
        raise InvalidSrcError(f"src nao pode conter '_' (Hotmart): {src!r}")
    if len(src) > MAX_SRC_LENGTH:
        raise InvalidSrcError(
            f"src excede {MAX_SRC_LENGTH} caracteres ({len(src)}): {src!r}. "
            "Use um creative_code mais curto."
        )
    return src
