import pytest
import json

from personal_ai_assistant.capstone.storage import JSONConversationStorage
from personal_ai_assistant.capstone.exceptions import StorageError
from personal_ai_assistant.capstone.models import (
    Message,
    Role
)
from personal_ai_assistant.capstone.storage import (
    JSONConversationStorage
)

@pytest.mark.asyncio
async def test_save_and_load_messages(tmp_path):
    # Arrange
    file_path = tmp_path / "conversation.json"

    storage = JSONConversationStorage(file_path)

    messages = [
        Message(
            role=Role.USER,
            content="Hello"
        ),
        Message(
            role=Role.ASSISTANT,
            content="Hi! How can I help?"
        )
    ]

    # Act
    await storage.save(messages)

    loaded_messages = await storage.load()

    # Assert
    assert file_path.exists()
    assert loaded_messages == messages


@pytest.mark.asyncio
async def test_load_corrupted_json(tmp_path):
    # Arrange
    file_path = tmp_path / "conversation.json"

    file_path.write_text(
        "invalid json",
        encoding="utf-8"
    )

    storage = JSONConversationStorage(file_path)

    # Act & Assert
    with pytest.raises(
        StorageError,
        match="Failed to load conversation history"
    ) as error_info:
        await storage.load()

    assert isinstance(
        error_info.value.__cause__,
        json.JSONDecodeError
    )



@pytest.mark.asyncio
async def test_save_failure(tmp_path, monkeypatch):
    # Arrange
    file_path = tmp_path / "conversation.json"
    storage = JSONConversationStorage(file_path)

    messages = [
        Message(role=Role.USER, content="Hello")
    ]

    def failing_write(data):
        raise OSError("Disk write failed")

    monkeypatch.setattr(
        storage,
        "_write_json",
        failing_write
    )

    # Act & Assert
    with pytest.raises(
        StorageError,
        match="Failed to save conversation history"
    ) as error_info:
        await storage.save(messages)

    assert isinstance(
        error_info.value.__cause__,
        OSError
    )
