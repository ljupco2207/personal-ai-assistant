from pydantic import ValidationError

from personal_ai_assistant.capstone.json_utils import (
    strip_json_code_fence,
)
from personal_ai_assistant.capstone.models import Message, Role
from personal_ai_assistant.capstone.protocols import (
    LLMProvider,
    StructuredLLMProvider
)
from personal_ai_assistant.capstone.structured_models import (
    IntentResult,
)
from personal_ai_assistant.capstone.prompts import (
    INTENT_CLASSIFIER_SYSTEM_PROMPT,
)


class IntentClassificationError(Exception):
    pass


class IntentClassifier:
    def __init__(self, provider: LLMProvider):
        self._provider = provider

    async def classify(self, user_message: str) -> IntentResult:
        if not user_message.strip():
            raise ValueError("User message cannot be empty")

        messages = [
            Message(
                role=Role.SYSTEM,
                content=INTENT_CLASSIFIER_SYSTEM_PROMPT,
            ),
            Message(
                role=Role.USER,
                content=user_message,
            ),
        ]

        return await self._provider.generate_structured(
            messages=messages,
            response_model=IntentResult,
        )