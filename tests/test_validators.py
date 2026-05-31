import pytest
from utils.validators import validate_amount, validate_date, validate_category_name


class TestValidateAmount:
    def test_valid_integer(self):
        assert validate_amount(100) is True

    def test_valid_float(self):
        assert validate_amount(9.99) is True

    def test_valid_string_number(self):
        assert validate_amount("50.5") is True

    def test_zero_is_invalid(self):
        assert validate_amount(0) is False

    def test_negative_is_invalid(self):
        assert validate_amount(-1) is False

    def test_string_text_is_invalid(self):
        assert validate_amount("abc") is False

    def test_none_is_invalid(self):
        assert validate_amount(None) is False

    def test_empty_string_is_invalid(self):
        assert validate_amount("") is False


class TestValidateDate:
    def test_valid_date(self):
        assert validate_date("2024-01-15") is True

    def test_wrong_format(self):
        assert validate_date("15/01/2024") is False

    def test_invalid_month(self):
        assert validate_date("2024-13-01") is False

    def test_invalid_day(self):
        assert validate_date("2024-01-32") is False

    def test_plain_text(self):
        assert validate_date("not-a-date") is False

    def test_none_is_invalid(self):
        assert validate_date(None) is False

    def test_empty_string(self):
        assert validate_date("") is False


class TestValidateCategoryName:
    def test_valid_name(self):
        assert validate_category_name("food") is True

    def test_valid_name_with_spaces(self):
        assert validate_category_name("  food  ") is True

    def test_empty_string_invalid(self):
        assert validate_category_name("") is False

    def test_only_spaces_invalid(self):
        assert validate_category_name("   ") is False

    def test_non_string_invalid(self):
        assert validate_category_name(123) is False

    def test_none_invalid(self):
        assert validate_category_name(None) is False
