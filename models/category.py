from dataclasses import dataclass


@dataclass
class Category:
    """Representa uma categoria usada para agrupar despesas."""

    name: str
    description: str = ""

    def __post_init__(self) -> None:
        self.name = self.name.strip().lower()
        self.description = self.description.strip()

    def to_dict(self) -> dict:
        """Converte a categoria para um dicionario serializavel em JSON."""
        return {"name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Cria uma categoria a partir de um dicionario."""
        return cls(name=data["name"], description=data.get("description", ""))

    def __str__(self) -> str:
        return self.name.capitalize()
