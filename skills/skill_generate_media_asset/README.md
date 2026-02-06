# Skill: `skill_generate_media_asset`

## Purpose
Generate **text, image, or video assets** from a task brief and persona, producing a structured `AgentOutput` that downstream judges and executors can consume.

## Primary Callers
- Worker agents executing content-creation tasks (`generate_video_caption`, `write_tweet_thread`, etc.).

## Input Contract (`MediaGenerationRequest`)

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

## Output Contract (`MediaGenerationResponse`)

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

## Usage Notes
- Mirrors the `Task Assignment` and `AgentOutput` patterns from the technical spec.
- Workers must not auto-publish; this skill only creates candidate assets.
- Judges and human reviewers consume the output via separate flows.
