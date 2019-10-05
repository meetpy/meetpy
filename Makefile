.PHONY: docker-build \
	docker-login \
	docker-push

TAG = latest

docker-build:
	@docker build . -t pykonik/meetpy:$(TAG)

docker-login:
	@echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USER --password-stdin

docker-push: docker-login
	@docker push pykonik/meetpy:$(TAG)
