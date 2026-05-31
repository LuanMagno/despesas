from datetime import datetime
from typing import Any


class ValidationService:
    """Centraliza validacoes usadas pelas regras de negocio."""

    def validate_amount(self, value: Any) -> bool:
        """Valida se o valor informado representa um numero positivo."""
        try:
            return float(value) > 0
        except (TypeError, ValueError):
            return False

    def validate_date(self, date_str: str | None) -> bool:
        """Valida datas no formato AAAA-MM-DD."""
        try:
            datetime.strptime(str(date_str), "%Y-%m-%d")
            return True
        except (TypeError, ValueError):
            return False

    def validate_category_name(self, name: Any) -> bool:
        """Valida se o nome da categoria e um texto nao vazio."""
        return isinstance(name, str) and bool(name.strip())

    def validate_index(self, index: int, size: int) -> bool:
        """Valida se um indice esta dentro do tamanho da lista."""
        return 0 <= index < size
