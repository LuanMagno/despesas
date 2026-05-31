from datetime import datetime


class DateService:
    """Agrupa operacoes de data usadas pelo sistema."""

    def today(self) -> str:
        """Retorna a data atual no formato AAAA-MM-DD."""
        return datetime.today().strftime("%Y-%m-%d")

    def month_key(self, date_str: str) -> str:
        """Retorna a chave mensal AAAA-MM de uma data AAAA-MM-DD."""
        return date_str[:7]

    def format_br(self, date_str: str) -> str:
        """Formata uma data AAAA-MM-DD para DD/MM/AAAA."""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except (TypeError, ValueError):
            return date_str
