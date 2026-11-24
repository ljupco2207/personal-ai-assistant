import anthropic
import httpx
import pytest

from unittest.mock import AsyncMock, Mock
from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.exceptions import (
    ProviderError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    ProviderConnectionError,
    ProviderServerError,
)
from personal_ai_assistant.capstone.models import Message, Role


def make_response(status_code: int) -> httpx.Response:
    request = httpx.Request(
        "POST",
        "https://api.anthropic.com/v1/messages",
    )
    return httpx.Response(
        status_code=status_code,
        request=request,
    )


@pytest.mark.parametrize(
    "sdk_error, expected_error",
    [
        (
            anthropic.AuthenticationError(
                "Invalid API key",
                response=make_response(401),
                body=None,
            ),
            ProviderAuthenticationError,
        ),
        (
            anthropic.RateLimitError(
                "Rate limit exceeded",
                response=make_response(429),
                body=None,
            ),
            ProviderRateLimitError,
        ),
        (
            anthropic.APIConnectionError(
                request=httpx.Request(
                    "POST",
                    "https://api.anthropic.com/v1/messages",
                ),
            ),
            ProviderConnectionError,
        ),
        (
            anthropic.APITimeoutError(
                request=httpx.Request(
                    "POST",
                    "https://api.anthropic.com/v1/messages",
                ),
            ),
            ProviderConnectionError,
        ),
        (
            anthropic.InternalServerError(
                "Server unavailable",
                response=make_response(500),
                body=None,
            ),
            ProviderServerError,
        ),
        (
            anthropic.BadRequestError(
                "Invalid request",
                response=make_response(400),
                body=None,
            ),
            ProviderError,
        ),
        (
            anthropic.PermissionDeniedError(
                "Permission denied",
                response=make_response(403),
                body=None,
            ),
            ProviderError,
        ),
    ],
)
@pytest.mark.asyncio
async def test_anthropic_error_mapping(
    sdk_error,
    expected_error,
):
    client = Mock()
    client.messages.create = AsyncMock(
        side_effect=sdk_error
    )

    provider = AnthropicProvider(client=client)

    messages = [
        Message(
            role=Role.USER,
            content="Hello",
        )
    ]

    with pytest.raises(expected_error) as exc_info:
        await provider.generate(messages)

    assert exc_info.value.__cause__ is sdk_error
    client.messages.create.assert_awaited_once()
