#!/usr/bin/env bash

set -xv
set -e

ES_ADDR=${ES_ADDR:-"localhost:9200"}
ES_INDEX=${ES_INDEX:-"shaw-products"}

curl -v -XDELETE "http://${ES_ADDR}/${ES_INDEX}"
curl -XPUT "http://${ES_ADDR}/${ES_INDEX}" -H 'Content-Type: application/json' -d'
{
  "mappings": {
    "_doc": {
      "properties": {
        "event_time":  { "type": "date"    },
        "product":     { "type": "keyword" },
        "warehouseId": { "type": "keyword" },
        "city":        { "type": "text"    },
        "cost":        { "type": "float"   },
        "location":    { "type": "geo_point" }
      }
    }
  }
}'
