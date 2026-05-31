from dataclasses import dataclass


@dataclass
class Budget:
    """Representa o limite de gasto de uma categoria."""

    category: str
    limit: float

    def __post_init__(self) -> None:
        self.category = self.category.strip().lower()
        self.limit = float(self.limit)

    def to_dict(self) -> dict:
        """Converte o orcamento para um dicionario serializavel em JSON."""
        return {"category": self.category, "limit": self.limit}

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Cria um orcamento a partir de um dicionario."""
        return cls(category=data["category"], limit=data["limit"])

    def check_limit(self, spent: float) -> bool:
        """Retorna True quando o gasto esta dentro do limite."""
        return spent <= self.limit

    def __str__(self) -> str:
        return f"{self.category.capitalize()}: R${self.limit:.2f}"
