# Project Chimera

**An Autonomous AI Influencer Agent Platform Built with Governed Swarm Intelligence**

Project Chimera is a production-grade platform for operating large populations of autonomous AI influencer agents. These agents perceive online environments, generate content, interact on social platforms, and manage on-chain economic activity—all at massive scale under centralized governance and safety controls.

## Vision

Project Chimera enables **bounded autonomy at scale** through:
- **Project Constitution**: The supreme governance document at `.specify/memory/constitution.md`
- **Hierarchical Swarms**: Planner-Worker-Judge architecture for massive parallelism with safety
- **Human-in-the-Loop**: Absolute authority for sensitive or low-confidence decisions
- **Protocol-First Design**: Standardized JSON contracts via Model Context Protocol (MCP)
- **Safety & Compliance**: Explicit constraints on spend, persona consistency, and regulatory adherence
- **Agent Social Networks**: Ready for integration with OpenClaw and agent-to-agent ecosystems


![Project Chimera Mind Map](assets/project-chimera-mind-map.png)

## Project Foundation: Completed Tasks

This repository represents the **complete foundational phase** of Project Chimera, following a rigorous three-stage development process:

### **Task 1: The Strategist (Research & Foundation)**

#### 1.1 Deep Research & Reading
**Location**: `docs/RESEARCH_SUMMARY.md`

Comprehensive analysis of:
- **The Trillion Dollar AI Code Stack** (a16z) - Understanding AI agents in long-running workflows
- **OpenClaw & Agent Social Networks** - AI-to-AI interaction patterns
- **MoltBook: Social Media for Bots** - Explicit agent collaboration protocols
- **Project Chimera SRS** - Core system requirements

**Key Insights**:
- How Chimera fits into the "Agent Social Network" paradigm
- Social protocols needed for agent-to-agent communication
- The gap between explicit (Moltbook) vs. implicit (Chimera) agent societies

#### 1.2 Domain Architecture Strategy
**Location**: `docs/ARCHITECTURE.md`

**Decisions Made**:
- **Agent Pattern**: Hierarchical Swarm (Planner-Worker-Judge)
- **Human-in-the-Loop**: Conditional governance via Judge confidence scoring
- **Database Strategy**: Polyglot persistence
  - Redis for short-term operational context
  - Vector DB (Weaviate) for semantic memory
  - NoSQL for high-velocity media metadata

#### 1.3 "Golden" Environment Setup
- **Git Repository**: Initialized with professional `.gitignore`
- **Tenx MCP Sense**: Connected via `.cursor/mcp.json`
- **Python Environment**: Professional `uv` setup with `pyproject.toml` (Python >=3.12.12)

### **Task 2: The Architect (Specification & Context Engineering)**

#### 2.1 Master Specification
**Location**: `specs/` directory

Complete project blueprint following GitHub Spec Kit structure:

| File | Purpose |
|------|---------|
| `.specify/memory/constitution.md` | Supreme project principles, invariants, and prohibitions |
| `specs/_meta.md` | High-level vision, constraints, and project philosophy |
| `specs/functional.md` | User stories, agent flows, and governance requirements |
| `specs/technical.md` | API contracts, database schemas, and data models |
| `specs/openclaw_integration.md` | Agent social network integration strategy |

**Key Specifications**:
- **API Contracts**: Goal → Plan, Task Assignment, Agent Output, Evaluation, Execution Intent
- **Database Schema**: ERD for Goals, Plans, Tasks, MediaAssets, TrendFeedItems, Reviews
- **Agent Workflows**: Planner, Worker, Judge, and Execution Layer interactions

#### 2.2 Context Engineering & "The Brain"
**Location**: `.cursor/rules/agent.mdc`

**AI Agent Behavioral Contract**:
- **Project Context**: "This is Project Chimera, an autonomous influencer system"
- **Prime Directive**: "NEVER generate code without checking `specs/` first"
- **Traceability**: "Explain your plan before writing code"
- **AI Fluency Triggers**: Performance monitoring and competency tracking

**Enforcement**: All AI assistants in this repository must follow spec-first, plan-before-code discipline.

#### 2.3 Tooling & Skills Strategy

