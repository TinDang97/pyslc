BINARY_NAME=pyslc-service
DOCKER_REGISTRY=ghcr.io/pyslc-service
VERSION=0.1.0

## Run the dev stack docker compose setup. This exposes DB and NLP services
## for local development. This does not start the Zep service.
dev: build service
	poetry install
	poetry run alembic upgrade head
	poetry run uvicorn app.api.v1.app:app --host 0.0.0.0 --port 8888 --reload

## Run the dev stack docker compose setup. This exposes DB and NLP services
start: init
	poetry run uvicorn app.api.v1.app:app --host

service: build
	docker compose -f docker-compose.yaml up -d db zep

down:
	docker compose -f docker-compose.yaml down

init: build service
	poetry install
	poetry run alembic upgrade head

build: ## Use the dockerfile to build the container
	docker compose -f docker-compose.yaml build db zep

release: ## Release the container with tag latest and version
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)
	# Push the docker images
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)

clean: down ## Clean up the docker containers
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .coverage

clean_all: clean
	docker compose -f docker-compose.yaml down --volumes --remove-orphans
