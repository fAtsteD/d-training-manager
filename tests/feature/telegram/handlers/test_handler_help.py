from d_training_manager.telegram import telegram_bot
from tests.fixtures.telegram import TelebotMock, TelegramCreateTextMessage


def test_help_message(
    telegram_bot_mock: TelebotMock,
    telegram_create_text_message: TelegramCreateTextMessage,
):
    telegram_command = telegram_create_text_message("/help")

    telegram_bot.process_update_dict(telegram_command)

    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0].chat_id == telegram_command["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0].text.startswith("I am your training manager bot.")
