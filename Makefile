# ==============================================================================
# Makefile for Project Chimera
#
# Provides reproducible commands for detailed setup, testing, and specification checks
# using the Dockerized environment.
# ==============================================================================

IMAGE_NAME := chimera-dev
# Detect OS for path handling if necessary, but $(CURDIR) usually works.
# For Windows PWD might need conversion? Docker Desktop handles c:/... usually.
DOCKER_CMD := docker run --rm -v "$(CURDIR):/app" $(IMAGE_NAME)

.PHONY: setup test lint format spec-check help

# Default target
help:
	@echo "Chimera Automation Makefile"
	@echo "---------------------------"
	@echo "make setup       - Build the Docker environment"
	@echo "make lint        - Run all linting checks (flake8, black, isort, mypy, bandit)"
	@echo "make format      - Auto-format code with black and isort"
	@echo "make test        - Run tests inside the Docker container"
	@echo "make spec-check  - Verify code compliance with specs (Not implemented yet)"

# 1. Setup: Builds the reproducible development environment
setup:
	docker build -t $(IMAGE_NAME) .

# 2. Test: Runs the test suite inside the container
test:
	$(DOCKER_CMD) pytest tests/

# 3. Lint: Runs all linting and security checks
lint:
	@echo "Running Ruff linter..."
	@$(DOCKER_CMD) ruff check .
	@echo "\nRunning Ruff formatter (check)..."
	@$(DOCKER_CMD) ruff format --check .
	@echo "\nRunning MyPy type checks..."
	@$(DOCKER_CMD) mypy .
	@echo "\nRunning Bandit security checks..."
	@$(DOCKER_CMD) bandit -r . -c pyproject.toml --quiet
	@echo "\n✅ All linting checks passed!"

# 4. Format: Auto-format code
format:
	@echo "Formatting with Ruff..."
	@$(DOCKER_CMD) ruff check --fix .
	@echo "Formatting with Ruff formatter..."
	@$(DOCKER_CMD) ruff format .
	@echo "\n✅ Code formatted!"

# 5. Pre-commit: Run hooks on all files
pre-commit:
	@echo "Running pre-commit on all files..."
	@$(DOCKER_CMD) pre-commit run --all-files

# 6. Spec-Check: Validates alignment with specs/
# Currently fails as per requirements to indicate missing implementation or violation.
spec-check:
	@# Validates alignment with specs/
	@$(DOCKER_CMD) uv run python scripts/spec_check.py
