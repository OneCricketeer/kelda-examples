#!/usr/bin/env bash

set -e

BOOTSTRAP=${BOOTSTRAP:-"localhost:29092"}
TOPIC=${TOPIC:-"test"}

python3 ../generateData-shaw.py 1000 |\
    kafka-console-producer --broker-list "${BOOTSTRAP}" --topic "${TOPIC}"
