"""Gera assets/js/tracking-config.generated.js a partir de tools/tracking/.env.

Uso:
    python etapa_5_a_v1_generate_tracking_config.py

Para antes de qualquer coisa se POSTHOG_PROJECT_TOKEN estiver ausente --
nunca escreve um arquivo publico com token vazio, e nunca imprime o valor
do token (mesmo ele nao sendo uma Personal API Key, ver README).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from trevo_tracking.config import Config  # noqa: E402
from trevo_tracking.tracking_config import build_public_config  # noqa: E402

TOOL_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TOOL_ROOT.parent.parent
OUTPUT_PATH = REPO_ROOT / "assets" / "js" / "tracking-config.generated.js"

HEADER = """/*
 * GERADO POR tools/tracking/etapa_5_a_v1_generate_tracking_config.py -- nao editar a mao.
 *
 * Este arquivo E publico e commitado DE PROPOSITO: posthogProjectToken e
 * um token de ingestao do SDK web (nao uma Personal API Key) e, por
 * definicao, precisa chegar ao navegador para o PostHog funcionar.
 * Ver tools/tracking/README.md, secao "Project token x Personal API Key".
 */
"""


def main() -> int:
    config = Config.from_env()
    if not config.has_token:
        print(json.dumps({"status": "POSTHOG_PROJECT_TOKEN_AUSENTE"}))
        return 1

    public_config = build_public_config(config)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    body = (
        HEADER
        + "window.__TREVO_TRACKING_CONFIG__ = "
        + json.dumps(public_config, indent=2, ensure_ascii=False)
        + ";\n"
    )
    OUTPUT_PATH.write_text(body, encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "OK",
                "written": str(OUTPUT_PATH),
                "posthog_project_token": "PRESENTE",
                "posthog_host": config.posthog_host,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
