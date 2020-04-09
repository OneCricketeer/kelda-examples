import logging
from .gen.sonic_gen import generate as generate_sonic

from . import kafka_producer as producer

kafka_buffer_limit = 100000  # TODO: check where this limit is set


def generate_data(instances=1, topic_name=None):
    '''
    Record the event synchronously.
    Calling flush() guarantees that each event is written to Kafka
    before continuing
    '''
    if not topic_name:
        logging.error('topic_name was not defined')
        return None

    logging.info('pre-flush producer')
    producer.flush()
    logging.debug(f'producing {instances} messages')
    _count = 0
    _limit_breach = 0
    peaks = [(2, 0.25, 1), (11, 1, 1), (19, 4, 2)]  # , (18, 3, 2)
    try:
        # for _ in range(instances):
        for payload in generate_sonic(instances, peaks):
            producer.produce(topic_name, payload)
            _count += 1
            if _count >= kafka_buffer_limit:
                logging.info('flushing producer on full buffer')
                producer.flush()
                _count = 0
                _limit_breach += 1
    except BufferError as e:
        logging.error('flushing producer on buffer error', e)
        producer.flush()

    logging.info('post-flush producer')
    producer.flush()
    logging.debug(f'sent {(_limit_breach * kafka_buffer_limit) + _count} messages')