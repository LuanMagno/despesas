class ReportService:
    """Gera dados consolidados para relatorios."""

    def __init__(self, expense_service):
        self.expense_service = expense_service

    def category_report(self) -> dict[str, float]:
        """Soma despesas agrupadas por categoria."""
        summary: dict[str, float] = {}
        for expense in self.expense_service.get_all():
            summary[expense.category] = summary.get(expense.category, 0.0) + expense.amount
        return summary

    def monthly_report(self) -> dict[str, float]:
        """Retorna o resumo mensal produzido pelo servico de despesas."""
        return self.expense_service.get_monthly_summary()

    def total_report(self) -> float:
        """Calcula o total geral do relatorio por categoria."""
        return sum(self.category_report().values())
