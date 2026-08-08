import httpx

from trevo_instagram import auth
from trevo_instagram.config import Config


def test_inspect_without_credentials_is_blocked():
    result = auth.inspect(Config())
    assert result.status == "INSTAGRAM_READ_BLOCKED_MISSING_CREDENTIALS"
    assert result.error is not None


def test_inspect_never_exposes_raw_token_in_result():
    result = auth.inspect(Config(access_token="super-secret", ig_user_id="1"))
    # sem rede real configurada aqui (sem monkeypatch de client), so
    # garantimos que a fingerprint nunca contem o token bruto
    assert "super-secret" not in result.token_fingerprint


def test_inspect_business_account_is_read_ready(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"id": "1", "username": "trevo", "account_type": "BUSINESS"})

    import trevo_instagram.client as client_module

    original_init = client_module.InstagramClient.__init__

    def patched_init(self, config, transport=None):
        original_init(self, config, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(client_module.InstagramClient, "__init__", patched_init)

    result = auth.inspect(Config(access_token="tok", ig_user_id="1"))
    assert result.status == "INSTAGRAM_READ_READY"
    assert result.username == "trevo"


def test_inspect_personal_account_requires_professional(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"id": "1", "username": "trevo", "account_type": "PERSONAL"})

    import trevo_instagram.client as client_module

    original_init = client_module.InstagramClient.__init__

    def patched_init(self, config, transport=None):
        original_init(self, config, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(client_module.InstagramClient, "__init__", patched_init)

    result = auth.inspect(Config(access_token="tok", ig_user_id="1"))
    assert result.status == "INSTAGRAM_PROFESSIONAL_ACCOUNT_REQUIRED"


def test_inspect_api_error_is_blocked(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": {"message": "Invalid token"}})

    import trevo_instagram.client as client_module

    original_init = client_module.InstagramClient.__init__

    def patched_init(self, config, transport=None):
        original_init(self, config, transport=httpx.MockTransport(handler))

    monkeypatch.setattr(client_module.InstagramClient, "__init__", patched_init)

    result = auth.inspect(Config(access_token="tok", ig_user_id="1"))
    assert result.status == "INSTAGRAM_READ_BLOCKED_API_ERROR"
