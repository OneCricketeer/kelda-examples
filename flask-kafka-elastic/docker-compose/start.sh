#!/usr/bin/env bash

set -e

export TOPIC='shaw-products'
KIBANA_VERSION=$(grep ELASTIC_TAG .env | cut -d= -f2)

function create_index_mapping() {
  if [ "$#" -ne 1 ]; then
    echo "Missing topic parameter"
    exit 1;
  fi
  echo -e "\n\n==> Creating ElasticSearch Indicies..."
  ES_INDEX="${1}" ./shaw-es-mapping.sh
}

function create_index_pattern() {
  echo -e "\n\n==> Creating Kibana Index Pattern"
  sleep 3
  curl -X POST 'http://localhost:5601/api/saved_objects/index-pattern' --compressed \
      -H "kbn-version: ${KIBANA_VERSION}" -H 'content-type: application/json' \
      -H 'Referer: http://localhost:5601/app/kibana' \
      --data '{"attributes":{"title":"shaw-*","timeFieldName":"event_time"}}'
}

function post_connector() {
  echo -e "\n\n==> Loading Kafka Connect Elasticsearch Sink"
  ./load-es-kafkaconnect.sh
  sleep 5
}

function finish() {
  echo -e "\n\n==> TODO: Import kibana dashboards"
  sleep 5

  # Kafka Connect UI
  open http://localhost:8003

  # Kibana
  open 'http://localhost:5601/app/kibana#/discover?_g=(time:(from:now%2Fw,mode:quick,to:now%2Fw))&_a=(columns:!(_source),interval:auto,sort:!(event_time,desc))'
}

function docker_compose() {
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

  post_connector

  echo -e "\n\n==> Producing Data to Kafka topic='${TOPIC}'..."
  ## To show the data. Run this before the load script to see active consumption
  # docker-compose -p testkafkaelastickibana exec kafka bash -c "kafka-console-consumer --bootstrap-server localhost:9092 --topic shaw-products --from-beginning"
  ./load-data.sh

  create_index_pattern

  finish
}

docker_compose
