"""Configuracao carregada do ambiente/.env. Mesma convencao de
tools/instagram e tools/pagespeed: .env local a ferramenta, nunca
commitado.

Nota de seguranca (ver README): POSTHOG_PROJECT_TOKEN NAO e uma Personal
API Key -- e o token de ingestao do SDK web, feito para rodar no
navegador. `Config.__repr__` ainda assim nunca mostra o valor completo em
logs/tracebacks acidentais, por consistencia com o resto do repo -- mas
isso nao o torna secreto: ele e injetado de proposito no JavaScript
publico por `etapa_5_a_v1_generate_tracking_config.py`.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_POSTHOG_HOST = "https://us.i.posthog.com"


def load_dotenv(path: Path) -> None:
    """Carrega pares KEY=VALUE de um arquivo .env para os.environ, sem
    sobrescrever variaveis ja definidas no ambiente. Nao loga o
    conteudo. No-op se o arquivo nao existir."""
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


def token_fingerprint(token: str | None) -> str:
    if not token:
        return "AUSENTE"
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:8]}"


@dataclass
class Config:
    posthog_project_token: str | None = None
    posthog_host: str = DEFAULT_POSTHOG_HOST

    def __repr__(self) -> str:  # pragma: no cover - trivial
        token_state = "PRESENTE" if self.posthog_project_token else "AUSENTE"
        return f"Config(posthog_project_token={token_state}, posthog_host={self.posthog_host!r})"

    __str__ = __repr__

    @property
    def has_token(self) -> bool:
        return bool(self.posthog_project_token)

    @classmethod
    def from_env(cls, dotenv_path: Path | None = None) -> "Config":
        if dotenv_path is None:
            dotenv_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path)
        return cls(
            posthog_project_token=os.environ.get("POSTHOG_PROJECT_TOKEN") or None,
            posthog_host=os.environ.get("POSTHOG_HOST", DEFAULT_POSTHOG_HOST),
        )
