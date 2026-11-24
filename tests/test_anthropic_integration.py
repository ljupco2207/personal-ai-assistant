import pytest

from unittest.mock import AsyncMock, Mock
from personal_ai_assistant.capstone.anthropic_provider import AnthropicProvider
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.storage import JSONConversationStorage
from personal_ai_assistant.capstone.models import Role


@pytest.mark.asyncio
async def test_assistant_remembers_conversation(tmp_path):
    # ARRANGE: Mock only the external Anthropic API
    client = Mock()
    client.messages.create = AsyncMock()

    def make_response(text):
        response = Mock()
        response.model = "claude-haiku-4-5"
        response.content = [
            Mock(type="text", text=text)
        ]
        return response

    client.messages.create.side_effect = [
        make_response("Hello Alex!"),
        make_response("Your name is Alex."),
    ]

    # Use real application components
    provider = AnthropicProvider(client=client)

    storage = JSONConversationStorage(
        tmp_path / "conversation.json"
    )

    service = AssistantService(
        provider=provider,
        storage=storage,
    )

    # ACT: First message
    first_response = await service.send_message(
        "Hello! My name is Alex."
    )

    assert first_response.message.content == "Hello Alex!"

    # ACT: Second message
    second_response = await service.send_message(
        "What is my name?"
    )

    # ASSERT: Verify responses
    assert second_response.message.content == "Your name is Alex."

    # Verify that two API requests were made
    assert client.messages.create.await_count == 2

    # Verify conversation was saved
    history = await storage.load()

    assert len(history) == 4
    assert history[0].role == Role.USER
    assert history[1].role == Role.ASSISTANT
    assert history[2].role == Role.USER
    assert history[3].role == Role.ASSISTANT

    # Verify second request included previous messages
    second_call = client.messages.create.await_args_list[1]

    assert second_call.kwargs["messages"] == [
        {
            "role": "user",
            "content": "Hello! My name is Alex.",
        },
        {
            "role": "assistant",
            "content": "Hello Alex!",
        },
        {
            "role": "user",
            "content": "What is my name?",
        },
    ]
