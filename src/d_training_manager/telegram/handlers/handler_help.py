import telebot


def send_help(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    bot.reply_to(message, "Hello! I am your training manager bot.")
