import pytest
from unittest.mock import MagicMock
from services.budget_service import BudgetService
from models.budget import Budget
from storage.file_storage import FileStorage


@pytest.fixture
def mock_storage():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {"expenses": [], "categories": [], "budgets": []}
    storage.save.return_value = True
    return storage


@pytest.fixture
def service(mock_storage):
    return BudgetService(mock_storage)


def test_set_budget_new_category(service):
    service.set_budget(Budget("food", 500.0))
    assert len(service.get_all()) == 1


def test_set_budget_updates_existing(service):
    service.set_budget(Budget("food", 500.0))
    service.set_budget(Budget("food", 800.0))
    assert len(service.get_all()) == 1
    assert service.get_budget("food").limit == 800.0


def test_get_budget_existing(service):
    service.set_budget(Budget("food", 300.0))
    b = service.get_budget("food")
    assert b is not None
    assert b.limit == 300.0


def test_get_budget_nonexistent_returns_none(service):
    assert service.get_budget("nonexistent") is None


def test_get_budget_case_insensitive(service):
    service.set_budget(Budget("food", 300.0))
    assert service.get_budget("FOOD") is not None


def test_check_overspend_false_within_limit(service):
    service.set_budget(Budget("food", 500.0))
    assert service.check_overspend("food", 499.0) is False


def test_check_overspend_true_over_limit(service):
    service.set_budget(Budget("food", 500.0))
    assert service.check_overspend("food", 501.0) is True


def test_check_overspend_no_budget_returns_false(service):
    assert service.check_overspend("unregistered", 9999.0) is False


def test_get_all_returns_copy(service):
    service.set_budget(Budget("food", 300.0))
    result = service.get_all()
    result.clear()
    assert len(service.get_all()) == 1


def test_load_from_storage_with_existing_data():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {
        "budgets": [{"category": "rent", "limit": 1200.0}],
        "expenses": [],
        "categories": [],
    }
    storage.save.return_value = True
    svc = BudgetService(storage)
    assert svc.get_budget("rent").limit == 1200.0
