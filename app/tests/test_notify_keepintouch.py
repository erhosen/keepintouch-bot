import datetime as dt

from freezegun import freeze_time
from tgbot.handlers.notification import run_notify_keepintouch


def test_no_contacts(mbot):
    stats = run_notify_keepintouch(mbot)

    assert stats['total'] == 0
    assert stats['sent'] == 0


@freeze_time('2022-08-01')
def test_not_ready_yet(mbot, contact):
    contact.last_contact_date = dt.date(2022, 8, 1)
    contact.save()

    stats = run_notify_keepintouch(mbot)

    assert stats['total'] == 1
    assert stats['sent'] == 0


@freeze_time('2022-08-01')
def test_notification_sent(mbot, contact):
    contact.last_contact_date = dt.date(2022, 7, 11)
    contact.save()

    stats = run_notify_keepintouch(mbot)

    assert stats['total'] == 1
    assert stats['sent'] == 1

    contact.refresh_from_db()

    assert contact.last_contact_date == dt.date(2022, 8, 1)

    assert mbot.text == (
        "💬 It's time to write a few words to [Jane](https://t.me/+78888888888) \n\n"
        "Last time you contacted *21 days ago* (List A)\n"
    )
