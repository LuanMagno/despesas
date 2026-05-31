from models.category import Category
from repositories.category_repository import CategoryRepository
from services.validation_service import ValidationService


class CategoryService:
    """Executa regras de negocio relacionadas a categorias."""

    def __init__(self, repository_or_storage, validator: ValidationService | None = None):
        if isinstance(repository_or_storage, CategoryRepository):
            self.repository = repository_or_storage
        else:
            self.repository = CategoryRepository(repository_or_storage)
        self.validator = validator or ValidationService()

    def add(self, category: Category) -> bool:
        """Adiciona uma categoria quando o nome e valido e ainda nao existe."""
        if not self.validator.validate_category_name(category.name):
            return False
        if self.exists(category.name):
            return False
        return self.repository.add(category)

    def delete(self, name: str) -> bool:
        """Remove uma categoria pelo nome."""
        if not self.validator.validate_category_name(name):
            return False
        return self.repository.delete(name)

    def get_all(self) -> list[Category]:
        """Retorna todas as categorias cadastradas."""
        return self.repository.list_all()

    def exists(self, name: str) -> bool:
        """Verifica se uma categoria ja esta cadastrada."""
        if not self.validator.validate_category_name(name):
            return False
        return self.repository.find_by_name(name) is not None
