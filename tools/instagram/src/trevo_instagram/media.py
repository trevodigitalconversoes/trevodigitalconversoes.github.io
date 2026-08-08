"""Validacao 100% local de midia, sem nenhuma chamada de rede.

Regras verificadas em developers.facebook.com (Instagram Graph API
reference, IG User /media) em 2026-08-08:
  - formato: apenas JPEG e aceito para criar o container de imagem;
  - aspect ratio: entre 4:5 (0.8) e 1.91:1 (~1.91);
  - largura: minimo 320px, maximo 1440px (a Meta reescala fora disso,
    mas fora da faixa e reportado aqui como aviso, nao erro fatal);
  - tamanho maximo de arquivo: 8 MB;
  - espaco de cor: sRGB (a Meta converte automaticamente se nao for).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

MIN_ASPECT_RATIO = 4 / 5  # 0.8 (retrato)
MAX_ASPECT_RATIO = 1.91  # paisagem
MIN_WIDTH_PX = 320
MAX_WIDTH_PX = 1440
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024


@dataclass
class MediaValidationResult:
    path: Path
    exists: bool
    sha256: str | None = None
    file_size_bytes: int | None = None
    format: str | None = None
    width: int | None = None
    height: int | None = None
    aspect_ratio: float | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid_for_publish(self) -> bool:
        return self.exists and not self.errors


def _sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_media(path: Path) -> MediaValidationResult:
    if not path.exists():
        return MediaValidationResult(
            path=path, exists=False, errors=[f"arquivo nao encontrado: {path}"]
        )

    file_size = path.stat().st_size
    sha256 = _sha256_of(path)
    result = MediaValidationResult(
        path=path, exists=True, sha256=sha256, file_size_bytes=file_size
    )

    if file_size > MAX_FILE_SIZE_BYTES:
        result.errors.append(
            f"arquivo tem {file_size} bytes, acima do maximo de "
            f"{MAX_FILE_SIZE_BYTES} bytes (8 MB) para publicacao de imagem"
        )

    try:
        with Image.open(path) as img:
            result.format = img.format
            result.width, result.height = img.size
            result.aspect_ratio = round(img.width / img.height, 4)
            mode = img.mode
    except Exception as exc:  # noqa: BLE001 - erro de imagem invalida
        result.errors.append(f"nao foi possivel abrir como imagem: {exc}")
        return result

    if result.format != "JPEG":
        result.errors.append(
            f"formato {result.format} nao e aceito para publicacao direta "
            "(a API so aceita JPEG) -- gerar uma versao .jpg antes de publicar"
        )

    if result.aspect_ratio is not None and not (
        MIN_ASPECT_RATIO - 1e-3 <= result.aspect_ratio <= MAX_ASPECT_RATIO + 1e-3
    ):
        result.errors.append(
            f"aspect ratio {result.aspect_ratio} fora da faixa aceita "
            f"({MIN_ASPECT_RATIO:.3f}-{MAX_ASPECT_RATIO})"
        )

    if result.width is not None:
        if result.width < MIN_WIDTH_PX:
            result.warnings.append(
                f"largura {result.width}px abaixo de {MIN_WIDTH_PX}px "
                "(a Meta reescala automaticamente, mas qualidade pode cair)"
            )
        elif result.width > MAX_WIDTH_PX:
            result.warnings.append(
                f"largura {result.width}px acima de {MAX_WIDTH_PX}px "
                "(a Meta reescala automaticamente)"
            )

    if mode not in ("RGB", "RGBA"):
        result.warnings.append(
            f"modo de cor {mode} nao e RGB/RGBA -- confirmar conversao para sRGB"
        )

    return result
