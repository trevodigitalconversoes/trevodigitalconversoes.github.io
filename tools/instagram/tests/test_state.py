from pathlib import Path

from trevo_instagram.state import PublicationRecord, StateStore


def test_new_state_store_has_no_records(tmp_path: Path):
    store = StateStore(tmp_path / "state")
    assert store.get("abc") is None
    assert store.is_already_published("abc") is False


def test_save_and_retrieve_record(tmp_path: Path):
    store = StateStore(tmp_path / "state")
    record = PublicationRecord(
        publication_hash="abc123",
        manifest_path="m.toml",
        asset_sha256="deadbeef",
        caption_sha256="feedface",
        status="PUBLISHED",
        media_id="media-1",
    )
    store.save(record)
    loaded = store.get("abc123")
    assert loaded is not None
    assert loaded.media_id == "media-1"
    assert store.is_already_published("abc123") is True


def test_failed_record_is_not_considered_published(tmp_path: Path):
    store = StateStore(tmp_path / "state")
    record = PublicationRecord(
        publication_hash="xyz",
        manifest_path="m.toml",
        asset_sha256="a",
        caption_sha256="b",
        status="FAILED",
    )
    store.save(record)
    assert store.is_already_published("xyz") is False
