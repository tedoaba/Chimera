## Developer Tooling Strategy (MCP) for Project Chimera

This document describes the **developer-side MCP tools** required to build, test, and debug Project Chimera’s planner, worker, judge, and execution layers. It focuses on **capabilities and configuration expectations**, not installation details.

---

## 1. Core Development Tooling MCP Servers

### 1.1 `filesystem-mcp`

- **Purpose**:  
  - Provide structured, tool-based access to the Chimera codebase and configuration files.  
  - Enable agents to **read, diff, and write** project files in a controlled way during development tasks (refactors, spec updates, config changes).
- **Primary Use Cases**:  
  - Editing specs (`functional.md`, `technical.md`, `openclaw_integration.md`) and derived documents.  
  - Maintaining skills metadata under `skills/` (IO contracts, README updates).  
  - Adjusting configuration for planners, workers, judges without manual editor intervention.
- **Configuration Notes**:  
  - Scope access to the **Chimera workspace root** only (e.g., `c:/Users/user/tedoaba/Chimera`).  
  - Enforce **read-only** mode for sensitive directories (secrets, credentials, production config).  
  - Enable a clear **audit trail** of file operations (who/what changed which files, when).  
  - Configure path allow/deny lists so tools cannot modify `.git` internals or OS-level paths.
- **Dependencies / Requirements**:  
  - Stable, POSIX-like file operations (create, read, write, move, delete).  
  - Underlying editor/host must support MCP transport (e.g., Cursor or another IDE with MCP support).

---

### 1.2 `git-mcp`

- **Purpose**:  
  - Expose Git operations (status, diff, branch, commit, merge, tag) to agents through a controlled MCP interface.  
  - Allow agents to **propose and manage changes as cohesive commits** aligned with Chimera’s spec-driven workflow.
- **Primary Use Cases**:  
  - Generating and reviewing diffs for spec or code edits before merging.  
  - Branch-based workflows for feature development (e.g., new skills, planner strategies).  
  - Attaching Git metadata to observability pipelines (linking traces to commit SHAs).
- **Configuration Notes**:  
  - Restrict destructive commands: no force-push, no history rewrites by default.  
  - Require **explicit approval** for commits that touch governance-critical files (e.g., safety rules, financial guardrail configs).  
  - Standardize commit message format, e.g. `role: short summary` (planner/worker/judge/infra).
- **Dependencies / Requirements**:  
  - Local Git repository initialized at the Chimera root.  
  - SSH/HTTPS credentials handled **outside** MCP (host environment responsibility).

---

### 1.3 `test-runner-mcp`

- **Purpose**:  
  - Provide a stable interface to run **unit, integration, and contract tests** for Chimera’s internals (planning, worker tasks, judge rules, execution intents).  
  - Allow automated regression checks whenever specs or skills definitions change.
- **Primary Use Cases**:  
  - Running targeted suites for planner/worker/judge modules.  
  - Verifying adherence to API contracts defined in `technical.md` (Goal → Plan, Task Assignment, Execution Intent, etc.).  
  - Smoke tests for new MCP integrations (e.g., execution tools).
- **Configuration Notes**:  
  - Expose commands as **named test profiles** (e.g., `unit`, `integration`, `contracts`) instead of raw shell strings.  
  - Return structured results: `{ suite, passed, failed, durationMs, failures[] }`.  
  - Enforce resource limits (time, CPU) to prevent runaway test runs.
- **Dependencies / Requirements**:  
  - Project test framework set up (e.g., `pytest`, `jest`, or equivalent).  
  - Stable test data fixtures for planner/worker/judge flows.

---

### 1.4 `schema-linter-mcp`

- **Purpose**:  
  - Validate JSON-like contracts defined in `technical.md` and related specs against a central schema registry.  
  - Ensure that internal messages (Goal → Plan, Task Assignment, Worker Output → Judge, Execution Intent) remain **backwards compatible** and consistent.
- **Primary Use Cases**:  
  - Linting new or modified API shapes when changing planners, workers, or execution layers.  
  - Detecting breaking changes before they reach runtime agents.  
  - Recording schema versions and hashes referenced in OpenClaw publication (schema hash).
