import pytest
from tgbot.core import CallbackMarker
from tgbot.handlers.contacts import callback_delete_contact


def test_delete_contact(mbot, telegram_callback_update, contact):
    telegram_callback_update.callback_query.data = f'{CallbackMarker.DELETE_CONTACT}:1'
    callback_delete_contact(telegram_callback_update, {})

    assert mbot.text == "Jane was deleted"
    with pytest.raises(contact.DoesNotExist):
        contact.refresh_from_db()
