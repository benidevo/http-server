start:
	sh run.sh

format:
	pipenv run isort ./app
	pipenv run black ./app

lint: format
	pipenv run mypy ./app

install-dev:
	pipenv install --dev

.PHONY: start format lint install-dev
