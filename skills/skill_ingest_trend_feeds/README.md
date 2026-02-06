# Skill: `skill_ingest_trend_feeds`

## Purpose
Fetch and normalize **trend, news, and mention feeds** relevant to a campaign goal so that planners and workers operate on up-to-date context.

## Primary Callers
- Planner (during goal → plan and re-planning).
- Worker (when refreshing context for content generation).

## Input Contract (`TrendIngestRequest`)

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

## Output Contract (`TrendIngestResponse`)

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

## Usage Notes
- Aligns with the `TrendFeedItem` entity from the technical spec.
- Planners should record `trendId` references in plan context for auditability.
- The skill **does not** modify state; it only reads external feeds and normalizes them.
