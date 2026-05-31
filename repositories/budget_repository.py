from models.budget import Budget


class BudgetRepository:
    """Persistencia de orcamentos dentro do arquivo JSON."""

    def __init__(self, storage):
        self.storage = storage

    def list_all(self) -> list[Budget]:
        """Lista todos os orcamentos salvos."""
        data = self.storage.load()
        return [Budget.from_dict(item) for item in data.get("budgets", [])]

    def save_all(self, budgets: list[Budget]) -> bool:
        """Substitui a lista de orcamentos persistida."""
        data = self.storage.load()
        data["budgets"] = [budget.to_dict() for budget in budgets]
        return self.storage.save(data)

    def upsert(self, budget: Budget) -> bool:
        """Cria ou atualiza o orcamento de uma categoria."""
        budgets = self.list_all()
        for index, current in enumerate(budgets):
            if current.category == budget.category:
                budgets[index] = budget
                return self.save_all(budgets)
        budgets.append(budget)
        return self.save_all(budgets)

    def delete(self, category: str) -> bool:
        """Remove um orcamento pela categoria."""
        normalized = category.strip().lower()
        budgets = self.list_all()
        updated = [budget for budget in budgets if budget.category != normalized]
        if len(updated) == len(budgets):
            return False
        return self.save_all(updated)

    def find_by_category(self, category: str) -> Budget | None:
        """Busca um orcamento por categoria."""
        normalized = category.strip().lower()
        for budget in self.list_all():
            if budget.category == normalized:
                return budget
        return None
