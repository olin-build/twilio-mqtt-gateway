import logging
import os
import sys

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from send_mqtt_messages import publish

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')

HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
PORT = int(os.environ.get('PORT', 5000))
FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 'PORT' not in os.environ
RESPONSE_TEXT = os.environ.get('RESPONSE_TEXT')
GITHUB_URL = 'https://github.com/olinlibrary/bear-as-a-service'

app = Flask(__name__)


@app.route('/')
def home():
    return f'The server is running. <a href="{GITHUB_URL}">More…</a>'


@app.route('/sms_webhook', methods=['POST'])
def sms_webhook():
    topic = request.form['To'].replace('+', 'incoming-sms-')
    payload = request.form.to_dict(flat=True)
    logger.info('publish {} to {}'.format(payload, topic))
    publish(topic, **request.form)

    resp = MessagingResponse()
    if RESPONSE_TEXT:
        resp.message(RESPONSE_TEXT)
    return str(resp)

logger.setLevel(logging.INFO)
logger.info(f"Listening on http://{HOST}:{PORT} FLASK_DEBUG={FLASK_DEBUG}'")
app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
