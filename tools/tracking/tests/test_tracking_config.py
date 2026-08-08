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


def test_init_options_never_enable_recording_or_autocapture():
    assert POSTHOG_INIT_OPTIONS["disable_session_recording"] is True
    assert POSTHOG_INIT_OPTIONS["autocapture"] is False
    assert POSTHOG_INIT_OPTIONS["disable_persistence"] is True
    assert POSTHOG_INIT_OPTIONS["capture_pageleave"] is False
    assert POSTHOG_INIT_OPTIONS["debug"] is False


def test_init_options_captures_pageview_and_campaign_params():
    assert POSTHOG_INIT_OPTIONS["capture_pageview"] is True
    assert POSTHOG_INIT_OPTIONS["save_campaign_params"] is True
