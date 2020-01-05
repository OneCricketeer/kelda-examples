#!/usr/bin/env bash

set -e

docker-compose -p testkafkaelastickibana stop && docker-compose -p testkafkaelastickibana rm -f