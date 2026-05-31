import matplotlib.pyplot as plt


class ReportService:
    def __init__(self, expense_service):
        self.expense_service = expense_service

    def category_report(self) -> dict:
        summary = {}
        for expense in self.expense_service.get_all():
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount
        return summary

    def monthly_report(self) -> dict:
        return self.expense_service.get_monthly_summary()

    def generate_chart(self) -> None:
        data = self.category_report()
        if not data:
            print("Nenhuma despesa para exibir no gráfico.")
            return
        plt.figure(figsize=(8, 6))
        plt.bar(data.keys(), data.values(), color="skyblue")
        plt.title("Distribuição de Despesas por Categoria")
        plt.xlabel("Categoria")
        plt.ylabel("Valor Gasto (R$)")
        plt.tight_layout()
        plt.show()
