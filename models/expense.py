from dataclasses import dataclass, field

from services.date_service import DateService
from services.validation_service import ValidationService


@dataclass
class Expense:
    """Representa uma despesa cadastrada pelo usuario."""

    amount: float
    category: str
    date: str | None = None
    description: str = ""
    _date_service: DateService = field(default_factory=DateService, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.amount = float(self.amount)
        self.category = self.category.strip().lower()
        self.date = self.date or self._date_service.today()
        self.description = self.description.strip()

    def to_dict(self) -> dict:
        """Converte a despesa para um dicionario serializavel em JSON."""
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Cria uma despesa a partir de um dicionario."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data.get("date"),
            description=data.get("description", ""),
        )

    def validate(self) -> bool:
        """Verifica se a despesa possui valor, categoria e data validos."""
        validator = ValidationService()
        return (
            validator.validate_amount(self.amount)
            and validator.validate_category_name(self.category)
            and validator.validate_date(self.date)
        )

    def __str__(self) -> str:
        return f"{self.date} - {self.category.capitalize()}: R${self.amount:.2f} ({self.description})"
