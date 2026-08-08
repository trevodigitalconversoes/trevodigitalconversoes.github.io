from __future__ import annotations

import pytest

from trevo_tracking.config import Config
from trevo_tracking.tracking_config import POSTHOG_INIT_OPTIONS, build_public_config


def test_build_public_config_requires_token():
    with pytest.raises(ValueError):
        build_public_config(Config(posthog_project_token=None))


def test_build_public_config_includes_token_and_options():
    config = Config(posthog_project_token="phc_abc123")
    public_config = build_public_config(config)
    assert public_config["posthogProjectToken"] == "phc_abc123"
    assert public_config["posthogInitOptions"] == POSTHOG_INIT_OPTIONS
    assert public_config["experimentId"] == "mt01"
    assert public_config["productSlug"] == "fotografia-presets-lightroom"


def test_init_options_now_enables_analytics_capabilities():
    """Decisao do usuario (2026-08-08): habilitar progressivamente
    autocapture/heatmaps/Web Vitals/Session Replay, revertendo o desenho
    minimo original."""
    assert POSTHOG_INIT_OPTIONS["autocapture"] is True
    assert POSTHOG_INIT_OPTIONS["disable_session_recording"] is False
    assert POSTHOG_INIT_OPTIONS["capture_heatmaps"] is True
    assert POSTHOG_INIT_OPTIONS["capture_performance"] == {"web_vitals": True}
    assert POSTHOG_INIT_OPTIONS["capture_pageleave"] is True
    assert POSTHOG_INIT_OPTIONS["disable_persistence"] is False


def test_init_options_still_no_person_identification():
    """Habilitar autocapture/replay/heatmaps nao muda a decisao de nunca
    identificar visitantes -- person_profiles continua o valor que nunca
    cria profile sem identify() explicito (que este projeto nunca chama)."""
    assert POSTHOG_INIT_OPTIONS["person_profiles"] == "identified_only"


def test_init_options_console_recording_explicitly_off():
    """O projeto PostHog permite console recording, mas esta pre-sell
    especificamente mantem desligado -- decisao registrada no README."""
    assert POSTHOG_INIT_OPTIONS["enable_recording_console_log"] is False


def test_init_options_masks_inputs_explicitly():
    assert POSTHOG_INIT_OPTIONS["session_recording"] == {"maskAllInputs": True}


def test_init_options_never_opts_into_network_payload_capture():
    """Nao deve existir NENHUMA chave relacionada a captura de payload de
    rede (request/response body) -- permanece no estado default
    (desligado), nunca opt-in nesta pre-sell."""
    session_recording = POSTHOG_INIT_OPTIONS["session_recording"]
    forbidden_keys = {"recordBody", "recordHeaders", "captureNetworkV2", "recordCanvas"}
    assert not forbidden_keys.intersection(session_recording.keys())


def test_init_options_captures_pageview_and_campaign_params():
    assert POSTHOG_INIT_OPTIONS["capture_pageview"] is True
    assert POSTHOG_INIT_OPTIONS["save_campaign_params"] is True


def test_init_options_debug_off():
    assert POSTHOG_INIT_OPTIONS["debug"] is False
