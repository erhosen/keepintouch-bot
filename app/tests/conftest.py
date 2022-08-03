import pytest
from django.conf import settings


class YCContext:
    def __init__(self):
        self.token = {"access_token": "CggVAgAAABoBMRKABHGgpZ......", "expires_in": 42299, "token_type": "Bearer"}


@pytest.fixture
def yc_context():
    return YCContext()


def pytest_configure():
    settings.configure(
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'INSTALLED_APPS': [
                    'django.contrib.contenttypes',
                    'django.contrib.messages',
                    'tgbot.apps.TgbotConfig',
                ],
            }
        },
        DEBUG=True,
    )
