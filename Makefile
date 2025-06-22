build-DTrainingManagerFunction:
	uv export --frozen --no-dev --no-editable --no-hashes --no-annotate --no-header -o "$(ARTIFACTS_DIR)/requirements.txt" --no-progress --no-python-downloads
	uv pip install --no-build-isolation --target $(ARTIFACTS_DIR) -r "$(ARTIFACTS_DIR)/requirements.txt" --no-progress --no-python-downloads

check: lint check-types

check-types: pyright mypy

format:
	isort .
	black .

format-check: format check-types

init: install-app-dev install-hooks

install-app-dev:
	uv sync --locked --all-groups

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
