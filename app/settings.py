import os

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
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}


INSTALLED_APPS = [
    'tgbot.apps.TgbotConfig',
    'django.contrib.contenttypes',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = False
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_ID = int(os.environ['TELEGRAM_ID'])
