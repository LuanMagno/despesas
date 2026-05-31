from datetime import datetime


class Expense:
    def __init__(self, amount: float, category: str, date: str = None, description: str = ""):
        self.amount = float(amount)
        self.category = category.strip().lower()
        self.date = date if date else datetime.today().strftime('%Y-%m-%d')
        self.description = description

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            amount=data["amount"],
            category=data["category"],
            date=data.get("date"),
            description=data.get("description", ""),
        )

    def validate(self) -> bool:
        if self.amount <= 0:
            return False
        if not self.category.strip():
            return False
        try:
            datetime.strptime(self.date, '%Y-%m-%d')
        except ValueError:
            return False
        return True

    def __str__(self) -> str:
        return (
            f"{self.date} - {self.category.capitalize()}: "
            f"R${self.amount:.2f} ({self.description})"
        )
