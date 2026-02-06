# UI & UX Specification

This document defines the screens, flows, and component mappings for Project Chimera's management interface.

## Core Screens

### 1. Command Center (Dashboard)
- **Purpose**: High-level observability of active campaigns, system health, and financial status.
- **Key Metrics**:
  - Total Active Plans
  - Aggregated Spend vs. Budget
  - Average Judge Confidence
  - Workers Throughput (Tasks/hr)
- **UI Elements**:
  - Real-time activity feed (streaming Trace/Audit Log).
  - Gauge charts for budget consumption.
  - System status indicators (Planner, Worker Swarm, Judge).

### 2. Campaign Planner (Goal Intake)
- **Purpose**: Allow Human Orchestrators to submit new goals.
- **Form Fields**:
  - `Title`: String
  - `Goal Description`: Text area
  - `Constraints`:
    - `Budget USD`: Number
    - `Deadline`: Datetime picker
    - `Persona`: Dropdown (mapped to `specs/personas.md`)
- **Mapping**: Submits to `POST /api/v1/goals` using the **Goal → Plan Request** contract.

### 3. Review Queue (Human-in-the-Loop)
- **Purpose**: Interface for Human Reviewers to approve/edit/reject items escalated by the Judge.
- **Columns/Cards**:
  - `Asset Preview`: Text/Image/Video display.
  - `Rationale`: Why did it escalate? (e.g., "Sensitive Topic: Finance").
  - `Confidence Score`: Percentage gauge.
  - `Evidence`: Links to source data or safety check results.
- **Actions**:
  - `Approve`: Closes the review, marks as approved.
  - `Edit & Approve`: Open a text editor for the content field, then approve.
  - `Reject`: Permanently stop this action.
- **Mapping**: Interacts with `GET /api/v1/reviews` and `PATCH /api/v1/reviews/{reviewId}`.

### 4. Audit Trail (Log Explorer)
- **Purpose**: Deep-dive into specific task chains for debugging and compliance.
- **Features**:
  - Filter by `planId`, `taskId`, or `actor`.
  - JSON view for every event (Plan versioning, Worker output, Judge evaluation).
- **Mapping**: Queries the `Trace/Audit Log` entities.

## User Flows

### Flow A: New Campaign Launch
1. Orchestrator opens **Campaign Planner**.
2. Fills details and clicks "Submit".
3. UI sends `Goal Request`.
4. UI transitions to **Command Center**, showing a new entry in "Active Plans".
5. Clicking the entry opens a detailed **Plan View** showing the generated task graph.

### Flow B: Escalated Review Handling
1. Reviewer receives a notification of "Pending Review".
2. Reviewer opens **Review Queue**.
3. UI loads `HumanReview` entities with `status=pending`.
4. Reviewer clicks "Edit & Approve" on a video caption.
5. UI updates the `approvedPayload` and calls the API.
6. The Plan proceeds to **Execution Layer**.

## Component Structure & Mapping

| Component | UI Library / Pattern | Technical Map (Data Entity) |
| :--- | :--- | :--- |
| `GoalForm` | Reactive Form | `Goal` entity |
| `TaskGraph` | Node-link diagram (e.g., React Flow) | `Plan.tasks[]` array |
| `AssetPreview` | Media gallery / Markdown renderer | `AgentOutput` & `MediaAsset` |
| `JudgeEvaluationCard` | Logic list with confidence badges | `Evaluation` entity |
| `HumanReviewPanel` | Side drawer / Modal | `HumanReview` entity |
| `LogTable` | Paginated data grid with JSON trees | `Trace/Audit Log` |

## Backend Contract Mapping

| Screen Action | Endpoint | Method | JSON Payload (TECHNICAL.md) |
| :--- | :--- | :--- | :--- |
| Submit New Goal | `/api/v1/goals` | POST | `Goal → Plan Request` |
| Get All Plans | `/api/v1/plans` | GET | `[Plan Entity]` |
| Get Review Queue | `/api/v1/reviews` | GET | `[HumanReview Entity]` |
| Resolve Review | `/api/v1/reviews/{id}` | PATCH | `Human Response` |
| Stream Logs | `/api/v1/logs/stream` | WS/SSE | `Trace/Audit Log` |
