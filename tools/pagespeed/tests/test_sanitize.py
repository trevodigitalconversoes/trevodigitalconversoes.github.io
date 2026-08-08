from __future__ import annotations

from trevo_pagespeed.sanitize import key_fingerprint, redact_text, redact_url


def test_redact_url_removes_key_param():
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&key=AIzaSyFAKEKEY1234567890"
    redacted = redact_url(url)
    assert "AIzaSyFAKEKEY1234567890" not in redacted
    assert "key=%2A%2A%2A" in redacted  # '***' urlencoded
    assert "url=" in redacted


def test_redact_url_preserves_other_params():
    url = "https://example.com/path?strategy=mobile&key=AIzaFAKE1234567890AB"
    redacted = redact_url(url)
    assert "strategy=mobile" in redacted


def test_redact_text_removes_bare_google_key():
    text = "erro ao chamar API com key=AIzaSyABCDEF1234567890abcdefgh"
    redacted = redact_text(text)
    assert "AIzaSyABCDEF1234567890abcdefgh" not in redacted
    assert "AIza***" in redacted


def test_redact_text_without_key_is_unchanged():
    text = "erro generico sem segredo"
    assert redact_text(text) == text


def test_key_fingerprint_absent():
    assert key_fingerprint(None) == "AUSENTE"
    assert key_fingerprint("") == "AUSENTE"


def test_key_fingerprint_stable_and_short():
    fp1 = key_fingerprint("AIzaSameKeyValue1234567890")
    fp2 = key_fingerprint("AIzaSameKeyValue1234567890")
    assert fp1 == fp2
    assert fp1.startswith("sha256:")
    assert "AIzaSameKeyValue1234567890" not in fp1


def test_key_fingerprint_differs_for_different_keys():
    fp1 = key_fingerprint("key-one-AIza1111111111111")
    fp2 = key_fingerprint("key-two-AIza2222222222222")
    assert fp1 != fp2
