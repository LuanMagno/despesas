import pytest
from unittest.mock import MagicMock
from services.expense_service import ExpenseService
from models.expense import Expense
from storage.file_storage import FileStorage


@pytest.fixture
def mock_storage():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {"expenses": [], "categories": [], "budgets": []}
    storage.save.return_value = True
    return storage


@pytest.fixture
def service(mock_storage):
    return ExpenseService(mock_storage)


def test_add_valid_expense(service):
    e = Expense(100.0, "food", "2024-01-15", "lunch")
    assert service.add(e) is True
    assert len(service.get_all()) == 1


def test_add_invalid_amount_returns_false(service):
    e = Expense(-10.0, "food", "2024-01-15")
    assert service.add(e) is False
    assert len(service.get_all()) == 0


def test_add_invalid_date_returns_false(service):
    e = Expense(50.0, "food", "bad-date")
    assert service.add(e) is False


def test_delete_existing_expense(service):
    service.add(Expense(100.0, "food", "2024-01-15", "lunch"))
    assert service.delete(0) is True
    assert len(service.get_all()) == 0


def test_delete_invalid_index_returns_false(service):
    assert service.delete(0) is False
    assert service.delete(-1) is False


def test_get_all_returns_copy(service):
    service.add(Expense(100.0, "food", "2024-01-15"))
    all_expenses = service.get_all()
    all_expenses.clear()
    assert len(service.get_all()) == 1


def test_get_by_category_filters_correctly(service):
    service.add(Expense(100.0, "food", "2024-01-15"))
    service.add(Expense(200.0, "transport", "2024-01-16"))
    service.add(Expense(50.0, "food", "2024-01-17"))
    result = service.get_by_category("food")
    assert len(result) == 2
    assert all(e.category == "food" for e in result)


def test_get_by_category_case_insensitive(service):
    service.add(Expense(100.0, "food", "2024-01-15"))
    result = service.get_by_category("FOOD")
    assert len(result) == 1


def test_get_total_sums_all(service):
    service.add(Expense(100.0, "food", "2024-01-15"))
    service.add(Expense(50.0, "transport", "2024-01-16"))
    assert service.get_total() == 150.0


def test_get_total_empty_is_zero(service):
    assert service.get_total() == 0.0


def test_get_monthly_summary(service):
    service.add(Expense(100.0, "food", "2024-01-10"))
    service.add(Expense(50.0, "food", "2024-01-25"))
    service.add(Expense(200.0, "rent", "2024-02-01"))
    summary = service.get_monthly_summary()
    assert summary["2024-01"] == 150.0
    assert summary["2024-02"] == 200.0


def test_load_from_storage_with_existing_data():
    storage = MagicMock(spec=FileStorage)
    storage.load.return_value = {
        "expenses": [
            {"amount": 99.0, "category": "food", "date": "2024-05-01", "description": "pizza"}
        ],
        "categories": [],
        "budgets": [],
    }
    storage.save.return_value = True
    svc = ExpenseService(storage)
    assert len(svc.get_all()) == 1
    assert svc.get_all()[0].amount == 99.0
