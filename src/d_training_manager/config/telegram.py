import os
from dataclasses import dataclass


@dataclass
class TelegramConfig:
    @property
    def api_token(self) -> str:
        return os.getenv("TELEGRAM_API_TOKEN", "")
