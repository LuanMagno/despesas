from models.category import Category


class CategoryService:
    def __init__(self, storage):
        self.storage = storage
        self._categories: list = []
        self._load()

    def _load(self):
        data = self.storage.load()
        self._categories = [Category.from_dict(c) for c in data.get("categories", [])]

    def _save(self):
        data = self.storage.load()
        data["categories"] = [c.to_dict() for c in self._categories]
        self.storage.save(data)

    def add(self, category: Category) -> bool:
        if self.exists(category.name):
            return False
        self._categories.append(category)
        self._save()
        return True

    def delete(self, name: str) -> bool:
        for i, c in enumerate(self._categories):
            if c.name == name.strip().lower():
                self._categories.pop(i)
                self._save()
                return True
        return False

    def get_all(self) -> list:
        return list(self._categories)

    def exists(self, name: str) -> bool:
        return any(c.name == name.strip().lower() for c in self._categories)
