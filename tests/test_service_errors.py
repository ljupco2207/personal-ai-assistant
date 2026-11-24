import pytest

from unittest.mock import AsyncMock
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.exceptions import (
    ProviderError,
    ProviderRateLimitError,
)


@pytest.mark.asyncio
async def test_service_preserves_provider_error():
    provider = AsyncMock()
    storage = AsyncMock()

    error = ProviderRateLimitError("Rate limit exceeded")
    provider.generate.side_effect = error
    storage.load.return_value = []

    service = AssistantService(
        provider=provider,
        storage=storage,
    )

    with pytest.raises(ProviderRateLimitError) as exc:
        await service.send_message("Hello")

    assert exc.value is error
    storage.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_service_wraps_unexpected_error():
    provider = AsyncMock()
    storage = AsyncMock()

    original_error = RuntimeError("Unexpected failure")
    provider.generate.side_effect = original_error
    storage.load.return_value = []

    service = AssistantService(
        provider=provider,
        storage=storage,
    )

    with pytest.raises(ProviderError) as exc:
        await service.send_message("Hello")

    assert exc.value.__cause__ is original_error
    storage.save.assert_not_awaited()
