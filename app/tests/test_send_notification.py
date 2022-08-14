from freezegun import freeze_time
from tgbot.handlers.notification import send_notification_message


@freeze_time('2022-08-01')
def test_send_notification_message(mbot, contact):
    send_notification_message(mbot, contact.user, contact)

    assert mbot.text == (
        "💬 It's time to write a few words to [Jane](https://t.me/+78888888888) \n\n"
        "Last time you contacted *21 days ago* (List A)\n"
    )
    assert mbot.reply_markup.inline_keyboard[0][0].text == 'Ok'
    assert mbot.reply_markup.inline_keyboard[0][1].text == 'Tomorrow'
    assert mbot.reply_markup.inline_keyboard[0][2].text == 'In a week'
    assert mbot.reply_markup.inline_keyboard[0][3].text == 'Demote'

    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'KEEPINTOUCH:1:0'
    assert mbot.reply_markup.inline_keyboard[0][1].callback_data == 'KEEPINTOUCH:1:1'
    assert mbot.reply_markup.inline_keyboard[0][2].callback_data == 'KEEPINTOUCH:1:7'
    assert mbot.reply_markup.inline_keyboard[0][3].callback_data == 'KEEPINTOUCH:1:-1'
