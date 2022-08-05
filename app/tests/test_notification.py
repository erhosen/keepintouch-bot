import datetime as dt

import pytest
from freezegun import freeze_time
from telegram import Update
from tgbot.core import Group
from tgbot.handlers.notification import callback_keepintouch, send_notification_message


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


@freeze_time('2022-08-01')
def test_callback_keepintouch_ok(mbot, callback_keepintouch_json, contact):
    callback_keepintouch_json['callback_query']['data'] = 'KEEPINTOUCH:1:0'
    update = Update.de_json(callback_keepintouch_json, mbot)
    callback_keepintouch(update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 8, 1)
    assert mbot.text == 'Well done 👍\nNext notification will be in 21 days from now'


@freeze_time('2022-08-01')
def test_callback_keepintouch_tomorrow(mbot, callback_keepintouch_json, contact):
    callback_keepintouch_json['callback_query']['data'] = 'KEEPINTOUCH:1:1'
    update = Update.de_json(callback_keepintouch_json, mbot)
    callback_keepintouch(update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 7, 12)
    assert mbot.text == "I'll notify you again in a day 👌"


@freeze_time('2022-08-01')
def test_callback_keepintouch_in_a_week(mbot, callback_keepintouch_json, contact):
    callback_keepintouch_json['callback_query']['data'] = 'KEEPINTOUCH:1:7'
    update = Update.de_json(callback_keepintouch_json, mbot)
    callback_keepintouch(update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 7, 18)
    assert mbot.text == "I'll notify you again in 7 days 👌"


@freeze_time('2022-08-01')
def test_callback_keepintouch_demote(mbot, callback_keepintouch_json, contact):
    callback_keepintouch_json['callback_query']['data'] = 'KEEPINTOUCH:1:-1'
    update = Update.de_json(callback_keepintouch_json, mbot)
    callback_keepintouch(update, {})

    contact.refresh_from_db()
    assert contact.group == Group.B
    assert contact.last_contact_date == dt.date(2022, 7, 11)
    assert mbot.text == (
        "Contact [Jane](https://t.me/+78888888888) was demoted to *group B*\n" "I'll notify you again in a month 👌"
    )


@freeze_time('2022-08-01')
def test_callback_keepintouch_final_demote(mbot, callback_keepintouch_json, contact):
    contact.group = Group.D
    contact.save()
    callback_keepintouch_json['callback_query']['data'] = 'KEEPINTOUCH:1:-1'
    update = Update.de_json(callback_keepintouch_json, mbot)
    callback_keepintouch(update, {})

    from tgbot.models import Contact

    with pytest.raises(Contact.DoesNotExist):
        contact.refresh_from_db()

    assert mbot.text == (
        "Contact [Jane](https://t.me/+78888888888) deleted.\nNo more notifications for this contact. 😢"
    )
