from faker import Faker

from d_training_manager.telegram import bot
from tests.fixtures.telegram import TelebotMock, TelegramCreateContactMessage


def test_contact_registered_successfully(
    faker: Faker,
    telegram_bot_mock: TelebotMock,
    telegram_create_contact_message: TelegramCreateContactMessage,
):
    user_telegram_id = faker.random_int(min=1, max=1000000)
    user_first_name = faker.first_name()
    user_last_name = faker.last_name()
    user_phone_number = faker.phone_number()
    telegram_user_contact = telegram_create_contact_message(
        from_id=user_telegram_id,
        user_first_name=user_first_name,
        user_last_name=user_last_name,
        user_phone_number=user_phone_number,
    )

    bot.process_update_dict(telegram_user_contact)

    assert len(telegram_bot_mock.send_messages) == 1
    assert telegram_bot_mock.send_messages[0].chat_id == telegram_user_contact["message"]["chat"]["id"]
    assert telegram_bot_mock.send_messages[0].text.startswith(
        "You have been successfully authenticated.\n",
    )
