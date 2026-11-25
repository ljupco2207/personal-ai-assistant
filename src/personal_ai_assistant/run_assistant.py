import asyncio
import os

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from personal_ai_assistant.capstone.anthropic_provider import AnthropicProvider
from personal_ai_assistant.capstone.service import AssistantService
from personal_ai_assistant.capstone.storage import JSONConversationStorage
from personal_ai_assistant.capstone.prompts import PYTHON_TUTOR_SYSTEM_PROMPT
from personal_ai_assistant.capstone.models import (
    Message,
    Role
)


async def main() -> None:
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is missing")

    async with AsyncAnthropic(api_key=api_key) as client:
        provider = AnthropicProvider(client=client)

        storage = JSONConversationStorage(
            "data/conversation.json"
        )

        service = AssistantService(
            provider=provider,
            storage=storage,
            system_prompt=PYTHON_TUTOR_SYSTEM_PROMPT
        )

        existing_messages = await storage.load()

        if not existing_messages:
            await storage.save([
                Message(
                    role=Role.SYSTEM,
                    content=PYTHON_TUTOR_SYSTEM_PROMPT
                )
            ])

        response = await service.send_message(
            "Explain Python decorators."
        )

        print("Claude:", response.message.content)


if __name__ == "__main__":
    asyncio.run(main())
