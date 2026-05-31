from unittest.mock import MagicMock, patch

from services.chart_service import ChartService


def test_generate_category_chart_returns_false_without_data():
    report_service = MagicMock()
    report_service.category_report.return_value = {}
    chart = ChartService(report_service)
    assert chart.generate_category_chart() is False


@patch("services.chart_service.plt")
def test_generate_category_chart_calls_matplotlib(mock_plt):
    report_service = MagicMock()
    report_service.category_report.return_value = {"alimentacao": 100.0}
    chart = ChartService(report_service)
    assert chart.generate_category_chart() is True
    mock_plt.bar.assert_called_once()
    mock_plt.show.assert_called_once()
