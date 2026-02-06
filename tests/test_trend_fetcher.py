import inspect
from typing import Any, get_args, get_origin, get_type_hints


def test_trend_ingest_request_contract():
    """
    The trend ingest request must follow the TrendIngestRequest contract
    from skills/README.md:

    {
      "requestId": "uuid",
      "goal": { "id": "goal-uuid", "title": "..." },
      "filters": {
        "tags": [string],
        "sources": [string],
        "lookbackHours": int
      },
      "trace": { "planId": "plan-uuid?", "taskId": "task-uuid?" }
    }
    """
    import trend_fetcher  # import inside test for TDD "empty slot"

    assert hasattr(trend_fetcher, "TrendIngestRequest")

    request_type = trend_fetcher.TrendIngestRequest
    assert issubclass(
        request_type, dict
    ), "TrendIngestRequest should be a TypedDict or dict-like type"

    hints = get_type_hints(request_type)

    # Required top-level fields
    assert hints.get("requestId") is str
    assert "goal" in hints, "goal field must be present"
    assert "filters" in hints, "filters field must be present"
    assert "trace" in hints, "trace field must be present"


def test_trend_feed_item_contract():
    """
    A single TrendFeedItem must match the technical spec:

    {
      "trendId": "trend-uuid",
      "source": "news|social|mentions|...",
      "tag": "string",
      "score": float,
      "capturedAt": "RFC3339 timestamp",
      "payload": {}
    }
    """
    import trend_fetcher

    assert hasattr(trend_fetcher, "TrendFeedItem")

    item_type = trend_fetcher.TrendFeedItem
    assert issubclass(
        item_type, dict
    ), "TrendFeedItem should be a TypedDict or dict-like type"

    hints = get_type_hints(item_type)

    assert hints.get("trendId") is str
    assert hints.get("source") is str
    assert hints.get("tag") is str
    assert hints.get("score") in (float, int)
    assert hints.get("capturedAt") is str

    payload_hint = hints.get("payload")
    assert payload_hint is not None, "payload field must be present"
    origin = get_origin(payload_hint)
    args = get_args(payload_hint)

    # payload should be a mapping/dict-like of arbitrary JSON
    assert origin is dict or issubclass(
        payload_hint, dict
    ), "payload should be a dict-like type"
    if args:
        key_type, value_type = args
        assert key_type in (str, Any)
        assert value_type is Any or value_type is object


def test_trend_ingest_response_contract():
    """
    TrendIngestResponse must align with skills/README.md:

    {
      "requestId": "uuid",
      "goalId": "goal-uuid",
      "items": [TrendFeedItem],
      "capturedAt": "RFC3339 timestamp"
    }
    """
    import trend_fetcher

    assert hasattr(trend_fetcher, "TrendIngestResponse")
    assert hasattr(trend_fetcher, "TrendFeedItem")

    response_type = trend_fetcher.TrendIngestResponse
    item_type = trend_fetcher.TrendFeedItem

    assert issubclass(
        response_type, dict
    ), "TrendIngestResponse should be a TypedDict or dict-like type"

    hints = get_type_hints(response_type)

    assert hints.get("requestId") is str
    assert hints.get("goalId") is str
    assert hints.get("capturedAt") is str

    items_hint = hints.get("items")
    assert items_hint is not None, "items field must be present"

    origin = get_origin(items_hint)
    args = get_args(items_hint)
    assert origin is list, "items must be a list type"
    assert args and args[0] is item_type, "items must contain TrendFeedItem elements"


def test_fetch_trends_function_signature():
    """
    trend_fetcher.fetch_trends must be the primary entry point:

    def fetch_trends(request: TrendIngestRequest) -> TrendIngestResponse
    """
    import trend_fetcher

    assert hasattr(trend_fetcher, "TrendIngestRequest")
    assert hasattr(trend_fetcher, "TrendIngestResponse")
    assert hasattr(trend_fetcher, "fetch_trends")

    func = trend_fetcher.fetch_trends
    sig = inspect.signature(func)

    params = list(sig.parameters.values())
    assert len(params) == 1, "fetch_trends must accept exactly one parameter"
    assert params[0].name == "request"
    assert (
        params[0].annotation is trend_fetcher.TrendIngestRequest
    ), "request must be annotated as TrendIngestRequest"

    assert (
        sig.return_annotation is trend_fetcher.TrendIngestResponse
    ), "return type must be TrendIngestResponse"

