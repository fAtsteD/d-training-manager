import telebot

from d_training_manager import config
from d_training_manager.telegram.handlers import handler_help


def create_bot() -> telebot.TeleBot:
    return telebot.TeleBot(
        threaded=False,
        token=config.telegram.api_token,
    )


def process_update_dict(update: dict) -> None:
    """Create a bot and process the given update"""
    bot = create_bot()
    register_handlers(bot)
    update_obj = telebot.types.Update.de_json(update)

    if update_obj:
        bot.process_new_updates([update_obj])


def register_handlers(bot: telebot.TeleBot) -> None:
    bot.register_message_handler(
        callback=handler_help.send_help,
        commands=["help", "start"],
        pass_bot=True,
    )
