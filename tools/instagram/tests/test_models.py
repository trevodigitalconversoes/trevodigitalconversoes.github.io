from pathlib import Path

import pytest

from trevo_instagram.models import Manifest, ManifestError


def _write(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "manifest.toml"
    path.write_text(content, encoding="utf-8")
    return path


def test_valid_manifest_loads(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        caption_file = "cap.txt"
        alt_text = "alt"
        media_url = "https://example.com/img.jpg"
        """,
    )
    manifest = Manifest.load(path)
    assert manifest.account.name == "acc"
    assert manifest.post.asset_path == "img.jpg"


def test_missing_manifest_raises(tmp_path: Path):
    with pytest.raises(ManifestError):
        Manifest.load(tmp_path / "missing.toml")


def test_invalid_toml_raises(tmp_path: Path):
    path = _write(tmp_path, "not = [valid toml")
    with pytest.raises(ManifestError):
        Manifest.load(path)


def test_wrong_schema_version_raises(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 2
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        """,
    )
    with pytest.raises(ManifestError):
        Manifest.load(path)


def test_unsupported_post_type_raises(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "carousel"
        asset_path = "img.jpg"
        """,
    )
    with pytest.raises(ManifestError):
        Manifest.load(path)


def test_secret_key_in_manifest_raises(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        access_token = "should-not-be-here"
        """,
    )
    with pytest.raises(ManifestError, match="access_token"):
        Manifest.load(path)


def test_resolve_asset_path_relative_to_manifest_dir(tmp_path: Path):
    (tmp_path / "img.jpg").write_bytes(b"fake")
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        """,
    )
    manifest = Manifest.load(path)
    resolved = manifest.post.resolve_asset_path(manifest.base_dir)
    assert resolved == (tmp_path / "img.jpg").resolve()


def test_resolve_caption_missing_file_raises(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        caption_file = "missing.txt"
        """,
    )
    manifest = Manifest.load(path)
    with pytest.raises(ManifestError):
        manifest.post.resolve_caption(manifest.base_dir)


def test_resolve_caption_empty_when_absent(tmp_path: Path):
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        """,
    )
    manifest = Manifest.load(path)
    assert manifest.post.resolve_caption(manifest.base_dir) == ""


def test_caption_with_unicode_and_hashtags(tmp_path: Path):
    (tmp_path / "cap.txt").write_text(
        "Análise, seleção e divulgação — #trevo #afiliados", encoding="utf-8"
    )
    path = _write(
        tmp_path,
        """
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "img.jpg"
        caption_file = "cap.txt"
        """,
    )
    manifest = Manifest.load(path)
    caption = manifest.post.resolve_caption(manifest.base_dir)
    assert "Análise" in caption
    assert "#trevo" in caption