- **Configuration Notes**:  
  - Define canonical schemas for all key entities: Goal, Plan, Task, AgentOutput, Evaluation, HumanReview, ExecutionIntent, TrendFeedItem.  
  - Enforce versioned schema evolution (e.g., `v1`, `v1.1`) rather than ad hoc field changes.  
  - Expose severity levels (error/warning/info) and remediation hints.
- **Dependencies / Requirements**:  
  - JSON Schema or equivalent validation engine.  
  - Schema sources stored in-version (e.g., `specs/schemas/`) and accessible via `filesystem-mcp`.

---

## 2. Observability & Debugging Tools

### 2.1 `logs-mcp`

- **Purpose**:  
  - Provide structured access to **planner, worker, judge, and execution traces**, aligned with entities in the technical spec (Goal, Plan, Task, ExecutionIntent, Trace/Audit Log).  
  - Support root-cause analysis and regression debugging from within the development environment.
- **Primary Use Cases**:  
  - Querying traces for a specific `goalId`, `planId`, or `taskId`.  
  - Inspecting Judge rationales and risk flags for misclassifications.  
  - Reviewing ExecutionIntent flows, idempotency behavior, and external references.
- **Configuration Notes**:  
  - Enforce query scoping (e.g., by environment: `dev`, `staging`, `sandbox`) to avoid production data leakage.  
  - Normalize log entries to a consistent envelope: `{ traceId, actor, action, timestamp, payloadSummary, error? }`.  
  - Provide time-limited access tokens or environment-specific endpoints configured outside MCP.
- **Dependencies / Requirements**:  
  - Central logging/trace backend (e.g., OpenTelemetry-compatible store, cloud logs, or self-hosted DB).  
  - Stable APIs/queries exposed for MCP consumption.

---

### 2.2 `metrics-mcp`

- **Purpose**:  
  - Surface **aggregated metrics** relevant to Chimera’s operation: throughput, approval rates, spend, failure patterns.  
  - Allow agents to propose guardrail or configuration changes based on real performance data.
- **Primary Use Cases**:  
  - Monitoring quality and safety guardrail effectiveness (judge approval vs. escalation rates).  
  - Tracking financial guardrail adherence (spend per goal/intent vs. budget caps).  
  - Identifying hotspots in planner/worker tasks (high latency, frequent retries).
- **Configuration Notes**:  
  - Expose fixed metric views or queries (e.g., `campaign_overview`, `safety_overview`, `spend_overview`) rather than arbitrary query strings.  
  - Return time-bucketed series with clear units (e.g., `ratePerHour`, `usd`, `count`).  
  - Guard sensitive financial or PII details; expose aggregates only in dev-facing tools.
- **Dependencies / Requirements**:  
  - Metrics backend (e.g., Prometheus, cloud metrics service) with stable endpoints.  
  - Alignment between metric names and functional spec concepts (Goal, Plan, Task, ExecutionIntent).

---

## 3. Execution & Sandbox Integration Tools

### 3.1 `execution-sandbox-mcp`

- **Purpose**:  
  - Emulate **ExecutionIntent** handling (post/reply/upload_video/transfer_funds) in a **non-production sandbox**, for safe end-to-end testing.  
  - Validate that planner and worker outputs form valid, executable intents under budget and policy constraints.
- **Primary Use Cases**:  
  - Running dry-runs of full workflows from Goal → Plan → Task → Judge → ExecutionIntent.  
  - Testing failure modes (platform unreachable, policy violations, budget exceeded).  
  - Verifying idempotency behavior using `idempotencyKey`.
- **Configuration Notes**:  
  - Require explicit environment flag (e.g., `env: sandbox`) on all calls.  
  - Never forward real credentials or tokens to external platforms.  
  - Persist simulated `externalRef` identifiers only in sandbox storage, clearly labeled as such.
- **Dependencies / Requirements**:  
  - Mock or sandbox endpoints for external platforms (YouTube, social networks, payment rails).  
  - Consistent mapping from internal actions to sandbox behaviors.

