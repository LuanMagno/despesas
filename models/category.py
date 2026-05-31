class Category:
    def __init__(self, name: str, description: str = ""):
        self.name = name.strip().lower()
        self.description = description

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description}

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(name=data["name"], description=data.get("description", ""))

    def __str__(self) -> str:
        return self.name.capitalize()
