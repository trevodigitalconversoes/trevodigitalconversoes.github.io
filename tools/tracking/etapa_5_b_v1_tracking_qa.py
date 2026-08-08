"""QA estatico local do contrato de tracking -- sem rede, sem browser.
Complementa (nao substitui) os testes automatizados e o QA em browser
(ver docs/etapa_5_c_v1_contrato_tracking_microteste01.md).

Uso:
    python etapa_5_b_v1_tracking_qa.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from trevo_tracking.hotlink_builder import build_hotlink  # noqa: E402
from trevo_tracking.src_builder import build_hotmart_src  # noqa: E402
from trevo_tracking.tracking_config import HOTLINK_BASE  # noqa: E402

TOOL_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TOOL_ROOT.parent.parent
TRACKING_JS = REPO_ROOT / "assets" / "js" / "etapa_5_d_v1_tracking.js"
GENERATED_CONFIG_JS = REPO_ROOT / "assets" / "js" / "tracking-config.generated.js"
PRESELL_HTML = REPO_ROOT / "produtos" / "fotografia-presets-lightroom" / "index.html"

# Padroes que NUNCA podem aparecer no JS publico deste microteste.
#
# Nota (2026-08-08): heatmaps/session replay/autocapture/Web Vitals sao
# agora habilitados DE PROPOSITO via config.posthogInitOptions (decisao
# do usuario) -- por isso NAO ha mais um bloqueio generico para as
# palavras "heatmaps"/"session recording" aqui. O que continua proibido e
# codigo que identifica pessoas, chama APIs de surveys/feature flags
# diretamente, ou opta explicitamente por captura de payload de rede.
FORBIDDEN_JS_PATTERNS = [
    r"\.identify\s*\(",
    r"\.alias\s*\(",
    r"\.group\s*\(",
    r"\.setPersonProperties\s*\(",
    r"\.getSurveys\s*\(",
    r"\.getFeatureFlag\s*\(",
    r"\.onFeatureFlags\s*\(",
    r"recordBody",
    r"recordHeaders",
    r"captureNetworkV2",
]


def check_tracking_js() -> dict:
    if not TRACKING_JS.exists():
        return {"ok": False, "error": f"nao encontrado: {TRACKING_JS}"}
    source = TRACKING_JS.read_text(encoding="utf-8")
    violations = [p for p in FORBIDDEN_JS_PATTERNS if re.search(p, source)]
    return {"ok": not violations, "violations": violations}


def check_generated_config() -> dict:
    if not GENERATED_CONFIG_JS.exists():
        return {"ok": False, "status": "NAO_GERADO", "hint": "rode etapa_5_a_v1_generate_tracking_config.py"}
    source = GENERATED_CONFIG_JS.read_text(encoding="utf-8")
    match = re.search(r"window\.__TREVO_TRACKING_CONFIG__\s*=\s*(\{.*\});", source, re.DOTALL)
    if not match:
        return {"ok": False, "status": "FORMATO_INESPERADO"}
    data = json.loads(match.group(1))
    token_present = bool(data.get("posthogProjectToken"))
    return {
        "ok": token_present,
        "status": "OK" if token_present else "TOKEN_AUSENTE",
        "posthog_project_token": "PRESENTE" if token_present else "AUSENTE",
        "posthog_host": data.get("posthogHost"),
        "init_options": data.get("posthogInitOptions"),
    }


def check_ctas() -> dict:
    if not PRESELL_HTML.exists():
        return {"ok": False, "error": f"nao encontrado: {PRESELL_HTML}"}
    source = PRESELL_HTML.read_text(encoding="utf-8")
    anchors = re.findall(r"<a\s+class=\"cta-button\"[^>]*>", source)
    if not anchors:
        return {"ok": False, "error": "nenhum CTA (a.cta-button) encontrado"}
    missing_position = [a for a in anchors if "data-cta-position=" not in a]
    missing_href = [a for a in anchors if HOTLINK_BASE not in a]
    return {
        "ok": not missing_position and not missing_href,
        "cta_count": len(anchors),
        "missing_data_cta_position": len(missing_position),
        "missing_hotlink_href": len(missing_href),
    }


def check_src_contract() -> dict:
    cases = {
        "est01": build_hotmart_src(experiment_id="mt01", creative_code="est01"),
        "est02": build_hotmart_src(experiment_id="mt01", creative_code="est02"),
        "vid01": build_hotmart_src(experiment_id="mt01", creative_code="vid01"),
        "sem_creative": build_hotmart_src(experiment_id="mt01", creative_code=None),
    }
    expected = {
        "est01": "g|mt01|est01",
        "est02": "g|mt01|est02",
        "vid01": "g|mt01|vid01",
        "sem_creative": "g|mt01|none",
    }
    ok = cases == expected
    return {"ok": ok, "cases": cases, "expected": expected}


def check_hotlink_contract() -> dict:
    src = build_hotmart_src(experiment_id="mt01", creative_code="est01")
    with_utms = build_hotlink(
        HOTLINK_BASE,
        src=src,
        campaign_params={
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "mt01-foto18",
            "utm_content": "est01",
            "campaign_id": "123",  # nao deve aparecer no HotLink
        },
    )
    no_params = build_hotlink(HOTLINK_BASE, src=src, campaign_params={})
    ok = (
        "campaign_id" not in with_utms
        and "src=g%7Cmt01%7Cest01" in with_utms
        and "utm_source=google" in with_utms
        and no_params.startswith(HOTLINK_BASE)
    )
    return {"ok": ok, "with_utms": with_utms, "no_params": no_params}


def main() -> int:
    results = {
        "tracking_js": check_tracking_js(),
        "generated_config": check_generated_config(),
        "ctas": check_ctas(),
        "src_contract": check_src_contract(),
        "hotlink_contract": check_hotlink_contract(),
    }
    overall_ok = all(r.get("ok") for r in results.values())
    print(json.dumps({"overall_ok": overall_ok, **results}, indent=2, ensure_ascii=False))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
