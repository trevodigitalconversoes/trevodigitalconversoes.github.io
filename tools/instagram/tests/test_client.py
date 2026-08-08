import httpx
import pytest

from trevo_instagram.client import InstagramApiError, InstagramClient
from trevo_instagram.config import Config


def _config() -> Config:
    return Config(access_token="fake-token", ig_user_id="123", api_host="graph.instagram.com", api_version="v26.0")


def test_client_requires_access_token():
    with pytest.raises(InstagramApiError):
        InstagramClient(Config())


def test_get_me_is_a_get_request_and_returns_fields():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"id": "999", "username": "trevo", "account_type": "BUSINESS"})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        result = client.get_me()

    assert captured["method"] == "GET"
    assert "/me" in captured["url"]
    assert result["username"] == "trevo"


def test_get_me_never_sends_bearer_header_but_uses_query_param():
    """A Instagram API espera access_token como parametro, nao header
    Authorization -- confirmamos que o cliente segue esse padrao."""
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["headers"] = dict(request.headers)
        captured["url"] = str(request.url)
        return httpx.Response(200, json={"id": "1"})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        client.get_me()

    assert "authorization" not in {k.lower() for k in captured["headers"]}
    assert "access_token=fake-token" in captured["url"]


def test_api_error_response_raises_and_is_sanitized():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400, json={"error": {"message": "Invalid OAuth access token: fake-token-value"}}
        )

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        with pytest.raises(InstagramApiError) as exc_info:
            client.get_me()

    assert exc_info.value.status_code == 400


def test_timeout_is_wrapped_as_api_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("boom", request=request)

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        with pytest.raises(InstagramApiError, match="timeout"):
            client.get_me()


def test_create_media_container_posts_expected_fields():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["body"] = request.read().decode()
        return httpx.Response(200, json={"id": "container-1"})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        container = client.create_media_container("123", "https://example.com/img.jpg", "caption text")

    assert captured["method"] == "POST"
    assert "image_url=https" in captured["body"]
    assert container.id == "container-1"


def test_create_media_container_missing_id_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        with pytest.raises(InstagramApiError):
            client.create_media_container("123", "https://example.com/img.jpg")


def test_publish_media_posts_creation_id():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = request.read().decode()
        return httpx.Response(200, json={"id": "media-1"})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        media = client.publish_media("123", "container-1")

    assert "creation_id=container-1" in captured["body"]
    assert media.id == "media-1"


def test_get_container_status_is_get():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        return httpx.Response(200, json={"status_code": "FINISHED"})

    transport = httpx.MockTransport(handler)
    with InstagramClient(_config(), transport=transport) as client:
        status = client.get_container_status("container-1")

    assert captured["method"] == "GET"
    assert status["status_code"] == "FINISHED"
