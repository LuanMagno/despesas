from models.expense import Expense


class ExpenseRepository:
    """Persistencia de despesas dentro do arquivo JSON."""

    def __init__(self, storage):
        self.storage = storage

    def list_all(self) -> list[Expense]:
        """Lista todas as despesas salvas."""
        data = self.storage.load()
        return [Expense.from_dict(item) for item in data.get("expenses", [])]

    def save_all(self, expenses: list[Expense]) -> bool:
        """Substitui a lista de despesas persistida."""
        data = self.storage.load()
        data["expenses"] = [expense.to_dict() for expense in expenses]
        return self.storage.save(data)

    def add(self, expense: Expense) -> bool:
        """Adiciona uma despesa ao armazenamento."""
        expenses = self.list_all()
        expenses.append(expense)
        return self.save_all(expenses)

    def delete(self, index: int) -> bool:
        """Remove uma despesa pelo indice zero-based."""
        expenses = self.list_all()
        if 0 <= index < len(expenses):
            expenses.pop(index)
            return self.save_all(expenses)
        return False

    def update(self, index: int, expense: Expense) -> bool:
        """Atualiza uma despesa pelo indice zero-based."""
        expenses = self.list_all()
        if 0 <= index < len(expenses):
            expenses[index] = expense
            return self.save_all(expenses)
        return False

    def find_by_category(self, category: str) -> list[Expense]:
        """Busca despesas de uma categoria."""
        normalized = category.strip().lower()
        return [expense for expense in self.list_all() if expense.category == normalized]
