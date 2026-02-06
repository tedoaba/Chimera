## Chimera Runtime Skills

This directory defines **runtime skills** that Chimera agents invoke via tools/MCP during execution.  
Each skill is **atomic, self-contained**, and has an explicit **Input/Output contract** so that planners, workers, and judges can use them reliably.

Skills are **not implementations**; they are **interfaces** that runtime infrastructure fulfills.

---

## Design Principles

- **Mission-critical only**: Skills directly support core flows from the functional and technical specs (goal intake, trend ingestion, content creation, evaluation, and execution).  
- **Explicit contracts**: Every skill declares a strict JSON-like input and output shape.  
- **Role clarity**: Each skill notes which agent roles (Planner, Worker, Judge, Execution Layer) are expected to call it.  
- **Composable, not monolithic**: Skills do one thing well and can be composed into larger plans.

---

## Core Skills Registry

| Skill Name | Purpose | Link |
|:---|:---|:---|
| `skill_ingest_trend_feeds` | Fetch and normalize trend/news/mention feeds | [Docs](./skill_ingest_trend_feeds/README.md) |
| `skill_generate_media_asset` | Generate text, image, or video assets | [Docs](./skill_generate_media_asset/README.md) |
| `skill_execute_publish_intent` | Execute validated intents against external platforms | [Docs](./skill_execute_publish_intent/README.md) |

---

## Adding New Skills

When defining additional skills:

1. **Name**: Use `skill_<verb>_<object>` (e.g., `skill_evaluate_content_safety`).
2. **Directory**: Create `skills/skill_<name>/`.
3. **Docs**: Add `skills/skill_<name>/README.md` with purpose, callers, contracts, and usage notes.
4. **Alignment**: Tie each skill back to entities and flows in the functional and technical specs.
