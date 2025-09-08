import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DatabaseConfig:
    @property
    def connection(self) -> Optional[str]:
        return os.getenv("DB_CONNECTION", None)

    @property
    def host(self) -> Optional[str]:
        return os.getenv("DB_HOST", None)

    @property
    def port(self) -> Optional[str]:
        return os.getenv("DB_PORT", None)

    @property
    def url(self) -> Optional[str]:
        if self.connection and self.host and self.port:
            return f"{self.connection}://{self.host}:{self.port}"

        return None
