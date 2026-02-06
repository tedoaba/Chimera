# Project Chimera

Project Chimera is a platform for autonomous AI influencer agents designed to perceive online environments, generate content, interact on social platforms, and manage on-chain economic activity at scale. It operates as a governed swarm of **Planner**, **Worker**, and **Judge** agents to ensure safe, high-throughput execution of influence campaigns.

## 🚀 Vision

The goal of Project Chimera is to optimize parallel throughput of media campaigns while maintaining strict auditability and bounded autonomy. It emphasizes:
-   **Hierarchical Swarms**: A single planner orchestrating stateless workers, verified by judges.
-   **Human-in-the-Loop**: Automatic execution for high-confidence actions; human review for sensitive or low-confidence tasks.
-   **Protocol-First**: Standardized JSON contracts for all inter-agent communication.
-   **Safety**: Explicit constraints on spend, persona consistency, and regulatory compliance.

## 🏗 Architecture

The system follows a three-role agentic pattern:

1.  **Planner**: Decomposes high-level campaign goals into a graph of executable tasks with dependencies. It manages adaptation and re-planning based on feedback.
2.  **Worker**: Executes individual tasks, such as generating text/media assets or fetching data via MCP tools.
3.  **Judge**: Evaluates worker outputs against safety, quality, and persona guidelines. It assigns confidence scores and routes decisions (Approve, Retry, Escalate).

## 📂 Project Structure

```
Chimera/
├── .github/            # CI/CD workflows (GitHub Actions)
├── .coderabbit.yaml    # AI Code Review policies
├── skills/             # Agent skills and capabilities
├── specs/              # Project blueprints and specifications
│   ├── _meta.md        # Vision & constraints
│   ├── functional.md   # Functional requirements
│   ├── technical.md    # Technical architecture & contracts
│   └── openclaw...     # Integration specs
├── tests/              # Unit and integration tests
├── scripts/            # Utility scripts
├── Dockerfile          # Reproducible development environment
├── Makefile            # Standardized command automation
├── pyproject.toml      # Project metadata and dependencies
```

## 🛠 Prerequisites

-   **Docker**: Required for the containerized environment.
-   **Python 3.12+**: If running locally outside Docker.
-   **uv**: Recommended for fast dependency management.

## ⚡ Getting Started

This project uses a `Makefile` to strictly standardize development commands.

### 1. Setup Environment
Build the Docker image containing all dependencies and tools:
```bash
make setup
```

### 2. Run Tests
Execute the test suite within the isolated container:
```bash
make test
```

### 3. Verify Specs
Check code compliance against the architectural specifications (currently a placeholder):
```bash
make spec-check
```

## 🔄 CI/CD & Governance

-   **GitHub Actions**: Automatically runs `make test` on every push to ensure build integrity.
-   **CodeRabbit**: AI-powered code reviews enforce specification alignment and security checks on Pull Requests.
-   **Strict Typing**: Python code follows strict typing guidelines to ensure reliability.

## 🤝 Contributing

1.  Read the `specs/` directory to understand the core architecture.
2.  Follow the **Planner-Worker-Judge** pattern for any new agentic features.
3.  Ensure all new modules have corresponding tests in `tests/`.
4.  Run `make test` before submitting any changes.

## 📄 License

See `LICENSE` file for details.
