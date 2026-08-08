"""Regressao: media_url com sintaxe Markdown, escape de regex indevido,
objeto do PowerShell serializado, hostname ausente ou string vazia
devem ser rejeitados por is_public_http_url() -- e por consequencia por
prepare(), sem nunca chegar a rede.
"""

from trevo_instagram.publishing import is_public_http_url

VALID_RAW_GITHUB_URL = (
    "https://raw.githubusercontent.com/trevodigitalconversoes/"
    "trevodigitalconversoes.github.io/feature/claude/"
    "migrar-presell-fotografia-trevo/assets/social/post-02-institucional.jpg"
)


def test_accepts_valid_raw_githubusercontent_url():
    ok, error = is_public_http_url(VALID_RAW_GITHUB_URL)
    assert ok is True
    assert error is None


def test_rejects_markdown_link_syntax():
    url = f"[{VALID_RAW_GITHUB_URL}]({VALID_RAW_GITHUB_URL})"
    ok, error = is_public_http_url(url)
    assert ok is False
    assert error is not None


def test_rejects_backslash_escaped_dot_in_host():
    url = "https://raw\\.githubusercontent.com/a/b.jpg"
    ok, error = is_public_http_url(url)
    assert ok is False
    assert "\\" in error or "regex" in error.lower()


def test_rejects_powershell_internalhost_object_string():
    url = "https://System.Management.Automation.Internal.Host.InternalHost/a/b.jpg"
    ok, error = is_public_http_url(url)
    assert ok is False
    assert "powershell" in error.lower()


def test_rejects_url_without_scheme():
    ok, error = is_public_http_url("raw.githubusercontent.com/a/b.jpg")
    assert ok is False


def test_rejects_empty_string():
    ok, error = is_public_http_url("")
    assert ok is False


def test_rejects_whitespace_only_string():
    ok, error = is_public_http_url("   ")
    assert ok is False


def test_rejects_none():
    ok, error = is_public_http_url(None)
    assert ok is False


def test_rejects_leading_trailing_whitespace():
    ok, error = is_public_http_url(f"  {VALID_RAW_GITHUB_URL}  ")
    assert ok is False
    assert "espaço" in error or "espaco" in error.lower() or "branco" in error.lower()


def test_rejects_localhost():
    ok, error = is_public_http_url("http://localhost:8080/img.jpg")
    assert ok is False


def test_rejects_127_0_0_1():
    ok, error = is_public_http_url("http://127.0.0.1/img.jpg")
    assert ok is False


def test_rejects_file_scheme():
    ok, error = is_public_http_url("file:///C:/img.jpg")
    assert ok is False


def test_rejects_hostname_without_dot():
    ok, error = is_public_http_url("https://localhostbutnotcaught/img.jpg")
    assert ok is False


def test_individual_forbidden_characters_are_each_rejected():
    for bad in ["[", "]", "(", ")", "\\"]:
        url = f"https://example.com/a{bad}b.jpg"
        ok, error = is_public_http_url(url)
        assert ok is False, f"deveria rejeitar URL contendo {bad!r}"
