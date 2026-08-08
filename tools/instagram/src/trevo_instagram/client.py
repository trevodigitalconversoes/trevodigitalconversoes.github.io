"""Cliente HTTP isolado para a Instagram API (Instagram API with Instagram
Login). Host/versao centralizados em Config -- nunca hardcoded em mais de
um lugar. Todo erro e sanitizado antes de propagar.

Endpoints usados (verificados em developers.facebook.com em 2026-08-08):
  GET  /{version}/me?fields=...                         -> inspect
  POST /{version}/{ig_user_id}/media                     -> criar container
  GET  /{version}/{container_id}?fields=status_code      -> status
  POST /{version}/{ig_user_id}/media_publish              -> publicar
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from .config import Config
from .sanitize import redact_text, redact_url


class InstagramApiError(RuntimeError):
    """Erro da API, com mensagem sanitizada (sem token/segredo)."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(redact_text(message))
        self.status_code = status_code

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"InstagramApiError(status_code={self.status_code}, message={self.args[0]!r})"


@dataclass
class MediaContainer:
    id: str


@dataclass
class PublishedMedia:
    id: str


class InstagramClient:
    """Cliente fino e testavel. Todas as chamadas mutaveis (create_media_
    container, publish_media) devem ser chamadas apenas pelo modulo de
    publishing, depois de todas as salvaguardas terem sido checadas."""

    def __init__(self, config: Config, transport: httpx.BaseTransport | None = None):
        if not config.access_token:
            raise InstagramApiError("access_token ausente na configuracao")
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout_seconds,
            transport=transport,
            follow_redirects=False,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "InstagramClient":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _auth_params(self) -> dict[str, str]:
        assert self._config.access_token is not None
        return {"access_token": self._config.access_token}

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self._client.request(method, path, **kwargs)
        except httpx.TimeoutException as exc:
            raise InstagramApiError(f"timeout chamando {redact_url(path)}") from exc
        except httpx.HTTPError as exc:
            raise InstagramApiError(
                f"erro de rede chamando {redact_url(path)}: {redact_text(str(exc))}"
            ) from exc

        if response.status_code >= 400:
            # A API da Meta normalmente retorna {"error": {"message": ...}}
            try:
                body = response.json()
                message = body.get("error", {}).get("message", response.text)
            except ValueError:
                message = response.text
            raise InstagramApiError(
                redact_text(message), status_code=response.status_code
            )

        try:
            return response.json()
        except ValueError as exc:
            raise InstagramApiError("resposta nao-JSON da API") from exc

    # ---- Read-only ----

    def get_me(self, fields: str = "id,username,account_type") -> dict[str, Any]:
        """GET /me -- somente leitura. Usado por `inspect`."""
        params = {"fields": fields, **self._auth_params()}
        return self._request("GET", "/me", params=params)

    def get_container_status(self, container_id: str) -> dict[str, Any]:
        """GET /{container_id}?fields=status_code -- somente leitura."""
        params = {"fields": "status_code", **self._auth_params()}
        return self._request("GET", f"/{container_id}", params=params)

    # ---- Mutavel: NUNCA chamar fora do fluxo de publishing.publish() ----

    def create_media_container(
        self, ig_user_id: str, image_url: str, caption: str = ""
    ) -> MediaContainer:
        data = {"image_url": image_url, "caption": caption, **self._auth_params()}
        result = self._request("POST", f"/{ig_user_id}/media", data=data)
        container_id = result.get("id")
        if not container_id:
            raise InstagramApiError(f"resposta sem 'id' ao criar container: {result}")
        return MediaContainer(id=container_id)

    def publish_media(self, ig_user_id: str, creation_id: str) -> PublishedMedia:
        data = {"creation_id": creation_id, **self._auth_params()}
        result = self._request("POST", f"/{ig_user_id}/media_publish", data=data)
        media_id = result.get("id")
        if not media_id:
            raise InstagramApiError(f"resposta sem 'id' ao publicar: {result}")
        return PublishedMedia(id=media_id)
