from pathlib import Path

from trevo_instagram.config import Config, load_dotenv


def test_config_without_token_has_no_credentials():
    config = Config()
    assert config.has_credentials is False
    assert config.access_token is None


def test_config_with_token_has_credentials():
    config = Config(access_token="fake-token", ig_user_id="12345")
    assert config.has_credentials is True


def test_config_repr_never_contains_raw_token():
    config = Config(access_token="super-secret-value", ig_user_id="12345")
    text = repr(config)
    assert "super-secret-value" not in text
    assert "PRESENTE" in text
    text_str = str(config)
    assert "super-secret-value" not in text_str


def test_config_repr_without_token_says_ausente():
    config = Config()
    assert "AUSENTE" in repr(config)


def test_config_base_url_uses_host_and_version():
    config = Config(api_host="graph.instagram.com", api_version="v26.0")
    assert config.base_url == "https://graph.instagram.com/v26.0"


def test_config_from_env_reads_variables(monkeypatch, tmp_path):
    monkeypatch.setenv("INSTAGRAM_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("INSTAGRAM_USER_ID", "999")
    monkeypatch.setenv("INSTAGRAM_ALLOW_PUBLISH", "1")
    config = Config.from_env(dotenv_path=tmp_path / "nonexistent.env")
    assert config.access_token == "tok"
    assert config.ig_user_id == "999"
    assert config.allow_publish_env is True


def test_config_from_env_defaults_allow_publish_false(monkeypatch, tmp_path):
    config = Config.from_env(dotenv_path=tmp_path / "nonexistent.env")
    assert config.allow_publish_env is False


def test_load_dotenv_does_not_override_existing_env(monkeypatch, tmp_path):
    monkeypatch.setenv("INSTAGRAM_USER_ID", "from-shell")
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("INSTAGRAM_USER_ID=from-dotenv\n", encoding="utf-8")
    load_dotenv(dotenv_path)
    import os

    assert os.environ["INSTAGRAM_USER_ID"] == "from-shell"


def test_load_dotenv_sets_unset_variable(monkeypatch, tmp_path):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text("INSTAGRAM_ACCESS_TOKEN=from-dotenv-token\n", encoding="utf-8")
    load_dotenv(dotenv_path)
    import os

    assert os.environ["INSTAGRAM_ACCESS_TOKEN"] == "from-dotenv-token"


def test_load_dotenv_missing_file_is_noop(tmp_path):
    load_dotenv(tmp_path / "does-not-exist.env")  # nao deve lancar exception
