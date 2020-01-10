TAG?=kelda-starter-flask-kafka
REPO?=cricketeerone
VERSION?=$(shell cat version.txt)

HOST_HTTP_PORT?=8080

GUNICORN_CMD_ARGS?="pserve --reload"

build-docker:
	docker build -t $(REPO)/$(TAG):$(VERSION) .

push-docker: build-docker
	docker push $(REPO)/$(TAG):$(VERSION)

clean-docker:
	docker rmi $(REPO)/$(TAG):$(VERSION)

run-docker:
	docker run --rm -ti \
    -p $(HOST_HTTP_PORT):80 \
    $(REPO)/$(TAG):$(VERSION)

run-docker-dev:
	docker run --rm -ti \
		-e GUNICORN_CMD_ARGS="$(GUNICORN_CMD_ARGS)" \
    -v $(PWD)/app:/app/app:ro \
    -p $(HOST_HTTP_PORT):80 \
    $(REPO)/$(TAG):$(VERSION)
