# Use specific Python version for reproducibility
FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the virtual environment path outside /app to avoid conflict with bind mounts
ENV UV_PROJECT_ENVIRONMENT="/venv"
# Add the virtual environment to the PATH
ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH"

# Set working directory
WORKDIR /app

# Install system dependencies
# git: required for some python package installations
# build-essential: required for compiling extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install project dependencies
# --frozen: Sync exactly with uv.lock
# --all-extras: Install all optional dependencies including [dev] for linting tools
RUN uv sync --frozen --all-extras --no-install-project

# Default command
CMD ["pytest"]
