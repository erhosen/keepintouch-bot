"""
Django settings for keepintouch project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from typing import Dict, List

from pydantic import BaseSettings, Field
from pydjantic import BaseDBConfig, to_django

# Build paths inside the project like this: BASE_DIR / 'subdir'.
CUR_DIR = Path(__file__).resolve().parent
BASE_DIR = CUR_DIR.parent


class DatabaseSettings(BaseDBConfig):
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases
    default: str = Field(default="", env="DATABASE_URL")

    class Config:
        env_file = CUR_DIR / '.env'


class GeneralSettings(BaseSettings):
    # https://docs.djangoproject.com/en/dev/ref/settings/
    SECRET_KEY: str = Field(default="", env='DJANGO_SECRET_KEY')
    DEBUG: bool = Field(default=False, env='DEBUG')
    DATABASES = DatabaseSettings()

    ALLOWED_HOSTS: List[str] = ['*']
    ROOT_URLCONF = 'keepintouch.urls'
    WSGI_APPLICATION = 'keepintouch.wsgi.application'

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tgbot.apps.TgbotConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


class I18NSettings(BaseSettings):
    # https://docs.djangoproject.com/en/3.1/topics/i18n/
    LANGUAGE_CODE: str = 'en-us'
    TIME_ZONE: str = 'UTC'
    USE_I18N: bool = True
    USE_TZ: bool = True


class StaticSettings(BaseSettings):
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    STATIC_URL: str = '/static/'

    TEMPLATES: List[Dict] = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]


class LoggingSettings(BaseSettings):
    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING: Dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        # "loggers": {
        #     "django.db.backends": {
        #         "level": "DEBUG",
        #         "handlers": ["console"],
        #         "propagate": False,
        #     }
        # },
    }


class ProjectSettings(GeneralSettings, I18NSettings, StaticSettings, LoggingSettings):
    TELEGRAM_TOKEN: str
    TELEGRAM_LOGS_CHAT_ID: int

    class Config:
        env_file = CUR_DIR / '.env'


to_django(ProjectSettings())
