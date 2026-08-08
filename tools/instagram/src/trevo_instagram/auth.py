"""Inspecao read-only da conta configurada. Nunca faz POST."""

from __future__ import annotations

from dataclasses import dataclass

from .client import InstagramApiError, InstagramClient
from .config import Config
from .sanitize import token_fingerprint

PROFESSIONAL_ACCOUNT_TYPES = {"BUSINESS", "MEDIA_CREATOR"}


@dataclass
class InspectResult:
    status: str
    token_fingerprint: str
    ig_user_id: str | None = None
    username: str | None = None
    account_type: str | None = None
    error: str | None = None

    @property
    def is_ready(self) -> bool:
        return self.status == "INSTAGRAM_READ_READY"


def inspect(config: Config) -> InspectResult:
    """Executa somente chamadas GET/read-only. Nunca imprime o token --
    so uma fingerprint sha256 truncada, para conferencia sem exposicao.
    """
    fingerprint = token_fingerprint(config.access_token)

    if not config.has_credentials:
        return InspectResult(
            status="INSTAGRAM_READ_BLOCKED_MISSING_CREDENTIALS",
            token_fingerprint=fingerprint,
            error=(
                "INSTAGRAM_ACCESS_TOKEN e/ou INSTAGRAM_USER_ID ausentes. "
                "Ver 'AÇÃO SUA' no README para obter as credenciais."
            ),
        )

    try:
        with InstagramClient(config) as client:
            me = client.get_me()
    except InstagramApiError as exc:
        return InspectResult(
            status="INSTAGRAM_READ_BLOCKED_API_ERROR",
            token_fingerprint=fingerprint,
            error=str(exc),
        )

    account_type = me.get("account_type")
    result = InspectResult(
        status="INSTAGRAM_READ_READY",
        token_fingerprint=fingerprint,
        ig_user_id=me.get("id"),
        username=me.get("username"),
        account_type=account_type,
    )

    if account_type and account_type not in PROFESSIONAL_ACCOUNT_TYPES:
        result.status = "INSTAGRAM_PROFESSIONAL_ACCOUNT_REQUIRED"
        result.error = (
            f"account_type={account_type!r} nao e uma conta profissional "
            "(Business/Creator). Transforme a conta manualmente no app do "
            "Instagram antes de prosseguir -- esta ferramenta nao converte "
            "contas automaticamente."
        )

    return result
