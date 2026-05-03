from telebot import TeleBot
from telebot.types import Update

from d_training_manager import config
from d_training_manager.telegram.handlers import handler_contact, handler_help, handler_start
from d_training_manager.telegram.middleware.auth import AuthMiddleware


def create_bot() -> TeleBot:
    return TeleBot(
        threaded=False,
        token=config.telegram.api_token,
        use_class_middlewares=True,
    )


def initialize_bot(bot: TeleBot) -> None:
    bot.setup_middleware(AuthMiddleware(skip_texts=["/start", "/help"]))
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


def process_update_dict(update: dict) -> None:
    """Create a bot and process the given update"""
    bot = create_bot()
    initialize_bot(bot)
    update_obj = Update.de_json(update)

    if update_obj:
        bot.process_new_updates([update_obj])
