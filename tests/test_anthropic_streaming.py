
from unittest.mock import AsyncMock, MagicMock

import anthropic
import httpx
import pytest

from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.exceptions import (
    ProviderRateLimitError,
    ProviderConnectionError,
)
from personal_ai_assistant.capstone.models import Message, Role


def make_messages():
    return [Message(role=Role.USER, content="Hello")]


def make_stream_client(text_stream=None, enter_error=None):
    stream = MagicMock()
    stream.text_stream = text_stream

    context_manager = MagicMock()
    context_manager.__aenter__ = AsyncMock(
        return_value=stream,
        side_effect=enter_error,
    )
    context_manager.__aexit__ = AsyncMock(
        return_value=False
    )

    client = MagicMock()
    client.messages.stream.return_value = context_manager

    return client


@pytest.mark.asyncio
async def test_stream_returns_text_chunks():

    async def fake_text_stream():
        yield "Hello"
        yield " "
        yield "world!"

    client = make_stream_client(
        text_stream=fake_text_stream()
    )

    provider = AnthropicProvider(client=client)

    chunks = [
        chunk
        async for chunk in provider.stream(make_messages())
    ]

    assert chunks == ["Hello", " ", "world!"]
    client.messages.stream.assert_called_once()


@pytest.mark.asyncio
async def test_stream_rate_limit_error():
    request = httpx.Request(
        "POST",
        "https://api.anthropic.com/v1/messages",
    )

    response = httpx.Response(
        429,
        request=request,
    )

    sdk_error = anthropic.RateLimitError(
        "Rate limit exceeded",
        response=response,
        body=None,
    )

    client = make_stream_client(
        enter_error=sdk_error
    )

    provider = AnthropicProvider(client=client)

    with pytest.raises(ProviderRateLimitError) as exc:
        async for _ in provider.stream(make_messages()):
            pass

    assert exc.value.__cause__ is sdk_error


@pytest.mark.asyncio
async def test_stream_connection_error_after_chunk():
    request = httpx.Request(
        "POST",
        "https://api.anthropic.com/v1/messages",
    )

    sdk_error = anthropic.APIConnectionError(
        request=request
    )

    async def failing_text_stream():
        yield "Partial response"
        raise sdk_error

    client = make_stream_client(
        text_stream=failing_text_stream()
    )

    provider = AnthropicProvider(client=client)

    chunks = []

    with pytest.raises(ProviderConnectionError) as exc:
        async for chunk in provider.stream(make_messages()):
            chunks.append(chunk)

    assert chunks == ["Partial response"]
    assert exc.value.__cause__ is sdk_error
    
