from typing import Optional

from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message

from d_training_manager.telegram import telegram_user


class AuthMiddleware(BaseMiddleware):

    def __init__(self, skip_texts: list[str] = []):
        self.update_types = ["message", "edited_message"]
        self.skip_texts = skip_texts

    def pre_process(self, message: Message, data: dict):
        if message.text in self.skip_texts or message.contact:
            return

        user = telegram_user.get_user_by_message(message)

        if not user:
            return CancelUpdate()

    def post_process(self, message: Message, data: dict, exception: Optional[Exception]):
        pass
