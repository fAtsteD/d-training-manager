from telebot import TeleBot
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup

from d_training_manager.telegram import telegram_user


def process_message(message: Message, bot: TeleBot) -> None:
    user = telegram_user.get_user_by_message(message)

    if not user:
        _request_contact(bot, message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        "You are already authenticated.\n"
        + "How can I assist you today?"
        + "\n\n"
        + "You can run `/help` to get a list of available commands.",
    )


def _request_contact(bot: TeleBot, chat_id: int) -> None:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Share Phone Number", request_contact=True)
    markup.add(button)
    bot.send_message(
        chat_id,
        "Hello! I am your training manager bot.\n" + "Please share your phone number to authenticate.",
        reply_markup=markup,
    )
