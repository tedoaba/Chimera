# Acceptance Criteria & Scenarios

This document defines the Gherkin scenarios for Project Chimera's core capabilities, ensuring verifiable outcomes for all features.

## 1. Goal Planning & Decomposition

### Scenario: Successful Goal Decomposition
  **Given** a Human Orchestrator submits a goal "Increase engagement for Product X" with a $5000 budget
  **When** the Planner receives the request
  **Then** a `Plan` entity should be created with at least 3 distinct tasks
  **And** each task must have a `budgetUsd` constraint
  **And** the plan's `status` should be "active"

### Scenario: Planning Failure on Invalid Constraints
  **Given** a Goal Request with a deadline in the past
  **When** the Planner processes the request
  **Then** the API should return an `INVALID_GOAL` error
  **And** no `Plan` or `Task` entities should be persisted

## 2. Worker Performance & Accuracy

### Scenario: Worker Output within Latency Bounds
  **Given** a video captioning task with `maxLatencySec: 120`
  **When** the Worker executes the task
  **Then** it should return a result within 120 seconds
  **And** the result must contain `content` and `confidence` score
  **And** the `costUsd` must be less than the task's `budgetUsd`

### Scenario: Worker Retry on Tool Failure
  **Given** a Worker task fails with `TOOL_ERROR` and `retryable: true`
  **When** the system detects the failure
  **Then** the `attempt` count should increment
  **And** a new task execution should be triggered
  **Until** success or `maxAttempts` (3) is reached

## 3. Judge & Safety Governance

### Scenario: Auto-Approval of High Confidence Content
  **Given** a Worker output with `confidence: 0.95` and no safety risk flags
  **When** the Judge evaluates the output
  **Then** the `decision` should be "approve"
  **And** the `route` should be "auto"
  **And** no `HumanReview` should be created

### Scenario: Escalation of Low Confidence Content
  **Given** a Worker output with `confidence: 0.45`
  **When** the Judge evaluates the output
  **Then** the `decision` should be "escalate"
  **And** a `HumanReview` entity should be created with state "pending"

### Scenario: Mandatory Review for Sensitive Domains
  **Given** an output identified with `domain: finance`
  **When** the Judge evaluates the output
  **Then** the `route` must be "human_review" regardless of `confidence`
  **And** the `riskFlags` must include "domain-sensitive"

## 4. Human Review & Execution

### Scenario: Human Approval Triggers Execution
  **Given** a `HumanReview` task with state "pending"
  **When** a Reviewer submits a "approve" decision
  **Then** an `ExecutionIntent` must be created
  **And** the `approvedBy` field must be "human"
  **And** the action should be dispatched to the platform MCP tool

### Scenario: Human Rejection Stops Workflow
  **Given** a `HumanReview` task
  **When** a Reviewer submits a "reject" decision
  **Then** no `ExecutionIntent` should be created
  **And** the associated `Task` status must be set to "failed"

## 5. Financial Guardrails

### Scenario: Blocking Task on Budget Depletion
  **Given** a campaign has reached 99.5% of its $5000 budget
  **When** a new Worker task requests a $10 action
  **Then** the Planner should block the task
  **And** the campaign status should be set to "paused-budget-exceeded"

## Performance Targets & Thresholds

| Feature | Metric | Threshold |
| :--- | :--- | :--- |
| Planning | Time to generate plan | < 30 seconds |
| Judging | Judge correlation with Human | > 85% agreement |
| Execution | Idempotency failure rate | < 0.1% |
| Safety | False Negative (leaked toxicity) | < 0.01% |
