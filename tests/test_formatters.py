import pytest
from utils.formatters import format_currency, format_date, format_expense_row
from models.expense import Expense


class TestFormatCurrency:
    def test_integer_value(self):
        assert format_currency(100) == "R$ 100.00"

    def test_float_value(self):
        assert format_currency(9.5) == "R$ 9.50"

    def test_large_value_with_comma(self):
        assert format_currency(1000.0) == "R$ 1,000.00"

    def test_zero(self):
        assert format_currency(0) == "R$ 0.00"


class TestFormatDate:
    def test_valid_date(self):
        assert format_date("2024-01-15") == "15/01/2024"

    def test_invalid_date_returns_original(self):
        assert format_date("not-a-date") == "not-a-date"

    def test_wrong_format_returns_original(self):
        assert format_date("15/01/2024") == "15/01/2024"


class TestFormatExpenseRow:
    def test_row_contains_all_fields(self):
        e = Expense(100.0, "food", "2024-01-15", "lunch")
        row = format_expense_row(1, e)
        assert "1." in row
        assert "15/01/2024" in row
        assert "Food" in row
        assert "100.00" in row
        assert "lunch" in row

    def test_index_in_row(self):
        e = Expense(50.0, "transport", "2024-03-20", "uber")
        row = format_expense_row(3, e)
        assert row.startswith("3.")
