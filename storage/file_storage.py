import json
import os
import shutil
from datetime import datetime


class FileStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> dict:
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def save(self, data: dict) -> bool:
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False

    def backup(self) -> str:
        if not os.path.exists(self.filepath):
            return ""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f"{self.filepath}.{timestamp}.bak"
        shutil.copy2(self.filepath, backup_path)
        return backup_path
