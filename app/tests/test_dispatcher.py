import pytest
from tgbot.dispatcher import Unauthenticated


def test_process_telegram_event_from_owner(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    process_telegram_event(telegram_message_update.to_dict())


def test_process_telegram_event_from_stranger(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    telegram_message_update.message.from_user.id = 7777777777
    with pytest.raises(Unauthenticated):
        process_telegram_event(telegram_message_update.to_dict())
