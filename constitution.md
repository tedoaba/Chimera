<!--
SYNC IMPACT REPORT
Version change: 0.0.0 → 1.0.0
List of modified principles:
- Initial drafting of Project Chimera Constitution
Added sections:
- I. Spec-Centricity (Source of Truth)
- II. Mandatory Spec Alignment (Zero-Drift)
- III. Hierarchical Swarm Governance
- IV. Human-in-the-Loop Safety Authority
- V. Deterministic Conflict Resolution
- Operational Invariants
- Prohibitions
Templates requiring updates:
- .specify/templates/plan-template.md (✅ updated)
- .specify/templates/spec-template.md (✅ updated)
- .specify/templates/tasks-template.md (✅ updated)
Follow-up TODOs:
- None
-->

# Project Chimera Constitution

## Core Principles

### I. Spec-Centricity (Source of Truth)
The `specs/` directory is the absolute source of truth for all system behavior, architecture, and governance. No design or implementation decision is valid unless it is explicitly derived from or captured within a specification file. If a conflict exists between the code and the spec, the spec is correct by definition.

### II. Mandatory Spec Alignment (Zero-Drift)
Implementation without a corresponding, approved, and up-to-date specification is strictly forbidden. Code, infrastructure, and agent logic are downstream artifacts of the specification layer. Any implementation drift must be resolved by either updating the specification (post-ratification) or reverting the implementation to match the spec.

### III. Hierarchical Swarm Governance
The system must maintain a strict Hierarchical Swarm architecture: Planner -> Worker -> Judge. Every action must follow this lifecycle. No worker agent may initiate external impact without a validated plan from the Planner and a safety/quality validation from the Judge.

### IV. Human-in-the-Loop Safety Authority
Humans serve as the terminal safety and ethical authority. Any action involving sensitive domains (including but not limited to finance, legal, health, and politics) or any action assigned a "Low Confidence" score by the Judge must be gated by explicit human approval. AI agents are prohibited from unilaterally executing high-stakes decisions without human oversight.

### V. Deterministic Conflict Resolution
Conflicts between competing specifications or requirements are resolved through a hierarchy of precedence:
1. This Constitution (Global Invariants)
2. Meta-Specifications (`specs/_meta.md`)
3. Domain-specific Specifications (Functional/Technical)
In the event of an unresolvable logical conflict, the Human Orchestrator is the final authority for resolution.

## Operational Invariants

- **Stateless Workers**: Worker agents must be stateless and horizontally scalable; their identity and state must be managed exclusively by the Planner.
- **Traceability**: Every agent action, decision, and confidence score must be recorded in an immutable audit log.
- **Protocol Adherence**: All tool use and data ingestion must strictly adhere to the Model Context Protocol (MCP).

## Prohibitions

- **No Code in Specs**: Specification files must remain implementation-agnostic. They define the *what*, not the *how*.
- **No Invisible Agents**: All AI agents must disclose their nature in interactions; deceptive identity practices are strictly forbidden.
- **No Unsampled Impact**: Fully autonomous execution without the possibility of human sampling or override is prohibited.

## Governance

This Constitution supersedes all other operational practices and guidelines. Amendments to these principles require a formal ratification process involving the Human Orchestrator and updated documentation. All pull requests and system updates must be validated against these principles.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
