import json
import logging
import sys

import paho.mqtt.publish as mqtt_publish

import mqtt_config

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('messages')


def publish(topic, **payload):
    logger.info('publish topic=%s payload=%s', topic, payload)
    mqtt_publish.single(topic,
                        payload=json.dumps(payload),
                        qos=1,
                        retain=True,
                        hostname=mqtt_config.hostname,
                        auth=mqtt_config.auth,
                        port=mqtt_config.port,
                        client_id='')


def repl(topic):
    while True:
        try:
            message = input('> ')
        except EOFError:
            break
        publish(topic, message=message)


def main(topic='speak'):
    # logger.setLevel(logging.INFO)
    if not mqtt_config.hostname:
        print('At least one of these must be set:',
              ', '.join(mqtt_config.MQTT_ENV_VARS), file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) > 1:
        message = sys.argv[1]
        publish(topic, message=message)
    else:
        repl(topic)


if __name__ == '__main__':
    main()
