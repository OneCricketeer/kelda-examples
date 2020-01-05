from app import app
from .kafka import get_kafka_producer
from flask import render_template

# Create a Kafka Producer
producer=get_kafka_producer()


# print a nice greeting.
def say_hello(username = "World"):
    '''
    record the event synchronously
    calling flush() guarantees that each event is written to Kafka before continuing
    '''
    producer.produce('webapp', username + ', says-hello')
    producer.flush()


@app.route('/')
def index():
  t = render_template('index.j2')
  say_hello()
  return t


@app.route('/<username>')
def hello(username):
  t = render_template('index.j2', username=username)
  say_hello(username)
  return t
