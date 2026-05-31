from unittest.mock import MagicMock

from models.expense import Expense
from services.report_service import ReportService


def test_category_report_empty():
    expense_service = MagicMock()
    expense_service.get_all.return_value = []
    report = ReportService(expense_service)
    assert report.category_report() == {}


def test_category_report_sums_by_category():
    expense_service = MagicMock()
    expense_service.get_all.return_value = [
        Expense(100.0, "alimentacao", "2024-01-10"),
        Expense(50.0, "alimentacao", "2024-01-20"),
        Expense(200.0, "aluguel", "2024-01-01"),
    ]
    report = ReportService(expense_service)
    assert report.category_report() == {"alimentacao": 150.0, "aluguel": 200.0}


def test_monthly_report_delegates_to_service():
    expense_service = MagicMock()
    expense_service.get_monthly_summary.return_value = {"2024-01": 300.0}
    report = ReportService(expense_service)
    assert report.monthly_report() == {"2024-01": 300.0}


def test_total_report_sums_category_values():
    expense_service = MagicMock()
    expense_service.get_all.return_value = [
        Expense(100.0, "alimentacao", "2024-01-10"),
        Expense(50.0, "transporte", "2024-01-20"),
    ]
    report = ReportService(expense_service)
    assert report.total_report() == 150.0
