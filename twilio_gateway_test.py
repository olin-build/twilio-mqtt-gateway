import flask
import os
import sys

from unittest.mock import MagicMock, patch
from twilio_gateway import app
from flask import url_for

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
    # FIXME the app should flatten these
    assert publish.called_once_with('incoming-sms-16175552323',
                                    From=['+16175553434'],
                                    To=['+16175553434'],
                                    Body=['message body'])
