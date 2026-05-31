import pytest
from datetime import datetime
from models.expense import Expense


def test_creation_stores_fields():
    e = Expense(100.0, "Food", "2024-01-15", "lunch")
    assert e.amount == 100.0
    assert e.category == "food"
    assert e.date == "2024-01-15"
    assert e.description == "lunch"


def test_category_is_lowercased():
    e = Expense(50.0, "TRANSPORT")
    assert e.category == "transport"


def test_default_date_is_today():
    e = Expense(50.0, "food")
    assert e.date == datetime.today().strftime('%Y-%m-%d')


def test_to_dict_returns_correct_keys():
    e = Expense(100.0, "food", "2024-01-15", "lunch")
    d = e.to_dict()
    assert d == {"amount": 100.0, "category": "food", "date": "2024-01-15", "description": "lunch"}


def test_from_dict_creates_expense():
    d = {"amount": 75.0, "category": "rent", "date": "2024-03-01", "description": "monthly rent"}
    e = Expense.from_dict(d)
    assert e.amount == 75.0
    assert e.category == "rent"
    assert e.date == "2024-03-01"


def test_from_dict_without_description():
    d = {"amount": 20.0, "category": "food", "date": "2024-01-10"}
    e = Expense.from_dict(d)
    assert e.description == ""


def test_validate_valid_expense():
    e = Expense(100.0, "food", "2024-01-15", "lunch")
    assert e.validate() is True


def test_validate_zero_amount():
    e = Expense(0.0, "food", "2024-01-15")
    assert e.validate() is False


def test_validate_negative_amount():
    e = Expense(-50.0, "food", "2024-01-15")
    assert e.validate() is False


def test_validate_invalid_date():
    e = Expense(100.0, "food", "not-a-date")
    assert e.validate() is False


def test_validate_wrong_date_format():
    e = Expense(100.0, "food", "15/01/2024")
    assert e.validate() is False


def test_validate_empty_category():
    e = Expense(100.0, "food", "2024-01-15")
    e.category = "   "
    assert e.validate() is False


def test_str_contains_category_and_amount():
    e = Expense(100.0, "food", "2024-01-15", "lunch")
    s = str(e)
    assert "Food" in s
    assert "100.00" in s
    assert "2024-01-15" in s
