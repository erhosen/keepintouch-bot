import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
CUR_DIR = Path(__file__).resolve().parent
BASE_DIR = CUR_DIR.parent

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'tgbot.apps.TgbotConfig',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = False
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_LOGS_CHAT_ID = os.environ['TELEGRAM_LOGS_CHAT_ID']