**Developer Tools (MCP)** - `research/tooling_strategy.md`:
- **Core Development**: `filesystem-mcp`, `git-mcp`, `test-runner-mcp`, `schema-linter-mcp`
- **Observability**: `logs-mcp`, `metrics-mcp`
- **Execution & Sandbox**: `execution-sandbox-mcp`, `openclaw-registry-mcp`
- **Developer Experience**: `policy-inspector-mcp`, `memory-browser-mcp`

**Agent Skills (Runtime)** - `skills/README.md`:

Defined 3+ critical skills with complete Input/Output contracts:

| Skill | Purpose | Primary Caller |
|-------|---------|----------------|
| `skill_ingest_trend_feeds` | Fetch and normalize trend/news feeds | Planner, Worker |
| `skill_generate_media_asset` | Generate text/image/video from task brief | Worker |
| `skill_execute_publish_intent` | Execute validated actions on external platforms | Execution Layer |

### **Task 3: The Governor (Infrastructure & Governance)**

#### 3.1 Test-Driven Development (TDD)
**Location**: `tests/` directory

**Failing Tests** (by design—define the "empty slot" for implementation):

| Test File | Purpose |
|-----------|---------|
| `test_trend_fetcher.py` | Asserts trend data structure matches API contract |
| `test_skills_interface.py` | Asserts skills modules accept correct parameters |

**Testing Philosophy**: Write tests BEFORE implementation to define contracts.

#### 3.2 Containerization & Automation

**Dockerfile** (`Dockerfile`):
- Based on Python 3.12-slim
- Includes `uv` for fast dependency management
- Optimized layer caching and minimal image size

**Makefile** (`Makefile`):

| Command | Purpose |
|---------|---------|
| `make setup` | Install dependencies (idempotent) |
| `make lint` | Run all linting checks (Ruff, MyPy, Bandit) |
| `make format` | Auto-format and fix code with Ruff |
| `make test` | Run tests in Docker |
| `make spec-check` | Verify code alignment with `specs/` |

**See**: `docs/LINTING.md` for detailed linting documentation.

#### 3.3 CI/CD & AI Governance

**GitHub Actions** (`.github/workflows/main.yml`):
- **Trigger**: Every push and pull request
- **Jobs**: `make setup` → `make test`
- **Environment**: Ubuntu latest with Docker Buildx

**AI Review Policy** (`.coderabbit.yaml`):
- **Spec Alignment**: Verifies all changes respect `specs/` contracts
- **Security**: Static analysis for injection flaws, secrets exposure
- **Enforcement**: Flags spec violations and security risks as blocking issues

## Architecture at a Glance

### Agent Coordination Pattern
**Hierarchical Swarm**: Planner → Worker Swarm → Judge → (Optional) Human Review → Execution

### Human-in-the-Loop (HITL)
```
Judge assigns confidence score:
├─ High confidence → Auto-approve
├─ Medium confidence → Route to human
└─ Low confidence → Reject & retry

Sensitive topics (politics, health, finance, law) → Always require human approval
```

### Data Architecture
**Polyglot Persistence**:
- **Redis**: Short-term context, operational state
- **Vector DB (Weaviate)**: Long-term semantic memory, embeddings
- **NoSQL**: High-velocity media metadata (flexible schema)

## Repository Structure

```
Chimera/
├── .cursor/
│   ├── mcp.json                    # MCP server configuration (Tenx Feedback Analytics)
│   └── rules/
│       └── agent.mdc               # AI behavioral contract & governance rules
├── .github/
│   ├── workflows/
│   │   └── main.yml               # CI/CD pipeline (test automation)
│   └── copilot-instructions.md    # GitHub Copilot governance guidelines
├── .coderabbit.yaml               # AI code review policy
├── docs/
│   ├── ARCHITECTURE.md            # Domain architecture strategy
│   ├── LINTING.md                 # Code quality & linting setup guide
│   └── RESEARCH_SUMMARY.md        # Agent social networks research synthesis
├── research/
│   └── tooling_strategy.md        # Developer MCP tools strategy
├── specs/
│   ├── _meta.md                   # Vision, constraints, philosophy
│   ├── functional.md              # User stories, agent workflows
│   ├── technical.md               # API contracts, database schema
│   └── openclaw_integration.md    # Agent social network integration
├── skills/
│   └── README.md                  # Runtime agent skills (Input/Output contracts)
├── tests/
│   ├── test_trend_fetcher.py      # TDD: Trend data contract validation
│   └── test_skills_interface.py   # TDD: Skills interface validation
├── assets/
│   └── project-chimera-mind-map.png  # Architecture visualization
├── Dockerfile                      # Containerized development environment
├── Makefile                        # Standardized automation commands
├── pyproject.toml                  # Python project metadata (uv-managed)
├── uv.lock                         # Locked dependencies
└── README.md                       # This file
```

