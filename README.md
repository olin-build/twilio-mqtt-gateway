# Twilio → MQTT Gateway
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

A web application that implements a Twilio callback to relay incoming SMS
messages to a MQTT server.

This allows a number of clients to subscribe to incoming SMS messages, without
each requiring a web presence.

For the original motivation, see the Olin Library
[Bear-as-a-Service](https://github.com/olinlibrary/bear-as-a-service) project.

Each number `+16175551212` is published with topic `incoming-sms-16175551212`,
and with a payload of the JSON-encoded HTTP request form fields.

## Configuration

`MQTT_URL`, `CLOUDMQTT_URL`, `CLOUDAMQP_URL` — if you're not using a local
RabbitMQ server, set one of these.

`RESPONSE_TEXT` — if set, respond to incoming messages with this text.

`HOST`, `PORT`, `FLASK_DEBUG` — what you'd expect.

## Development

Either set install a local RabbitMQ server, *or* set `MQTT_URL` to a remote
server.

Run `python twilio_gateway.py`.

Install [ngrok](https://ngrok.com). In another terminal, run
`ngrok http 5000`. This gives your local webserver a public hostname that you
can configure Twilio to connect to.

Provision a Twilio phone number, and direct it to your local instance.

1. Go to the Twilio phone number configuration page, e.g. <https://www.twilio.com/console/phone-numbers/{sid}>.
2. Under "Messaging: A Message Comes In", set the webhook to the server URL
   followed by the `/sms_webhook` path, e.g.
   `https://c115d7a2.ngrok.io/sms_webhook`.

The Jupyter notebook in this directory demonstrates how to do this
programmatically, and for a list of numbers.

### Installing a RabbitMQ server

For local development, you may find it useful to run a local RabbitMQ server.

macOS: `brew install rabbitmq` (and then follow the instructions to launch the
daemon, now and on restart).

Add `rabbitmqadmin` to your path. (On macOS: `export
PATH=/usr/local/Cellar/rabbitmq/3.7.2/sbin/:PATH`.) Alternatively, you can
replace `rabbitmqadmin` by `/path/to/rabbitmqadmin` in the instructions below.

Create a queue for your phone number, and bind it to the topic:

```bash
rabbitmqadmin declare queue name=incoming-sms-16175551010
rabbitmqadmin declare binding source=amq.topic destination_type=queue \
    destination=incoming-sms-16175551010 routing_key=incoming-sms-16175551010
```

The Jupyter notebook in this directory demonstrates how to do this
programmatically.

## Deployment

You will need a RabbitMQ server. I'm using
[CloudAMQP](https://www.cloudamqp.com). Set `CLOUDMQTT_URL` to its URL.

## License

MIT
