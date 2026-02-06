# Skill: `skill_execute_publish_intent`

## Purpose
Take a validated **ExecutionIntent** (post/reply/upload_video/transfer_funds) and execute it against external platforms, honoring budgets and idempotency requirements.

## Primary Callers
- Planner or dedicated Execution Layer, **after** Judge or human approval.

## Input Contract (`ExecutionIntentRequest`)

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

## Output Contract (`ExecutionIntentResponse`)

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

## Usage Notes
- Conforms to the `Execution Intent` contract in the technical spec.
- Must enforce idempotency on `idempotencyKey` to avoid duplicate posts/payments.
- In non-production environments, this skill should route to a sandbox implementation.
