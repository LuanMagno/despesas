from services.date_service import DateService


def format_currency(value: float) -> str:
    """Formata valores monetarios em reais."""
    return f"R$ {value:,.2f}"


def format_date(date_str: str) -> str:
    """Formata uma data AAAA-MM-DD para DD/MM/AAAA."""
    return DateService().format_br(date_str)


def format_expense_row(index: int, expense) -> str:
    """Formata uma linha de despesa para exibicao no terminal."""
    return (
        f"{index}. {format_date(expense.date)} - "
        f"{expense.category.capitalize()}: {format_currency(expense.amount)} "
        f"({expense.description})"
    )
