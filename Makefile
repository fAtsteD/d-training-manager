include .env

build-DTrainingManagerFunction:
	uv pip install --no-installer-metadata --no-compile-bytecode --python-platform x86_64-manylinux2014 --no-build-isolation --target $(ARTIFACTS_DIR) --no-progress --no-python-downloads --no-deps .

build-DTrainingManagerFunctionLayer:
	uv export --frozen --no-dev --no-editable --no-hashes --no-annotate --no-header --no-emit-project -o "$(ARTIFACTS_DIR)/requirements.txt" --no-progress --no-python-downloads
	uv pip install --no-installer-metadata --no-compile-bytecode --python-platform x86_64-manylinux2014 --no-build-isolation --target "$(ARTIFACTS_DIR)/python" -r "$(ARTIFACTS_DIR)/requirements.txt" --no-progress --no-python-downloads
	rm -f "$(ARTIFACTS_DIR)/requirements.txt"

check: lint check-types

check-types: pyright mypy

format:
	uv run isort .
	uv run black .

format-check: format check-types

init: install-app-dev install-hooks

install-app-dev:
	uv sync --locked --all-groups

install-hooks:
	cp hooks/* .git/hooks
	chmod +x .git/hooks/*

lint:
	uv run isort --check-only .
	uv run black --check .

mypy:
	uv run mypy src
	uv run mypy tests

pyright:
	uv run pyright src
	uv run pyright tests

sam-build-prod:
	sam build --parameter-overrides Stage=prod TelegramApiKey=$(TELEGRAM_API_TOKEN)

sam-build-dev:
	sam build --parameter-overrides Stage=dev TelegramApiKey=$(TELEGRAM_API_TOKEN) DdUrl=$(DB_URL)

sam-local-start: sam-build-dev
	docker-compose -f docker-compose.dev.yml up -d
	sam local start-api --parameter-overrides Stage=dev TelegramApiKey=$(TELEGRAM_API_TOKEN) DdUrl=$(DB_URL)

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=reporting
