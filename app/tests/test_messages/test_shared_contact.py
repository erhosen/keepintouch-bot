import pytest
from telegram import Contact
from tgbot.core import KEEPINTOUCH_RULES
from tgbot.handlers import message_shared_contact


@pytest.fixture
def message_shared_contact_update(telegram_message_update, mbot):
    telegram_message_update.message.contact = Contact.de_json(
        {'phone_number': '+78888888888', 'first_name': 'Jane', 'user_id': 888888888}, mbot
    )
    return telegram_message_update


def test_message_shared_contact(mbot, message_shared_contact_update):
    message_shared_contact(message_shared_contact_update, {})

    assert mbot.text == f"What group do you want to add Jane to? \n\nThe rules are simple: \n{KEEPINTOUCH_RULES}"

    assert mbot.reply_markup.inline_keyboard[0][0].text == 'A'
    assert mbot.reply_markup.inline_keyboard[0][1].text == 'B'
    assert mbot.reply_markup.inline_keyboard[0][2].text == 'C'
    assert mbot.reply_markup.inline_keyboard[0][3].text == 'D'

    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'SET_GROUP:1:A'
    assert mbot.reply_markup.inline_keyboard[0][1].callback_data == 'SET_GROUP:1:B'
    assert mbot.reply_markup.inline_keyboard[0][2].callback_data == 'SET_GROUP:1:C'
    assert mbot.reply_markup.inline_keyboard[0][3].callback_data == 'SET_GROUP:1:D'
