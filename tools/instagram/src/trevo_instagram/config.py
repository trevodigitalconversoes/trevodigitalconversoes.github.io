"""Configuracao segura, carregada do ambiente. Nunca hardcoda segredos."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_API_HOST = "graph.instagram.com"
# Verificado em developers.facebook.com/docs/graph-api/changelog em 2026-08-08:
# versao mais recente publicada pela Meta era v26.0. Configuravel via env --
# nao hardcodar sem revisitar a documentacao oficial antes de mudar o default.
DEFAULT_API_VERSION = "v26.0"
DEFAULT_TIMEOUT_SECONDS = 20.0


def load_dotenv(path: Path) -> None:
    """Carrega pares KEY=VALUE de um arquivo .env para os.environ, sem
    sobrescrever variaveis ja definidas no ambiente. Parser minimo de
    proposito -- evita adicionar python-dotenv como dependencia so para
    isso. Ignora linhas vazias/comentarios. Nao faz logging do conteudo.
    """
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass
class Config:
    """Configuracao do adaptador. NUNCA logar/imprimir access_token.

    O __repr__ e sobrescrito para nunca vazar o token, mesmo em
    tracebacks ou logs acidentais que chamem repr(config).
    """

    access_token: str | None = field(default=None)
    ig_user_id: str | None = field(default=None)
    api_host: str = DEFAULT_API_HOST
    api_version: str = DEFAULT_API_VERSION
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    allow_publish_env: bool = False

    def __repr__(self) -> str:  # pragma: no cover - trivial
        token_state = "PRESENTE" if self.access_token else "AUSENTE"
        return (
            f"Config(access_token={token_state}, "
            f"ig_user_id={self.ig_user_id!r}, "
            f"api_host={self.api_host!r}, api_version={self.api_version!r})"
        )

    __str__ = __repr__

    @property
    def base_url(self) -> str:
        return f"https://{self.api_host}/{self.api_version}"

    @property
    def has_credentials(self) -> bool:
        return bool(self.access_token and self.ig_user_id)

    @classmethod
    def from_env(cls, dotenv_path: Path | None = None) -> "Config":
        if dotenv_path is None:
            dotenv_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path)
        return cls(
            access_token=os.environ.get("INSTAGRAM_ACCESS_TOKEN") or None,
            ig_user_id=os.environ.get("INSTAGRAM_USER_ID") or None,
            api_host=os.environ.get("INSTAGRAM_API_HOST", DEFAULT_API_HOST),
            api_version=os.environ.get("INSTAGRAM_API_VERSION", DEFAULT_API_VERSION),
            timeout_seconds=float(
                os.environ.get("INSTAGRAM_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)
            ),
            allow_publish_env=os.environ.get("INSTAGRAM_ALLOW_PUBLISH") == "1",
        )
