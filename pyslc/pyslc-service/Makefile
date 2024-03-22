
## Run the dev stack docker compose setup. This exposes DB and NLP services
## for local development. This does not start the Zep service.
dev:
	docker compose -f docker-compose.yaml up -d --build
	poetry install
	poetry run alembic upgrade head
	poetry run uvicorn app.api.v1.app:app --host 0.0.0.0 --port 8888 --reload

start:
	docker compose -f docker-compose.yaml up --build

detach:
	docker compose -f docker-compose.yaml up -d --build

## Docker:
docker-build: ## Use the dockerfile to build the container
	docker compose -f docker-compose.yaml build

docker-release: ## Release the container with tag latest and version
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)
	# Push the docker images
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)
