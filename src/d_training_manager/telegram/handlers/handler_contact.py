from typing import Optional

from aws_lambda_powertools import Logger, Tracer
from telebot import TeleBot
from telebot.types import Message

from d_training_manager.database import user_registry
from d_training_manager.database.models import DBUser

tracer = Tracer()
logger = Logger(child=True)


@tracer.capture_method
def process_message(message: Message, bot: TeleBot) -> None:
    contact = message.contact
    from_user = message.from_user

    if not contact or not from_user:
        return

    telegram_id = contact.user_id or from_user.id

    if not telegram_id:
        bot.send_message(
            message.chat.id, "Invalid contact information.\n" + "Please share your phone number to authenticate."
        )
        logger.warning("Received contact information without user's telegram ID")
        return

    if not contact.phone_number:
        return

    phone_number = _clean_phone_number(contact.phone_number)
    user = _update_user(
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_number=phone_number,
        telegram_id=telegram_id,
    )
    bot.send_message(
        message.chat.id,
        "You have been successfully authenticated.\n\n" + "You can run `/help` to get a list of available commands.",
    )
    logger.info("User created/updated successfully")


def _clean_phone_number(phone_number: str) -> str:
    return "".join(filter(lambda char: char.isdigit() or char in ["+"], phone_number))


def _update_user(
    telegram_id: int,
    phone_number: str,
    first_name: str,
    last_name: Optional[str] = None,
) -> DBUser:
    user = user_registry.get_by_telegram_id(telegram_id)

    if not user:
        user = user_registry.get_by_phone(phone_number)

    if not user:
        user = DBUser()

    user.phone = phone_number
    user.telegram_id = telegram_id

    if not user.first_name and first_name:
        user.first_name = first_name

    if not user.last_name and last_name:
        user.last_name = last_name

    user_registry.update(user)
    return user
