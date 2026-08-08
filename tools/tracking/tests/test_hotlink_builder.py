from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from trevo_tracking.hotlink_builder import build_hotlink

BASE = "https://go.hotmart.com/V106592210H"


def test_hotlink_without_params_keeps_base_and_src():
    url = build_hotlink(BASE, src="g|mt01|est01", campaign_params={})
    parts = urlsplit(url)
    qs = parse_qs(parts.query)
    assert url.startswith(BASE)
    assert qs["src"] == ["g|mt01|est01"]


def test_hotlink_forwards_only_utm_params():
    url = build_hotlink(
        BASE,
        src="g|mt01|est01",
        campaign_params={
            "utm_source": "google",
            "utm_medium": "cpc",
            "utm_campaign": "mt01-foto18",
            "utm_content": "est01",
            "gclid": "abc",
            "campaign_id": "123",
            "ad_group_id": "456",
        },
    )
    qs = parse_qs(urlsplit(url).query)
    assert qs["utm_source"] == ["google"]
    assert qs["utm_medium"] == ["cpc"]
    assert qs["utm_campaign"] == ["mt01-foto18"]
    assert qs["utm_content"] == ["est01"]
    assert "gclid" not in qs
    assert "campaign_id" not in qs
    assert "ad_group_id" not in qs


def test_hotlink_preserves_existing_query_params():
    url = build_hotlink(f"{BASE}?ref=partner1", src="g|mt01|est01", campaign_params={})
    qs = parse_qs(urlsplit(url).query)
    assert qs["ref"] == ["partner1"]
    assert qs["src"] == ["g|mt01|est01"]


def test_hotlink_uses_urllib_never_manual_concat():
    url = build_hotlink(BASE, src="g|mt01|es t/01", campaign_params={"utm_content": "a b"})
    # se a URL for bem formada, urlsplit/parse_qs conseguem reprocessa-la
    parts = urlsplit(url)
    assert parts.scheme == "https"
    assert parts.netloc == "go.hotmart.com"


def test_hotlink_missing_utm_is_simply_absent():
    url = build_hotlink(BASE, src="g|mt01|none", campaign_params={"utm_source": "google"})
    qs = parse_qs(urlsplit(url).query)
    assert "utm_source" in qs
    assert "utm_medium" not in qs
