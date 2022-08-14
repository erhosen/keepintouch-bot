import datetime as dt

import pytest
from django.conf import settings
from telegram import Update


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


def pytest_configure():
    settings.configure(
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'tgbot.apps.TgbotConfig',
            'django.contrib.contenttypes',
            'django.contrib.messages',
        ],
        TELEGRAM_TOKEN='123456789:AABBCCDDEEFFgghhiiijjkkllmmnnoopp',
        TELEGRAM_ID=999999999,
        DEBUG=True,
    )


@pytest.fixture
def mbot():
    class Bot:
        def __init__(self):
            self.kwargs = {}
            self.defaults = None
            super().__init__()

        def send_message(self, *args, **kwargs):
            self.kwargs.update(kwargs)

        def edit_message_text(self, *args, **kwargs):
            self.kwargs.update(kwargs)

        def send_photo(self, *args, **kwargs):
            self.kwargs.update(kwargs)

        def set_my_commands(self, *args, **kwargs):
            self.kwargs.update(kwargs)

        def delete_my_commands(self, *args, **kwargs):
            pass

        @property
        def text(self):
            return self.kwargs.get('text')

        @property
        def reply_markup(self):
            return self.kwargs.get('reply_markup')

        @property
        def caption(self):
            return self.kwargs.get('caption')

        @property
        def photo(self):
            return self.kwargs.get('photo')

        @property
        def chat_id(self):
            return self.kwargs.get('chat_id')

        @property
        def commands(self):
            return self.kwargs.get('commands')

    return Bot()


@pytest.fixture
def telegram_message_update(mbot):
    return Update.de_json(
        {
            'update_id': 999999999,
            'message': {
                'message_id': 999999999,
                'from': {
                    'id': 999999999,
                    "is_bot": False,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'username': 'jdoe',
                    "language_code": "en-US",
                },
                'chat': {
                    'id': 999999999,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'username': 'jdoe',
                    "type": "private",
                },
                'date': dt.datetime.now().timestamp(),
                'text': 'text',
            },
        },
        mbot,
    )


@pytest.fixture
def telegram_callback_update(telegram_message_update, mbot):
    return Update.de_json(
        {
            'update_id': 999999999,
            'callback_query': {
                'id': 999999999,
                'from': telegram_message_update.message.from_user.to_dict(),
                'message': telegram_message_update.message.to_dict(),
                'chat_instance': '999999999',
                'data': 'data',
            },
        },
        mbot,
    )


@pytest.fixture
def user():
    from tgbot.models import User

    return User.objects.create(user_id=999999999, first_name='John')


@pytest.fixture
def contact(user):
    from tgbot.core import GROUP_POLICY, Group
    from tgbot.models import Contact

    return Contact.objects.create(
        user=user,
        phone_number='+78888888888',
        first_name='Jane',
        group=Group.A,
        last_contact_date=dt.date(2022, 8, 1) - GROUP_POLICY[Group.A],
    )
