"""Verifica invariantes do JS publico (assets/js/etapa_5_d_v1_tracking.js)
por leitura estatica -- nao executa o arquivo (nao ha DOM/browser em
pytest). Complementado pelo QA em browser real (etapa 19 do runbook)."""

from __future__ import annotations

from pathlib import Path

TRACKING_JS = Path(__file__).resolve().parents[1].parent.parent / "assets" / "js" / "etapa_5_d_v1_tracking.js"


def _source() -> str:
    assert TRACKING_JS.exists(), f"arquivo nao encontrado: {TRACKING_JS}"
    return TRACKING_JS.read_text(encoding="utf-8")


def test_never_calls_identify_or_alias_or_group():
    source = _source()
    assert ".identify(" not in source
    assert ".alias(" not in source
    assert ".group(" not in source
    assert ".setPersonProperties(" not in source


def test_never_hardcodes_capabilities_that_belong_in_python_config():
    """Autocapture/heatmaps/Web Vitals/Session Replay agora sao
    habilitados de proposito (decisao do usuario em 2026-08-08), mas a
    fonte de verdade e config.posthogInitOptions (Python), nunca
    hardcoded aqui -- o JS so repassa o objeto ao posthog.init()."""
    source = _source()
    assert "startSessionRecording" not in source
    assert "loadFeatureFlags" not in source
    assert "posthog.init(config.posthogProjectToken, initOptions)" in source


def test_never_calls_survey_or_feature_flag_apis():
    source = _source()
    assert ".getSurveys(" not in source
    assert ".getFeatureFlag(" not in source
    assert ".onFeatureFlags(" not in source


def test_never_opts_into_network_payload_capture():
    source = _source()
    for forbidden in ("recordBody", "recordHeaders", "captureNetworkV2"):
        assert forbidden not in source


def test_no_personal_data_fields_referenced():
    source = _source().lower()
    for field in ("email", "phone", "cpf", "endereco", "address", "nome_completo"):
        assert field not in source


def test_capture_call_is_wrapped_in_try_catch():
    source = _source()
    capture_idx = source.index('posthogInstance.capture("outbound_hotmart"')
    click_handler_start = source.index("anchor.addEventListener(")
    click_handler_body = source[click_handler_start:capture_idx]
    assert "try {" in click_handler_body
    after_capture = source[capture_idx:]
    assert "} catch (err) {" in after_capture[: after_capture.index("});")]


def test_cta_href_is_rewritten_before_any_network_dependent_step():
    """O href precisa ser resolvido de forma sincrona (nao depender do
    PostHog ja ter carregado) -- senao um clique rapido usaria um href
    quebrado."""
    source = _source()
    set_href_idx = source.index('anchor.setAttribute("href"')
    posthog_capture_idx = source.index('posthogInstance.capture("outbound_hotmart"')
    assert set_href_idx < posthog_capture_idx


def test_only_forwards_utm_params_to_hotlink():
    source = _source()
    assert 'HOTMART_FORWARDED_PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]' in source


def test_src_max_length_and_fallback_present():
    source = _source()
    assert "SRC_MAX_LENGTH = 30" in source
    assert 'SRC_FALLBACK_CREATIVE = "none"' in source


def test_early_return_when_config_missing():
    source = _source()
    idx = source.index("if (!config || !config.posthogProjectToken)")
    assert "return;" in source[idx : idx + 60]
