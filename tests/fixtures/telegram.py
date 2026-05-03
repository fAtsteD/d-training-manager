import datetime
from dataclasses import dataclass
from typing import Optional, Protocol, Union

import pytest
from faker import Faker
from telebot import REPLY_MARKUP_TYPES, TeleBot
from telebot.types import LinkPreviewOptions, Message, MessageEntity, ReplyParameters

from d_training_manager import config
from d_training_manager.telegram import telegram_bot


class TelebotMock(TeleBot):
    def __init__(self, faker: Faker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = faker
        self.send_messages: list["TelebotSendMessageDict"] = []

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[list[MessageEntity]] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[REPLY_MARKUP_TYPES] = None,
        timeout: Optional[int] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        business_connection_id: Optional[str] = None,
        message_effect_id: Optional[str] = None,
        allow_paid_broadcast: Optional[bool] = None,
    ) -> Message:
        self.send_messages.append(
            TelebotSendMessageDict(
                chat_id=chat_id,
                reply_markup=reply_markup,
                text=text,
            )
        )
        return Message.de_json(
            {
                "chat": {
                    "id": chat_id,
                    "first_name": self.faker.first_name(),
                    "last_name": self.faker.first_name(),
                    "username": self.faker.user_name(),
                    "type": "private",
                },
                "date": int(datetime.datetime.now().timestamp()),
                "from": {
                    "id": self.faker.random_int(min=1, max=1000000),
                    "is_bot": True,
                    "first_name": self.faker.first_name(),
                    "username": self.faker.user_name(),
                },
                "message_id": self.faker.random_int(min=1, max=1000000),
            }
        )


@dataclass
class TelebotSendMessageDict:
    chat_id: Union[int, str]
    reply_markup: Optional[REPLY_MARKUP_TYPES]
    text: str


class TelegramCreateTextMessage(Protocol):

    def __call__(self, text: str, from_id: Optional[int] = None) -> dict:
        """Create a Telegram text message."""
        ...


class TelegramCreateContactMessage(Protocol):

    def __call__(self, from_id: int, user_first_name: str, user_last_name: str, user_phone_number: str) -> dict:
        """Create a Telegram contact content message."""
        ...


@pytest.fixture(autouse=True)
def telegram_bot_mock(
    faker: Faker,
    monkeypatch: pytest.MonkeyPatch,
) -> TelebotMock:
    telebot_mock = TelebotMock(
        faker=faker,
        threaded=False,
        token=config.telegram.api_token,
        use_class_middlewares=True,
    )
    telegram_bot.initialize_bot(telebot_mock)
    monkeypatch.setattr(
        telegram_bot,
        "create_bot",
        lambda: telebot_mock,
    )
    return telebot_mock


@pytest.fixture
def telegram_create_text_message(faker: Faker) -> TelegramCreateTextMessage:

    def create_text_message(text: str, from_id: Optional[int] = None) -> dict:
        from_id = from_id or faker.random_int(min=1, max=1000000)
        user_first_name = faker.first_name()
        user_last_name = faker.last_name()
        user_username = faker.user_name()
        return {
            "message": {
                "chat": {
                    "id": faker.random_int(min=1, max=1000000),
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "username": user_username,
                    "type": "private",
                },
                "date": int(datetime.datetime.now().timestamp()),
                "from": {
                    "id": from_id,
                    "is_bot": False,
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "username": user_username,
                    "language_code": "en",
                },
                "message_id": faker.random_int(min=1, max=1000000),
                "text": text,
            },
            "update_id": faker.random_int(min=1, max=1000000),
        }

    return create_text_message


@pytest.fixture
def telegram_create_contact_message(faker: Faker) -> TelegramCreateContactMessage:

    def create_contact_message(from_id: int, user_first_name: str, user_last_name: str, user_phone_number: str) -> dict:
        from_id = from_id or faker.random_int(min=1, max=1000000)
        user_username = faker.user_name()
        return {
            "message": {
                "chat": {
                    "id": faker.random_int(min=1, max=1000000),
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "username": user_username,
                    "type": "private",
                },
                "contact": {
                    "phone_number": user_phone_number,
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "user_id": from_id,
                },
                "date": int(datetime.datetime.now().timestamp()),
                "from": {
                    "id": from_id,
                    "is_bot": False,
                    "first_name": user_first_name,
                    "last_name": user_last_name,
                    "username": user_username,
                    "language_code": "en",
                },
                "message_id": faker.random_int(min=1, max=1000000),
            },
            "update_id": faker.random_int(min=1, max=1000000),
        }

    return create_contact_message
