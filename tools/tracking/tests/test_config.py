from __future__ import annotations

import os

from trevo_tracking.config import Config, load_dotenv, token_fingerprint


def test_from_env_missing_token(monkeypatch, tmp_path):
    monkeypatch.delenv("POSTHOG_PROJECT_TOKEN", raising=False)
    config = Config.from_env(dotenv_path=tmp_path / "nope.env")
    assert config.posthog_project_token is None
    assert config.has_token is False


def test_from_env_reads_dotenv(monkeypatch, tmp_path):
    monkeypatch.delenv("POSTHOG_PROJECT_TOKEN", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("POSTHOG_PROJECT_TOKEN=phc_abc123\n", encoding="utf-8")
    config = Config.from_env(dotenv_path=env_file)
    assert config.posthog_project_token == "phc_abc123"
    assert config.has_token is True


def test_load_dotenv_does_not_override_existing_env(monkeypatch, tmp_path):
    monkeypatch.setenv("POSTHOG_PROJECT_TOKEN", "already-set")
    env_file = tmp_path / ".env"
    env_file.write_text("POSTHOG_PROJECT_TOKEN=from-file\n", encoding="utf-8")
    load_dotenv(env_file)
    assert os.environ["POSTHOG_PROJECT_TOKEN"] == "already-set"


def test_repr_never_leaks_token():
    config = Config(posthog_project_token="phc_super_secret_looking_value")
    assert "phc_super_secret_looking_value" not in repr(config)
    assert "phc_super_secret_looking_value" not in str(config)
    assert "PRESENTE" in repr(config)


def test_repr_ausente_without_token():
    assert "AUSENTE" in repr(Config(posthog_project_token=None))


def test_token_fingerprint_absent():
    assert token_fingerprint(None) == "AUSENTE"


def test_token_fingerprint_never_contains_raw_value():
    fp = token_fingerprint("phc_abc123")
    assert "phc_abc123" not in fp
    assert fp.startswith("sha256:")


def test_default_host():
    config = Config(posthog_project_token="x")
    assert config.posthog_host == "https://us.i.posthog.com"
