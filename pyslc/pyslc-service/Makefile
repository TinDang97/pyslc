
## Run the dev stack docker compose setup. This exposes DB and NLP services
## for local development. This does not start the Zep service.
dev:
	docker compose -f docker-compose.dev.yaml up db nlp

start:
	docker compose -f docker-compose.yaml up

detach:
	docker compose -f docker-compose.yaml up -d

## Docker:
docker-build: ## Use the dockerfile to build the container
	DOCKER_BUILDKIT=1 docker build --rm --tag $(BINARY_NAME) .

docker-release: ## Release the container with tag latest and version
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker tag $(BINARY_NAME) $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)
	# Push the docker images
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):latest
	docker push $(DOCKER_REGISTRY)$(BINARY_NAME):$(VERSION)
