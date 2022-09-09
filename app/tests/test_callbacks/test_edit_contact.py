from tgbot.core import CallbackMarker
from tgbot.handlers.contacts import callback_edit_contact


def test_callback_edit_contact(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = f'{CallbackMarker.EDIT_CONTACT}:1'
    callback_edit_contact(telegram_callback_update, {})

    assert mbot.text == '*List A* | [Jane](https://t.me/+78888888888) | a month'

    assert mbot.reply_markup.inline_keyboard[0][0].text == 'A'
    assert mbot.reply_markup.inline_keyboard[0][1].text == 'B'
    assert mbot.reply_markup.inline_keyboard[0][2].text == 'C'
    assert mbot.reply_markup.inline_keyboard[0][3].text == 'D'

    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'SET_GROUP:1:A'
    assert mbot.reply_markup.inline_keyboard[0][1].callback_data == 'SET_GROUP:1:B'
    assert mbot.reply_markup.inline_keyboard[0][2].callback_data == 'SET_GROUP:1:C'
    assert mbot.reply_markup.inline_keyboard[0][3].callback_data == 'SET_GROUP:1:D'
