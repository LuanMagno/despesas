import pytest

from models.category import Category
from services.category_service import CategoryService
from storage.file_storage import FileStorage


@pytest.fixture
def service(tmp_path):
    return CategoryService(FileStorage(str(tmp_path / "dados.json")))


def test_add_new_category(service):
    assert service.add(Category("alimentacao")) is True
    assert len(service.get_all()) == 1


def test_add_duplicate_returns_false(service):
    service.add(Category("alimentacao"))
    assert service.add(Category("ALIMENTACAO")) is False
    assert len(service.get_all()) == 1


def test_add_invalid_category_returns_false(service):
    assert service.add(Category("   ")) is False


def test_delete_existing_category(service):
    service.add(Category("alimentacao"))
    assert service.delete("ALIMENTACAO") is True
    assert service.get_all() == []


def test_delete_nonexistent_returns_false(service):
    assert service.delete("inexistente") is False


def test_exists_true_and_false(service):
    service.add(Category("transporte"))
    assert service.exists("TRANSPORTE") is True
    assert service.exists("alimentacao") is False


def test_get_all_returns_independent_list(service):
    service.add(Category("alimentacao"))
    categories = service.get_all()
    categories.clear()
    assert len(service.get_all()) == 1
