import pytest

from unittest.mock import AsyncMock, Mock
from personal_ai_assistant.capstone.anthropic_provider import AnthropicProvider
from personal_ai_assistant.capstone.models import (
    AssistantResponse,
    Message,
    Role,
)


@pytest.fixture
def mock_client():
    client = Mock()
    client.messages.create = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_generate_returns_assistant_response(mock_client):
    # Arrange
    mock_response = Mock()
    mock_response.model = "claude-haiku-4-5"

    text_block = Mock()
    text_block.type = "text"
    text_block.text = "Hello from Claude!"

    mock_response.content = [text_block]
    mock_client.messages.create.return_value = mock_response

    provider = AnthropicProvider(client=mock_client)

    # Act
    result = await provider.generate([
        Message(role=Role.USER, content="Hello")
    ])

    # Assert
    assert isinstance(result, AssistantResponse)
    assert result.message.role == Role.ASSISTANT
    assert result.message.content == "Hello from Claude!"
    assert result.model_name == "claude-haiku-4-5"

    mock_client.messages.create.assert_awaited_once_with(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello"}
        ],
    )


@pytest.mark.asyncio
async def test_generate_extracts_system_message(mock_client):
    # Arrange
    mock_response = Mock()
    mock_response.model = "claude-haiku-4-5"
    mock_response.content = [
        Mock(type="text", text="Python is a programming language.")
    ]
    mock_client.messages.create.return_value = mock_response

    provider = AnthropicProvider(client=mock_client)

    # Act
    await provider.generate([
        Message(Role.SYSTEM, "You are a Python tutor."),
        Message(Role.USER, "What is Python?"),
    ])

    # Assert
    mock_client.messages.create.assert_awaited_once_with(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="You are a Python tutor.",
        messages=[
            {"role": "user", "content": "What is Python?"}
        ],
    )
