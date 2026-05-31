import pytest
from unittest.mock import MagicMock, patch
from services.report_service import ReportService
from services.expense_service import ExpenseService
from models.expense import Expense


@pytest.fixture
def mock_expense_service():
    service = MagicMock(spec=ExpenseService)
    service.get_all.return_value = []
    service.get_monthly_summary.return_value = {}
    return service


def test_category_report_empty(mock_expense_service):
    report = ReportService(mock_expense_service)
    assert report.category_report() == {}


def test_category_report_sums_by_category(mock_expense_service):
    mock_expense_service.get_all.return_value = [
        Expense(100.0, "food", "2024-01-10"),
        Expense(50.0, "food", "2024-01-20"),
        Expense(200.0, "rent", "2024-01-01"),
    ]
    report = ReportService(mock_expense_service)
    result = report.category_report()
    assert result["food"] == 150.0
    assert result["rent"] == 200.0


def test_monthly_report_delegates_to_service(mock_expense_service):
    mock_expense_service.get_monthly_summary.return_value = {"2024-01": 300.0, "2024-02": 200.0}
    report = ReportService(mock_expense_service)
    result = report.monthly_report()
    assert result["2024-01"] == 300.0
    assert result["2024-02"] == 200.0


@patch("services.report_service.plt")
def test_generate_chart_skips_when_no_data(mock_plt, mock_expense_service):
    mock_expense_service.get_all.return_value = []
    report = ReportService(mock_expense_service)
    report.generate_chart()
    mock_plt.show.assert_not_called()


@patch("services.report_service.plt")
def test_generate_chart_calls_show_with_data(mock_plt, mock_expense_service):
    mock_expense_service.get_all.return_value = [
        Expense(100.0, "food", "2024-01-10"),
    ]
    report = ReportService(mock_expense_service)
    report.generate_chart()
    mock_plt.show.assert_called_once()


@patch("services.report_service.plt")
def test_generate_chart_sets_title(mock_plt, mock_expense_service):
    mock_expense_service.get_all.return_value = [
        Expense(100.0, "food", "2024-01-10"),
    ]
    report = ReportService(mock_expense_service)
    report.generate_chart()
    mock_plt.title.assert_called_once()
