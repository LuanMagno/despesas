from unittest.mock import MagicMock

from storage.file_storage import FileStorage


def test_load_nonexistent_file(tmp_path):
    storage = FileStorage(str(tmp_path / "test.json"))
    assert storage.load() == {}


def test_save_and_load_roundtrip(tmp_path):
    filepath = str(tmp_path / "test.json")
    storage = FileStorage(filepath)
    data = {"expenses": [{"amount": 100.0, "category": "alimentacao"}], "budgets": []}
    assert storage.save(data) is True
    assert storage.load() == data


def test_save_creates_parent_directory(tmp_path):
    storage = FileStorage(str(tmp_path / "pasta" / "test.json"))
    assert storage.save({"key": "value"}) is True
    assert storage.load() == {"key": "value"}


def test_save_returns_false_when_file_manager_fails(tmp_path):
    manager = MagicMock()
    manager.exists.return_value = False
    manager.ensure_parent_dir.side_effect = OSError
    storage = FileStorage(str(tmp_path / "test.json"), manager)
    assert storage.save({"key": "value"}) is False


def test_load_returns_empty_on_corrupt_json(tmp_path):
    filepath = tmp_path / "bad.json"
    filepath.write_text("{ invalid json }", encoding="utf-8")
    storage = FileStorage(str(filepath))
    assert storage.load() == {}


def test_backup_creates_bak_file(tmp_path):
    filepath = str(tmp_path / "test.json")
    storage = FileStorage(filepath)
    storage.save({"expenses": []})
    backup_path = storage.backup()
    assert backup_path
    assert backup_path.endswith(".bak")


def test_backup_nonexistent_file_returns_empty(tmp_path):
    storage = FileStorage(str(tmp_path / "missing.json"))
    assert storage.backup() == ""


def test_save_preserves_unicode(tmp_path):
    storage = FileStorage(str(tmp_path / "test.json"))
    data = {"description": "Almoco na padaria"}
    storage.save(data)
    assert storage.load()["description"] == "Almoco na padaria"
