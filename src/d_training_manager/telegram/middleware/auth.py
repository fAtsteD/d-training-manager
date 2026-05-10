from typing import Optional

from aws_lambda_powertools import Logger, Tracer
from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message

from d_training_manager.telegram import telegram_user

logger = Logger(child=True)
tracer = Tracer()


class AuthMiddleware(BaseMiddleware):

    def __init__(self, skip_texts: list[str] = []):
        self.update_types = ["message", "edited_message"]
        self.skip_texts = skip_texts

    def pre_process(self, message: Message, data: dict):
        logger.append_keys(
            telegram_id=message.from_user.id if message.from_user else None,
            user_id=None,
        )

        if message.text in self.skip_texts or message.contact:
            logger.info("Skipping authentication for message")
            return

        user = telegram_user.get_user_by_message(message)

        if not user:
            logger.warning("Unauthorized access attempt")
            return CancelUpdate()

        logger.append_keys(
            telegram_id=int(user.telegram_id),
            user_id=user.id,
        )
        tracer.put_metadata(key="user_id", value=user.id)
        logger.info("User authenticated successfully")

    def post_process(self, message: Message, data: dict, exception: Optional[Exception]):
        pass
