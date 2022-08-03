#!/usr/bin/env python
import json
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def handler(event, context):
    """
    Handle lambda call
    """
    # Prepare environment variables
    import dotenv

    dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.environ.setdefault('DATABASE_PASSWORD', context.token["access_token"])  # iam_token is database password`

    # Setup django
    import django

    django.setup()

    # Handle lambda call
    body = json.loads(event['body'])
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