---

### 3.2 `openclaw-registry-mcp` (Optional)

- **Purpose**:  
  - When OpenClaw is enabled, provide a tool interface for publishing Chimera’s **status, capabilities, and safety posture** to the OpenClaw/Moltbook registry, as described in `openclaw_integration.md`.  
  - Allow developers to verify that published signals (status, capabilities, limits, schema hash) match the local configuration.
- **Primary Use Cases**:  
  - Triggering manual heartbeats in development to inspect payloads.  
  - Validating signatures and schema hashes before enabling autonomous publication.  
  - Inspecting recent published signals for audit and debugging.
- **Configuration Notes**:  
  - Allow this MCP server to be **disabled entirely** when OpenClaw participation is not permitted.  
  - Require configuration of registry endpoint, signing keys, and heartbeat interval via environment or config files (not inline).  
  - Enforce that no cross-agent execution commands are accepted—only status/metadata publishing is permitted.
- **Dependencies / Requirements**:  
  - Network access to the OpenClaw registry endpoint for dev/staging environments.  
  - Key management handled by the host environment (signing keys not stored in the repo).

---

## 4. Developer Experience & Safety

### 4.1 `policy-inspector-mcp`

- **Purpose**:  
  - Centralize access to **safety, persona, and financial guardrail policies** that influence planner, worker, judge, and execution behavior.  
  - Help developers understand how changes in prompts, tasks, or skills affect governance.
- **Primary Use Cases**:  
  - Viewing effective safety rules applied to a given task type (`generate_video_caption`, etc.).  
  - Inspecting financial guardrails per goal/intent (budget caps, downgrade behavior).  
  - Explaining why a Judge or Execution layer blocked or escalated an action.
- **Configuration Notes**:  
  - Treat policies as versioned documents, with clear `policyVersion` and `effectiveDate`.  
  - Support diffing policy versions via `filesystem-mcp` + `git-mcp`, but expose read-only views here.  
  - Provide human-readable summaries along with structured policy objects.
- **Dependencies / Requirements**:  
  - Policy store (files, DB, or configuration service) accessible from development environments.  
  - Alignment with functional spec sections for Quality & Safety Governance and Financial Guardrails.

---

### 4.2 `memory-browser-mcp`

- **Purpose**:  
  - Allow developers to inspect **state, memory, and learning artifacts** (short-term caches, vector stores, long-term memory) without writing ad hoc queries.  
  - Help validate that planners and workers have the right context (persona, history, trends).
- **Primary Use Cases**:  
  - Viewing memory entries related to a given `goalId` or `planId`.  
  - Inspecting embeddings and associated metadata for MediaAssets and TrendFeedItems.  
  - Debugging context drift when workers produce off-persona or stale content.
- **Configuration Notes**:  
  - Provide read-only access in development to avoid accidental mutation of memory state.  
  - Support simple filters: by entity type (Goal, Plan, Task, MediaAsset, TrendFeedItem), by time window, by tag.  
  - Scrub or aggregate any PII or sensitive user data before exposure.
- **Dependencies / Requirements**:  
  - Underlying vector store and document store reachable from dev environment.  
  - Stable mapping between stored entities and the logical data model in `technical.md`.

---

## 5. Tooling Principles

- **Directly Empower Agent Development**:  
  All MCP tools listed above exist to make it easier to **design, implement, test, and debug** Chimera’s planner/worker/judge/execution ecosystem. Non-essential or purely operational tools are out of scope here.

- **No Runtime Secrets in Repo**:  
  Credentials, API keys, and signing keys are injected by the host environment; MCP tools only reference them indirectly via configuration.

- **Spec-First Workflow**:  
  Tooling should reinforce the specs in `functional.md`, `technical.md`, and `openclaw_integration.md`. Any change to contracts or entities should be validated by schema, tests, and Git reviews via MCP.

- **Safety and Financial Guardrails as First-Class Concerns**:  
  Observability, policy inspection, metrics, and sandbox execution tools must all support the **Quality & Safety Governance**, **Financial Guardrails**, and **Observability & Audit** sections of the functional spec.

