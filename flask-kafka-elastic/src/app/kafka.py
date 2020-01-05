import os
from confluent_kafka import Producer


def get_kafka_producer():
    bootstrap = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    return Producer({'bootstrap.servers':bootstrap})
