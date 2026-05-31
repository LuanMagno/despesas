from models.expense import Expense
from repositories.expense_repository import ExpenseRepository
from services.date_service import DateService
from services.validation_service import ValidationService


class ExpenseService:
    """Executa regras de negocio relacionadas a despesas."""

    def __init__(
        self,
        repository_or_storage,
        validator: ValidationService | None = None,
        date_service: DateService | None = None,
    ):
        if isinstance(repository_or_storage, ExpenseRepository):
            self.repository = repository_or_storage
        else:
            self.repository = ExpenseRepository(repository_or_storage)
        self.validator = validator or ValidationService()
        self.date_service = date_service or DateService()

    def add(self, expense: Expense) -> bool:
        """Adiciona uma despesa valida."""
        if not expense.validate():
            return False
        return self.repository.add(expense)

    def delete(self, index: int) -> bool:
        """Remove uma despesa pelo indice informado."""
        return self.repository.delete(index)

    def update(self, index: int, expense: Expense) -> bool:
        """Atualiza uma despesa valida pelo indice informado."""
        if not expense.validate():
            return False
        return self.repository.update(index, expense)

    def get_all(self) -> list[Expense]:
        """Retorna todas as despesas cadastradas."""
        return self.repository.list_all()

    def get_by_category(self, category: str) -> list[Expense]:
        """Retorna despesas de uma categoria."""
        return self.repository.find_by_category(category)

    def get_total(self) -> float:
        """Calcula o total geral de despesas."""
        return sum(expense.amount for expense in self.get_all())

    def get_total_by_category(self, category: str) -> float:
        """Calcula o total gasto em uma categoria."""
        return sum(expense.amount for expense in self.get_by_category(category))

    def get_monthly_summary(self) -> dict[str, float]:
        """Agrupa despesas por mes no formato AAAA-MM."""
        summary: dict[str, float] = {}
        for expense in self.get_all():
            month = self.date_service.month_key(expense.date)
            summary[month] = summary.get(month, 0.0) + expense.amount
        return summary
