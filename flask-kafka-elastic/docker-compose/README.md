# Test Elasticsearch/Kibana/Kafka/Kafka Connect (docker)

## Pre-reqs
- Docker and `docker-compose`
- Kafka (version 0.10+) (only for local CLI tools), otherwise, `docker exec` can be used

## Using
1. `./start.sh`
2. Navigate to Management -> Saved Objects
3. Import `../kibana_exports/all.json` (re-associate index pattern to `shaw-*` if any conflicts arise)
4. Present demo

## Clean up
- `./clean.sh`