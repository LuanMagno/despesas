from repositories.budget_repository import BudgetRepository
from repositories.category_repository import CategoryRepository
from repositories.expense_repository import ExpenseRepository
from services.budget_service import BudgetService
from services.category_service import CategoryService
from services.chart_service import ChartService
from services.expense_service import ExpenseService
from services.report_service import ReportService
from storage.file_storage import FileStorage
from ui.menu import Menu


class ExpenseTracker:
    """Fachada da aplicacao de controle de despesas pessoais."""

    def __init__(self, data_file: str = "expenses.json"):
        storage = FileStorage(data_file)
        self.expense_repository = ExpenseRepository(storage)
        self.category_repository = CategoryRepository(storage)
        self.budget_repository = BudgetRepository(storage)

        self.expense_service = ExpenseService(self.expense_repository)
        self.category_service = CategoryService(self.category_repository)
        self.budget_service = BudgetService(self.budget_repository)
        self.report_service = ReportService(self.expense_service)
        self.chart_service = ChartService(self.report_service)
        self.menu = Menu(
            self.expense_service,
            self.category_service,
            self.budget_service,
            self.report_service,
            self.chart_service,
        )

    def add_expense(self) -> None:
        """Encaminha o cadastro de despesa para o menu."""
        self.menu.add_expense()

    def manage_expenses(self) -> None:
        """Encaminha o gerenciamento de despesas para o menu."""
        self.menu.manage_expenses()

    def view_expenses(self) -> None:
        """Encaminha a visualizacao de despesas para o menu."""
        self.menu.view_expenses()

    def delete_expense(self) -> None:
        """Encaminha a remocao de despesa para o menu."""
        self.menu.delete_expense()

    def edit_expense(self) -> None:
        """Encaminha a edicao de despesa para o menu."""
        self.menu.edit_expense()

    def manage_categories(self) -> None:
        """Encaminha o gerenciamento de categorias para o menu."""
        self.menu.manage_categories()

    def manage_budgets(self) -> None:
        """Encaminha o gerenciamento de orcamentos para o menu."""
        self.menu.manage_budgets()

    def add_budget(self) -> None:
        """Encaminha o cadastro de orcamento para o menu."""
        self.menu.add_budget()

    def edit_budget(self) -> None:
        """Encaminha a edicao de orcamento para o menu."""
        self.menu.edit_budget()

    def delete_budget(self) -> None:
        """Encaminha a exclusao de orcamento para o menu."""
        self.menu.delete_budget()

    def generate_report(self) -> None:
        """Encaminha a geracao de relatorio para o menu."""
        self.menu.generate_report()

    def run(self) -> None:
        """Inicia a interface de linha de comando."""
        self.menu.run()


if __name__ == "__main__":
    ExpenseTracker().run()
