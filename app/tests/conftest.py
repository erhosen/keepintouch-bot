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
