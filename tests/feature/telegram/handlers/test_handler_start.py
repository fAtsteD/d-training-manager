from telebot.types import ReplyKeyboardMarkup

from d_training_manager.telegram import bot
from tests.factories.database import DBUserFactory
from tests.fixtures.telegram import TelebotMock, TelegramCreateTextMessage


def test_request_contact(
    telegram_bot_mock: TelebotMock,
    telegram_create_text_message: TelegramCreateTextMessage,
):
    telegram_command = telegram_create_text_message("/start")

    bot.process_update_dict(telegram_command)

    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0].chat_id == telegram_command["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0].text.startswith(
        "Hello! I am your training manager bot.\n" + "Please share your phone number to authenticate.",
    )
    assert telegram_bot_mock.send_messages[0].reply_markup is not None
    assert isinstance(telegram_bot_mock.send_messages[0].reply_markup, ReplyKeyboardMarkup)
    assert isinstance(telegram_bot_mock.send_messages[0].reply_markup.keyboard[0][0], dict)
    assert telegram_bot_mock.send_messages[0].reply_markup.keyboard[0][0]["text"] == "Share Phone Number"
    assert telegram_bot_mock.send_messages[0].reply_markup.keyboard[0][0]["request_contact"] == True


def test_registered_user(
    telegram_bot_mock: TelebotMock,
    telegram_create_text_message: TelegramCreateTextMessage,
):
    user = DBUserFactory.create()
    telegram_command = telegram_create_text_message("/start", from_id=int(user.telegram_id))

    bot.process_update_dict(telegram_command)

    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0].chat_id == telegram_command["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0].text.startswith(
        "You are already authenticated.\n" + "How can I assist you today?"
    )
