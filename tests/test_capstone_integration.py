import pytest

from unittest.mock import AsyncMock, call
from personal_ai_assistant.capstone.models import (
    Message,
    Role,
    AssistantResponse,
)
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.storage import JSONConversationStorage


@pytest.mark.asyncio
async def test_assistant_persists_conversation(tmp_path):
    file_path = tmp_path / "conversation.json"
    storage = JSONConversationStorage(file_path)
    provider = AsyncMock()

    reply = Message(
        role=Role.ASSISTANT,
        content="Hello!"
    )

    provider.generate.return_value = AssistantResponse(
        message=reply,
        model_name="mock-model"
    )

    service = AssistantService(provider, storage)

    response = await service.send_message("Hi")

    assert response.message == reply
    assert file_path.exists()

    assert await storage.load() == [
        Message(role=Role.USER, content="Hi"),
        reply
    ]


@pytest.mark.asyncio
async def test_assistant_remembers_previous_messages(tmp_path):
    storage = JSONConversationStorage(
        tmp_path / "conversation.json"
    )
    provider = AsyncMock()

    first_reply = Message(
        role=Role.ASSISTANT,
        content="Hi!"
    )
    second_reply = Message(
        role=Role.ASSISTANT,
        content="Python is a programming language."
    )

    provider.generate.side_effect = [
        AssistantResponse(first_reply, "mock-model"),
        AssistantResponse(second_reply, "mock-model"),
    ]

    service = AssistantService(provider, storage)

    await service.send_message("Hello")
    await service.send_message("What is Python?")

    first_user = Message(Role.USER, "Hello")
    second_user = Message(Role.USER, "What is Python?")

    provider.generate.assert_has_awaits([
        call([first_user]),
        call([first_user, first_reply, second_user]),
    ])

    assert provider.generate.await_count == 2

    assert await storage.load() == [
        first_user,
        first_reply,
        second_user,
        second_reply,
    ]
