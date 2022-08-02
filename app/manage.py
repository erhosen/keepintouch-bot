#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keepintouch.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def _set_database_url(context):
    """
    Dark magic to set database url from lambda environment variables. Yandex.Cloud :|
    """
    dsn = os.environ["DATABASE_URL_PLACEHOLDER"]  # placeholder like `postgres://user:{iam_token}@host:port/db`
    iam_token = context.token["access_token"]  # surprise #2: iam_token inside lambda `context`
    db_url = dsn.format(iam_token=iam_token)
    os.environ.setdefault('DATABASE_URL', db_url)


def handler(event, context):
    """
    Handle lambda call
    """
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keepintouch.settings')
    _set_database_url(context)
    django.setup()

    body = json.loads(event['body'])  # type: ignore
    from tgbot.dispatcher import process_telegram_event

    process_telegram_event(body)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"ok": "POST request processed"}, ensure_ascii=False),
        'isBase64Encoded': False,
    }


if __name__ == '__main__':
    main()
