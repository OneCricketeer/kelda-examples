#!/usr/bin/env bash

set -xv

CONNECT_HOST=${CONNECT_HOST:-"http://localhost:8083"}

curl -X POST "${CONNECT_HOST}/connectors" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d@elastic-sink-connector.json