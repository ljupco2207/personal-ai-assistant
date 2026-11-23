from .models import Message, Role, AssistantResponse
from .protocols import LLMProvider, ConversationStorage


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

        response = await self.provider.generate(messages)

        await self.storage.save([
            *messages,
            response.message
        ])

        return response