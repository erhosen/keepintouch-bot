import datetime as dt

import pytest
from freezegun import freeze_time
from tgbot.core import Group
from tgbot.handlers.notification import callback_keepintouch


@freeze_time('2022-08-01')
def test_callback_keepintouch_ok(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = 'KEEPINTOUCH:1:0'
    callback_keepintouch(telegram_callback_update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 8, 1)
    assert mbot.text == 'Well done 👍\nNext notification will be in 21 days from now'


@freeze_time('2022-08-01')
def test_callback_keepintouch_tomorrow(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = 'KEEPINTOUCH:1:1'
    callback_keepintouch(telegram_callback_update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 7, 12)
    assert mbot.text == "I'll notify you again in a day 👌"


@freeze_time('2022-08-01')
def test_callback_keepintouch_in_a_week(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = 'KEEPINTOUCH:1:7'
    callback_keepintouch(telegram_callback_update, {})

    contact.refresh_from_db()
    assert contact.last_contact_date == dt.date(2022, 7, 18)
    assert mbot.text == "I'll notify you again in 7 days 👌"


@freeze_time('2022-08-01')
def test_callback_keepintouch_demote(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = 'KEEPINTOUCH:1:-1'
    callback_keepintouch(telegram_callback_update, {})

    contact.refresh_from_db()
    assert contact.group == Group.B
    assert contact.last_contact_date == dt.date(2022, 7, 11)
    assert mbot.text == (
        "Contact [Jane](https://t.me/+78888888888) was demoted to *group B*\n" "I'll notify you again in a month 👌"
    )


@freeze_time('2022-08-01')
def test_callback_keepintouch_final_demote(mbot, telegram_callback_update, contact):
    contact.group = Group.D
    contact.save()
    telegram_callback_update.callback_query.data = 'KEEPINTOUCH:1:-1'
    callback_keepintouch(telegram_callback_update, {})

    from tgbot.models import Contact

    with pytest.raises(Contact.DoesNotExist):
        contact.refresh_from_db()

    assert mbot.text == (
        "Contact [Jane](https://t.me/+78888888888) deleted.\nNo more notifications for this contact. 😢"
    )
