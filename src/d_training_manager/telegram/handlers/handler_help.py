from telebot import TeleBot
from telebot.types import Message


def process_message(message: Message, bot: TeleBot) -> None:
    bot.reply_to(message, "Hello! I am your training manager bot.")
