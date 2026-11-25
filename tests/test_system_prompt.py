import pytest
from unittest.mock import AsyncMock

from personal_ai_assistant.capstone.models import (
    Message,
    Role,
    AssistantResponse,
)
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.prompts import (
    PYTHON_TUTOR_SYSTEM_PROMPT,
)


@pytest.mark.asyncio
async def test_service_passes_system_prompt_to_provider():
    # Arrange
    system_message = Message(
        role=Role.SYSTEM,
        content=PYTHON_TUTOR_SYSTEM_PROMPT,
    )

    user_message = Message(
        role=Role.USER,
        content="Explain Python decorators.",
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
    storage.load.return_value = [system_message]

    service = AssistantService(
        provider=provider,
        storage=storage,
    )

    # Act
    await service.send_message(user_message.content)

    # Assert
    provider.generate.assert_awaited_once_with(
        [system_message, user_message]
    )

    storage.save.assert_awaited_once_with(
        [system_message, user_message, assistant_message]
    )