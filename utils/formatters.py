from datetime import datetime


def format_currency(value: float) -> str:
    return f"R$ {value:,.2f}"


def format_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return date_str


def format_expense_row(index: int, expense) -> str:
    return (
        f"{index}. {format_date(expense.date)} - "
        f"{expense.category.capitalize()}: {format_currency(expense.amount)} "
        f"({expense.description})"
    )
