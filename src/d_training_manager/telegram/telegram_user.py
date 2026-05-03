from typing import Optional

from telebot.types import Message

from d_training_manager.database.models import DBUser
from d_training_manager.database.registry_user import UserRegistry


def get_user_by_message(message: Message) -> Optional[DBUser]:
    message_user = message.from_user

    if not message_user:
        return None

    user_registry = UserRegistry()
    return user_registry.get_by_telegram_id(message_user.id)
