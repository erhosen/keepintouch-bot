import datetime as dt

import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def mbot():
    class Bot:
        def __init__(self):
            self.args = []
            self.kwargs = {}
            self.defaults = None
            super().__init__()

        def send_message(self, *args, **kwargs):
            self.args.append(args)
            self.kwargs.update(kwargs)

        def edit_message_text(self, *args, **kwargs):
            self.args.append(args)
            self.kwargs.update(kwargs)

        @property
        def text(self):
            return self.kwargs.get('text')

        @property
        def reply_markup(self):
            return self.kwargs.get('reply_markup')

    return Bot()


@pytest.fixture
def start_command_json():
    return {
        "update_id": 999999999,
        "message": {
            "message_id": 999999999,
            "from": {
                "id": 999999999,
                "is_bot": False,
                "first_name": "John",
                "last_name": "Doe",
                "username": "jdoe",
                "language_code": "en-US",
            },
            "chat": {
                "id": 999999999,
                "first_name": "John",
                "last_name": "Doe",
                "username": "jdoe",
                "type": "private",
            },
            "date": 1546300800,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        },
    }


@pytest.fixture
def callback_keepintouch_json():
    return {
        "update_id": 999999999,
        "callback_query": {
            "id": 999999999,
            "from": {
                "id": 999999999,
                "is_bot": False,
                "first_name": "John",
                "last_name": "Doe",
                "username": "jdoe",
                "language_code": "en-US",
            },
            "message": {
                "message_id": 999999999,
                "from": {
                    "id": 999999999,
                    "is_bot": False,
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "jdoe",
                    "language_code": "en-US",
                },
                "chat": {
                    "id": 999999999,
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "jdoe",
                    "type": "private",
                },
                "date": 1546300800,
                "text": "",
                "entities": [],
            },
            "chat_instance": "999999999",
            "data": "KEEPINTOUCH:1:0",
            "game_short_name": None,
        },
    }


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
        DEBUG=True,
    )
