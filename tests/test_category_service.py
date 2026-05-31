import pytest
from unittest.mock import MagicMock
from services.category_service import CategoryService
from models.category import Category
from storage.file_storage import FileStorage


@pytest.fixture
def mock_storage():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {"expenses": [], "categories": [], "budgets": []}
    storage.save.return_value = True
    return storage


@pytest.fixture
def service(mock_storage):
    return CategoryService(mock_storage)


def test_add_new_category(service):
    assert service.add(Category("food")) is True
    assert len(service.get_all()) == 1


def test_add_duplicate_returns_false(service):
    service.add(Category("food"))
    assert service.add(Category("food")) is False
    assert len(service.get_all()) == 1


def test_add_duplicate_case_insensitive(service):
    service.add(Category("food"))
    assert service.add(Category("FOOD")) is False


def test_delete_existing_category(service):
    service.add(Category("food"))
    assert service.delete("food") is True
    assert len(service.get_all()) == 0


def test_delete_nonexistent_returns_false(service):
    assert service.delete("nonexistent") is False


def test_delete_case_insensitive(service):
    service.add(Category("food"))
    assert service.delete("FOOD") is True


def test_get_all_returns_copy(service):
    service.add(Category("food"))
    result = service.get_all()
    result.clear()
    assert len(service.get_all()) == 1


def test_exists_true(service):
    service.add(Category("food"))
    assert service.exists("food") is True


def test_exists_false(service):
    assert service.exists("food") is False


def test_exists_case_insensitive(service):
    service.add(Category("food"))
    assert service.exists("FOOD") is True


def test_load_from_storage_with_existing_data():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {
        "categories": [{"name": "transport", "description": ""}],
        "expenses": [],
        "budgets": [],
    }
    storage.save.return_value = True
    svc = CategoryService(storage)
    assert svc.exists("transport") is True
