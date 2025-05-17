import telebot

from d_training_manager import config

bot = telebot.TeleBot(config.telegram.api_token)
