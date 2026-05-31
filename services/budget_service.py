from models.budget import Budget


class BudgetService:
    def __init__(self, storage):
        self.storage = storage
        self._budgets: list = []
        self._load()

    def _load(self):
        data = self.storage.load()
        self._budgets = [Budget.from_dict(b) for b in data.get("budgets", [])]

    def _save(self):
        data = self.storage.load()
        data["budgets"] = [b.to_dict() for b in self._budgets]
        self.storage.save(data)

    def set_budget(self, budget: Budget) -> None:
        for i, b in enumerate(self._budgets):
            if b.category == budget.category:
                self._budgets[i] = budget
                self._save()
                return
        self._budgets.append(budget)
        self._save()

    def get_budget(self, category: str):
        for b in self._budgets:
            if b.category == category.strip().lower():
                return b
        return None

    def check_overspend(self, category: str, spent: float) -> bool:
        budget = self.get_budget(category)
        if budget is None:
            return False
        return not budget.check_limit(spent)

    def get_all(self) -> list:
        return list(self._budgets)
