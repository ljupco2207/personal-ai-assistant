from typing import Protocol
from .models import Message, AssistantResponse


class LLMProvider(Protocol):
    async def generate(
        self,
        messages: list[Message]
    ) -> AssistantResponse:
        ...


class ConversationStorage(Protocol):
    async def save(
        self,
        messages: list[Message]
    ) -> None:
        ...

    async def load(self) -> list[Message]:
        ...
