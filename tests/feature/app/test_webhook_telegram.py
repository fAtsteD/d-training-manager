from tests.fixtures.app import HttpApiTestClient
from tests.fixtures.telegram import TelebotMock, TelegramCreateCommand


def test_webhook_with_success_command(
    http_api_client: HttpApiTestClient,
    telegram_bot_mock: TelebotMock,
    telegram_create_command: TelegramCreateCommand,
):
    telegram_command = telegram_create_command("/start")
    response = http_api_client.post(
        path=f"/webhook/telegram",
        data=telegram_command,
    )
    assert response.status_code == 201
    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0]["chat_id"] == telegram_command["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0]["text"] == "Hello! I am your training manager bot."
