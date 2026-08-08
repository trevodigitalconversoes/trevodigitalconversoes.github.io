"""Controle local simples de publicacao, para evitar duplicar posts por
engano. Sem banco de dados -- um arquivo JSON por hash de publicacao,
dentro de um diretorio ignorado pelo Git (.instagram-state/).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class PublicationRecord:
    publication_hash: str
    manifest_path: str
    asset_sha256: str
    caption_sha256: str
    status: str
    container_id: str | None = None
    media_id: str | None = None
    timestamp: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class StateStore:
    def __init__(self, state_dir: Path):
        self._dir = state_dir
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, publication_hash: str) -> Path:
        return self._dir / f"{publication_hash}.json"

    def get(self, publication_hash: str) -> PublicationRecord | None:
        path = self._path_for(publication_hash)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return PublicationRecord(**data)

    def save(self, record: PublicationRecord) -> None:
        path = self._path_for(record.publication_hash)
        path.write_text(
            json.dumps(record.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def is_already_published(self, publication_hash: str) -> bool:
        record = self.get(publication_hash)
        return record is not None and record.status == "PUBLISHED"
