
import pytest

from personal_ai_assistant.capstone.exceptions import ProviderError
from personal_ai_assistant.capstone.intent_classifier import IntentClassifier
from personal_ai_assistant.capstone.models import Message, Role
from personal_ai_assistant.capstone.structured_models import IntentResult


class MockStructuredLLMProvider:
    def __init__(self, result: IntentResult):
        self.result = result
        self.received_messages = None
        self.received_model = None
        self.call_count = 0

    async def generate_structured(
        self,
        messages: list[Message],
        response_model: type[IntentResult],
    ) -> IntentResult:
        self.call_count += 1
        self.received_messages = messages
        self.received_model = response_model

        return self.result


@pytest.mark.asyncio
async def test_classifier_returns_valid_intent():
    expected = IntentResult(
        intent="reminder",
        task="call John",
        date="tomorrow",
    )

    provider = MockStructuredLLMProvider(result=expected)
    classifier = IntentClassifier(provider=provider)

    result = await classifier.classify(
        "Remind me to call John tomorrow."
    )

    assert result == expected
    assert result.intent == "reminder"
    assert result.task == "call John"
    assert result.date == "tomorrow"

    assert provider.received_model is IntentResult
    assert provider.call_count == 1


@pytest.mark.asyncio
async def test_classify_rejects_empty_message():
    provider = MockStructuredLLMProvider(
        result=IntentResult(
            intent="general",
            task="hello",
            date=None,
        )
    )

    classifier = IntentClassifier(provider=provider)

    with pytest.raises(
        ValueError,
        match="User message cannot be empty",
    ):
        await classifier.classify("   ")

    assert provider.received_messages is None
    assert provider.call_count == 0


@pytest.mark.asyncio
async def test_classify_sends_correct_messages():
    provider = MockStructuredLLMProvider(
        result=IntentResult(
            intent="reminder",
            task="call John",
            date="tomorrow",
        )
    )

    classifier = IntentClassifier(provider=provider)

    await classifier.classify(
        "Remind me to call John tomorrow"
    )

    messages = provider.received_messages

    assert len(messages) == 2

    assert messages[0].role == Role.SYSTEM
    assert messages[1].role == Role.USER

    assert (
        messages[1].content
        == "Remind me to call John tomorrow"
    )

    assert provider.received_model is IntentResult


@pytest.mark.asyncio
async def test_classifier_sends_system_and_user_messages():
    provider = MockStructuredLLMProvider(
        result=IntentResult(
            intent="general",
            task="Explain Python decorators",
            date=None,
        )
    )

    classifier = IntentClassifier(provider=provider)

    await classifier.classify("Explain Python decorators")

    messages = provider.received_messages

    assert len(messages) == 2

    assert messages[0].role == Role.SYSTEM
    assert messages[0].content.strip() != ""

    assert messages[1].role == Role.USER
    assert messages[1].content == "Explain Python decorators"

    assert provider.call_count == 1


@pytest.mark.asyncio
async def test_classifier_propagates_provider_error():
    class FailingProvider:
        async def generate_structured(
            self,
            messages,
            response_model,
        ):
            raise ProviderError("Structured generation failed")

    classifier = IntentClassifier(
        provider=FailingProvider()
    )

    with pytest.raises(
        ProviderError,
        match="Structured generation failed",
    ):
        await classifier.classify("Remind me tomorrow")
