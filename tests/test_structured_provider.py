
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from personal_ai_assistant.capstone.anthropic_provider import (
    AnthropicProvider,
)
from personal_ai_assistant.capstone.exceptions import ProviderError
from personal_ai_assistant.capstone.models import Message, Role
from personal_ai_assistant.capstone.structured_models import IntentResult


def make_mock_provider(json_text: str, stop_reason: str = "end_turn"):
    mock_client = MagicMock()

    mock_client.messages.create = AsyncMock(
        return_value=SimpleNamespace(
            stop_reason=stop_reason,
            content=[
                SimpleNamespace(
                    type="text",
                    text=json_text,
                )
            ],
        )
    )

    return AnthropicProvider(client=mock_client), mock_client


@pytest.mark.asyncio
async def test_generate_structured_returns_validated_model():
    provider, mock_client = make_mock_provider(
        '{"intent":"reminder","task":"call John","date":"tomorrow"}'
    )

    result = await provider.generate_structured(
        messages=[
            Message(
                role=Role.USER,
                content="Remind me to call John tomorrow",
            )
        ],
        response_model=IntentResult,
    )

    assert isinstance(result, IntentResult)
    assert result.intent == "reminder"
    assert result.task == "call John"
    assert result.date == "tomorrow"

    request = mock_client.messages.create.await_args.kwargs

    assert (
        request["output_config"]["format"]["schema"]
        == IntentResult.model_json_schema()
    )


@pytest.mark.asyncio
async def test_generate_structured_rejects_invalid_json():
    provider, _ = make_mock_provider("not valid JSON")

    with pytest.raises(ProviderError):
        await provider.generate_structured(
            messages=[
                Message(role=Role.USER, content="Hello")
            ],
            response_model=IntentResult,
        )


@pytest.mark.asyncio
async def test_generate_structured_rejects_unsupported_intent():
    provider, _ = make_mock_provider(
        '{"intent":"shopping","task":"buy milk","date":null}'
    )

    with pytest.raises(ProviderError):
        await provider.generate_structured(
            messages=[
                Message(role=Role.USER, content="Buy milk")
            ],
            response_model=IntentResult,
        )


@pytest.mark.asyncio
async def test_generate_structured_rejects_incomplete_response():
    provider, _ = make_mock_provider(
        '{"intent":"reminder","task":"call John","date":"tomorrow"}',
        stop_reason="max_tokens",
    )

    with pytest.raises(ProviderError):
        await provider.generate_structured(
            messages=[
                Message(role=Role.USER, content="Remind me tomorrow")
            ],
            response_model=IntentResult,
        )


@pytest.mark.asyncio
async def test_generate_structured_sends_system_prompt():
    provider, mock_client = make_mock_provider(
        '{"intent":"general","task":"hello","date":null}'
    )

    await provider.generate_structured(
        messages=[
            Message(role=Role.SYSTEM, content="Classify the user intent."),
            Message(role=Role.USER, content="Hello"),
        ],
        response_model=IntentResult,
    )

    request = mock_client.messages.create.await_args.kwargs

    assert request["system"] == "Classify the user intent."
    assert request["messages"] == [
        {"role": "user", "content": "Hello"}
    ]
