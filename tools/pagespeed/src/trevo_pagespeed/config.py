"""Configuracao segura, carregada do ambiente/.env. Nunca hardcoda a chave.

Convencao do repo (ver tools/instagram/src/trevo_instagram/config.py): cada
ferramenta local tem seu proprio .env, nunca commitado, resolvido a partir
da raiz da propria ferramenta (tools/pagespeed/.env).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PAGESPEED_API_HOST = "www.googleapis.com"
DEFAULT_CRUX_API_HOST = "chromeuxreport.googleapis.com"
DEFAULT_TIMEOUT_SECONDS = 30.0


def load_dotenv(path: Path) -> None:
    """Carrega pares KEY=VALUE de um arquivo .env para os.environ, sem
    sobrescrever variaveis ja definidas no ambiente ou ja presentes no
    proprio processo. Parser minimo de proposito -- evita adicionar
    python-dotenv como dependencia so para isso. Nao faz logging do
    conteudo. Se o .env nao existir, e um no-op (o resto do repo nao deve
    quebrar por causa disso)."""
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
    """Configuracao do adaptador. NUNCA logar/imprimir api_key.

    O __repr__ e sobrescrito para nunca vazar a chave, mesmo em tracebacks
    ou logs acidentais que chamem repr(config).
    """

    api_key: str | None = None
    pagespeed_api_host: str = DEFAULT_PAGESPEED_API_HOST
    crux_api_host: str = DEFAULT_CRUX_API_HOST
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    def __repr__(self) -> str:  # pragma: no cover - trivial
        key_state = "PRESENTE" if self.api_key else "AUSENTE"
        return (
            f"Config(api_key={key_state}, "
            f"pagespeed_api_host={self.pagespeed_api_host!r}, "
            f"crux_api_host={self.crux_api_host!r})"
        )

    __str__ = __repr__

    @property
    def has_credentials(self) -> bool:
        return bool(self.api_key)

    @property
    def pagespeed_base_url(self) -> str:
        return f"https://{self.pagespeed_api_host}/pagespeedonline/v5"

    @property
    def crux_base_url(self) -> str:
        return f"https://{self.crux_api_host}/v1"

    @classmethod
    def from_env(cls, dotenv_path: Path | None = None) -> "Config":
        if dotenv_path is None:
            dotenv_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path)
        return cls(
            api_key=os.environ.get("GOOGLE_PAGESPEED_API_KEY") or None,
            pagespeed_api_host=os.environ.get(
                "GOOGLE_PAGESPEED_API_HOST", DEFAULT_PAGESPEED_API_HOST
            ),
            crux_api_host=os.environ.get("GOOGLE_CRUX_API_HOST", DEFAULT_CRUX_API_HOST),
            timeout_seconds=float(
                os.environ.get("GOOGLE_PAGESPEED_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)
            ),
        )
