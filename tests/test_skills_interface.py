from typing import Any, Dict, List, get_args, get_origin, get_type_hints
import inspect


def _assert_list_of(inner_type, annotated_type, message: str) -> None:
    origin = get_origin(annotated_type)
    args = get_args(annotated_type)
    assert origin in (list, List), message
    assert args and args[0] is inner_type, message


def test_skill_ingest_trend_feeds_run_signature_and_contract():
    """
    skills/skill_ingest_trend_feeds must expose:

    - TrendIngestRequest type with required fields:
      requestId: str
      goal: dict-like
      filters: dict-like
      trace: dict-like
    - TrendIngestResponse type with:
      requestId: str
      goalId: str
      items: List[TrendFeedItem]
      capturedAt: str
    - TrendFeedItem aligned with technical TrendFeedItem entity.
    - run(request: TrendIngestRequest) -> TrendIngestResponse
    """
    from skills import skill_ingest_trend_feeds as skill  # noqa: WPS433

    # Types must exist
    assert hasattr(skill, "TrendIngestRequest")
    assert hasattr(skill, "TrendIngestResponse")
    assert hasattr(skill, "TrendFeedItem")

    request_type = skill.TrendIngestRequest
    response_type = skill.TrendIngestResponse
    item_type = skill.TrendFeedItem

    assert issubclass(request_type, dict)
    assert issubclass(response_type, dict)
    assert issubclass(item_type, dict)

    # Request contract (top-level)
    req_hints = get_type_hints(request_type)
    assert req_hints.get("requestId") is str
    assert "goal" in req_hints
    assert "filters" in req_hints
    assert "trace" in req_hints

    # Item contract (nested TrendFeedItem)
    item_hints = get_type_hints(item_type)
    assert item_hints.get("trendId") is str
    assert item_hints.get("source") is str
    assert item_hints.get("tag") is str
    assert item_hints.get("score") in (float, int)
    assert item_hints.get("capturedAt") is str
    payload_hint = item_hints.get("payload")
    assert payload_hint is not None
    origin = get_origin(payload_hint)
    args = get_args(payload_hint)
    assert origin in (dict, Dict) or issubclass(payload_hint, dict)
    if args:
        key_type, value_type = args
        assert key_type in (str, Any)
        assert value_type is Any or value_type == object

    # Response contract
    resp_hints = get_type_hints(response_type)
    assert resp_hints.get("requestId") is str
    assert resp_hints.get("goalId") is str
    assert resp_hints.get("capturedAt") is str
    items_hint = resp_hints.get("items")
    assert items_hint is not None
    _assert_list_of(
        item_type,
        items_hint,
        "items must be List[TrendFeedItem]",
    )

    # Function signature
    assert hasattr(skill, "run")
    sig = inspect.signature(skill.run)
    params = list(sig.parameters.values())
    assert len(params) == 1, "run must accept exactly one parameter"
    assert params[0].name == "request"
    assert (
        params[0].annotation is request_type
    ), "run(request) must be annotated with TrendIngestRequest"
    assert (
        sig.return_annotation is response_type
    ), "run must return TrendIngestResponse"


def test_skill_generate_media_asset_run_signature_and_contract():
    """
    skills/skill_generate_media_asset must expose:

    - MediaGenerationRequest with required fields:
      taskId: str
      planId: str
      type: str ("text|image|video")
      brief: dict-like (prompt, persona, goalId, trendRefs, mediaContext)
      constraints: dict-like (budgetUsd, maxLatencySec, length)
      trace: dict-like (requestId)
    - MediaGenerationResponse aligned with skills/README.md.
    - run(request: MediaGenerationRequest) -> MediaGenerationResponse
    """
    from skills import skill_generate_media_asset as skill  # noqa: WPS433

    assert hasattr(skill, "MediaGenerationRequest")
    assert hasattr(skill, "MediaGenerationResponse")
    assert hasattr(skill, "run")

    request_type = skill.MediaGenerationRequest
    response_type = skill.MediaGenerationResponse

    assert issubclass(request_type, dict)
    assert issubclass(response_type, dict)

    req_hints = get_type_hints(request_type)
    assert req_hints.get("taskId") is str
    assert req_hints.get("planId") is str
    assert req_hints.get("type") is str
    assert "brief" in req_hints
    assert "constraints" in req_hints
    assert "trace" in req_hints

    # Response contract (high level mirror of AgentOutput)
    resp_hints = get_type_hints(response_type)
    assert resp_hints.get("taskId") is str
    assert resp_hints.get("planId") is str
    assert "output" in resp_hints
    assert "evidence" in resp_hints
    assert resp_hints.get("confidence") in (float, int)
    assert resp_hints.get("costUsd") in (float, int)
    assert resp_hints.get("startedAt") is str
    assert resp_hints.get("endedAt") is str

    # Function signature for run(...)
    sig = inspect.signature(skill.run)
    params = list(sig.parameters.values())
    assert len(params) == 1, "run must accept exactly one parameter"
    assert params[0].name == "request"
    assert (
        params[0].annotation is request_type
    ), "run(request) must be annotated with MediaGenerationRequest"
    assert (
        sig.return_annotation is response_type
    ), "run must return MediaGenerationResponse"


def test_skill_execute_publish_intent_run_signature_and_contract():
    """
    skills/skill_execute_publish_intent must expose:

    - ExecutionIntentRequest with:
      intent: dict-like ExecutionIntent
      environment: str ("sandbox|staging|production")
    - ExecutionIntentResponse with:
      intentId: str
      status: str ("accepted|executed|failed")
      externalRef: str (optional)
      error: dict-like matching Error Object contract (optional)
    - run(request: ExecutionIntentRequest) -> ExecutionIntentResponse
    """
    from skills import skill_execute_publish_intent as skill  # noqa: WPS433

    assert hasattr(skill, "ExecutionIntentRequest")
    assert hasattr(skill, "ExecutionIntentResponse")
    assert hasattr(skill, "run")

    request_type = skill.ExecutionIntentRequest
    response_type = skill.ExecutionIntentResponse

    assert issubclass(request_type, dict)
    assert issubclass(response_type, dict)

    req_hints = get_type_hints(request_type)
    assert "intent" in req_hints
    assert req_hints.get("environment") is str

    resp_hints = get_type_hints(response_type)
    assert resp_hints.get("intentId") is str
    assert resp_hints.get("status") is str
    # externalRef and error may be optional, but when present must be well-typed.
    assert "externalRef" in resp_hints
    assert "error" in resp_hints

    # Function signature
    sig = inspect.signature(skill.run)
    params = list(sig.parameters.values())
    assert len(params) == 1, "run must accept exactly one parameter"
    assert params[0].name == "request"
    assert (
        params[0].annotation is request_type
    ), "run(request) must be annotated with ExecutionIntentRequest"
    assert (
        sig.return_annotation is response_type
    ), "run must return ExecutionIntentResponse"

