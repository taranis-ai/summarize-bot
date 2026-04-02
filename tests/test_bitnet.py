import httpx
import pytest

from summarize_bot.bitnet import Bitnet
from summarize_bot.config import Config

REAL_ASYNC_CLIENT = httpx.AsyncClient


@pytest.mark.asyncio
async def test_bitnet_returns_short_text_unchanged():
    model = Bitnet()
    text = "short text"

    result = await model.predict(text)

    assert result == {"summary": text}


@pytest.mark.asyncio
async def test_bitnet_extracts_summary_from_chat_completions(monkeypatch):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["json"] = request.read().decode("utf-8")
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "This is the generated summary.",
                        }
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)

    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            self._client = REAL_ASYNC_CLIENT(transport=transport, timeout=kwargs.get("timeout"))

        async def __aenter__(self):
            return self._client

        async def __aexit__(self, exc_type, exc, tb):
            await self._client.aclose()

    monkeypatch.setattr("summarize_bot.bitnet.httpx.AsyncClient", MockAsyncClient)

    model = Bitnet()
    text = "x" * Config.MAX_LEN

    result = await model.predict(text)

    assert result == {"summary": "This is the generated summary."}
    assert captured["url"] == f"{Config.BITNET_SERVER_URL}/v1/chat/completions"
    assert "\"messages\"" in captured["json"]


@pytest.mark.asyncio
async def test_bitnet_raises_for_missing_choices():
    model = Bitnet()

    with pytest.raises(ValueError, match="choices"):
        model._extract_summary({})


@pytest.mark.asyncio
async def test_bitnet_raises_for_empty_content():
    model = Bitnet()

    with pytest.raises(ValueError, match="empty summary"):
        model._extract_summary({"choices": [{"message": {"content": "   "}}]})


@pytest.mark.asyncio
async def test_bitnet_propagates_http_errors(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "upstream failed"})

    transport = httpx.MockTransport(handler)

    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            self._client = REAL_ASYNC_CLIENT(transport=transport, timeout=kwargs.get("timeout"))

        async def __aenter__(self):
            return self._client

        async def __aexit__(self, exc_type, exc, tb):
            await self._client.aclose()

    monkeypatch.setattr("summarize_bot.bitnet.httpx.AsyncClient", MockAsyncClient)

    model = Bitnet()
    text = "x" * Config.MAX_LEN

    with pytest.raises(httpx.HTTPStatusError):
        await model.predict(text)
