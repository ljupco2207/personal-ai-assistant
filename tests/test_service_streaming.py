
from unittest.mock import AsyncMock, Mock

import pytest

from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.models import Message, Role
from personal_ai_assistant.capstone.exceptions import (
    ProviderError,
    ProviderRateLimitError,
)


@pytest.mark.asyncio
async def test_stream_message_saves_conversation():

    async def fake_stream(messages):
        yield "Hello"
        yield " "
        yield "world!"

    provider = Mock()
    provider.stream.side_effect = fake_stream

    storage = Mock()
    storage.load = AsyncMock(return_value=[])
    storage.save = AsyncMock()

    service = AssistantService(provider, storage)

    chunks = [
        chunk
        async for chunk in service.stream_message("Hi")
    ]

    assert chunks == ["Hello", " ", "world!"]

    storage.save.assert_awaited_once_with([
        Message(role=Role.USER, content="Hi"),
        Message(role=Role.ASSISTANT, content="Hello world!"),
    ])


@pytest.mark.asyncio
async def test_stream_message_preserves_provider_error():

    async def failing_stream(messages):
        raise ProviderRateLimitError("Rate limit exceeded")
        yield ""  # Makes this an async generator

    provider = Mock()
    provider.stream.side_effect = failing_stream

    storage = Mock()
    storage.load = AsyncMock(return_value=[])
    storage.save = AsyncMock()

    service = AssistantService(provider, storage)

    with pytest.raises(ProviderRateLimitError):
        async for _ in service.stream_message("Hello"):
            pass

    storage.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_stream_message_wraps_unexpected_error():

    async def failing_stream(messages):
        yield "Partial response"
        raise RuntimeError("Connection interrupted")

    provider = Mock()
    provider.stream.side_effect = failing_stream

    storage = Mock()
    storage.load = AsyncMock(return_value=[])
    storage.save = AsyncMock()

    service = AssistantService(provider, storage)

    chunks = []

    with pytest.raises(ProviderError) as exc:
        async for chunk in service.stream_message("Hello"):
            chunks.append(chunk)

    assert chunks == ["Partial response"]
    assert isinstance(exc.value.__cause__, RuntimeError)
    storage.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_stream_early_close_does_not_save():

    async def fake_stream(messages):
        yield "First chunk"
        yield "Second chunk"

    provider = Mock()
    provider.stream.side_effect = fake_stream

    storage = Mock()
    storage.load = AsyncMock(return_value=[])
    storage.save = AsyncMock()

    service = AssistantService(
        provider=provider,
        storage=storage,
    )

    stream = service.stream_message("Hello")

    # Receive only the first chunk
    first_chunk = await anext(stream)

    assert first_chunk == "First chunk"

    # Simulate the user pressing "Stop Generating"
    await stream.aclose()

    # Incomplete response must NOT be saved
    storage.save.assert_not_awaited()

