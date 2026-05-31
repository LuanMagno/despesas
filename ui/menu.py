from models.budget import Budget
from models.category import Category
from models.expense import Expense
from utils.formatters import format_currency, format_expense_row


class Menu:
    """Interface de linha de comando do controle de despesas."""

    def __init__(self, expense_service, category_service, budget_service, report_service, chart_service):
        self.expense_service = expense_service
        self.category_service = category_service
        self.budget_service = budget_service
        self.report_service = report_service
        self.chart_service = chart_service

    def add_expense(self) -> None:
        """Solicita dados e cadastra uma despesa."""
        if not self._show_categories():
            print("Cadastre uma categoria antes de adicionar despesas.")
            return
        try:
            amount = float(input("Valor: ").strip())
            category = input("Categoria: ").strip()
            if not self.category_service.exists(category):
                print("Categoria nao cadastrada.")
                return
            date = input("Data (AAAA-MM-DD) [Enter para hoje]: ").strip()
            description = input("Descricao: ").strip()
            expense = Expense(amount, category, date or None, description)

            if self.expense_service.add(expense):
                print("Despesa adicionada com sucesso.")
                spent = self.expense_service.get_total_by_category(category)
                if self.budget_service.check_overspend(category, spent):
                    budget = self.budget_service.get_budget(category)
                    print(f"AVISO: Limite de {format_currency(budget.limit)} para '{category}' foi ultrapassado!")
            else:
                print("Erro ao adicionar despesa. Verifique valor, categoria e data.")
        except (ValueError, KeyboardInterrupt):
            print("Operacao cancelada ou valor invalido.")

    def manage_expenses(self) -> None:
        """Gerencia visualizacao, cadastro, remocao e edicao de despesas."""
        print("\n--- Despesas ---")
        self._show_expenses()
        print("1. Visualizar  2. Adicionar  3. Remover  4. Editar  5. Voltar")
        choice = input("Opcao: ").strip()
        if choice == "1":
            self.view_expenses()
        elif choice == "2":
            self.add_expense()
        elif choice == "3":
            self.delete_expense()
        elif choice == "4":
            self.edit_expense()

    def view_expenses(self) -> None:
        """Mostra despesas cadastradas, com filtro opcional por categoria."""
        category = input("Filtrar por categoria? (Enter para todas): ").strip().lower()
        expenses = self.expense_service.get_by_category(category) if category else self.expense_service.get_all()
        if not expenses:
            print("Nenhuma despesa encontrada.")
            return
        for index, expense in enumerate(expenses, 1):
            print(format_expense_row(index, expense))
        total = sum(expense.amount for expense in expenses)
        print(f"\nTotal: {format_currency(total)}")

    def delete_expense(self) -> None:
        """Remove uma despesa escolhida pelo usuario."""
        expenses = self.expense_service.get_all()
        if not expenses:
            print("Nenhuma despesa cadastrada.")
            return
        for index, expense in enumerate(expenses, 1):
            print(format_expense_row(index, expense))
        try:
            selected = int(input("Numero da despesa a remover: ").strip()) - 1
            if self.expense_service.delete(selected):
                print("Despesa removida com sucesso.")
            else:
                print("Indice invalido.")
        except ValueError:
            print("Entrada invalida.")

    def edit_expense(self) -> None:
        """Edita uma despesa escolhida pelo usuario."""
        expenses = self.expense_service.get_all()
        if not expenses:
            print("Nenhuma despesa cadastrada.")
            return
        self._show_expenses()
        try:
            selected = int(input("Numero da despesa a editar: ").strip()) - 1
            if selected < 0 or selected >= len(expenses):
                print("Indice invalido.")
                return

            current = expenses[selected]
            self._show_categories()
            amount_text = input(f"Valor [{current.amount}]: ").strip()
            category = input(f"Categoria [{current.category}]: ").strip() or current.category
            if not self.category_service.exists(category):
                print("Categoria nao cadastrada.")
                return
            date = input(f"Data [{current.date}]: ").strip() or current.date
            description = input(f"Descricao [{current.description}]: ").strip() or current.description
            amount = float(amount_text) if amount_text else current.amount
            updated = Expense(amount, category, date, description)

            if self.expense_service.update(selected, updated):
                print("Despesa editada com sucesso.")
            else:
                print("Despesa invalida.")
        except ValueError:
            print("Entrada invalida.")

    def manage_categories(self) -> None:
        """Gerencia cadastro e remocao de categorias."""
        print("\n--- Categorias ---")
        self._show_categories()
        print("1. Adicionar  2. Remover  3. Voltar")
        choice = input("Opcao: ").strip()
        if choice == "1":
            name = input("Nome da categoria: ").strip()
            description = input("Descricao (opcional): ").strip()
            if self.category_service.add(Category(name, description)):
                print("Categoria adicionada com sucesso.")
            else:
                print("Categoria invalida ou ja existe.")
        elif choice == "2":
            name = input("Nome da categoria a remover: ").strip()
            if self.category_service.delete(name):
                print("Categoria removida com sucesso.")
            else:
                print("Categoria nao encontrada.")

    def manage_budgets(self) -> None:
        """Gerencia orcamentos por categoria."""
        print("\n--- Orcamentos ---")
        self._show_budgets()
        print("1. Adicionar  2. Editar  3. Excluir  4. Voltar")
        choice = input("Opcao: ").strip()
        if choice == "1":
            self.add_budget()
        elif choice == "2":
            self.edit_budget()
        elif choice == "3":
            self.delete_budget()

    def add_budget(self) -> None:
        """Adiciona um orcamento para uma categoria existente."""
        if not self._show_categories():
            print("Cadastre uma categoria antes de criar orcamentos.")
            return
        category = input("Categoria: ").strip()
        if not self.category_service.exists(category):
            print("Categoria nao cadastrada.")
            return
        try:
            limit = float(input("Limite (R$): ").strip())
            if self.budget_service.set_budget(Budget(category, limit)):
                print("Orcamento definido com sucesso.")
            else:
                print("Orcamento invalido.")
        except ValueError:
            print("Valor invalido.")

    def edit_budget(self) -> None:
        """Edita o limite de um orcamento existente."""
        if not self.budget_service.get_all():
            print("Nenhum orcamento cadastrado.")
            return
        category = input("Categoria do orcamento a editar: ").strip()
        if self.budget_service.get_budget(category) is None:
            print("Orcamento nao encontrado.")
            return
        try:
            limit = float(input("Novo limite (R$): ").strip())
            if self.budget_service.set_budget(Budget(category, limit)):
                print("Orcamento editado com sucesso.")
            else:
                print("Orcamento invalido.")
        except ValueError:
            print("Valor invalido.")

    def delete_budget(self) -> None:
        """Exclui um orcamento por categoria."""
        if not self.budget_service.get_all():
            print("Nenhum orcamento cadastrado.")
            return
        category = input("Categoria do orcamento a excluir: ").strip()
        if self.budget_service.delete(category):
            print("Orcamento excluido com sucesso.")
        else:
            print("Orcamento nao encontrado.")

    def generate_report(self) -> None:
        """Exibe relatorios por categoria e por mes."""
        print("\n--- Relatorio por Categoria ---")
        data = self.report_service.category_report()
        if not data:
            print("Nenhuma despesa registrada.")
            return
        for category, total in sorted(data.items(), key=lambda item: item[1], reverse=True):
            print(f"  {category.capitalize()}: {format_currency(total)}")
        print(f"\nTotal geral: {format_currency(self.report_service.total_report())}")

        print("\n--- Relatorio Mensal ---")
        for month, total in sorted(self.report_service.monthly_report().items()):
            print(f"  {month}: {format_currency(total)}")

        if input("\nGerar grafico? (s/n): ").strip().lower() == "s":
            if not self.chart_service.generate_category_chart():
                print("Nenhuma despesa para exibir no grafico.")

    def run(self) -> None:
        """Executa o loop principal do menu."""
        while True:
            print("\n=== Controle de Despesas Pessoais ===")
            print("1. Gerenciar despesas")
            print("2. Gerenciar categorias")
            print("3. Gerenciar orcamentos")
            print("4. Relatorios / Grafico")
            print("5. Sair")
            choice = input("Escolha: ").strip()
            if choice == "1":
                self.manage_expenses()
            elif choice == "2":
                self.manage_categories()
            elif choice == "3":
                self.manage_budgets()
            elif choice == "4":
                self.generate_report()
            elif choice == "5":
                print("Encerrando...")
                break
            else:
                print("Opcao invalida.")

    def _show_categories(self) -> bool:
        """Mostra categorias cadastradas e retorna se existe alguma."""
        categories = self.category_service.get_all()
        if not categories:
            print("  Nenhuma categoria cadastrada.")
            return False
        print("Categorias cadastradas:")
        for category in categories:
            print(f"  - {category}")
        return True

    def _show_expenses(self) -> bool:
        """Mostra despesas cadastradas e retorna se existe alguma."""
        expenses = self.expense_service.get_all()
        if not expenses:
            print("  Nenhuma despesa cadastrada.")
            return False
        for index, expense in enumerate(expenses, 1):
            print(format_expense_row(index, expense))
        return True

    def _show_budgets(self) -> bool:
        """Mostra orcamentos cadastrados e retorna se existe algum."""
        budgets = self.budget_service.get_all()
        if not budgets:
            print("  Nenhum orcamento cadastrado.")
            return False
        for budget in budgets:
            spent = self.expense_service.get_total_by_category(budget.category)
            status = "EXCEDIDO" if self.budget_service.check_overspend(budget.category, spent) else "OK"
            print(f"  {budget} | Gasto: {format_currency(spent)} [{status}]")
        return True
