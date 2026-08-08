from pathlib import Path

import httpx
import pytest

from trevo_instagram.client import InstagramClient
from trevo_instagram.config import Config
from trevo_instagram.models import Manifest
from trevo_instagram.publishing import (
    PublishBlockedError,
    PublishNotConfirmedError,
    prepare,
    publish,
)
from trevo_instagram.state import StateStore


def _write_manifest(tmp_path: Path, *, media_url: str, asset_name: str = "img.jpg") -> Path:
    path = tmp_path / "manifest.toml"
    path.write_text(
        f"""
        schema_version = 1
        [account]
        name = "acc"
        [post]
        type = "image"
        asset_path = "{asset_name}"
        caption_file = "cap.txt"
        alt_text = "alt"
        media_url = "{media_url}"
        """,
        encoding="utf-8",
    )
    (tmp_path / "cap.txt").write_text("legenda de teste", encoding="utf-8")
    return path


class TestPrepareNeverHitsNetwork:
    def test_prepare_with_valid_jpeg_and_public_url_is_ready(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "READY"
        assert not plan.blockers

    def test_prepare_rejects_file_url(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="file:///C:/img.jpg")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "BLOCKED"
        assert any("http" in b for b in plan.blockers)

    def test_prepare_rejects_localhost_url(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="http://localhost:8080/img.jpg")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "BLOCKED"
        assert any("local" in b for b in plan.blockers)

    def test_prepare_blocks_missing_media_url(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "BLOCKED"

    def test_prepare_rejects_markdown_wrapped_url(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        raw_url = "https://raw.githubusercontent.com/org/repo/branch/asset.jpg"
        manifest_path = _write_manifest(tmp_path, media_url=f"[{raw_url}]({raw_url})")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "BLOCKED"
        assert any("Markdown" in b or "media_url" in b for b in plan.blockers)

    def test_prepare_accepts_real_raw_githubusercontent_url(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        raw_url = (
            "https://raw.githubusercontent.com/trevodigitalconversoes/"
            "trevodigitalconversoes.github.io/feature/claude/"
            "migrar-presell-fotografia-trevo/assets/social/post-02-institucional.jpg"
        )
        manifest_path = _write_manifest(tmp_path, media_url=raw_url)
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "READY"
        assert plan.media_url == raw_url

    def test_prepare_blocks_png_asset(self, tmp_path, valid_png):
        (tmp_path / "img.jpg").write_bytes(valid_png.read_bytes())  # extensao .jpg, conteudo PNG
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        plan = prepare(manifest, StateStore(tmp_path / "state"))
        assert plan.status.value == "BLOCKED"
        assert any("JPEG" in b for b in plan.blockers)


class TestPublishSafeguards:
    def test_publish_without_any_confirmation_is_blocked_before_network(self, tmp_path, valid_jpeg, monkeypatch):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=False)

        def fail_if_called(*args, **kwargs):
            raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")

        monkeypatch.setattr(InstagramClient, "create_media_container", fail_if_called)

        with pytest.raises(PublishNotConfirmedError):
            publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=False,
            )

    def test_publish_with_only_cli_flag_is_blocked(self, tmp_path, valid_jpeg, monkeypatch):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=False)

        def fail_if_called(*args, **kwargs):
            raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")

        monkeypatch.setattr(InstagramClient, "create_media_container", fail_if_called)

        with pytest.raises(PublishNotConfirmedError):
            publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=True,  # so uma das duas protecoes
            )

    def test_publish_with_only_env_flag_is_blocked(self, tmp_path, valid_jpeg, monkeypatch):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=True)  # so a outra

        def fail_if_called(*args, **kwargs):
            raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")

        monkeypatch.setattr(InstagramClient, "create_media_container", fail_if_called)

        with pytest.raises(PublishNotConfirmedError):
            publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=False,
            )

    def test_publish_with_both_confirmations_reaches_mutable_client(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=True)

        calls = {"container": 0, "publish": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/media") and request.method == "POST":
                calls["container"] += 1
                return httpx.Response(200, json={"id": "container-1"})
            if request.url.path.endswith("/media_publish"):
                calls["publish"] += 1
                return httpx.Response(200, json={"id": "media-1"})
            if "status_code" in str(request.url):
                return httpx.Response(200, json={"status_code": "FINISHED"})
            raise AssertionError(f"unexpected request: {request.url}")

        import trevo_instagram.client as client_module

        original_init = client_module.InstagramClient.__init__

        def patched_init(self, cfg, transport=None):
            original_init(self, cfg, transport=httpx.MockTransport(handler))

        import pytest as _pytest

        mp = _pytest.MonkeyPatch()
        mp.setattr(client_module.InstagramClient, "__init__", patched_init)
        try:
            record = publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=True,
                poll_status=True,
            )
        finally:
            mp.undo()

        assert calls["container"] == 1
        assert calls["publish"] == 1
        assert record.status == "PUBLISHED"
        assert record.media_id == "media-1"

    def test_publish_blocked_plan_never_reaches_client(self, tmp_path, valid_jpeg, monkeypatch):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="")  # bloqueado: sem media_url
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=True)

        def fail_if_called(*args, **kwargs):
            raise AssertionError("nao deveria chegar ao cliente com plano bloqueado")

        monkeypatch.setattr(InstagramClient, "create_media_container", fail_if_called)

        with pytest.raises(PublishBlockedError):
            publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=True,
            )

    def test_duplicate_publish_is_blocked_by_default(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token="tok", ig_user_id="1", allow_publish_env=True)
        state_store = StateStore(tmp_path / "state")

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/media") and request.method == "POST":
                return httpx.Response(200, json={"id": "container-1"})
            if request.url.path.endswith("/media_publish"):
                return httpx.Response(200, json={"id": "media-1"})
            return httpx.Response(200, json={"status_code": "FINISHED"})

        import trevo_instagram.client as client_module
        import pytest as _pytest

        original_init = client_module.InstagramClient.__init__

        def patched_init(self, cfg, transport=None):
            original_init(self, cfg, transport=httpx.MockTransport(handler))

        mp = _pytest.MonkeyPatch()
        mp.setattr(client_module.InstagramClient, "__init__", patched_init)
        try:
            first = publish(manifest, config, state_store, confirm_publish_flag=True)
            assert first.status == "PUBLISHED"

            with pytest.raises(PublishBlockedError, match="ja publicado"):
                publish(manifest, config, state_store, confirm_publish_flag=True)
        finally:
            mp.undo()

    def test_missing_credentials_blocks_publish(self, tmp_path, valid_jpeg):
        (tmp_path / "img.jpg").write_bytes(valid_jpeg.read_bytes())
        manifest_path = _write_manifest(tmp_path, media_url="https://example.com/img.jpg")
        manifest = Manifest.load(manifest_path)
        config = Config(access_token=None, ig_user_id=None, allow_publish_env=True)

        with pytest.raises((PublishBlockedError, PublishNotConfirmedError)):
            publish(
                manifest,
                config,
                StateStore(tmp_path / "state"),
                confirm_publish_flag=True,
            )
