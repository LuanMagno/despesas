from utils.file_manager import FileManager


def test_exists_returns_false_for_missing_file(tmp_path):
    assert FileManager().exists(str(tmp_path / "missing.json")) is False


def test_ensure_parent_dir_creates_directory(tmp_path):
    filepath = tmp_path / "nova" / "dados.json"
    FileManager().ensure_parent_dir(str(filepath))
    assert filepath.parent.exists()


def test_backup_missing_file_returns_empty(tmp_path):
    assert FileManager().backup(str(tmp_path / "missing.json")) == ""
