import pytest

from dataclasses import FrozenInstanceError
from personal_ai_assistant.capstone.models import (
    Message,
    Role,
    AssistantResponse
)

def test_message_creation():
    # Arrange
    message = Message(
        role=Role.USER,
        content="Hello"
    )

    # Assert
    assert message.role == Role.USER
    assert message.content == "Hello"


def test_message_is_immutable():
    # Arrange
    message = Message(
        role=Role.USER,
        content="Hello"
    )

    # Act & Assert
    with pytest.raises(FrozenInstanceError):
        message.content = "Changed"


def test_assistant_response_creation():
    # Arrange
    message = Message(
        role=Role.ASSISTANT,
        content="Hello! How can I help?"
    )

    response = AssistantResponse(
        message=message,
        model_name="mock-model"
    )

    # Assert
    assert response.message == message
    assert response.message.role == Role.ASSISTANT
    assert response.model_name == "mock-model"


def test_assistant_response_is_immutable():
    # Arrange
    response = AssistantResponse(
        message=Message(
            role=Role.ASSISTANT,
            content="Hello!"
        ),
        model_name="mock-model"
    )

    # Act & Assert
    with pytest.raises(FrozenInstanceError):
        response.model_name = "another-model"


@pytest.mark.parametrize(
    "role, expected_value",
    [
        (Role.USER, "user"),
        (Role.ASSISTANT, "assistant"),
        (Role.SYSTEM, "system"),
    ]
)
def test_role_values(role: Role, expected_value: str):
    assert role.value == expected_value
