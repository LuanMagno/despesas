from models.budget import Budget
from models.category import Category
from models.expense import Expense
from repositories.budget_repository import BudgetRepository
from repositories.category_repository import CategoryRepository
from repositories.expense_repository import ExpenseRepository
from storage.file_storage import FileStorage


def test_expense_repository_add_find_and_delete(tmp_path):
    repository = ExpenseRepository(FileStorage(str(tmp_path / "dados.json")))
    assert repository.add(Expense(25.0, "transporte", "2024-03-01")) is True
    assert len(repository.find_by_category("TRANSPORTE")) == 1
    assert repository.update(0, Expense(30.0, "transporte", "2024-03-02")) is True
    assert repository.list_all()[0].amount == 30.0
    assert repository.delete(0) is True
    assert repository.list_all() == []


def test_expense_repository_delete_invalid_index(tmp_path):
    repository = ExpenseRepository(FileStorage(str(tmp_path / "dados.json")))
    assert repository.delete(10) is False


def test_category_repository_add_find_and_delete(tmp_path):
    repository = CategoryRepository(FileStorage(str(tmp_path / "dados.json")))
    assert repository.add(Category("lazer")) is True
    assert repository.find_by_name("LAZER").name == "lazer"
    assert repository.delete("lazer") is True
    assert repository.find_by_name("lazer") is None


def test_budget_repository_upsert_and_find(tmp_path):
    repository = BudgetRepository(FileStorage(str(tmp_path / "dados.json")))
    assert repository.upsert(Budget("mercado", 400.0)) is True
    assert repository.upsert(Budget("mercado", 600.0)) is True
    budgets = repository.list_all()
    assert len(budgets) == 1
    assert repository.find_by_category("MERCADO").limit == 600.0
    assert repository.delete("mercado") is True
    assert repository.find_by_category("mercado") is None
