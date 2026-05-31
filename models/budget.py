class Budget:
    def __init__(self, category: str, limit: float):
        self.category = category.strip().lower()
        self.limit = float(limit)

    def to_dict(self) -> dict:
        return {"category": self.category, "limit": self.limit}

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        return cls(category=data["category"], limit=data["limit"])

    def check_limit(self, spent: float) -> bool:
        return spent <= self.limit

    def __str__(self) -> str:
        return f"{self.category.capitalize()}: R${self.limit:.2f}"
