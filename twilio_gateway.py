import logging
import os
import sys

from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse

import send_mqtt_messages


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')

HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
PORT = int(os.environ.get('PORT', 5000))
FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 'PORT' not in os.environ
RESPONSE_TEXT = os.environ.get('RESPONSE_TEXT')
GITHUB_README_URL = 'https://github.com/olin-build/twilio-mqtt-gateway#README'

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', readme_url=GITHUB_README_URL)


@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    topic = request.form['To'].replace('+', 'incoming-sms-')
    payload = request.form.to_dict(flat=True)
    logger.info('publish {} to {}'.format(payload, topic))
    send_mqtt_messages.publish(topic, **request.form)

    resp = MessagingResponse()
    if RESPONSE_TEXT:
        resp.message(RESPONSE_TEXT)
    return str(resp)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.info(f"Listening on http://{HOST}:{PORT} FLASK_DEBUG={FLASK_DEBUG}'")
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
