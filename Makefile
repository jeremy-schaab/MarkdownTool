.PHONY: help install install-dev test test-cov lint format clean build docs run

help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:		## Install production dependencies
	pip install -e .

install-dev:		## Install development dependencies
	pip install -e ".[dev,test]"
	pre-commit install

test:			## Run tests
	pytest

test-cov:		## Run tests with coverage
	pytest --cov=src/markdown_manager --cov-report=html --cov-report=term-missing

lint:			## Run linting
	flake8 src/ tests/
	mypy src/
	bandit -r src/

format:			## Format code
	black src/ tests/
	isort src/ tests/

format-check:		## Check code formatting
	black --check src/ tests/
	isort --check-only src/ tests/

clean:			## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:			## Build package
	python -m build

build-exe:		## Build Windows executable
	python scripts/build_exe.py

build-installer:	## Build professional Windows installer (requires Inno Setup)
	python scripts/build_installer.py

install-build:		## Install build dependencies
	pip install -e ".[build]"

docs:			## Generate documentation (placeholder)
	@echo "Documentation generation not implemented yet"

run:			## Run the application
	python -m markdown_manager.cli

run-dev:		## Run in development mode
	ENVIRONMENT=development python -m markdown_manager.cli

docker-build:		## Build Docker image
	docker build -t markdown-manager .

docker-run:		## Run Docker container
	docker run -p 8501:8501 markdown-manager

pre-commit:		## Run pre-commit hooks
	pre-commit run --all-files

security:		## Run security checks
	bandit -r src/
	safety check

all-checks:		## Run all quality checks
	make format-check
	make lint
	make test-cov
	make security