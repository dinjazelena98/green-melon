.PHONY: format check typecheck lint test all clean help

help:
	@echo "Available commands:"
	@echo "  make format     - Format code with ruff"
	@echo "  make check      - Lint code with ruff and fix issues"
	@echo "  make ty         - Run type checking with ty"
	@echo "  make all        - Run format, check, and ty"
	@echo "  make clean      - Remove cache files"

format:
	ruff format green_melon

check:
	ruff check --fix green_melon

ty:
	ty check -v green_melon

# Run all checks
all: format check ty

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true