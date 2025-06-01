build-DTrainingManagerFunction:
	mkdir -p $(ARTIFACTS_DIR)/d_training_manager
	cd src/d_training_manager && find . -type f -name '*.py' -exec cp --parents {} $(ARTIFACTS_DIR)/d_training_manager \; && cd - > /dev/null
	cp requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r requirements.txt -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin

check: lint check-types

check-types: pyright mypy

format:
	isort .
	black .

format-check: format check-types

init: install-app-dev install-hooks

install-app-dev:
	pip install -e ".[dev]"

install-hooks:
	cp hooks/* .git/hooks
	chmod +x .git/hooks/*

lint:
	isort --check-only .
	black --check .

mypy:
	mypy src
	mypy tests

pyright:
	pyright src
	pyright tests

test:
	pytest

test-coverage:
	pytest --cov=reporting
