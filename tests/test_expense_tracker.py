from unittest.mock import patch

import pytest

from expense_tracker import ExpenseTracker
from models.budget import Budget
from models.category import Category
from models.expense import Expense


@pytest.fixture
def tracker(tmp_path):
    return ExpenseTracker(str(tmp_path / "test.json"))


def test_run_exits_on_choice_7(tracker, capsys):
    with patch("builtins.input", side_effect=["5"]):
        tracker.run()
    assert "Encerrando" in capsys.readouterr().out


def test_run_invalid_choice_then_exit(tracker, capsys):
    with patch("builtins.input", side_effect=["9", "5"]):
        tracker.run()
    assert "Opcao invalida" in capsys.readouterr().out


def test_add_expense_valid(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["100.0", "alimentacao", "", "almoco"]):
        tracker.add_expense()
    assert "sucesso" in capsys.readouterr().out


def test_add_expense_invalid_amount(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["abc"]):
        tracker.add_expense()
    assert "invalido" in capsys.readouterr().out


def test_add_expense_invalid_category(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["50.0", "inexistente"]):
        tracker.add_expense()
    assert "Categoria nao cadastrada" in capsys.readouterr().out


def test_add_expense_invalid_date(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["50.0", "alimentacao", "31-13-2024", "teste"]):
        tracker.add_expense()
    assert "Erro ao adicionar" in capsys.readouterr().out


def test_add_expense_without_categories(tracker, capsys):
    tracker.add_expense()
    assert "Cadastre uma categoria" in capsys.readouterr().out


def test_view_expenses_empty(tracker, capsys):
    with patch("builtins.input", return_value=""):
        tracker.view_expenses()
    assert "Nenhuma despesa" in capsys.readouterr().out


def test_view_expenses_with_filter(tracker, capsys):
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15", "almoco"))
    with patch("builtins.input", return_value="alimentacao"):
        tracker.view_expenses()
    assert "Alimentacao" in capsys.readouterr().out


def test_delete_expense_no_expenses(tracker, capsys):
    tracker.delete_expense()
    assert "Nenhuma despesa" in capsys.readouterr().out


def test_delete_expense_invalid_index(tracker, capsys):
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    with patch("builtins.input", return_value="99"):
        tracker.delete_expense()
    assert "Indice invalido" in capsys.readouterr().out


def test_delete_expense_valid(tracker, capsys):
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    with patch("builtins.input", return_value="1"):
        tracker.delete_expense()
    assert "sucesso" in capsys.readouterr().out


def test_edit_expense_valid(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    tracker.category_service.add(Category("transporte"))
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15", "almoco"))
    with patch("builtins.input", side_effect=["1", "75.5", "transporte", "2024-01-16", "uber"]):
        tracker.edit_expense()
    out = capsys.readouterr().out
    assert "editada com sucesso" in out
    assert tracker.expense_service.get_all()[0].category == "transporte"


def test_edit_expense_invalid_category(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15", "almoco"))
    with patch("builtins.input", side_effect=["1", "", "inexistente"]):
        tracker.edit_expense()
    assert "Categoria nao cadastrada" in capsys.readouterr().out


def test_manage_expenses_add_option(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["2", "100.0", "alimentacao", "", "almoco"]):
        tracker.manage_expenses()
    assert "Despesa adicionada" in capsys.readouterr().out


def test_manage_categories_add(tracker, capsys):
    with patch("builtins.input", side_effect=["1", "mercado", "compras"]):
        tracker.manage_categories()
    assert "sucesso" in capsys.readouterr().out


def test_manage_categories_add_duplicate(tracker, capsys):
    tracker.category_service.add(Category("mercado"))
    with patch("builtins.input", side_effect=["1", "mercado", ""]):
        tracker.manage_categories()
    assert "ja existe" in capsys.readouterr().out


def test_manage_categories_remove(tracker, capsys):
    tracker.category_service.add(Category("mercado"))
    with patch("builtins.input", side_effect=["2", "mercado"]):
        tracker.manage_categories()
    assert "sucesso" in capsys.readouterr().out


def test_manage_categories_remove_nonexistent(tracker, capsys):
    with patch("builtins.input", side_effect=["2", "inexistente"]):
        tracker.manage_categories()
    assert "nao encontrada" in capsys.readouterr().out


def test_manage_budgets_set(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["1", "alimentacao", "500"]):
        tracker.manage_budgets()
    assert "sucesso" in capsys.readouterr().out


def test_manage_budgets_invalid_limit(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["1", "alimentacao", "abc"]):
        tracker.manage_budgets()
    assert "Valor invalido" in capsys.readouterr().out


def test_manage_budgets_edit(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    tracker.budget_service.set_budget(Budget("alimentacao", 100.0))
    with patch("builtins.input", side_effect=["2", "alimentacao", "250"]):
        tracker.manage_budgets()
    assert "editado com sucesso" in capsys.readouterr().out
    assert tracker.budget_service.get_budget("alimentacao").limit == 250.0


def test_manage_budgets_delete(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    tracker.budget_service.set_budget(Budget("alimentacao", 100.0))
    with patch("builtins.input", side_effect=["3", "alimentacao"]):
        tracker.manage_budgets()
    assert "excluido com sucesso" in capsys.readouterr().out
    assert tracker.budget_service.get_budget("alimentacao") is None


def test_manage_budgets_rejects_unknown_category(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    with patch("builtins.input", side_effect=["1", "inexistente"]):
        tracker.manage_budgets()
    assert "Categoria nao cadastrada" in capsys.readouterr().out


def test_generate_report_empty(tracker, capsys):
    tracker.generate_report()
    assert "Nenhuma despesa" in capsys.readouterr().out


def test_generate_report_with_data_no_chart(tracker, capsys):
    tracker.expense_service.add(Expense(100.0, "alimentacao", "2024-01-15"))
    with patch("builtins.input", return_value="n"):
        tracker.generate_report()
    assert "Alimentacao" in capsys.readouterr().out


def test_add_expense_triggers_budget_warning(tracker, capsys):
    tracker.category_service.add(Category("alimentacao"))
    tracker.budget_service.set_budget(Budget("alimentacao", 50.0))
    with patch("builtins.input", side_effect=["100.0", "alimentacao", "", "almoco caro"]):
        tracker.add_expense()
    assert "AVISO" in capsys.readouterr().out
