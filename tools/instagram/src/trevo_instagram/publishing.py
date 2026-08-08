"""Fluxo de preparacao e publicacao. `prepare` nunca faz rede mutavel.
`publish` exige dupla confirmacao mecanica antes de qualquer chamada que
mute a conta (criar container / media_publish).
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from .client import InstagramApiError, InstagramClient
from .config import Config
from .media import MediaValidationResult, validate_media
from .models import Manifest, PublishState
from .state import PublicationRecord, StateStore

_LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}  # noqa: S104 (comparacao, nao bind)

# Caracteres que nunca devem aparecer numa media_url real. Cobre o caso
# classico de colar um link Markdown inteiro (`[texto](url)`) em vez da
# URL pura, e barras invertidas (nunca validas em URL http(s) -- em
# particular `raw\.githubusercontent.com` e um erro de digitacao onde
# alguem tentou escapar o ponto como se estivesse escrevendo uma regex).
_FORBIDDEN_URL_CHARS = ("[", "]", "(", ")", "\\")

# Fragmentos que indicam que um objeto do PowerShell (ex.: $Host, que e
# a variavel automatica somente-leitura do console, nao uma string) foi
# serializado/interpolado por engano no lugar de uma URL de verdade.
_POWERSHELL_OBJECT_MARKERS = (
    "system.management.automation",
    "internalhost",
)


class PublishNotConfirmedError(RuntimeError):
    """Levantado quando publish() e chamado sem as duas confirmacoes
    mecanicas exigidas. Isso deve acontecer ANTES de qualquer chamada
    de rede mutavel."""


class PublishBlockedError(RuntimeError):
    """Levantado quando o plano de publicacao nao esta pronto (media
    invalida, URL publica ausente, ja publicado, etc.)."""


def is_public_http_url(url: str | None) -> tuple[bool, str | None]:
    """Valida que `url` e uma URL http(s) publica plausivel para a Meta
    buscar via fetch. Rejeita explicitamente os erros de configuracao
    mais comuns (link Markdown colado por engano, hostname com barra
    invertida de um escape de regex mal aplicado, objeto do PowerShell
    serializado, host local, string vazia/so espaco).

    Retorna (ok, motivo_do_erro_ou_None). Nunca lanca excecao -- quem
    chama decide o que fazer com o resultado (ver `prepare`/`publish`).
    """
    if url is None:
        return False, "media_url ausente no manifesto"

    stripped = url.strip()
    if not stripped:
        return False, "media_url ausente ou em branco no manifesto"
    if stripped != url:
        return False, "media_url tem espaco em branco no inicio/fim -- provavel erro de copia/cola"

    for bad_char in _FORBIDDEN_URL_CHARS:
        if bad_char in url:
            return False, (
                f"media_url contem o caractere {bad_char!r}, inaceitavel numa URL "
                "http(s) -- parece um link Markdown colado por engano "
                "(`[texto](url)`) ou um escape de regex (`\\.`) aplicado a uma "
                "URL literal. Use a URL pura, sem colchetes/parenteses/barra invertida."
            )

    lowered = url.lower()
    for marker in _POWERSHELL_OBJECT_MARKERS:
        if marker in lowered:
            return False, (
                f"media_url contem {marker!r}, que parece um objeto do PowerShell "
                "(ex.: $Host, a variavel automatica somente-leitura do console) "
                "serializado por engano no lugar de uma URL. Construa a URL como "
                "string pura -- nunca use `$host`/`$Host` como nome de variavel, "
                "esse nome e reservado pelo PowerShell."
            )

    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        return False, f"media_url deve ser http(s), recebido esquema {parts.scheme!r}"

    hostname = (parts.hostname or "").lower()
    if not hostname:
        return False, "media_url sem hostname valido"
    if hostname in _LOCAL_HOSTS or hostname.endswith(".local"):
        return False, f"media_url aponta para host local ({hostname}) -- inaceitavel para publicacao real"
    if "." not in hostname:
        return False, f"hostname {hostname!r} nao parece um dominio valido (sem ponto)"

    return True, None


# Alias retrocompativel -- codigo interno usava este nome antes da
# validacao ser reforcada e exportada como API publica reutilizavel.
_is_public_http_url = is_public_http_url


@dataclass
class PreparePlan:
    manifest_path: Path
    account_name: str
    asset_path: Path
    media: MediaValidationResult
    caption: str
    alt_text: str | None
    media_url: str | None
    publication_hash: str
    blockers: list[str] = field(default_factory=list)
    already_published: bool = False

    @property
    def status(self) -> PublishState:
        if self.already_published:
            return PublishState.PUBLISHED
        if self.blockers:
            return PublishState.BLOCKED
        return PublishState.READY

    def to_dict(self) -> dict:
        return {
            "manifest_path": str(self.manifest_path),
            "account_name": self.account_name,
            "asset_path": str(self.asset_path),
            "asset_sha256": self.media.sha256,
            "asset_format": self.media.format,
            "asset_width": self.media.width,
            "asset_height": self.media.height,
            "asset_aspect_ratio": self.media.aspect_ratio,
            "media_errors": self.media.errors,
            "media_warnings": self.media.warnings,
            "caption_preview": (self.caption[:120] + "...")
            if len(self.caption) > 120
            else self.caption,
            "alt_text": self.alt_text,
            "media_url": self.media_url,
            "publication_hash": self.publication_hash,
            "status": self.status.value,
            "blockers": self.blockers,
        }


def _publication_hash(asset_sha256: str, caption: str, account_name: str) -> str:
    digest = hashlib.sha256()
    digest.update(asset_sha256.encode("utf-8"))
    digest.update(caption.encode("utf-8"))
    digest.update(account_name.encode("utf-8"))
    return digest.hexdigest()[:16]


def prepare(manifest: Manifest, state_store: StateStore) -> PreparePlan:
    """Somente leitura local: resolve caminhos, valida a imagem, calcula
    hashes, monta o plano. NUNCA chama a API da Meta."""
    asset_path = manifest.post.resolve_asset_path(manifest.base_dir)
    media = validate_media(asset_path)
    caption = manifest.post.resolve_caption(manifest.base_dir)

    blockers: list[str] = list(media.errors)

    media_url_ok, media_url_error = _is_public_http_url(manifest.post.media_url)
    if not media_url_ok:
        blockers.append(media_url_error or "media_url invalida")

    asset_sha = media.sha256 or "sem-hash"
    pub_hash = _publication_hash(asset_sha, caption, manifest.account.name)

    already_published = state_store.is_already_published(pub_hash)

    return PreparePlan(
        manifest_path=manifest.source_path,
        account_name=manifest.account.name,
        asset_path=asset_path,
        media=media,
        caption=caption,
        alt_text=manifest.post.alt_text,
        media_url=manifest.post.media_url,
        publication_hash=pub_hash,
        blockers=blockers,
        already_published=already_published,
    )


def publish(
    manifest: Manifest,
    config: Config,
    state_store: StateStore,
    *,
    confirm_publish_flag: bool,
    allow_duplicate: bool = False,
    poll_status: bool = True,
    poll_attempts: int = 5,
    poll_delay_seconds: float = 2.0,
) -> PublicationRecord:
    """Publica de verdade. So chega a fazer POST se AMBAS as protecoes
    estiverem presentes:
      1) confirm_publish_flag (--confirm-publish na CLI)
      2) config.allow_publish_env (INSTAGRAM_ALLOW_PUBLISH=1 no ambiente)
    Sem as duas, aborta antes de qualquer chamada de rede mutavel.
    """
    if not (confirm_publish_flag and config.allow_publish_env):
        raise PublishNotConfirmedError(
            "publicacao bloqueada: exige --confirm-publish E "
            "INSTAGRAM_ALLOW_PUBLISH=1 simultaneamente. "
            f"confirm_publish_flag={confirm_publish_flag}, "
            f"INSTAGRAM_ALLOW_PUBLISH={config.allow_publish_env}"
        )

    plan = prepare(manifest, state_store)

    if plan.already_published and not allow_duplicate:
        raise PublishBlockedError(
            f"manifesto ja publicado antes (hash={plan.publication_hash}); "
            "use allow_duplicate para forcar republicacao"
        )

    if plan.blockers and not (plan.already_published and allow_duplicate):
        raise PublishBlockedError(
            f"plano de publicacao bloqueado: {'; '.join(plan.blockers)}"
        )

    if not config.has_credentials:
        raise PublishBlockedError("credenciais ausentes (access_token/ig_user_id)")

    assert plan.media_url is not None  # garantido por prepare() sem blockers
    assert config.ig_user_id is not None

    record = PublicationRecord(
        publication_hash=plan.publication_hash,
        manifest_path=str(plan.manifest_path),
        asset_sha256=plan.media.sha256 or "",
        caption_sha256=hashlib.sha256(plan.caption.encode("utf-8")).hexdigest(),
        status=PublishState.CONTAINER_CREATED.value,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    try:
        with InstagramClient(config) as client:
            container = client.create_media_container(
                config.ig_user_id, plan.media_url, plan.caption
            )
            record.container_id = container.id
            state_store.save(record)

            if poll_status:
                for _ in range(poll_attempts):
                    status = client.get_container_status(container.id)
                    code = status.get("status_code")
                    if code == "FINISHED":
                        break
                    if code in ("ERROR", "EXPIRED"):
                        record.status = PublishState.FAILED.value
                        record.error = f"container status={code}"
                        state_store.save(record)
                        raise PublishBlockedError(f"container falhou: status={code}")
                    time.sleep(poll_delay_seconds)

            media = client.publish_media(config.ig_user_id, container.id)
            record.media_id = media.id
            record.status = PublishState.PUBLISHED.value
            state_store.save(record)
            return record
    except InstagramApiError as exc:
        record.status = PublishState.FAILED.value
        record.error = str(exc)
        state_store.save(record)
        raise
