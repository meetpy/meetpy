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

piptools:
	pip install pip --upgrade
	pip install pip-tools

deps: piptools
	pip-compile requirements/base.in -o requirements/base.txt --upgrade

deps-prod: piptools
	pip-compile requirements/base.in requirements/production.in -o requirements/production.txt --upgrade

install-dev: piptools
	pip-sync requirements/base.txt

install-production: piptools
	pip-sync requirements/production.txt

install: install-dev
