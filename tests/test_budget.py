import pytest
from models.budget import Budget


def test_creation_lowercases_category():
    b = Budget("FOOD", 500.0)
    assert b.category == "food"
    assert b.limit == 500.0


def test_to_dict():
    b = Budget("food", 300.0)
    assert b.to_dict() == {"category": "food", "limit": 300.0}


def test_from_dict():
    b = Budget.from_dict({"category": "transport", "limit": 200.0})
    assert b.category == "transport"
    assert b.limit == 200.0


def test_check_limit_within():
    b = Budget("food", 500.0)
    assert b.check_limit(499.99) is True


def test_check_limit_exactly_at_limit():
    b = Budget("food", 500.0)
    assert b.check_limit(500.0) is True


def test_check_limit_exceeded():
    b = Budget("food", 500.0)
    assert b.check_limit(500.01) is False


def test_str_format():
    b = Budget("food", 300.0)
    assert str(b) == "Food: R$300.00"
