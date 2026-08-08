from __future__ import annotations

from trevo_tracking.params import ALLOWED_CAMPAIGN_PARAMS, HOTMART_FORWARDED_PARAMS, sanitize_query_params


def test_sanitize_keeps_only_whitelisted():
    result = sanitize_query_params({"utm_source": "google", "unknown_param": "evil", "gclid": "abc"})
    assert result == {"utm_source": "google", "gclid": "abc"}


def test_sanitize_drops_unknown_param_entirely():
    result = sanitize_query_params({"session_id": "leak", "fbclid": "x"})
    assert result == {}


def test_sanitize_empty_input():
    assert sanitize_query_params({}) == {}


def test_all_contract_params_present():
    expected = {
        "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
        "campaign_id", "ad_group_id", "ad_id", "device", "network", "matchtype",
        "gclid", "gbraid", "wbraid", "gad_source",
    }
    assert ALLOWED_CAMPAIGN_PARAMS == frozenset(expected)


def test_hotmart_forwarded_is_subset_of_allowed():
    assert set(HOTMART_FORWARDED_PARAMS).issubset(ALLOWED_CAMPAIGN_PARAMS)


def test_hotmart_forwarded_excludes_google_identifiers():
    for key in ("gclid", "campaign_id", "ad_group_id", "ad_id"):
        assert key not in HOTMART_FORWARDED_PARAMS
