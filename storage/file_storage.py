import json

from utils.file_manager import FileManager


class FileStorage:
    """Responsavel por ler e gravar dados em um arquivo JSON."""

    def __init__(self, filepath: str, file_manager: FileManager | None = None):
        self.filepath = filepath
        self.file_manager = file_manager or FileManager()

    def load(self) -> dict:
        """Carrega os dados do arquivo JSON; retorna vazio em caso de erro."""
        if not self.file_manager.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError):
            return {}

    def save(self, data: dict) -> bool:
        """Salva um dicionario no arquivo JSON."""
        try:
            self.file_manager.ensure_parent_dir(self.filepath)
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except OSError:
            return False

    def backup(self) -> str:
        """Cria uma copia de seguranca do arquivo atual."""
        return self.file_manager.backup(self.filepath)
