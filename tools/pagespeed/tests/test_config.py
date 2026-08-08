from __future__ import annotations

from pathlib import Path

from trevo_pagespeed.config import Config, load_dotenv


def test_from_env_missing_key(monkeypatch, tmp_path):
    monkeypatch.delenv("GOOGLE_PAGESPEED_API_KEY", raising=False)
    config = Config.from_env(dotenv_path=tmp_path / "does-not-exist.env")
    assert config.api_key is None
    assert config.has_credentials is False


def test_from_env_reads_dotenv(monkeypatch, tmp_path):
    monkeypatch.delenv("GOOGLE_PAGESPEED_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("GOOGLE_PAGESPEED_API_KEY=abc123\n", encoding="utf-8")
    config = Config.from_env(dotenv_path=env_file)
    assert config.api_key == "abc123"
    assert config.has_credentials is True


def test_load_dotenv_does_not_override_existing_env(monkeypatch, tmp_path):
    monkeypatch.setenv("GOOGLE_PAGESPEED_API_KEY", "already-set")
    env_file = tmp_path / ".env"
    env_file.write_text("GOOGLE_PAGESPEED_API_KEY=from-file\n", encoding="utf-8")
    load_dotenv(env_file)
    import os

    assert os.environ["GOOGLE_PAGESPEED_API_KEY"] == "already-set"


def test_load_dotenv_missing_file_is_noop(tmp_path):
    load_dotenv(tmp_path / "nope.env")  # nao deve lancar


def test_load_dotenv_ignores_comments_and_blank_lines(monkeypatch, tmp_path):
    monkeypatch.delenv("GOOGLE_PAGESPEED_API_KEY", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "# comentario\n\nGOOGLE_PAGESPEED_API_KEY=xyz\n# outro comentario\n",
        encoding="utf-8",
    )
    load_dotenv(env_file)
    import os

    assert os.environ["GOOGLE_PAGESPEED_API_KEY"] == "xyz"


def test_repr_never_leaks_key():
    config = Config(api_key="super-secret-value")
    text = repr(config)
    text_str = str(config)
    assert "super-secret-value" not in text
    assert "super-secret-value" not in text_str
    assert "PRESENTE" in text


def test_repr_shows_ausente_without_key():
    config = Config(api_key=None)
    assert "AUSENTE" in repr(config)
