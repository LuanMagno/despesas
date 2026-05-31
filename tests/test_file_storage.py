import pytest
import json
import os
from storage.file_storage import FileStorage


def test_load_nonexistent_file(tmp_path):
    storage = FileStorage(str(tmp_path / "test.json"))
    assert storage.load() == {}


def test_save_and_load_roundtrip(tmp_path):
    filepath = str(tmp_path / "test.json")
    storage = FileStorage(filepath)
    data = {"expenses": [{"amount": 100.0, "category": "food"}], "budgets": []}
    assert storage.save(data) is True
    assert storage.load() == data


def test_save_returns_false_on_invalid_path(tmp_path):
    storage = FileStorage(str(tmp_path / "missing_dir" / "test.json"))
    assert storage.save({"key": "value"}) is False


def test_load_returns_empty_on_corrupt_json(tmp_path):
    filepath = str(tmp_path / "bad.json")
    with open(filepath, 'w') as f:
        f.write("{ invalid json }")
    storage = FileStorage(filepath)
    assert storage.load() == {}


def test_backup_creates_bak_file(tmp_path):
    filepath = str(tmp_path / "test.json")
    storage = FileStorage(filepath)
    storage.save({"expenses": []})
    backup_path = storage.backup()
    assert backup_path != ""
    assert os.path.exists(backup_path)
    assert backup_path.endswith(".bak")


def test_backup_nonexistent_file_returns_empty(tmp_path):
    storage = FileStorage(str(tmp_path / "missing.json"))
    assert storage.backup() == ""


def test_save_preserves_unicode(tmp_path):
    filepath = str(tmp_path / "test.json")
    storage = FileStorage(filepath)
    data = {"description": "Almoço na padaria"}
    storage.save(data)
    loaded = storage.load()
    assert loaded["description"] == "Almoço na padaria"
