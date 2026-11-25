from typing import Protocol
from .models import Message, AssistantResponse
from collections.abc import AsyncIterator
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class StructuredLLMProvider(Protocol):
    async def generate_structured(
        self,
        messages: list[Message],
        response_model: type[T],
    ) -> T:
        ...

class LLMProvider(Protocol):

    async def generate(
        self,
        messages: list[Message],
    ) -> AssistantResponse:
        ...

    def stream(
        self,
        messages: list[Message],
    ) -> AsyncIterator[str]:
        ...

class ConversationStorage(Protocol):
    async def save(
        self,
        messages: list[Message]
    ) -> None:
        ...

    async def load(self) -> list[Message]:
        ...
