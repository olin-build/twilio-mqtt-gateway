from unittest.mock import patch

from twilio_gateway import app

app.testing = True
client = app.test_client()


def test_home_page():
    assert client.get('/').status_code == 200


@patch('send_mqtt_messages.publish')
def test_webhook(publish):
    data = dict(
        To='+16175552323',
        From='+16175553434',
        Body='message body',
    )
    assert client.post('/sms_webhook', data=data).status_code == 200
    publish.assert_called_once_with('incoming-sms-16175552323',
                                    From='+16175553434',
                                    To='+16175552323',
                                    Body='message body')
