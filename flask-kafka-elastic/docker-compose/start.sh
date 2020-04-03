#!/usr/bin/env bash

set -e

export TOPIC='blimp-demo'
KIBANA_VERSION="$(grep ELASTIC_TAG .env | cut -d= -f2)"
KIBANA_URL='http://localhost:5601'

function create_index_mapping() {
  if [ "$#" -ne 1 ]; then
    echo "Missing topic parameter"
    exit 1;
  fi
  echo -e "\n\n==> Creating ElasticSearch Indicies..."
  ES_INDEX="${1}" ./sonic-es-mapping.sh
}

function create_index_pattern() {
  echo -e "\n\n==> Creating Kibana Index Pattern"
  sleep 3
  curl -w'\n' -X POST "${KIBANA_URL}/api/saved_objects/index-pattern" --compressed \
      -H "kbn-version: ${KIBANA_VERSION}" -H 'content-type: application/json' \
      -H "Referer: ${KIBANA_URL}/app/kibana" \
      --data '{"attributes":{"title":"sonic-*","timeFieldName":"event_time"}}'
}

function post_connector() {
  echo -e "\n\n==> Loading Kafka Connect Elasticsearch Sink"
  ./load-es-kafkaconnect.sh
  sleep 5
}

function open_kibana() {
  echo -e "\n\n==> TODO: Import kibana dashboards"
  sleep 5

  # Kafka Connect UI
  #open http://localhost:8003

  # Kibana
  open "${KIBANA_URL}/app/kibana#/discover?_g=(time:(from:now%2Fw,mode:quick,to:now%2Fw))&_a=(columns:!(_source),interval:auto,sort:!(event_time,desc))"
}

function load_data() {
  echo -e "\n\n==> Producing Data to Kafka topic='${TOPIC}'..."
  ## To show the data. Run this before the load script to see active consumption
  # docker-compose -p testkafkaelastickibana exec kafka bash -c "kafka-console-consumer --bootstrap-server localhost:9092 --topic shaw-products --from-beginning"
  # ./load-data.sh
  curl -v -X POST 'http://localhost:8080/generate?c=1000'

  # post_connector
  create_index_pattern
}

function demo_docker_compose() {
  docker-compose -p testkafkaelastickibana up -d
  echo "==> Waiting for services to start up..."
  sleep 45

  create_index_mapping $TOPIC

  echo -e "\n\n==> Creating Kafka Topics..."
  DOCKER_KAFKA_ZK_CHROOT='zookeeper:2181/kafka'
  docker-compose -p testkafkaelastickibana exec kafka bash -c \
  "kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_configs --replication-factor 1 --partitions 1 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_offsets --replication-factor 1 --partitions 10 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_status --replication-factor 1 --partitions 10 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic ${TOPIC} --replication-factor 1 --partitions 5"

  load_data

  open_kibana
}

function demo_blimp() {
  blimp up
  echo "==> Waiting for services to start up..."
  sleep 45

  create_index_mapping $TOPIC

  echo -e "\n\n==> Creating Kafka Topics..."
  DOCKER_KAFKA_ZK_CHROOT='zookeeper:2181/kafka'
  docker-compose -p testkafkaelastickibana exec kafka bash -c \
  "kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_configs --replication-factor 1 --partitions 1 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_offsets --replication-factor 1 --partitions 10 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic kafka-connect_status --replication-factor 1 --partitions 10 --config cleanup.policy=compact --disable-rack-aware \
    && kafka-topics --create --if-not-exists --zookeeper ${DOCKER_KAFKA_ZK_CHROOT} --topic ${TOPIC} --replication-factor 1 --partitions 5"

  load_data

  open_kibana
}


# function main() { 
demo_blimp
# }
