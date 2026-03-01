import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    @property
    def url(self) -> Optional[str]:
        return os.getenv("DB_URL", None) or None
