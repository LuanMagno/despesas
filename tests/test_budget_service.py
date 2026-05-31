import pytest

from models.budget import Budget
from services.budget_service import BudgetService
from storage.file_storage import FileStorage


@pytest.fixture
def service(tmp_path):
    return BudgetService(FileStorage(str(tmp_path / "dados.json")))


def test_set_budget_new_category(service):
    assert service.set_budget(Budget("alimentacao", 500.0)) is True
    assert len(service.get_all()) == 1


def test_set_budget_updates_existing(service):
    service.set_budget(Budget("alimentacao", 500.0))
    service.set_budget(Budget("alimentacao", 800.0))
    assert len(service.get_all()) == 1
    assert service.get_budget("alimentacao").limit == 800.0


def test_set_budget_invalid_limit_returns_false(service):
    assert service.set_budget(Budget("alimentacao", 0)) is False


def test_get_budget_nonexistent_returns_none(service):
    assert service.get_budget("inexistente") is None


def test_get_budget_case_insensitive(service):
    service.set_budget(Budget("alimentacao", 300.0))
    assert service.get_budget("ALIMENTACAO") is not None


def test_check_overspend_false_within_limit(service):
    service.set_budget(Budget("alimentacao", 500.0))
    assert service.check_overspend("alimentacao", 499.0) is False


def test_check_overspend_true_over_limit(service):
    service.set_budget(Budget("alimentacao", 500.0))
    assert service.check_overspend("alimentacao", 501.0) is True


def test_check_overspend_no_budget_returns_false(service):
    assert service.check_overspend("nao-cadastrado", 9999.0) is False


def test_delete_existing_budget(service):
    service.set_budget(Budget("alimentacao", 500.0))
    assert service.delete("ALIMENTACAO") is True
    assert service.get_budget("alimentacao") is None


def test_delete_nonexistent_budget_returns_false(service):
    assert service.delete("inexistente") is False
