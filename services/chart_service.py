import matplotlib.pyplot as plt


class ChartService:
    """Gera graficos a partir dos dados de relatorio."""

    def __init__(self, report_service):
        self.report_service = report_service

    def generate_category_chart(self) -> bool:
        """Gera um grafico de barras por categoria.

        Retorna False quando nao existem dados para exibir.
        """
        data = self.report_service.category_report()
        if not data:
            return False
        plt.figure(figsize=(8, 6))
        plt.bar(data.keys(), data.values(), color="skyblue")
        plt.title("Distribuicao de Despesas por Categoria")
        plt.xlabel("Categoria")
        plt.ylabel("Valor Gasto (R$)")
        plt.tight_layout()
        plt.show()
        return True