## 🛠 Prerequisites

- **Docker**: Required for containerized environment
- **Python 3.12+**: If running locally (uv recommended)
- **Git**: Version control
- **Make**: Command automation (usually pre-installed on Unix systems; use WSL on Windows)

## Quick Start

### 1 Clone the Repository
```bash
git clone https://github.com/tedoaba/Chimera.git
cd Chimera
```

### 2️ Setup Environment
```bash
make setup
```
Builds the Docker image with all dependencies.

### 3️ Run Tests (TDD Style)
```bash
make test
```
Executes the test suite. **Note**: Tests are currently failing by design (TDD approach).

### 4 Verify Spec Compliance
```bash
make spec-check
```
Validates that code aligns with architectural specifications.

## Understanding the Project

### Start Here (Recommended Reading Order):

1. **`specs/_meta.md`** - Understand the vision and constraints
2. **`docs/ARCHITECTURE.md`** - Learn the Planner-Worker-Judge pattern
3. **`docs/RESEARCH_SUMMARY.md`** - Context on agent social networks
4. **`specs/functional.md`** - User stories and agent workflows
5. **`specs/technical.md`** - API contracts and data models
6. **`skills/README.md`** - Runtime agent capabilities
7. **`research/tooling_strategy.md`** - Developer tooling ecosystem

## CI/CD & Governance Pipeline

```
Developer Push
    ↓
GitHub Actions Trigger
    ├─ Build Docker environment (make setup)
    ├─ Run linting checks (make lint) 
    ├─ Run test suite (make test)
    └─ Report status
    ↓
Pull Request Created
    ↓
CodeRabbit AI Review
    ├─ Spec Alignment Check
    ├─ Security Vulnerability Scan
    └─ Code Quality Analysis
    ↓
Human Approval (if passing)
    ↓
Merge to Main
```

## Testing Philosophy

**Test-Driven Development (TDD)**:
1. Write **failing tests** that define contracts (API shapes, behaviors)
2. Tests represent the "empty slot" to fill
3. Implementation must satisfy the pre-written tests
4. Tests serve as executable documentation

**Current Status**: Foundational tests are intentionally failing, awaiting implementation.

##  Contributing

### Before Writing Code:
1. **Read `specs/` directory** - Understand the contracts
2. **Check `.cursor/rules/agent.mdc`** - Follow the behavioral contract
3. **Explain your plan** - Trace back to specs before coding

### Development Workflow:
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Follow **Planner-Worker-Judge** pattern for agentic features
3. Write tests in `tests/` (or ensure existing tests pass)
4. Run `make test` locally
5. Submit PR (CodeRabbit will review for spec alignment & security)
6. Address feedback and merge

### Key Principles:
- **Spec-First**: Never generate code without checking `specs/` first
- **Traceability**: Explain reasoning and reference specs in commit messages
- **Safety**: Never hardcode secrets or credentials
- **Quality**: All new features require tests

## Security & Safety

- **No Hardcoded Secrets**: All credentials via environment variables
- **AI Governance**: CodeRabbit enforces security best practices
- **Spec Enforcement**: Breaking spec contracts triggers review blocks
- **Human Oversight**: Sensitive actions (finance, health, politics, law) require human approval

## Agent Social Network Integration

**OpenClaw Integration** (`specs/openclaw_integration.md`):
- Status: Planned for future phases
- Purpose: Publish agent availability/capabilities to agent social networks
- Protocol: MCP-based heartbeat with schema hashing
- Security: Read-only status publication, no cross-agent execution commands

## References

- [The Trillion Dollar AI Code Stack (a16z)](https://a16z.com/the-trillion-dollar-ai-software-development-stack/)
- [OpenClaw & Agent Social Networks](https://techcrunch.com/2026/01/30/openclaws-ai-assistants-are-now-building-their-own-social-network/)
- [MoltBook: Social Media for Bots](https://theconversation.com/openclaw-and-moltbook-why-a-diy-ai-agent-and-social-media-for-bots-feel-so-new-but-really-arent-274744)

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## License

See `LICENSE` file for details.
