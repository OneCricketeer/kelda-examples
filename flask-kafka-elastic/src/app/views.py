import logging
from flask import render_template, request, Response

from app import app
from . import kafka_producer as producer
from .config import topic_name, bootstrap as kafka_bootstrap
from .gen.sonic_gen import generate as generate_sonic

kafka_buffer_limit = 100000  # TODO: check where this limit is set


def generate_data(instances=1, topic_name=None):
    '''
    record the event synchronously
    calling flush() guarantees that each event is written to Kafka before continuing
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


@app.route('/')
def index():
    args = request.args
    resp = render_template('index.j2', kafka_bootstrap=kafka_bootstrap)
    # count = args.get('c', 1)
    # say_hello(instances=int(count), topic_name=topic_name)
    return resp


@app.route('/generate', methods=['GET'])
def generate():
    args = request.args
    count = int(args.get('c', 1))
    generate_data(count, topic_name=topic_name)
    return Response('data sent', status=202)

# @app.route('/<username>')
# def hello(username):
#     args = request.args
#     resp = render_template('index.j2', username=username,
#                            kafka_bootstrap=kafka_bootstrap)
#     count = args.get('c', 1)
#     say_hello(username, instances=int(count), topic_name=topic_name)
#     return resp
