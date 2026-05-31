from storage.file_storage import FileStorage
from services.expense_service import ExpenseService
from services.category_service import CategoryService
from services.budget_service import BudgetService
from services.report_service import ReportService
from models.expense import Expense
from models.category import Category
from models.budget import Budget
from utils.validators import validate_amount, validate_date, validate_category_name
from utils.formatters import format_expense_row, format_currency


class ExpenseTracker:
    def __init__(self, data_file: str = "expenses.json"):
        storage = FileStorage(data_file)
        self.expense_service = ExpenseService(storage)
        self.category_service = CategoryService(storage)
        self.budget_service = BudgetService(storage)
        self.report_service = ReportService(self.expense_service)

    def add_expense(self):
        try:
            amount_str = input("Valor: ").strip()
            if not validate_amount(amount_str):
                print("Valor inválido.")
                return
            amount = float(amount_str)

            category = input("Categoria (ex: alimentação, aluguel): ").strip()
            if not validate_category_name(category):
                print("Categoria inválida.")
                return

            date = input("Data (AAAA-MM-DD) [Enter para hoje]: ").strip()
            if date and not validate_date(date):
                print("Data inválida.")
                return

            description = input("Descrição: ").strip()
            expense = Expense(amount, category, date or None, description)

            if self.expense_service.add(expense):
                print("Despesa adicionada com sucesso.")
                spent = sum(e.amount for e in self.expense_service.get_by_category(category))
                if self.budget_service.check_overspend(category, spent):
                    budget = self.budget_service.get_budget(category)
                    print(f"AVISO: Limite de {format_currency(budget.limit)} para '{category}' foi ultrapassado!")
            else:
                print("Erro ao adicionar despesa.")
        except (ValueError, KeyboardInterrupt):
            print("Operação cancelada.")

    def view_expenses(self):
        category = input("Filtrar por categoria? (Enter para todas): ").strip().lower()
        expenses = (
            self.expense_service.get_by_category(category)
            if category
            else self.expense_service.get_all()
        )
        if not expenses:
            print("Nenhuma despesa encontrada.")
            return
        for i, e in enumerate(expenses, 1):
            print(format_expense_row(i, e))
        print(f"\nTotal: {format_currency(sum(e.amount for e in expenses))}")

    def delete_expense(self):
        expenses = self.expense_service.get_all()
        if not expenses:
            print("Nenhuma despesa cadastrada.")
            return
        for i, e in enumerate(expenses, 1):
            print(format_expense_row(i, e))
        try:
            index = int(input("Número da despesa a remover: ").strip()) - 1
            if self.expense_service.delete(index):
                print("Despesa removida com sucesso.")
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida.")

    def manage_categories(self):
        print("\n--- Categorias ---")
        cats = self.category_service.get_all()
        if cats:
            for c in cats:
                print(f"  • {c}")
        else:
            print("  Nenhuma categoria cadastrada.")
        print("1. Adicionar  2. Remover  3. Voltar")
        choice = input("Opção: ").strip()
        if choice == "1":
            name = input("Nome da categoria: ").strip()
            desc = input("Descrição (opcional): ").strip()
            if self.category_service.add(Category(name, desc)):
                print("Categoria adicionada com sucesso.")
            else:
                print("Categoria já existe.")
        elif choice == "2":
            name = input("Nome da categoria a remover: ").strip()
            if self.category_service.delete(name):
                print("Categoria removida com sucesso.")
            else:
                print("Categoria não encontrada.")

    def manage_budgets(self):
        print("\n--- Orçamentos ---")
        budgets = self.budget_service.get_all()
        if budgets:
            for b in budgets:
                spent = sum(e.amount for e in self.expense_service.get_by_category(b.category))
                status = "EXCEDIDO" if self.budget_service.check_overspend(b.category, spent) else "OK"
                print(f"  {b} | Gasto: {format_currency(spent)} [{status}]")
        else:
            print("  Nenhum orçamento cadastrado.")
        print("1. Definir orçamento  2. Voltar")
        if input("Opção: ").strip() == "1":
            category = input("Categoria: ").strip()
            try:
                limit = float(input("Limite (R$): ").strip())
                self.budget_service.set_budget(Budget(category, limit))
                print("Orçamento definido com sucesso.")
            except ValueError:
                print("Valor inválido.")

    def generate_report(self):
        print("\n--- Relatório por Categoria ---")
        data = self.report_service.category_report()
        if not data:
            print("Nenhuma despesa registrada.")
            return
        for cat, total in sorted(data.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat.capitalize()}: {format_currency(total)}")
        print(f"\nTotal geral: {format_currency(sum(data.values()))}")

        print("\n--- Relatório Mensal ---")
        monthly = self.report_service.monthly_report()
        for month, total in sorted(monthly.items()):
            print(f"  {month}: {format_currency(total)}")

        if input("\nGerar gráfico? (s/n): ").strip().lower() == "s":
            self.report_service.generate_chart()

    def run(self):
        while True:
            print("\n=== Controle de Despesas Pessoais ===")
            print("1. Adicionar despesa")
            print("2. Visualizar despesas")
            print("3. Remover despesa")
            print("4. Gerenciar categorias")
            print("5. Gerenciar orçamentos")
            print("6. Relatórios / Gráfico")
            print("7. Sair")
            choice = input("Escolha: ").strip()
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.delete_expense()
            elif choice == "4":
                self.manage_categories()
            elif choice == "5":
                self.manage_budgets()
            elif choice == "6":
                self.generate_report()
            elif choice == "7":
                print("Encerrando...")
                break
            else:
                print("Opção inválida.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
