import pytest
from unittest.mock import AsyncMock

from personal_ai_assistant.capstone.models import (
    Message,
    Role,
    AssistantResponse,
)
from personal_ai_assistant.capstone.service import AssistantService


@pytest.mark.asyncio
async def test_system_prompt_is_sent_but_not_saved():
    # Arrange
    system_prompt = "You are a Python tutor."

    user_message = Message(
        role=Role.USER,
        content="Explain decorators.",
    )

    assistant_message = Message(
        role=Role.ASSISTANT,
        content="Decorators wrap functions.",
    )

    provider = AsyncMock()
    provider.generate.return_value = AssistantResponse(
        message=assistant_message,
        model_name="mock-model",
    )

    storage = AsyncMock()
    storage.load.return_value = []

    service = AssistantService(
        provider=provider,
        storage=storage,
        system_prompt=system_prompt,
    )

    # Act
    await service.send_message(user_message.content)

    # Assert: system prompt is sent to provider
    provider.generate.assert_awaited_once_with([
        Message(
            role=Role.SYSTEM,
            content=system_prompt,
        ),
        user_message,
    ])

    # Assert: system prompt is NOT persisted
    storage.save.assert_awaited_once_with([
        user_message,
        assistant_message,
    ])

    @pytest.mark.asyncio
    async def test_streaming_system_prompt_is_not_saved():
        # Arrange
        system_prompt = "You are a Python tutor."

        user_message = Message(
            role=Role.USER,
            content="Explain async/await.",
        )

        received_messages = []

        async def fake_stream(messages):
            received_messages.extend(messages)
            yield "Async "
            yield "allows concurrency."

        provider = AsyncMock()
        provider.stream.side_effect = fake_stream

        storage = AsyncMock()
        storage.load.return_value = []

        service = AssistantService(
            provider=provider,
            storage=storage,
            system_prompt=system_prompt,
        )

        # Act
        chunks = []

        async for chunk in service.stream_message(
            user_message.content
        ):
            chunks.append(chunk)

        # Assert: streamed text is correct
        assert "".join(chunks) == "Async allows concurrency."

        # Assert: system prompt is NOT persisted
        storage.save.assert_awaited_once_with([
            user_message,
            Message(
                role=Role.ASSISTANT,
                content="Async allows concurrency.",
            ),
        ])

        assert received_messages == [
            Message(
                role=Role.SYSTEM,
                content=system_prompt,
            ),
            user_message,
        ]   