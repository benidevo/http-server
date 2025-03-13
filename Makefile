start:
	sh run.sh

test:
	codecrafters test

format:
	pipenv run isort ./app
	pipenv run black ./app

lint: format
	pipenv run mypy ./app

install-dev:
	pipenv install --dev

.PHONY: start test format lint install-dev
