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
	pip-compile requirements.in -o requirements.txt --upgrade
	pip-compile requirements-pg.in -o requirements-pg.txt --upgrade

install: piptools
	pip-sync requirements.txt

check check/lint: check/lint/black check/lint/isort check/lint/ruff  ## Run all checks.

check/lint/black:  ## Run black lint check.
	black --check --diff .

check/lint/ruff:  ## Run flake8 lint check.
	ruff check .
	
check/lint/isort:  ## Run isort lint check.
	isort --check --diff .

format: format/black format/isort  ## autoformat source files.

format/black:  ### autoformat source files using black only.
	black .

format/isort:  ## autoformat source files using isort only.
	isort .  '
