import pytest

from models.expense import Expense
from services.expense_service import ExpenseService
from storage.file_storage import FileStorage


@pytest.fixture
def service(tmp_path):
    return ExpenseService(FileStorage(str(tmp_path / "dados.json")))


def test_add_valid_expense(service):
    expense = Expense(100.0, "alimentacao", "2024-01-15", "almoco")
    assert service.add(expense) is True
    assert len(service.get_all()) == 1


def test_add_invalid_amount_returns_false(service):
    expense = Expense(-10.0, "alimentacao", "2024-01-15")
    assert service.add(expense) is False
    assert service.get_all() == []


def test_add_invalid_date_returns_false(service):
    expense = Expense(50.0, "alimentacao", "data-invalida")
    assert service.add(expense) is False


def test_delete_existing_expense(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    assert service.delete(0) is True
    assert service.get_all() == []


def test_delete_invalid_index_returns_false(service):
    assert service.delete(0) is False
    assert service.delete(-1) is False


def test_update_existing_expense(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    updated = Expense(80.0, "transporte", "2024-01-16")
    assert service.update(0, updated) is True
    assert service.get_all()[0].category == "transporte"


def test_update_invalid_expense_returns_false(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    assert service.update(0, Expense(0, "alimentacao", "2024-01-15")) is False
    assert service.get_all()[0].amount == 100.0


def test_update_invalid_index_returns_false(service):
    assert service.update(99, Expense(80.0, "transporte", "2024-01-16")) is False


def test_get_all_returns_independent_list(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    expenses = service.get_all()
    expenses.clear()
    assert len(service.get_all()) == 1


def test_get_by_category_filters_correctly(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    service.add(Expense(200.0, "transporte", "2024-01-16"))
    service.add(Expense(50.0, "alimentacao", "2024-01-17"))
    result = service.get_by_category("ALIMENTACAO")
    assert len(result) == 2
    assert all(expense.category == "alimentacao" for expense in result)


def test_get_total_sums_all(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    service.add(Expense(50.0, "transporte", "2024-01-16"))
    assert service.get_total() == 150.0


def test_get_total_by_category(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    service.add(Expense(50.0, "transporte", "2024-01-16"))
    assert service.get_total_by_category("alimentacao") == 100.0


def test_get_monthly_summary(service):
    service.add(Expense(100.0, "alimentacao", "2024-01-10"))
    service.add(Expense(50.0, "alimentacao", "2024-01-25"))
    service.add(Expense(200.0, "aluguel", "2024-02-01"))
    assert service.get_monthly_summary() == {"2024-01": 150.0, "2024-02": 200.0}
