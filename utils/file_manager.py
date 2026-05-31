import os
import shutil
from datetime import datetime


class FileManager:
    """Oferece operacoes simples para arquivos usados pela aplicacao."""

    def exists(self, filepath: str) -> bool:
        """Retorna True quando o arquivo existe."""
        return os.path.exists(filepath)

    def ensure_parent_dir(self, filepath: str) -> None:
        """Cria o diretorio pai do arquivo quando ele foi informado."""
        parent = os.path.dirname(filepath)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def backup(self, filepath: str) -> str:
        """Cria uma copia de seguranca do arquivo e retorna o caminho criado."""
        if not self.exists(filepath):
            return ""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)
        return backup_path
