from trevo_instagram.sanitize import (
    redact_mapping,
    redact_text,
    redact_url,
    token_fingerprint,
)


def test_redact_url_hides_access_token():
    url = "https://graph.instagram.com/v26.0/me?fields=id&access_token=SECRET123"
    redacted = redact_url(url)
    assert "SECRET123" not in redacted
    assert "access_token=%2A%2A%2A" in redacted or "access_token=***" in redacted
    assert "fields=id" in redacted


def test_redact_text_hides_bearer_token():
    text = "request failed: Authorization: Bearer abc.def-ghi_123"
    redacted = redact_text(text)
    assert "abc.def-ghi_123" not in redacted
    assert "Bearer ***" in redacted


def test_redact_mapping_hides_secret_keys():
    data = {"access_token": "SECRET", "caption": "hello", "app_secret": "S2"}
    redacted = redact_mapping(data)
    assert redacted["access_token"] == "***"
    assert redacted["app_secret"] == "***"
    assert redacted["caption"] == "hello"


def test_token_fingerprint_never_reversible_and_stable():
    fp1 = token_fingerprint("my-token")
    fp2 = token_fingerprint("my-token")
    fp3 = token_fingerprint("other-token")
    assert fp1 == fp2
    assert fp1 != fp3
    assert "my-token" not in fp1
    assert fp1.startswith("sha256:")


def test_token_fingerprint_absent():
    assert token_fingerprint(None) == "AUSENTE"
    assert token_fingerprint("") == "AUSENTE"
