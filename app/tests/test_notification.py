from tgbot.handlers.notification import _send_notification_message
from tgbot.models import Contact, User


def test_send_notification_message(mbot):
    user = User.objects.create(user_id=999999999, first_name='John')
    contact = Contact.objects.create(user=user, phone_number='+78888888888', first_name='Jane')
    _send_notification_message(mbot, user, contact)

    assert mbot.text == (
        "💬 It's time to write a few words to [Jane](https://t.me/+78888888888) \n\n"
        "Last time you contacted *now* (List C)\n"
    )
    assert mbot.reply_markup.inline_keyboard[0][0].text == 'Ok'
    assert mbot.reply_markup.inline_keyboard[0][1].text == 'Tomorrow'
    assert mbot.reply_markup.inline_keyboard[0][2].text == 'In a week'
    assert mbot.reply_markup.inline_keyboard[0][3].text == 'Demote'

    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'KEEPINTOUCH:1:0'
    assert mbot.reply_markup.inline_keyboard[0][1].callback_data == 'KEEPINTOUCH:1:1'
    assert mbot.reply_markup.inline_keyboard[0][2].callback_data == 'KEEPINTOUCH:1:7'
    assert mbot.reply_markup.inline_keyboard[0][3].callback_data == 'KEEPINTOUCH:1:-1'
