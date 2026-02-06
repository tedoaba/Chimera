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

.PHONY: setup test spec-check help

# Default target
help:
	@echo "Chimera Automation Makefile"
	@echo "---------------------------"
	@echo "make setup       - Build the Docker environment"
	@echo "make test        - Run tests inside the Docker container"
	@echo "make spec-check  - Verify code compliance with specs (Not implemented yet)"

# 1. Setup: Builds the reproducible development environment
setup:
	docker build -t $(IMAGE_NAME) .

# 2. Test: Runs the test suite inside the container
test:
	$(DOCKER_CMD) pytest tests/

# 3. Spec-Check: Validates alignment with specs/
# Currently fails as per requirements to indicate missing implementation or violation.
spec-check:
	@# Validates alignment with specs/
	@$(DOCKER_CMD) uv run python scripts/spec_check.py
