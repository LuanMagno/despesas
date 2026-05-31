from models.budget import Budget
from repositories.budget_repository import BudgetRepository
from services.validation_service import ValidationService


class BudgetService:
    """Executa regras de negocio relacionadas a orcamentos."""

    def __init__(self, repository_or_storage, validator: ValidationService | None = None):
        if isinstance(repository_or_storage, BudgetRepository):
            self.repository = repository_or_storage
        else:
            self.repository = BudgetRepository(repository_or_storage)
        self.validator = validator or ValidationService()

    def set_budget(self, budget: Budget) -> bool:
        """Cria ou atualiza o orcamento de uma categoria."""
        if not self.validator.validate_category_name(budget.category):
            return False
        if not self.validator.validate_amount(budget.limit):
            return False
        return self.repository.upsert(budget)

    def get_budget(self, category: str) -> Budget | None:
        """Busca o orcamento de uma categoria."""
        if not self.validator.validate_category_name(category):
            return None
        return self.repository.find_by_category(category)

    def check_overspend(self, category: str, spent: float) -> bool:
        """Retorna True quando o gasto ultrapassa o orcamento."""
        budget = self.get_budget(category)
        if budget is None:
            return False
        return not budget.check_limit(spent)

    def delete(self, category: str) -> bool:
        """Remove o orcamento de uma categoria."""
        if not self.validator.validate_category_name(category):
            return False
        return self.repository.delete(category)

    def get_all(self) -> list[Budget]:
        """Retorna todos os orcamentos cadastrados."""
        return self.repository.list_all()
