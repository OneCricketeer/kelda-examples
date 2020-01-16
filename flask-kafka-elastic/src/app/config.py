import os

# Kafka bootstrap servers
bootstrap = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
# Topic name to use for Kafka
topic_name = os.getenv('KAFKA_TOPIC')
