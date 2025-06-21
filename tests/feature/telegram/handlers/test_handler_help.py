import pytest

from d_training_manager.telegram import bot
from tests.fixtures.telegram import TelebotMock, TelegramCreateCommand


@pytest.mark.parametrize(
    "command",
    [
        "/start",
        "/help",
    ],
    ids=[
        "command start",
        "command help",
    ],
)
def test_webhook_with_success_command(
    command: str,
    telegram_bot_mock: TelebotMock,
    telegram_create_command: TelegramCreateCommand,
):
    telegram_command = telegram_create_command(command)

    bot.process_update_dict(telegram_command)

    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0]["chat_id"] == telegram_command["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0]["text"] == "Hello! I am your training manager bot."
