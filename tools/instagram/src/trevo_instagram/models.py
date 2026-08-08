"""Modelos de dados: manifesto declarativo de post e estados de publicacao.

O manifesto e dados, nao codigo -- especifico de cada conta/post, mas o
parser/modelo em si nao conhece nada do Trevo alem do que le do TOML.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class PublishState(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    READY = "READY"
    CONTAINER_CREATED = "CONTAINER_CREATED"
    PROCESSING = "PROCESSING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class ManifestError(ValueError):
    """Manifesto invalido ou incompleto."""


@dataclass(frozen=True)
class AccountSpec:
    name: str


@dataclass(frozen=True)
class PostSpec:
    type: str
    asset_path: str
    caption_file: str | None
    alt_text: str | None
    media_url: str | None

    def resolve_asset_path(self, base_dir: Path) -> Path:
        p = Path(self.asset_path)
        return p if p.is_absolute() else (base_dir / p).resolve()

    def resolve_caption(self, base_dir: Path) -> str:
        if not self.caption_file:
            return ""
        p = Path(self.caption_file)
        p = p if p.is_absolute() else (base_dir / p).resolve()
        if not p.exists():
            raise ManifestError(f"caption_file nao encontrado: {p}")
        return p.read_text(encoding="utf-8").strip()


@dataclass(frozen=True)
class Manifest:
    schema_version: int
    account: AccountSpec
    post: PostSpec
    source_path: Path

    @property
    def base_dir(self) -> Path:
        return self.source_path.parent

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        if not path.exists():
            raise ManifestError(f"manifesto nao encontrado: {path}")
        with path.open("rb") as f:
            try:
                data = tomllib.load(f)
            except tomllib.TOMLDecodeError as exc:
                raise ManifestError(f"TOML invalido em {path}: {exc}") from exc

        schema_version = data.get("schema_version")
        if schema_version != 1:
            raise ManifestError(
                f"schema_version nao suportado: {schema_version!r} (esperado 1)"
            )

        account_data = data.get("account")
        if not account_data or not account_data.get("name"):
            raise ManifestError("secao [account] com 'name' e obrigatoria")

        post_data = data.get("post")
        if not post_data:
            raise ManifestError("secao [post] e obrigatoria")

        post_type = post_data.get("type")
        if post_type != "image":
            raise ManifestError(
                f"post.type={post_type!r} nao suportado nesta fatia (so 'image')"
            )

        asset_path = post_data.get("asset_path")
        if not asset_path:
            raise ManifestError("post.asset_path e obrigatorio")

        for forbidden_key in ("access_token", "app_secret", "client_secret", "token"):
            if forbidden_key in post_data or forbidden_key in account_data:
                raise ManifestError(
                    f"manifesto nao deve conter '{forbidden_key}' -- "
                    "segredos vao em variaveis de ambiente, nunca no manifesto"
                )

        return cls(
            schema_version=schema_version,
            account=AccountSpec(name=account_data["name"]),
            post=PostSpec(
                type=post_type,
                asset_path=asset_path,
                caption_file=post_data.get("caption_file"),
                alt_text=post_data.get("alt_text"),
                media_url=post_data.get("media_url"),
            ),
            source_path=path,
        )
