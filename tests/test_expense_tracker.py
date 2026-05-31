import pytest
from unittest.mock import patch, MagicMock
from expense_tracker import ExpenseTracker


@pytest.fixture
def tracker(tmp_path):
    return ExpenseTracker(str(tmp_path / "test.json"))


def test_run_exits_on_choice_7(tracker, capsys):
    with patch("builtins.input", side_effect=["7"]):
        tracker.run()
    assert "Encerrando" in capsys.readouterr().out


def test_run_invalid_choice_then_exit(tracker, capsys):
    with patch("builtins.input", side_effect=["9", "7"]):
        tracker.run()
    assert "inválida" in capsys.readouterr().out


def test_add_expense_valid(tracker, capsys):
    with patch("builtins.input", side_effect=["100.0", "food", "", "lunch"]):
        tracker.add_expense()
    assert "sucesso" in capsys.readouterr().out


def test_add_expense_invalid_amount(tracker, capsys):
    with patch("builtins.input", side_effect=["abc"]):
        tracker.add_expense()
    assert "inválido" in capsys.readouterr().out


def test_add_expense_invalid_category(tracker, capsys):
    with patch("builtins.input", side_effect=["50.0", "   "]):
        tracker.add_expense()
    assert "inválida" in capsys.readouterr().out


def test_add_expense_invalid_date(tracker, capsys):
    with patch("builtins.input", side_effect=["50.0", "food", "31-13-2024"]):
        tracker.add_expense()
    assert "inválida" in capsys.readouterr().out


def test_view_expenses_empty(tracker, capsys):
    with patch("builtins.input", return_value=""):
        tracker.view_expenses()
    assert "Nenhuma" in capsys.readouterr().out


def test_view_expenses_with_filter(tracker, capsys):
    tracker.expense_service.add(__import__('models.expense', fromlist=['Expense']).Expense(100.0, "food", "2024-01-15", "lunch"))
    with patch("builtins.input", return_value="food"):
        tracker.view_expenses()
    out = capsys.readouterr().out
    assert "Food" in out


def test_delete_expense_no_expenses(tracker, capsys):
    tracker.delete_expense()
    assert "Nenhuma" in capsys.readouterr().out


def test_delete_expense_invalid_index(tracker, capsys):
    tracker.expense_service.add(__import__('models.expense', fromlist=['Expense']).Expense(100.0, "food", "2024-01-15"))
    with patch("builtins.input", return_value="99"):
        tracker.delete_expense()
    assert "inválido" in capsys.readouterr().out.lower()


def test_delete_expense_valid(tracker, capsys):
    from models.expense import Expense
    tracker.expense_service.add(Expense(100.0, "food", "2024-01-15"))
    with patch("builtins.input", return_value="1"):
        tracker.delete_expense()
    assert "sucesso" in capsys.readouterr().out


def test_manage_categories_add(tracker, capsys):
    with patch("builtins.input", side_effect=["1", "groceries", ""]):
        tracker.manage_categories()
    assert "sucesso" in capsys.readouterr().out


def test_manage_categories_add_duplicate(tracker, capsys):
    from models.category import Category
    tracker.category_service.add(Category("food"))
    with patch("builtins.input", side_effect=["1", "food", ""]):
        tracker.manage_categories()
    assert "já existe" in capsys.readouterr().out


def test_manage_categories_remove(tracker, capsys):
    from models.category import Category
    tracker.category_service.add(Category("food"))
    with patch("builtins.input", side_effect=["2", "food"]):
        tracker.manage_categories()
    assert "sucesso" in capsys.readouterr().out


def test_manage_categories_remove_nonexistent(tracker, capsys):
    with patch("builtins.input", side_effect=["2", "nonexistent"]):
        tracker.manage_categories()
    assert "não encontrada" in capsys.readouterr().out


def test_manage_categories_back(tracker, capsys):
    with patch("builtins.input", return_value="3"):
        tracker.manage_categories()


def test_manage_budgets_set(tracker, capsys):
    with patch("builtins.input", side_effect=["1", "food", "500"]):
        tracker.manage_budgets()
    assert "sucesso" in capsys.readouterr().out


def test_manage_budgets_invalid_limit(tracker, capsys):
    with patch("builtins.input", side_effect=["1", "food", "abc"]):
        tracker.manage_budgets()
    assert "inválido" in capsys.readouterr().out


def test_manage_budgets_back(tracker, capsys):
    with patch("builtins.input", return_value="2"):
        tracker.manage_budgets()


def test_generate_report_empty(tracker, capsys):
    with patch("builtins.input", return_value="n"):
        tracker.generate_report()
    assert "Nenhuma" in capsys.readouterr().out


def test_generate_report_with_data_no_chart(tracker, capsys):
    from models.expense import Expense
    tracker.expense_service.add(Expense(100.0, "food", "2024-01-15"))
    with patch("builtins.input", return_value="n"):
        tracker.generate_report()
    out = capsys.readouterr().out
    assert "Food" in out


def test_add_expense_triggers_budget_warning(tracker, capsys):
    from models.budget import Budget
    tracker.budget_service.set_budget(Budget("food", 50.0))
    with patch("builtins.input", side_effect=["100.0", "food", "", "expensive lunch"]):
        tracker.add_expense()
    assert "AVISO" in capsys.readouterr().out
