.PHONY: lint

lint:
	uv run ruff check --fix green_melon
	uv run ruff format green_melon
	uv run mypy green_melon