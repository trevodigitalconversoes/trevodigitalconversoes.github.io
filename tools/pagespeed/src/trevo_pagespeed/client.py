"""Cliente HTTP isolado para PageSpeed Insights API v5 e Chrome UX Report
(CrUX) API v1. Endpoints confirmados na documentacao oficial do Google em
2026-08-08:

  GET  https://www.googleapis.com/pagespeedonline/v5/runPagespeed
       params: url, key, strategy (mobile|desktop),
               category (repetido: performance, accessibility,
               best-practices, seo), locale.

  POST https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=...
       body (page):   {"url": "..."}
       body (origin): {"origin": "..."}
       -> 404 quando nao ha dados suficientes para o alvo consultado.

Retry so para erros transitorios (timeout, erro de conexao, HTTP 429 e
5xx). Erros permanentes (4xx exceto 429, JSON invalido) nunca sao
mascarados como sucesso nem re-tentados.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from .config import Config
from .sanitize import redact_text, redact_url

_TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


class PageSpeedApiError(RuntimeError):
    """Erro da API, com mensagem sanitizada (sem API key)."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(redact_text(message))
        self.status_code = status_code

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"PageSpeedApiError(status_code={self.status_code}, message={self.args[0]!r})"


@dataclass
class CruxOutcome:
    """Resultado bruto de uma consulta CrUX, ja distinguindo os motivos de
    ausencia de dados exigidos pela etapa 8 do runbook."""

    status: str  # PASS / NO_DATA / NOT_ENABLED / BLOCKED
    data: dict[str, Any] | None
    error: str | None


class PageSpeedClient:
    """Cliente fino e testavel. `transport` permite injetar
    httpx.MockTransport nos testes -- nenhum teste deste pacote deve tocar
    a rede real."""

    def __init__(
        self,
        config: Config,
        transport: httpx.BaseTransport | None = None,
        *,
        max_retries: int = 2,
        retry_backoff_seconds: float = 1.0,
        sleep_fn=time.sleep,
    ):
        if not config.api_key:
            raise PageSpeedApiError("GOOGLE_PAGESPEED_API_KEY ausente na configuracao")
        self._config = config
        self._client = httpx.Client(timeout=config.timeout_seconds, transport=transport)
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds
        self._sleep = sleep_fn

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "PageSpeedClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _get_with_retry(self, url: str, params: dict[str, Any]) -> httpx.Response:
        last_error: Exception | None = None
        attempts = self._max_retries + 1
        for attempt in range(attempts):
            try:
                response = self._client.get(url, params=params)
            except httpx.TimeoutException as exc:
                last_error = exc
                if attempt < attempts - 1:
                    self._sleep(self._retry_backoff_seconds * (attempt + 1))
                    continue
                raise PageSpeedApiError(f"timeout chamando {redact_url(str(exc))}") from exc
            except httpx.HTTPError as exc:
                raise PageSpeedApiError(
                    f"erro de rede chamando a API: {redact_text(str(exc))}"
                ) from exc

            if response.status_code in _TRANSIENT_STATUS_CODES and attempt < attempts - 1:
                self._sleep(self._retry_backoff_seconds * (attempt + 1))
                continue
            return response
        # So chega aqui se todas as tentativas deram timeout.
        raise PageSpeedApiError("timeout apos todas as tentativas") from last_error

    def _post_with_retry(self, url: str, json_body: dict[str, Any]) -> httpx.Response:
        last_error: Exception | None = None
        attempts = self._max_retries + 1
        for attempt in range(attempts):
            try:
                response = self._client.post(url, json=json_body)
            except httpx.TimeoutException as exc:
                last_error = exc
                if attempt < attempts - 1:
                    self._sleep(self._retry_backoff_seconds * (attempt + 1))
                    continue
                raise PageSpeedApiError(f"timeout chamando {redact_url(str(exc))}") from exc
            except httpx.HTTPError as exc:
                raise PageSpeedApiError(
                    f"erro de rede chamando a API: {redact_text(str(exc))}"
                ) from exc

            if response.status_code in _TRANSIENT_STATUS_CODES and attempt < attempts - 1:
                self._sleep(self._retry_backoff_seconds * (attempt + 1))
                continue
            return response
        raise PageSpeedApiError("timeout apos todas as tentativas") from last_error

    def run_pagespeed(
        self,
        url: str,
        strategy: str,
        categories: list[str],
        locale: str = "pt-BR",
    ) -> dict[str, Any]:
        """GET runPagespeed. Retorna o JSON bruto. Nunca mascara erro
        permanente como sucesso: HTTP >= 400 sempre levanta
        PageSpeedApiError."""
        if strategy not in ("mobile", "desktop"):
            raise PageSpeedApiError(f"strategy invalida: {strategy!r}")

        endpoint = f"{self._config.pagespeed_base_url}/runPagespeed"
        params: dict[str, Any] = {
            "url": url,
            "key": self._config.api_key,
            "strategy": strategy,
            "category": categories,
            "locale": locale,
        }
        response = self._get_with_retry(endpoint, params)
        return self._parse_json_or_raise(response)

    def query_crux(self, *, url: str | None = None, origin: str | None = None) -> CruxOutcome:
        """POST records:queryRecord. Distingue os casos exigidos pela
        etapa 8: sem dados suficientes (404) vs API/chave sem permissao
        (403/PERMISSION_DENIED) vs API nao habilitada (403 com mensagem de
        API desabilitada, ou 404 generico do proprio host) vs sucesso."""
        if bool(url) == bool(origin):
            raise PageSpeedApiError("query_crux exige exatamente um de url/origin")

        endpoint = f"{self._config.crux_base_url}/records:queryRecord"
        body: dict[str, Any] = {"url": url} if url else {"origin": origin}

        try:
            response = self._client.post(
                f"{endpoint}?key={self._config.api_key}", json=body
            )
        except httpx.TimeoutException as exc:
            return CruxOutcome(status="BLOCKED", data=None, error=f"timeout: {exc}")
        except httpx.HTTPError as exc:
            return CruxOutcome(status="BLOCKED", data=None, error=redact_text(str(exc)))

        if response.status_code == 200:
            try:
                return CruxOutcome(status="PASS", data=response.json(), error=None)
            except ValueError:
                return CruxOutcome(
                    status="BLOCKED", data=None, error="resposta CrUX nao-JSON"
                )

        try:
            body_json = response.json()
            message = body_json.get("error", {}).get("message", response.text)
            reason = body_json.get("error", {}).get("status", "")
        except ValueError:
            message = response.text
            reason = ""

        message = redact_text(message)

        if response.status_code == 404:
            return CruxOutcome(status="NO_DATA", data=None, error=message)
        if response.status_code == 403 or "PERMISSION_DENIED" in reason:
            if "has not been used" in message or "is disabled" in message:
                return CruxOutcome(status="NOT_ENABLED", data=None, error=message)
            return CruxOutcome(status="NOT_ENABLED", data=None, error=message)
        return CruxOutcome(status="BLOCKED", data=None, error=f"{response.status_code}: {message}")

    def _parse_json_or_raise(self, response: httpx.Response) -> dict[str, Any]:
        if response.status_code >= 400:
            try:
                body = response.json()
                message = body.get("error", {}).get("message", response.text)
            except ValueError:
                message = response.text
            raise PageSpeedApiError(redact_text(message), status_code=response.status_code)
        try:
            return response.json()
        except ValueError as exc:
            raise PageSpeedApiError("resposta nao-JSON da API") from exc
