from .models import Message, Role, AssistantResponse
from .protocols import LLMProvider, ConversationStorage
from .exceptions import ProviderError
from collections.abc import AsyncIterator


class AssistantService:
    def __init__(
        self,
        provider: LLMProvider,
        storage: ConversationStorage
    ):
        self.provider = provider
        self.storage = storage

    async def send_message(self, content: str) -> AssistantResponse:
        if not content.strip():
            raise ValueError("Message cannot be empty")

        history = await self.storage.load()

        user_message = Message(
            role=Role.USER,
            content=content
        )

        messages = [*history, user_message]

        try: 
            response = await self.provider.generate(messages)
        except ProviderError:
            raise

        except Exception as error:
            raise ProviderError(
                "LLM generation failed"
            ) from error

        await self.storage.save([
            *messages,
            response.message
        ])

        return response

    
    async def stream_message(
        self,
        content: str,
    ) -> AsyncIterator[str]:

        if not content.strip():
            raise ValueError("Message cannot be empty")

        history = await self.storage.load()

        user_message = Message(
            role=Role.USER,
            content=content,
        )

        messages = [*history, user_message]

        chunks: list[str] = []

        try:
            async for chunk in self.provider.stream(messages):
                chunks.append(chunk)
                yield chunk

        except ProviderError:
            raise

        except Exception as error:
            raise ProviderError(
                "LLM streaming failed"
            ) from error

        assistant_message = Message(
            role=Role.ASSISTANT,
            content="".join(chunks),
        )

        await self.storage.save([
            *messages,
            assistant_message,
        ])
