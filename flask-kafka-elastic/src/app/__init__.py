import logging, os
logging.basicConfig(level=logging.DEBUG)

from app import kafka, config
from flask import Flask, send_from_directory


# Create a app-wide Kafka Producer and AdminClient
kafka_producer = kafka.get_kafka_producer(config.bootstrap)
kafka_admin = kafka.get_admin_client(config.bootstrap)

if config.topic_name:
    logging.debug('creating kafka topic {}'.format(config.topic_name))
    kafka.create_topic(kafka_admin, config.topic_name, partitions=5)

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

from app import views