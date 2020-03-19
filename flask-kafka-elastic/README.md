# Elastic/Kafka/Kibana (EKK) pipelines

*Getting started*

1. Converted `docker-compose` folder to using k8s with <https://kompose.io> 
2. Restructured services into workspaces for [`kelda`](https://kelda.io)
3. Created `data-gen` (Python) app

## TODO

Automate the following steps in k8s-land

1. `start.sh` HTTP calls
2. Navigate to Management -> Saved Objects
3. Import `../kibana_exports/all.json` (re-associate index pattern to `shaw-*` if any conflicts arise)
4. Open Kibana
5. Things from `clean.sh`
