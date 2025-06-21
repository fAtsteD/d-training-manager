import datetime
from typing import Optional, Protocol, TypedDict, Union

import faker
import pytest
import telebot

from d_training_manager import config
from d_training_manager.telegram import bot


class TelebotMock(telebot.TeleBot):
    def __init__(self, faker: faker.Faker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = faker
        self.send_messages: list["TelebotSendMessageDict"] = []

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[telebot.types.MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
        timeout: Optional[int] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional[telebot.types.ReplyParameters] = None,
        link_preview_options: Optional[telebot.types.LinkPreviewOptions] = None,
        business_connection_id: Optional[str] = None,
        message_effect_id: Optional[str] = None,
        allow_paid_broadcast: Optional[bool] = None,
    ) -> telebot.types.Message:
        self.send_messages.append(
            {
                "chat_id": chat_id,
                "text": text,
            }
        )
        return telebot.types.Message.de_json(
            {
                "message_id": self.faker.random_int(min=1, max=1000000),
                "from": {
                    "id": self.faker.random_int(min=1, max=1000000),
                    "is_bot": True,
                    "first_name": self.faker.first_name(),
                    "username": self.faker.user_name(),
                },
                "chat": {
                    "id": chat_id,
                    "first_name": self.faker.first_name(),
                    "last_name": self.faker.first_name(),
                    "username": self.faker.user_name(),
                    "type": "private",
                },
                "date": int(datetime.datetime.now().timestamp()),
            }
        )


class TelebotSendMessageDict(TypedDict):
    chat_id: Union[int, str]
    text: str


class TelegramCreateCommand(Protocol):
    def __call__(self, command: str) -> dict:
        """Create a Telegram command message."""
        ...


@pytest.fixture(autouse=True)
def telegram_bot_mock(
    faker: faker.Faker,
    monkeypatch: pytest.MonkeyPatch,
) -> TelebotMock:
    telebot_mock = TelebotMock(
        faker=faker,
        threaded=False,
        token=config.telegram.api_token,
    )
    bot.register_handlers(telebot_mock)
    monkeypatch.setattr(
        bot,
        "create_bot",
        lambda: telebot_mock,
    )
    return telebot_mock


@pytest.fixture
def telegram_create_command(faker: faker.Faker) -> TelegramCreateCommand:
    def create_command(command: str) -> dict:
        return {
            "update_id": faker.random_int(min=1, max=1000000),
            "message": {
                "message_id": faker.random_int(min=1, max=1000000),
                "from": {
                    "id": faker.random_int(min=1, max=1000000),
                    "is_bot": False,
                    "first_name": faker.first_name(),
                    "last_name": faker.last_name(),
                    "username": faker.user_name(),
                    "language_code": "en",
                },
                "chat": {
                    "id": faker.random_int(min=1, max=1000000),
                    "first_name": faker.first_name(),
                    "last_name": faker.last_name(),
                    "username": faker.user_name(),
                    "type": "private",
                },
                "date": int(datetime.datetime.now().timestamp()),
                "text": command,
            },
        }

    return create_command
