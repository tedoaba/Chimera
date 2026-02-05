## Chimera Runtime Skills

This directory defines **runtime skills** that Chimera agents invoke via tools/MCP during execution.  
Each skill is **atomic, self-contained**, and has an explicit **Input/Output contract** so that planners, workers, and judges can use them reliably.

Skills are **not implementations**; they are **interfaces** that runtime infrastructure fulfills.

---

## Design Principles

- **Mission-critical only**: Skills here directly support core flows from the functional and technical specs (goal intake, trend ingestion, content creation, evaluation, and execution).  
- **Explicit contracts**: Every skill declares a strict JSON-like input and output shape.  
- **Role clarity**: Each skill notes which agent roles (Planner, Worker, Judge, Execution Layer) are expected to call it.  
- **Composable, not monolithic**: Skills do one thing well and can be composed into larger plans.

Each skill lives in its own subdirectory:

- `skills/skill_<name>/README.md`

See below for the initial set of core skills.

---

## Skill: `skill_ingest_trend_feeds`

- **Purpose**:  
  Fetch and normalize **trend, news, and mention feeds** relevant to a campaign goal so that planners and workers operate on up-to-date context.

- **Primary Callers**:  
  - Planner (during goal → plan and re-planning).  
  - Worker (when refreshing context for content generation).

- **Input Contract** (`TrendIngestRequest`):

```json
{
  "requestId": "uuid",
  "goal": {
    "id": "goal-uuid",
    "title": "Increase engagement for product X"
  },
  "filters": {
    "tags": ["productX", "launch"],
    "sources": ["news", "social", "mentions"],
    "lookbackHours": 24
  },
  "trace": {
    "planId": "plan-uuid?",
    "taskId": "task-uuid?"
  }
}
```

- **Output Contract** (`TrendIngestResponse`):

```json
{
  "requestId": "uuid",
  "goalId": "goal-uuid",
  "items": [
    {
      "trendId": "trend-uuid",
      "source": "news",
      "tag": "productX",
      "score": 0.82,
      "capturedAt": "2026-02-05T10:00:00Z",
      "payload": {}
    }
  ],
  "capturedAt": "2026-02-05T10:01:00Z"
}
```

- **Usage Notes**:  
  - Aligns with the `TrendFeedItem` entity from the technical spec.  
  - Planners should record `trendId` references in plan context for auditability.  
  - The skill **does not** modify state; it only reads external feeds and normalizes them.

---

## Skill: `skill_generate_media_asset`

- **Purpose**:  
  Generate **text, image, or video assets** from a task brief and persona, producing a structured `AgentOutput` that downstream judges and executors can consume.

- **Primary Callers**:  
  - Worker agents executing content-creation tasks (`generate_video_caption`, `write_tweet_thread`, etc.).

- **Input Contract** (`MediaGenerationRequest`):

```json
{
  "taskId": "task-uuid",
  "planId": "plan-uuid",
  "type": "text|image|video",
  "brief": {
    "prompt": "30s launch teaser",
    "persona": "brand-safe upbeat",
    "goalId": "goal-uuid",
    "trendRefs": ["trend-uuid-1", "trend-uuid-2"],
    "mediaContext": [
      { "mediaId": "vid-123", "url": "s3://...", "role": "source" }
    ]
  },
  "constraints": {
    "budgetUsd": 50,
    "maxLatencySec": 120,
    "length": {
      "maxChars": 280,
      "maxDurationSec": 30
    }
  },
  "trace": {
    "requestId": "uuid"
  }
}
```

- **Output Contract** (`MediaGenerationResponse`):

```json
{
  "taskId": "task-uuid",
  "planId": "plan-uuid",
  "output": {
    "type": "text|image|video",
    "content": "Ready for launch? Watch now.",
    "mediaRefs": ["vid-123", "thumb-456"]
  },
  "evidence": {
    "sources": [{ "url": "https://...", "type": "link" }],
    "safetyChecks": []
  },
  "confidence": 0.7,
  "costUsd": 1.2,
  "startedAt": "2026-02-05T10:00:00Z",
  "endedAt": "2026-02-05T10:00:10Z"
}
```

- **Usage Notes**:  
  - Mirrors the `Task Assignment` and `AgentOutput` patterns from the technical spec.  
  - Workers must not auto-publish; this skill only creates candidate assets.  
  - Judges and human reviewers consume the output via separate flows.

---

## Skill: `skill_execute_publish_intent`

- **Purpose**:  
  Take a validated **ExecutionIntent** (post/reply/upload_video/transfer_funds) and execute it against external platforms, honoring budgets and idempotency requirements.

- **Primary Callers**:  
  - Planner or dedicated Execution Layer, **after** Judge or human approval.

- **Input Contract** (`ExecutionIntentRequest`):

```json
{
  "intent": {
    "intentId": "exec-uuid",
    "taskId": "task-uuid",
    "action": "post|reply|upload_video|transfer_funds",
    "target": { "platform": "youtube", "channelId": "abc123" },
    "payload": {
      "content": "text or media ref",
      "mediaRefs": ["vid-123"]
    },
    "budgetUsd": 20,
    "approvedBy": "judge|human",
    "idempotencyKey": "exec-uuid",
    "trace": {
      "planId": "plan-uuid",
      "reviewId": "rev-uuid?"
    }
  },
  "environment": "sandbox|staging|production"
}
```

- **Output Contract** (`ExecutionIntentResponse`):

```json
{
  "intentId": "exec-uuid",
  "status": "accepted|executed|failed",
  "externalRef": "platform-post-id",
  "error": {
    "code": "STRING_UPPER_SNAKE",
    "message": "human-readable",
    "details": {},
    "retryable": true,
    "backoffSec": 30
  }
}
```

- **Usage Notes**:  
  - Conforms to the `Execution Intent` contract in the technical spec.  
  - Must enforce idempotency on `idempotencyKey` to avoid duplicate posts/payments.  
  - In non-production environments, this skill should route to a sandbox implementation.

---

## Adding New Skills

When defining additional skills:

- **Name**: Use `skill_<verb>_<object>` (e.g., `skill_evaluate_content_safety`).  
- **Docs**: Add `skills/skill_<name>/README.md` with:
  - Purpose and primary callers.  
  - Input/Output JSON examples with required vs. optional fields.  
  - Error behaviors and retry guidance.  
- **Alignment**: Tie each skill back to entities and flows in the functional and technical specs so that planners can compose them safely.

