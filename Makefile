.PHONY: lint

lint:
	uv run ruff check --fix green_melon tests
	uv run ruff format green_melon tests
	uv run mypy green_melon tests

.PHONY: test

test:
	uv run pytest tests