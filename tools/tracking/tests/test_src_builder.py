from __future__ import annotations

import pytest

from trevo_tracking.src_builder import FALLBACK_CREATIVE_CODE, InvalidSrcError, build_hotmart_src


def test_contract_examples():
    assert build_hotmart_src(experiment_id="mt01", creative_code="est01") == "g|mt01|est01"
    assert build_hotmart_src(experiment_id="mt01", creative_code="est02") == "g|mt01|est02"
    assert build_hotmart_src(experiment_id="mt01", creative_code="vid01") == "g|mt01|vid01"


def test_missing_creative_uses_documented_fallback():
    src = build_hotmart_src(experiment_id="mt01", creative_code=None)
    assert src == f"g|mt01|{FALLBACK_CREATIVE_CODE}"


def test_underscore_in_creative_is_sanitized_to_hyphen():
    src = build_hotmart_src(experiment_id="mt01", creative_code="est_01")
    assert "_" not in src
    assert src == "g|mt01|est-01"


def test_never_exceeds_30_chars():
    src = build_hotmart_src(experiment_id="mt01", creative_code="est01")
    assert len(src) <= 30


def test_too_long_creative_raises_instead_of_truncating_silently():
    with pytest.raises(InvalidSrcError):
        build_hotmart_src(experiment_id="mt01", creative_code="a-creative-code-way-too-long-for-hotmart")


def test_arbitrary_special_chars_stripped():
    src = build_hotmart_src(experiment_id="mt01", creative_code="Est 01!@#")
    assert src == "g|mt01|est-01"


def test_custom_network_prefix():
    src = build_hotmart_src(experiment_id="mt01", creative_code="est01", network_prefix="s")
    assert src.startswith("s|")


def test_invalid_experiment_id_raises():
    with pytest.raises(InvalidSrcError):
        build_hotmart_src(experiment_id="___", creative_code="est01")
