from telebot import TeleBot
from telebot.types import Update

from d_training_manager import config
from d_training_manager.telegram.handlers import handler_contact, handler_help, handler_start


def create_bot() -> TeleBot:
    return TeleBot(
        threaded=False,
        token=config.telegram.api_token,
    )


def process_update_dict(update: dict) -> None:
    """Create a bot and process the given update"""
    bot = create_bot()
    register_handlers(bot)
    update_obj = Update.de_json(update)

    if update_obj:
        bot.process_new_updates([update_obj])


def register_handlers(bot: TeleBot) -> None:
    bot.register_message_handler(
        callback=handler_contact.process_message,
        content_types=["contact"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handler_help.process_message,
        commands=["help"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handler_start.process_message,
        commands=["start"],
        pass_bot=True,
    )
