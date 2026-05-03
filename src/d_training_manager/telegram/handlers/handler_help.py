from telebot import TeleBot
from telebot.types import Message


def process_message(message: Message, bot: TeleBot) -> None:
    bot.send_message(message.chat.id, "I am your training manager bot.\n\n" + _allowed_commands())


def _allowed_commands() -> str:
    return "\n".join(
        [
            "Available commands:",
            "/help - Show this message",
            "/start - Start the bot",
        ]
    )
