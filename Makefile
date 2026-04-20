.PHONY: dev story lint fix

dev:
	uv run textual run --dev src/tusb/__main__.py

story:
	uv run textual run src/tusb/storybook/__main__.py

lint:
	uv run ruff check src/

fix:
	uv run ruff check src/ --fix