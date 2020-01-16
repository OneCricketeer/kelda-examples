import logging
from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions, ConfigResource, ConfigSource

def get_admin_client(bootstrap, conf={}):
    return AdminClient({'bootstrap.servers': bootstrap})


def get_kafka_producer(bootstrap, conf={}):
    return Producer({'bootstrap.servers': bootstrap})


def create_topic(admin, name, replicas=1, partitions=1, configs={}):
    new_topics = [NewTopic(name, num_partitions=partitions,
                           replication_factor=replicas)]
    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    fs = admin.create_topics(new_topics)

    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logging.info("Topic {} created".format(topic))
        except Exception as e:
            if isinstance(e, KafkaError):
                logging.debug(dir(e))
            logging.error("Failed to create topic {}: {}".format(topic, e))
