import pytest

from unittest.mock import AsyncMock
from personal_ai_assistant.capstone.models import (
    Message,
    Role,
    AssistantResponse
)
from personal_ai_assistant.capstone.service import AssistantService

@pytest.mark.asyncio
async def test_send_message_success():
    # Arrange
    provider = AsyncMock()
    storage = AsyncMock()

    storage.load.return_value = []

    assistant_message = Message(
        role=Role.ASSISTANT,
        content="Hello! How can I help?"
    )

    expected_response = AssistantResponse(
        message=assistant_message,
        model_name="mock-model"
    )

    provider.generate.return_value = expected_response

    service = AssistantService(
        provider=provider,
        storage=storage
    )

    # Act
    response = await service.send_message("Hello")

    # Assert
    assert response == expected_response

    storage.load.assert_awaited_once()

    provider.generate.assert_awaited_once_with([
        Message(role=Role.USER, content="Hello")
    ])

    storage.save.assert_awaited_once_with([
        Message(role=Role.USER, content="Hello"),
        assistant_message
    ])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "content",
    ["", "   ", "\n\t"]
)
async def test_send_message_empty(content: str):
    # Arrange
    provider = AsyncMock()
    storage = AsyncMock()

    service = AssistantService(
        provider=provider,
        storage=storage
    )

    # Act & Assert
    with pytest.raises(
        ValueError,
        match="Message cannot be empty"
    ):
        await service.send_message(content)

    storage.load.assert_not_awaited()
    provider.generate.assert_not_awaited()
    storage.save.assert_not_awaited()



@pytest.mark.asyncio
async def test_send_message_with_history():
    # Arrange
    provider = AsyncMock()
    storage = AsyncMock()

    history = [
        Message(role=Role.USER, content="Hi"),
        Message(role=Role.ASSISTANT, content="Hello!")
    ]

    storage.load.return_value = history

    assistant_message = Message(
        role=Role.ASSISTANT,
        content="Python async/await allows concurrent I/O."
    )

    provider.generate.return_value = AssistantResponse(
        message=assistant_message,
        model_name="mock-model"
    )

    service = AssistantService(provider, storage)

    # Act
    await service.send_message("Explain async/await")

    # Assert
    expected_messages = [
        *history,
        Message(
            role=Role.USER,
            content="Explain async/await"
        )
    ]

    provider.generate.assert_awaited_once_with(
        expected_messages
    )

    storage.save.assert_awaited_once_with([
        *expected_messages,
        assistant_message
    ])
