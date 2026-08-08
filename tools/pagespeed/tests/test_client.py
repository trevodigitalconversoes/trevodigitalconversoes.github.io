from __future__ import annotations

import json

import httpx
import pytest

from trevo_pagespeed.client import PageSpeedApiError, PageSpeedClient


def _client_with_transport(config, handler, **kwargs) -> PageSpeedClient:
    transport = httpx.MockTransport(handler)
    return PageSpeedClient(config, transport=transport, sleep_fn=lambda _: None, **kwargs)


def test_requires_api_key():
    from trevo_pagespeed.config import Config

    with pytest.raises(PageSpeedApiError):
        PageSpeedClient(Config(api_key=None))


def test_run_pagespeed_success(config, sample_lighthouse_json):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["key"] == config.api_key
        assert request.url.params["strategy"] == "mobile"
        return httpx.Response(200, json=sample_lighthouse_json)

    client = _client_with_transport(config, handler)
    result = client.run_pagespeed("https://example.com", "mobile", ["performance"])
    assert result == sample_lighthouse_json


def test_run_pagespeed_invalid_strategy(config):
    client = _client_with_transport(config, lambda r: httpx.Response(200, json={}))
    with pytest.raises(PageSpeedApiError):
        client.run_pagespeed("https://example.com", "tablet", ["performance"])


def test_run_pagespeed_permanent_error_not_retried(config):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(400, json={"error": {"message": "URL invalida"}})

    client = _client_with_transport(config, handler)
    with pytest.raises(PageSpeedApiError) as exc_info:
        client.run_pagespeed("https://example.com", "mobile", ["performance"])
    assert calls["n"] == 1
    assert "URL invalida" in str(exc_info.value)


def test_run_pagespeed_transient_error_retries_then_succeeds(config, sample_lighthouse_json):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503, json={"error": {"message": "temporariamente indisponivel"}})
        return httpx.Response(200, json=sample_lighthouse_json)

    client = _client_with_transport(config, handler, max_retries=3)
    result = client.run_pagespeed("https://example.com", "mobile", ["performance"])
    assert calls["n"] == 3
    assert result == sample_lighthouse_json


def test_run_pagespeed_transient_error_exhausts_retries(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": {"message": "erro persistente"}})

    client = _client_with_transport(config, handler, max_retries=1)
    with pytest.raises(PageSpeedApiError):
        client.run_pagespeed("https://example.com", "mobile", ["performance"])


def test_run_pagespeed_timeout_retries_then_raises(config):
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out", request=request)

    client = _client_with_transport(config, handler, max_retries=1)
    with pytest.raises(PageSpeedApiError) as exc_info:
        client.run_pagespeed("https://example.com", "mobile", ["performance"])
    assert config.api_key not in str(exc_info.value)


def test_run_pagespeed_error_message_never_leaks_key(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403, json={"error": {"message": f"chave invalida: key={config.api_key}"}}
        )

    client = _client_with_transport(config, handler)
    with pytest.raises(PageSpeedApiError) as exc_info:
        client.run_pagespeed("https://example.com", "mobile", ["performance"])
    assert config.api_key not in str(exc_info.value)


def test_run_pagespeed_invalid_json_response(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not json")

    client = _client_with_transport(config, handler)
    with pytest.raises(PageSpeedApiError):
        client.run_pagespeed("https://example.com", "mobile", ["performance"])


def test_query_crux_success(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "record": {
                    "key": {"formFactor": "PHONE"},
                    "metrics": {
                        "largest_contentful_paint": {"percentiles": {"p75": 2100}},
                    },
                    "collectionPeriod": {"firstDate": {}, "lastDate": {}},
                }
            },
        )

    client = _client_with_transport(config, handler)
    outcome = client.query_crux(url="https://example.com/page")
    assert outcome.status == "PASS"
    assert outcome.data is not None


def test_query_crux_no_data_returns_documented_status(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": {"message": "no data", "status": "NOT_FOUND"}})

    client = _client_with_transport(config, handler)
    outcome = client.query_crux(url="https://example.com/nova-pagina")
    assert outcome.status == "NO_DATA"


def test_query_crux_permission_denied(config):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            json={"error": {"message": "Chrome UX Report API has not been used", "status": "PERMISSION_DENIED"}},
        )

    client = _client_with_transport(config, handler)
    outcome = client.query_crux(origin="https://example.com")
    assert outcome.status == "NOT_ENABLED"


def test_query_crux_requires_exactly_one_target(config):
    client = _client_with_transport(config, lambda r: httpx.Response(200, json={}))
    with pytest.raises(PageSpeedApiError):
        client.query_crux()
    with pytest.raises(PageSpeedApiError):
        client.query_crux(url="a", origin="b")
