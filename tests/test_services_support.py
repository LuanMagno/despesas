from services.date_service import DateService
from services.validation_service import ValidationService


def test_date_service_month_key():
    assert DateService().month_key("2024-05-31") == "2024-05"


def test_date_service_format_br_invalid_returns_original():
    assert DateService().format_br("data") == "data"


def test_validation_service_validate_index():
    validator = ValidationService()
    assert validator.validate_index(0, 1) is True
    assert validator.validate_index(1, 1) is False
    assert validator.validate_index(-1, 1) is False
