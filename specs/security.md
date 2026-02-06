# Security & Governance Specification

This document details the security architecture, authentication mechanisms, and safety protocols for Project Chimera.

## Authentication & Authorization

### 1. Unified Authentication
- **Service-to-Service**: Agents and MCP tools authenticate via **Mutual TLS (mTLS)** or **OIDC Service Tokens**. Internal requests must include an `X-Agent-ID` and `X-Request-Provenance` header.
- **Human Users**: OAuth2 with OpenID Connect (OIDC). Supports SSO (e.g., Google, GitHub).
- **Session Management**: JWT (JSON Web Tokens) with a short TTL (15 minutes) and Refresh Tokens (24 hours).

### 2. Role-Based Access Control (RBAC)
| Role | Permissions |
| :--- | :--- |
| **CFO Controller** | Manage spend limits, view financial audit logs. No campaign editing. |
| **Orchestrator** | Create goals, view all plans, trigger re-plans. |
| **Reviewer** | Access Review Queue, approve/reject escalated content. |
| **Auditor** | Read-only access to all trace logs and safety evidence. |
| **System Admin** | Manage identities, rotate keys, configure safety thresholds. |

## Content Safety Pipeline

Every output from a Worker must pass through the **Judge Safety Layer** before reaching human review or execution.

### Stage 1: Automated Scanners
- **Llama Guard / Perspective API**: Multi-class classification (Hate, Harassment, Self-harm, Physical violence, Sexual, PII).
- **Keyword Blacklist**: Domain-specific restricted terms (e.g., medical advice, financial "guarantees").
- **Regex Detectors**: PII (Emails, SSNs, Private Addresses).

### Stage 2: Policy Compliance (LLM Judge)
- **Constraint Matching**: Verify content respects the `persona` and `constraints` defined in the Goal.
- **Disclosure Check**: Ensure AI-nature disclosure is present where required by platform policy.

### Stage 3: Domain Gating
- If the identified topic falls into **Sensitive Domains** (Politics, Finance, Health, Law), the `route` is automatically set to `human_review` regardless of the confidence score.

## Rate Limiting & Protection

### API Gateways
- **Orchestrator/Reviewer Endpoints**: 60 requests/min per IP.
- **Worker Endpoints**: 500 requests/min total (swarming protection).
- **Execution Tools**: Enforced delay to match platform TOS (e.g., 1 post per hour for YouTube API keys).

### Token Handling
- Secrets (API Keys, OAuth Secrets) are never stored in the database.
- Use a **Vault / KMS** (e.g., AWS Secrets Manager, HashiCorp Vault).
- Access tokens for social platforms are scoped per-campaign and include a `budgetUsd` attribute.

## Financial Guardrails (Hard Limits)

1. **Goal Cap**: A hard stop when a campaign reaches 100% of its `budgetUsd`. All pending tasks for that goal are cancelled.
2. **Action Cap**: Max cost per individual execution (e.g., "Do not spend >$50 on a single promoted post").
3. **Daily Burn Rate**: Max spend per 24h window for the entire project.

## Incident Response
- **Panic Button**: A global flag that stops all **Execution Layer** actions.
- **Revocation**: Ability to invalidate a `traceId` or `goalId`, triggering an immediate stop to associated worker tasks.
