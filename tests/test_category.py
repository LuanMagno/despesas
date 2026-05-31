import pytest
from models.category import Category


def test_creation_lowercases_name():
    c = Category("FOOD", "eating out")
    assert c.name == "food"
    assert c.description == "eating out"


def test_creation_default_description():
    c = Category("transport")
    assert c.description == ""


def test_to_dict():
    c = Category("food", "eating")
    assert c.to_dict() == {"name": "food", "description": "eating"}


def test_from_dict():
    c = Category.from_dict({"name": "rent", "description": "monthly"})
    assert c.name == "rent"
    assert c.description == "monthly"


def test_from_dict_without_description():
    c = Category.from_dict({"name": "health"})
    assert c.description == ""


def test_str_capitalizes():
    c = Category("food")
    assert str(c) == "Food"
