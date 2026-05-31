from models.expense import Expense


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage
        self._expenses: list = []
        self._load()

    def _load(self):
        data = self.storage.load()
        self._expenses = [Expense.from_dict(e) for e in data.get("expenses", [])]

    def _save(self):
        data = self.storage.load()
        data["expenses"] = [e.to_dict() for e in self._expenses]
        self.storage.save(data)

    def add(self, expense: Expense) -> bool:
        if not expense.validate():
            return False
        self._expenses.append(expense)
        self._save()
        return True

    def delete(self, index: int) -> bool:
        if 0 <= index < len(self._expenses):
            self._expenses.pop(index)
            self._save()
            return True
        return False

    def get_all(self) -> list:
        return list(self._expenses)

    def get_by_category(self, category: str) -> list:
        return [e for e in self._expenses if e.category == category.strip().lower()]

    def get_total(self) -> float:
        return sum(e.amount for e in self._expenses)

    def get_monthly_summary(self) -> dict:
        summary = {}
        for expense in self._expenses:
            month = expense.date[:7]
            summary[month] = summary.get(month, 0) + expense.amount
        return summary
