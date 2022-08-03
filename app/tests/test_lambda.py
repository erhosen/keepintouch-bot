import json
import re

from manage import handler


def test_handler(yc_context):
    event = {
        'body': json.dumps(
            {
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
                    "text": "Hello, World!",
                },
            }
        )
    }
    response = handler(event, yc_context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"ok": "POST request processed"}'


def test_start_command(requests_mock, yc_context):
    tgapi_mock = requests_mock.post(
        re.compile(r'https://api.telegram.org/bot'),
        json={'ok': True},
    )

    event = {
        'body': json.dumps(
            {
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
        )
    }
    response = handler(event, yc_context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"ok": "POST request processed"}'

    assert tgapi_mock.called
    assert tgapi_mock.call_count == 1
