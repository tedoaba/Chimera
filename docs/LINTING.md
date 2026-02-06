# Code Quality & Linting Setup

Project Chimera uses a modern, high-performance linting and code quality pipeline to ensure consistency, security, and maintainability. Our stack is centered around **Ruff**, a lightning-fast Python linter and formatter.

## Tools

### 1. **Ruff** - All-in-one Linter & Formatter
- **Replaces**: `flake8`, `black`, `isort`, `pyupgrade`, and more.
- **Style Enforcement**: Enforces PEP 8 and hundreds of other rules.
- **Formatting**: Handles code formatting with an opinionated style similar to Black.
- **Import Sorting**: Automatically organizes and cleans up imports.
- **Configuration**: `pyproject.toml` → `[tool.ruff]`
- **Speed**: Written in Rust, it is 10-100x faster than traditional tools.

### 2. **MyPy** - Static Type Checker
- **Purpose**: Validates type hints and type safety across the project.
- **Configuration**: `pyproject.toml` → `[tool.mypy]`
- **Enforcement**: Strictly enforced in CI to catch type-related bugs before runtime.
- **Exclusions**: Validates core logic while excluding external dependencies and ignored modules.

### 3. **Bandit** - Security Linter
- **Purpose**: Scans for common security vulnerabilities (SQL injection, weak crypto, etc.).
- **Configuration**: `pyproject.toml` → `[tool.bandit]`
- **Scope**: Integrated into the Ruff ruleset (`S` category) but also run standalone for deep scanning.
- **Exclusions**: Skips `B101` (assert checks) in tests to allow TDD patterns.

### 4. **Pre-commit Hooks**
- **Purpose**: Automatically runs all checks before code is even committed.
- **Setup**: Configured in `.pre-commit-config.yaml`.
- **Hooks**: Includes trailing whitespace filters, YAML/TOML checkers, Ruff, and MyPy.

## Usage

### Local Development

#### Run all linting checks:
```bash
make lint
```
This runs `ruff check`, `ruff format --check`, `mypy`, and `bandit`.

#### Auto-format and fix code:
```bash
make format
```
This runs `ruff check --fix` and `ruff format`.

#### Run pre-commit on all files:
```bash
make pre-commit
```

#### Individual tools (via Docker):
```bash
# Linter check
docker run --rm -v "$(pwd):/app" chimera-dev ruff check .

# Formatter check
docker run --rm -v "$(pwd):/app" chimera-dev ruff format --check .

# Auto-fix and format
docker run --rm -v "$(pwd):/app" chimera-dev ruff check --fix .
docker run --rm -v "$(pwd):/app" chimera-dev ruff format .

# Type checking
docker run --rm -v "$(pwd):/app" chimera-dev mypy .

# Security scanning
docker run --rm -v "$(pwd):/app" chimera-dev bandit -r . -c pyproject.toml
```

### CI/CD Pipeline

Linting is a **mandatory quality gate** in our GitHub Actions workflow (`.github/workflows/main.yml`):

1. **Build Environment** - Docker image with deterministic dependencies.
2. **Run Linting** - Executes `make lint`. Any violation fails the build.
3. **Run Tests** - Only executed if linting passes successfully.

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | **Central Config**: Ruff, MyPy, Bandit, and Pytest settings. |
| `.pre-commit-config.yaml` | Local git hook configuration. |
| `.gitignore` | Excludes `.ruff_cache`, `.mypy_cache`, and other linter artifacts. |

## Why This Matters for AI Agents

1. **Spec Alignment**: Validates that function signatures match architectural contracts.
2. **Security**: Catching vulnerabilities (like insecure `eval` or `subprocess` calls) is critical for autonomous agents.
3. **Consistency**: Ruff ensures that agent-generated code looks identical to human-written code.
4. **Type Safety**: MyPy ensures that the complex JSON schemas used in MCP and Swarm communication are respected.
5. **Fast Feedback**: Ruff's extreme speed allows agents to self-correct their style in milliseconds.

## Troubleshooting

### "make: command not found"
- **WSL/Linux/macOS**: Usually pre-installed.
- **Windows**: Use PowerShell or install via `winget install GnuWin32.Make`.

### Linting fails on my changes
- Run `make format` to automatically fix formatting and simple linting errors.
- If a violation is intentional, use `# noqa: <RULE_CODE>` (e.g., `# noqa: E501`) and provide a brief comment explaining why.

### Docker build is slow
- The `Dockerfile` uses layers to cache dependencies. Ensure you aren't changing `pyproject.toml` unnecessarily.
- Using `uv` inside Docker significantly speeds up environment setup.

## Integration with Agent Rules

Our linting setup directly enforces the **Spec-First Behavior** defined in `.cursor/rules/agent.mdc`:

- **Rule 2 (Specs)**: Type checks validate alignment with `specs/`.
- **Rule 6 (Output)**: Automated formatting ensures high-quality code generation.
- **Rule 7 (Enforcement)**: CI blocks any PR that deviates from these standards.
