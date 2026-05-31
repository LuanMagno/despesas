from models.category import Category


class CategoryRepository:
    """Persistencia de categorias dentro do arquivo JSON."""

    def __init__(self, storage):
        self.storage = storage

    def list_all(self) -> list[Category]:
        """Lista todas as categorias salvas."""
        data = self.storage.load()
        return [Category.from_dict(item) for item in data.get("categories", [])]

    def save_all(self, categories: list[Category]) -> bool:
        """Substitui a lista de categorias persistida."""
        data = self.storage.load()
        data["categories"] = [category.to_dict() for category in categories]
        return self.storage.save(data)

    def add(self, category: Category) -> bool:
        """Adiciona uma categoria ao armazenamento."""
        categories = self.list_all()
        categories.append(category)
        return self.save_all(categories)

    def delete(self, name: str) -> bool:
        """Remove uma categoria pelo nome."""
        normalized = name.strip().lower()
        categories = self.list_all()
        updated = [category for category in categories if category.name != normalized]
        if len(updated) == len(categories):
            return False
        return self.save_all(updated)

    def find_by_name(self, name: str) -> Category | None:
        """Busca uma categoria pelo nome."""
        normalized = name.strip().lower()
        for category in self.list_all():
            if category.name == normalized:
                return category
        return None
