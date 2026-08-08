from pathlib import Path

from trevo_instagram.media import validate_media


def test_missing_file_reports_error(tmp_path: Path):
    result = validate_media(tmp_path / "nope.jpg")
    assert result.exists is False
    assert result.is_valid_for_publish is False
    assert "nao encontrado" in result.errors[0]


def test_valid_jpeg_passes(valid_jpeg: Path):
    result = validate_media(valid_jpeg)
    assert result.is_valid_for_publish is True
    assert result.format == "JPEG"
    assert result.aspect_ratio == 0.8
    assert result.sha256 is not None
    assert len(result.sha256) == 64


def test_png_is_rejected_for_publish(valid_png: Path):
    result = validate_media(valid_png)
    assert result.is_valid_for_publish is False
    assert any("JPEG" in e for e in result.errors)


def test_bad_aspect_ratio_is_rejected(bad_aspect_jpeg: Path):
    result = validate_media(bad_aspect_jpeg)
    assert result.is_valid_for_publish is False
    assert any("aspect ratio" in e for e in result.errors)


def test_hash_is_deterministic(valid_jpeg: Path):
    r1 = validate_media(valid_jpeg)
    r2 = validate_media(valid_jpeg)
    assert r1.sha256 == r2.sha256
