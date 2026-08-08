from __future__ import annotations

import os
from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture(autouse=True)
def _clean_instagram_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Garante que testes nunca herdem credenciais reais do ambiente do
    desenvolvedor por acidente."""
    for key in (
        "INSTAGRAM_ACCESS_TOKEN",
        "INSTAGRAM_USER_ID",
        "INSTAGRAM_API_HOST",
        "INSTAGRAM_API_VERSION",
        "INSTAGRAM_TIMEOUT_SECONDS",
        "INSTAGRAM_ALLOW_PUBLISH",
    ):
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def valid_jpeg(tmp_path: Path) -> Path:
    path = tmp_path / "valid.jpg"
    img = Image.new("RGB", (1080, 1350), color=(10, 20, 30))
    img.save(path, "JPEG", quality=90)
    return path


@pytest.fixture
def valid_png(tmp_path: Path) -> Path:
    path = tmp_path / "valid.png"
    img = Image.new("RGB", (1080, 1350), color=(10, 20, 30))
    img.save(path, "PNG")
    return path


@pytest.fixture
def bad_aspect_jpeg(tmp_path: Path) -> Path:
    path = tmp_path / "bad_aspect.jpg"
    img = Image.new("RGB", (1080, 400), color=(10, 20, 30))  # aspect ~2.7, fora da faixa
    img.save(path, "JPEG", quality=90)
    return path
