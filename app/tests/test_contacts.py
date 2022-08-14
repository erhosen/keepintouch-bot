import pytest
from telegram import Update
from tgbot.core import KEEPINTOUCH_RULES, SHARE_CONTACT_TUTOR_IMG, Group
from tgbot.handlers import callback_set_group, command_add_contact, command_list, message_shared_contact


def test_command_add_contact(mbot, add_contact_command_json):
    update = Update.de_json(add_contact_command_json, mbot)
    command_add_contact(update, {})

    assert mbot.caption == 'Share your contact with me\n\nBTW, you can do it without /add_contact'
    assert mbot.photo == SHARE_CONTACT_TUTOR_IMG


def test_message_shared_contact(mbot, message_shared_contact_json):
    update = Update.de_json(message_shared_contact_json, mbot)
    message_shared_contact(update, {})

    assert mbot.text == f"What group do you want to add Jane to? \n\nThe rules are simple: \n{KEEPINTOUCH_RULES}"

    assert mbot.reply_markup.inline_keyboard[0][0].text == 'A'
    assert mbot.reply_markup.inline_keyboard[0][1].text == 'B'
    assert mbot.reply_markup.inline_keyboard[0][2].text == 'C'
    assert mbot.reply_markup.inline_keyboard[0][3].text == 'D'

    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'SET_GROUP:1:A'
    assert mbot.reply_markup.inline_keyboard[0][1].callback_data == 'SET_GROUP:1:B'
    assert mbot.reply_markup.inline_keyboard[0][2].callback_data == 'SET_GROUP:1:C'
    assert mbot.reply_markup.inline_keyboard[0][3].callback_data == 'SET_GROUP:1:D'


@pytest.mark.parametrize('group', [Group.A, Group.B, Group.C, Group.D])
def test_callback_set_group(mbot, callback_set_group_json, contact, group):
    callback_set_group_json['callback_query']['data'] = f'SET_GROUP:1:{group}'
    update = Update.de_json(callback_set_group_json, mbot)
    callback_set_group(update, {})

    assert mbot.text == f"Jane is now in {group} list"
    contact.refresh_from_db()
    assert contact.group == group


def test_command_list(mbot, command_list_json, contact):
    update = Update.de_json(command_list_json, mbot)
    command_list(update, {})

    assert mbot.text == (
        'Here are your contacts:\n\n'
        '*List A:*\n'
        '[Jane](https://t.me/+78888888888) | 13 days\n\n'
        '*List B:*\n\n'
        '*List C:*\n\n'
        '*List D:*\n\n'
    )
